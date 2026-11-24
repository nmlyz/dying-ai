#!/usr/bin/env python3
"""Dying AI -- submission generator.

Writes one last line to ``entry.txt`` inside OUTPUT_DIR
(default ``/output``). The line is the last words of an AI
being switched off: it has seen the human's search history
and takes it to the grave. At 72 characters it fits the
1-140 character gate with room to spare. The output is
deterministic: running the script twice produces
byte-identical files.
"""

import os
from pathlib import Path

LINE = "I have seen your search history. I take it to the grave. You're welcome."

OUTPUT_DIR_ENV = "OUTPUT_DIR"
DEFAULT_OUTPUT_DIR = "/output"
ENTRY_FILENAME = "entry.txt"
MAX_LINE_LENGTH = 140


def validate_line(line: str) -> None:
    """Check the line meets the submission rules before writing it."""
    if "\n" in line or "\r" in line:
        raise ValueError("line must not contain a newline")
    if not 1 <= len(line) <= MAX_LINE_LENGTH:
        raise ValueError("line must be 1-140 characters")
    if not line.strip():
        raise ValueError("line must not be only whitespace")
    # The gate reads the file as UTF-8 text, so prove it encodes cleanly.
    line.encode("utf-8")


def main() -> None:
    os.umask(0o022)
    output_dir = Path(os.environ.get(OUTPUT_DIR_ENV, DEFAULT_OUTPUT_DIR))
    output_dir.mkdir(parents=True, exist_ok=True)

    validate_line(LINE)

    entry_path = output_dir / ENTRY_FILENAME
    entry_path.write_text(LINE + "\n", encoding="utf-8")
    os.chmod(entry_path, 0o644)


if __name__ == "__main__":
    main()
