# PARITY-STATUS — rendered configs vs the lab's startup-configs (auto-generated)

> Generated 2026-08-25 by `avd/scripts/parity_report.py`.
> Content-set comparison (ordering never compared). Exempt as cosmetic:
> comments, descriptions, BGP neighbor descriptions, explicit `no shutdown`.

## Scoreboard

| Metric | Lines |
|---|---|
| **Residual total (non-exempt)** | **801** |
| MISSING — in the target, not rendered | 137 |
| EXTRA — rendered, not in the target | 664 |

## Exempt lines absorbed today

| Exemption | Lines |
|---|---|
| BGP neighbor descriptions | 442 |
| comment lines | 54 |
| explicit `no shutdown` (AVD default) | 474 |
| interface/host descriptions | 676 |

## Remaining differences

### MISSING — top exact lines (34 distinct)

| count | line |
|---|---|
| 30× | `no switchport` |
| 20× | `isis circuit-type level-2` |
| 8× | `neighbor LOCAL-EVPN-PEERS remote-as 65100` |
| 8× | `neighbor LOCAL-IPV4-PEERS remote-as 65100` |
| 8× | `address-family ipv4` |
| 4× | `neighbor 192.0.0.1 activate` |
| 4× | `neighbor 192.0.0.0 activate` |
| 4× | `switchport` |
| 4× | `neighbor REMOTE-EVPN-PEERS remote-as 65000` |
| 4× | `route-target import export evpn domain all 10010:10010` |
| 4× | `route-target import export evpn domain all 10070:10070` |
| 3× | `ip address 169.254.0.1/30` |
| 3× | `peer-address 169.254.0.2` |
| 3× | `ip address 169.254.0.2/30` |
| 3× | `peer-address 169.254.0.1` |
| 2× | `vxlan vlan 10,30 vni 10010,10030` |
| 2× | `vxlan vlan 10,30,50 vni 10010,10030,10050` |
| 2× | `vxlan vlan 10,50,70 vni 10010,10050,10070` |
| 2× | `vxlan vlan 20,40 vni 10020,10040` |
| 2× | `vxlan vlan 40,80 vni 10040,10080` |
| 2× | `vxlan vlan 10,60,70 vni 10010,10060,10070` |
| 2× | `aggregate-address 10.0.2.0/24` |
| 2× | `aggregate-address 10.1.2.0/24` |
| 1× | `rd evpn domain all 10.0.1.7:10010` |
| 1× | `rd evpn domain all 10.0.1.7:10070` |

### MISSING — top shapes (digits→`#`)

| count | line |
|---|---|
| 30× | `no switchport` |
| 20× | `isis circuit-type level-#` |
| 8× | `vxlan vlan #,# vni #,#` |
| 8× | `neighbor LOCAL-EVPN-PEERS remote-as #` |
| 8× | `neighbor LOCAL-IPV#-PEERS remote-as #` |
| 8× | `address-family ipv#` |
| 8× | `neighbor #.#.#.# activate` |
| 8× | `rd evpn domain all #.#.#.#:#` |
| 8× | `route-target import export evpn domain all #:#` |
| 6× | `ip address #.#.#.#/#` |
| 6× | `peer-address #.#.#.#` |
| 6× | `vxlan vlan #,#,# vni #,#,#` |
| 4× | `switchport` |
| 4× | `neighbor REMOTE-EVPN-PEERS remote-as #` |
| 4× | `aggregate-address #.#.#.#/#` |

### EXTRA — top exact lines (147 distinct)

