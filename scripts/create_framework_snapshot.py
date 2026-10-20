#!/usr/bin/env python3
"""Create a minimal verified framework-contract snapshot for offline validation."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path


def git_text(repo: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(repo), *args],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip() or "git command failed")
    return result.stdout


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--repository-url", required=True)
    parser.add_argument("--commit", required=True)
    args = parser.parse_args()

    repo = args.repo.resolve()
    resolved = git_text(repo, "rev-parse", "--verify", f"{args.commit}^{{commit}}").strip()
    if resolved != args.commit:
        raise RuntimeError(f"commit resolved to {resolved}, expected {args.commit}")
    contract = git_text(repo, "show", f"{args.commit}:framework.yaml")
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    (output / "framework.yaml").write_text(contract, encoding="utf-8")
    metadata = {
        "schema_version": 1,
        "repository": args.repository_url,
        "commit": args.commit,
        "framework_yaml_sha256": hashlib.sha256(contract.encode("utf-8")).hexdigest(),
    }
    (output / "snapshot.json").write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(f"WROTE: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

