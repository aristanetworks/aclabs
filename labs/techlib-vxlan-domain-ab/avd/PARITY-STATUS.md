# PARITY-STATUS — running tally (auto-generated)

> Generated 2026-07-22 by `avd/scripts/parity_report.py`.
> Contract: **content-set parity** (line ordering exempt) — see
> `PARITY-LEDGER.md` for the class taxonomy and capability verdicts.

## Scoreboard

| Metric | Lines |
|---|---|
| **Residual total (non-exempt)** | **1157** |
| MISSING — in the guide, not yet rendered | 527 |
| EXTRA — rendered, not in the guide | 630 |
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

### MISSING — top exact lines (128 distinct)

| count | line |
|---|---|
| 32× | `no switchport` |
| 32× | `pim ipv4 local-interface Loopback0` |
| 26× | `mld` |
| 20× | `routing` |
| 20× | `isis circuit-type level-2` |
| 18× | `address-family ipv4` |
| 18× | `address-family ipv6` |
| 18× | `ipv6` |
| 17× | `spanning-tree edge-port bpduguard default` |
| 16× | `pim ipv4 sparse-mode` |
| 14× | `ip igmp` |
| 14× | `no autostate` |
| 12× | `vxlan multicast ipv6` |
| 12× | `mld snooping` |
| 12× | `identifier auto lacp` |

### MISSING — top shapes (digits→`#`)

| count | line |
|---|---|
| 36× | `address-family ipv#` |
| 34× | `pim ipv# local-interface Loopback#` |
| 32× | `no switchport` |
| 26× | `mld` |
| 20× | `routing` |
| 20× | `ipv#` |
| 20× | `isis circuit-type level-#` |
| 17× | `spanning-tree edge-port bpduguard default` |
| 16× | `pim ipv# sparse-mode` |
| 14× | `ip igmp` |

### EXTRA — top exact lines (229 distinct)

| count | line |
|---|---|
| 38× | `ipv6 enable` |
| 26× | `switchport mode access` |
| 14× | `spanning-tree bpduguard enable` |
| 12× | `router bfd` |
| 12× | `multihop interval 1000 min-rx 1000 multiplier 3` |
| 10× | `vxlan vlan 10 vni 10010` |
| 10× | `vlan internal order ascending range 1006 1199` |
| 9× | `spanning-tree mst 0 priority 32768` |
| 8× | `mtu 9114` |
| 8× | `set origin incomplete` |
| 8× | `neighbor 10.0.1.201 remote-as 65100` |
| 8× | `neighbor 10.0.1.202 remote-as 65100` |
| 8× | `neighbor 10.0.1.203 remote-as 65100` |
| 8× | `neighbor 10.0.1.204 remote-as 65100` |
| 8× | `route-map RM-EVPN-SOO-IN deny 10` |

### EXTRA — top shapes (digits→`#`)

| count | line |
|---|---|
| 72× | `neighbor #.#.#.# remote-as #` |
| 38× | `ipv# enable` |
| 34× | `vxlan vlan # vni #` |
| 26× | `switchport mode access` |
| 24× | `router-id #.#.#.#` |
| 17× | `ip address #.#.#.#/#` |
| 14× | `spanning-tree bpduguard enable` |
| 14× | `ip address virtual source-nat vrf PROD address #.#.#.#` |
| 13× | `rd #.#.#.#:#` |
| 12× | `router bfd` |

## Per-node residual

| Node | missing | extra | total |
|---|---|---|---|
| A-LEAF1 | 29 | 29 | 58 |
| A-LEAF2 | 30 | 30 | 60 |
| A-LEAF3 | 38 | 34 | 72 |
| A-LEAF4 | 39 | 35 | 74 |
| A-LEAF5 | 32 | 28 | 60 |
| A-LEAF6 | 36 | 26 | 62 |
| A-LEAF7 | 8 | 48 | 56 |
| A-LEAF8 | 8 | 48 | 56 |
| A-SPINE1 | 2 | 3 | 5 |
| A-SPINE2 | 2 | 3 | 5 |
| A-SPINE3 | 2 | 3 | 5 |
| A-SPINE4 | 2 | 3 | 5 |
| B-LEAF1 | 25 | 25 | 50 |
| B-LEAF2 | 25 | 25 | 50 |
| B-LEAF3 | 54 | 39 | 93 |
| B-LEAF4 | 54 | 39 | 93 |
| B-LEAF5 | 27 | 20 | 47 |
| B-LEAF6 | 27 | 20 | 47 |
| B-LEAF7 | 13 | 53 | 66 |
| B-LEAF8 | 13 | 53 | 66 |
| B-SPINE1 | 12 | 2 | 14 |
| B-SPINE2 | 12 | 2 | 14 |
| B-SPINE3 | 12 | 2 | 14 |
| B-SPINE4 | 12 | 2 | 14 |
| B-SW1 | 7 | 20 | 27 |
| BB1 | 3 | 19 | 22 |
| BB2 | 3 | 19 | 22 |
| **TOTAL** | **527** | **630** | **1157** |
