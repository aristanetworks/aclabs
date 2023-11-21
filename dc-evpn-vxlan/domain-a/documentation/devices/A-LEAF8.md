# A-LEAF8

## Table of Contents

- [Management](#management)
  - [Management Interfaces](#management-interfaces)
  - [IP Name Servers](#ip-name-servers)
  - [NTP](#ntp)
  - [Management API HTTP](#management-api-http)
- [Authentication](#authentication)
  - [Local Users](#local-users)
  - [AAA Authorization](#aaa-authorization)
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
| Management1 | oob_management | oob | MGMT | 192.168.0.108/24 | - |

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
   ip address 192.168.0.108/24
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
| 10 | Blue | - |
| 20 | Green | - |
| 30 | Orange | - |
| 40 | Purple | - |
| 50 | Yellow | - |
| 60 | Red | - |
| 70 | Brown | - |
| 80 | Black | - |
| 3001 | MLAG_iBGP_Prod | LEAF_PEER_L3 |
| 3002 | MLAG_iBGP_Dev | LEAF_PEER_L3 |
| 4093 | LEAF_PEER_L3 | LEAF_PEER_L3 |
| 4094 | MLAG_PEER | MLAG |

### VLANs Device Configuration

```eos
!
vlan 10
   name Blue
!
vlan 20
   name Green
!
vlan 30
   name Orange
!
vlan 40
   name Purple
!
vlan 50
   name Yellow
!
vlan 60
   name Red
!
vlan 70
   name Brown
!
vlan 80
   name Black
!
vlan 3001
   name MLAG_iBGP_Prod
   trunk group LEAF_PEER_L3
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
| Ethernet5 | MLAG_PEER_A-LEAF7_Ethernet5 | *trunk | *- | *- | *['LEAF_PEER_L3', 'MLAG'] | 1000 |
| Ethernet6 | MLAG_PEER_A-LEAF7_Ethernet6 | *trunk | *- | *- | *['LEAF_PEER_L3', 'MLAG'] | 1000 |

*Inherited from Port-Channel Interface

##### IPv4

| Interface | Description | Type | Channel Group | IP Address | VRF |  MTU | Shutdown | ACL In | ACL Out |
| --------- | ----------- | -----| ------------- | ---------- | ----| ---- | -------- | ------ | ------- |
| Ethernet1 | P2P_LINK_TO_A-SPINE1_Ethernet8 | routed | - | 192.168.1.57/31 | default | 9214 | False | - | - |
| Ethernet2 | P2P_LINK_TO_A-SPINE2_Ethernet8 | routed | - | 192.168.1.59/31 | default | 9214 | False | - | - |
| Ethernet3 | P2P_LINK_TO_A-SPINE3_Ethernet8 | routed | - | 192.168.1.61/31 | default | 9214 | False | - | - |
| Ethernet4 | P2P_LINK_TO_A-SPINE4_Ethernet8 | routed | - | 192.168.1.63/31 | default | 9214 | False | - | - |
| Ethernet7 | P2P_LINK_TO_BB1_Ethernet2 | routed | - | 172.16.1.4/31 | default | 9214 | False | - | - |
| Ethernet8 | P2P_LINK_TO_BB2_Ethernet2 | routed | - | 172.16.1.6/31 | default | 9214 | False | - | - |

#### Ethernet Interfaces Device Configuration

```eos
!
interface Ethernet1
   description P2P_LINK_TO_A-SPINE1_Ethernet8
   no shutdown
   mtu 9214
   no switchport
   ip address 192.168.1.57/31
!
interface Ethernet2
   description P2P_LINK_TO_A-SPINE2_Ethernet8
   no shutdown
   mtu 9214
   no switchport
   ip address 192.168.1.59/31
!
interface Ethernet3
   description P2P_LINK_TO_A-SPINE3_Ethernet8
   no shutdown
   mtu 9214
   no switchport
   ip address 192.168.1.61/31
!
interface Ethernet4
   description P2P_LINK_TO_A-SPINE4_Ethernet8
   no shutdown
   mtu 9214
   no switchport
   ip address 192.168.1.63/31
!
interface Ethernet5
   description MLAG_PEER_A-LEAF7_Ethernet5
   no shutdown
   channel-group 1000 mode active
!
interface Ethernet6
   description MLAG_PEER_A-LEAF7_Ethernet6
   no shutdown
   channel-group 1000 mode active
!
interface Ethernet7
   description P2P_LINK_TO_BB1_Ethernet2
   no shutdown
   mtu 9214
   no switchport
   ip address 172.16.1.4/31
!
interface Ethernet8
   description P2P_LINK_TO_BB2_Ethernet2
   no shutdown
   mtu 9214
   no switchport
   ip address 172.16.1.6/31
```

### Port-Channel Interfaces

#### Port-Channel Interfaces Summary

##### L2

| Interface | Description | Type | Mode | VLANs | Native VLAN | Trunk Group | LACP Fallback Timeout | LACP Fallback Mode | MLAG ID | EVPN ESI |
| --------- | ----------- | ---- | ---- | ----- | ----------- | ------------| --------------------- | ------------------ | ------- | -------- |
| Port-Channel1000 | MLAG_PEER_A-LEAF7_Po1000 | switched | trunk | - | - | ['LEAF_PEER_L3', 'MLAG'] | - | - | - | - |

#### Port-Channel Interfaces Device Configuration

```eos
!
interface Port-Channel1000
   description MLAG_PEER_A-LEAF7_Po1000
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
| Loopback0 | EVPN_Overlay_Peering | default | 10.0.0.12/32 |
| Loopback1 | VTEP_VXLAN_Tunnel_Source | default | 10.1.1.11/32 |
| Loopback101 | Prod_VTEP_DIAGNOSTICS | Prod | 10.101.101.12/32 |
| Loopback102 | Dev_VTEP_DIAGNOSTICS | Dev | 10.102.102.12/32 |

##### IPv6

| Interface | Description | VRF | IPv6 Address |
| --------- | ----------- | --- | ------------ |
| Loopback0 | EVPN_Overlay_Peering | default | - |
| Loopback1 | VTEP_VXLAN_Tunnel_Source | default | - |
| Loopback101 | Prod_VTEP_DIAGNOSTICS | Prod | - |
| Loopback102 | Dev_VTEP_DIAGNOSTICS | Dev | - |


#### Loopback Interfaces Device Configuration

```eos
!
interface Loopback0
   description EVPN_Overlay_Peering
   no shutdown
   ip address 10.0.0.12/32
!
interface Loopback1
   description VTEP_VXLAN_Tunnel_Source
   no shutdown
   ip address 10.1.1.11/32
!
interface Loopback101
   description Prod_VTEP_DIAGNOSTICS
   no shutdown
   vrf Prod
   ip address 10.101.101.12/32
!
interface Loopback102
   description Dev_VTEP_DIAGNOSTICS
   no shutdown
   vrf Dev
   ip address 10.102.102.12/32
```

### VLAN Interfaces

#### VLAN Interfaces Summary

| Interface | Description | VRF |  MTU | Shutdown |
| --------- | ----------- | --- | ---- | -------- |
| Vlan10 | Blue | Prod | 9014 | False |
| Vlan20 | Green | Prod | 9014 | False |
| Vlan30 | Orange | Prod | 9014 | False |
| Vlan40 | Purple | Prod | 9014 | False |
| Vlan50 | Yellow | Dev | 9014 | False |
| Vlan60 | Red | Dev | 9014 | False |
| Vlan70 | Brown | Dev | 9014 | False |
| Vlan80 | Black | Dev | 9014 | False |
| Vlan3001 | MLAG_PEER_L3_iBGP: vrf Prod | Prod | 9214 | False |
| Vlan3002 | MLAG_PEER_L3_iBGP: vrf Dev | Dev | 9214 | False |
| Vlan4093 | MLAG_PEER_L3_PEERING | default | 9214 | False |
| Vlan4094 | MLAG_PEER | default | 1500 | False |

##### IPv4

| Interface | VRF | IP Address | IP Address Virtual | IP Router Virtual Address | VRRP | ACL In | ACL Out |
| --------- | --- | ---------- | ------------------ | ------------------------- | ---- | ------ | ------- |
| Vlan10 |  Prod  |  -  |  10.10.10.1/24  |  -  |  -  |  -  |  -  |
| Vlan20 |  Prod  |  -  |  10.20.20.1/24  |  -  |  -  |  -  |  -  |
| Vlan30 |  Prod  |  -  |  10.30.30.1/24  |  -  |  -  |  -  |  -  |
| Vlan40 |  Prod  |  -  |  10.40.40.1/24  |  -  |  -  |  -  |  -  |
| Vlan50 |  Dev  |  -  |  10.50.50.1/24  |  -  |  -  |  -  |  -  |
| Vlan60 |  Dev  |  -  |  10.60.60.1/24  |  -  |  -  |  -  |  -  |
| Vlan70 |  Dev  |  -  |  10.70.70.1/24  |  -  |  -  |  -  |  -  |
| Vlan80 |  Dev  |  -  |  10.80.80.1/24  |  -  |  -  |  -  |  -  |
| Vlan3001 |  Prod  |  192.0.0.1/31  |  -  |  -  |  -  |  -  |  -  |
| Vlan3002 |  Dev  |  192.0.0.1/31  |  -  |  -  |  -  |  -  |  -  |
| Vlan4093 |  default  |  192.0.0.1/31  |  -  |  -  |  -  |  -  |  -  |
| Vlan4094 |  default  |  169.254.0.1/31  |  -  |  -  |  -  |  -  |  -  |

#### VLAN Interfaces Device Configuration

```eos
!
interface Vlan10
   description Blue
   no shutdown
   mtu 9014
   vrf Prod
   ip address virtual 10.10.10.1/24
!
interface Vlan20
   description Green
   no shutdown
   mtu 9014
   vrf Prod
   ip address virtual 10.20.20.1/24
!
interface Vlan30
   description Orange
   no shutdown
   mtu 9014
   vrf Prod
   ip address virtual 10.30.30.1/24
!
interface Vlan40
   description Purple
   no shutdown
   mtu 9014
   vrf Prod
   ip address virtual 10.40.40.1/24
!
interface Vlan50
   description Yellow
   no shutdown
   mtu 9014
   vrf Dev
   ip address virtual 10.50.50.1/24
!
interface Vlan60
   description Red
   no shutdown
   mtu 9014
   vrf Dev
   ip address virtual 10.60.60.1/24
!
interface Vlan70
   description Brown
   no shutdown
   mtu 9014
   vrf Dev
   ip address virtual 10.70.70.1/24
!
interface Vlan80
   description Black
   no shutdown
   mtu 9014
   vrf Dev
   ip address virtual 10.80.80.1/24
!
interface Vlan3001
   description MLAG_PEER_L3_iBGP: vrf Prod
   no shutdown
   mtu 9214
   vrf Prod
   ip address 192.0.0.1/31
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
| Source Interface | Loopback1 |
| UDP port | 4789 |
| EVPN MLAG Shared Router MAC | mlag-system-id |

##### VLAN to VNI, Flood List and Multicast Group Mappings

| VLAN | VNI | Flood List | Multicast Group |
| ---- | --- | ---------- | --------------- |
| 10 | 10010 | - | - |
| 20 | 10020 | - | - |
| 30 | 10030 | - | - |
| 40 | 10040 | - | - |
| 50 | 10050 | - | - |
| 60 | 10060 | - | - |
| 70 | 10070 | - | - |
| 80 | 10080 | - | - |

##### VRF to VNI and Multicast Group Mappings

| VRF | VNI | Multicast Group |
| ---- | --- | --------------- |
| Dev | 50002 | - |
| Prod | 50001 | - |

#### VXLAN Interface Device Configuration

```eos
!
interface Vxlan1
   description A-LEAF8_VTEP
   vxlan source-interface Loopback1
   vxlan virtual-router encapsulation mac-address mlag-system-id
   vxlan udp-port 4789
   vxlan vlan 10 vni 10010
   vxlan vlan 20 vni 10020
   vxlan vlan 30 vni 10030
   vxlan vlan 40 vni 10040
   vxlan vlan 50 vni 10050
   vxlan vlan 60 vni 10060
   vxlan vlan 70 vni 10070
   vxlan vlan 80 vni 10080
   vxlan vrf Dev vni 50002
   vxlan vrf Prod vni 50001
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
| Prod | True |

#### IP Routing Device Configuration

```eos
!
ip routing
ip routing vrf Dev
no ip routing vrf MGMT
ip routing vrf Prod
```

### IPv6 Routing

#### IPv6 Routing Summary

| VRF | Routing Enabled |
| --- | --------------- |
| default | False |
| Dev | false |
| MGMT | false |
| Prod | false |

### ARP

Global ARP timeout: 1500

### Router BGP

#### Router BGP Summary

| BGP AS | Router ID |
| ------ | --------- |
| 65178 | 10.0.0.12 |

| BGP Tuning |
| ---------- |
| graceful-restart restart-time 300 |
| graceful-restart |
| no bgp default ipv4-unicast |
| distance bgp 20 200 200 |
| maximum-paths 4 ecmp 4 |

#### Router BGP Peer Groups

##### EVPN-OVERLAY-CORE

| Settings | Value |
| -------- | ----- |
| Address Family | evpn |
| Local AS | 65500 |
| Source | Loopback0 |
| BFD | True |
| Ebgp multihop | 15 |
| Send community | all |
| Maximum routes | 0 (no limit) |

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
| Remote AS | 65178 |
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
| 172.16.0.1 | 65500 | default | - | Inherited from peer group EVPN-OVERLAY-CORE | Inherited from peer group EVPN-OVERLAY-CORE | - | Inherited from peer group EVPN-OVERLAY-CORE | - | - | - |
| 172.16.0.2 | 65500 | default | - | Inherited from peer group EVPN-OVERLAY-CORE | Inherited from peer group EVPN-OVERLAY-CORE | - | Inherited from peer group EVPN-OVERLAY-CORE | - | - | - |
| 172.16.1.5 | 65500 | default | - | Inherited from peer group IPv4-UNDERLAY-PEERS | Inherited from peer group IPv4-UNDERLAY-PEERS | - | - | - | - | - |
| 172.16.1.7 | 65500 | default | - | Inherited from peer group IPv4-UNDERLAY-PEERS | Inherited from peer group IPv4-UNDERLAY-PEERS | - | - | - | - | - |
| 192.0.0.0 | Inherited from peer group MLAG-IPv4-UNDERLAY-PEER | default | - | Inherited from peer group MLAG-IPv4-UNDERLAY-PEER | Inherited from peer group MLAG-IPv4-UNDERLAY-PEER | - | - | - | - | - |
| 192.168.1.56 | 65100 | default | - | Inherited from peer group IPv4-UNDERLAY-PEERS | Inherited from peer group IPv4-UNDERLAY-PEERS | - | - | - | - | - |
| 192.168.1.58 | 65100 | default | - | Inherited from peer group IPv4-UNDERLAY-PEERS | Inherited from peer group IPv4-UNDERLAY-PEERS | - | - | - | - | - |
| 192.168.1.60 | 65100 | default | - | Inherited from peer group IPv4-UNDERLAY-PEERS | Inherited from peer group IPv4-UNDERLAY-PEERS | - | - | - | - | - |
| 192.168.1.62 | 65100 | default | - | Inherited from peer group IPv4-UNDERLAY-PEERS | Inherited from peer group IPv4-UNDERLAY-PEERS | - | - | - | - | - |
| 192.0.0.0 | Inherited from peer group MLAG-IPv4-UNDERLAY-PEER | Dev | - | Inherited from peer group MLAG-IPv4-UNDERLAY-PEER | Inherited from peer group MLAG-IPv4-UNDERLAY-PEER | - | - | - | - | - |
| 192.0.0.0 | Inherited from peer group MLAG-IPv4-UNDERLAY-PEER | Prod | - | Inherited from peer group MLAG-IPv4-UNDERLAY-PEER | Inherited from peer group MLAG-IPv4-UNDERLAY-PEER | - | - | - | - | - |

#### Router BGP EVPN Address Family

- VPN import pruning is __enabled__

##### EVPN Peer Groups

| Peer Group | Activate | Encapsulation |
| ---------- | -------- | ------------- |
| EVPN-OVERLAY-CORE | True | default |
| EVPN-OVERLAY-PEERS | True | default |

##### EVPN DCI Gateway Summary

| Settings | Value |
| -------- | ----- |
| Remote Domain Peer Groups | EVPN-OVERLAY-CORE |
| L3 Gateway Configured | True |
| L3 Gateway Inter-domain | True |

#### Router BGP VLANs

| VLAN | Route-Distinguisher | Both Route-Target | Import Route Target | Export Route-Target | Redistribute |
| ---- | ------------------- | ----------------- | ------------------- | ------------------- | ------------ |
| 10 | 10.0.0.12:10010 | 10010:10010<br>remote 10010:10010 | - | - | learned |
| 20 | 10.0.0.12:10020 | 10020:10020<br>remote 10020:10020 | - | - | learned |
| 30 | 10.0.0.12:10030 | 10030:10030<br>remote 10030:10030 | - | - | learned |
| 40 | 10.0.0.12:10040 | 10040:10040<br>remote 10040:10040 | - | - | learned |
| 50 | 10.0.0.12:10050 | 10050:10050<br>remote 10050:10050 | - | - | learned |
| 60 | 10.0.0.12:10060 | 10060:10060<br>remote 10060:10060 | - | - | learned |
| 70 | 10.0.0.12:10070 | 10070:10070<br>remote 10070:10070 | - | - | learned |
| 80 | 10.0.0.12:10080 | 10080:10080<br>remote 10080:10080 | - | - | learned |

#### Router BGP VRFs

| VRF | Route-Distinguisher | Redistribute |
| --- | ------------------- | ------------ |
| Dev | 10.0.0.12:50002 | connected |
| Prod | 10.0.0.12:50001 | connected |

#### Router BGP Device Configuration

```eos
!
router bgp 65178
   router-id 10.0.0.12
   distance bgp 20 200 200
   graceful-restart restart-time 300
   graceful-restart
   maximum-paths 4 ecmp 4
   no bgp default ipv4-unicast
   neighbor EVPN-OVERLAY-CORE peer group
   neighbor EVPN-OVERLAY-CORE local-as 65500 no-prepend replace-as
   neighbor EVPN-OVERLAY-CORE update-source Loopback0
   neighbor EVPN-OVERLAY-CORE bfd
   neighbor EVPN-OVERLAY-CORE ebgp-multihop 15
   neighbor EVPN-OVERLAY-CORE send-community
   neighbor EVPN-OVERLAY-CORE maximum-routes 0
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
   neighbor MLAG-IPv4-UNDERLAY-PEER remote-as 65178
   neighbor MLAG-IPv4-UNDERLAY-PEER next-hop-self
   neighbor MLAG-IPv4-UNDERLAY-PEER description A-LEAF7
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
   neighbor 172.16.0.1 peer group EVPN-OVERLAY-CORE
   neighbor 172.16.0.1 remote-as 65500
   neighbor 172.16.0.1 description BB1
   neighbor 172.16.0.2 peer group EVPN-OVERLAY-CORE
   neighbor 172.16.0.2 remote-as 65500
   neighbor 172.16.0.2 description BB2
   neighbor 172.16.1.5 peer group IPv4-UNDERLAY-PEERS
   neighbor 172.16.1.5 remote-as 65500
   neighbor 172.16.1.5 description BB1
   neighbor 172.16.1.7 peer group IPv4-UNDERLAY-PEERS
   neighbor 172.16.1.7 remote-as 65500
   neighbor 172.16.1.7 description BB2
   neighbor 192.0.0.0 peer group MLAG-IPv4-UNDERLAY-PEER
   neighbor 192.0.0.0 description A-LEAF7
   neighbor 192.168.1.56 peer group IPv4-UNDERLAY-PEERS
   neighbor 192.168.1.56 remote-as 65100
   neighbor 192.168.1.56 description A-SPINE1_Ethernet8
   neighbor 192.168.1.58 peer group IPv4-UNDERLAY-PEERS
   neighbor 192.168.1.58 remote-as 65100
   neighbor 192.168.1.58 description A-SPINE2_Ethernet8
   neighbor 192.168.1.60 peer group IPv4-UNDERLAY-PEERS
   neighbor 192.168.1.60 remote-as 65100
   neighbor 192.168.1.60 description A-SPINE3_Ethernet8
   neighbor 192.168.1.62 peer group IPv4-UNDERLAY-PEERS
   neighbor 192.168.1.62 remote-as 65100
   neighbor 192.168.1.62 description A-SPINE4_Ethernet8
   redistribute connected route-map RM-CONN-2-BGP
   !
   vlan 10
      rd 10.0.0.12:10010
      rd evpn domain remote 10.0.0.12:10010
      route-target both 10010:10010
      route-target import export evpn domain remote 10010:10010
      redistribute learned
   !
   vlan 20
      rd 10.0.0.12:10020
      rd evpn domain remote 10.0.0.12:10020
      route-target both 10020:10020
      route-target import export evpn domain remote 10020:10020
      redistribute learned
   !
   vlan 30
      rd 10.0.0.12:10030
      rd evpn domain remote 10.0.0.12:10030
      route-target both 10030:10030
      route-target import export evpn domain remote 10030:10030
      redistribute learned
   !
   vlan 40
      rd 10.0.0.12:10040
      rd evpn domain remote 10.0.0.12:10040
      route-target both 10040:10040
      route-target import export evpn domain remote 10040:10040
      redistribute learned
   !
   vlan 50
      rd 10.0.0.12:10050
      rd evpn domain remote 10.0.0.12:10050
      route-target both 10050:10050
      route-target import export evpn domain remote 10050:10050
      redistribute learned
   !
   vlan 60
      rd 10.0.0.12:10060
      rd evpn domain remote 10.0.0.12:10060
      route-target both 10060:10060
      route-target import export evpn domain remote 10060:10060
      redistribute learned
   !
   vlan 70
      rd 10.0.0.12:10070
      rd evpn domain remote 10.0.0.12:10070
      route-target both 10070:10070
      route-target import export evpn domain remote 10070:10070
      redistribute learned
   !
   vlan 80
      rd 10.0.0.12:10080
      rd evpn domain remote 10.0.0.12:10080
      route-target both 10080:10080
      route-target import export evpn domain remote 10080:10080
      redistribute learned
   !
   address-family evpn
      neighbor EVPN-OVERLAY-CORE activate
      neighbor EVPN-OVERLAY-CORE domain remote
      neighbor EVPN-OVERLAY-PEERS activate
      neighbor default next-hop-self received-evpn-routes route-type ip-prefix inter-domain
      route import match-failure action discard
   !
   address-family ipv4
      no neighbor EVPN-OVERLAY-CORE activate
      no neighbor EVPN-OVERLAY-PEERS activate
      neighbor IPv4-UNDERLAY-PEERS activate
      neighbor MLAG-IPv4-UNDERLAY-PEER activate
   !
   vrf Dev
      rd 10.0.0.12:50002
      route-target import evpn 50002:50002
      route-target export evpn 50002:50002
      router-id 10.0.0.12
      neighbor 192.0.0.0 peer group MLAG-IPv4-UNDERLAY-PEER
      redistribute connected route-map RM-CONN-2-BGP-VRFS
   !
   vrf Prod
      rd 10.0.0.12:50001
      route-target import evpn 50001:50001
      route-target export evpn 50001:50001
      router-id 10.0.0.12
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
| Prod | enabled |

### VRF Instances Device Configuration

```eos
!
vrf instance Dev
!
vrf instance MGMT
!
vrf instance Prod
```

## Virtual Source NAT

### Virtual Source NAT Summary

| Source NAT VRF | Source NAT IP Address |
| -------------- | --------------------- |
| Dev | 10.102.102.12 |
| Prod | 10.101.101.12 |

### Virtual Source NAT Configuration

```eos
!
ip address virtual source-nat vrf Dev address 10.102.102.12
ip address virtual source-nat vrf Prod address 10.101.101.12
```

## EOS CLI

```eos
!
agent KernelFib environment KERNELFIB_PROGRAM_ALL_ECMP='true'

```
