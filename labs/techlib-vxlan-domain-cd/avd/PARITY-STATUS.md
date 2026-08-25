# PARITY-STATUS — rendered configs vs the lab's startup-configs (auto-generated)

> Generated 2026-08-25 by `avd/scripts/parity_report.py`.
> Content-set comparison (ordering never compared). Exempt as cosmetic:
> comments, descriptions, BGP neighbor descriptions, explicit `no shutdown`.

## Scoreboard

| Metric | Lines |
|---|---|
| **Residual total (non-exempt)** | **546** |
| MISSING — in the target, not rendered | 156 |
| EXTRA — rendered, not in the target | 390 |

## Exempt lines absorbed today

| Exemption | Lines |
|---|---|
| BGP neighbor descriptions | 294 |
| comment lines | 54 |
| explicit `no shutdown` (AVD default) | 348 |
| interface/host descriptions | 670 |

## Remaining differences

### MISSING — top exact lines (34 distinct)

| count | line |
|---|---|
| 26× | `no switchport` |
| 12× | `neighbor interface Ethernet1 peer-group LOCAL-IPV6-PEERS` |
| 12× | `neighbor interface Ethernet2 peer-group LOCAL-IPV6-PEERS` |
| 12× | `neighbor interface Ethernet3 peer-group LOCAL-IPV6-PEERS` |
| 12× | `neighbor interface Ethernet4 peer-group LOCAL-IPV6-PEERS` |
| 8× | `neighbor LOCAL-EVPN-PEERS remote-as 65300` |
| 8× | `switchport` |
| 6× | `neighbor interface Vlan4093 peer-group MLAG-IPV6-PEER` |
| 4× | `neighbor REMOTE-EVPN-MPLS-PEERS remote-as 65000` |
| 4× | `route-target import evpn domain all 10010:10010` |
| 4× | `route-target export evpn domain all 10010:10010` |
| 4× | `route-target import evpn domain all 10070:10070` |
| 4× | `route-target export evpn domain all 10070:10070` |
| 4× | `neighbor interface Ethernet5 peer-group LOCAL-IPV6-PEERS` |
| 4× | `neighbor interface Ethernet6 peer-group LOCAL-IPV6-PEERS` |
| 4× | `neighbor interface Ethernet7 peer-group LOCAL-IPV6-PEERS` |
| 4× | `neighbor interface Ethernet8 peer-group LOCAL-IPV6-PEERS` |
| 2× | `vxlan vlan 10,30 vni 10010,10030` |
| 2× | `vxlan vlan 10,30,50 vni 10010,10030,10050` |
| 2× | `vxlan vlan 50,70 vni 10050,10070` |
| 2× | `vxlan vlan 10,50,70 vni 10010,10050,10070` |
| 2× | `vxlan vlan 20,40 vni 10020,10040` |
| 2× | `vxlan vlan 40,80 vni 10040,10080` |
| 2× | `vxlan vlan 10,60,70 vni 10010,10060,10070` |
| 1× | `rd evpn domain all 10.0.3.7:10010` |

### MISSING — top shapes (digits→`#`)

| count | line |
|---|---|
| 64× | `neighbor interface Ethernet# peer-group LOCAL-IPV#-PEERS` |
| 26× | `no switchport` |
| 10× | `vxlan vlan #,# vni #,#` |
| 8× | `neighbor LOCAL-EVPN-PEERS remote-as #` |
| 8× | `switchport` |
| 8× | `rd evpn domain all #.#.#.#:#` |
| 8× | `route-target import evpn domain all #:#` |
| 8× | `route-target export evpn domain all #:#` |
| 6× | `neighbor interface Vlan# peer-group MLAG-IPV#-PEER` |
| 6× | `vxlan vlan #,#,# vni #,#,#` |
| 4× | `neighbor REMOTE-EVPN-MPLS-PEERS remote-as #` |

### EXTRA — top exact lines (73 distinct)

