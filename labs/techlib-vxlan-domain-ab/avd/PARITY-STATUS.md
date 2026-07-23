# PARITY-STATUS — running tally (auto-generated)

> Generated 2026-07-23 by `avd/scripts/parity_report.py`.
> Contract: **content-set parity** (line ordering exempt) — see
> `PARITY-LEDGER.md` for the class taxonomy and capability verdicts.

## Scoreboard

| Metric | Lines |
|---|---|
| **Residual total (non-exempt)** | **192** |
| MISSING — in the guide, not yet rendered | 38 |
| EXTRA — rendered, not in the guide | 154 |
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

### MISSING — top exact lines (22 distinct)

| count | line |
|---|---|
| 6× | `route type ethernet-segment route-target auto` |
| 4× | `no switchport` |
| 3× | `switchport trunk allowed vlan 40,80` |
| 2× | `switchport` |
| 2× | `network 10.0.2.0/24` |
| 2× | `network 10.1.2.0/24` |
| 2× | `vrf MGMT` |
| 2× | `spanning-tree mode mstp` |
| 2× | `management ssh` |
| 1× | `ip address 10.1.1.2/32` |
| 1× | `ip address 10.1.1.4/32` |
| 1× | `rd 10.0.1.6:10050` |
| 1× | `ip address 10.1.1.6/32` |
| 1× | `network 10.0.2.7/32` |
| 1× | `network 10.1.2.7/32` |

### MISSING — top shapes (digits→`#`)

| count | line |
|---|---|
| 8× | `network #.#.#.#/#` |
| 6× | `route type ethernet-segment route-target auto` |
| 4× | `no switchport` |
| 3× | `ip address #.#.#.#/#` |
| 3× | `switchport trunk allowed vlan #,#` |
| 2× | `switchport` |
| 2× | `vlan #` |
| 2× | `vrf MGMT` |
| 2× | `spanning-tree mode mstp` |
| 2× | `management ssh` |

### EXTRA — top exact lines (60 distinct)

| count | line |
|---|---|
| 19× | `router multicast` |
| 7× | `switchport mode access` |
| 6× | `vrf DEV` |
| 4× | `interface Loopback101` |
| 4× | `vrf PROD` |
| 4× | `interface Loopback102` |
| 4× | `neighbor 10.0.0.1 remote-as 65000` |
| 4× | `neighbor 10.0.0.2 remote-as 65000` |
| 4× | `route-target both 10010:10010` |
| 4× | `route-target both 10070:10070` |
| 4× | `address-family evpn` |
| 4× | `evpn ethernet-segment domain all` |
| 4× | `no neighbor REMOTE-EVPN-PEERS activate` |
| 4× | `redistribute learned` |
| 4× | `switchport` |

### EXTRA — top shapes (digits→`#`)

| count | line |
|---|---|
| 19× | `router multicast` |
| 11× | `ip address #.#.#.#/#` |
| 11× | `rd #.#.#.#:#` |
| 10× | `route-target both #:#` |
| 8× | `interface Loopback#` |
| 8× | `neighbor #.#.#.# remote-as #` |
| 7× | `switchport mode access` |
| 6× | `vrf DEV` |
| 4× | `vrf PROD` |
| 4× | `address-family evpn` |

## Per-node residual

| Node | missing | extra | total |
|---|---|---|---|
| A-LEAF1 | 0 | 1 | 1 |
| A-LEAF2 | 1 | 2 | 3 |
| A-LEAF3 | 0 | 1 | 1 |
| A-LEAF4 | 1 | 2 | 3 |
| A-LEAF5 | 2 | 3 | 5 |
| A-LEAF6 | 2 | 3 | 5 |
| A-LEAF7 | 1 | 18 | 19 |
| A-LEAF8 | 1 | 18 | 19 |
| A-SPINE1 | 0 | 0 | 0 |
| A-SPINE2 | 0 | 0 | 0 |
| A-SPINE3 | 0 | 0 | 0 |
| A-SPINE4 | 0 | 0 | 0 |
| B-LEAF1 | 1 | 1 | 2 |
| B-LEAF2 | 1 | 1 | 2 |
| B-LEAF3 | 1 | 4 | 5 |
| B-LEAF4 | 1 | 4 | 5 |
| B-LEAF5 | 2 | 2 | 4 |
| B-LEAF6 | 2 | 2 | 4 |
| B-LEAF7 | 5 | 28 | 33 |
| B-LEAF8 | 5 | 28 | 33 |
| B-SPINE1 | 0 | 0 | 0 |
| B-SPINE2 | 0 | 0 | 0 |
| B-SPINE3 | 0 | 0 | 0 |
| B-SPINE4 | 0 | 0 | 0 |
| B-SW1 | 6 | 12 | 18 |
| BB1 | 3 | 12 | 15 |
| BB2 | 3 | 12 | 15 |
| **TOTAL** | **38** | **154** | **192** |
