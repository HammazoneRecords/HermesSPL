#!/usr/bin/env python3
"""Triangulum One-Liner Installer.

Cross-platform bootstrap for HermesSPL Triangulum. Detects the host OS,
fetches the correct installer, runs it, and verifies with `triangulum doctor`.

    python scripts/triangulum-install.py
    curl -fsSL https://hermes-spl.dev/install | python3

Flags:
    --force      Reinstall even if a triangulum binary already exists.
    --dev        Install the development (preview) channel instead of stable.
    --no-hooks   Skip post-install hook registration.
    --dry-run    Print what would happen without executing anything.

Exit codes:
    0   installed and verified
    1   install failed or verification failed
    2   user aborted / nothing to do
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import shutil
import ssl
import stat
import subprocess
import sys
import tempfile
import textwrap
from pathlib import Path
from urllib.error import URLError
from urllib.request import urlopen

__version__ = "1.0.0"

DEFAULT_BASE_URL = "https://install.hermes-spl.dev"
DEV_BASE_URL = "https://install-dev.hermes-spl.dev"

TRIANGULUM_REPO = "nousresearch/hermes-agent"


# ---------------------------------------------------------------------------
# Platform detection
# ---------------------------------------------------------------------------

def detect_target() -> tuple[str, str, str]:
    """Return (os_id, arch_id, installer_suffix) for the current host.

    os_id:       "linux" | "macos" | "windows"
    arch_id:     "x86_64" | "aarch64" | "arm64"
    suffix:      "" | ".exe"
    """
    system = platform.system().lower()
    machine = platform.machine().lower()

    if system == "linux":
        os_id = "linux"
        suffix = ""
    elif system == "darwin":
        os_id = "macos"
        suffix = ""
    elif system == "windows":
        os_id = "windows"
        suffix = ".exe"
    else:
        print(f"error: unsupported operating system: {system}", file=sys.stderr)
        sys.exit(1)

    if machine in ("x86_64", "amd64"):
        arch_id = "x86_64"
    elif machine in ("aarch64", "arm64"):
        arch_id = "arm64" if os_id == "macos" else "aarch64"
    else:
        print(f"error: unsupported architecture: {machine}", file=sys.stderr)
        sys.exit(1)

    return os_id, arch_id, suffix


# ---------------------------------------------------------------------------
# Download helpers
# ---------------------------------------------------------------------------

def _fetch(url: str, timeout: int = 120) -> bytes:
    """GET *url* and return raw bytes. Fails loudly on any error."""
    ctx = ssl.create_default_context()
    try:
        with urlopen(url, timeout=timeout, context=ctx) as resp:
            return resp.read()
    except (URLError, OSError) as exc:
        print(f"error: download failed: {exc}", file=sys.stderr)
        sys.exit(1)


def _fetch_json(url: str, timeout: int = 30) -> dict:
    data = _fetch(url, timeout)
    try:
        return json.loads(data.decode())
    except (ValueError, UnicodeDecodeError) as exc:
        print(f"error: bad manifest JSON: {exc}", file=sys.stderr)
        sys.exit(1)


def download_with_progress(url: str, dest: Path) -> None:
    """Download *url* to *dest* with a simple CLI progress indicator."""
    ctx = ssl.create_default_context()
    with urlopen(url, timeout=180, context=ctx) as resp:
        total = int(resp.headers.get("Content-Length", 0))
        downloaded = 0
        chunk_size = 64 * 1024
        with dest.open("wb") as fh:
            while True:
                chunk = resp.read(chunk_size)
                if not chunk:
                    break
                fh.write(chunk)
                downloaded += len(chunk)
                if total:
                    pct = downloaded * 100 // total
                    bar = "#" * (pct // 2) + "-" * (50 - pct // 2)
                    sys.stdout.write(f"\r  [{bar}] {pct}%")
                    sys.stdout.flush()
    if total:
        sys.stdout.write("\n")


# ---------------------------------------------------------------------------
# Install logic
# ---------------------------------------------------------------------------

def find_existing_install() -> Path | None:
    """Return the path to an existing `triangulum` binary, or None."""
    return shutil.which("triangulum")


def compute_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(128 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def run_installer(binary_path: Path, no_hooks: bool) -> None:
    """Execute the downloaded installer binary with the right flags."""
    cmd = [str(binary_path), "install"]
    if no_hooks:
        cmd.append("--no-hooks")
    print(f"  Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, check=False)
    if result.returncode != 0:
        print("error: installer exited with code", result.returncode, file=sys.stderr)
        sys.exit(1)


def verify_install() -> bool:
    """Run `triangulum doctor` and check that all checks pass."""
    doctor = shutil.which("triangulum")
    if doctor is None:
        print("  verification: triangulum not found on PATH after install", file=sys.stderr)
        return False

    try:
        proc = subprocess.run(
            [doctor, "doctor"],
            capture_output=True,
            text=True,
            timeout=60,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        print(f"  verification: triangulum doctor failed: {exc}", file=sys.stderr)
        return False

    print(proc.stdout)
    if proc.returncode != 0:
        if proc.stderr:
            print(proc.stderr, file=sys.stderr)
        return False
    return True


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="triangulum-install",
        description=textwrap.dedent(__doc__).strip(),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument(
        "--force",
        action="store_true",
        help="Reinstall even if triangulum is already on PATH.",
    )
    p.add_argument(
        "--dev",
        action="store_true",
        help="Install the development (preview) channel.",
    )
    p.add_argument(
        "--no-hooks",
        action="store_true",
        help="Skip post-install hook registration.",
    )
    p.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the planned action without downloading or executing anything.",
    )
    p.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    return p


def main() -> None:
    args = build_parser().parse_args()

    os_id, arch_id, suffix = detect_target()
    channel = "dev" if args.dev else "stable"
    base_url = DEV_BASE_URL if args.dev else DEFAULT_BASE_URL

    print(f"Triangulum Installer {__version__}")
    print(f"  channel : {channel}")
    print(f"  target  : {os_id} / {arch_id}")

    # ---- preflight: already installed? --------------------------------
    existing = find_existing_install()
    if existing and not args.force:
        print(f"  triangulum already installed at {existing}")
        print("  (use --force to reinstall)")
        sys.exit(2)

    manifest_url = f"{base_url}/v1/{channel}/{os_id}/{arch_id}/manifest.json"
    installer_filename = f"triangulum-installer-{os_id}-{arch_id}{suffix}"
    installer_url = f"{base_url}/v1/{channel}/{os_id}/{arch_id}/{installer_filename}"

    if args.dry_run:
        print(f"  manifest : {manifest_url}")
        print(f"  source  : {installer_url}")
        print("  [dry-run] would download and run the installer")
        sys.exit(0)

    manifest = _fetch_json(manifest_url)
    installer_filename = manifest.get("installer") or installer_filename
    installer_url = manifest.get("url") or f"{base_url}/v1/{channel}/{os_id}/{arch_id}/{installer_filename}"
    expected_sha = manifest.get("sha256", "")

    print(f"  manifest : {manifest_url}")
    print(f"  source  : {installer_url}")

    # ---- download ----------------------------------------------------
    tmp_dir = Path(tempfile.mkdtemp(prefix="triangulum-install-"))
    local_path = tmp_dir / installer_filename
    try:
        print("  downloading installer...")
        download_with_progress(installer_url, local_path)

        if expected_sha:
            actual_sha = compute_sha256(local_path)
            if actual_sha != expected_sha:
                print(
                    f"error: checksum mismatch\n  expected: {expected_sha}\n  got:      {actual_sha}",
                    file=sys.stderr,
                )
                sys.exit(1)
            print("  checksum OK")

        # Make executable on POSIX.
        if os_id != "windows":
            mode = local_path.stat().st_mode
            local_path.chmod(mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

        # ---- run installer -------------------------------------------
        print("  launching installer...")
        run_installer(local_path, args.no_hooks)

        # ---- verify --------------------------------------------------
        print("  verifying with triangulum doctor...")
        if verify_install():
            print("  ✓ triangulum installed and verified")
        else:
            print("error: verification failed", file=sys.stderr)
            sys.exit(1)
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)


if __name__ == "__main__":
    main()
