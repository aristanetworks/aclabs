# PARITY-STATUS — running tally (auto-generated)

> Generated 2026-07-23 by `avd/scripts/parity_report.py`.
> Contract: **content-set parity** (line ordering exempt) — see
> `PARITY-LEDGER.md` for the class taxonomy and capability verdicts.

## Scoreboard

| Metric | Lines |
|---|---|
| **Residual total (non-exempt)** | **240** |
| MISSING — in the guide, not yet rendered | 52 |
| EXTRA — rendered, not in the guide | 188 |
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
| interface/host descriptions | 697 |
| line ordering (positions never compared) | n/a — structural |

## Remaining differences

### MISSING — top exact lines (29 distinct)

| count | line |
|---|---|
| 6× | `route type ethernet-segment route-target auto` |
| 4× | `no switchport` |
| 3× | `vxlan vlan 10,70 vni 10010,10070` |
| 3× | `switchport trunk allowed vlan 40,80` |
| 2× | `vxlan vlan 10,30 vni 10010,10030` |
| 2× | `vxlan vlan 10,30,50 vni 10010,10030,10050` |
| 2× | `switchport` |
| 2× | `vxlan vlan 10,50,70 vni 10010,10050,10070` |
| 2× | `vxlan vlan 20,40 vni 10020,10040` |
| 2× | `vxlan vlan 40,80 vni 10040,10080` |
| 2× | `network 10.0.2.0/24` |
| 2× | `network 10.1.2.0/24` |
| 2× | `vrf MGMT` |
| 2× | `spanning-tree mode mstp` |
| 2× | `management ssh` |

### MISSING — top shapes (digits→`#`)

| count | line |
|---|---|
| 10× | `vxlan vlan #,# vni #,#` |
| 8× | `network #.#.#.#/#` |
| 6× | `route type ethernet-segment route-target auto` |
| 4× | `vxlan vlan #,#,# vni #,#,#` |
| 4× | `no switchport` |
| 3× | `ip address #.#.#.#/#` |
| 3× | `switchport trunk allowed vlan #,#` |
| 2× | `switchport` |
| 2× | `vlan #` |
| 2× | `vrf MGMT` |

### EXTRA — top exact lines (68 distinct)

| count | line |
|---|---|
| 19× | `router multicast` |
| 10× | `vxlan vlan 10 vni 10010` |
| 7× | `switchport mode access` |
| 6× | `vrf DEV` |
| 5× | `vxlan vlan 70 vni 10070` |
| 4× | `vxlan vlan 30 vni 10030` |
| 4× | `vxlan vlan 50 vni 10050` |
| 4× | `interface Loopback101` |
| 4× | `vrf PROD` |
| 4× | `interface Loopback102` |
| 4× | `neighbor 10.0.0.1 remote-as 65000` |
| 4× | `neighbor 10.0.0.2 remote-as 65000` |
| 4× | `route-target both 10010:10010` |
| 4× | `route-target both 10070:10070` |
| 4× | `address-family evpn` |

### EXTRA — top shapes (digits→`#`)

| count | line |
|---|---|
| 34× | `vxlan vlan # vni #` |
| 19× | `router multicast` |
| 11× | `ip address #.#.#.#/#` |
| 11× | `rd #.#.#.#:#` |
| 10× | `route-target both #:#` |
| 8× | `interface Loopback#` |
| 8× | `neighbor #.#.#.# remote-as #` |
| 7× | `switchport mode access` |
| 6× | `vrf DEV` |
| 4× | `vrf PROD` |

## Per-node residual

| Node | missing | extra | total |
|---|---|---|---|
| A-LEAF1 | 1 | 3 | 4 |
| A-LEAF2 | 2 | 4 | 6 |
| A-LEAF3 | 1 | 4 | 5 |
| A-LEAF4 | 2 | 5 | 7 |
| A-LEAF5 | 2 | 3 | 5 |
| A-LEAF6 | 2 | 3 | 5 |
| A-LEAF7 | 2 | 21 | 23 |
| A-LEAF8 | 2 | 21 | 23 |
| A-SPINE1 | 0 | 0 | 0 |
| A-SPINE2 | 0 | 0 | 0 |
| A-SPINE3 | 0 | 0 | 0 |
| A-SPINE4 | 0 | 0 | 0 |
| B-LEAF1 | 2 | 3 | 5 |
| B-LEAF2 | 2 | 3 | 5 |
| B-LEAF3 | 2 | 6 | 8 |
| B-LEAF4 | 2 | 6 | 8 |
| B-LEAF5 | 3 | 4 | 7 |
| B-LEAF6 | 3 | 4 | 7 |
| B-LEAF7 | 6 | 31 | 37 |
| B-LEAF8 | 6 | 31 | 37 |
| B-SPINE1 | 0 | 0 | 0 |
| B-SPINE2 | 0 | 0 | 0 |
| B-SPINE3 | 0 | 0 | 0 |
| B-SPINE4 | 0 | 0 | 0 |
| B-SW1 | 6 | 12 | 18 |
| BB1 | 3 | 12 | 15 |
| BB2 | 3 | 12 | 15 |
| **TOTAL** | **52** | **188** | **240** |
