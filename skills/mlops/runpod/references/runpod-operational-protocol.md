# RunPod Operational Protocol

Use this before, during, and after every RunPod session. Goal: spend-aware GPU work with preserved evidence and no accidental credit burn.

## 0. Core rules

1. **No blind pod spend**: before creating a pod, record starting balance if the user provides it or if the console/API exposes it.
2. **Pods are temporary unless explicitly declared persistent**: default action after artifact sync is terminate and verify zero pods.
3. **Archive before retry**: any failed, tiny, partial, or malformed output must be moved/copied to `FAILED_OUTPUTS/<timestamp>/` before rerun or overwrite.
4. **Artifacts first**: copy inputs to persistent workspace before model install/download; sync outputs back to local ANDROMALIUS before termination.
5. **Proof over claim**: final report must include pod count, output paths, file sizes, and termination verification.
6. **Never print API keys**: check config/permissions without echoing secrets.

## 1. Session ledger format

Create or update a local ledger file in the project workspace before pod creation:

```md
# RunPod Session Ledger — <YYYY-MM-DD HH:MM UTC>

## Intent
- Task:
- User-approved scope:
- Starting balance: $<amount or unknown>
- Max spend / stop condition:

## Pod plan
- Pod name:
- GPU:
- Expected $/hr:
- Expected runtime:
- Expected max cost:
- Image:
- Model:
- Storage:

## Runtime events
| UTC time | Event | Pod ID | Cost/hr | Notes |
|---|---|---|---:|---|

## Artifacts
| Path | Size | Status |
|---|---:|---|

## Shutdown proof
- Terminated pod IDs:
- `runpod.get_pods()` remaining count:
- Final balance if known:
- Estimated spend:
```

## 2. Preflight checklist

Run all before pod creation:

- Confirm `~/.runpod/config.toml` exists and is mode `600`.
- Confirm key permissions are sufficient for the needed action.
- Confirm `runpod.get_pods()` count and list pod names/costs without secrets.
- If existing pods are running, decide: reuse, stop, or terminate. Do not create duplicates blindly.
- Record starting balance if user provides it.
- Compute rough expected spend: `cost_per_hour * expected_minutes / 60`.
- Confirm local artifact directory exists, e.g. `/root/MW_CENTRAL/TRIANGULUM/HELIOS/NYX/RUNPOD_SESSIONS/<session-id>/` or task-specific folder.

## 3. Pod creation protocol

Preferred approach:

1. Create minimal SSH-accessible pod first when startup command is uncertain.
2. Verify SSH and GPU:
   ```bash
   ssh <host> "echo SSH_OK && nvidia-smi --query-gpu=name,memory.total,memory.free --format=csv,noheader && df -h /workspace /runpod-volume / 2>/dev/null || df -h /"
   ```
3. Copy inputs to `/runpod-volume/<session>/inputs/` before heavy installs.
4. Install/model-load after SSH is proven.
5. Use `nohup` logs under `/runpod-volume/<session>/logs/`.

Avoid embedding long startup commands in pod creation unless already proven; failed startup may delay port assignment while credits burn.

## 4. Generation/output protocol

Before every rerun:

```bash
mkdir -p FAILED_OUTPUTS/$(date -u +%Y%m%dT%H%M%SZ)
# Move any invalid prior outputs into that folder before overwriting.
```

Validation gates:

- Each expected output exists.
- Each output has a sane size threshold for task type.
- If generated text is unexpectedly tiny, empty, repetitive, or warning-tagged, mark failed and archive it.
- Sync good and failed outputs back locally.

## 5. Shutdown protocol

Always do these before final answer unless user explicitly says keep pod alive:

1. Sync `/runpod-volume/<session>/outputs/`, logs, and scripts back to local workspace.
2. Create a local archive package.
3. Terminate all pods created for the session.
4. Verify `runpod.get_pods()` returns zero or only intentionally retained pods.
5. Record final pod count and estimated spend in ledger.

## 6. Required final report format

```md
## RunPod result
- Starting balance: $...
- Ending balance: $... / unavailable
- Estimated spend: $...
- Pods created: <ids/names>
- Pods remaining: <count>
- Shutdown status: verified / not verified

## Outputs
- `<path>` — <bytes>

## Failures preserved
- `<FAILED_OUTPUTS/path>` — <bytes>

## Notes
- What model actually ran:
- What failed and why:
- What not proven:
```

## 7. Known failure handling

- **70B OOM on A40**: full/unquantized 70B may fail. Use quantized model, smaller model, or larger GPU.
- **vLLM FlashInfer/Ninja compile failure**: bypass vLLM with direct Transformers or use a vLLM image/version known to work.
- **Tiny output after max-context warning**: input exceeded context. Archive tiny files, rerun with smaller prompt/context window.
- **Port never assigned**: terminate quickly, create minimal SSH pod, then install manually.
