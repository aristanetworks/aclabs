#!/usr/bin/env python3
"""Generate PARITY-STATUS.md — the running parity tally for the AVD rebuild.

Compares avd/intended/configs/*.cfg (rendered) against
startup-configs/clab-arista-evpn-dg-domain-ab/*/startup-config (the guide),
under the amended parity contract (content-set parity; see PARITY-LEDGER.md).

Reports:
  1. Scoreboard — residual non-exempt line count, per side.
  2. Accepted deviations — each exemption with the line count it absorbs
     TODAY (measured live, so the cost of every acceptance stays visible).
  3. Remaining differences — top exact lines and digit-normalized shapes,
     each side, plus a per-node residual table.

Run from the lab root:  python3 avd/scripts/parity_report.py
"""
import re
from collections import Counter
from datetime import date
from pathlib import Path

LAB = Path(__file__).resolve().parents[2]
SC = LAB / "startup-configs/clab-arista-evpn-dg-domain-ab"
RC = LAB / "avd/intended/configs"
OUT = LAB / "avd/PARITY-STATUS.md"

EXEMPT_COUNTS = Counter()


def classify_exempt(s: str) -> str | None:
    if not s or s == "!":
        return None  # structural blanks/bangs — not counted as deviations
    if s.startswith("! "):
        return "comment lines"
    if s.startswith("description "):
        return "interface/host descriptions"
    if s == "no shutdown":
        return "explicit `no shutdown` (accepted AVD default)"
    return ""  # not exempt


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


missing, extra = Counter(), Counter()
per_node = []
for d in sorted(SC.iterdir()):
    rc = RC / f"{d.name}.cfg"
    if not rc.is_file():
        continue
    a = Counter(lines(d / "startup-config"))
    b = Counter(lines(rc))
    m, e = a - b, b - a
    per_node.append((d.name, sum(m.values()), sum(e.values())))
    missing.update(m)
    extra.update(e)

m_total, e_total = sum(missing.values()), sum(extra.values())
m_shapes = Counter()
for ln, c in missing.items():
    m_shapes[norm(ln)] += c
e_shapes = Counter()
for ln, c in extra.items():
    e_shapes[norm(ln)] += c

report = f"""# PARITY-STATUS — running tally (auto-generated)

> Generated {date.today().isoformat()} by `avd/scripts/parity_report.py`.
> Contract: **content-set parity** (line ordering exempt) — see
> `PARITY-LEDGER.md` for the class taxonomy and capability verdicts.

## Scoreboard

| Metric | Lines |
|---|---|
| **Residual total (non-exempt)** | **{m_total + e_total}** |
| MISSING — in the guide, not yet rendered | {m_total} |
| EXTRA — rendered, not in the guide | {e_total} |
| Baseline at campaign start (round-11 models, same contract) | 2,943 |

## Accepted deviations (the exemption list, with today's absorbed counts)

These are the deliberate departures from strict line-for-line parity.
Counts are measured live across both sides so the cost of each
acceptance stays visible.

| Accepted deviation | Lines absorbed today |
|---|---|
""" + "\n".join(
    f"| {k} | {v} |" for k, v in sorted(EXEMPT_COUNTS.items())
) + f"""
| line ordering (positions never compared) | n/a — structural |

## Remaining differences

### MISSING — top exact lines ({len(missing)} distinct)

{top_table(missing, 15)}

### MISSING — top shapes (digits→`#`)

{top_table(m_shapes, 10)}

### EXTRA — top exact lines ({len(extra)} distinct)

{top_table(extra, 15)}

### EXTRA — top shapes (digits→`#`)

{top_table(e_shapes, 10)}

## Per-node residual

| Node | missing | extra | total |
|---|---|---|---|
""" + "\n".join(
    f"| {n} | {m} | {e} | {m + e} |" for n, m, e in per_node
) + f"""
| **TOTAL** | **{m_total}** | **{e_total}** | **{m_total + e_total}** |
"""

OUT.write_text(report)
print(f"PARITY-STATUS.md written — residual {m_total + e_total} "
      f"(missing {m_total} / extra {e_total})")
