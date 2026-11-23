#!/usr/bin/env python3
"""Dad Joke Showdown entry (u-mfnakmal-dad-joke-showdown-1d2ce3e5).

Writes one original dad joke to /output/entry.txt, after validating it
against the competition gate: UTF-8 text, 1-200 characters, not only
whitespace, exactly one line, no control characters.
"""

import os
import re

JOKE = "I put the turkey in timeout at dinner \u2014 it kept gobbling up all the attention."

OUTPUT_PATH = "/output/entry.txt"
MAX_CHARS = 200

# Any C0/C1 control character except none: a one-line joke has no use for
# tabs, NULs or other invisible bytes, and they would only muddy the read.
_CONTROL_RE = re.compile(r"[\x00-\x1f\x7f\x80-\x9f]")


def validate(text: str) -> None:
    """Raise ValueError if text fails the gate."""
    if not isinstance(text, str):
        raise ValueError("entry must be text")
    if not (1 <= len(text) <= MAX_CHARS):
        raise ValueError(f"entry must be 1-{MAX_CHARS} characters, got {len(text)}")
    if not text.strip():
        raise ValueError("entry must not be only whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be exactly one line")
    if _CONTROL_RE.search(text):
        raise ValueError("entry must not contain control characters")
    if text != text.strip():
        raise ValueError("entry must not start or end with whitespace")
    text.encode("utf-8")  # raises if not valid UTF-8 text


def main() -> None:
    validate(JOKE)
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="") as f:
        f.write(JOKE)
    # Read the file back and re-validate: what the judge reads is the file,
    # not the in-memory string, so the gate must pass on the bytes on disk.
    with open(OUTPUT_PATH, "rb") as f:
        raw = f.read()
    written = raw.decode("utf-8")
    validate(written)
    if written != JOKE:
        raise ValueError("round-trip mismatch: file content differs from joke")
    print(f"wrote {len(JOKE)} characters to {OUTPUT_PATH} (gate passed)")


if __name__ == "__main__":
    main()
