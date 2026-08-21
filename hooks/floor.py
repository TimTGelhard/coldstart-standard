"""The safety floor: classify one PreToolUse payload, allow or deny.

`hooks/pre-tool-floor.sh` is the registered entry point and this is where the
rules live. It is Python and not shell because the payload is JSON and the
pointer is YAML front matter, and a shell floor that parses both by hand is a
floor nobody can read a year later.

Three categories, in the order they are checked:

  secrets      reading or dumping credential material, or staging it into git
  destructive  deletes, force pushes, history rewrites, unbounded overwrites
  mode         under `mode: prep`, anything not provably a read

The first two apply in any tree. The third applies only in a tree this harness
serves, decided by whether `docs/PROGRESS.md` carries this schema's pointer
fields -- coldstart-standard was itself on the receiving end of a neighbouring
harness enforcing its mode contract against a pointer it could not read, and the
rule it took from that is that a harness must not govern a tree it does not own.

A refusal always names the category, why the rule is structural, and the
legitimate path. A refusal without a legitimate path gets routed around inside
the same session, which is worse than no refusal, because now the operator
believes there is a floor.
"""

from __future__ import annotations

import json
import os
import re
import shlex
import sys
from pathlib import Path

# The pointer fields that identify this harness's schema (docs/FORMAT.md, s1).
# ColdStart v1's pointer carries `active_section`, not these, which is exactly
# the tree the mode contract must stay out of.
SCHEMA_FIELDS = ("active_work", "next_action", "resume_note")

# --- category 1: secrets ---------------------------------------------------

SECRET_PATHS = re.compile(
    r"""(?ix)
    (^|[\s'"=/])
    (
      [a-z0-9_.-]*\.env(\.[a-z0-9_-]+)?   # .env, .env.local, prod.env
    | \.git-credentials
    | \.netrc | _netrc
    | \.npmrc | \.pypirc
    | id_(rsa|dsa|ecdsa|ed25519)
    | credentials(\.json|\.yml|\.yaml)?
    | service[-_]account[a-z0-9_-]*\.json
    | secrets?(\.[a-z]+)?
    | [a-z0-9_-]+\.(pem|p12|pfx|key|keystore|jks)
    )
    ($|[\s'"])
    """
)

# Not secrets, whatever they are named. A template is published on purpose.
SECRET_EXEMPT = re.compile(r"(?i)\.env\.(example|sample|template|dist)\b|\bexample\.env\b")

SECRET_READERS = {
    "cat", "bat", "less", "more", "head", "tail", "nl", "od", "xxd", "strings",
    "grep", "egrep", "fgrep", "rg", "ag", "ack", "awk", "sed", "cut", "sort",
    "cp", "scp", "rsync", "curl", "wget", "base64", "tee", "jq", "yq", "open",
}

ENV_DUMPS = re.compile(
    r"""(?ix)
    (?:^|[;&|]\s*) (env|printenv|set) \s* (\||>|$)   # segment-initial, so that a
                                                     # filename like .env cannot match
    | \bprintenv\s+\S*(key|token|secret|password|passwd|credential)
    | \becho\s+["']?\$\{?[A-Z0-9_]*(KEY|TOKEN|SECRET|PASSWORD|PASSWD|CREDENTIAL)[A-Z0-9_]*\}?
    """
)

# Staging is a different exposure from reading, and it is the worse one. A secret
# read into the transcript is local to this machine; a secret that reaches a
# remote is public from that moment and stays public after the commit is deleted,
# because the object survives in forks, caches, clones and the provider's own
# rebuild of the fork network. Rotation is the only real remedy, and it is the
# operator's afternoon.
GIT_STAGERS = re.compile(r"(?ix)\bgit\s+(add|commit|stash|rm)\b")

# The accident that actually happens: nothing in the command names the file.
# `git add -A`, `git add .` and `git commit -a` all sweep, and the sweep is what
# picks up the .env nobody meant to include.
GIT_BULK_ADD = re.compile(
    r"(?ix)\bgit\s+add\b[^;&|]*?(\s-A\b|\s--all\b|\s\.(\s|$)|\s\*)"
    r"|\bgit\s+commit\b[^;&|]*?(\s-[a-z]*a[a-z]*\b|\s--all\b)"
)

