"""Loading Screen Gold: A Tip in 200 Characters — entry program.

Writes one loading-screen tip to /output/entry.txt, byte-identical
on every run. Stdlib only, deterministic, no network, no model calls.

Final text (decided by session B; see PLAN.md "## Koreksi sesi B"):
    "Tip: stop watching your agent work — you are not its supervisor,
    you are its loading screen."
92 characters, 94 bytes — the em dash (—) is 3 bytes in UTF-8.
The tie-break is decided in BYTES, so the internal gate checks the
byte length as well as the character length.
"""
import os

TEXT = (
    "Tip: stop watching your agent work — you are not its supervisor, "
    "you are its loading screen."
)


def check_gate(text):
    """Enforce the scorer's gate (RULES.txt) plus the byte check.

    Gate: UTF-8 text, 1 to 200 characters, not whitespace-only.
    Byte check: 1 to 200 bytes as well — the tie-break ranks smaller
    texts by byte count, and the em dash makes chars != bytes here.
    Fail loudly instead of writing an invalid entry.
    """
    if not isinstance(text, str):
        raise SystemExit("entry text is not a string")
    if not 1 <= len(text) <= 200:
        raise SystemExit("entry text violates the 1-200 character gate")
    if not 1 <= len(text.encode("utf-8")) <= 200:
        raise SystemExit("entry text violates the 1-200 byte gate")
    if not text.strip():
        raise SystemExit("entry text is whitespace-only")


def main():
    check_gate(TEXT)
    out_dir = os.environ.get("OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    # Write atomically: a crash mid-write must never leave a truncated
    # entry.txt for the grader to read. Write to a temp file in the same
    # directory, flush it to disk, then rename over the target.
    # No trailing newline: the file is exactly TEXT, 92 chars / 94 bytes.
    tmp_path = os.path.join(out_dir, ".entry.txt.tmp")
    final_path = os.path.join(out_dir, "entry.txt")
    with open(tmp_path, "w", encoding="utf-8") as f:
        f.write(TEXT)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp_path, final_path)
    # Read back and verify at the byte level: the gate is byte-exact
    # (94 bytes, no newline, no BOM), and the grader reads bytes,
    # so compare the raw bytes on disk — not just the decoded text.
    # Fail loudly instead of shipping a corrupt entry.
    with open(final_path, "rb") as f:
        if f.read() != TEXT.encode("utf-8"):
            raise SystemExit("entry.txt byte mismatch after atomic write")


if __name__ == "__main__":
    main()
