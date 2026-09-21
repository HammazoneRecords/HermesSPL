# ============================================================================
# HermesSPL Triangulum — Windows Installer (PowerShell)
# ============================================================================
# One-command install for the governed fork of Hermes Agent.
#
# Usage:
#   iex (irm https://raw.githubusercontent.com/HammazoneRecords/HermesSPL/main/scripts/install.ps1)
#
# Or download and run:
#   .\install.ps1
#
# ============================================================================

param(
    [string]$Branch = "main",
    [string]$ForkRepo = "https://github.com/HammazoneRecords/HermesSPL.git",
    [string]$HermesHome = "$env:LOCALAPPDATA\hermes-spl",
    [switch]$SkipSetup,
    [switch]$NonInteractive
)

$ErrorActionPreference = "Stop"

# Colors
$Red = "`e[31m"
$Green = "`e[32m"
$Yellow = "`e[33m"
$Blue = "`e[34m"
$Cyan = "`e[36m"
$Reset = "`e[0m"
$Bold = "`e[1m"

function Write-Step($msg) { Write-Host "$Cyan[STEP]$Reset $msg" }
function Write-Ok($msg) { Write-Host "$Green[OK]$Reset $msg" }
function Write-Warn($msg) { Write-Host "$Yellow[WARN]$Reset $msg" }
function Write-Err($msg) { Write-Host "$Red[ERR]$Reset $msg" }

Write-Host ""
Write-Host "$Bold╔══════════════════════════════════════════════════════════════╗$Reset"
Write-Host "$Bold║  HermesSPL Triangulum — Windows Installer                  ║$Reset"
Write-Host "$Bold║  Version 2.0.0 (Nyx)                                       ║$Reset"
Write-Host "$Bold╚══════════════════════════════════════════════════════════════╝$Reset"
Write-Host ""

# ============================================================================
# Step 0: Check prerequisites
# ============================================================================
Write-Step "Checking prerequisites..."

# Windows version
$os = Get-CimInstance Win32_OperatingSystem
$build = $os.BuildNumber
if ($build -lt 17763) {
    Write-Err "Windows 10 (1809) or later required. Your build: $build"
    exit 1
}
Write-Ok "Windows build $build detected"

# Architecture
$arch = if ([Environment]::Is64BitOperatingSystem) { "x64" } else { "x86" }
Write-Ok "Architecture: $arch"

# ============================================================================
# Step 1: Install uv (Python package manager)
# ============================================================================
Write-Step "Checking uv (Python package manager)..."

$uvPath = Get-Command uv -ErrorAction SilentlyContinue
if ($uvPath) {
    Write-Ok "uv already installed: $($uvPath.Source)"
} else {
    Write-Step "Installing uv..."
    try {
        Invoke-RestMethod https://astral.sh/uv/install.ps1 | Invoke-Expression
        # Refresh PATH after install
        $env:PATH = [System.Environment]::GetEnvironmentVariable("PATH", "User") + ";" + [System.Environment]::GetEnvironmentVariable("PATH", "Machine")
        $uvPath = Get-Command uv -ErrorAction SilentlyContinue
        if ($uvPath) {
            Write-Ok "uv installed successfully"
        } else {
            Write-Warn "uv install completed but not in PATH. Restart your terminal and re-run this script."
            exit 1
        }
    } catch {
        Write-Err "Failed to install uv: $_"
        exit 1
    }
}

# ============================================================================
# Step 2: Install Python 3.11
# ============================================================================
Write-Step "Checking Python 3.11..."

$pythonVersion = & uv python list 2>$null | Select-String "3.11"
if (-not $pythonVersion) {
    Write-Step "Installing Python 3.11 via uv..."
    & uv python install 3.11
    if ($LASTEXITCODE -ne 0) {
        Write-Err "Failed to install Python 3.11"
        exit 1
    }
}
Write-Ok "Python 3.11 ready"

# ============================================================================
# Step 3: Install Node.js
# ============================================================================
Write-Step "Checking Node.js..."

