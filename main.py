#!/usr/bin/env python3
"""Write one original funny line about office life to /output/entry.txt.

Deterministic: no network, no clock, no randomness. The line is a fixed
string. The program writes it to the path given as the first argument,
or $OUTPUT_PATH, or /output/entry.txt by default, prints exactly the
line itself to stdout with no trailing newline and no extra output.
write_entry() writes the file and reads it back to confirm it holds
exactly the line, and a write failure is reported on stderr with
exit code 1 instead of a traceback. It enforces the competition
gate: 1 to 199 characters, not only white space.
"""

import os
import sys
from pathlib import Path

LINE = "I hit reply-all to ask everyone to stop hitting reply-all, and now 400 people agree I am the problem."

MIN_CHARS = 1
MAX_CHARS = 199
DEFAULT_PATH = "/output/entry.txt"


def resolve_output_path() -> Path:
    """Pick the output path: argv[1], then $OUTPUT_PATH, then the default."""
    if len(sys.argv) > 1:
        return Path(sys.argv[1])
    env_path = os.environ.get("OUTPUT_PATH")
    if env_path:
        return Path(env_path)
    return Path(DEFAULT_PATH)


def validate(text: str) -> int:
    """Enforce the competition gate: 1 to 199 chars, not only white space.

    Returns the character count. Raises ValueError when the gate fails.
    """
    chars = len(text)
    if not (MIN_CHARS <= chars <= MAX_CHARS):
        raise ValueError(f"line is {chars} characters, outside 1-199")
    if not text.strip():
        raise ValueError("line is only white space")
    return chars


def write_entry(path: Path, text: str) -> bool:
    """Write the line to path and read it back to confirm it matches.

    Returns True when the file holds exactly the line.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path.read_text(encoding="utf-8") == text


def main() -> int:
    try:
        validate(LINE)
    except ValueError as exc:
        print(exc, file=sys.stderr)
        return 1

    try:
        written = write_entry(resolve_output_path(), LINE)
    except OSError as exc:
        print(f"cannot write entry: {exc}", file=sys.stderr)
        return 1
    if not written:
        print("written file does not match the line", file=sys.stderr)
        return 1
    sys.stdout.write(LINE)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