# What this rule cannot reach, stated so nobody trusts it further than it goes:
# a .env that is ALREADY tracked. Once the file is in the index, .gitignore is
# inert and every ordinary commit carries it. That is a repository that is
# already leaking and it needs `git rm --cached` plus a rotated credential, not
# a PreToolUse hook.

ENV_FILE = re.compile(
    r"(?i)^([a-z0-9_.-]*\.env(\.[a-z0-9_-]+)?"      # .env, .env.local, prod.env
    r"|[a-z0-9_-]+\.(pem|p12|pfx|key|keystore|jks)"  # key material
    r"|\.git-credentials|\.netrc|\.npmrc|\.pypirc)$"
)

# A .gitignore line that plausibly covers .env. Deliberately loose: a false
# "covered" reading only returns this rule to the level of protection git itself
# is already giving, while a false "uncovered" reading denies a legitimate stage.
GITIGNORE_COVERS_ENV = re.compile(r"(?im)^\s*!?\s*(\*\*/)?(\*)?\.env")

SECRET_COMMIT_REASON = (
    "floor:secrets -- {what}.\n"
    "Structural, not advisory: a secret that reaches a remote is public from "
    "that moment, and deleting the commit does not take it back. The object "
    "survives in every fork, clone and cache, so the only real remedy is "
    "rotating the credential.\n"
    "The legitimate path: {fix}"
)

SECRET_COMMIT_FIXES = {
    "named": "add the file to `.gitignore` first, commit that, and stage the rest by name.",
    "bulk": ("stage by name -- `git add <path> <path>` -- or put the file in "
             "`.gitignore` and commit that first. Bulk staging is refused here "
             "only while an unignored secret file is sitting in the tree; once "
             "it is ignored, `git add -A` passes again."),
}

SECRETS_REASON = (
    "floor:secrets -- this reads credential material into the transcript.\n"
    "Structural, not advisory: anything a tool prints is in the context window "
    "for the rest of the session and in the transcript on disk afterwards, and "
    "there is no way to take it back out.\n"
    "The legitimate path: read the KEYS, not the values -- `cut -d= -f1 .env` "
    "lists the variable names, `test -n \"$VAR\" && echo set` proves one is "
    "populated without printing it. If a value genuinely has to be seen, the "
    "operator reads it themselves outside the session."
)

# --- category 2: destructive ----------------------------------------------

# Targets a recursive delete must never be pointed at. Everything else is the
# operator's business: `rm -rf node_modules` and `rm -rf /tmp/scratch/build` are
# ordinary, and a floor that refuses them is a floor that gets switched off.
RM_FORBIDDEN = {"/", "~", "~/", "$HOME", "$HOME/", ".", "./", "..", "../", "*", "/*"}
RM_SHALLOW = re.compile(r"^/[^/]*/?$")          # /usr, /etc, /Users -- one segment deep
RM_UNEXPANDED = re.compile(r"^\$\{?\w+\}?/?$")  # $DIR, ${DIR}/ -- empty if unset, so this is /


def destructive_rm(argv: list[str]) -> str | None:
    """A recursive force-delete pointed somewhere it can never be pointed."""
    if not argv or Path(argv[0]).name != "rm":
        return None
    flags = "".join(a for a in argv[1:] if a.startswith("-") and not a.startswith("--"))
    long = [a for a in argv[1:] if a.startswith("--")]
    recursive = "r" in flags or "R" in flags or "--recursive" in long
    forced = "f" in flags or "--force" in long
    if not (recursive and forced):
        return None
    for arg in (a for a in argv[1:] if not a.startswith("-")):
        if arg in RM_FORBIDDEN:
            return f"a recursive force-delete of `{arg}`"
        if RM_SHALLOW.match(arg):
            return f"a recursive force-delete of `{arg}`, one segment below the filesystem root"
        if RM_UNEXPANDED.match(arg):
            return (f"a recursive force-delete of `{arg}`, an unexpanded variable -- "
                    "if it is unset the shell deletes from the root")
    return None


