# TRIANGULUM Public Installation and Windows Test Plan

## Purpose

This fork must be installable and testable on a separate Windows computer without access to the development machine, live PLUTO instance, or private credentials.

## Product boundary

- Product/runtime name: HermesSPL
- Public fork identity: TRIANGULUM
- Private development workspace: ANDROMALIUS data namespace inside TRIANGULUM
- Live PLUTO instance: never bundled, referenced, or required
- Public package: code, documented defaults, schemas, tests, and example configuration only
- Private material excluded: credentials, auth state, session databases, personal memories, private vaults, caches, logs, and machine-specific absolute paths

## Windows installation paths

### Recommended desktop path

1. Download the Hermes Desktop installer from the public Hermes site.
2. Install Hermes Desktop on Windows.
3. Clone or download the TRIANGULUM fork into a user-owned directory.
4. Run the TRIANGULUM setup command or launcher.
5. Complete provider configuration locally; never ship credentials in the repository.
6. Run the smoke-test command.

### Command-line path

PowerShell installation of the Hermes base runtime:

```powershell
iex (irm https://hermes-agent.nousresearch.com/install.ps1)
```

Then install the TRIANGULUM fork in a separate directory and run its setup script. The fork must provide a PowerShell bootstrapper that:

- checks Windows and Python/Node prerequisites;
- creates a per-user virtual environment;
- installs the fork in editable or packaged mode;
- creates a user-local TRIANGULUM home/data directory;
- applies safe default configuration;
- refuses to use `/root/MW_CENTRAL`, `PLUTO`, or developer-only paths;
- runs import, hook, and isolation smoke tests.

## Required public artifacts

- `install.ps1` — Windows bootstrapper
- `install.sh` — POSIX bootstrapper
- `triangulum.ps1` — launcher and diagnostic commands
- `config.example.yaml` — no credentials
- `PUBLIC_INSTALL.md` — user-facing instructions
- `SECURITY.md` — credential and data-boundary policy
- `SMOKE_TESTS.md` — acceptance tests
- package/build metadata for reproducible installation
- export/restore procedure that excludes secrets by default

## Windows acceptance tests

A clean Windows machine must prove:

1. Installation succeeds for a non-administrator user where supported.
2. `triangulum doctor` reports the active fork and data root.
3. No runtime path contains `/root/MW_CENTRAL/PLUTO` or another developer-only path.
4. Agent profiles use the public continent/element names.
5. Hooks import and execute.
6. A harmless tool call completes the RITE cycle.
7. Unauthorized session access is blocked.
8. A Drayl append/query round trip succeeds.
9. Signal states reject invalid transitions.
10. Secrets are requested locally and are absent from package artifacts.
11. Uninstall removes only TRIANGULUM-owned files.
12. Logs and receipts identify the fork without exposing private data.

## Public release gates

Do not call the fork publicly installable until the clean-machine Windows test passes, private-data scan passes, package manifest is reviewed, and the smoke-test receipt is archived.