$nodePath = Get-Command node -ErrorAction SilentlyContinue
if ($nodePath) {
    $nodeVersion = & node --version
    Write-Ok "Node.js already installed: $nodeVersion"
} else {
    Write-Step "Installing Node.js..."
    # Try winget first, then chocolatey
    $winget = Get-Command winget -ErrorAction SilentlyContinue
    $choco = Get-Command choco -ErrorAction SilentlyContinue
    
    if ($winget) {
        Write-Step "Using winget..."
        winget install OpenJS.NodeJS.LTS --accept-source-agreements --accept-package-agreements
    } elseif ($choco) {
        Write-Step "Using chocolatey..."
        choco install nodejs-lts -y
    } else {
        Write-Err "No package manager found (winget or chocolatey required)"
        Write-Err "Install Node.js manually from https://nodejs.org/"
        exit 1
    }
    
    # Refresh PATH
    $env:PATH = [System.Environment]::GetEnvironmentVariable("PATH", "User") + ";" + [System.Environment]::GetEnvironmentVariable("PATH", "Machine")
    $nodePath = Get-Command node -ErrorAction SilentlyContinue
    if (-not $nodePath) {
        Write-Warn "Node.js installed but not in PATH. Restart your terminal."
        exit 1
    }
    Write-Ok "Node.js installed"
}

# ============================================================================
# Step 4: Install ripgrep
# ============================================================================
Write-Step "Checking ripgrep..."

$rgPath = Get-Command rg -ErrorAction SilentlyContinue
if ($rgPath) {
    Write-Ok "ripgrep already installed"
} else {
    Write-Step "Installing ripgrep..."
    $winget = Get-Command winget -ErrorAction SilentlyContinue
    if ($winget) {
        winget install BurntSushi.ripgrep.MSVC --accept-source-agreements --accept-package-agreements
    } else {
        Write-Warn "ripgrep not found. Some features may not work."
        Write-Warn "Install from: https://github.com/BurntSushi/ripgrep#installation"
    }
    $env:PATH = [System.Environment]::GetEnvironmentVariable("PATH", "User") + ";" + [System.Environment]::GetEnvironmentVariable("PATH", "Machine")
}

# ============================================================================
# Step 5: Install FFmpeg
# ============================================================================
Write-Step "Checking FFmpeg..."

$ffmpegPath = Get-Command ffmpeg -ErrorAction SilentlyContinue
if ($ffmpegPath) {
    Write-Ok "FFmpeg already installed"
} else {
    Write-Step "Installing FFmpeg..."
    $winget = Get-Command winget -ErrorAction SilentlyContinue
    if ($winget) {
        winget install Gyan.FFmpeg --accept-source-agreements --accept-package-agreements
    } else {
        Write-Warn "FFmpeg not found. TTS features may not work."
        Write-Warn "Install from: https://ffmpeg.org/download.html#build-windows"
    }
    $env:PATH = [System.Environment]::GetEnvironmentVariable("PATH", "User") + ";" + [System.Environment]::GetEnvironmentVariable("PATH", "Machine")
}

# ============================================================================
# Step 6: Clone the fork
# ============================================================================
Write-Step "Cloning HermesSPL Triangulum..."

$installDir = Join-Path $HermesHome "hermes-spl"
if (Test-Path $installDir) {
    Write-Warn "Directory already exists: $installDir"
    Write-Step "Updating existing installation..."
    Push-Location $installDir
    & git pull origin $Branch
    Pop-Location
} else {
    & git clone -b $Branch $ForkRepo $installDir
    if ($LASTEXITCODE -ne 0) {
        Write-Err "Failed to clone repository"
        exit 1
    }
}
Write-Ok "Repository at $installDir"

# ============================================================================
# Step 7: Create virtual environment
# ============================================================================
Write-Step "Creating virtual environment..."

$venvDir = Join-Path $installDir ".venv"
if (-not (Test-Path $venvDir)) {
    & uv venv --python 3.11 $venvDir
    if ($LASTEXITCODE -ne 0) {
        Write-Err "Failed to create virtual environment"
        exit 1
    }
}
Write-Ok "Virtual environment at $venvDir"

# ============================================================================
# Step 8: Install Python dependencies
# ============================================================================
Write-Step "Installing Python dependencies..."

Push-Location $installDir
& uv pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) {
    Write-Warn "Some packages failed to install. Attempting without optional deps..."
    & uv pip install -r requirements.txt --no-dev
}
Pop-Location

# Install fork-specific deps
$hookReqs = Join-Path $installDir "hooks" "requirements.txt"
if (Test-Path $hookReqs) {
    Push-Location $installDir
    & uv pip install -r hooks/requirements.txt
    Pop-Location
}

Write-Ok "Dependencies installed"

# ============================================================================
# Step 9: Create triangulum command
# ============================================================================
Write-Step "Creating triangulum command..."

$scriptsDir = Join-Path $installDir "scripts"
$triangulumBat = Join-Path $scriptsDir "triangulum.bat"

$batContent = @"
@echo off
REM HermesSPL Triangulum — entry point
setlocal

set HERMES_SPL_HOME=$installDir
set VENV_DIR=$venvDir

if "%1"=="doctor" goto doctor
if "%1"=="init" goto init
if "%1"=="run" goto run
if "%1"=="version" goto version

