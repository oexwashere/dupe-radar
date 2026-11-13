import argparse
import fnmatch
import hashlib
import json
import os
from pathlib import Path


def digest(path):
    result = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            result.update(chunk)
    return result.hexdigest()


def scan(root, ignore=(".git", "node_modules", ".venv")):
    root = Path(root)
    if root.is_symlink() or not root.is_dir():
        raise ValueError("Choose a real directory, not a symlink.")
    sizes = {}
    errors = []
    count = 0

    def failed(error):
        errors.append({"path": str(error.filename), "error": str(error)})

    for directory, dirs, files in os.walk(root, followlinks=False, onerror=failed):
        dirs[:] = sorted(
            d
            for d in dirs
            if not (Path(directory) / d).is_symlink()
            and not any(fnmatch.fnmatch(d, p) for p in ignore)
        )
        for name in sorted(files):
            path = Path(directory) / name
            if path.is_symlink() or any(fnmatch.fnmatch(name, p) for p in ignore):
                continue
            try:
                if not path.is_file():
                    continue
                size = path.stat().st_size
                count += 1
                sizes.setdefault(size, []).append(path)
            except OSError as e:
                failed(e)
    groups = []
    for size, paths in sorted(sizes.items()):
        if len(paths) < 2:
            continue
        hashes = {}
        for path in paths:
            try:
                hashes.setdefault(digest(path), []).append(str(path.relative_to(root)))
            except OSError as e:
                failed(e)
        for checksum, matches in sorted(hashes.items()):
            if len(matches) > 1:
                groups.append(
                    {
                        "size": size,
                        "sha256": checksum,
                        "files": sorted(matches),
                        "reclaimable_bytes": size * (len(matches) - 1),
                    }
                )
    return {
        "files_scanned": count,
        "groups": groups,
        "reclaimable_bytes": sum(g["reclaimable_bytes"] for g in groups),
        "errors": errors,
    }


def main():
    p = argparse.ArgumentParser(description="Read-only duplicate file finder.")
    p.add_argument("directory")
    p.add_argument("--ignore", action="append", default=[])
    a = p.parse_args()
    try:
        report = scan(a.directory, (".git", "node_modules", ".venv", *a.ignore))
        print(json.dumps(report, indent=2))
        if report["errors"]:
            p.exit(1)
    except (OSError, ValueError) as e:
        p.exit(2, f"Error: {e}\n")


if __name__ == "__main__":
    main()
