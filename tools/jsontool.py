#!/usr/bin/env python3
"""jsontool.py — tiny offline JSON CLI for agent-json-skills.

Stdlib only. No dependencies, no network, no cloud.
Validates, formats, flattens, queries, and diffs JSON files.

Usage:
  python tools/jsontool.py validate data.json
  python tools/jsontool.py format data.json pretty.json
  python tools/jsontool.py flatten data.json flat.json
  python tools/jsontool.py get data.json user.address.city
  python tools/jsontool.py diff old.json new.json
"""
import argparse
import json
import os
import sys


def fail(msg):
    print(f"jsontool: error: {msg}", file=sys.stderr)
    return 2


def load_json(path):
    if not os.path.isfile(path):
        print(f"jsontool: error: file not found: {path}", file=sys.stderr)
        return None, False
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f), True
    except json.JSONDecodeError as e:
        print(f"jsontool: invalid JSON in {path}: {e}", file=sys.stderr)
        return None, False
    except UnicodeDecodeError as e:
        print(f"jsontool: error: cannot read {path}: {e}", file=sys.stderr)
        return None, False


def save_json(path, data, indent=2, sort_keys=False):
    parent = os.path.dirname(os.path.abspath(path))
    os.makedirs(parent, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=indent, ensure_ascii=False, sort_keys=sort_keys)
        f.write("\n")


def cmd_validate(a):
    data, ok = load_json(a.input)
    if not ok:
        return 2
    kind = "object" if isinstance(data, dict) else "array" if isinstance(data, list) else type(data).__name__
    print(f"Valid JSON: {a.input} ({kind})")
    return 0


def cmd_format(a):
    data, ok = load_json(a.input)
    if not ok:
        return 2
    save_json(a.output, data, indent=a.indent, sort_keys=a.sort_keys)
    print(f"Formatted: {a.input} -> {a.output} (indent={a.indent}, sort_keys={a.sort_keys})")
    return 0


def flatten(value, prefix="", out=None):
    if out is None:
        out = {}
    if isinstance(value, dict):
        if not value:
            out[prefix] = {}
        for k, v in value.items():
            key = f"{prefix}.{k}" if prefix else str(k)
            flatten(v, key, out)
    elif isinstance(value, list):
        if not value:
            out[prefix] = []
        for i, v in enumerate(value):
            flatten(v, f"{prefix}.{i}" if prefix else str(i), out)
    else:
        out[prefix] = value
    return out


def cmd_flatten(a):
    data, ok = load_json(a.input)
    if not ok:
        return 2
    save_json(a.output, flatten(data))
    print(f"Flattened: {len(flatten(data))} keys. Saved: {a.output}")
    return 0


def cmd_get(a):
    data, ok = load_json(a.input)
    if not ok:
        return 2
    current = data
    for part in a.path.split("."):
        if isinstance(current, dict):
            if part not in current:
                return fail(f"key '{part}' not found in {a.path}")
            current = current[part]
        elif isinstance(current, list):
            try:
                current = current[int(part)]
            except (ValueError, IndexError):
                return fail(f"index '{part}' not valid for list in {a.path}")
        else:
            return fail(f"cannot go deeper at '{part}' in {a.path}")
    if isinstance(current, (dict, list)):
        print(json.dumps(current, indent=2, ensure_ascii=False))
    else:
        print(current)
    return 0


def diff_values(old, new, path, changes):
    if type(old) is not type(new) and not (isinstance(old, (int, float)) and isinstance(new, (int, float))):
        changes.append(f"~ {path}: {old!r} -> {new!r} (type changed)")
        return
    if isinstance(old, dict):
        for k in old.keys() - new.keys():
            changes.append(f"- {path + '.' if path else ''}{k}: {old[k]!r} (removed)")
        for k in new.keys() - old.keys():
            changes.append(f"+ {path + '.' if path else ''}{k}: {new[k]!r} (added)")
        for k in old.keys() & new.keys():
            diff_values(old[k], new[k], f"{path}.{k}" if path else str(k), changes)
    elif isinstance(old, list):
        if len(old) != len(new):
            changes.append(f"~ {path}: list length {len(old)} -> {len(new)}")
        for i, (o, n) in enumerate(zip(old, new)):
            diff_values(o, n, f"{path}[{i}]", changes)
    elif old != new:
        changes.append(f"~ {path}: {old!r} -> {new!r}")


def cmd_diff(a):
    old, ok1 = load_json(a.old)
    new, ok2 = load_json(a.new)
    if not (ok1 and ok2):
        return 2
    changes = []
    diff_values(old, new, "", changes)
    if not changes:
        print("No differences.")
        return 0
    print(f"{len(changes)} difference(s):")
    for c in changes:
        print("  " + c)
    return 0


def main(argv=None):
    p = argparse.ArgumentParser(prog="jsontool", description="Tiny offline JSON CLI (stdlib only).")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("validate", help="Check a file is valid JSON")
    s.add_argument("input")
    s.set_defaults(fn=cmd_validate)

    s = sub.add_parser("format", help="Pretty-print JSON with sorted keys option")
    s.add_argument("input"); s.add_argument("output")
    s.add_argument("--indent", type=int, default=2)
    s.add_argument("--sort-keys", action="store_true")
    s.set_defaults(fn=cmd_format)

    s = sub.add_parser("flatten", help="Flatten nested JSON to dot-separated keys")
    s.add_argument("input"); s.add_argument("output")
    s.set_defaults(fn=cmd_flatten)

    s = sub.add_parser("get", help="Get a value by dot path, e.g. user.address.city")
    s.add_argument("input"); s.add_argument("path")
    s.set_defaults(fn=cmd_get)

    s = sub.add_parser("diff", help="Show added, removed, and changed keys")
    s.add_argument("old"); s.add_argument("new")
    s.set_defaults(fn=cmd_diff)

    a = p.parse_args(argv)
    return a.fn(a)


if __name__ == "__main__":
    raise SystemExit(main())
