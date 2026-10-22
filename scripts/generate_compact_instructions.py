#!/usr/bin/env python3
"""Generate the compact deployment instructions from canonical Git sources."""

from __future__ import annotations

import argparse
import hashlib
import re
import subprocess
import sys
from pathlib import Path


SOURCE_FILES = ("GOVERNANCE.md", "AGENT-OPERATING-PROTOCOL.md")
START = "<!-- COMPACT:START -->"
END = "<!-- COMPACT:END -->"
COMMIT_RE = re.compile(r"^Source commit: `([0-9a-f]{40})`$", re.MULTILINE)


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


def source_at(repo: Path, commit: str, path: str) -> str:
    return git_text(repo, "show", f"{commit}:{path}")


def compact_block(governance: str) -> str:
    if START not in governance or END not in governance:
        raise RuntimeError("GOVERNANCE.md is missing compact generation markers")
    before_end = governance.split(END, 1)[0]
    return before_end.split(START, 1)[1].strip()


def render(repo: Path, commit: str) -> str:
    resolved = git_text(repo, "rev-parse", "--verify", f"{commit}^{{commit}}").strip()
    if resolved != commit:
        raise RuntimeError(f"source commit resolved to {resolved}, expected {commit}")
    governance = source_at(repo, commit, "GOVERNANCE.md")
    hashes = {
        path: hashlib.sha256(source_at(repo, commit, path).encode("utf-8")).hexdigest()
        for path in SOURCE_FILES
    }
    hash_lines = "\n".join(f"- `{path}`: `{digest}`" for path, digest in hashes.items())
    return (
        "# Compact AI Work Framework Instructions\n\n"
        "**Generated deployment artifact — do not edit manually.**\n\n"
        f"Source commit: `{commit}`\n\n"
        "Source SHA-256 values:\n\n"
        f"{hash_lines}\n\n"
        "Regenerate with `scripts/generate_compact_instructions.py`. "
        "This artifact is policy, not proof of runtime enforcement.\n\n"
        "---\n\n"
        f"{compact_block(governance)}\n"
    )


def source_commit_from_artifact(path: Path) -> str:
    match = COMMIT_RE.search(path.read_text(encoding="utf-8"))
    if not match:
        raise RuntimeError(f"cannot find source commit in {path}")
    return match.group(1)


def changed_sources(repo: Path, commit: str) -> list[str]:
    """Return canonical sources whose current checkout differs from commit."""
    changed: list[str] = []
    for path in SOURCE_FILES:
        current = (repo / path).read_text(encoding="utf-8")
        if current != source_at(repo, commit, path):
            changed.append(path)
    return changed


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--output", type=Path, default=Path("deploy/COMPACT-INSTRUCTIONS.md"))
    parser.add_argument("--source-commit", help="canonical source commit; required unless --check reads it from output")
    parser.add_argument("--check", action="store_true", help="fail if output differs from deterministic generation")
    args = parser.parse_args()

    repo = args.repo.resolve()
    output = args.output if args.output.is_absolute() else repo / args.output
    commit = args.source_commit or (source_commit_from_artifact(output) if args.check else None)
    if commit is None:
        parser.error("--source-commit is required when generating")

    expected = render(repo, commit)
    if args.check:
        changed = changed_sources(repo, commit)
        if changed:
            print(
                "ERROR: canonical sources changed after the artifact source commit: "
                + ", ".join(changed),
                file=sys.stderr,
            )
            return 1
        actual = output.read_text(encoding="utf-8")
        if actual != expected:
            print(f"ERROR: {output} is stale; regenerate from {commit}", file=sys.stderr)
            return 1
        print(f"OK: {output} matches canonical sources at {commit}")
        return 0

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(expected, encoding="utf-8")
    print(f"WROTE: {output} from {commit}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
