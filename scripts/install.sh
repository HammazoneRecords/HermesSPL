#!/bin/bash
# ============================================================================
# HermesSPL Triangulum — Linux/macOS Installer
# ============================================================================
# One-command install for the governed fork of Hermes Agent.
#
# Usage:
#   curl -fsSL https://raw.githubusercontent.com/your-org/hermes-spl/main/scripts/install.sh | bash
#
# Or download and run:
#   chmod +x install.sh && ./install.sh
#
# ============================================================================

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'
BOLD='\033[1m'

# Configuration
FORK_REPO="https://github.com/your-org/hermes-spl.git"
BRANCH="main"
HERMES_SPL_HOME="${HERMES_SPL_HOME:-$HOME/.hermes-spl}"
INSTALL_DIR="$HERMES_SPL_HOME/hermes-spl"

# Options
SKIP_SETUP=false
NON_INTERACTIVE=false

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --skip-setup) SKIP_SETUP=true; shift ;;
        --non-interactive) NON_INTERACTIVE=true; shift ;;
        --branch) BRANCH="$2"; shift 2 ;;
        *) shift ;;
    esac
done

write_step() { echo -e "${CYAN}[STEP]${NC} $1"; }
write_ok() { echo -e "${GREEN}[OK]${NC} $1"; }
write_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
write_err() { echo -e "${RED}[ERR]${NC} $1"; }

echo ""
echo -e "${BOLD}╔══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BOLD}║  HermesSPL Triangulum — Linux/macOS Installer              ║${NC}"
echo -e "${BOLD}║  Version 2.0.0 (Nyx)                                       ║${NC}"
echo -e "${BOLD}╚══════════════════════════════════════════════════════════════╝${NC}"
echo ""

# ============================================================================
# Step 0: Detect OS
# ============================================================================
write_step "Detecting OS..."

OS="unknown"
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="linux"
    if [ -f /etc/debian_version ]; then
        DISTRO="debian"
    elif [ -f /etc/redhat-release ]; then
        DISTRO="redhat"
    elif [ -f /etc/arch-release ]; then
        DISTRO="arch"
    else
        DISTRO="unknown"
    fi
