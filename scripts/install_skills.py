#!/usr/bin/env python3
"""Link the complete library into an agent skill directory without overwrites."""

import argparse
import os
from pathlib import Path
import sys


def install(source_root: Path, target_dir: Path) -> tuple[int, int]:
    source_root = source_root.expanduser().resolve(strict=True)
    target_dir = target_dir.expanduser().resolve()
    if target_dir == source_root or source_root in target_dir.parents:
        raise ValueError("Choose an installation directory outside the library checkout.")

    skills = sorted(path.parent for path in source_root.rglob("SKILL.md"))
    if not skills:
        raise ValueError("No skills found in the source library.")
    names = [path.name for path in skills]
    if len(names) != len(set(names)):
        raise ValueError("Skill folder names must be unique across the library.")

    # Check every destination before creating links, so known conflicts are atomic.
    pending = []
    unchanged = 0
    for source in skills:
        destination = target_dir / source.name
        if os.path.lexists(destination):
            if destination.is_symlink() and destination.resolve() == source.resolve():
                unchanged += 1
                continue
            raise FileExistsError(f"Will not overwrite existing skill: {destination}")
        pending.append((source, destination))

    target_dir.mkdir(parents=True, exist_ok=True)
    for source, destination in pending:
        destination.symlink_to(source, target_is_directory=True)
    return len(pending), unchanged


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target-dir", type=Path, required=True,
                        help="Agent's personal or project skill directory")
    args = parser.parse_args()
    try:
        created, unchanged = install(Path(__file__).resolve().parents[1], args.target_dir)
    except (OSError, ValueError) as error:
        print(f"Installation stopped: {error}", file=sys.stderr)
        return 1
    print(f"Created {created} links; {unchanged} already linked. No skills overwritten.")
    print("Keep this checkout in place: links and relative dependencies use it.")
    print("No BMAD, media tools, accounts or scheduled tasks were installed.")
    print("Restart your agent if needed, then invoke new-product-from-scratch.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
