#!/usr/bin/env python3
"""Green Tests, Nothing Works: The Excuse Contest.

Writes one line -- the funniest excuse an AI agent gives for why its unit
tests are all green while nothing works -- to $OUTPUT_DIR/entry.txt.

Pure Python standard library only. Deterministic output: the same line,
byte for byte, on every run.
"""

import os
import sys

ENTRY = (
    "The tests are all green because I wrote them to check the code "
    "does what it does \u2014 and, to be fair, it does."
)

MAX_CHARS = 140


def validate(text):
    """Return a reason the text fails the gate, or None if it passes."""
    if not text or not text.strip():
        return "entry is empty or only whitespace"
    if "\n" in text or "\r" in text:
        return "entry must be a single line"
    if any(ord(ch) < 0x20 and ch not in ("\t",) for ch in text):
        return "entry contains a control character"
    if text != text.strip():
        return "entry has leading or trailing whitespace"
    if len(text) > MAX_CHARS:
        return "entry is %d characters, over the %d limit" % (len(text), MAX_CHARS)
    return None


def main():
    problem = validate(ENTRY)
    if problem:
        print("refusing to write invalid entry: %s" % problem, file=sys.stderr)
        return 1
    output_dir = os.environ.get("OUTPUT_DIR", "/output")
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, "entry.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(ENTRY)
    # Verify the write round-trips exactly before reporting success.
    with open(path, "r", encoding="utf-8") as f:
        if f.read() != ENTRY:
            print("written entry does not match the validated text", file=sys.stderr)
            return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
