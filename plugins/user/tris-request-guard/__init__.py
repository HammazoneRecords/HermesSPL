"""TRISMIGISTUS live Hermes request guard plugin.

This plugin is project-local proof glue: it runs inside Hermes' plugin system,
around the real provider execution path, without editing Hermes core.
"""
from __future__ import annotations

import json
import logging
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict

ROOT = Path("/root/MW_CENTRAL/TRIANGULUM/HELIOS/NYX")
GUARD_DIR = ROOT / ".hermes" / "model_guard"
LOG = ROOT / ".hermes" / "plans" / "proof" / "tris_request_guard_plugin_events.jsonl"
if str(GUARD_DIR) not in sys.path:
    sys.path.insert(0, str(GUARD_DIR))

from tris_model_guard import TrisModelGuard  # type: ignore  # noqa: E402
from tris_model_router import TrisModelRouter  # type: ignore  # noqa: E402
from rate_limit_pacer import RateLimitPacer  # type: ignore  # noqa: E402

logger = logging.getLogger(__name__)
_ACTIVE: Dict[str, Dict[str, Any]] = {}


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _append(entry: Dict[str, Any]) -> None:
    LOG.parent.mkdir(parents=True, exist_ok=True)
    entry.setdefault("created_utc", _now())
    with LOG.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry, ensure_ascii=False, sort_keys=True, default=str) + "\n")


def _lock_profile(session_id: str, provider: str, model: str, api_request_id: str) -> str:
    tail = (api_request_id or session_id or "unknown").split(":", 1)[0]
    safe_model = model.replace("/", "_").replace(":", "_")[:40]
    return f"plugin_live__{tail}__{provider}__{safe_model}"


def _preflight(*, session_id: str, provider: str, model: str, api_request_id: str, platform: str, api_mode: str) -> Dict[str, Any]:
    router = TrisModelRouter()
    guard = TrisModelGuard()
    pacer = RateLimitPacer()
    lock_id = _lock_profile(session_id, provider, model, api_request_id)
    try:
        candidates = router.best_for("reasoning")[:5]
        before = pacer.peek(provider, model) if provider and model else None
        release_first = guard.release(lock_id, session_id=session_id)
        acquired = guard.acquire(lock_id, provider=provider, model=model, role="plugin-live-request", session_id=session_id)
        paced = pacer.acquire_paced(lock_id, provider, model, max_wait_seconds=5) if provider and model else {"allowed": False, "reason": "missing_provider_or_model"}
        after = pacer.peek(provider, model) if provider and model else None
        receipt = {
            "event": "llm_execution:before_next_call",
            "phase": "before_provider_dispatch",
            "session_id": session_id,
            "platform": platform,
            "provider": provider,
            "model": model,
            "api_mode": api_mode,
            "api_request_id": api_request_id,
            "lock_profile": lock_id,
            "router_candidates": candidates,
            "guard_pre_release": release_first,
            "guard_acquire": acquired,
            "pacer_before": before,
            "pacer_acquire": paced,
            "pacer_after": after,
            "source": "tris-request-guard-plugin",
        }
        _append(receipt)
        if isinstance(acquired, dict) and acquired.get("error"):
            raise RuntimeError(f"TRISMIGISTUS guard denied model lock: {acquired}")
        if not paced.get("allowed"):
            raise RuntimeError(f"TRISMIGISTUS pacer denied provider call: {paced}")
        _ACTIVE[api_request_id] = {"lock_profile": lock_id, "session_id": session_id, "provider": provider, "model": model}
        return receipt
    finally:
        router.close()
        guard.close()
        pacer.close()


def _release(api_request_id: str, *, reason: str, extra: Dict[str, Any] | None = None) -> None:
    active = _ACTIVE.pop(api_request_id, None)
    if not active:
        return
    guard = TrisModelGuard()
    try:
        released = guard.release(active["lock_profile"], session_id=active["session_id"])
        _append({
            "event": reason,
            "phase": "after_provider_response_or_error",
            "api_request_id": api_request_id,
            "lock_profile": active["lock_profile"],
            "session_id": active["session_id"],
            "provider": active["provider"],
            "model": active["model"],
            "guard_release": released,
            "extra": extra or {},
            "source": "tris-request-guard-plugin",
        })
    finally:
        guard.close()


def _on_llm_execution(*, request: Dict[str, Any], next_call, session_id: str = "", platform: str = "", provider: str = "", model: str = "", api_mode: str = "", api_request_id: str = "", **_: Any) -> Any:
    _preflight(session_id=session_id, provider=provider, model=model, api_request_id=api_request_id, platform=platform, api_mode=api_mode)
    try:
        return next_call(request)
    except BaseException as exc:
        _release(api_request_id, reason="llm_execution:error_release", extra={"error_type": type(exc).__name__, "error": str(exc)[:500]})
        raise


def _on_post_api_request(*, api_request_id: str = "", finish_reason: str = "", response_model: str = "", api_duration: float = 0.0, usage: Any = None, **_: Any) -> None:
    _release(api_request_id, reason="post_api_request:success_release", extra={"finish_reason": finish_reason, "response_model": response_model, "api_duration": api_duration, "usage_present": bool(usage)})


def _on_api_request_error(*, api_request_id: str = "", error: Any = None, status_code: Any = None, reason: str = "", **_: Any) -> None:
    _release(api_request_id, reason="api_request_error:release", extra={"error": error, "status_code": status_code, "reason": reason})


def register(ctx) -> None:
    ctx.register_middleware("llm_execution", _on_llm_execution)
    ctx.register_hook("post_api_request", _on_post_api_request)
    ctx.register_hook("api_request_error", _on_api_request_error)
    logger.info("tris-request-guard plugin registered llm_execution/post_api_request/api_request_error")
