# PARITY-STATUS — running tally (auto-generated)

> Generated 2026-07-23 by `avd/scripts/parity_report.py`.
> Contract: **content-set parity** (line ordering exempt) — see
> `PARITY-LEDGER.md` for the class taxonomy and capability verdicts.

## Scoreboard

| Metric | Lines |
|---|---|
| **Residual total (non-exempt)** | **90** |
| MISSING — in the guide, not yet rendered | 19 |
| EXTRA — rendered, not in the guide | 71 |
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

### MISSING — top exact lines (11 distinct)

| count | line |
|---|---|
| 6× | `route type ethernet-segment route-target auto` |
| 3× | `switchport trunk allowed vlan 40,80` |
| 2× | `switchport` |
| 1× | `ip address 10.1.1.2/32` |
| 1× | `ip address 10.1.1.4/32` |
| 1× | `rd 10.0.1.6:10050` |
| 1× | `ip address 10.1.1.6/32` |
| 1× | `vlan 40` |
| 1× | `name Purple` |
| 1× | `vlan 80` |
| 1× | `name Black` |

### MISSING — top shapes (digits→`#`)

| count | line |
|---|---|
| 6× | `route type ethernet-segment route-target auto` |
| 3× | `ip address #.#.#.#/#` |
| 3× | `switchport trunk allowed vlan #,#` |
| 2× | `switchport` |
| 2× | `vlan #` |
| 1× | `rd #.#.#.#:#` |
| 1× | `name Purple` |
| 1× | `name Black` |

### EXTRA — top exact lines (21 distinct)

| count | line |
|---|---|
| 19× | `router multicast` |
| 4× | `switchport mode access` |
| 4× | `interface Loopback101` |
| 4× | `vrf PROD` |
| 4× | `interface Loopback102` |
| 4× | `vrf DEV` |
| 4× | `address-family evpn` |
| 4× | `evpn ethernet-segment domain all` |
| 3× | `switchport trunk allowed vlan none` |
| 3× | `switchport` |
| 2× | `ip address 10.101.101.7/32` |
| 2× | `ip address 10.102.102.7/32` |
| 2× | `ip address 10.101.101.8/32` |
| 2× | `ip address 10.102.102.8/32` |
| 2× | `interface Port-Channel7` |

### EXTRA — top shapes (digits→`#`)

| count | line |
|---|---|
| 19× | `router multicast` |
| 11× | `ip address #.#.#.#/#` |
| 8× | `interface Loopback#` |
| 4× | `switchport mode access` |
| 4× | `vrf PROD` |
| 4× | `vrf DEV` |
| 4× | `address-family evpn` |
| 4× | `evpn ethernet-segment domain all` |
| 3× | `switchport trunk allowed vlan none` |
| 3× | `switchport` |

## Per-node residual

| Node | missing | extra | total |
|---|---|---|---|
| A-LEAF1 | 0 | 1 | 1 |
| A-LEAF2 | 1 | 2 | 3 |
| A-LEAF3 | 0 | 1 | 1 |
| A-LEAF4 | 1 | 2 | 3 |
| A-LEAF5 | 1 | 3 | 4 |
| A-LEAF6 | 1 | 3 | 4 |
| A-LEAF7 | 1 | 9 | 10 |
| A-LEAF8 | 1 | 9 | 10 |
| A-SPINE1 | 0 | 0 | 0 |
| A-SPINE2 | 0 | 0 | 0 |
| A-SPINE3 | 0 | 0 | 0 |
| A-SPINE4 | 0 | 0 | 0 |
| B-LEAF1 | 1 | 1 | 2 |
| B-LEAF2 | 1 | 1 | 2 |
| B-LEAF3 | 1 | 5 | 6 |
| B-LEAF4 | 1 | 5 | 6 |
| B-LEAF5 | 2 | 2 | 4 |
| B-LEAF6 | 2 | 2 | 4 |
| B-LEAF7 | 0 | 9 | 9 |
| B-LEAF8 | 0 | 9 | 9 |
| B-SPINE1 | 0 | 0 | 0 |
| B-SPINE2 | 0 | 0 | 0 |
| B-SPINE3 | 0 | 0 | 0 |
| B-SPINE4 | 0 | 0 | 0 |
| B-SW1 | 5 | 5 | 10 |
| BB1 | 0 | 1 | 1 |
| BB2 | 0 | 1 | 1 |
| **TOTAL** | **19** | **71** | **90** |