elif [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macos"
    DISTRO="macos"
fi

write_ok "Detected: $OS ($DISTRO)"

# ============================================================================
# Step 1: Install uv
# ============================================================================
write_step "Checking uv (Python package manager)..."

if command -v uv &> /dev/null; then
    write_ok "uv already installed"
else
    write_step "Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    source $HOME/.local/bin/env 2>/dev/null || true
    export PATH="$HOME/.local/bin:$PATH"
    write_ok "uv installed"
fi

# ============================================================================
# Step 2: Install Python 3.11
# ============================================================================
write_step "Checking Python 3.11..."

if uv python list 2>/dev/null | grep -q "3.11"; then
    write_ok "Python 3.11 already available"
else
    write_step "Installing Python 3.11..."
    uv python install 3.11
    write_ok "Python 3.11 installed"
fi

# ============================================================================
# Step 3: Install Node.js
# ============================================================================
write_step "Checking Node.js..."

if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    write_ok "Node.js already installed: $NODE_VERSION"
else
    write_step "Installing Node.js..."
    if [ "$OS" == "macos" ]; then
        if command -v brew &> /dev/null; then
            brew install node
        else
            write_err "Homebrew not found. Install from https://nodejs.org/"
            exit 1
        fi
    elif [ "$DISTRO" == "debian" ]; then
        curl -fsSL https://deb.nodesource.com/setup_26.x | sudo -E bash -
        sudo apt install -y nodejs
    elif [ "$DISTRO" == "redhat" ]; then
        curl -fsSL https://rpm.nodesource.com/setup_26.x | sudo bash -
        sudo yum install -y nodejs
    elif [ "$DISTRO" == "arch" ]; then
        sudo pacman -S nodejs npm
    else
        write_err "Unsupported distro. Install Node.js manually from https://nodejs.org/"
        exit 1
    fi
    write_ok "Node.js installed"
fi

# ============================================================================
# Step 4: Install ripgrep
# ============================================================================
write_step "Checking ripgrep..."

if command -v rg &> /dev/null; then
    write_ok "ripgrep already installed"
else
    write_step "Installing ripgrep..."
    if [ "$OS" == "macos" ]; then
        brew install ripgrep
    elif [ "$DISTRO" == "debian" ]; then
        sudo apt install -y ripgrep
    elif [ "$DISTRO" == "redhat" ]; then
        sudo yum install -y ripgrep
    elif [ "$DISTRO" == "arch" ]; then
        sudo pacman -S ripgrep
    else
        write_warn "ripgrep not installed. Some features may not work."
    fi
    write_ok "ripgrep installed"
fi

# ============================================================================
# Step 5: Install FFmpeg
# ============================================================================
write_step "Checking FFmpeg..."

if command -v ffmpeg &> /dev/null; then
    write_ok "FFmpeg already installed"
else
    write_step "Installing FFmpeg..."
    if [ "$OS" == "macos" ]; then
        brew install ffmpeg
    elif [ "$DISTRO" == "debian" ]; then
        sudo apt install -y ffmpeg
    elif [ "$DISTRO" == "redhat" ]; then
        sudo yum install -y ffmpeg
    elif [ "$DISTRO" == "arch" ]; then
        sudo pacman -S ffmpeg
    else
        write_warn "FFmpeg not installed. TTS features may not work."
    fi
    write_ok "FFmpeg installed"
fi

# ============================================================================
# Step 6: Clone the fork
# ============================================================================
write_step "Cloning HermesSPL Triangulum..."

if [ -d "$INSTALL_DIR" ]; then
    write_warn "Directory already exists: $INSTALL_DIR"
    write_step "Updating existing installation..."
    cd "$INSTALL_DIR"
    git pull origin "$BRANCH"
else
    git clone -b "$BRANCH" "$FORK_REPO" "$INSTALL_DIR"
fi
write_ok "Repository at $INSTALL_DIR"

# ============================================================================
# Step 7: Create virtual environment
# ============================================================================
write_step "Creating virtual environment..."

VENV_DIR="$INSTALL_DIR/.venv"
if [ ! -d "$VENV_DIR" ]; then
    uv venv --python 3.11 "$VENV_DIR"
fi
write_ok "Virtual environment at $VENV_DIR"

# ============================================================================
# Step 8: Install Python dependencies
# ============================================================================
write_step "Installing Python dependencies..."

cd "$INSTALL_DIR"
uv pip install -r requirements.txt 2>/dev/null || uv pip install -r requirements.txt --no-dev

# Install hook deps
if [ -f hooks/requirements.txt ]; then
    uv pip install -r hooks/requirements.txt
fi

write_ok "Dependencies installed"

# ============================================================================
# Step 9: Create triangulum command
# ============================================================================
write_step "Creating triangulum command..."

BIN_DIR="$HOME/.local/bin"
mkdir -p "$BIN_DIR"

cat > "$BIN_DIR/triangulum" << EOF
#!/bin/bash
# HermesSPL Triangulum — entry point

HERMES_SPL_HOME="$INSTALL_DIR"
VENV_DIR="$INSTALL_DIR/.venv"

case "\$1" in
    doctor)
        "\$VENV_DIR/bin/python" -c "
import sys
sys.path.insert(0, '$INSTALL_DIR')
import hooks.pre_tool_call.color_neutralizer
import hooks.pre_tool_call.solobic_cpu
import hooks.pre_tool_call.sfl_hook
import hooks.post_tool_call.rite_framework
import protocols.signal_protocol
import memory.drayl_backend
print('ALL_SYSTEMS_OK')
"
        ;;
    init)
        mkdir -p "\$HOME/.hermes-spl/chats"
        mkdir -p "\$HOME/.hermes-spl/logs"
        echo "Initialized workspace at \$HOME/.hermes-spl"
        ;;
    run)
        cd "\$HERMES_SPL_HOME"
        exec "\$VENV_DIR/bin/python" triangulum run
        ;;
    version)
        echo "HermesSPL Triangulum v2.0.0 (Nyx)"
        ;;
    *)
        echo "Usage: triangulum [doctor|init|run|version]"
        exit 1
        ;;
