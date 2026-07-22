# PARITY-STATUS — running tally (auto-generated)

> Generated 2026-07-22 by `avd/scripts/parity_report.py`.
> Contract: **content-set parity** (line ordering exempt) — see
> `PARITY-LEDGER.md` for the class taxonomy and capability verdicts.

## Scoreboard

| Metric | Lines |
|---|---|
| **Residual total (non-exempt)** | **529** |
| MISSING — in the guide, not yet rendered | 91 |
| EXTRA — rendered, not in the guide | 438 |
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

### MISSING — top exact lines (40 distinct)

| count | line |
|---|---|
| 17× | `spanning-tree edge-port bpduguard default` |
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

### MISSING — top shapes (digits→`#`)

| count | line |
|---|---|
| 17× | `spanning-tree edge-port bpduguard default` |
| 10× | `vxlan vlan #,# vni #,#` |
| 10× | `vlan #,#` |
| 8× | `network #.#.#.#/#` |
| 6× | `neighbor MLAG-IPV#-PEER route-map RM-MLAG-PEER-OUT out` |
| 6× | `route type ethernet-segment route-target auto` |
| 4× | `vxlan vlan #,#,# vni #,#,#` |
| 4× | `no switchport` |
| 3× | `ip address #.#.#.#/#` |
| 3× | `switchport trunk allowed vlan #,#` |

### EXTRA — top exact lines (136 distinct)

| count | line |
|---|---|
| 38× | `ipv6 enable` |
| 19× | `router multicast` |
| 14× | `vrf PROD` |
| 14× | `vrf DEV` |
| 13× | `spanning-tree bpduguard enable` |
| 10× | `vxlan vlan 10 vni 10010` |
| 10× | `vlan internal order ascending range 1006 1199` |
| 9× | `spanning-tree mst 0 priority 32768` |
| 8× | `set origin incomplete` |
| 8× | `route-map RM-EVPN-SOO-IN deny 10` |
| 8× | `match extcommunity ECL-EVPN-SOO` |
| 8× | `route-map RM-EVPN-SOO-IN permit 20` |
| 8× | `route-map RM-EVPN-SOO-OUT permit 10` |
| 8× | `neighbor LOCAL-EVPN-PEERS route-map RM-EVPN-SOO-IN in` |
| 8× | `neighbor LOCAL-EVPN-PEERS route-map RM-EVPN-SOO-OUT out` |

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
| 13× | `spanning-tree bpduguard enable` |
| 12× | `ip address virtual source-nat vrf DEV address #.#.#.#` |
| 11× | `ip address #.#.#.#/#` |

## Per-node residual

| Node | missing | extra | total |
|---|---|---|---|
| A-LEAF1 | 4 | 13 | 17 |
| A-LEAF2 | 5 | 14 | 19 |
| A-LEAF3 | 4 | 18 | 22 |
| A-LEAF4 | 5 | 19 | 24 |
| A-LEAF5 | 5 | 12 | 17 |
| A-LEAF6 | 5 | 12 | 17 |
| A-LEAF7 | 5 | 33 | 38 |
| A-LEAF8 | 5 | 33 | 38 |
| A-SPINE1 | 0 | 1 | 1 |
| A-SPINE2 | 0 | 1 | 1 |
| A-SPINE3 | 0 | 1 | 1 |
| A-SPINE4 | 0 | 1 | 1 |
| B-LEAF1 | 4 | 17 | 21 |
| B-LEAF2 | 4 | 17 | 21 |
| B-LEAF3 | 4 | 23 | 27 |
| B-LEAF4 | 4 | 23 | 27 |
| B-LEAF5 | 5 | 21 | 26 |
| B-LEAF6 | 5 | 21 | 26 |
| B-LEAF7 | 7 | 48 | 55 |
| B-LEAF8 | 7 | 48 | 55 |
| B-SPINE1 | 0 | 1 | 1 |
| B-SPINE2 | 0 | 1 | 1 |
| B-SPINE3 | 0 | 1 | 1 |
| B-SPINE4 | 0 | 1 | 1 |
| B-SW1 | 7 | 20 | 27 |
| BB1 | 3 | 19 | 22 |
| BB2 | 3 | 19 | 22 |
| **TOTAL** | **91** | **438** | **529** |
