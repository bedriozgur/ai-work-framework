#!/usr/bin/env python3
"""Create a minimal verified framework-contract snapshot for offline validation."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from urllib.parse import urlparse


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


def normalize_repository(value: str) -> str:
    value = value.strip().rstrip("/")
    if value.endswith(".git"):
        value = value[:-4]
    if value.startswith("git@") and ":" in value:
        host, path = value[4:].split(":", 1)
        value = f"https://{host}/{path}"
    elif value.startswith("ssh://git@"):
        parsed = urlparse(value)
        value = f"https://{parsed.hostname or ''}{parsed.path}"
    parsed = urlparse(value)
    if parsed.scheme in {"http", "https"} and parsed.hostname:
        return f"https://{parsed.hostname.lower()}{parsed.path.rstrip('/')}"
    return value


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--repository-url", required=True)
    parser.add_argument("--commit", required=True)
    parser.add_argument("--force", action="store_true", help="replace an existing snapshot")
    args = parser.parse_args()

    repo = args.repo.resolve()
    origin = git_text(repo, "config", "--get", "remote.origin.url").strip()
    if not origin:
        raise RuntimeError("framework repository has no remote.origin.url")
    if normalize_repository(origin) != normalize_repository(args.repository_url):
        raise RuntimeError(
            f"repository URL {args.repository_url!r} does not match local origin {origin!r}"
        )
    resolved = git_text(repo, "rev-parse", "--verify", f"{args.commit}^{{commit}}").strip()
    if resolved != args.commit:
        raise RuntimeError(f"commit resolved to {resolved}, expected {args.commit}")
    contract = git_text(repo, "show", f"{args.commit}:framework.yaml")
    output = args.output.resolve()
    targets = (output / "framework.yaml", output / "snapshot.json")
    existing = [str(path) for path in targets if path.exists()]
    if existing and not args.force:
        raise RuntimeError("snapshot target exists; use --force to replace: " + ", ".join(existing))
    output.mkdir(parents=True, exist_ok=True)
    (output / "framework.yaml").write_text(contract, encoding="utf-8")
    metadata = {
        "schema_version": 1,
        "repository": normalize_repository(args.repository_url),
        "commit": args.commit,
        "framework_yaml_sha256": hashlib.sha256(contract.encode("utf-8")).hexdigest(),
    }
    metadata_raw = json.dumps(metadata, indent=2, sort_keys=True) + "\n"
    (output / "snapshot.json").write_text(metadata_raw, encoding="utf-8")
    print(f"WROTE: {output}")
    print(f"SNAPSHOT_JSON_SHA256: {hashlib.sha256(metadata_raw.encode('utf-8')).hexdigest()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
