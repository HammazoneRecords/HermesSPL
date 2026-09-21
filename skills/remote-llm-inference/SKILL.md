---
name: remote-llm-inference
description: "Deploy Ollama on a remote GPU VPS via SSH tunnel for Hermes."
version: 0.1.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [remote-llm, vps, ollama, gpu-inference, ssh-tunnel, uncensored-model]
    related_skills: [local-llm-deployment]
---

# Remote LLM Inference

Deploy Ollama on a remote GPU VPS and expose it to local Hermes Agent via an SSH tunnel. The VPS runs the model; prompts travel over SSH; responses return through the tunnel. Suitable when local hardware lacks a GPU, when you need a dedicated inference host, or when deploying uncensored models that shouldn't touch your local machine.

**Not a Faraday cage** — prompts leave your local machine over the SSH tunnel. Do NOT use for PII or sensitive data unless the VPS is fully trusted.

## When to Use

- Local machine has no GPU but a remote VPS has one (NVIDIA A40, A100, etc.)
- Deploying uncensored models for a specific workload (e.g., Jhanos gates) where you want isolation from local inference
- Need more VRAM or CPU than local hardware provides
- VPS is a dedicated inference host (RunPod, Vast.ai, Hetzner, etc.)

**Don't use for:** PII/sensitive data (unless VPS is in your trust boundary), low-latency interactive workloads (SSH adds ~10-50ms per call), or when the VPS is unreliable (RunPod containers restart without warning).

## Architecture

```
Local Machine                    VPS (GPU Server)
┌──────────────┐   SSH Tunnel    ┌──────────────────┐
│ Hermes Agent │───localhost:11434──▶│ Ollama :11434    │
│ (or script)  │                   │ + model weights   │
└──────────────┘                   └──────────────────┘
```

## Prerequisites

- SSH access to the VPS (key-based, not password)
- VPS has a GPU with sufficient VRAM for the target model
- Internet access on VPS for Ollama install + model pull
- Hermes Agent running locally

## Procedure

### Step 1 — Generate SSH Key & Configure

```bash
ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519 -N '' -C 'hermes-agent-vps'
```

Add the public key to the VPS `~/.ssh/authorized_keys`. If the VPS is a container that restarts (e.g., RunPod), you must re-add the key after each restart.

Configure `~/.ssh/config`:

```
Host vps-llm
    HostName <VPS_IP>
    Port <SSH_PORT>
    User root
    IdentityFile ~/.ssh/id_ed25519
    StrictHostKeyChecking yes
```

**Pitfall — stale ControlMaster socket blocks new connections.** If you get `Permission denied` on a host that previously worked, check for stale sockets in `~/.ssh/sockets/` and remove them, or use `ssh -S none vps-llm` to bypass control multiplexing.

### Step 2 — Probe VPS Hardware

```bash
ssh vps-llm "nproc; free -h | grep Mem; nvidia-smi --query-gpu=name,memory.total --format=csv,noheader; df -h /; df -h /workspace 2>/dev/null || echo NO_WORKSPACE"
```

Size the model to the hardware:

| VRAM | Max model (Q4_K_M) | Notes |
|------|---------------------|-------|
| 8 GB | 7B | llama3:8b, mistral:7b, dolphin-llama3:8b |
| 24 GB | 13B-34B | llama3:70b too large; qwen2.5:14b, mythalion:13b |
| 46 GB (A40) | 70B | dolphin-llama3:70b, llama3:70b |
| 80 GB (A100) | 70B+ with room |

### Step 3 — Install Ollama on VPS

```bash
ssh vps-llm "apt-get update -qq && apt-get install -y -qq zstd && curl -fsSL https://ollama.com/install.sh | sh"
```

Pitfall — VPS root overlay is often small (20 GB on RunPod).** Ollama's default `~/.ollama` fills the root partition on large model pulls. Redirect before starting:

```bash
ssh vps-llm "export OLLAMA_MODELS=/workspace/.ollama/models; export TMPDIR=/workspace/tmp; mkdir -p \$OLLAMA_MODELS \$TMPDIR"
```

Pitfall — `ollama pull` started with `&` over SSH dies when the SSH session disconnects (even with `nohup`). Symptom: pull reaches ~90% then vanishes. Fix: run pulls inside a tmux session:

