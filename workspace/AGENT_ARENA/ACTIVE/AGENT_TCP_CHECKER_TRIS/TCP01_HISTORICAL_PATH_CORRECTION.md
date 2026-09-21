# TCP01 Historical Path Correction

Created UTC: 2026-09-12T07:26:35.156278+00:00

## Observed issue

Copied TCP01 historical report(s) reference obsolete lowercase paths under `/root/MW_CENTRAL/Pluto/agents/...`.

## Resolution

Those historical report files are retained unchanged for provenance. They do not authorize actions. The active canonical TCP01 root is:

`/root/MW_CENTRAL/TRIANGULUM/HELIOS/NYX/AGENT_ARENA/ACTIVE/AGENT_TCP01_TRIS`

## Current scope

Writes remain confined to the active TCP01 root and occur only under an explicit Tris task packet.
