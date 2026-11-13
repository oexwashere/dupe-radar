# Design notes

## Scope

Find duplicate files by content without deleting or moving anything.

## Implementation decisions

Files are grouped by size before hashing. Only groups with matching sizes are hashed, using 1 MiB chunks and SHA-256. Directory symlinks are never followed; unreadable files and directories are reported rather than silently discarded.

## Boundaries

The estimate describes logical duplicate bytes, not guaranteed disk savings. Hard links, sparse files, compression, and filesystem deduplication can change physical storage use. Files may change during a scan. No files are deleted, moved, or modified.

## Verification

The Python unittest suite uses deterministic fixtures and temporary directories for filesystem tests.

Tests describe expected behavior rather than depending on a live external service. CI configuration is included, but remote CI execution is not implied by local test results.