```bash
ssh vps-llm "tmux new-session -d -s pull 'export OLLAMA_MODELS=/workspace/.ollama/models; export TMPDIR=/workspace/tmp; ollama pull <model-name> 2>&1 | tee /workspace/pull.log; sleep 3600'"
```

The tmux session survives SSH disconnect; poll with `tmux list-sessions` and `tail -f /workspace/pull.log`.

If `/workspace` doesn't exist, check for other large mounts (`df -h`) or use `/tmp` if sufficient RAM exists.

### Step 4 — Start Ollama Daemon

VPS containers usually lack systemd. Use `setsid` to fully detach:

```bash
ssh vps-llm "pkill -9 -f ollama 2>/dev/null; sleep 2; export OLLAMA_MODELS=/workspace/.ollama/models; export TMPDIR=/workspace/tmp; setsid /usr/local/bin/ollama serve > /workspace/ollama.log 2>&1 < /dev/null & echo PID=\$!; sleep 5; curl -s http://localhost:11434/api/version"
```

**Pitfall — `nohup` + `&` over SSH can hang or get killed when the SSH session closes.** `setsid` with `< /dev/null` is more reliable for long-running daemons.

### Step 5 — Pull Model

```bash
ssh vps-llm "export OLLAMA_MODELS=/workspace/.ollama/models; export TMPDIR=/workspace/tmp; ollama pull dolphin-llama3:8b"
```

For uncensored models: `dolphin-llama3:8b`, `dolphin-llama3:70b`, `dolphin-mixtral:8x7b`, `wizardlm-2:8x22b`.

### Step 5a — Verify role claims before handoff

After loading multiple models for a role-specific handoff, verify three separate facts and record them in the handoff/runbook:

1. **Loaded:** `curl http://localhost:11434/api/tags` shows the exact model name, family, parameter size, and quantization.
2. **Responds:** run a deterministic JSON probe through `http://localhost:11434/api/generate` with `stream:false`, `format:"json"`, and `temperature:0`.
3. **Role label:** source-check uncensored or safety-alignment claims against the model card/provider page before saying a model is suitable for an uncensored or entropy role.

Do not label every open-weight local model as fully uncensored. Treat aligned base families such as Gemma as useful architecture/style contrast unless a source and live probe justify the uncensored role. For Jhanos-style entropy work, bind the uncensored role to the model whose source explicitly says it is uncensored and whose live probe passes; keep Gemma-like models as contrast unless verified otherwise.

### Step 6 — Create SSH Tunnel

**Pitfall — `curl localhost:11434` run over SSH proves the daemon is alive on the VPS, not that it is reachable from the local machine.** The probe executes on the VPS against its own loopback. Check the actual bind address before assuming the tunnel topology:

```bash
ssh vps-llm "ss -tlnp | grep 11434"
```

`127.0.0.1:11434` = loopback-only — the ONLY route from the local machine is an SSH tunnel, and any public port is closed regardless of nginx. `0.0.0.0:11434` = the port may be reachable directly; still confirm the firewall allows it before skipping the tunnel.

Open a persistent tunnel that forks cleanly and survives idle periods:

```bash
ssh -o ConnectTimeout=8 -o ExitOnForwardFailure=yes \
    -o ServerAliveInterval=30 -o ServerAliveCountMax=3 \
    -N -f -L 11434:127.0.0.1:11434 vps-llm
```

`-f` forks to background (no PID printed — find it with `pgrep -f 'ssh.*11434'`); `ExitOnForwardFailure=yes` makes ssh fail fast if the forward can't bind instead of lingering alive with a dead tunnel; `ServerAliveInterval`/`ServerAliveCountMax` keep the tunnel up through idle periods.

Verify (the same port also serves OpenAI-compatible `/v1/chat/completions`):

```bash
python3 -c "import urllib.request,json; print(json.loads(urllib.request.urlopen('http://localhost:11434/api/version').read()))"
curl -s http://localhost:11434/v1/chat/completions -d '{"model":"<name>","messages":[{"role":"user","content":"Say ok"}]}'
```

### Step 7 — Wire to Hermes

Add a model alias to `~/.hermes/config.yaml`:

