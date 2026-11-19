# agent-json-skills

> **Agent Skills for JSON — validate, format, flatten, query, and diff JSON files. Offline, stdlib-only Python.**

**1 skill · 1 CLI · 0 dependencies · 100% offline**

[![GitHub stars](https://img.shields.io/github/stars/megaartaiking-cmd/agent-json-skills?style=social)](https://github.com/megaartaiking-cmd/agent-json-skills/stargazers)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue.svg)](tools/jsontool.py)

AI agents are great at code, but JSON files still mean pasting a whole file into a chat, or writing a one-off script every time something needs checking. This repo fixes that gap: a small Agent Skill (SKILL.md) plus a tiny Python CLI that validates, formats, flattens, queries, and diffs JSON files — in the terminal, on the user's own PC.

Works with Claude Code, Cursor, GitHub Copilot, Codex, Gemini CLI, and any agent that reads SKILL.md files.

## Why this exists

Agent Skills are the fastest-growing category on GitHub — small, composable skill bundles, one job per skill, install in one step. JSON is the data format agents touch most, and there is no small, offline, agent-native way to validate it, pull one value out, or see what changed between two files.

This one is:

- **Agent-native** — a skill in the open SKILL.md format, one job, clear rules
- **Offline** — no upload, no cloud, files never leave the PC
- **Lightweight** — stdlib-only Python, no pip install, no heavy app
- **Safe** — it never overwrites the input file; every command writes a new file, and invalid JSON is reported, never silently fixed

## Skills

| Skill | What it does | Command |
|---|---|---|
| `json-data` | Validate, format, flatten, query, diff JSON | `jsontool.py` |

The skill lives in `skills/json-data/SKILL.md` — copy that folder into your agent's skills folder, or point your agent at this repo.

## Quick start

```sh
git clone https://github.com/megaartaiking-cmd/agent-json-skills.git
cd agent-json-skills

# 1. Check the sample JSON is valid
python tools/jsontool.py validate examples/sample.json

# 2. Pretty-print it
python tools/jsontool.py format examples/sample.json pretty.json

# 3. Get one value by dot path
python tools/jsontool.py get examples/sample.json user.address.city
```

No installation needed — Python 3.9+ is the only requirement.

## Usage

```sh
# Check a file is valid JSON
python tools/jsontool.py validate data.json

# Pretty-print with 2-space indent
python tools/jsontool.py format data.json pretty.json

# Pretty-print with sorted keys
python tools/jsontool.py format data.json pretty.json --sort-keys

# Flatten nested JSON to dot-separated keys
python tools/jsontool.py flatten data.json flat.json

# Get a value by dot path (numbers index lists)
python tools/jsontool.py get data.json user.address.city
python tools/jsontool.py get data.json orders.0.item

# Show added, removed, and changed keys
python tools/jsontool.py diff old.json new.json
```

See [examples/commands.md](examples/commands.md) for all commands, and [examples/sample.json](examples/sample.json) for a small file to try them on.

## How it works

1. You (or your agent) describe the job in plain words: "is this JSON valid, and what is the city?"
2. The skill in `skills/json-data/` tells the agent the exact workflow, the command to run, and the rules — never overwrite the original, always write to a new file.
3. `tools/jsontool.py` (stdlib-only Python) does the work locally and reports the result.
4. Nothing is uploaded. The work happens on your PC.

## Works with

- Claude Code
- Cursor
- GitHub Copilot
- Codex
- Gemini CLI
- Any agent that reads Agent Skills (SKILL.md)

Copy `skills/json-data/` into your agent's skills directory, or ask your agent to read the SKILL.md file in this repo directly.

## FAQ

**Does it need the internet?**
No. After `git clone`, everything runs offline.

**What if the JSON is invalid?**
The tool reports the exact error with line and column, and stops. It never silently fixes a file.

**How do I read a nested value?**
Use a dot path: `user.address.city`. Use a number for list indexes: `orders.0.item`.

**What does `diff` compare?**
Keys, not lines. It lists added, removed, and changed keys — useful for data, not for prose.

**Will it run on an old PC?**
Yes — that is the point. It is a small Python script with no dependencies.

**Can I add a skill?**
Yes — copy `skills/json-data/` as a template, write a SKILL.md with a clear name, description, workflow, and rules, and open a pull request.

## Contributing

Issues and pull requests are welcome. Keep skills small, one job per skill, with a tested command in `tools/jsontool.py`. Please do not add dependencies — stdlib only.

## License

MIT — see [LICENSE](LICENSE).

## More Agent Skills

More offline Agent Skills by the same author — one focused skill per repo:

- [agent-audio-skills](https://github.com/megaartaiking-cmd/agent-audio-skills) — Trim podcasts, normalize volume, extract audio from video
- [agent-csv-skills](https://github.com/megaartaiking-cmd/agent-csv-skills) — Clean, filter, summarize CSVs; convert to JSON and Markdown
- [agent-markdown-skills](https://github.com/megaartaiking-cmd/agent-markdown-skills) — Markdown to HTML, table of contents, link check, word count
- [agent-git-skills](https://github.com/megaartaiking-cmd/agent-git-skills) — Commit messages, changelogs, repo health, branch cleanup
- [agent-text-skills](https://github.com/megaartaiking-cmd/agent-text-skills) — Summarize text, extract keywords, readability, dedupe
- [agent-file-skills](https://github.com/megaartaiking-cmd/agent-file-skills) — Organize folders, find duplicates, batch rename
- [agent-sql-skills](https://github.com/megaartaiking-cmd/agent-sql-skills) — Explore SQLite, run queries, export to CSV
- [agent-video-skills](https://github.com/megaartaiking-cmd/agent-video-skills) — Edit video offline — trim, make Shorts, add titles, colour-grade
- [LiteCut Pro](https://github.com/megaartaiking-cmd/LIGHT-CUT-VIDEO-EDITOR) — lightweight offline video editor for Windows 10

---

**Keywords:** agent skills, AI agent JSON, JSON validator, JSON formatter, JSON diff, Claude Code skills, Cursor skills, offline JSON tool, Python JSON CLI, JSON query
