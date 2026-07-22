# PARITY-STATUS — running tally (auto-generated)

> Generated 2026-07-22 by `avd/scripts/parity_report.py`.
> Contract: **content-set parity** (line ordering exempt) — see
> `PARITY-LEDGER.md` for the class taxonomy and capability verdicts.

## Scoreboard

| Metric | Lines |
|---|---|
| **Residual total (non-exempt)** | **1089** |
| MISSING — in the guide, not yet rendered | 465 |
| EXTRA — rendered, not in the guide | 624 |
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

### MISSING — top exact lines (125 distinct)

| count | line |
|---|---|
| 32× | `no switchport` |
| 26× | `mld` |
| 20× | `routing` |
| 20× | `isis circuit-type level-2` |
| 18× | `address-family ipv4` |
| 18× | `address-family ipv6` |
| 18× | `ipv6` |
| 17× | `spanning-tree edge-port bpduguard default` |
| 14× | `no autostate` |
| 12× | `vxlan multicast ipv6` |
| 12× | `mld snooping` |
| 12× | `identifier auto lacp` |
| 8× | `mtu 9014` |
| 8× | `neighbor LOCAL-EVPN-PEERS remote-as 65100` |
| 8× | `neighbor LOCAL-IPV4-PEERS remote-as 65100` |

### MISSING — top shapes (digits→`#`)

| count | line |
|---|---|
| 36× | `address-family ipv#` |
| 32× | `no switchport` |
| 26× | `mld` |
| 20× | `routing` |
| 20× | `ipv#` |
| 20× | `isis circuit-type level-#` |
| 17× | `spanning-tree edge-port bpduguard default` |
| 14× | `no autostate` |
| 12× | `vxlan multicast ipv#` |
| 12× | `mld snooping` |

### EXTRA — top exact lines (228 distinct)

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
| A-LEAF1 | 27 | 28 | 55 |
| A-LEAF2 | 28 | 29 | 57 |
| A-LEAF3 | 35 | 33 | 68 |
| A-LEAF4 | 36 | 34 | 70 |
| A-LEAF5 | 30 | 27 | 57 |
| A-LEAF6 | 34 | 25 | 59 |
| A-LEAF7 | 8 | 48 | 56 |
| A-LEAF8 | 8 | 48 | 56 |
| A-SPINE1 | 0 | 3 | 3 |
| A-SPINE2 | 0 | 3 | 3 |
| A-SPINE3 | 0 | 3 | 3 |
| A-SPINE4 | 0 | 3 | 3 |
| B-LEAF1 | 25 | 25 | 50 |
| B-LEAF2 | 25 | 25 | 50 |
| B-LEAF3 | 54 | 39 | 93 |
| B-LEAF4 | 54 | 39 | 93 |
| B-LEAF5 | 27 | 20 | 47 |
| B-LEAF6 | 27 | 20 | 47 |
| B-LEAF7 | 13 | 53 | 66 |
| B-LEAF8 | 13 | 53 | 66 |
| B-SPINE1 | 2 | 2 | 4 |
| B-SPINE2 | 2 | 2 | 4 |
| B-SPINE3 | 2 | 2 | 4 |
| B-SPINE4 | 2 | 2 | 4 |
| B-SW1 | 7 | 20 | 27 |
| BB1 | 3 | 19 | 22 |
| BB2 | 3 | 19 | 22 |
| **TOTAL** | **465** | **624** | **1089** |
