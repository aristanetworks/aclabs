# PARITY-STATUS — running tally (auto-generated)

> Generated 2026-07-22 by `avd/scripts/parity_report.py`.
> Contract: **content-set parity** (line ordering exempt) — see
> `PARITY-LEDGER.md` for the class taxonomy and capability verdicts.

## Scoreboard

| Metric | Lines |
|---|---|
| **Residual total (non-exempt)** | **407** |
| MISSING — in the guide, not yet rendered | 74 |
| EXTRA — rendered, not in the guide | 333 |
| Baseline at campaign start (round-11 models, same contract) | 2,943 |

## Accepted deviations (the exemption list, with today's absorbed counts)

These are the deliberate departures from strict line-for-line parity.
Counts are measured live across both sides so the cost of each
acceptance stays visible.

| Accepted deviation | Lines absorbed today |
|---|---|
| BGP neighbor descriptions (contract amended Day 54 s2) | 436 |
| comment lines | 54 |
| explicit `no shutdown` (accepted AVD default) | 481 |
| interface/host descriptions | 707 |
| line ordering (positions never compared) | n/a — structural |

## Remaining differences

### MISSING — top exact lines (39 distinct)

| count | line |
|---|---|
| 6× | `neighbor MLAG-IPV4-PEER route-map RM-MLAG-PEER-OUT out` |
| 6× | `route type ethernet-segment route-target auto` |
| 4× | `no switchport` |
| 3× | `vxlan vlan 10,70 vni 10010,10070` |
| 3× | `switchport trunk allowed vlan 40,80` |
| 2× | `vxlan vlan 10,30 vni 10010,10030` |
| 2× | `vlan 10,30` |
| 2× | `vxlan vlan 10,30,50 vni 10010,10030,10050` |
| 2× | `vlan 10,30,50` |
| 2× | `vlan 50,70` |
| 2× | `switchport` |
| 2× | `vxlan vlan 10,50,70 vni 10010,10050,10070` |
| 2× | `router bfd` |
| 2× | `multihop interval 1000 min-rx 1000 multiplier 3` |
| 2× | `vxlan vlan 20,40 vni 10020,10040` |

### MISSING — top shapes (digits→`#`)

| count | line |
|---|---|
| 10× | `vxlan vlan #,# vni #,#` |
| 10× | `vlan #,#` |
| 8× | `network #.#.#.#/#` |
| 6× | `neighbor MLAG-IPV#-PEER route-map RM-MLAG-PEER-OUT out` |
| 6× | `route type ethernet-segment route-target auto` |
| 4× | `vxlan vlan #,#,# vni #,#,#` |
| 4× | `no switchport` |
| 3× | `ip address #.#.#.#/#` |
| 3× | `switchport trunk allowed vlan #,#` |
| 2× | `vlan #,#,#` |

### EXTRA — top exact lines (108 distinct)

| count | line |
|---|---|
| 38× | `ipv6 enable` |
| 19× | `router multicast` |
| 14× | `vrf PROD` |
| 14× | `vrf DEV` |
| 10× | `vxlan vlan 10 vni 10010` |
| 8× | `set origin incomplete` |
| 7× | `switchport mode access` |
| 7× | `ipv4` |
| 6× | `route-map RM-MLAG-PEER-IN permit 10` |
| 6× | `neighbor MLAG-IPV4-PEER route-map RM-MLAG-PEER-IN in` |
| 5× | `vxlan vlan 70 vni 10070` |
| 4× | `vxlan vlan 30 vni 10030` |
| 4× | `vxlan vlan 50 vni 10050` |
| 4× | `interface Loopback101` |
| 4× | `interface Loopback102` |

### EXTRA — top shapes (digits→`#`)

| count | line |
|---|---|
| 38× | `ipv# enable` |
| 34× | `vxlan vlan # vni #` |
| 26× | `router-id #.#.#.#` |
| 19× | `router multicast` |
| 14× | `vrf PROD` |
| 14× | `ip address virtual source-nat vrf PROD address #.#.#.#` |
| 14× | `vrf DEV` |
| 12× | `ip address virtual source-nat vrf DEV address #.#.#.#` |
| 11× | `ip address #.#.#.#/#` |
| 11× | `rd #.#.#.#:#` |

## Per-node residual

| Node | missing | extra | total |
|---|---|---|---|
| A-LEAF1 | 3 | 11 | 14 |
| A-LEAF2 | 4 | 12 | 16 |
| A-LEAF3 | 3 | 16 | 19 |
| A-LEAF4 | 4 | 17 | 21 |
| A-LEAF5 | 4 | 11 | 15 |
| A-LEAF6 | 4 | 11 | 15 |
| A-LEAF7 | 4 | 33 | 37 |
| A-LEAF8 | 4 | 33 | 37 |
| A-SPINE1 | 0 | 0 | 0 |
| A-SPINE2 | 0 | 0 | 0 |
| A-SPINE3 | 0 | 0 | 0 |
| A-SPINE4 | 0 | 0 | 0 |
| B-LEAF1 | 3 | 8 | 11 |
| B-LEAF2 | 3 | 8 | 11 |
| B-LEAF3 | 3 | 14 | 17 |
| B-LEAF4 | 3 | 14 | 17 |
| B-LEAF5 | 4 | 12 | 16 |
| B-LEAF6 | 4 | 12 | 16 |
| B-LEAF7 | 6 | 39 | 45 |
| B-LEAF8 | 6 | 39 | 45 |
| B-SPINE1 | 0 | 0 | 0 |
| B-SPINE2 | 0 | 0 | 0 |
| B-SPINE3 | 0 | 0 | 0 |
| B-SPINE4 | 0 | 0 | 0 |
| B-SW1 | 6 | 13 | 19 |
| BB1 | 3 | 15 | 18 |
| BB2 | 3 | 15 | 18 |
| **TOTAL** | **74** | **333** | **407** |
