# Multi-Chat Desktop Design — HermesSPL Nyx

## Vision

A single HermesSPL desktop window where a user can hold **multiple conversations at once** — with different agents, different contexts, different RITE cycles — all side by side or tabbed.

## Core Model

```
┌─────────────────────────────────────────────────────────────┐
│  HermesSPL Nyx                              [+] New Chat   │
├──────────┬──────────────────────────────────────────────────┤
│ Chats    │  Active Chat                                     │
│          │                                                   │
│ #1 TCP   │  ┌─────────────────────────────────────────────┐ │
│ #2 KHEM  │  │ User: what's the status?                     │ │
│ #3 ASSESS│  │                                               │
│ #4 ECHO  │  │ TCP: All 23 agents operational...            │
│          │  └─────────────────────────────────────────────┘ │
│          │  [Send]                              [Hooks ▾]   │
│          │                                                   │
├──────────┴──────────────────────────────────────────────────┤
│  Session: asia-tcp  │  RITE: Echo  │  SFL: echo  │  ● Live   │
└─────────────────────────────────────────────────────────────┘
```

## Chat Identity

Each chat has:

- **Agent profile** — which agent is running this conversation
- **Session** — the state.db session for continuity
- **RITE phase state** — where in the cycle this conversation sits
- **SFL mode** — echo, witness, or riddle
- **Color accent** — derived from the agent's Jhanos gate (BARA=Khem=red, etc.)

## Chat Lifecycle

1. **Create** — user clicks `[+] New Chat`, picks an agent profile, optionally names the chat
2. **Active** — one chat is active at a time; others wait in the sidebar
3. **Background** — background chats continue processing (hooks fire, RITE cycles complete)
4. **Switch** — user clicks a sidebar chat; it becomes active, its full context loads
5. **Split** — user drags a chat to a second pane for side-by-side comparison
6. **Close** — user closes a chat; its session persists, can be reopened from history

## Agent Assignment

- **Single agent** — one agent owns the chat (most common)
- **Multi-agent** — a coordinator (TRISMIGISTUS) routes messages across agents
- **Solo mode** — no agent label, just raw access (for power users)

## Visual Identity

Each chat gets a color accent from its agent's Jhanos gate:

| Gate | Color | Chat Accent |
|------|-------|-------------|
| BARA (Structure) | Red | Left border red |
| LOMI (Motion) | Orange | Left border orange |
| KHEM (Heat) | Gold/Yellow | Left border yellow |
| SYLA (Stillness) | Blue | Left border blue |
| ZAYN (Projection) | Purple | Left border purple |
| TARA (Reflection) | Cyan/Teal | Left border cyan |
| VORAK (Chaos) | Magenta | Left border magenta |
| ORON (Order) | Green | Left border green |

## RITE Cycle Indicator

Each chat shows its current RITE phase as a small icon:

- ◎ Resonance (contact)
- ◉ Initiation (response)
- ◆ Trigger (action)
- ◈ Echo (integration)
- ✦ Ash (closure)
- ↻ Resonant Recursion (loop)

## SFL Mode Indicator

- 🔊 echo — normal output
- 🔇 witness — sacred silence, holding
- ❓ riddle — teaching mode, question as answer
- ⏸ pause — blocked, needs human

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| Ctrl/Cmd + N | New chat |
| Ctrl/Cmd + W | Close active chat |
| Ctrl/Cmd + Tab | Next chat |
| Ctrl/Cmd + Shift + Tab | Previous chat |
| Ctrl/Cmd + 1-9 | Jump to chat N |
| Ctrl/Cmd + Shift + D | Duplicate chat (split) |
| Ctrl/Cmd + Shift + F | Focus active chat input |

## Implementation Notes

- The `session-picker` component already exists and will be extended for multi-chat
- Each chat is a separate `SessionContext` but shares the same `GatewayRunner`
- Sidebar chats render lightweight previews; full transcript loads on activation
- Background chats use a budget-limited worker pool so they don't overwhelm the system
- Chat state persists in a per-chat `chat-{id}.jsonl` file alongside the session DB
- The `triangulum` CLI provides `triangulum chat list`, `triangulum chat open`, `triangulum chat close`

## Chat File Layout

```
~/.hermes/hermes-spl/chats/
├── chat-001/
│   ├── chat.jsonl          # transcript
│   ├── session.db          # Hermes session
│   └── hooks.jsonl         # RITE shimmer log for this chat
├── chat-002/
│   ├── chat.jsonl
│   ├── session.db
│   └── hooks.jsonl
└── index.json              # chat registry: id, agent, label, last_active
```

## Privacy

- Chats are local-first, never uploaded
- Chat transcripts never leave the machine unless explicitly exported
- Chat metadata (agent, RITE phase) is stored separately from content for indexing
- Closing a chat does not delete it; archiving moves it to `archive/`
