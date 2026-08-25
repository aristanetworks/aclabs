#!/usr/bin/env python3
"""Render-vs-target report for the techlib domain-ab AVD models.

Compares avd/intended/configs/*.cfg (rendered) with
startup-configs/clab-arista-evpn-dg-domain-ab/*/startup-config (targets)
as content SETS: every non-exempt line must appear on both sides, position
is never compared. Exempt (cosmetic by agreement): comment lines,
interface/host descriptions, BGP neighbor descriptions, `no shutdown`.

  python3 avd/scripts/parity_report.py            # summary -> avd/PARITY-STATUS.md + stdout
  python3 avd/scripts/parity_report.py A-LEAF1    # full missing/extra listing for one node
  python3 avd/scripts/parity_report.py --all      # full listing for every node
"""
import re
import sys
from collections import Counter
from datetime import date
from pathlib import Path

LAB = Path(__file__).resolve().parents[2]
SC = LAB / "startup-configs/clab-arista-evpn-dg-domain-ab"
RC = LAB / "avd/intended/configs"
OUT = LAB / "avd/PARITY-STATUS.md"

EXEMPT_COUNTS = Counter()


def classify_exempt(s: str) -> str | None:
    if not s or s == "!" or s == "end":
        return None
    if s.startswith("! "):
        return "comment lines"
    if s.startswith("description "):
        return "interface/host descriptions"
    if re.match(r"neighbor \S+ description ", s):
        return "BGP neighbor descriptions"
    if s == "no shutdown":
        return "explicit `no shutdown` (AVD default)"
    return ""


def lines(p: Path) -> list[str]:
    out = []
    for ln in p.read_text().splitlines():
        s = ln.strip()
        tag = classify_exempt(s)
        if tag is None:
            continue
        if tag:
            EXEMPT_COUNTS[tag] += 1
            continue
        out.append(ln.rstrip())
    return out


def norm(s: str) -> str:
    return re.sub(r"\d+", "#", s)


def top_table(counter: Counter, n: int) -> str:
    rows = [f"| {c}× | `{ln.strip()}` |" for ln, c in counter.most_common(n)]
    return "\n".join(["| count | line |", "|---|---|", *rows])


def node_diff(name: str):
    rc = RC / f"{name}.cfg"
    a = Counter(lines(SC / name / "startup-config"))
    b = Counter(lines(rc)) if rc.is_file() else Counter()
    return a - b, b - a, rc.is_file()


nodes = sorted(d.name for d in SC.iterdir() if d.is_dir())
args = [a for a in sys.argv[1:]]

if args and args != ["--all"]:
    for name in args:
        m, e, ok = node_diff(name)
        print(f"===== {name} {'(NOT RENDERED)' if not ok else ''} missing={sum(m.values())} extra={sum(e.values())}")
        print("--- MISSING (in target, not rendered)")
        for ln, c in sorted(m.items()):
            print(f"  {'x'+str(c)+' ' if c > 1 else ''}{ln}")
        print("--- EXTRA (rendered, not in target)")
        for ln, c in sorted(e.items()):
            print(f"  {'x'+str(c)+' ' if c > 1 else ''}{ln}")
    sys.exit(0)

missing, extra = Counter(), Counter()
per_node = []
for name in nodes:
    m, e, ok = node_diff(name)
    if not ok:
        per_node.append((name, "-", "-"))
        continue
    per_node.append((name, sum(m.values()), sum(e.values())))
    missing.update(m)
    extra.update(e)
    if args == ["--all"]:
        print(f"===== {name} missing={sum(m.values())} extra={sum(e.values())}")
        for ln, c in sorted(m.items()):
            print(f"  - {'x'+str(c)+' ' if c > 1 else ''}{ln}")
        for ln, c in sorted(e.items()):
            print(f"  + {'x'+str(c)+' ' if c > 1 else ''}{ln}")

m_total, e_total = sum(missing.values()), sum(extra.values())
m_shapes, e_shapes = Counter(), Counter()
for ln, c in missing.items():
    m_shapes[norm(ln)] += c
for ln, c in extra.items():
    e_shapes[norm(ln)] += c

report = f"""# PARITY-STATUS — rendered configs vs the lab's startup-configs (auto-generated)

> Generated {date.today().isoformat()} by `avd/scripts/parity_report.py`.
> Content-set comparison (ordering never compared). Exempt as cosmetic:
> comments, descriptions, BGP neighbor descriptions, explicit `no shutdown`.

## Scoreboard

| Metric | Lines |
|---|---|
| **Residual total (non-exempt)** | **{m_total + e_total}** |
| MISSING — in the target, not rendered | {m_total} |
| EXTRA — rendered, not in the target | {e_total} |

## Exempt lines absorbed today

| Exemption | Lines |
|---|---|
""" + "\n".join(f"| {k} | {v} |" for k, v in sorted(EXEMPT_COUNTS.items())) + f"""

## Remaining differences

### MISSING — top exact lines ({len(missing)} distinct)

{top_table(missing, 25)}

### MISSING — top shapes (digits→`#`)

{top_table(m_shapes, 15)}

### EXTRA — top exact lines ({len(extra)} distinct)

{top_table(extra, 40)}

### EXTRA — top shapes (digits→`#`)

{top_table(e_shapes, 20)}

## Per-node residual

| Node | missing | extra |
|---|---|---|
""" + "\n".join(f"| {n} | {m} | {e} |" for n, m, e in per_node) + f"""
| **TOTAL** | **{m_total}** | **{e_total}** |
"""

OUT.write_text(report)
print(f"PARITY-STATUS.md written — residual {m_total + e_total} (missing {m_total} / extra {e_total})")
for n, m, e in per_node:
    print(f"  {n:10s} missing={m:>4} extra={e:>4}")
