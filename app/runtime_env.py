"""Tiny repo-local env loader.

The lab uses a checked-in `.env.example` and generated `.env` file to switch
between lite and Docker modes. We keep this dependency-free so both notebooks
and the FastAPI app can pick up the same runtime flags without asking users to
`source` anything manually.
"""
from __future__ import annotations

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def load_repo_env() -> None:
    env_path = ROOT / ".env"
    if not env_path.exists():
        return

    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if "#" in value:
            value = value.split("#", 1)[0].rstrip()
        os.environ.setdefault(key, value)
