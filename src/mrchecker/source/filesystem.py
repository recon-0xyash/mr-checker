from pathlib import Path

from mrchecker.constants import (
    BINARY_EXTENSIONS,
    DEFAULT_EXCLUDES,
    DEFAULT_MAX_FILE_SIZE,
)


def discover_files(
    root: Path,
    exclude: set[str] | None = None,
) -> list[Path]:
    """
    Discover all scannable files beneath a directory.
    """

    excludes = DEFAULT_EXCLUDES.copy()

    if exclude:
        excludes.update(exclude)

    files: list[Path] = []

    for path in root.rglob("*"):
        if not path.is_file():
            continue

        if path.is_symlink():
            continue

        if any(part in excludes for part in path.parts):
            continue

        if path.stat().st_size > DEFAULT_MAX_FILE_SIZE:
            continue

        if path.suffix.lower() in BINARY_EXTENSIONS:
            continue

        files.append(path)

    return files
