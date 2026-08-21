---
name: prep
description: Plan a section — scope it, break it into 2-5 sessions, and write one work file under docs/work/ that the generator accepts. Plan files only, never code.
---

Read `skills/prep/SKILL.md` and follow it in order. The whole pass lives there; this wrapper is
resident and the skill is not.

`/prep` sets the pointer's `mode` field and touches no other field. It writes no code and does not
regenerate the indexes: the queue catches up at the next `/done`.