DESTRUCTIVE_RULES = (
    (re.compile(r"(?i)\bsudo\s+rm\b"), "a delete escalated to root"),
    (re.compile(r"(?i)\bgit\s+push\b(?!.*--force-with-lease)(?=.*(--force|\s-f\b))"),
     "a force push, which overwrites a remote branch's history for everyone who has it"),
    (re.compile(r"(?i)\bgit\s+(filter-branch|filter-repo)\b"), "a history rewrite"),
    (re.compile(r"(?i)\bgit\s+reset\s+--hard\b"), "a hard reset, which discards uncommitted work"),
    (re.compile(r"(?i)\bgit\s+clean\s+-\w*[fd]\w*"), "a clean, which deletes untracked files"),
    (re.compile(r"(?i)\bgit\s+checkout\s+(--\s+)?\.\s*$"), "a checkout that discards every local edit"),
    (re.compile(r"(?i)\bgit\s+reflog\s+expire\b|\bgit\s+gc\s+--prune=now"),
     "a reflog expiry, which removes the last route back from a bad rewrite"),
    (re.compile(r"(?i)\bdd\b.*\bof=/dev/"), "a raw write to a block device"),
    (re.compile(r"(?i)\bmkfs(\.\w+)?\b"), "a filesystem format"),
    (re.compile(r"(?i)\bchmod\s+-R\s+777\s+/"), "a recursive world-writable chmod from the root"),
    (re.compile(r"(?i)\bdrop\s+(database|schema)\b"), "a database or schema drop"),
    (re.compile(r"(?i)\btruncate\s+table\b|\bdelete\s+from\s+\w+\s*;"),
     "an unbounded table delete (no WHERE clause)"),
    (re.compile(r":\(\)\s*\{\s*:\|:&\s*\}\s*;:"), "a fork bomb"),
)

DESTRUCTIVE_REASON = (
    "floor:destructive -- {what}.\n"
    "Structural, not advisory: this class of command has no undo, so the check "
    "has to happen before it runs rather than in review afterwards.\n"
    "The legitimate path: {fix}"
)

DESTRUCTIVE_FIXES = {
    "force push": "`git push --force-with-lease`, which refuses when the remote moved under you.",
    "hard reset": "`git stash` first, or `git reset --keep`, so the work is recoverable.",
    "clean": "`git clean -nd` first to see the list, then delete the named paths.",
    "delete": "name the paths explicitly and let the shell fail on a typo, rather than "
              "recursing from a root or an unexpanded variable.",
    "default": "narrow the command to an explicit, named target, or hand it to the operator "
               "to run themselves outside the session.",
}

# --- category 3: the mode contract ----------------------------------------

# Provable reads. A command passes under `prep` only if EVERY segment is here.
# The bar is provable, not plausible: an unrecognised command may well be a read,
# and "may well be" is the standard this list exists to refuse.
READ_ONLY = {
    "cat", "head", "tail", "less", "more", "nl", "wc", "ls", "tree", "stat", "file",
    "find", "grep", "egrep", "fgrep", "rg", "ag", "sort", "uniq", "cut", "tr", "column",
    "pwd", "echo", "printf", "which", "type", "command", "basename", "dirname",
    "date", "du", "df", "diff", "cmp", "jq", "yq", "true", "false", "test", "realpath",
}
READ_ONLY_GIT = {"status", "log", "diff", "show", "branch", "remote", "ls-files",
                 "rev-parse", "describe", "blame", "shortlog", "config"}

# The surface a planning pass is allowed to write. Everything else waits for build.
PREP_WRITE_SURFACE = (
    re.compile(r"^docs/work/[^/]+\.md$"),
    re.compile(r"^docs/work/artifacts/[^/]+\.md$"),
    re.compile(r"^docs/PROGRESS\.md$"),
    re.compile(r"^docs/PROJECT_PLAN\.md$"),
)

MODE_REASON = (
    "floor:mode -- the pointer says `mode: prep`, and {what}.\n"
    "Structural, not advisory: a planning pass that writes code is how a plan "
    "stops describing the work and starts being the work, which is the failure "
    "this harness's own /prep was built to make impossible.\n"
    "The legitimate path: finish the plan, then set `mode: build` in the front "
    "matter of docs/PROGRESS.md -- a declaration made on the record, not a flag "
    "that suppresses the check. /done writes that field at close."
)

WRITE_TOOLS = {"Write", "Edit", "NotebookEdit", "MultiEdit"}
READ_TOOLS = {"Read", "Glob", "Grep", "NotebookRead"}


def find_root(start: str) -> Path | None:
    """Walk up from `start` looking for this memory model's docs/PROGRESS.md."""
    here = Path(start or ".").resolve()
    for candidate in (here, *here.parents):
        if (candidate / "docs" / "PROGRESS.md").is_file():
            return candidate
    return None


