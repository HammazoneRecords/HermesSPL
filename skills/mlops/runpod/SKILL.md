---
name: runpod
description: Use when working with the RunPod cloud GPU platform.
---

# RunPod

## Mandatory operational protocol

Before any RunPod action that can create, keep, or spend on pods, open and follow `references/runpod-operational-protocol.md`. For first-time or changed flows, run `references/cheapest-smoke-test.md` before expensive model work. Create/update a session ledger from `templates/runpod-session-ledger.md` in the project workspace. Preserve failed outputs before reruns, sync artifacts locally before shutdown, terminate pods unless explicitly kept alive, and verify remaining pod count before final reporting.

## Auth / key storage

Store the API key (prefix `rpa_`) in `~/.runpod/config.toml`, mode 600:

```toml
[default]
apikey = "rpa_..."
```

The Python `runpod` SDK reads this file at import time — it fails with `KeyError: 'api_key'` if the file is missing or malformed. The SDK does NOT read the `RUNPOD_API_KEY` env var. For direct HTTP calls (curl/Python urllib), use the `X-API-Key` header — `Authorization: Bearer <REDACTED>` gets a 401 on the GraphQL endpoint.

## Verify a key (GraphQL)

```python
import urllib.request, json

key = open("/root/.runpod/config.toml")  # parse with configparser
headers = {
    "Content-Type": "application/json",
    "X-API-Key": key,  # NOT "Authorization: Bearer"
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",  # Cloudflare blocks bare urllib
}
req = urllib.request.Request(
    "https://api.runpod.io/graphql",
    data=json.dumps({"query": "query { gpuTypes { id displayName memoryInGb } }"}).encode(),
    headers=headers
)
resp = urllib.request.urlopen(req, timeout=30)
```

Returns GPU types — confirms the key is live before doing any pod work.

## Pod creation (GraphQL mutation)

```graphql
mutation createPod($input: PodFindAndDeployOnDemandInput!) {
  podFindAndDeployOnDemand(input: $input) {
    id name imageName costPerHr
    runtime { ports { ip isIpPublic privatePort publicPort } }
  }
}
```

Key field names (verified against live schema 2026-09):
- `containerDiskInGb` (NOT `containerDiskSizeGb`)
- `dockerArgs` (NOT `dockerStartCmd`)
- `env` is `[{key: "...", value: "..."}]` (NOT a dict)
- `gpuTypeId` is the display name e.g. `"NVIDIA A40"` (NOT the id field)

## Pitfalls

- Config dir is dot-prefixed `~/.runpod/` — create the parent before writing `config.toml`.
- `chmod 600` the config file: it holds a secret.
- **Cloudflare Error 1010 (Access denied)**: the API sits behind Cloudflare WAF which blocks bare Python urllib. Always send a browser-like `User-Agent` header.
- **"Create API Key" vs full key**: RunPod console generates limited-scope keys by default. A key with only "Create" permission can read `gpuTypes` but gets `UNAUTHORIZED` on `podFindAndDeployOnDemand`. Generate a full-access key from console → Account → API Keys for pod creation.
- **Python SDK import crash**: `import runpod` reads credentials at import time and crashes with `KeyError: 'api_key'` if `~/.runpod/config.toml` is missing or the `[default]` section has no `apikey`. Fix: ensure the file exists and is valid TOML before importing. If the SDK still fails, bypass it — use `urllib.request` with `X-API-Key` header directly.
- **GPU VRAM for 70B Q4**: dolphin-llama3:70b Q4 needs ~40GB VRAM. A40 (48GB) is the cheapest match. RTX 4090/5090 (24GB) are too small unless you use a smaller quant (Q3/Q2).
- **Archive failed generations before retrying**: when a model run creates tiny/invalid outputs, immediately move them to `FAILED_OUTPUTS/<timestamp>/` before rerunning. Do not overwrite them; even bad generations can be manually repaired or used as debugging evidence.

## vLLM pod recipe

For creating a pod that serves an uncensored model via vLLM (OpenAI-compatible API), see `references/vllm-pod-recipe.md` for the verified GraphQL mutation, schema pitfalls, and GPU selection table.
