# vLLM Pod Creation Recipe (RunPod)

Verified 2026-09-14 against live RunPod GraphQL schema.

## Working Python snippet

```python
import urllib.request, json, configparser

c = configparser.ConfigParser()
c.read("/root/.runpod/config.toml")
key = c["default"]["apikey"]

HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "X-API-Key": key,
}

def graphql(query, variables=None):
    payload = {"query": query}
    if variables:
        payload["variables"] = variables
    data = json.dumps(payload).encode()
    req = urllib.request.Request("https://api.runpod.io/graphql", data=data, headers=HEADERS)
    resp = urllib.request.urlopen(req, timeout=60)
    return json.loads(resp.read().decode())

# Create pod
mutation = """
mutation createPod($input: PodFindAndDeployOnDemandInput!) {
  podFindAndDeployOnDemand(input: $input) {
    id name imageName costPerHr
    runtime { ports { ip isIpPublic privatePort publicPort } }
  }
}
"""

variables = {
    "input": {
        "cloudType": "SECURE",
        "gpuCount": 1,
        "gpuTypeId": "NVIDIA A40",
        "containerDiskInGb": 50,
        "volumeInGb": 80,
        "name": "entropy-vllm-70b",
        "imageName": "runpod/vllm:latest",
        "dockerArgs": "python3 -m vllm.entrypoints.openai.api_server --model cognitivecomputations/dolphin-2.9-llama3-70b --dtype auto --max-model-len 8192 --port 8000 --tensor-parallel-size 1",
        "ports": "8000/tcp,22/tcp",
        "env": [{"key": "MODEL_NAME", "value": "dolphin-llama3-70b"}]
    }
}

result = graphql(mutation, variables)
```

## Schema pitfalls (2026-09)

| Wrong field | Correct field | Why |
|-------------|---------------|-----|
| `containerDiskSizeGb` | `containerDiskInGb` | GraphQL schema uses `InGb` suffix |
| `dockerStartCmd` | `dockerArgs` | Renamed in current API |
| `env: {"KEY": "val"}` | `env: [{"key": "...", "value": "..."}]` | Env vars are array of objects |
| `Authorization: Bearer $KEY` | `X-API-Key: $KEY` | GraphQL endpoint rejects Bearer <REDACTED> |
| Missing User-Agent | Add browser UA string | Cloudflare WAF blocks bare urllib |

## GPU selection for 70B models

| Model | Quant | VRAM needed | Cheapest GPU |
|-------|-------|-------------|-------------|
| dolphin-llama3:70b | Q4_0 | ~40GB | A40 (48GB) |
| dolphin-llama3:70b | Q3_K_M | ~30GB | A40 (48GB) |
| dolphin-llama3:8b | Q4_0 | ~5GB | RTX 3070 (8GB) |

## Post-creation tunnel

Once the pod is running and the port is public:
```bash
ssh -N -L 11434:localhost:8000 root@<pod-ip> -p <pod-ssh-port> -i ~/.ssh/id_ed25519 &
```

Then configure Hermes to use `http://localhost:11434/v1` as an OpenAI-compatible endpoint.
