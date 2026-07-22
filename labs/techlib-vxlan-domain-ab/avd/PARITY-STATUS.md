# PARITY-STATUS — running tally (auto-generated)

> Generated 2026-07-22 by `avd/scripts/parity_report.py`.
> Contract: **content-set parity** (line ordering exempt) — see
> `PARITY-LEDGER.md` for the class taxonomy and capability verdicts.

## Scoreboard

| Metric | Lines |
|---|---|
| **Residual total (non-exempt)** | **2429** |
| MISSING — in the guide, not yet rendered | 956 |
| EXTRA — rendered, not in the guide | 1473 |
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

### MISSING — top exact lines (238 distinct)

| count | line |
|---|---|
| 84× | `isis enable 100` |
| 64× | `ip address unnumbered Loopback0` |
| 32× | `no switchport` |
| 32× | `pim ipv4 local-interface Loopback0` |
| 26× | `mld` |
| 26× | `neighbor default send-community` |
| 20× | `trunk group MLAG_PEER` |
| 20× | `routing` |
| 20× | `isis circuit-type level-2` |
| 18× | `address-family ipv4` |
| 18× | `address-family ipv6` |
| 18× | `ipv6` |
| 17× | `spanning-tree edge-port bpduguard default` |
| 16× | `pim ipv4 sparse-mode` |
| 14× | `ip igmp` |

### MISSING — top shapes (digits→`#`)

| count | line |
|---|---|
| 84× | `isis enable #` |
| 64× | `ip address unnumbered Loopback#` |
| 36× | `address-family ipv#` |
| 34× | `pim ipv# local-interface Loopback#` |
| 32× | `no switchport` |
| 32× | `neighbor #.#.#.# description A-SPINE#.IPV#` |
| 32× | `neighbor #.#.#.# description A-LEAF#.IPV#` |
| 30× | `seq # permit #.#.#.#/# eq #` |
| 26× | `mld` |
| 26× | `neighbor default send-community` |

### EXTRA — top exact lines (492 distinct)

| count | line |
|---|---|
| 84× | `isis enable EVPN_UNDERLAY` |
| 64× | `isis metric 50` |
| 38× | `ipv6 enable` |
| 28× | `trunk group MLAG` |
| 26× | `switchport mode access` |
| 24× | `neighbor LOCAL-EVPN-PEERS password 7 WzKnNSduqwPYvUePYIh40g==` |
| 24× | `neighbor LOCAL-EVPN-PEERS send-community` |
| 24× | `neighbor LOCAL-EVPN-PEERS maximum-routes 0` |
| 24× | `no neighbor LOCAL-EVPN-PEERS activate` |
| 16× | `mtu 9114` |
| 14× | `spanning-tree bpduguard enable` |
| 12× | `ip prefix-list PL-LOOPBACKS-EVPN-OVERLAY` |
| 12× | `seq 10 permit 10.0.1.0/24 eq 32` |
| 12× | `match ip address prefix-list PL-LOOPBACKS-EVPN-OVERLAY` |
| 12× | `router bfd` |

### EXTRA — top shapes (digits→`#`)

| count | line |
|---|---|
| 90× | `ip address #.#.#.#/#` |
| 84× | `isis enable EVPN_UNDERLAY` |
| 80× | `neighbor #.#.#.# remote-as #` |
| 64× | `isis metric #` |
| 38× | `ipv# enable` |
| 34× | `vxlan vlan # vni #` |
| 32× | `neighbor #.#.#.# description A-SPINE#_Ethernet#` |
| 32× | `neighbor #.#.#.# description A-LEAF#_Ethernet#` |
| 28× | `trunk group MLAG` |
| 26× | `switchport mode access` |

## Per-node residual

| Node | missing | extra | total |
|---|---|---|---|
| A-LEAF1 | 47 | 59 | 106 |
| A-LEAF2 | 48 | 60 | 108 |
| A-LEAF3 | 58 | 67 | 125 |
| A-LEAF4 | 59 | 68 | 127 |
| A-LEAF5 | 50 | 58 | 108 |
| A-LEAF6 | 54 | 56 | 110 |
| A-LEAF7 | 23 | 143 | 166 |
| A-LEAF8 | 24 | 144 | 168 |
| A-SPINE1 | 15 | 21 | 36 |
| A-SPINE2 | 15 | 21 | 36 |
| A-SPINE3 | 15 | 21 | 36 |
| A-SPINE4 | 15 | 21 | 36 |
| B-LEAF1 | 38 | 46 | 84 |
| B-LEAF2 | 38 | 46 | 84 |
| B-LEAF3 | 67 | 60 | 127 |
| B-LEAF4 | 67 | 60 | 127 |
| B-LEAF5 | 41 | 41 | 82 |
| B-LEAF6 | 41 | 41 | 82 |
| B-LEAF7 | 32 | 86 | 118 |
| B-LEAF8 | 32 | 86 | 118 |
| B-SPINE1 | 31 | 35 | 66 |
| B-SPINE2 | 31 | 35 | 66 |
| B-SPINE3 | 31 | 35 | 66 |
| B-SPINE4 | 31 | 35 | 66 |
| B-SW1 | 7 | 20 | 27 |
| BB1 | 23 | 54 | 77 |
| BB2 | 23 | 54 | 77 |
| **TOTAL** | **956** | **1473** | **2429** |
