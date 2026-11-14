#!/usr/bin/env python3
"""Install four review assets. Dry-run by default; never touch settings or permissions."""
from __future__ import annotations

import argparse
import os
import shutil
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

ASSETS = (
    "rules/review-first.md",
    "agents/review-auditor.md",
    "skills/review-package/SKILL.md",
    "skills/review-package/templates.md",
)
SOURCE = Path(__file__).resolve().parents[1] / "claude"


def safe_destination(target: Path, relative: str) -> Path:
    """Refuse symlinks within the managed destination, including the root."""
    destination = target / relative
    if target.is_symlink():
        raise ValueError(f"Refusing symlink target: {target}")
    current = target
    if current.exists() and not current.is_dir():
        raise ValueError(f"Target is not a directory: {current}")
    for part in Path(relative).parts:
        current = current / part
        if current.is_symlink():
            raise ValueError(f"Refusing symlink: {current}")
        if current != destination and current.exists() and not current.is_dir():
            raise ValueError(f"Parent is not a directory: {current}")
    if destination.exists() and not destination.is_file():
        raise ValueError(f"Destination is not a file: {destination}")
    return destination


def install(source: Path, target: Path, *, apply: bool = False,
            overwrite: bool = False) -> list[str]:
    target = target.expanduser().absolute()
    plan = []
    conflicts = []
    # Full preflight: a missing source or refused conflict causes no writes.
    for relative in ASSETS:
        origin = source / relative
        if not origin.is_file():
            raise ValueError(f"Missing source: {origin}")
        content = origin.read_bytes()
        destination = safe_destination(target, relative)
        previous = destination.read_bytes() if destination.exists() else None
        action = "KEEP" if previous == content else "CREATE" if previous is None else "REPLACE"
        plan.append((relative, destination, content, previous, action))
        if action == "REPLACE":
            conflicts.append(relative)
    messages = [f"{action}: {destination}" for _, destination, _, _, action in plan]
    if not apply:
        if conflicts and not overwrite:
            messages.append("Conflicts: --apply will refuse; compare manually or add --overwrite for backups.")
        return ["DRY RUN: no files changed.", *messages]
    if conflicts and not overwrite:
        raise ValueError("Existing differing files; no files changed: " + ", ".join(conflicts))

    backup_root = None
    if conflicts:
        backup_parent = target / ".review-kit-backups"
        if backup_parent.is_symlink():
            raise ValueError(f"Refusing symlink backup directory: {backup_parent}")
        backup_parent.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ-")
        backup_root = Path(tempfile.mkdtemp(prefix=stamp, dir=backup_parent))
    for relative, destination, content, previous, action in plan:
        if action == "KEEP":
            continue
        safe_destination(target, relative)
        current = destination.read_bytes() if destination.exists() else None
        if current != previous:
            raise ValueError(f"Destination changed during installation: {destination}")
        if action == "REPLACE":
            backup = backup_root / relative
            backup.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(destination, backup)
        destination.parent.mkdir(parents=True, exist_ok=True)
        temporary = None
        try:
            with tempfile.NamedTemporaryFile(dir=destination.parent, delete=False) as handle:
                temporary = Path(handle.name)
                handle.write(content)
            # Atomic per file; this is not a transaction over all four files.
            os.replace(temporary, destination)
        finally:
            if temporary is not None and temporary.exists():
                temporary.unlink()
    if backup_root:
        messages.append(f"Backups: {backup_root}")
    return ["APPLIED: review assets only; settings and permissions unchanged.", *messages]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", type=Path, default=Path.home() / ".claude")
    parser.add_argument("--apply", action="store_true", help="Write files; otherwise preview only")
    parser.add_argument("--overwrite", action="store_true", help="Back up and replace conflicting assets")
    args = parser.parse_args()
    try:
        print("\n".join(install(SOURCE, args.target, apply=args.apply, overwrite=args.overwrite)))
        return 0
    except (OSError, ValueError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
