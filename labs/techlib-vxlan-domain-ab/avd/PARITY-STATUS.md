# PARITY-STATUS — running tally (auto-generated)

> Generated 2026-07-22 by `avd/scripts/parity_report.py`.
> Contract: **content-set parity** (line ordering exempt) — see
> `PARITY-LEDGER.md` for the class taxonomy and capability verdicts.

## Scoreboard

| Metric | Lines |
|---|---|
| **Residual total (non-exempt)** | **1705** |
| MISSING — in the guide, not yet rendered | 706 |
| EXTRA — rendered, not in the guide | 999 |
| Baseline at campaign start (round-11 models, same contract) | 2,943 |

## Accepted deviations (the exemption list, with today's absorbed counts)

These are the deliberate departures from strict line-for-line parity.
Counts are measured live across both sides so the cost of each
acceptance stays visible.

| Accepted deviation | Lines absorbed today |
|---|---|
| comment lines | 54 |
| explicit `no shutdown` (accepted AVD default) | 492 |
| interface/host descriptions | 720 |
| line ordering (positions never compared) | n/a — structural |

## Remaining differences

### MISSING — top exact lines (228 distinct)

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
| 12× | `ip prefix-list PL-LOOPBACKS` |
| 12× | `seq 10 permit 10.0.0.0/16 eq 32` |

### MISSING — top shapes (digits→`#`)

| count | line |
|---|---|
| 36× | `address-family ipv#` |
| 34× | `pim ipv# local-interface Loopback#` |
| 32× | `no switchport` |
| 32× | `neighbor #.#.#.# description A-SPINE#.IPV#` |
| 32× | `neighbor #.#.#.# description A-LEAF#.IPV#` |
| 30× | `seq # permit #.#.#.#/# eq #` |
| 26× | `mld` |
| 20× | `routing` |
| 20× | `ipv#` |
| 20× | `isis circuit-type level-#` |

### EXTRA — top exact lines (402 distinct)

| count | line |
|---|---|
| 38× | `ipv6 enable` |
| 26× | `switchport mode access` |
| 16× | `mtu 9114` |
| 14× | `spanning-tree bpduguard enable` |
| 12× | `ip prefix-list PL-LOOPBACKS-EVPN-OVERLAY` |
| 12× | `seq 10 permit 10.0.1.0/24 eq 32` |
| 12× | `match ip address prefix-list PL-LOOPBACKS-EVPN-OVERLAY` |
| 12× | `router bfd` |
| 12× | `multihop interval 1000 min-rx 1000 multiplier 3` |
| 10× | `vxlan vlan 10 vni 10010` |
| 10× | `set origin incomplete` |
| 10× | `vlan internal order ascending range 1006 1199` |
| 9× | `spanning-tree mst 0 priority 32768` |
| 8× | `no spanning-tree vlan-id 4093-4094` |
| 8× | `seq 20 permit 10.1.1.0/24 eq 32` |

### EXTRA — top shapes (digits→`#`)

| count | line |
|---|---|
| 80× | `neighbor #.#.#.# remote-as #` |
| 38× | `ipv# enable` |
| 34× | `vxlan vlan # vni #` |
| 32× | `neighbor #.#.#.# description A-SPINE#_Ethernet#` |
| 32× | `neighbor #.#.#.# description A-LEAF#_Ethernet#` |
| 26× | `switchport mode access` |
| 26× | `ip address #.#.#.#/#` |
| 24× | `router-id #.#.#.#` |
| 21× | `rd #.#.#.#:#` |
| 20× | `seq # permit #.#.#.#/# eq #` |

## Per-node residual

| Node | missing | extra | total |
|---|---|---|---|
| A-LEAF1 | 38 | 40 | 78 |
| A-LEAF2 | 39 | 41 | 80 |
| A-LEAF3 | 47 | 46 | 93 |
| A-LEAF4 | 48 | 47 | 95 |
| A-LEAF5 | 41 | 39 | 80 |
| A-LEAF6 | 45 | 37 | 82 |
| A-LEAF7 | 21 | 130 | 151 |
| A-LEAF8 | 22 | 131 | 153 |
| A-SPINE1 | 14 | 14 | 28 |
| A-SPINE2 | 14 | 14 | 28 |
| A-SPINE3 | 14 | 14 | 28 |
| A-SPINE4 | 14 | 14 | 28 |
| B-LEAF1 | 25 | 25 | 50 |
| B-LEAF2 | 25 | 25 | 50 |
| B-LEAF3 | 54 | 39 | 93 |
| B-LEAF4 | 54 | 39 | 93 |
| B-LEAF5 | 27 | 20 | 47 |
| B-LEAF6 | 27 | 20 | 47 |
| B-LEAF7 | 18 | 65 | 83 |
| B-LEAF8 | 18 | 65 | 83 |
| B-SPINE1 | 12 | 2 | 14 |
| B-SPINE2 | 12 | 2 | 14 |
| B-SPINE3 | 12 | 2 | 14 |
| B-SPINE4 | 12 | 2 | 14 |
| B-SW1 | 7 | 20 | 27 |
| BB1 | 23 | 53 | 76 |
| BB2 | 23 | 53 | 76 |
| **TOTAL** | **706** | **999** | **1705** |
