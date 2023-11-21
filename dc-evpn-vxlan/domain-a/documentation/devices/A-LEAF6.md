# A-LEAF6

## Table of Contents

- [Management](#management)
  - [Management Interfaces](#management-interfaces)
  - [IP Name Servers](#ip-name-servers)
  - [NTP](#ntp)
  - [Management API HTTP](#management-api-http)
- [Authentication](#authentication)
  - [Local Users](#local-users)
  - [AAA Authorization](#aaa-authorization)
- [DHCP Relay](#dhcp-relay)
  - [DHCP Relay Summary](#dhcp-relay-summary)
  - [DHCP Relay Configuration](#dhcp-relay-configuration)
- [Monitoring](#monitoring)
  - [TerminAttr Daemon](#terminattr-daemon)
- [MLAG](#mlag)
  - [MLAG Summary](#mlag-summary)
  - [MLAG Device Configuration](#mlag-device-configuration)
- [Spanning Tree](#spanning-tree)
  - [Spanning Tree Summary](#spanning-tree-summary)
  - [Spanning Tree Device Configuration](#spanning-tree-device-configuration)
- [Internal VLAN Allocation Policy](#internal-vlan-allocation-policy)
  - [Internal VLAN Allocation Policy Summary](#internal-vlan-allocation-policy-summary)
  - [Internal VLAN Allocation Policy Configuration](#internal-vlan-allocation-policy-configuration)
- [VLANs](#vlans)
  - [VLANs Summary](#vlans-summary)
  - [VLANs Device Configuration](#vlans-device-configuration)
- [MAC Address Table](#mac-address-table)
  - [MAC Address Table Summary](#mac-address-table-summary)
  - [MAC Address Table Device Configuration](#mac-address-table-device-configuration)
- [Interfaces](#interfaces)
  - [Ethernet Interfaces](#ethernet-interfaces)
  - [Port-Channel Interfaces](#port-channel-interfaces)
  - [Loopback Interfaces](#loopback-interfaces)
  - [VLAN Interfaces](#vlan-interfaces)
  - [VXLAN Interface](#vxlan-interface)
- [Routing](#routing)
  - [Service Routing Protocols Model](#service-routing-protocols-model)
  - [Virtual Router MAC Address](#virtual-router-mac-address)
  - [IP Routing](#ip-routing)
  - [IPv6 Routing](#ipv6-routing)
  - [ARP](#arp)
  - [Router BGP](#router-bgp)
- [BFD](#bfd)
  - [Router BFD](#router-bfd)
- [Multicast](#multicast)
  - [IP IGMP Snooping](#ip-igmp-snooping)
  - [Router Multicast](#router-multicast)
  - [PIM Sparse Mode](#pim-sparse-mode)
- [Filters](#filters)
  - [Prefix-lists](#prefix-lists)
  - [Route-maps](#route-maps)
- [VRF Instances](#vrf-instances)
  - [VRF Instances Summary](#vrf-instances-summary)
  - [VRF Instances Device Configuration](#vrf-instances-device-configuration)
- [Virtual Source NAT](#virtual-source-nat)
  - [Virtual Source NAT Summary](#virtual-source-nat-summary)
  - [Virtual Source NAT Configuration](#virtual-source-nat-configuration)
- [EOS CLI](#eos-cli)

## Management

### Management Interfaces

#### Management Interfaces Summary

##### IPv4

| Management Interface | description | Type | VRF | IP Address | Gateway |
| -------------------- | ----------- | ---- | --- | ---------- | ------- |
| Management1 | oob_management | oob | MGMT | 192.168.0.106/24 | - |

##### IPv6

| Management Interface | description | Type | VRF | IPv6 Address | IPv6 Gateway |
| -------------------- | ----------- | ---- | --- | ------------ | ------------ |
| Management1 | oob_management | oob | MGMT | - | - |

#### Management Interfaces Device Configuration

```eos
!
interface Management1
   description oob_management
   no shutdown
   vrf MGMT
   ip address 192.168.0.106/24
```

### IP Name Servers

#### IP Name Servers Summary

| Name Server | VRF | Priority |
| ----------- | --- | -------- |
| 10.255.0.2 | MGMT | - |

#### IP Name Servers Device Configuration

```eos
ip name-server vrf MGMT 10.255.0.2
```

### NTP

#### NTP Summary

##### NTP Servers

| Server | VRF | Preferred | Burst | iBurst | Version | Min Poll | Max Poll | Local-interface | Key |
| ------ | --- | --------- | ----- | ------ | ------- | -------- | -------- | --------------- | --- |
| 0.pool.ntp.org | - | - | - | - | - | - | - | - | - |

#### NTP Device Configuration

```eos
!
ntp server 0.pool.ntp.org
```

### Management API HTTP

#### Management API HTTP Summary

| HTTP | HTTPS | Default Services |
| ---- | ----- | ---------------- |
| False | True | - |

#### Management API VRF Access

| VRF Name | IPv4 ACL | IPv6 ACL |
| -------- | -------- | -------- |
| MGMT | - | - |

#### Management API HTTP Configuration

```eos
!
management api http-commands
   protocol https
   no shutdown
   !
   vrf MGMT
      no shutdown
```

## Authentication

### Local Users

#### Local Users Summary

| User | Privilege | Role | Disabled | Shell |
| ---- | --------- | ---- | -------- | ----- |
| admin | 15 | network-admin | False | - |
| cvpadmin | 15 | network-admin | False | - |

#### Local Users Device Configuration

```eos
!
username admin privilege 15 role network-admin nopassword
username cvpadmin privilege 15 role network-admin secret sha512 <removed>
```

### AAA Authorization

#### AAA Authorization Summary

| Type | User Stores |
| ---- | ----------- |
| Exec | local |

Authorization for configuration commands is disabled.

#### AAA Authorization Device Configuration

```eos
aaa authorization exec default local
!
```

## DHCP Relay

### DHCP Relay Summary

- DHCP Relay is disabled for tunnelled requests

### DHCP Relay Configuration

```eos
!
dhcp relay
   tunnel requests disabled
```

## Monitoring

### TerminAttr Daemon

#### TerminAttr Daemon Summary

| CV Compression | CloudVision Servers | VRF | Authentication | Smash Excludes | Ingest Exclude | Bypass AAA |
| -------------- | ------------------- | --- | -------------- | -------------- | -------------- | ---------- |
| gzip | 192.168.0.5:9910 | MGMT | token,/tmp/token | ale,flexCounter,hardware,kni,pulse,strata | /Sysdb/cell/1/agent,/Sysdb/cell/2/agent | False |

#### TerminAttr Daemon Device Configuration

```eos
!
daemon TerminAttr
   exec /usr/bin/TerminAttr -cvaddr=192.168.0.5:9910 -cvauth=token,/tmp/token -cvvrf=MGMT -smashexcludes=ale,flexCounter,hardware,kni,pulse,strata -ingestexclude=/Sysdb/cell/1/agent,/Sysdb/cell/2/agent -taillogs
   no shutdown
```

## MLAG

### MLAG Summary

| Domain-id | Local-interface | Peer-address | Peer-link |
| --------- | --------------- | ------------ | --------- |
| 100 | Vlan4094 | 169.254.0.0 | Port-Channel1000 |

Dual primary detection is disabled.

### MLAG Device Configuration

```eos
!
mlag configuration
   domain-id 100
   local-interface Vlan4094
   peer-address 169.254.0.0
   peer-link Port-Channel1000
   reload-delay mlag 300
   reload-delay non-mlag 330
```

## Spanning Tree

### Spanning Tree Summary

STP mode: **mstp**

#### MSTP Instance and Priority

| Instance(s) | Priority |
| -------- | -------- |
| 0 | 0 |

#### Global Spanning-Tree Settings

- Spanning Tree disabled for VLANs: **4093-4094**

### Spanning Tree Device Configuration

```eos
!
spanning-tree mode mstp
no spanning-tree vlan-id 4093-4094
spanning-tree mst 0 priority 0
```

## Internal VLAN Allocation Policy

### Internal VLAN Allocation Policy Summary

| Policy Allocation | Range Beginning | Range Ending |
| ------------------| --------------- | ------------ |
| ascending | 1006 | 1199 |

### Internal VLAN Allocation Policy Configuration

```eos
!
vlan internal order ascending range 1006 1199
```

## VLANs

### VLANs Summary

| VLAN ID | Name | Trunk Groups |
| ------- | ---- | ------------ |
| 70 | Brown | - |
| 3002 | MLAG_iBGP_Dev | LEAF_PEER_L3 |
| 4093 | LEAF_PEER_L3 | LEAF_PEER_L3 |
| 4094 | MLAG_PEER | MLAG |

### VLANs Device Configuration

```eos
!
vlan 70
   name Brown
!
vlan 3002
   name MLAG_iBGP_Dev
   trunk group LEAF_PEER_L3
!
vlan 4093
   name LEAF_PEER_L3
   trunk group LEAF_PEER_L3
!
vlan 4094
   name MLAG_PEER
   trunk group MLAG
```

## MAC Address Table

### MAC Address Table Summary

- MAC address table entry maximum age: 1800 seconds

### MAC Address Table Device Configuration

```eos
!
mac address-table aging-time 1800
```

## Interfaces

### Ethernet Interfaces

#### Ethernet Interfaces Summary

##### L2

| Interface | Description | Mode | VLANs | Native VLAN | Trunk Group | Channel-Group |
| --------- | ----------- | ---- | ----- | ----------- | ----------- | ------------- |
| Ethernet5 | MLAG_PEER_A-LEAF5_Ethernet5 | *trunk | *- | *- | *['LEAF_PEER_L3', 'MLAG'] | 1000 |
| Ethernet6 | MLAG_PEER_A-LEAF5_Ethernet6 | *trunk | *- | *- | *['LEAF_PEER_L3', 'MLAG'] | 1000 |
| Ethernet7 | HostF_Ethernet2 | *access | *70 | *- | *- | 7 |

*Inherited from Port-Channel Interface

##### IPv4

| Interface | Description | Type | Channel Group | IP Address | VRF |  MTU | Shutdown | ACL In | ACL Out |
| --------- | ----------- | -----| ------------- | ---------- | ----| ---- | -------- | ------ | ------- |
| Ethernet1 | P2P_LINK_TO_A-SPINE1_Ethernet6 | routed | - | 192.168.1.41/31 | default | 9214 | False | - | - |
| Ethernet2 | P2P_LINK_TO_A-SPINE2_Ethernet6 | routed | - | 192.168.1.43/31 | default | 9214 | False | - | - |
| Ethernet3 | P2P_LINK_TO_A-SPINE3_Ethernet6 | routed | - | 192.168.1.45/31 | default | 9214 | False | - | - |
| Ethernet4 | P2P_LINK_TO_A-SPINE4_Ethernet6 | routed | - | 192.168.1.47/31 | default | 9214 | False | - | - |

#### Ethernet Interfaces Device Configuration

```eos
!
interface Ethernet1
   description P2P_LINK_TO_A-SPINE1_Ethernet6
   no shutdown
   mtu 9214
   no switchport
   ip address 192.168.1.41/31
   pim ipv4 sparse-mode
!
interface Ethernet2
   description P2P_LINK_TO_A-SPINE2_Ethernet6
   no shutdown
   mtu 9214
   no switchport
   ip address 192.168.1.43/31
   pim ipv4 sparse-mode
!
interface Ethernet3
   description P2P_LINK_TO_A-SPINE3_Ethernet6
   no shutdown
   mtu 9214
   no switchport
   ip address 192.168.1.45/31
   pim ipv4 sparse-mode
!
interface Ethernet4
   description P2P_LINK_TO_A-SPINE4_Ethernet6
   no shutdown
   mtu 9214
   no switchport
   ip address 192.168.1.47/31
   pim ipv4 sparse-mode
!
interface Ethernet5
   description MLAG_PEER_A-LEAF5_Ethernet5
   no shutdown
   channel-group 1000 mode active
!
interface Ethernet6
   description MLAG_PEER_A-LEAF5_Ethernet6
   no shutdown
   channel-group 1000 mode active
!
interface Ethernet7
   description HostF_Ethernet2
   no shutdown
   channel-group 7 mode active
```

### Port-Channel Interfaces

#### Port-Channel Interfaces Summary

##### L2

| Interface | Description | Type | Mode | VLANs | Native VLAN | Trunk Group | LACP Fallback Timeout | LACP Fallback Mode | MLAG ID | EVPN ESI |
| --------- | ----------- | ---- | ---- | ----- | ----------- | ------------| --------------------- | ------------------ | ------- | -------- |
| Port-Channel7 | HostF_HostF | switched | access | 70 | - | - | - | - | 7 | - |
| Port-Channel1000 | MLAG_PEER_A-LEAF5_Po1000 | switched | trunk | - | - | ['LEAF_PEER_L3', 'MLAG'] | - | - | - | - |

#### Port-Channel Interfaces Device Configuration

```eos
!
interface Port-Channel7
   description HostF_HostF
   no shutdown
   switchport
   switchport access vlan 70
   mlag 7
   spanning-tree portfast
!
interface Port-Channel1000
   description MLAG_PEER_A-LEAF5_Po1000
   no shutdown
   switchport
   switchport mode trunk
   switchport trunk group LEAF_PEER_L3
   switchport trunk group MLAG
```

### Loopback Interfaces

#### Loopback Interfaces Summary

##### IPv4

| Interface | Description | VRF | IP Address |
| --------- | ----------- | --- | ---------- |
| Loopback0 | EVPN_Overlay_Peering | default | 10.0.0.10/32 |
| Loopback1 | VTEP_VXLAN_Tunnel_Source | default | 10.1.1.9/32 |
| Loopback102 | Dev_VTEP_DIAGNOSTICS | Dev | 10.102.102.10/32 |

##### IPv6

| Interface | Description | VRF | IPv6 Address |
| --------- | ----------- | --- | ------------ |
| Loopback0 | EVPN_Overlay_Peering | default | - |
| Loopback1 | VTEP_VXLAN_Tunnel_Source | default | - |
| Loopback102 | Dev_VTEP_DIAGNOSTICS | Dev | - |


#### Loopback Interfaces Device Configuration

```eos
!
interface Loopback0
   description EVPN_Overlay_Peering
   no shutdown
   ip address 10.0.0.10/32
!
interface Loopback1
   description VTEP_VXLAN_Tunnel_Source
   no shutdown
   ip address 10.1.1.9/32
!
interface Loopback102
   description Dev_VTEP_DIAGNOSTICS
   no shutdown
   vrf Dev
   ip address 10.102.102.10/32
```

### VLAN Interfaces

#### VLAN Interfaces Summary

| Interface | Description | VRF |  MTU | Shutdown |
| --------- | ----------- | --- | ---- | -------- |
| Vlan70 | Brown | Dev | 9014 | False |
| Vlan3002 | MLAG_PEER_L3_iBGP: vrf Dev | Dev | 9214 | False |
| Vlan4093 | MLAG_PEER_L3_PEERING | default | 9214 | False |
| Vlan4094 | MLAG_PEER | default | 1500 | False |

##### IPv4

| Interface | VRF | IP Address | IP Address Virtual | IP Router Virtual Address | VRRP | ACL In | ACL Out |
| --------- | --- | ---------- | ------------------ | ------------------------- | ---- | ------ | ------- |
| Vlan70 |  Dev  |  -  |  10.70.70.1/24  |  -  |  -  |  -  |  -  |
| Vlan3002 |  Dev  |  192.0.0.1/31  |  -  |  -  |  -  |  -  |  -  |
| Vlan4093 |  default  |  192.0.0.1/31  |  -  |  -  |  -  |  -  |  -  |
| Vlan4094 |  default  |  169.254.0.1/31  |  -  |  -  |  -  |  -  |  -  |

#### VLAN Interfaces Device Configuration

```eos
!
interface Vlan70
   description Brown
   no shutdown
   mtu 9014
   vrf Dev
   ip address virtual 10.70.70.1/24
!
interface Vlan3002
   description MLAG_PEER_L3_iBGP: vrf Dev
   no shutdown
   mtu 9214
   vrf Dev
   ip address 192.0.0.1/31
!
interface Vlan4093
   description MLAG_PEER_L3_PEERING
   no shutdown
   mtu 9214
   ip address 192.0.0.1/31
   pim ipv4 sparse-mode
!
interface Vlan4094
   description MLAG_PEER
   no shutdown
   mtu 1500
   no autostate
   ip address 169.254.0.1/31
```

### VXLAN Interface

#### VXLAN Interface Summary

| Setting | Value |
| ------- | ----- |
| Source Interface | Loopback0 |
| MLAG Source Interface | Loopback1 |
| UDP port | 4789 |
| EVPN MLAG Shared Router MAC | mlag-system-id |

##### VLAN to VNI, Flood List and Multicast Group Mappings

| VLAN | VNI | Flood List | Multicast Group |
| ---- | --- | ---------- | --------------- |
| 70 | 10070 | - | - |

##### VRF to VNI and Multicast Group Mappings

| VRF | VNI | Multicast Group |
| ---- | --- | --------------- |
| Dev | 50002 | - |

#### VXLAN Interface Device Configuration

```eos
!
interface Vxlan1
   description A-LEAF6_VTEP
   vxlan source-interface Loopback0
   vxlan virtual-router encapsulation mac-address mlag-system-id
   vxlan udp-port 4789
   vxlan vlan 70 vni 10070
   vxlan vrf Dev vni 50002
   vxlan mlag source-interface Loopback1
```

## Routing

### Service Routing Protocols Model

Multi agent routing protocol model enabled

```eos
!
service routing protocols model multi-agent
```

### Virtual Router MAC Address

#### Virtual Router MAC Address Summary

##### Virtual Router MAC Address: 00:1c:73:00:00:01

#### Virtual Router MAC Address Configuration

```eos
!
ip virtual-router mac-address 00:1c:73:00:00:01
```

### IP Routing

#### IP Routing Summary

| VRF | Routing Enabled |
| --- | --------------- |
| default | True |
| Dev | True |
| MGMT | False |

#### IP Routing Device Configuration

```eos
!
ip routing
ip routing vrf Dev
no ip routing vrf MGMT
```

### IPv6 Routing

#### IPv6 Routing Summary

| VRF | Routing Enabled |
| --- | --------------- |
| default | False |
| Dev | false |
| MGMT | false |

### ARP

Global ARP timeout: 1500

### Router BGP

#### Router BGP Summary

| BGP AS | Router ID |
| ------ | --------- |
| 65156 | 10.0.0.10 |

| BGP Tuning |
| ---------- |
| graceful-restart restart-time 300 |
| graceful-restart |
| no bgp default ipv4-unicast |
| distance bgp 20 200 200 |
| maximum-paths 4 ecmp 4 |

#### Router BGP Peer Groups

##### EVPN-OVERLAY-PEERS

| Settings | Value |
| -------- | ----- |
| Address Family | evpn |
| Source | Loopback0 |
| BFD | True |
| Ebgp multihop | 3 |
| Send community | all |
| Maximum routes | 0 (no limit) |

##### IPv4-UNDERLAY-PEERS

| Settings | Value |
| -------- | ----- |
| Address Family | ipv4 |
| Send community | all |
| Maximum routes | 12000 |

##### MLAG-IPv4-UNDERLAY-PEER

| Settings | Value |
| -------- | ----- |
| Address Family | ipv4 |
| Remote AS | 65156 |
| Next-hop self | True |
| Send community | all |
| Maximum routes | 12000 |

#### BGP Neighbors

| Neighbor | Remote AS | VRF | Shutdown | Send-community | Maximum-routes | Allowas-in | BFD | RIB Pre-Policy Retain | Route-Reflector Client | Passive |
| -------- | --------- | --- | -------- | -------------- | -------------- | ---------- | --- | --------------------- | ---------------------- | ------- |
| 10.0.0.1 | 65100 | default | - | Inherited from peer group EVPN-OVERLAY-PEERS | Inherited from peer group EVPN-OVERLAY-PEERS | - | Inherited from peer group EVPN-OVERLAY-PEERS | - | - | - |
| 10.0.0.2 | 65100 | default | - | Inherited from peer group EVPN-OVERLAY-PEERS | Inherited from peer group EVPN-OVERLAY-PEERS | - | Inherited from peer group EVPN-OVERLAY-PEERS | - | - | - |
| 10.0.0.3 | 65100 | default | - | Inherited from peer group EVPN-OVERLAY-PEERS | Inherited from peer group EVPN-OVERLAY-PEERS | - | Inherited from peer group EVPN-OVERLAY-PEERS | - | - | - |
| 10.0.0.4 | 65100 | default | - | Inherited from peer group EVPN-OVERLAY-PEERS | Inherited from peer group EVPN-OVERLAY-PEERS | - | Inherited from peer group EVPN-OVERLAY-PEERS | - | - | - |
| 192.0.0.0 | Inherited from peer group MLAG-IPv4-UNDERLAY-PEER | default | - | Inherited from peer group MLAG-IPv4-UNDERLAY-PEER | Inherited from peer group MLAG-IPv4-UNDERLAY-PEER | - | - | - | - | - |
| 192.168.1.40 | 65100 | default | - | Inherited from peer group IPv4-UNDERLAY-PEERS | Inherited from peer group IPv4-UNDERLAY-PEERS | - | - | - | - | - |
| 192.168.1.42 | 65100 | default | - | Inherited from peer group IPv4-UNDERLAY-PEERS | Inherited from peer group IPv4-UNDERLAY-PEERS | - | - | - | - | - |
| 192.168.1.44 | 65100 | default | - | Inherited from peer group IPv4-UNDERLAY-PEERS | Inherited from peer group IPv4-UNDERLAY-PEERS | - | - | - | - | - |
| 192.168.1.46 | 65100 | default | - | Inherited from peer group IPv4-UNDERLAY-PEERS | Inherited from peer group IPv4-UNDERLAY-PEERS | - | - | - | - | - |
| 192.0.0.0 | Inherited from peer group MLAG-IPv4-UNDERLAY-PEER | Dev | - | Inherited from peer group MLAG-IPv4-UNDERLAY-PEER | Inherited from peer group MLAG-IPv4-UNDERLAY-PEER | - | - | - | - | - |

#### Router BGP EVPN Address Family

- VPN import pruning is __enabled__

##### EVPN Peer Groups

| Peer Group | Activate | Encapsulation |
| ---------- | -------- | ------------- |
| EVPN-OVERLAY-PEERS | True | default |

#### Router BGP VLANs

| VLAN | Route-Distinguisher | Both Route-Target | Import Route Target | Export Route-Target | Redistribute |
| ---- | ------------------- | ----------------- | ------------------- | ------------------- | ------------ |
| 70 | 10.0.0.10:10070 | 10070:10070 | - | - | learned |

#### Router BGP VRFs

| VRF | Route-Distinguisher | Redistribute |
| --- | ------------------- | ------------ |
| Dev | 10.0.0.10:50002 | connected |

#### Router BGP Device Configuration

```eos
!
router bgp 65156
   router-id 10.0.0.10
   distance bgp 20 200 200
   graceful-restart restart-time 300
   graceful-restart
   maximum-paths 4 ecmp 4
   no bgp default ipv4-unicast
   neighbor EVPN-OVERLAY-PEERS peer group
   neighbor EVPN-OVERLAY-PEERS update-source Loopback0
   neighbor EVPN-OVERLAY-PEERS bfd
   neighbor EVPN-OVERLAY-PEERS ebgp-multihop 3
   neighbor EVPN-OVERLAY-PEERS password 7 <removed>
   neighbor EVPN-OVERLAY-PEERS send-community
   neighbor EVPN-OVERLAY-PEERS maximum-routes 0
   neighbor IPv4-UNDERLAY-PEERS peer group
   neighbor IPv4-UNDERLAY-PEERS password 7 <removed>
   neighbor IPv4-UNDERLAY-PEERS send-community
   neighbor IPv4-UNDERLAY-PEERS maximum-routes 12000
   neighbor MLAG-IPv4-UNDERLAY-PEER peer group
   neighbor MLAG-IPv4-UNDERLAY-PEER remote-as 65156
   neighbor MLAG-IPv4-UNDERLAY-PEER next-hop-self
   neighbor MLAG-IPv4-UNDERLAY-PEER description A-LEAF5
   neighbor MLAG-IPv4-UNDERLAY-PEER password 7 <removed>
   neighbor MLAG-IPv4-UNDERLAY-PEER send-community
   neighbor MLAG-IPv4-UNDERLAY-PEER maximum-routes 12000
   neighbor MLAG-IPv4-UNDERLAY-PEER route-map RM-MLAG-PEER-IN in
   neighbor 10.0.0.1 peer group EVPN-OVERLAY-PEERS
   neighbor 10.0.0.1 remote-as 65100
   neighbor 10.0.0.1 description A-SPINE1
   neighbor 10.0.0.2 peer group EVPN-OVERLAY-PEERS
   neighbor 10.0.0.2 remote-as 65100
   neighbor 10.0.0.2 description A-SPINE2
   neighbor 10.0.0.3 peer group EVPN-OVERLAY-PEERS
   neighbor 10.0.0.3 remote-as 65100
   neighbor 10.0.0.3 description A-SPINE3
   neighbor 10.0.0.4 peer group EVPN-OVERLAY-PEERS
   neighbor 10.0.0.4 remote-as 65100
   neighbor 10.0.0.4 description A-SPINE4
   neighbor 192.0.0.0 peer group MLAG-IPv4-UNDERLAY-PEER
   neighbor 192.0.0.0 description A-LEAF5
   neighbor 192.168.1.40 peer group IPv4-UNDERLAY-PEERS
   neighbor 192.168.1.40 remote-as 65100
   neighbor 192.168.1.40 description A-SPINE1_Ethernet6
   neighbor 192.168.1.42 peer group IPv4-UNDERLAY-PEERS
   neighbor 192.168.1.42 remote-as 65100
   neighbor 192.168.1.42 description A-SPINE2_Ethernet6
   neighbor 192.168.1.44 peer group IPv4-UNDERLAY-PEERS
   neighbor 192.168.1.44 remote-as 65100
   neighbor 192.168.1.44 description A-SPINE3_Ethernet6
   neighbor 192.168.1.46 peer group IPv4-UNDERLAY-PEERS
   neighbor 192.168.1.46 remote-as 65100
   neighbor 192.168.1.46 description A-SPINE4_Ethernet6
   redistribute connected route-map RM-CONN-2-BGP
   !
   vlan 70
      rd 10.0.0.10:10070
      route-target both 10070:10070
      redistribute learned
   !
   address-family evpn
      neighbor EVPN-OVERLAY-PEERS activate
      route import match-failure action discard
   !
   address-family ipv4
      no neighbor EVPN-OVERLAY-PEERS activate
      neighbor IPv4-UNDERLAY-PEERS activate
      neighbor MLAG-IPv4-UNDERLAY-PEER activate
   !
   vrf Dev
      rd 10.0.0.10:50002
      route-target import evpn 50002:50002
      route-target export evpn 50002:50002
      router-id 10.0.0.10
      neighbor 192.0.0.0 peer group MLAG-IPv4-UNDERLAY-PEER
      redistribute connected route-map RM-CONN-2-BGP-VRFS
```

## BFD

### Router BFD

#### Router BFD Multihop Summary

| Interval | Minimum RX | Multiplier |
| -------- | ---------- | ---------- |
| 300 | 300 | 3 |

#### Router BFD Device Configuration

```eos
!
router bfd
   multihop interval 300 min-rx 300 multiplier 3
```

## Multicast

### IP IGMP Snooping

#### IP IGMP Snooping Summary

| IGMP Snooping | Fast Leave | Interface Restart Query | Proxy | Restart Query Interval | Robustness Variable |
| ------------- | ---------- | ----------------------- | ----- | ---------------------- | ------------------- |
| Enabled | - | - | - | - | - |

#### IP IGMP Snooping Device Configuration

```eos
```

### Router Multicast

#### IP Router Multicast Summary

- Routing for IPv4 multicast is enabled.
- Software forwarding by the Software Forwarding Engine (SFE)

#### Router Multicast Device Configuration

```eos
!
router multicast
   ipv4
      routing
      software-forwarding sfe
```


### PIM Sparse Mode

#### PIM Sparse Mode enabled interfaces

| Interface Name | VRF Name | IP Version | DR Priority | Local Interface |
| -------------- | -------- | ---------- | ----------- | --------------- |
| Ethernet1 | - | IPv4 | - | - |
| Ethernet2 | - | IPv4 | - | - |
| Ethernet3 | - | IPv4 | - | - |
| Ethernet4 | - | IPv4 | - | - |
| Vlan4093 | - | IPv4 | - | - |

## Filters

### Prefix-lists

#### Prefix-lists Summary

##### PL-LOOPBACKS-EVPN-OVERLAY

| Sequence | Action |
| -------- | ------ |
| 10 | permit 10.0.0.0/24 eq 32 |
| 20 | permit 10.1.1.0/24 eq 32 |

##### PL-MLAG-PEER-VRFS

| Sequence | Action |
| -------- | ------ |
| 10 | permit 192.0.0.0/31 |

#### Prefix-lists Device Configuration

```eos
!
ip prefix-list PL-LOOPBACKS-EVPN-OVERLAY
   seq 10 permit 10.0.0.0/24 eq 32
   seq 20 permit 10.1.1.0/24 eq 32
!
ip prefix-list PL-MLAG-PEER-VRFS
   seq 10 permit 192.0.0.0/31
```

### Route-maps

#### Route-maps Summary

##### RM-CONN-2-BGP

| Sequence | Type | Match | Set | Sub-Route-Map | Continue |
| -------- | ---- | ----- | --- | ------------- | -------- |
| 10 | permit | ip address prefix-list PL-LOOPBACKS-EVPN-OVERLAY | - | - | - |

##### RM-CONN-2-BGP-VRFS

| Sequence | Type | Match | Set | Sub-Route-Map | Continue |
| -------- | ---- | ----- | --- | ------------- | -------- |
| 10 | deny | ip address prefix-list PL-MLAG-PEER-VRFS | - | - | - |
| 20 | permit | - | - | - | - |

##### RM-MLAG-PEER-IN

| Sequence | Type | Match | Set | Sub-Route-Map | Continue |
| -------- | ---- | ----- | --- | ------------- | -------- |
| 10 | permit | - | origin incomplete | - | - |

#### Route-maps Device Configuration

```eos
!
route-map RM-CONN-2-BGP permit 10
   match ip address prefix-list PL-LOOPBACKS-EVPN-OVERLAY
!
route-map RM-CONN-2-BGP-VRFS deny 10
   match ip address prefix-list PL-MLAG-PEER-VRFS
!
route-map RM-CONN-2-BGP-VRFS permit 20
!
route-map RM-MLAG-PEER-IN permit 10
   description Make routes learned over MLAG Peer-link less preferred on spines to ensure optimal routing
   set origin incomplete
```

## VRF Instances

### VRF Instances Summary

| VRF Name | IP Routing |
| -------- | ---------- |
| Dev | enabled |
| MGMT | disabled |

### VRF Instances Device Configuration

```eos
!
vrf instance Dev
!
vrf instance MGMT
```

## Virtual Source NAT

### Virtual Source NAT Summary

| Source NAT VRF | Source NAT IP Address |
| -------------- | --------------------- |
| Dev | 10.102.102.10 |

### Virtual Source NAT Configuration

```eos
!
ip address virtual source-nat vrf Dev address 10.102.102.10
```

## EOS CLI

```eos
!
agent KernelFib environment KERNELFIB_PROGRAM_ALL_ECMP='true'

```
