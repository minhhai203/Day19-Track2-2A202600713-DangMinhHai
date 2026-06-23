#!/usr/bin/env bash
# Lite path: pure Python, in-process Qdrant, SQLite Feast online store.
# No Docker, no GPU, no external services. ~60s on a clean machine.

set -euo pipefail

echo "[lite] Day 19 lightweight setup"
echo "[lite] Stack: fastembed + qdrant-client[memory] + rank-bm25 + feast(sqlite) + FastAPI"
echo

# ── 1. Python ───────────────────────────────────────────────────────────
command -v python3 >/dev/null 2>&1 || { echo "[lite] python3 not found. Install Python 3.10+."; exit 1; }
PY_VER=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
echo "[lite] Python $PY_VER detected"

# ── 2. venv ─────────────────────────────────────────────────────────────
PYTHON_BIN="${PYTHON_BIN:-python3.11}"
if [ ! -d ".venv" ]; then
  if command -v uv >/dev/null 2>&1; then
    echo "[lite] Creating venv with uv (faster)"
    uv venv --python "$PYTHON_BIN" .venv
  else
    echo "[lite] Creating venv with python -m venv"
    "$PYTHON_BIN" -m venv .venv
  fi
fi
# shellcheck source=/dev/null
source .venv/bin/activate

# ── 3. Install deps ─────────────────────────────────────────────────────
if command -v uv >/dev/null 2>&1; then
  uv pip install -r requirements.txt
else
  pip install -q -U pip
  pip install -q -r requirements.txt
fi

# ── 4. Convert Jupytext sources to .ipynb ───────────────────────────────
jupytext --to notebook --update notebooks/*.py 2>/dev/null || jupytext --to notebook notebooks/*.py

# ── 5. .env scaffold ────────────────────────────────────────────────────
[ -f .env ] || cp .env.example .env
grep -q '^POSTGRES_HOST_PORT=' .env || echo 'POSTGRES_HOST_PORT=15432' >> .env

# ── 6. Render Feast config for lite mode ────────────────────────────────
python scripts/render_feast_config.py --mode lite

# ── 7. Seed corpus + golden set ─────────────────────────────────────────
python scripts/seed_corpus.py

# ── 8. Smoke test ───────────────────────────────────────────────────────
python scripts/verify_lite.py

cat <<EOF

[lite] Done. Activate the venv and start working:

    source .venv/bin/activate
    make api       # start FastAPI on :8000
    make lab       # open Jupyter on :8888
    make benchmark # Precision@10 + latency table

Tip: read VIBE-CODING.md before starting NB1 — it tells you what to delegate
to your AI assistant and what to think through yourself.
EOF