| count | line |
|---|---|
| 27× | `no enable password` |
| 27× | `protocol https` |
| 26× | `switchport mode access` |
| 25× | `transceiver qsfp default-mode 4x10G` |
| 24× | `neighbor LOCAL-EVPN-PEERS send-community` |
| 12× | `neighbor interface Ethernet1 peer-group LOCAL-IPV6-PEERS remote-as 65400` |
| 12× | `neighbor interface Ethernet2 peer-group LOCAL-IPV6-PEERS remote-as 65400` |
| 12× | `neighbor interface Ethernet3 peer-group LOCAL-IPV6-PEERS remote-as 65400` |
| 12× | `neighbor interface Ethernet4 peer-group LOCAL-IPV6-PEERS remote-as 65400` |
| 10× | `vxlan vlan 10 vni 10010` |
| 10× | `address-family evpn` |
| 9× | `spanning-tree mst 0 priority 32768` |
| 8× | `neighbor 2001:db8:c0::201 remote-as 65300` |
| 8× | `neighbor 2001:db8:c0::202 remote-as 65300` |
| 8× | `neighbor 2001:db8:c0::203 remote-as 65300` |
| 8× | `neighbor 2001:db8:c0::204 remote-as 65300` |
| 8× | `evpn multicast` |
| 8× | `spanning-tree mode mstp` |
| 7× | `vxlan vlan 70 vni 10070` |
| 6× | `ipv6 nd ra interval 5` |
| 6× | `neighbor MLAG-IPV6-PEER send-community` |
| 6× | `vxlan vlan 50 vni 10050` |
| 4× | `vxlan vlan 30 vni 10030` |
| 4× | `neighbor REMOTE-EVPN-MPLS-PEERS send-community` |
| 4× | `neighbor 2001:db8:bb::1 remote-as 65000` |
| 4× | `neighbor 2001:db8:bb::2 remote-as 65000` |
| 4× | `route-target both 10010:10010` |
| 4× | `route-target import export evpn domain remote 10010:10010` |
| 4× | `route-target both 10070:10070` |
| 4× | `route-target import export evpn domain remote 10070:10070` |
| 4× | `evpn ethernet-segment domain local` |
| 4× | `evpn ethernet-segment domain remote` |
| 4× | `vxlan vlan 40 vni 10040` |
| 4× | `neighbor interface Ethernet5 peer-group LOCAL-IPV6-PEERS remote-as 65400` |
| 4× | `neighbor interface Ethernet6 peer-group LOCAL-IPV6-PEERS remote-as 65400` |
| 4× | `neighbor interface Ethernet7 peer-group LOCAL-IPV6-PEERS remote-as 65400` |
| 4× | `neighbor interface Ethernet8 peer-group LOCAL-IPV6-PEERS remote-as 65400` |
| 3× | `vxlan vlan 60 vni 10060` |
| 2× | `vlan internal order ascending range 1006 1199` |
| 2× | `neighbor interface Vlan4093 peer-group MLAG-IPV6-PEER remote-as 65301` |

### EXTRA — top shapes (digits→`#`)

| count | line |
|---|---|
| 64× | `neighbor interface Ethernet# peer-group LOCAL-IPV#-PEERS remote-as #` |
| 38× | `vxlan vlan # vni #` |
| 32× | `neighbor #:db#:c#::# remote-as #` |
| 27× | `no enable password` |
| 27× | `protocol https` |
| 26× | `switchport mode access` |
| 25× | `transceiver qsfp default-mode #x#G` |
| 24× | `neighbor LOCAL-EVPN-PEERS send-community` |
| 18× | `router-id #.#.#.#` |
| 10× | `address-family evpn` |
| 9× | `spanning-tree mst # priority #` |
| 8× | `evpn multicast` |
| 8× | `neighbor #:db#:bb::# remote-as #` |
| 8× | `rd #.#.#.#:#` |
| 8× | `rd evpn domain remote #.#.#.#:#` |
| 8× | `route-target both #:#` |
| 8× | `route-target import export evpn domain remote #:#` |
| 8× | `spanning-tree mode mstp` |
| 6× | `ipv# nd ra interval #` |
| 6× | `neighbor MLAG-IPV#-PEER send-community` |

## Per-node residual

| Node | missing | extra |
|---|---|---|
| BB1 | 0 | 3 |
| BB2 | 0 | 3 |
| C-LEAF1 | 7 | 17 |
| C-LEAF2 | 7 | 17 |
| C-LEAF3 | 6 | 20 |
| C-LEAF4 | 6 | 20 |
| C-LEAF5 | 7 | 17 |
| C-LEAF6 | 7 | 17 |
| C-LEAF7 | 10 | 27 |
| C-LEAF8 | 10 | 27 |
| C-SPINE1 | 0 | 5 |
| C-SPINE2 | 0 | 5 |
| C-SPINE3 | 0 | 5 |
| C-SPINE4 | 0 | 5 |
| D-LEAF1 | 7 | 15 |
| D-LEAF2 | 7 | 15 |
| D-LEAF3 | 6 | 16 |
| D-LEAF4 | 6 | 16 |
| D-LEAF5 | 6 | 14 |
| D-LEAF6 | 6 | 14 |
| D-LEAF7 | 13 | 27 |
| D-LEAF8 | 13 | 27 |
| D-SPINE1 | 8 | 13 |
| D-SPINE2 | 8 | 13 |
| D-SPINE3 | 8 | 13 |
| D-SPINE4 | 8 | 13 |
| D-SW1 | 0 | 6 |
| **TOTAL** | **156** | **390** |
