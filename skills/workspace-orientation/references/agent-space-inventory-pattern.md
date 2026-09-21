# Agent Space Inventory Pattern

This reference captures the workflow for evaluating legacy agent workspaces (like `agent_space`) before reuse as a memory root. The user corrected the plan to require deep inventory before assuming current relevance.

## Trigger

When the user wants to reuse an existing agent workspace as a memory root, or when a workspace's purpose is unclear.

## Workflow

### 1. Surface-level inventory

List all files and directories with:
- File name and path
- Size
- Creation date
- Last modified date
- File type / purpose guess

### 2. Content classification

For each file, classify into one of:

| Category | Description | Action |
|----------|-------------|--------|
| **Active tool code** | Scripts, processors, utilities still in use | Keep; link to memory |
| **Policy reference** | Rules, protocols, orientation docs | Keep; may need updating |
| **Project memory** | Roadmaps, plans, project-specific notes | Evaluate for current relevance |
| **Integration artifact** | MCP servers, bus relays, bridges | Check if still running |
| **Historical artifact** | Old versions, superseded work | Archive or delete with permission |
| **Orphaned file** | Unclear purpose, no apparent owner | Flag for user review |

### 3. Relevance assessment

For each file, determine:
- Is this still actively used?
- Does it conflict with current workspace state?
- Is the information duplicated elsewhere?
- Would removing it break anything?

### 4. Decision matrix

| Category | Duplicate? | Current? | Action |
|----------|------------|----------|--------|
| Active tool | No | Yes | Keep in place; link from memory |
| Policy reference | No | Yes | Keep; update if stale |
| Project memory | No | Yes | Keep; integrate into Plato notes |
| Project memory | Yes | Yes | Dedupe; keep canonical |
| Historical | Yes | No | Archive to vault/ |
| Orphaned | Unknown | Unknown | Flag for user |

### 5. Migration plan

Before moving anything:
1. Create the target structure
2. Map source → target paths
3. Identify dependencies between files
4. Create symbolic links or copies (user's choice)
5. Update orientation docs

## Example: agent_space inventory

```
agent_space/
├── agent_space_orientation.md    → Policy reference (historical)
├── drayl_processor.py            → Active tool code (check usage)
├── no-edits.md                   → Policy reference (active)
├── ovando_brown_roadmap.md       → Project memory (check relevance)
├── vape-overview.md              → Tool documentation (check usage)
├── wwmd_ask_hybrid.py            → Active tool code (check usage)
└── session-bus/                  → Integration artifact (check if running)
    ├── bus_data.json
    ├── bus_server.py
    ├── README.md
    └── start_bus.bat
```

## Pitfalls

- Do not assume a file's purpose from its name alone
- Do not delete files without explicit user approval
- Do not migrate files without checking for dependencies
- Do not treat all files as equally relevant
- Archive copies must be preserved before any reorganization

## References

- `D:\MW_CENTRAL\agent_space` — the workspace under evaluation
- `D:\MW_CENTRAL\vault\2026-07\agent_space-archive-20260703` — archive copy
