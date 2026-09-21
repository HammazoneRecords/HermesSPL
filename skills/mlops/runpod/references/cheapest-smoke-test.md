# RunPod Cheapest Smoke Test

Use this to prove the RunPod operational protocol before spending on model runs.

## Purpose

This is a cockpit/protocol test, not a model-quality test. It proves: ledger, balance recording, pod creation, SSH, artifact sync, failed-output preservation, termination, and shutdown proof.

## Cheapest safe shape

- Use the cheapest practical SSH-capable GPU pod available.
- Runtime target: under 10 minutes.
- Max spend target: under `$0.10` where possible.
- No model download.
- No vLLM.
- No HuggingFace dependency.
- Workload: shell/Python only.

## Required folder structure

```text
/root/MW_CENTRAL/TRIANGULUM/HELIOS/NYX/RUNPOD_PROTOCOLS/SMOKE_TESTS/<session-id>/
  ledger.md
  inputs/
  outputs/
  FAILED_OUTPUTS/
  logs/
  proof/
```

## Workload

Remote script writes:

1. `outputs/hello-runpod.txt`
2. `outputs/system-proof.json` with UTC timestamp, hostname, GPU name, memory, and disk info.
3. `FAILED_OUTPUTS/<timestamp>/intentional-failure.txt` to prove failed-output preservation.

## Pass criteria

Pass only if:

- Ledger exists before pod creation.
- Starting balance is recorded or marked unavailable.
- Pod ID and cost/hr are recorded.
- SSH verification is saved.
- Good output is synced locally.
- Intentional failed output is preserved locally.
- Pod is terminated.
- Remaining pod count is verified.
- Final local archive exists.

## Escalation rule

Do not run expensive model sessions until this smoke test passes. After pass, stage upward:

1. small GPU + no-model protocol test
2. small GPU + tiny model API test
3. medium GPU + 8B/14B vLLM test
4. large GPU + quantized 70B test