| count | line |
|---|---|
| 64× | `isis metric 50` |
| 27× | `no enable password` |
| 27× | `protocol https` |
| 26× | `switchport mode access` |
| 25× | `transceiver qsfp default-mode 4x10G` |
| 24× | `neighbor LOCAL-EVPN-PEERS send-community` |
| 24× | `neighbor LOCAL-EVPN-PEERS maximum-routes 0` |
| 18× | `evpn multicast` |
| 18× | `router multicast` |
| 12× | `router bfd` |
| 12× | `multihop interval 300 min-rx 300 multiplier 3` |
| 12× | `neighbor LOCAL-IPV4-PEERS send-community` |
| 12× | `neighbor LOCAL-IPV4-PEERS maximum-routes 256000` |
| 12× | `maximum-paths 4` |
| 10× | `vrf PROD` |
| 10× | `vxlan vlan 10 vni 10010` |
| 10× | `address-family evpn` |
| 10× | `vlan internal order ascending range 1006 1199` |
| 9× | `spanning-tree mst 0 priority 32768` |
| 8× | `neighbor 10.0.1.201 remote-as 65100` |
| 8× | `neighbor 10.0.1.202 remote-as 65100` |
| 8× | `neighbor 10.0.1.203 remote-as 65100` |
| 8× | `neighbor 10.0.1.204 remote-as 65100` |
| 8× | `vrf DEV` |
| 8× | `spanning-tree mode mstp` |
| 8× | `route-map RM-EVPN-SOO-IN deny 10` |
| 8× | `match extcommunity ECL-EVPN-SOO` |
| 8× | `route-map RM-EVPN-SOO-IN permit 20` |
| 8× | `route-map RM-EVPN-SOO-OUT permit 10` |
| 8× | `neighbor LOCAL-EVPN-PEERS route-map RM-EVPN-SOO-IN in` |
| 8× | `neighbor LOCAL-EVPN-PEERS route-map RM-EVPN-SOO-OUT out` |
| 6× | `neighbor MLAG-IPV4-PEER send-community` |
| 6× | `neighbor MLAG-IPV4-PEER maximum-routes 256000` |
| 6× | `seq 30 permit 10.2.0.0/16 eq 32` |
| 5× | `vxlan vlan 70 vni 10070` |
| 4× | `vxlan vlan 30 vni 10030` |
| 4× | `vxlan vlan 50 vni 10050` |
| 4× | `neighbor REMOTE-EVPN-PEERS send-community` |
| 4× | `neighbor REMOTE-EVPN-PEERS maximum-routes 0` |
| 4× | `neighbor 10.0.0.1 remote-as 65000` |

### EXTRA — top shapes (digits→`#`)

| count | line |
|---|---|
| 72× | `neighbor #.#.#.# remote-as #` |
| 64× | `isis metric #` |
| 34× | `vxlan vlan # vni #` |
| 27× | `no enable password` |
| 27× | `protocol https` |
| 26× | `switchport mode access` |
| 26× | `router-id #.#.#.#` |
| 25× | `transceiver qsfp default-mode #x#G` |
| 24× | `neighbor LOCAL-EVPN-PEERS send-community` |
| 24× | `neighbor LOCAL-EVPN-PEERS maximum-routes #` |
| 18× | `evpn multicast` |
| 18× | `router multicast` |
| 12× | `router bfd` |
| 12× | `multihop interval # min-rx # multiplier #` |
| 12× | `neighbor LOCAL-IPV#-PEERS send-community` |
| 12× | `neighbor LOCAL-IPV#-PEERS maximum-routes #` |
| 12× | `maximum-paths #` |
| 10× | `vrf PROD` |
| 10× | `ip address virtual source-nat vrf PROD address #.#.#.#` |
| 10× | `address-family evpn` |

## Per-node residual

| Node | missing | extra |
|---|---|---|
| A-LEAF1 | 11 | 30 |
| A-LEAF2 | 11 | 30 |
| A-LEAF3 | 12 | 36 |
| A-LEAF4 | 12 | 36 |
| A-LEAF5 | 10 | 28 |
| A-LEAF6 | 10 | 28 |
| A-LEAF7 | 9 | 36 |
| A-LEAF8 | 9 | 36 |
| A-SPINE1 | 0 | 12 |
| A-SPINE2 | 0 | 12 |
| A-SPINE3 | 0 | 12 |
| A-SPINE4 | 0 | 12 |
| B-LEAF1 | 5 | 29 |
| B-LEAF2 | 5 | 29 |
| B-LEAF3 | 4 | 34 |
| B-LEAF4 | 4 | 34 |
| B-LEAF5 | 4 | 32 |
| B-LEAF6 | 4 | 32 |
| B-LEAF7 | 11 | 41 |
| B-LEAF8 | 11 | 41 |
| B-SPINE1 | 1 | 17 |
| B-SPINE2 | 1 | 17 |
| B-SPINE3 | 1 | 17 |
| B-SPINE4 | 1 | 17 |
| B-SW1 | 1 | 6 |
| BB1 | 0 | 5 |
| BB2 | 0 | 5 |
| **TOTAL** | **137** | **664** |
