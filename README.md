# Dupe Radar

Find duplicate files by content without deleting or moving anything.

## Features

- Size-first grouping to avoid hashing unrelated files
- Streaming SHA-256 hashing for large files
- Symlink exclusion and configurable ignore patterns
- Reclaimable-byte estimates and explicit unreadable-file reports

## Get started

Requires **Python 3.11+**. No third-party packages or installation step.

```sh
git clone https://github.com/oexwashere/dupe-radar.git
cd dupe-radar
python3 app.py --help
```

## Examples

```sh
python3 app.py examples/files
python3 app.py /path/to/project --ignore '*.log' --ignore '*.tmp'
```

Example files are intentionally small and contain no real credentials or user data. Output goes to stdout, making it easy to redirect into a report. Errors go to stderr.

## Verify

```sh
python3 -m unittest -v
python3 -m py_compile app.py
```

Tests use temporary directories when filesystem access is needed. They do not modify your working data or require a network connection. GitHub Actions is configured for Python 3.11, 3.12, and 3.13.

## Architecture

`app.py` contains the reusable functions and CLI entry point. `test_app.py` exercises boundary conditions and representative workflows. `examples/` contains runnable fixtures.

Files are grouped by size before hashing. Only groups with matching sizes are hashed, using 1 MiB chunks and SHA-256. Directory symlinks are never followed; unreadable files and directories are reported rather than silently discarded.

## Exit codes

`0` means the requested operation completed; `2` means a usage, input, or filesystem failure. `1` means a scan completed with unreadable-file errors.

## Limitations and data handling

The estimate describes logical duplicate bytes, not guaranteed disk savings. Hard links, sparse files, compression, and filesystem deduplication can change physical storage use. Files may change during a scan. No files are deleted, moved, or modified.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Keep changes focused and include a regression test when behavior changes.

## License

[MIT](LICENSE) · oexwashere
