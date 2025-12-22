#!/usr/bin/env python3
"""Pull required Ollama models for local experiments.

- Reads configured models from config/llm_config.yaml (via src.utils.config.load_config)
- Pulls only provider=ollama models (or an explicit subset passed on CLI)

Usage:
  python scripts/pull_ollama_models.py
  python scripts/pull_ollama_models.py --models llama32 qwen25_coder_7b

Notes:
- Requires the Ollama CLI (`ollama`) installed and the service running.
- This downloads model weights; it can take time and disk space.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path
from typing import List

# Add project root to path so `import src...` works when running as a script
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.utils.config import load_config


def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Pull Ollama models used in experiments")
    p.add_argument(
        "--models",
        nargs="+",
        default=None,
        help="Model names as defined in config/llm_config.yaml (default: all ollama models)",
    )
    p.add_argument(
        "--dry-run",
        action="store_true",
        help="Print what would be pulled without downloading",
    )
    return p.parse_args()


def _run(cmd: List[str]) -> int:
    proc = subprocess.run(cmd)
    return int(proc.returncode)


def main() -> int:
    args = _parse_args()
    cfg = load_config()

    selected_names = list(args.models) if args.models else list(cfg.llm_models.keys())

    # Resolve to actual Ollama model identifiers (e.g., llama3.2:latest)
    ollama_models: List[str] = []
    non_ollama: List[str] = []
    missing: List[str] = []

    for name in selected_names:
        mcfg = cfg.llm_models.get(name)
        if not mcfg:
            missing.append(name)
            continue
        if mcfg.provider != "ollama":
            non_ollama.append(name)
            continue
        ollama_models.append(mcfg.model)

    if missing:
        print("ERROR: Unknown model names in config/llm_config.yaml: " + ", ".join(missing), file=sys.stderr)
        return 2

    if non_ollama:
        print("Skipping non-Ollama models: " + ", ".join(non_ollama))

    if not ollama_models:
        print("No Ollama models to pull.")
        return 0

    # Deduplicate while preserving order
    seen = set()
    ordered = []
    for m in ollama_models:
        if m in seen:
            continue
        seen.add(m)
        ordered.append(m)

    print("Models to pull:")
    for m in ordered:
        print(f"  - {m}")

    if args.dry_run:
        return 0

    # Best-effort: pull one by one
    for m in ordered:
        print(f"\n==> ollama pull {m}")
        rc = _run(["ollama", "pull", m])
        if rc != 0:
            print(f"ERROR: Failed to pull {m} (exit {rc})", file=sys.stderr)
            return rc

    print("\nDone.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
