#!/bin/bash
# HermesSPL Install Script
# Installs the forked HermesSPL as a separate application
# Usage: bash install.sh

set -e

FORK_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV_DIR="$FORK_DIR/.venv"

echo "=== HermesSPL Installer ==="
echo ""

# Check Python version
PYTHON=$(which python3)
PY_VERSION=$($PYTHON --version 2>&1 | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "Python: $PYTHON (v$PY_VERSION)"

# Create virtual environment
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..."
    $PYTHON -m venv "$VENV_DIR"
fi

source "$VENV_DIR/bin/activate"

# Install dependencies
echo "Installing HermesSPL..."
pip install -e "$FORK_DIR" 2>&1 | tail -5

# Create config directory
CONFIG_DIR="$HOME/.hermes-spl"
mkdir -p "$CONFIG_DIR"
mkdir -p "$CONFIG_DIR/profiles"
mkdir -p "$CONFIG_DIR/plugins"

echo ""
echo "=== Install Complete ==="
echo ""
echo "Binary: $VENV_DIR/bin/hermes-spl"
echo "Config: $CONFIG_DIR"
echo ""
echo "To start:"
echo "  $VENV_DIR/bin/hermes-spl --help"
echo ""
echo "To activate the venv:"
echo "  source $VENV_DIR/bin/activate"
echo "  hermes-spl --help"
