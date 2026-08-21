#!/usr/bin/env python3
"""Derive the three index files by scanning the three folders.

Implements the contract in docs/FORMAT.md. Scans docs/work/, docs/decisions/ and
docs/fixes/, reads each file's front matter (and, for work and fixes, the items
inside it), and rewrites the generated region of docs/PROGRESS.md, docs/DECISIONS.md
and docs/FIXES.md. Everything above the GENERATED BELOW THIS LINE marker in each
index file is preserved verbatim, which is what keeps the pointer block untouched.

Python stdlib only. A malformed content file is a hard error naming the file, never
a silent skip: a file missing from an index is invisible, and that is the failure
mode this tool exists to prevent.

Usage:
    python tools/index.py            rewrite the three index files
    python tools/index.py --check    exit 1 if any file would change; write nothing
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

MARKER = "GENERATED BELOW THIS LINE"
SUBJECT_CAP = 120
FRONT_MATTER_FIELDS = ("title", "subject", "topic", "updated")
WORK_STATUSES = ("pending", "active", "done", "blocked")
FIX_TAGS = ("blocked", "later")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
WORK_NAME_RE = re.compile(r"^(\d{2})-([a-z0-9]+(?:-[a-z0-9]+)*)$")
SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SESSION_HEADING_RE = re.compile(r"^##\s+Session\s+(\d+)\b\s*(?:[-—–]\s*(.*))?$")
FIELD_RE = re.compile(r"^\*\*([A-Za-z ]+)\*\*:\s*(.*)$")


class FormatError(Exception):
    """A content file does not match docs/FORMAT.md."""

    def __init__(self, path: Path, message: str) -> None:
        super().__init__(f"{path}: {message}")
        self.path = path


@dataclass
class ContentFile:
    path: Path
    link: str
    title: str
    subject: str
    topic: str
    updated: str
    body: str


@dataclass
class Session:
    number: int
    name: str
    status: str
    goal: str


@dataclass
class FixItem:
    heading: str
    subject: str
    since: str
    closes_when: str
    tag: str | None


# --------------------------------------------------------------------------- parsing


def strip_fences(lines: list[str]) -> list[bool]:
    """Return a mask: True where the line is inside a fenced code block."""
    inside = False
    mask = []
    for line in lines:
        if line.lstrip().startswith("```"):
            mask.append(True)
            inside = not inside
            continue
        mask.append(inside)
    return mask


def split_front_matter(path: Path, text: str) -> tuple[dict[str, str], str]:
    lines = text.split("\n")
    if not lines or lines[0].strip() != "---":
        raise FormatError(path, "no front matter: the file must open with a --- line")
    try:
        end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
    except StopIteration:
        raise FormatError(path, "front matter is never closed by a --- line") from None

    fields: dict[str, str] = {}
    for i in range(1, end):
        raw = lines[i]
        if not raw.strip():
            continue
        if ":" not in raw:
            raise FormatError(path, f"front-matter line {i + 1} is not `key: value`: {raw!r}")
        key, value = raw.split(":", 1)
        key = key.strip()
        value = value.strip().strip('"')
        if key in fields:
            raise FormatError(path, f"front-matter key {key!r} appears twice")
        fields[key] = value
    return fields, "\n".join(lines[end + 1 :])


def cap(path: Path, label: str, value: str, warnings: list[str]) -> str:
    if len(value) <= SUBJECT_CAP:
        return value
    warnings.append(f"{path}: {label} is {len(value)} chars, truncated to {SUBJECT_CAP}")
    return value[: SUBJECT_CAP - 3] + "..."


def load_content_file(path: Path, docs: Path, kind: str, warnings: list[str]) -> ContentFile:
    text = path.read_text(encoding="utf-8")
    fields, body = split_front_matter(path, text)

    missing = [f for f in FRONT_MATTER_FIELDS if not fields.get(f)]
    if missing:
        raise FormatError(path, "front matter is missing " + ", ".join(missing))

    stem = path.stem
    if kind == "work":
        match = WORK_NAME_RE.match(stem)
        if not match:
            raise FormatError(path, "work filenames are NN-<section-slug>.md")
        expected_topic = match.group(2)
    else:
        if not SLUG_RE.match(stem):
            raise FormatError(path, f"{kind} filenames are <topic-slug>.md, kebab-case ASCII")
        expected_topic = stem

    if fields["topic"] != expected_topic:
        raise FormatError(
            path, f"topic {fields['topic']!r} does not match the filename stem {expected_topic!r}"
        )
    if not DATE_RE.match(fields["updated"]):
        raise FormatError(path, f"updated {fields['updated']!r} is not YYYY-MM-DD")
    if "\n" in fields["subject"]:
        raise FormatError(path, "subject must be one line")

    return ContentFile(
        path=path,
        link=path.relative_to(docs).as_posix(),
        title=fields["title"],
        subject=cap(path, "subject", fields["subject"], warnings),
        topic=fields["topic"],
        updated=fields["updated"],
        body=body,
    )


def item_blocks(path: Path, body: str) -> list[tuple[str, list[str]]]:
    """Split a body into (## heading text, lines) blocks, ignoring fenced code."""
    lines = body.split("\n")
    fenced = strip_fences(lines)
    blocks: list[tuple[str, list[str]]] = []
    current: list[str] | None = None
    for line, in_fence in zip(lines, fenced):
        if not in_fence and line.startswith("## "):
            current = []
            blocks.append((line[3:].strip(), current))
        elif current is not None:
            current.append(line)
    return blocks


def block_fields(path: Path, heading: str, lines: list[str]) -> dict[str, str]:
    """Read the **Key**: value fields of an item block, folding wrapped values."""
    fields: dict[str, str] = {}
    key: str | None = None
    fenced = strip_fences(lines)
    for line, in_fence in zip(lines, fenced):
        if in_fence:
            key = None
            continue
        match = FIELD_RE.match(line.strip())
        if match:
            key = match.group(1).strip()
            if key in fields:
                raise FormatError(path, f"item {heading!r} carries {key!r} twice")
            fields[key] = match.group(2).strip()
        elif key is not None:
            if not line.strip() or line.lstrip().startswith("**"):
                key = None
            else:
                fields[key] = (fields[key] + " " + line.strip()).strip()
    return fields


def parse_sessions(path: Path, body: str) -> list[Session]:
    sessions: list[Session] = []
    seen: set[int] = set()
    for heading, lines in item_blocks(path, body):
        match = SESSION_HEADING_RE.match("## " + heading)
        if not match:
            raise FormatError(path, f"heading {heading!r} is not `Session N - <name>`")
        number = int(match.group(1))
        if number in seen:
            raise FormatError(path, f"session {number} appears twice")
        seen.add(number)
        fields = block_fields(path, heading, lines)
        for required in ("Status", "Goal"):
            if not fields.get(required):
                raise FormatError(path, f"session {number} is missing **{required}**")
        status = fields["Status"].strip().lower()
        if status not in WORK_STATUSES:
            raise FormatError(
                path, f"session {number} status {status!r} is not one of {', '.join(WORK_STATUSES)}"
            )
        sessions.append(
            Session(number=number, name=(match.group(2) or "").strip(), status=status, goal=fields["Goal"])
        )
    if not sessions:
        raise FormatError(path, "a work file carries at least one `## Session N` block")
    return sorted(sessions, key=lambda s: s.number)


def parse_fixes(path: Path, body: str, warnings: list[str]) -> list[FixItem]:
    items: list[FixItem] = []
    for heading, lines in item_blocks(path, body):
        fields = block_fields(path, heading, lines)
        for required in ("Subject", "Since", "Closes when"):
            if not fields.get(required):
                raise FormatError(path, f"item {heading!r} is missing **{required}**")
        if not DATE_RE.match(fields["Since"]):
            raise FormatError(path, f"item {heading!r} has Since {fields['Since']!r}, not YYYY-MM-DD")
        tag = fields.get("Tag")
        if tag is not None:
            tag = tag.strip().lower()
            if tag not in FIX_TAGS:
                raise FormatError(
                    path, f"item {heading!r} has Tag {tag!r}, not one of {', '.join(FIX_TAGS)}"
                )
        if "Status" in fields:
            raise FormatError(path, f"item {heading!r} carries a Status field; the fixes queue is open-only")
        cap(path, f"item {heading!r} Closes when", fields["Closes when"], warnings)
        items.append(
            FixItem(
                heading=heading,
                subject=cap(path, f"item {heading!r} Subject", fields["Subject"], warnings),
                since=fields["Since"],
                closes_when=fields["Closes when"],
                tag=tag,
            )
        )
    return items


def count_entries(path: Path, body: str) -> int:
    return len(item_blocks(path, body))


# --------------------------------------------------------------------------- rendering


def render_progress(work: list[tuple[ContentFile, list[Session]]]) -> str:
    queue_rows: list[str] = []
    log_rows: list[str] = []
    for content, sessions in work:
        number = WORK_NAME_RE.match(content.path.stem).group(1)
        open_sessions = [s for s in sessions if s.status != "done"]
        if not open_sessions:
            log_rows.append(
                f"| {number} | {content.topic} | {content.subject} | "
                f"closed {content.updated} | [{content.link}]({content.link}) |"
            )
            continue
        for session in open_sessions:
            queue_rows.append(
                f"| {int(number)}.{session.number} | {content.topic} s{session.number} | "
                f"{session.goal} | {session.status} | [{content.link}]({content.link}) |"
            )

    out = ["", "## Queue — sessions not yet done", ""]
    if queue_rows:
        out += ["| # | Session | What it does | Status | File |", "|---|---|---|---|---|", *queue_rows]
    else:
        out.append("None open.")
    out += ["", "## Log — closed sections", ""]
    if log_rows:
        out += ["| # | Section | What it was | Closed | File |", "|---|---|---|---|---|", *log_rows]
    else:
        out.append("None yet.")
    out.append("")
    return "\n".join(out)


def render_decisions(files: list[ContentFile]) -> str:
    out = [""]
    if not files:
        out.append("None yet.")
    for content in files:
        entries = count_entries(content.path, content.body)
        noun = "entry" if entries == 1 else "entries"
        out.append(
            f"- **{content.title}** — {content.subject} · "
            f"[{content.link}]({content.link}) · {entries} {noun} · {content.updated}"
        )
    out.append("")
    return "\n".join(out)


def render_fixes(files: list[tuple[ContentFile, list[FixItem]]]) -> str:
    out = [""]
    rows = [(c, item) for c, items in files for item in items]
    if not rows:
        out.append("None open.")
    for content, item in rows:
        line = (
            f"- **{item.heading}** — {item.subject} · "
            f"[{content.link}]({content.link}) · since {item.since}"
        )
        if item.tag:
            line += f" · {item.tag}"
        out.append(line)
    out.append("")
    return "\n".join(out)


def splice(path: Path, generated: str) -> str:
    """Return the index file with everything below its marker line replaced."""
    if not path.exists():
        raise FormatError(path, "index file does not exist; the header is hand-owned, not generated")
    lines = path.read_text(encoding="utf-8").split("\n")
    marker_lines = [i for i, line in enumerate(lines) if MARKER in line]
    if not marker_lines:
        raise FormatError(path, f"no {MARKER!r} marker; the generated region is undefined")
    if len(marker_lines) > 1:
        raise FormatError(path, f"{MARKER!r} appears {len(marker_lines)} times; it must appear once")
    head = "\n".join(lines[: marker_lines[0] + 1])
    return head + "\n" + generated


# --------------------------------------------------------------------------- driver


def build(docs: Path, warnings: list[str]) -> dict[Path, str]:
    work_dir, decisions_dir, fixes_dir = docs / "work", docs / "decisions", docs / "fixes"
    for folder in (work_dir, decisions_dir, fixes_dir):
        if not folder.is_dir():
            raise FormatError(folder, "folder is missing; the three folders are the canonical side")

    work = []
    for path in sorted(work_dir.glob("*.md")):
        content = load_content_file(path, docs, "work", warnings)
        work.append((content, parse_sessions(path, content.body)))

    decisions = [
        load_content_file(path, docs, "decisions", warnings) for path in sorted(decisions_dir.glob("*.md"))
    ]

    fixes = []
    for path in sorted(fixes_dir.glob("*.md")):
        content = load_content_file(path, docs, "fixes", warnings)
        fixes.append((content, parse_fixes(path, content.body, warnings)))

    return {
        docs / "PROGRESS.md": splice(docs / "PROGRESS.md", render_progress(work)),
        docs / "DECISIONS.md": splice(docs / "DECISIONS.md", render_decisions(decisions)),
        docs / "FIXES.md": splice(docs / "FIXES.md", render_fixes(fixes)),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--root", default=None, help="repo root (default: the parent of tools/)")
    parser.add_argument(
        "--check", action="store_true", help="exit 1 if any index would change; write nothing"
    )
    parser.add_argument("--quiet", action="store_true", help="print nothing on success")
    args = parser.parse_args(argv)

    root = Path(args.root).resolve() if args.root else Path(__file__).resolve().parent.parent
    warnings: list[str] = []
    try:
        rendered = build(root / "docs", warnings)
    except FormatError as error:
        print(f"index: {error}", file=sys.stderr)
        return 2

    for warning in warnings:
        print(f"index: warning: {warning}", file=sys.stderr)

    changed = [p for p, text in rendered.items() if not p.exists() or p.read_text(encoding="utf-8") != text]
    if args.check:
        for path in changed:
            print(f"index: {path.relative_to(root)} is out of date", file=sys.stderr)
        return 1 if changed else 0

    for path in changed:
        path.write_text(rendered[path], encoding="utf-8")
    if not args.quiet:
        if changed:
            for path in changed:
                print(f"index: rewrote {path.relative_to(root)}")
        else:
            print("index: already current")
    return 0


if __name__ == "__main__":
    sys.exit(main())