```yaml
model:
  aliases:
    vps-llm:
      model: dolphin-llama3:8b
      provider: custom
      base_url: http://localhost:11434/v1
```

Usage:

```bash
hermes chat -q "Your prompt" --model vps-llm
```

Or hit the API directly from any local script:

```python
import urllib.request, json
payload = json.dumps({"model":"dolphin-llama3:8b","prompt":"...","stream":False}).encode()
req = urllib.request.Request("http://localhost:11434/api/generate", data=payload, headers={"Content-Type":"application/json"})
```

### Step 8 — Deploy Custom Modelfile (System Prompt)

To give a VPS Ollama model a custom system prompt (e.g., for a specialized role like the entropy model), create a Modelfile and push it to the VPS:

```bash
# Create Modelfile locally (see example below)
# Then push to VPS and create the model
scp EntropyModel.Modelfile vps-llm:/workspace/Modelfiles/entropy.Modelfile
ssh vps-llm "export OLLAMA_MODELS=/workspace/.ollama/models; ollama create entropy-model -f /workspace/Modelfiles/entropy.Modelfile"
```

**Modelfile structure:**

```
FROM dolphin-llama3:70b

PARAMETER temperature 0.7
PARAMETER top_p 0.92
PARAMETER num_ctx 8192

SYSTEM """You are the Entropy Model. Your system prompt goes here...
"""
```

**Pitfall — `ollama create` over SSH dies with the session.** Run inside tmux on the VPS:

```bash
ssh vps-llm "tmux new-session -d -s create-model 'export OLLAMA_MODELS=/workspace/.ollama/models; ollama create entropy-model -f /workspace/Modelfiles/entropy.Modelfile 2>&1 | tee /workspace/create-model.log; sleep 3600'"
```

Verify: `ollama list` shows the new model name. Test: `curl http://localhost:11434/api/generate -d '{"model":"entropy-model","prompt":"Say OK","stream":false}'`.

**Pitfall — tunnel must be alive to test locally.** If `curl localhost:11434` returns "Connection refused", the SSH tunnel is dead even if the SSH process exists. Restart: `ssh -N -f -L 11434:127.0.0.1:11434 vps-llm`.

## Recovery Patterns

### VPS container restarted (RunPod, etc.)

1. Port may change — re-check RunPod console for new SSH port
2. SSH key must be re-added to `~/.ssh/authorized_keys` via web terminal
3. Ollama must be reinstalled (new container = fresh filesystem)
4. Model must be re-pulled (or use a persistent mount for `OLLAMA_MODELS`)
5. Tunnel must be re-established

### Tunnel died silently

```bash
pgrep -f 'ssh.*11434.*vps-llm'  # check if alive
ssh -N -L 11434:127.0.0.1:11434 vps-llm > /tmp/ssh_tunnel.log 2>&1 &  # restart
```

### Role label drift

If a handoff says a model is loaded, uncensored, or assigned to an entropy/shadow role, re-verify that exact claim before repeating it. `api/tags` proves load only; it does not prove the model is uncensored or role-suitable. Source-check the model card and run a benign dark/philosophical JSON probe so the handoff separates `loaded`, `responds`, and `role suitability`.

### Connection refused intermittently

Remove stale ControlMaster socket and retry:

```bash
rm -f ~/.ssh/sockets/*
ssh -S none vps-llm "echo OK"
```

## Verification

```bash
# Service alive on VPS
ssh vps-llm "curl -s http://localhost:11434/api/version"

# Tunnel alive locally
python3 -c "import urllib.request,json; r=json.loads(urllib.request.urlopen('http://localhost:11434/api/tags').read()); print([m['name'] for m in r['models']])"

# Generation works
python3 -c "import urllib.request,json; p=json.dumps({'model':'dolphin-llama3:8b','prompt':'Say OK','stream':False}).encode(); r=json.loads(urllib.request.urlopen(urllib.request.Request('http://localhost:11434/api/generate',data=p,headers={'Content-Type':'application/json'})).read()); print(r['response'])"
```

## Related

- `local-llm-deployment` — local deployment for PII/sensitive workloads (Faraday cage variant)
- `remote-llm-deployment` — more detailed VPS deployment guide with full procedure
