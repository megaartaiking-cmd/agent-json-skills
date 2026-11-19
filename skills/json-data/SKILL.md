---
name: json-data
description: Validate, format, flatten, query, and diff JSON files, offline, with Python. Use when the user or agent wants to check, clean up, read a value from, or compare JSON data.
---

# JSON Data

Work with JSON files in the terminal. Validate a file, pretty-print it,
flatten nested data, pull out one value, or diff two files.
No cloud, no upload. Files stay local.

## When to use

- "Is this JSON valid?"
- "Format this JSON so I can read it"
- "What is the value of user.address.city?"
- "What changed between these two JSON files?"

## Workflow

1. Validate first — never guess at broken JSON:
   ```sh
   python tools/jsontool.py validate data.json
   ```
   If it is invalid, report the exact error (line and column) and stop.
2. Format — pretty-print with 2-space indent:
   ```sh
   python tools/jsontool.py format data.json pretty.json
   python tools/jsontool.py format data.json pretty.json --sort-keys
   ```
3. Flatten nested data to dot-separated keys:
   ```sh
   python tools/jsontool.py flatten data.json flat.json
   ```
4. Get one value by dot path (use a number for list indexes):
   ```sh
   python tools/jsontool.py get data.json user.address.city
   python tools/jsontool.py get data.json items.0.name
   ```
5. Diff two files:
   ```sh
   python tools/jsontool.py diff old.json new.json
   ```
6. Report the result. For `get`, print the value. For `diff`, list added, removed, and changed keys.

## Examples

**Check a config file before using it**
```sh
python tools/jsontool.py validate config.json
# Valid JSON: config.json (object)
```

**What is the user's city?**
```sh
python tools/jsontool.py get user.json user.address.city
# Paris
```

**What changed between two versions?**
```sh
python tools/jsontool.py diff v1.json v2.json
# 3 difference(s):
#   ~ user.age: 28 -> 29
#   + user.nickname: "Aisha" (added)
```

## Rules

- Never overwrite the input file. Always write to a new output file.
- Do not silently fix invalid JSON — report the error and let the user decide.
- Do not invent values for missing keys; say the key is missing.
- For large files, use `get` or `flatten` instead of pasting the whole file into a reply.
- `diff` compares by key, not by line — use it for data, not for prose.