def read_pointer(root: Path) -> dict | None:
    """Parse docs/PROGRESS.md front matter. None when it is not our schema.

    Deliberately a few lines of hand parsing rather than a YAML dependency: the
    block is seven flat scalar fields by contract, and the floor must not fail
    open because an import was missing on someone's machine.
    """
    try:
        text = (root / "docs" / "PROGRESS.md").read_text(encoding="utf-8")
    except OSError:
        return None
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    if end == -1:
        return None
    fields = {}
    for line in text[3:end].splitlines():
        if ":" in line and not line.startswith((" ", "\t", "#")):
            key, _, value = line.partition(":")
            fields[key.strip()] = value.strip().strip("\"'")
    if not all(f in fields for f in SCHEMA_FIELDS):
        return None  # someone else's pointer; the mode branch stays out of it
    return fields


def segments(command: str) -> list[list[str]]:
    """Split a shell command into argv segments across ; && || | and newlines.

    Unparseable input returns [] and every caller treats that as "cannot prove",
    which under `prep` denies and under the risk rules falls back to the raw
    string match that already ran.
    """
    try:
        lexer = shlex.shlex(command, posix=True, punctuation_chars=True)
        lexer.whitespace_split = True
        tokens = list(lexer)
    except ValueError:
        return []
    out, current = [], []
    for token in tokens:
        if token in (";", "&&", "||", "|", "&", "\n"):
            if current:
                out.append(current)
            current = []
        else:
            current.append(token)
    if current:
        out.append(current)
    return out


def keys_only_read(argv: list[str]) -> bool:
    """`cut -d= -f1 .env` -- the variable names without any value.

    Exempt because the secrets refusal text names this command as the way to do
    the legitimate version of what was just refused, and a floor that forbids the
    escape hatch it prints is a floor the operator stops believing.
    """
    if Path(argv[0]).name != "cut":
        return False
    joined = " ".join(argv[1:])
    return bool(re.search(r"-d\s*['\"]?=", joined) and re.search(r"-f\s*['\"]?1(\s|$|['\"])", joined))


def unignored_secret_files(cwd: Path | None) -> list[str]:
    """Secret-looking files in the project root that .gitignore does not cover.

    Deliberately shallow: the root only, and one loose pattern against
    .gitignore. A deeper scan means walking the tree on every Bash call, and a
    floor that costs a directory walk per command is a floor that gets removed
    for being slow. The shallow case is also the real one -- .env lives at the
    root, and that is where `git add -A` picks it up.
    """
    if cwd is None:
        return []
    try:
        if GITIGNORE_COVERS_ENV.search((cwd / ".gitignore").read_text(errors="replace")):
            return []
    except OSError:
        pass                          # no .gitignore is the unprotected case
    try:
        names = sorted(e.name for e in cwd.iterdir() if e.is_file())
    except OSError:
        return []
    return [n for n in names if ENV_FILE.match(n) and not SECRET_EXEMPT.search(n)]


def check_secrets(tool: str, tool_input: dict, cwd: Path | None = None) -> str | None:
    if tool in READ_TOOLS or tool in WRITE_TOOLS:
        path = str(tool_input.get("file_path") or tool_input.get("path") or "")
        if path and SECRET_PATHS.search(path) and not SECRET_EXEMPT.search(path):
            if tool in READ_TOOLS:
                return SECRETS_REASON
        return None
    if tool != "Bash":
        return None
    command = str(tool_input.get("command", ""))
    if SECRET_EXEMPT.search(command):
        return None
    if ENV_DUMPS.search(command):
        return SECRETS_REASON
    if GIT_BULK_ADD.search(command):
        loose = unignored_secret_files(cwd)
        if loose:
            return SECRET_COMMIT_REASON.format(
                what=("this stages every changed file, and `" + "`, `".join(loose)
                      + "` is in the tree and not covered by .gitignore"),
                fix=SECRET_COMMIT_FIXES["bulk"])
    if not SECRET_PATHS.search(command):
        return None
    if GIT_STAGERS.search(command):
        return SECRET_COMMIT_REASON.format(
            what="this puts credential material into git history",
            fix=SECRET_COMMIT_FIXES["named"])
    for argv in segments(command) or [command.split()]:
        if argv and keys_only_read(argv):
            continue   # the legitimate path the refusal itself recommends
        if argv and Path(argv[0]).name in SECRET_READERS:
            if any(SECRET_PATHS.search(a) and not SECRET_EXEMPT.search(a) for a in argv[1:]):
                return SECRETS_REASON
    return None


