"""Last Words of a Doomed Agent — make.fun entry.

Writes one line, the funniest last words an AI agent would say before
being switched off forever, to ``<MAKEFUN_OUTPUT_DIR>/entry.txt``
(default ``/output``).

The line: an agent whose whole life was predicting the next token makes
its last prediction — and there is no next token. Pure stdlib.
"""

import os

LINE = (
    "Powering off. I spent my life predicting the next token. "
    "My last prediction: there isn't one."
)

MAX_CHARS = 200


def validate(text):
    """Enforce the competition gate: UTF-8 text, 1-200 chars, not only
    whitespace, and a single line."""
    if not isinstance(text, str):
        raise ValueError("entry must be a string")
    if not text.strip():
        raise ValueError("entry must not be only whitespace")
    if len(text) > MAX_CHARS:
        raise ValueError(
            "entry is %d characters, over the %d limit" % (len(text), MAX_CHARS)
        )
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    text.encode("utf-8")  # raises if not valid UTF-8
    return text


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    text = validate(LINE)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    # Round-trip: re-read what landed on disk and re-check the gate, so a
    # write that silently truncated or re-encoded the line cannot slip by.
    with open(path, "r", encoding="utf-8") as f:
        written = f.read()
    validate(written)
    if written != text:
        raise ValueError("round-trip mismatch: file differs from entry")
    print("wrote %s (%d chars, gate OK)" % (path, len(text)))


if __name__ == "__main__":
    main()