esac
EOF

chmod +x "$BIN_DIR/triangulum"

# Add to PATH if needed
if [[ ":$PATH:" != *":$BIN_DIR:"* ]]; then
    echo "export PATH=\"\$HOME/.local/bin:\$PATH\"" >> ~/.bashrc
    write_ok "Added $BIN_DIR to PATH (restart terminal or run: source ~/.bashrc)"
fi

write_ok "triangulum command available at $BIN_DIR"

# ============================================================================
# Step 10: Enable hooks
# ============================================================================
write_step "Enabling hooks..."

HOOKS_CONFIG="$INSTALL_DIR/config/hooks.yaml"
HOOKS_DIR="$(dirname "$HOOKS_CONFIG")"

if [ ! -f "$HOOKS_CONFIG" ]; then
    mkdir -p "$HOOKS_DIR"
    cat > "$HOOKS_CONFIG" << EOF
# HermesSPL Triangulum — Hook Configuration
hooks:
  pre_tool_call:
    - color_neutralizer
    - solobic_cpu
    - sfl_hook
    - session_access_guard
  post_tool_call:
    - rite_framework

theme: jamaica-rbg
multi_chat: true
EOF
    write_ok "Hooks enabled"
else
    write_ok "Hooks config already exists"
fi

# ============================================================================
# Step 11: Set theme
# ============================================================================
write_step "Setting Jamaica RBG theme..."

cat > "$INSTALL_DIR/config.yaml" << EOF
# HermesSPL Triangulum Configuration
display:
  skin: jamaica-rbg
  compact: false
  show_reasoning: true

agent:
  name: triangulum
  version: "2.0.0"
  codename: Nyx

hooks:
  enabled: true

multi_chat:
  enabled: true
EOF

write_ok "Theme set to Jamaica RBG"

# ============================================================================
# Step 12: Run doctor
# ============================================================================
write_step "Running health check..."

"$VENV_DIR/bin/python" -c "
import sys
sys.path.insert(0, '$INSTALL_DIR')
try:
    import hooks.pre_tool_call.color_neutralizer
    import hooks.pre_tool_call.solobic_cpu
    import hooks.pre_tool_call.sfl_hook
    import hooks.post_tool_call.rite_framework
    import protocols.signal_protocol
    import memory.drayl_backend
    print('ALL_SYSTEMS_OK')
except Exception as e:
    print(f'ERROR: {e}')
    sys.exit(1)
"

if [ $? -eq 0 ]; then
    write_ok "All systems healthy"
else
    write_warn "Some checks failed. Run 'triangulum doctor' for details."
fi

# ============================================================================
# Complete
# ============================================================================
echo ""
echo -e "${BOLD}╔══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BOLD}║  Installation Complete!                                    ║${NC}"
echo -e "${BOLD}╠══════════════════════════════════════════════════════════════╣${NC}"
echo -e "${BOLD}║  Run one of these commands:                                ║${NC}"
echo -e "${BOLD}║                                                              ║${NC}"
echo -e "${BOLD}║    triangulum doctor    — verify installation              ║${NC}"
echo -e "${BOLD}║    triangulum init      — create workspace                 ║${NC}"
echo -e "${BOLD}║    triangulum run       — start the gateway                ║${NC}"
echo -e "${BOLD}║    hermes desktop       — open multi-chat desktop          ║${NC}"
echo -e "${BOLD}║                                                              ║${NC}"
echo -e "${BOLD}║  Restart your terminal first if triangulum is not found.   ║${NC}"
echo -e "${BOLD}╚══════════════════════════════════════════════════════════════╝${NC}"
echo ""
