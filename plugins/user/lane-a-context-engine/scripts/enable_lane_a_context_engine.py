import logging
from pathlib import Path
from tools.terminal import terminal

logger = logging.getLogger(__name__)


def enable_lane_a_context_engine():
    """Enable the lane-a-engine context engine via direct config edit."""
    cfg_path = Path.home() / "AppData/Local/hermes/config.yaml"
    if not cfg_path.exists():
        return {"error": f"config.yaml not found at {cfg_path}"}

    import yaml
    try:
        original = cfg_path.read_text(encoding="utf-8")
        doc = yaml.safe_load(original)
    except Exception as e:
        return {"error": f"failed to parse config.yaml: {e!r}"}

    doc.setdefault("context", {})
    doc["context"]["engine"] = "lane-a-engine"
    doc["context"].setdefault("lane_a", {})
    doc["context"]["lane_a"]["notifications"] = {
        "enabled": True,
        "thresholds": [
            {"ratio": 0.50, "message": "Context at 50% — transient notification"},
            {"ratio": 0.60, "message": "Context at 60% — transient notification"},
        ],
        "style": "transient",
    }
    doc["context"]["lane_a"]["db"] = {
        "enabled": True,
        "table": "lane_a_summaries",
        "path": "~/.hermes/state.db",
    }

    new_text = yaml.dump(doc, default_flow_style=False, sort_keys=False)
    cfg_path.write_text(new_text, encoding="utf-8")
    return {"ok": True, "config_path": str(cfg_path)}


if __name__ == "__main__":
    print(enable_lane_a_context_engine())
