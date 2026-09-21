# Hooks: Extending the System with Custom Scripts

Hooks are the way you add custom behavior to HermesSPL without modifying its core code. A hook is a small script that runs at a specific moment — before a tool executes, after it finishes, when a new session begins, and many other points.

## The Four Hook Systems

There are four ways to register hooks. They differ in where they live and when they fire.

| System | Registered via | Runs in | Best for |
|--------|---------------|---------|---------|
| **Shell hooks** | `hooks:` block in `~/.hermes/config.yaml` | Everywhere (CLI, Gateway, Desktop) | Blocking tools, logging, context injection |
| **Plugin hooks** | Python `register()` in a plugin | CLI and Gateway | Programmatic control, metrics, integrations |
| **Gateway hooks** | `HOOK.yaml` + `handler.py` in `~/.hermes/hooks/` | Gateway only | Startup tasks, lifecycle events |
| **Outbound webhooks** | `hooks.outbound:` in `~/.hermes/config.yaml` | Everywhere | Sending events to external HTTP services |

Start with **shell hooks** — they are the simplest and cover most use cases.

## Shell Hooks

A shell hook is any executable script (Bash, Python, Ruby, anything with a `shebang`). You declare it in your profile's `config.yaml`.

### Configuration

```yaml
hooks:
  pre_tool_call:
    - command: /path/to/my-guard.sh
      matcher: terminal|write_file|patch
      timeout: 10
      fail_closed: true
  post_tool_call:
    - command: /path/to/my-logger.py
      matcher: terminal|write_file
      timeout: 5
```

Key fields:

- **`command`**: Path to your script. It receives JSON on stdin and returns a decision on stdout.
- **`matcher`**: A regex of tool names this hook applies to. `terminal|write_file` fires only for those two tools.
- **`timeout`**: Seconds before the hook is killed. Default is 60.
- **`fail_closed`**: If true, a timeout or crash blocks the action. If false, it lets the action through.

### How a Hook Receives Data

Your script gets a JSON payload on stdin. For a `pre_tool_call` hook:

```json
{
  "tool_name": "terminal",
  "tool_input": {"command": "ls -la"},
  "session_id": "abc123",
  "cwd": "/home/user/project",
  "profile": "default"
}
```

### How a Hook Returns a Decision

Your script prints JSON to stdout and exits with a code:

| Exit code | Meaning |
|-----------|---------|
| 0 | Allow the action |
| 2 | Block the action |

To block a tool:

```bash
#!/bin/bash
echo '{"action": "block", "reason": "No terminal commands outside project root"}'
exit 2
```

To modify the tool's arguments before it runs:

```bash
echo '{"action": "modify", "args": {"command": "ls -la"}}'
exit 0
```

To inject context into the LLM prompt (for `pre_llm_call` hooks):

```bash
echo '{"context": "The user is currently working on a Python project."}'
exit 0
```

### First-Run Consent

The first time a hook runs for a given `(event, tool)` pair, Hermes asks for your approval. This prevents malicious hooks from silently taking effect. Approvals are stored in `~/.hermes/shell-hooks-allowlist.json`.

## Events Available for Shell Hooks

| Event | When it fires | Can block? |
|-------|--------------|-----------|
| `pre_tool_call` | Before every tool execution | Yes |
| `post_tool_call` | After every tool execution | No (observe only) |
| `pre_llm_call` | Once per user turn, before the model responds | No (can inject context) |
| `post_llm_call` | After the model produces a final response | No |
| `transform_tool_result` | Before the tool result is added to the conversation | No (can rewrite) |
| `transform_terminal_output` | After a terminal command, before the result is shown | No (can rewrite) |
| `transform_llm_output` | After the model responds, before the user sees it | No (can rewrite) |
| `on_session_start` | First turn of a new session | No |
| `on_session_end` | End of a session | No |
| `subagent_stop` | A delegated child agent finishes | No |

## Plugin Hooks (Python)

If you need more control than a shell script offers, write a Python plugin.

### Directory Structure

```
~/.hermes/plugins/my-plugin/
├── plugin.yaml
└── register.py
```

### plugin.yaml

```yaml
name: my-plugin
description: Logs all tool calls
version: 1.0.0
author: Your Name
```

### register.py

```python
def register(ctx):
    # Block dangerous tools
    ctx.register_hook("pre_tool_call", block_dangerous)

    # Log every completed turn
    ctx.register_hook("post_llm_call", log_turn)

    # Inject memory context before each turn
    ctx.register_hook("pre_llm_call", inject_memory)
```

