# PARITY-STATUS — running tally (auto-generated)

> Generated 2026-07-23 by `avd/scripts/parity_report.py`.
> Contract: **content-set parity** (line ordering exempt) — see
> `PARITY-LEDGER.md` for the class taxonomy and capability verdicts.

## Scoreboard

| Metric | Lines |
|---|---|
| **Residual total (non-exempt)** | **57** |
| MISSING — in the guide, not yet rendered | 0 |
| EXTRA — rendered, not in the guide | 57 |
| Baseline at campaign start (round-11 models, same contract) | 2,943 |

## Accepted deviations (the exemption list, with today's absorbed counts)

These are the deliberate departures from strict line-for-line parity.
Counts are measured live across both sides so the cost of each
acceptance stays visible.

| Accepted deviation | Lines absorbed today |
|---|---|
| BGP neighbor descriptions (contract amended Day 54 s2) | 436 |
| comment lines | 54 |
| explicit `no shutdown` (accepted AVD default) | 480 |
| interface/host descriptions | 694 |
| line ordering (positions never compared) | n/a — structural |

## Remaining differences

### MISSING — top exact lines (0 distinct)

| count | line |
|---|---|

### MISSING — top shapes (digits→`#`)

| count | line |
|---|---|

### EXTRA — top exact lines (11 distinct)

| count | line |
|---|---|
| 19× | `router multicast` |
| 10× | `address-family evpn` |
| 4× | `interface Loopback101` |
| 4× | `vrf PROD` |
| 4× | `interface Loopback102` |
| 4× | `vrf DEV` |
| 4× | `evpn ethernet-segment domain all` |
| 2× | `ip address 10.101.101.7/32` |
| 2× | `ip address 10.102.102.7/32` |
| 2× | `ip address 10.101.101.8/32` |
| 2× | `ip address 10.102.102.8/32` |

### EXTRA — top shapes (digits→`#`)

| count | line |
|---|---|
| 19× | `router multicast` |
| 10× | `address-family evpn` |
| 8× | `interface Loopback#` |
| 8× | `ip address #.#.#.#/#` |
| 4× | `vrf PROD` |
| 4× | `vrf DEV` |
| 4× | `evpn ethernet-segment domain all` |

## Per-node residual

| Node | missing | extra | total |
|---|---|---|---|
| A-LEAF1 | 0 | 1 | 1 |
| A-LEAF2 | 0 | 1 | 1 |
| A-LEAF3 | 0 | 1 | 1 |
| A-LEAF4 | 0 | 1 | 1 |
| A-LEAF5 | 0 | 1 | 1 |
| A-LEAF6 | 0 | 1 | 1 |
| A-LEAF7 | 0 | 9 | 9 |
| A-LEAF8 | 0 | 9 | 9 |
| A-SPINE1 | 0 | 0 | 0 |
| A-SPINE2 | 0 | 0 | 0 |
| A-SPINE3 | 0 | 0 | 0 |
| A-SPINE4 | 0 | 0 | 0 |
| B-LEAF1 | 0 | 2 | 2 |
| B-LEAF2 | 0 | 2 | 2 |
| B-LEAF3 | 0 | 2 | 2 |
| B-LEAF4 | 0 | 2 | 2 |
| B-LEAF5 | 0 | 2 | 2 |
| B-LEAF6 | 0 | 2 | 2 |
| B-LEAF7 | 0 | 9 | 9 |
| B-LEAF8 | 0 | 9 | 9 |
| B-SPINE1 | 0 | 0 | 0 |
| B-SPINE2 | 0 | 0 | 0 |
| B-SPINE3 | 0 | 0 | 0 |
| B-SPINE4 | 0 | 0 | 0 |
| B-SW1 | 0 | 1 | 1 |
| BB1 | 0 | 1 | 1 |
| BB2 | 0 | 1 | 1 |
| **TOTAL** | **0** | **57** | **57** |
