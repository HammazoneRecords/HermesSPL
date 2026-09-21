#!/bin/bash
# Register the scope enforcement hook in Hermes config
# Run this once: bash register_scope_hook.sh

CONFIG=~/.hermes/config.yaml

# Check if already registered
if grep -q "pluto_scope_guard.py" "$CONFIG"; then
    echo "Scope guard hook already registered."
    exit 0
fi

# Add the scope guard hook after the existing pre_tool_call entry
# Using sed to insert after the fail_closed: true line of the first hook
sed -i '/^  pre_tool_call:/,/^  post_tool_call:/ {
    /fail_closed: true/ {
        a\    - command: python3 /root/MW_CENTRAL/TRIANGULUM/HELIOS/NYX/Y-MINDWAVE/H3_SYSTEM/07_HOOKS/00_SHELL/pluto_scope_guard.py\n      matcher: write_file|patch\n      timeout: 10\n      fail_closed: true
    }
}' "$CONFIG"

echo "✅ Scope guard hook registered."
echo ""
echo "Verifying..."
grep -A4 "pluto_scope_guard" "$CONFIG"
echo ""
echo "Restart Hermes session for hook to take effect."
