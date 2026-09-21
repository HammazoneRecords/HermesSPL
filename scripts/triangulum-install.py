#!/usr/bin/env python3
"""
triangulum-install.py — HermesSPL one-liner bootstrap.

Clones the repo and runs the platform installer.

Windows:
    python -c "import urllib.request; exec(urllib.request.urlopen('https://raw.githubusercontent.com/HammazoneRecords/HermesSPL/main/scripts/triangulum-install.py').read())"

Linux / macOS:
    curl -fsSL https://raw.githubusercontent.com/HammazoneRecords/HermesSPL/main/scripts/triangulum-install.py | python3
"""

import os
import platform
import shutil
import subprocess
import sys
import tempfile
import urllib.request
from pathlib import Path

REPO_URL = "https://github.com/HammazoneRecords/HermesSPL.git"
INSTALL_DIR = Path.home() / ".hermes" / "HermesSPL"


def run(cmd, **kwargs):
    """Run a command, printing it first."""
    print(f"  $ {' '.join(cmd)}")
    result = subprocess.run(cmd, **kwargs)
    if result.returncode != 0:
        print(f"  command failed with exit code {result.returncode}")
        sys.exit(result.returncode)


def main():
    print("=== HermesSPL Triangulum Installer ===\n")

    system = platform.system().lower()
    if system == "windows":
        installer = ["powershell.exe", "-ExecutionPolicy", "Bypass", "-File", "scripts/install.ps1"]
    else:
        installer = ["bash", "scripts/install.sh"]

    # Clone repo
    if INSTALL_DIR.exists():
        print(f"  updating existing install at {INSTALL_DIR}")
        run(["git", "pull"], cwd=INSTALL_DIR)
    else:
        print(f"  cloning to {INSTALL_DIR}")
        run(["git", "clone", REPO_URL, str(INSTALL_DIR)])

    # Run installer
    print(f"\n  running installer...")
    run(installer, cwd=INSTALL_DIR)

    # Verify
    print(f"\n  verifying...")
    python_exe = INSTALL_DIR / ".venv" / ("Scripts" if system == "windows" else "bin") / ("python.exe" if system == "windows" else "python")
    if python_exe.exists():
        run([str(python_exe), "-c", 
             "import hooks.pre_tool_call.color_neutralizer; "
             "import hooks.pre_tool_call.solobic_cpu; "
             "import hooks.pre_tool_call.sfl_hook; "
             "import hooks.post_tool_call.rite_framework; "
             "import protocols.signal_protocol; "
             "import memory.drayl_backend; "
             "print('ALL_SYSTEMS_OK')"],
            cwd=INSTALL_DIR)
    else:
        print(f"  virtual environment not found at {python_exe}")
        print(f"  the installer may still be initializing. retry in a minute.")

    print(f"\n=== Installation Complete ===")
    print(f"  cd {INSTALL_DIR}")
    if system == "windows":
        print(f"  triangulum doctor")
    else:
        print(f"  ./triangulum doctor")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n  cancelled.")
        sys.exit(2)
    except Exception as e:
        print(f"\n  unexpected error: {e}", file=sys.stderr)
        sys.exit(1)