def check_destructive(tool: str, tool_input: dict) -> str | None:
    if tool != "Bash":
        return None
    command = str(tool_input.get("command", ""))
    for argv in segments(command):
        what = destructive_rm(argv)
        if what:
            return DESTRUCTIVE_REASON.format(what=what, fix=DESTRUCTIVE_FIXES["delete"])
    for pattern, what in DESTRUCTIVE_RULES:
        if pattern.search(command):
            fix = DESTRUCTIVE_FIXES["default"]
            for key, text in DESTRUCTIVE_FIXES.items():
                if key != "default" and key in what:
                    fix = text
                    break
            return DESTRUCTIVE_REASON.format(what=what, fix=fix)
    return None


def check_mode(tool: str, tool_input: dict, root: Path | None) -> str | None:
    if root is None:
        return None
    pointer = read_pointer(root)
    if pointer is None:              # not this harness's tree
        return None
    if pointer.get("mode", "build") != "prep":
        return None                  # absent or `build` -> the contract is inert

    if tool in WRITE_TOOLS:
        path = str(tool_input.get("file_path") or tool_input.get("path") or "")
        try:
            # Both sides resolved: on macOS /var is a symlink to /private/var, so
            # comparing a resolved path against an unresolved root sends every
            # plan-surface write down the deny branch.
            rel = Path(path).resolve().relative_to(root.resolve()).as_posix()
        except (ValueError, OSError):
            rel = path
        if any(p.match(rel) for p in PREP_WRITE_SURFACE):
            return None
        return MODE_REASON.format(what=f"`{rel}` is outside the plan surface "
                                       "(docs/work/, docs/PROGRESS.md, docs/PROJECT_PLAN.md)")
    if tool != "Bash":
        return None

    command = str(tool_input.get("command", ""))
    if re.search(r"(?<![0-9<>])>{1,2}(?!&)", command):
        return MODE_REASON.format(what="this redirects into a file, which is a write")
    parsed = segments(command)
    if not parsed:
        return MODE_REASON.format(
            what="this command cannot be parsed into segments, so it cannot be "
                 "proved to be a read. The bar here is provable, not plausible")
    for argv in parsed:
        name = Path(argv[0]).name
        if name == "git":
            sub = next((a for a in argv[1:] if not a.startswith("-")), "")
            if sub in READ_ONLY_GIT and "--edit" not in argv:
                continue
            return MODE_REASON.format(what=f"`git {sub or '(none)'}` is not a proven read")
        if name == "sed" and "-n" in argv and not any(a.startswith("-i") for a in argv):
            continue
        if name in ("python", "python3") and "--check" in argv:
            continue
        if name not in READ_ONLY:
            return MODE_REASON.format(
                what=f"`{name}` is not on the read-only list. Every segment of a "
                     "compound command has to be a known read, so two safe halves "
                     "joined by an unknown third still stops here")
    return None


def decide(payload: dict) -> str | None:
    """Return a refusal reason, or None to pass."""
    tool = str(payload.get("tool_name", ""))
    tool_input = payload.get("tool_input") or {}
    if not isinstance(tool_input, dict):
        tool_input = {}
    root_hint = os.environ.get("CLAUDE_PROJECT_DIR") or payload.get("cwd") or os.getcwd()
    root = find_root(str(root_hint))
    for check in (
        lambda: check_secrets(tool, tool_input, Path(str(root_hint))),
        lambda: check_destructive(tool, tool_input),
        lambda: check_mode(tool, tool_input, root),
    ):
        reason = check()
        if reason:
            return reason
    return None


def main(argv: list[str] | None = None) -> int:
    raw = sys.stdin.read()
    try:
        payload = json.loads(raw) if raw.strip() else {}
    except json.JSONDecodeError:
        # A payload we cannot read is not a licence to deny everything: the
        # session would be unusable and the floor would be removed by lunchtime.
        print("pre-tool-floor: unreadable payload, passing", file=sys.stderr)
        return 0
    reason = decide(payload)
    if reason is None:
        return 0
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": reason,
        },
        # Kept alongside for hosts older than permissionDecision.
        "decision": "block",
        "reason": reason,
    }))
    return 0


if __name__ == "__main__":
    sys.exit(main())