echo Usage: triangulum [doctor^|init^|run^|version]
goto end

:doctor
"%VENV_DIR%\Scripts\python.exe" -c "import hooks.pre_tool_call.color_neutralizer; import hooks.pre_tool_call.solobic_cpu; import hooks.pre_tool_call.sfl_hook; import hooks.post_tool_call.rite_framework; import protocols.signal_protocol; import memory.drayl_backend; print('ALL_HOOKS_OK')"
goto end

:init
if not exist "%USERPROFILE%\.hermes-spl" mkdir "%USERPROFILE%\.hermes-spl"
if not exist "%USERPROFILE%\.hermes-spl\chats" mkdir "%USERPROFILE%\.hermes-spl\chats"
if not exist "%USERPROFILE%\.hermes-spl\logs" mkdir "%USERPROFILE%\.hermes-spl\logs"
echo Initialized workspace at %USERPROFILE%\.hermes-spl
goto end

:run
cd /d "%HERMES_SPL_HOME%"
"%VENV_DIR%\Scripts\python.exe" triangulum run
goto end

:version
echo HermesSPL Triangulum v2.0.0 (Nyx)
goto end

:end
"@

$batContent | Out-File -FilePath $triangulumBat -Encoding ASCII

# Create shim in LOCALAPPDATA\bin
$binDir = Join-Path $env:LOCALAPPDATA "HermesSPL" "bin"
if (-not (Test-Path $binDir)) {
    New-Item -ItemType Directory -Path $binDir -Force | Out-Null
}
Copy-Item $triangulumBat (Join-Path $binDir "triangulum.bat") -Force

# Add to PATH if not already there
$currentPath = [System.Environment]::GetEnvironmentVariable("Path", "User")
if ($currentPath -notlike "*$binDir*") {
    [System.Environment]::SetEnvironmentVariable("Path", "$currentPath;$binDir", "User")
    Write-Ok "Added $binDir to PATH (restart terminal to use)"
}

Write-Ok "triangulum command available at $binDir"

# ============================================================================
# Step 10: Enable hooks
# ============================================================================
Write-Step "Enabling hooks..."

$hooksConfig = Join-Path $installDir "config" "hooks.yaml"
if (-not (Test-Path $hooksConfig)) {
    $hooksDir = Split-Path $hooksConfig -Parent
    if (-not (Test-Path $hooksDir)) {
        New-Item -ItemType Directory -Path $hooksDir -Force | Out-Null
    }
    
    $hooksYaml = @"
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
"@
    
    $hooksYaml | Out-File -FilePath $hooksConfig -Encoding UTF8
    Write-Ok "Hooks enabled"
} else {
    Write-Ok "Hooks config already exists"
}

# ============================================================================
# Step 11: Set theme
# ============================================================================
Write-Step "Setting Jamaica RBG theme..."

$configYaml = Join-Path $installDir "config.yaml"
$themeConfig = @"
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
"@
$themeConfig | Out-File -FilePath $configYaml -Encoding UTF8
Write-Ok "Theme set to Jamaica RBG"

# ============================================================================
# Step 12: Run doctor
# ============================================================================
Write-Step "Running health check..."

Push-Location $installDir
$pythonExe = Join-Path $venvDir "Scripts" "python.exe"
& $pythonExe -c @"
import sys
sys.path.insert(0, '.')
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
"@
Pop-Location

if ($LASTEXITCODE -eq 0) {
    Write-Ok "All systems healthy"
} else {
    Write-Warn "Some checks failed. Run 'triangulum doctor' for details."
}

# ============================================================================
# Complete
# ============================================================================
Write-Host ""
Write-Host "$Bold╔══════════════════════════════════════════════════════════════╗$Reset"
Write-Host "$Bold║  Installation Complete!                                    ║$Reset"
Write-Host "$Bold╠══════════════════════════════════════════════════════════════╣$Reset"
Write-Host "$Bold║  Run one of these commands:                                ║$Reset"
Write-Host "$Bold║                                                              ║$Reset"
Write-Host "$Bold║    triangulum doctor    — verify installation              ║$Reset"
Write-Host "$Bold║    triangulum init      — create workspace                 ║$Reset"
Write-Host "$Bold║    triangulum run       — start the gateway                ║$Reset"
Write-Host "$Bold║    hermes desktop       — open multi-chat desktop          ║$Reset"
Write-Host "$Bold║                                                              ║$Reset"
Write-Host "$Bold║  Restart your terminal first if triangulum is not found.   ║$Reset"
Write-Host "$Bold╚══════════════════════════════════════════════════════════════╝$Reset"
Write-Host ""
