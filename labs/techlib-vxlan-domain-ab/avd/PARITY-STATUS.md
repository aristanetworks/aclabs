# PARITY-STATUS — running tally (auto-generated)

> Generated 2026-07-22 by `avd/scripts/parity_report.py`.
> Contract: **content-set parity** (line ordering exempt) — see
> `PARITY-LEDGER.md` for the class taxonomy and capability verdicts.

## Scoreboard

| Metric | Lines |
|---|---|
| **Residual total (non-exempt)** | **1905** |
| MISSING — in the guide, not yet rendered | 750 |
| EXTRA — rendered, not in the guide | 1155 |
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

### MISSING — top exact lines (229 distinct)

| count | line |
|---|---|
| 32× | `no switchport` |
| 32× | `pim ipv4 local-interface Loopback0` |
| 26× | `mld` |
| 26× | `neighbor default send-community` |
| 20× | `routing` |
| 20× | `isis circuit-type level-2` |
| 18× | `address-family ipv4` |
| 18× | `address-family ipv6` |
| 18× | `ipv6` |
| 17× | `spanning-tree edge-port bpduguard default` |
| 16× | `pim ipv4 sparse-mode` |
| 14× | `ip igmp` |
| 14× | `no autostate` |
| 14× | `update wait-install` |
| 12× | `vxlan multicast ipv6` |

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
| 26× | `neighbor default send-community` |
| 20× | `routing` |
| 20× | `ipv#` |

### EXTRA — top exact lines (421 distinct)

| count | line |
|---|---|
| 38× | `ipv6 enable` |
| 26× | `switchport mode access` |
| 24× | `neighbor LOCAL-EVPN-PEERS send-community` |
| 24× | `neighbor LOCAL-EVPN-PEERS maximum-routes 0` |
| 24× | `no neighbor LOCAL-EVPN-PEERS activate` |
| 16× | `mtu 9114` |
| 14× | `spanning-tree bpduguard enable` |
| 12× | `ip prefix-list PL-LOOPBACKS-EVPN-OVERLAY` |
| 12× | `seq 10 permit 10.0.1.0/24 eq 32` |
| 12× | `match ip address prefix-list PL-LOOPBACKS-EVPN-OVERLAY` |
| 12× | `router bfd` |
| 12× | `multihop interval 1000 min-rx 1000 multiplier 3` |
| 12× | `maximum-paths 4` |
| 12× | `neighbor LOCAL-IPV4-PEERS send-community` |
| 12× | `neighbor LOCAL-IPV4-PEERS maximum-routes 256000` |

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
| 24× | `neighbor LOCAL-EVPN-PEERS send-community` |
| 24× | `neighbor LOCAL-EVPN-PEERS maximum-routes #` |
| 24× | `no neighbor LOCAL-EVPN-PEERS activate` |

## Per-node residual

| Node | missing | extra | total |
|---|---|---|---|
| A-LEAF1 | 40 | 49 | 89 |
| A-LEAF2 | 41 | 50 | 91 |
| A-LEAF3 | 49 | 55 | 104 |
| A-LEAF4 | 50 | 56 | 106 |
| A-LEAF5 | 43 | 48 | 91 |
| A-LEAF6 | 47 | 46 | 93 |
| A-LEAF7 | 23 | 139 | 162 |
| A-LEAF8 | 24 | 140 | 164 |
| A-SPINE1 | 15 | 19 | 34 |
| A-SPINE2 | 15 | 19 | 34 |
| A-SPINE3 | 15 | 19 | 34 |
| A-SPINE4 | 15 | 19 | 34 |
| B-LEAF1 | 27 | 30 | 57 |
| B-LEAF2 | 27 | 30 | 57 |
| B-LEAF3 | 56 | 44 | 100 |
| B-LEAF4 | 56 | 44 | 100 |
| B-LEAF5 | 30 | 25 | 55 |
| B-LEAF6 | 30 | 25 | 55 |
| B-LEAF7 | 21 | 69 | 90 |
| B-LEAF8 | 21 | 69 | 90 |
| B-SPINE1 | 13 | 8 | 21 |
| B-SPINE2 | 13 | 8 | 21 |
| B-SPINE3 | 13 | 8 | 21 |
| B-SPINE4 | 13 | 8 | 21 |
| B-SW1 | 7 | 20 | 27 |
| BB1 | 23 | 54 | 77 |
| BB2 | 23 | 54 | 77 |
| **TOTAL** | **750** | **1155** | **1905** |
