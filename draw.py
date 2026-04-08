#!/usr/bin/env python3
"""
draw.py — fills a GitHub contribution graph with backdated commits,
leaving a question mark cut out of the current visible year.

Uses git fast-import so that even 1,000,000 commits finish in ~1 minute.

Part of "What GitHub Can't See."

Run inside an initialized git repo:
    git init -b main
    git config user.name  "Your Name"
    git config user.email "your-github-email@example.com"
    python3 draw.py --dry-run    # preview
    python3 draw.py              # full send
"""

import os
import random
import subprocess
import sys
from datetime import datetime, timedelta

# ─── Configuration ──────────────────────────────────────────────

ACTIVE_PATTERN = "QUESTION"

# The total number of commits to create.
# Start small to see how it feels, then crank.
#   12_000    — decent statement, 15 yrs of history
#   100_000   — absurd, unmistakable
#   1_000_000 — full send. Takes ~1 min locally via fast-import.
TARGET_COMMITS = 99_999

# How many years before the current visible year to fill.
# 15 puts you around 2011 — well before most accounts existed.
YEARS_BACK = 15

# ─── Patterns (7 rows = Sun..Sat) ───────────────────────────────

LETTERS = {
    "C": [
        ".###.",
        "#...#",
        "#....",
        "#....",
        "#....",
        "#...#",
        ".###.",
    ],
    "O": [
        ".###.",
        "#...#",
        "#...#",
        "#...#",
        "#...#",
        "#...#",
        ".###.",
    ],
    "D": [
        "###..",
        "#..#.",
        "#...#",
        "#...#",
        "#...#",
        "#..#.",
        "###..",
    ],
    "E": [
        "#####",
        "#....",
        "#....",
        "####.",
        "#....",
        "#....",
        "#####",
    ],
    "R": [
        "####.",
        "#...#",
        "#...#",
        "####.",
        "#.#..",
        "#..#.",
        "#...#",
    ],
}

WORD = "CODER"

