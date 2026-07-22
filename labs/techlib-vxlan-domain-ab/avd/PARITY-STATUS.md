# PARITY-STATUS — running tally (auto-generated)

> Generated 2026-07-22 by `avd/scripts/parity_report.py`.
> Contract: **content-set parity** (line ordering exempt) — see
> `PARITY-LEDGER.md` for the class taxonomy and capability verdicts.

## Scoreboard

| Metric | Lines |
|---|---|
| **Residual total (non-exempt)** | **921** |
| MISSING — in the guide, not yet rendered | 333 |
| EXTRA — rendered, not in the guide | 588 |
| Baseline at campaign start (round-11 models, same contract) | 2,943 |

## Accepted deviations (the exemption list, with today's absorbed counts)

These are the deliberate departures from strict line-for-line parity.
Counts are measured live across both sides so the cost of each
acceptance stays visible.

| Accepted deviation | Lines absorbed today |
|---|---|
| BGP neighbor descriptions (contract amended Day 54 s2) | 436 |
| comment lines | 54 |
| explicit `no shutdown` (accepted AVD default) | 478 |
| interface/host descriptions | 704 |
| line ordering (positions never compared) | n/a — structural |

## Remaining differences

### MISSING — top exact lines (119 distinct)

| count | line |
|---|---|
| 20× | `isis circuit-type level-2` |
| 18× | `address-family ipv4` |
| 18× | `address-family ipv6` |
| 17× | `spanning-tree edge-port bpduguard default` |
| 14× | `no autostate` |
| 12× | `identifier auto lacp` |
| 8× | `mtu 9014` |
| 8× | `address-family ipv4` |
| 8× | `bgp session tracker TRACK-LOCAL-EVPN-PEERS` |
| 8× | `vrf DEV` |
| 6× | `domain-id 100` |
| 6× | `neighbor MLAG-IPV4-PEER route-map RM-MLAG-PEER-OUT out` |
| 6× | `lacp system-id c0d6.8200.0000` |
| 6× | `route type ethernet-segment route-target auto` |
| 6× | `recovery delay 10 seconds` |

### MISSING — top shapes (digits→`#`)

| count | line |
|---|---|
| 36× | `address-family ipv#` |
| 20× | `isis circuit-type level-#` |
| 17× | `spanning-tree edge-port bpduguard default` |
| 14× | `no autostate` |
| 12× | `identifier auto lacp` |
| 12× | `lacp system-id c#d#.#.#` |
| 12× | `net #.#.#.#.#.#` |
| 11× | `ip address #.#.#.#/#` |
| 10× | `vxlan vlan #,# vni #,#` |
| 10× | `vlan #,#` |

### EXTRA — top exact lines (192 distinct)

| count | line |
|---|---|
| 38× | `ipv6 enable` |
| 26× | `switchport mode access` |
| 19× | `router multicast` |
| 16× | `vrf PROD` |
| 14× | `spanning-tree bpduguard enable` |
| 12× | `router bfd` |
| 12× | `multihop interval 1000 min-rx 1000 multiplier 3` |
| 12× | `vrf DEV` |
| 10× | `vxlan vlan 10 vni 10010` |
| 10× | `vlan internal order ascending range 1006 1199` |
| 9× | `spanning-tree mst 0 priority 32768` |
| 8× | `mtu 9114` |
| 8× | `set origin incomplete` |
| 8× | `route-map RM-EVPN-SOO-IN deny 10` |
| 8× | `match extcommunity ECL-EVPN-SOO` |

### EXTRA — top shapes (digits→`#`)

| count | line |
|---|---|
| 38× | `ipv# enable` |
| 34× | `vxlan vlan # vni #` |
| 26× | `switchport mode access` |
| 24× | `router-id #.#.#.#` |
| 19× | `router multicast` |
| 17× | `ip address #.#.#.#/#` |
| 16× | `vrf PROD` |
| 14× | `spanning-tree bpduguard enable` |
| 14× | `ip address virtual source-nat vrf PROD address #.#.#.#` |
| 13× | `rd #.#.#.#:#` |

## Per-node residual

| Node | missing | extra | total |
|---|---|---|---|
| A-LEAF1 | 15 | 22 | 37 |
| A-LEAF2 | 16 | 23 | 39 |
| A-LEAF3 | 21 | 28 | 49 |
| A-LEAF4 | 22 | 29 | 51 |
| A-LEAF5 | 19 | 21 | 40 |
| A-LEAF6 | 23 | 19 | 42 |
| A-LEAF7 | 6 | 40 | 46 |
| A-LEAF8 | 6 | 40 | 46 |
| A-SPINE1 | 0 | 3 | 3 |
| A-SPINE2 | 0 | 3 | 3 |
| A-SPINE3 | 0 | 3 | 3 |
| A-SPINE4 | 0 | 3 | 3 |
| B-LEAF1 | 16 | 27 | 43 |
| B-LEAF2 | 16 | 27 | 43 |
| B-LEAF3 | 46 | 41 | 87 |
| B-LEAF4 | 46 | 41 | 87 |
| B-LEAF5 | 17 | 23 | 40 |
| B-LEAF6 | 17 | 23 | 40 |
| B-LEAF7 | 13 | 53 | 66 |
| B-LEAF8 | 13 | 53 | 66 |
| B-SPINE1 | 2 | 2 | 4 |
| B-SPINE2 | 2 | 2 | 4 |
| B-SPINE3 | 2 | 2 | 4 |
| B-SPINE4 | 2 | 2 | 4 |
| B-SW1 | 7 | 20 | 27 |
| BB1 | 3 | 19 | 22 |
| BB2 | 3 | 19 | 22 |
| **TOTAL** | **333** | **588** | **921** |
