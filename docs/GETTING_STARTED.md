# Getting Started with HermesSPL

Welcome. This guide takes about five minutes and gets you to your first conversation.

## What You're Looking At

HermesSPL is a personal AI assistant you run on your own machine. It chats with you through Telegram, Discord, Slack, or a desktop window. It can search the web, read and write files, run shell commands, and automate tasks.

Unlike most AI tools, everything stays on your computer. No one else sees your conversations.

## Step 1: Install

### Linux / macOS / WSL2

```bash
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash
```

Then clone this repository and run:

```bash
./triangulum init
```

### Windows (PowerShell)

```powershell
iex (irm https://hermes-agent.nousresearch.com/install.ps1)
```

Then inside this repository:

```powershell
.\triangulum init
```

`init` creates a workspace — a folder where the assistant stores its memory, configuration, and conversation history. Your data lives there, not in the cloud.

## Step 2: Start the Gateway

```bash
./triangulum run
```

The gateway is the background process that listens for messages. Once it's running, you can chat through any connected platform (Telegram, Discord, etc.) or open the desktop window.

## Step 3: Chat

Open a chat:

```bash
./triangulum chat open
```

Or launch the desktop app, click **[+] New Chat**, and pick a profile.

Type a message. The assistant responds.

## Key Commands

| Command | What it does |
|---------|-------------|
| `./triangulum doctor` | Checks that everything is installed correctly |
| `./triangulum version` | Shows the current version |
| `/new` | Starts a fresh conversation |
| `/status` | Shows session info |
| `/hooks` | Lists active hook scripts |

## What Are Hooks?

Hooks are small scripts that run automatically at specific moments — before a tool executes, after a command finishes, when a new conversation starts. They let you add rules, logging, or safety checks without changing the assistant's core code.

For example, a hook can block dangerous shell commands or log every file write. See [HOOKS.md](HOOKS.md) for details.

## What's a Profile?

A profile is a self-contained assistant identity. Each profile has its own:

- System prompt (how it behaves)
- Set of tools it can use
- Hook scripts
- Memory files

You can have multiple profiles for different purposes — one for coding, one for writing, one for research — and switch between them.

## What's a Session?

A session is one continuous conversation. When you type `/new`, the old session ends and a fresh one begins. The assistant remembers past sessions but treats each new one as a clean slate unless you tell it otherwise.

## What Next?

- Read [PHILOSOPHY.md](PHILOSOPHY.md) to understand the thinking behind this project.
- Read [HOOKS.md](HOOKS.md) to learn how to extend the system with custom scripts.
- Read [CONCEPTS.md](CONCEPTS.md) to navigate the formalized vocabulary used throughout.

## Getting Help

```bash
# Run the health check
./triangulum doctor

# View logs
hermes logs --follow
```

If something breaks, `doctor` tells you what's wrong and how to fix it.