def get_word_cells(year):
    """Return set of dates in `year` that form WORD on the contribution graph."""
    # Find the first Sunday on/after Jan 1 of `year`
    jan1 = datetime(year, 1, 1)
    offset = (6 - jan1.weekday()) % 7  # weekday: Mon=0..Sun=6
    first_sunday = jan1 + timedelta(days=offset)

    letter_w = 5
    gap = 1
    total_w = len(WORD) * letter_w + (len(WORD) - 1) * gap  # 29
    start_week = max(0, (52 - total_w) // 2)  # center

    cells = set()
    for li, ch in enumerate(WORD):
        glyph = LETTERS[ch]
        base_week = start_week + li * (letter_w + gap)
        for col in range(letter_w):
            week_sunday = first_sunday + timedelta(weeks=base_week + col)
            for row in range(7):
                if glyph[row][col] == "#":
                    d = (week_sunday + timedelta(days=row)).date()
                    if d.year == year:
                        cells.add(d)
    return cells


PATTERNS = {
    "QUESTION": [
        ".###.",
        "#...#",
        "....#",
        "..##.",
        "..#..",
        ".....",
        "..#..",
    ],
    "EYE": [
        "..#..",
        ".#.#.",
        "#.#.#",
        "#.#.#",
        "#.#.#",
        ".#.#.",
        "..#..",
    ],
    "LINE": [
        "..#..",
        "..#..",
        "..#..",
        "..#..",
        "..#..",
        "..#..",
        "..#..",
    ],
}

MESSAGES = [
    "surface",
    "counted",
    "public trace",
    "recognized mark",
    "what was kept",
    "the visible part",
    "what the graph remembers",
    "above the waterline",
    "legible",
    "what survived",
    "the residue",
    "still here",
]

# ─── Pattern placement ──────────────────────────────────────────

def get_hole_cells(pattern, current_saturday):
    """Dates that must be LEFT EMPTY to form the pattern as negative space."""
    rows = len(pattern)
    cols = len(pattern[0])

    middle_week   = 26
    right_edge_wk = middle_week + (cols // 2)
    current_sunday = current_saturday - timedelta(days=6)

    holes = set()
    for col in range(cols):
        week_offset = right_edge_wk - col
        week_sunday = current_sunday - timedelta(weeks=week_offset)
        for row in range(rows):
            if pattern[row][col] == "#":
                holes.add((week_sunday + timedelta(days=row)).date())
    return holes


# ─── Schedule ───────────────────────────────────────────────────

def build_schedule():
    """
    Returns a list of datetime objects — one per commit to create.
    Density is derived from TARGET_COMMITS so the total lands close to target.
    """
    today = datetime.now()

    word_cells_2024 = get_word_cells(2024)
    word_cells_2025 = get_word_cells(2025)
    word_cells = word_cells_2024 | word_cells_2025

    rng = random.Random(1337)
    schedule = []

    eligible = [d for d in sorted(word_cells)
                if datetime(d.year, d.month, d.day) <= today]
    n = len(eligible)
    base_count = TARGET_COMMITS // n
    remainder = TARGET_COMMITS % n
    for idx, d in enumerate(eligible):
        base = datetime(d.year, d.month, d.day)
        count = base_count + (1 if idx < remainder else 0)
        for i in range(count):
            schedule.append(base + timedelta(seconds=i))

    return schedule


# ─── Fast-import writer ────────────────────────────────────────

def get_identity():
    try:
        name = subprocess.check_output(
            ["git", "config", "user.name"], text=True).strip()
    except subprocess.CalledProcessError:
        name = ""
    try:
        email = subprocess.check_output(
            ["git", "config", "user.email"], text=True).strip()
    except subprocess.CalledProcessError:
        email = ""
    if not name:
        name = "Anonymous"
    if not email:
        email = "anon@example.com"
    return name, email


def run_fast_import(schedule, dry_run=False):
    total = len(schedule)
    name, email = get_identity()

    if dry_run:
        print(f"Would create {total:,} commits via git fast-import.")
        print()
        print("Sample:")
        samples = [0, 1, 2, total // 4, total // 2, 3 * total // 4,
                   total - 2, total - 1]
        for idx in samples:
            if 0 <= idx < total:
                msg = MESSAGES[(idx + 1) % len(MESSAGES)]
                print(f"  [{idx+1:>9,}]  {schedule[idx].isoformat()}  {msg}")
        return

    proc = subprocess.Popen(
        ["git", "fast-import", "--quiet", "--force"],
        stdin=subprocess.PIPE,
    )
    out = proc.stdin

    def w(b):
        if isinstance(b, str):
            b = b.encode()
        out.write(b)

    prev_mark = None
    try:
        for i, when in enumerate(schedule, start=1):
            msg = MESSAGES[i % len(MESSAGES)]
            ts  = int(when.timestamp())

            # marks.txt content is a single overwritten line — keeps
            # blob size tiny and constant so fast-import stays fast.
            content = f"{i:,} of {total:,} recognized marks\n".encode()

            blob_mark   = 2 * i - 1
            commit_mark = 2 * i

            w(f"blob\nmark :{blob_mark}\ndata {len(content)}\n")
            w(content)
            w("\n")

            msg_b = msg.encode()
            w(f"commit refs/heads/main\n")
            w(f"mark :{commit_mark}\n")
            w(f"author {name} <{email}> {ts} +0000\n")
            w(f"committer {name} <{email}> {ts} +0000\n")
            w(f"data {len(msg_b)}\n")
            w(msg_b)
            w("\n")
            if prev_mark is not None:
                w(f"from :{prev_mark}\n")
            w(f"M 100644 :{blob_mark} marks.txt\n\n")

            prev_mark = commit_mark

            if i % 50_000 == 0:
                print(f"  streamed {i:>9,}/{total:,}", flush=True)
    finally:
        out.close()
        rc = proc.wait()
        if rc != 0:
            print(f"git fast-import exited with code {rc}", file=sys.stderr)
            sys.exit(rc)

    # Check out the resulting tree so the working directory reflects main
    subprocess.run(["git", "checkout", "-f", "main"],
                   check=True, capture_output=True)


def main():
    dry_run = "--dry-run" in sys.argv

    schedule = build_schedule()
    total = len(schedule)

    print(f"Pattern        : {ACTIVE_PATTERN}  (cut as negative space)")
    print(f"Years of fill  : {YEARS_BACK + 1}  (current + {YEARS_BACK} prior)")
    print(f"Target commits : {TARGET_COMMITS:,}")
    print(f"Actual commits : {total:,}")
    print(f"Mode           : {'dry run' if dry_run else 'LIVE (fast-import)'}")
    print()

    run_fast_import(schedule, dry_run=dry_run)

    if dry_run:
        print(f"\nNo commits made. {total:,} commits planned.")
    else:
        print(f"\nDone. {total:,} commits written. Push when ready.")


if __name__ == "__main__":
    main()