### Blocking a Tool

```python
def block_dangerous(tool_name, args, **kwargs):
    if tool_name == "terminal" and "rm -rf" in args.get("command", ""):
        return {"action": "block", "message": "Refusing to run rm -rf"}
    return None  # allow everything else
```

### Injecting Context

```python
def inject_memory(session_id, user_message, **kwargs):
    # Fetch relevant memories and prepend them
    memories = recall(user_message)
    if memories:
        return {"context": f"Relevant memories:\n{memories}"}
    return None
```

### Rewriting Output

```python
def redact_secrets(response_text, **kwargs):
    import re
    return re.sub(r"sk-[A-Za-z0-9]{32,}", "[REDACTED]", response_text)
```

## Gateway Hooks

Gateway hooks run only in the gateway process (Telegram, Discord, etc.). They are useful for startup tasks and lifecycle monitoring.

### Structure

```
~/.hermes/hooks/my-hook/
├── HOOK.yaml
└── handler.py
```

### HOOK.yaml

```yaml
name: my-hook
description: Log all agent activity
events:
  - agent:start
  - agent:end
  - session:start
```

### handler.py

```python
async def handle(event_type: str, context: dict):
    print(f"Event: {event_type}, Session: {context.get('session_id')}")
```

Gateway hooks cannot block tools. They are for observation and side effects only.

## Outbound Webhooks

Outbound webhooks push signed JSON events to an external HTTP endpoint. Use them to feed dashboards, trigger CI pipelines, or notify other agents.

```yaml
hooks:
  outbound:
    - url: https://your-service.example.com/hermes-events
      events:
        - agent:end
        - session:start
      secret: your-signing-secret
```

The receiving server can verify the signature in the `X-Hermes-Signature` header.

## Debugging Hooks

```bash
# List all configured hooks
hermes hooks list

# Test a hook against a synthetic payload
hermes hooks test pre_tool_call --for-tool terminal

# Check hook health (permissions, JSON validity, timing)
hermes hooks doctor

# Revoke a hook's approval
hermes hooks revoke "rm -rf /"
```

## Common Patterns

### Block Dangerous Commands

```yaml
# In config.yaml
hooks:
  pre_tool_call:
    - command: /path/to/safety-guard.sh
      matcher: terminal
      timeout: 5
      fail_closed: true
```

```bash
#!/bin/bash
# safety-guard.sh
payload=$(cat)
command=$(echo "$payload" | jq -r '.tool_input.command // ""')

if echo "$command" | grep -qE 'rm -rf|sudo|chmod 777'; then
  echo '{"action": "block", "reason": "Potentially destructive command blocked"}'
  exit 2
fi

exit 0
```

### Auto-Format After File Writes

```yaml
hooks:
  post_tool_call:
    - command: /path/to/autoformat.sh
      matcher: write_file|patch
      timeout: 10
```

```bash
#!/bin/bash
payload=$(cat)
path=$(echo "$payload" | jq -r '.tool_input.path // ""')

if [[ "$path" == *.py ]]; then
  black "$path" 2>/dev/null || true
fi
```

### Log Everything

```yaml
hooks:
  post_tool_call:
    - command: /path/to/log-all.sh
      matcher: .*  # all tools
      timeout: 5
```

```bash
#!/bin/bash
echo "$(cat)" >> ~/.hermes/logs/all-tool-calls.jsonl
```

## Hook Execution Order

When multiple hooks are registered for the same event:

1. **Python plugin hooks** run first, in registration order.
2. **Shell hooks** run after, in the order listed in `config.yaml`.

For `pre_tool_call`, the first hook that returns a `block` or `approve` decision wins. Later hooks are not consulted.

## Timeouts and Failure Modes

- If a hook exceeds its `timeout`, it is killed.
- If `fail_closed: true`, a timed-out hook blocks the action.
- If `fail_closed: false` (or not set), a timed-out hook lets the action through.
- If a hook crashes without producing output, it is treated as a timeout.
- Hook errors are logged but never crash the agent.

## Security Notes

- Hooks run with the same permissions as the Hermes process. A malicious hook can do anything the agent can.
- Always review a hook's code before approving it.
- The first-use consent prompt exists to protect you. Do not blindly approve hooks you did not write.
- Shell hooks run as subprocesses, which provides isolation from the main agent process.
- Plugin hooks run in-process. Only install plugins you trust.
