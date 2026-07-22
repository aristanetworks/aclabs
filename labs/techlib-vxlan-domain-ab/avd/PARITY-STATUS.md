# PARITY-STATUS — running tally (auto-generated)

> Generated 2026-07-22 by `avd/scripts/parity_report.py`.
> Contract: **content-set parity** (line ordering exempt) — see
> `PARITY-LEDGER.md` for the class taxonomy and capability verdicts.

## Scoreboard

| Metric | Lines |
|---|---|
| **Residual total (non-exempt)** | **735** |
| MISSING — in the guide, not yet rendered | 227 |
| EXTRA — rendered, not in the guide | 508 |
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

### MISSING — top exact lines (68 distinct)

| count | line |
|---|---|
| 20× | `isis circuit-type level-2` |
| 18× | `address-family ipv4` |
| 18× | `address-family ipv6` |
| 17× | `spanning-tree edge-port bpduguard default` |
| 14× | `no autostate` |
| 8× | `mtu 9014` |
| 8× | `address-family ipv4` |
| 6× | `domain-id 100` |
| 6× | `neighbor MLAG-IPV4-PEER route-map RM-MLAG-PEER-OUT out` |
| 6× | `route type ethernet-segment route-target auto` |
| 6× | `recovery delay 10 seconds` |
| 4× | `neighbor 192.0.0.1 activate` |
| 4× | `neighbor 192.0.0.0 activate` |
| 4× | `no switchport` |
| 4× | `neighbor REMOTE-EVPN-PEERS remote-as 65000` |

### MISSING — top shapes (digits→`#`)

| count | line |
|---|---|
| 36× | `address-family ipv#` |
| 20× | `isis circuit-type level-#` |
| 17× | `spanning-tree edge-port bpduguard default` |
| 14× | `no autostate` |
| 12× | `net #.#.#.#.#.#` |
| 10× | `vxlan vlan #,# vni #,#` |
| 10× | `vlan #,#` |
| 9× | `ip address #.#.#.#/#` |
| 8× | `mtu #` |
| 8× | `address-family ipv#` |

### EXTRA — top exact lines (158 distinct)

| count | line |
|---|---|
| 38× | `ipv6 enable` |
| 19× | `router multicast` |
| 14× | `vrf PROD` |
| 14× | `vrf DEV` |
| 13× | `spanning-tree bpduguard enable` |
| 12× | `router bfd` |
| 12× | `multihop interval 1000 min-rx 1000 multiplier 3` |
| 10× | `vxlan vlan 10 vni 10010` |
| 10× | `vlan internal order ascending range 1006 1199` |
| 9× | `spanning-tree mst 0 priority 32768` |
| 8× | `mtu 9114` |
| 8× | `set origin incomplete` |
| 8× | `route-map RM-EVPN-SOO-IN deny 10` |
| 8× | `match extcommunity ECL-EVPN-SOO` |
| 8× | `route-map RM-EVPN-SOO-IN permit 20` |

### EXTRA — top shapes (digits→`#`)

| count | line |
|---|---|
| 38× | `ipv# enable` |
| 34× | `vxlan vlan # vni #` |
| 26× | `router-id #.#.#.#` |
| 19× | `router multicast` |
| 17× | `ip address #.#.#.#/#` |
| 14× | `vrf PROD` |
| 14× | `ip address virtual source-nat vrf PROD address #.#.#.#` |
| 14× | `vrf DEV` |
| 13× | `spanning-tree bpduguard enable` |
| 12× | `router bfd` |

## Per-node residual

| Node | missing | extra | total |
|---|---|---|---|
| A-LEAF1 | 15 | 20 | 35 |
| A-LEAF2 | 16 | 21 | 37 |
| A-LEAF3 | 21 | 26 | 47 |
| A-LEAF4 | 22 | 27 | 49 |
| A-LEAF5 | 16 | 19 | 35 |
| A-LEAF6 | 16 | 19 | 35 |
| A-LEAF7 | 4 | 33 | 37 |
| A-LEAF8 | 4 | 33 | 37 |
| A-SPINE1 | 0 | 3 | 3 |
| A-SPINE2 | 0 | 3 | 3 |
| A-SPINE3 | 0 | 3 | 3 |
| A-SPINE4 | 0 | 3 | 3 |
| B-LEAF1 | 10 | 19 | 29 |
| B-LEAF2 | 10 | 19 | 29 |
| B-LEAF3 | 12 | 25 | 37 |
| B-LEAF4 | 12 | 25 | 37 |
| B-LEAF5 | 13 | 23 | 36 |
| B-LEAF6 | 13 | 23 | 36 |
| B-LEAF7 | 11 | 49 | 60 |
| B-LEAF8 | 11 | 49 | 60 |
| B-SPINE1 | 2 | 2 | 4 |
| B-SPINE2 | 2 | 2 | 4 |
| B-SPINE3 | 2 | 2 | 4 |
| B-SPINE4 | 2 | 2 | 4 |
| B-SW1 | 7 | 20 | 27 |
| BB1 | 3 | 19 | 22 |
| BB2 | 3 | 19 | 22 |
| **TOTAL** | **227** | **508** | **735** |
