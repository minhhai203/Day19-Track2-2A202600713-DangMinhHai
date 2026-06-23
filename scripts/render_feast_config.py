"""Render Feast repo config for the current stack.

The lab supports two modes:
  - lite:  SQLite online store + file offline store
  - docker: Redis online store + Postgres offline store

This script rewrites `app/feast_repo/feature_store.yaml` so Feast always sees
the correct backend for the current setup. Keep the template simple and avoid
manual edits after switching modes; just rerun this script.
"""
from __future__ import annotations

import argparse
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FEAST_DIR = ROOT / "app" / "feast_repo"
CONFIG_PATH = FEAST_DIR / "feature_store.yaml"

LITE_CONFIG = """project: lab19
provider: local
registry: registry_lite.db
online_store:
  type: sqlite
  path: online_store_lite.db
offline_store:
  type: file
entity_key_serialization_version: 3
"""

DOCKER_CONFIG = """project: lab19
provider: local
registry: registry_docker.db
online_store:
  type: redis
  connection_string: localhost:6379
offline_store:
  type: postgres
  host: localhost
  port: {postgres_port}
  database: feast_offline
  user: feast
  password: feast
  sslmode: disable
  db_schema: public
entity_key_serialization_version: 3
"""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("lite", "docker"), default="lite")
    args = parser.parse_args()

    FEAST_DIR.mkdir(parents=True, exist_ok=True)
    postgres_port = os.getenv("POSTGRES_HOST_PORT", "15432")
    config = DOCKER_CONFIG.format(postgres_port=postgres_port) if args.mode == "docker" else LITE_CONFIG
    CONFIG_PATH.write_text(config, encoding="utf-8")
    print(f"Rendered Feast config -> {CONFIG_PATH} ({args.mode})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
