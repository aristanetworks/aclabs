# A-SPINE4

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
- [Spanning Tree](#spanning-tree)
  - [Spanning Tree Summary](#spanning-tree-summary)
  - [Spanning Tree Device Configuration](#spanning-tree-device-configuration)
- [Internal VLAN Allocation Policy](#internal-vlan-allocation-policy)
  - [Internal VLAN Allocation Policy Summary](#internal-vlan-allocation-policy-summary)
  - [Internal VLAN Allocation Policy Configuration](#internal-vlan-allocation-policy-configuration)
- [MAC Address Table](#mac-address-table)
  - [MAC Address Table Summary](#mac-address-table-summary)
  - [MAC Address Table Device Configuration](#mac-address-table-device-configuration)
- [Interfaces](#interfaces)
  - [Switchport Default](#switchport-default)
  - [Ethernet Interfaces](#ethernet-interfaces)
  - [Loopback Interfaces](#loopback-interfaces)
- [Routing](#routing)
  - [Service Routing Protocols Model](#service-routing-protocols-model)
  - [IP Routing](#ip-routing)
  - [IPv6 Routing](#ipv6-routing)
  - [ARP](#arp)
  - [Router BGP](#router-bgp)
- [BFD](#bfd)
  - [Router BFD](#router-bfd)
- [Multicast](#multicast)
  - [Router Multicast](#router-multicast)
  - [PIM Sparse Mode](#pim-sparse-mode)
- [Filters](#filters)
  - [Prefix-lists](#prefix-lists)
  - [Route-maps](#route-maps)
- [VRF Instances](#vrf-instances)
  - [VRF Instances Summary](#vrf-instances-summary)
  - [VRF Instances Device Configuration](#vrf-instances-device-configuration)
- [EOS CLI](#eos-cli)

## Management

### Management Interfaces

#### Management Interfaces Summary

##### IPv4

| Management Interface | description | Type | VRF | IP Address | Gateway |
| -------------------- | ----------- | ---- | --- | ---------- | ------- |
| Management1 | oob_management | oob | MGMT | 192.168.0.14/24 | - |

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
   ip address 192.168.0.14/24
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

## Spanning Tree

### Spanning Tree Summary

STP mode: **none**

### Spanning Tree Device Configuration

```eos
!
spanning-tree mode none
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

## MAC Address Table

### MAC Address Table Summary

- MAC address table entry maximum age: 1800 seconds

### MAC Address Table Device Configuration

```eos
!
mac address-table aging-time 1800
```

## Interfaces

### Switchport Default

#### Switchport Defaults Summary

- Default Switchport Mode: routed

#### Switchport Default Configuration

```eos
!
switchport default mode routed
```

### Ethernet Interfaces

#### Ethernet Interfaces Summary

##### L2

| Interface | Description | Mode | VLANs | Native VLAN | Trunk Group | Channel-Group |
| --------- | ----------- | ---- | ----- | ----------- | ----------- | ------------- |

*Inherited from Port-Channel Interface

##### IPv4

| Interface | Description | Type | Channel Group | IP Address | VRF |  MTU | Shutdown | ACL In | ACL Out |
| --------- | ----------- | -----| ------------- | ---------- | ----| ---- | -------- | ------ | ------- |
| Ethernet1 | P2P_LINK_TO_A-LEAF1_Ethernet4 | routed | - | 192.168.1.6/31 | default | 9214 | False | - | - |
| Ethernet2 | P2P_LINK_TO_A-LEAF2_Ethernet4 | routed | - | 192.168.1.14/31 | default | 9214 | False | - | - |
| Ethernet3 | P2P_LINK_TO_A-LEAF3_Ethernet4 | routed | - | 192.168.1.22/31 | default | 9214 | False | - | - |
| Ethernet4 | P2P_LINK_TO_A-LEAF4_Ethernet4 | routed | - | 192.168.1.30/31 | default | 9214 | False | - | - |
| Ethernet5 | P2P_LINK_TO_A-LEAF5_Ethernet4 | routed | - | 192.168.1.38/31 | default | 9214 | False | - | - |
| Ethernet6 | P2P_LINK_TO_A-LEAF6_Ethernet4 | routed | - | 192.168.1.46/31 | default | 9214 | False | - | - |
| Ethernet7 | P2P_LINK_TO_A-LEAF7_Ethernet4 | routed | - | 192.168.1.54/31 | default | 9214 | False | - | - |
| Ethernet8 | P2P_LINK_TO_A-LEAF8_Ethernet4 | routed | - | 192.168.1.62/31 | default | 9214 | False | - | - |

#### Ethernet Interfaces Device Configuration

```eos
!
interface Ethernet1
   description P2P_LINK_TO_A-LEAF1_Ethernet4
   no shutdown
   mtu 9214
   no switchport
   ip address 192.168.1.6/31
   pim ipv4 sparse-mode
!
interface Ethernet2
   description P2P_LINK_TO_A-LEAF2_Ethernet4
   no shutdown
   mtu 9214
   no switchport
   ip address 192.168.1.14/31
   pim ipv4 sparse-mode
!
interface Ethernet3
   description P2P_LINK_TO_A-LEAF3_Ethernet4
   no shutdown
   mtu 9214
   no switchport
   ip address 192.168.1.22/31
   pim ipv4 sparse-mode
!
interface Ethernet4
   description P2P_LINK_TO_A-LEAF4_Ethernet4
   no shutdown
   mtu 9214
   no switchport
   ip address 192.168.1.30/31
   pim ipv4 sparse-mode
!
interface Ethernet5
   description P2P_LINK_TO_A-LEAF5_Ethernet4
   no shutdown
   mtu 9214
   no switchport
   ip address 192.168.1.38/31
   pim ipv4 sparse-mode
!
interface Ethernet6
   description P2P_LINK_TO_A-LEAF6_Ethernet4
   no shutdown
   mtu 9214
   no switchport
   ip address 192.168.1.46/31
   pim ipv4 sparse-mode
!
interface Ethernet7
   description P2P_LINK_TO_A-LEAF7_Ethernet4
   no shutdown
   mtu 9214
   no switchport
   ip address 192.168.1.54/31
!
interface Ethernet8
   description P2P_LINK_TO_A-LEAF8_Ethernet4
   no shutdown
   mtu 9214
   no switchport
   ip address 192.168.1.62/31
```

### Loopback Interfaces

#### Loopback Interfaces Summary

##### IPv4

| Interface | Description | VRF | IP Address |
| --------- | ----------- | --- | ---------- |
| Loopback0 | EVPN_Overlay_Peering | default | 10.0.0.4/32 |

##### IPv6

| Interface | Description | VRF | IPv6 Address |
| --------- | ----------- | --- | ------------ |
| Loopback0 | EVPN_Overlay_Peering | default | - |


#### Loopback Interfaces Device Configuration

```eos
!
interface Loopback0
   description EVPN_Overlay_Peering
   no shutdown
   ip address 10.0.0.4/32
```

## Routing

### Service Routing Protocols Model

Multi agent routing protocol model enabled

```eos
!
service routing protocols model multi-agent
```

### IP Routing

#### IP Routing Summary

| VRF | Routing Enabled |
| --- | --------------- |
| default | True |
| MGMT | False |

#### IP Routing Device Configuration

```eos
!
ip routing
no ip routing vrf MGMT
```

### IPv6 Routing

#### IPv6 Routing Summary

| VRF | Routing Enabled |
| --- | --------------- |
| default | False |
| MGMT | false |

### ARP

Global ARP timeout: 1500

### Router BGP

#### Router BGP Summary

| BGP AS | Router ID |
| ------ | --------- |
| 65100 | 10.0.0.4 |

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
| Next-hop unchanged | True |
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

#### BGP Neighbors

| Neighbor | Remote AS | VRF | Shutdown | Send-community | Maximum-routes | Allowas-in | BFD | RIB Pre-Policy Retain | Route-Reflector Client | Passive |
| -------- | --------- | --- | -------- | -------------- | -------------- | ---------- | --- | --------------------- | ---------------------- | ------- |
| 10.0.0.5 | 65112 | default | - | Inherited from peer group EVPN-OVERLAY-PEERS | Inherited from peer group EVPN-OVERLAY-PEERS | - | Inherited from peer group EVPN-OVERLAY-PEERS | - | - | - |
| 10.0.0.6 | 65112 | default | - | Inherited from peer group EVPN-OVERLAY-PEERS | Inherited from peer group EVPN-OVERLAY-PEERS | - | Inherited from peer group EVPN-OVERLAY-PEERS | - | - | - |
| 10.0.0.7 | 65134 | default | - | Inherited from peer group EVPN-OVERLAY-PEERS | Inherited from peer group EVPN-OVERLAY-PEERS | - | Inherited from peer group EVPN-OVERLAY-PEERS | - | - | - |
| 10.0.0.8 | 65134 | default | - | Inherited from peer group EVPN-OVERLAY-PEERS | Inherited from peer group EVPN-OVERLAY-PEERS | - | Inherited from peer group EVPN-OVERLAY-PEERS | - | - | - |
| 10.0.0.9 | 65156 | default | - | Inherited from peer group EVPN-OVERLAY-PEERS | Inherited from peer group EVPN-OVERLAY-PEERS | - | Inherited from peer group EVPN-OVERLAY-PEERS | - | - | - |
| 10.0.0.10 | 65156 | default | - | Inherited from peer group EVPN-OVERLAY-PEERS | Inherited from peer group EVPN-OVERLAY-PEERS | - | Inherited from peer group EVPN-OVERLAY-PEERS | - | - | - |
| 10.0.0.11 | 65178 | default | - | Inherited from peer group EVPN-OVERLAY-PEERS | Inherited from peer group EVPN-OVERLAY-PEERS | - | Inherited from peer group EVPN-OVERLAY-PEERS | - | - | - |
| 10.0.0.12 | 65178 | default | - | Inherited from peer group EVPN-OVERLAY-PEERS | Inherited from peer group EVPN-OVERLAY-PEERS | - | Inherited from peer group EVPN-OVERLAY-PEERS | - | - | - |
| 192.168.1.7 | 65112 | default | - | Inherited from peer group IPv4-UNDERLAY-PEERS | Inherited from peer group IPv4-UNDERLAY-PEERS | - | - | - | - | - |
| 192.168.1.15 | 65112 | default | - | Inherited from peer group IPv4-UNDERLAY-PEERS | Inherited from peer group IPv4-UNDERLAY-PEERS | - | - | - | - | - |
| 192.168.1.23 | 65134 | default | - | Inherited from peer group IPv4-UNDERLAY-PEERS | Inherited from peer group IPv4-UNDERLAY-PEERS | - | - | - | - | - |
| 192.168.1.31 | 65134 | default | - | Inherited from peer group IPv4-UNDERLAY-PEERS | Inherited from peer group IPv4-UNDERLAY-PEERS | - | - | - | - | - |
| 192.168.1.39 | 65156 | default | - | Inherited from peer group IPv4-UNDERLAY-PEERS | Inherited from peer group IPv4-UNDERLAY-PEERS | - | - | - | - | - |
| 192.168.1.47 | 65156 | default | - | Inherited from peer group IPv4-UNDERLAY-PEERS | Inherited from peer group IPv4-UNDERLAY-PEERS | - | - | - | - | - |
| 192.168.1.55 | 65178 | default | - | Inherited from peer group IPv4-UNDERLAY-PEERS | Inherited from peer group IPv4-UNDERLAY-PEERS | - | - | - | - | - |
| 192.168.1.63 | 65178 | default | - | Inherited from peer group IPv4-UNDERLAY-PEERS | Inherited from peer group IPv4-UNDERLAY-PEERS | - | - | - | - | - |

#### Router BGP EVPN Address Family

##### EVPN Peer Groups

| Peer Group | Activate | Encapsulation |
| ---------- | -------- | ------------- |
| EVPN-OVERLAY-PEERS | True | default |

#### Router BGP Device Configuration

```eos
!
router bgp 65100
   router-id 10.0.0.4
   distance bgp 20 200 200
   graceful-restart restart-time 300
   graceful-restart
   maximum-paths 4 ecmp 4
   no bgp default ipv4-unicast
   neighbor EVPN-OVERLAY-PEERS peer group
   neighbor EVPN-OVERLAY-PEERS next-hop-unchanged
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
   neighbor 10.0.0.5 peer group EVPN-OVERLAY-PEERS
   neighbor 10.0.0.5 remote-as 65112
   neighbor 10.0.0.5 description A-LEAF1
   neighbor 10.0.0.6 peer group EVPN-OVERLAY-PEERS
   neighbor 10.0.0.6 remote-as 65112
   neighbor 10.0.0.6 description A-LEAF2
   neighbor 10.0.0.7 peer group EVPN-OVERLAY-PEERS
   neighbor 10.0.0.7 remote-as 65134
   neighbor 10.0.0.7 description A-LEAF3
   neighbor 10.0.0.8 peer group EVPN-OVERLAY-PEERS
   neighbor 10.0.0.8 remote-as 65134
   neighbor 10.0.0.8 description A-LEAF4
   neighbor 10.0.0.9 peer group EVPN-OVERLAY-PEERS
   neighbor 10.0.0.9 remote-as 65156
   neighbor 10.0.0.9 description A-LEAF5
   neighbor 10.0.0.10 peer group EVPN-OVERLAY-PEERS
   neighbor 10.0.0.10 remote-as 65156
   neighbor 10.0.0.10 description A-LEAF6
   neighbor 10.0.0.11 peer group EVPN-OVERLAY-PEERS
   neighbor 10.0.0.11 remote-as 65178
   neighbor 10.0.0.11 description A-LEAF7
   neighbor 10.0.0.12 peer group EVPN-OVERLAY-PEERS
   neighbor 10.0.0.12 remote-as 65178
   neighbor 10.0.0.12 description A-LEAF8
   neighbor 192.168.1.7 peer group IPv4-UNDERLAY-PEERS
   neighbor 192.168.1.7 remote-as 65112
   neighbor 192.168.1.7 description A-LEAF1_Ethernet4
   neighbor 192.168.1.15 peer group IPv4-UNDERLAY-PEERS
   neighbor 192.168.1.15 remote-as 65112
   neighbor 192.168.1.15 description A-LEAF2_Ethernet4
   neighbor 192.168.1.23 peer group IPv4-UNDERLAY-PEERS
   neighbor 192.168.1.23 remote-as 65134
   neighbor 192.168.1.23 description A-LEAF3_Ethernet4
   neighbor 192.168.1.31 peer group IPv4-UNDERLAY-PEERS
   neighbor 192.168.1.31 remote-as 65134
   neighbor 192.168.1.31 description A-LEAF4_Ethernet4
   neighbor 192.168.1.39 peer group IPv4-UNDERLAY-PEERS
   neighbor 192.168.1.39 remote-as 65156
   neighbor 192.168.1.39 description A-LEAF5_Ethernet4
   neighbor 192.168.1.47 peer group IPv4-UNDERLAY-PEERS
   neighbor 192.168.1.47 remote-as 65156
   neighbor 192.168.1.47 description A-LEAF6_Ethernet4
   neighbor 192.168.1.55 peer group IPv4-UNDERLAY-PEERS
   neighbor 192.168.1.55 remote-as 65178
   neighbor 192.168.1.55 description A-LEAF7_Ethernet4
   neighbor 192.168.1.63 peer group IPv4-UNDERLAY-PEERS
   neighbor 192.168.1.63 remote-as 65178
   neighbor 192.168.1.63 description A-LEAF8_Ethernet4
   redistribute connected route-map RM-CONN-2-BGP
   !
   address-family evpn
      neighbor EVPN-OVERLAY-PEERS activate
   !
   address-family ipv4
      no neighbor EVPN-OVERLAY-PEERS activate
      neighbor IPv4-UNDERLAY-PEERS activate
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

### Router Multicast

#### IP Router Multicast Summary

- Routing for IPv4 multicast is enabled.

#### Router Multicast Device Configuration

```eos
!
router multicast
   ipv4
      routing
```


### PIM Sparse Mode

#### PIM Sparse Mode enabled interfaces

| Interface Name | VRF Name | IP Version | DR Priority | Local Interface |
| -------------- | -------- | ---------- | ----------- | --------------- |
| Ethernet1 | - | IPv4 | - | - |
| Ethernet2 | - | IPv4 | - | - |
| Ethernet3 | - | IPv4 | - | - |
| Ethernet4 | - | IPv4 | - | - |
| Ethernet5 | - | IPv4 | - | - |
| Ethernet6 | - | IPv4 | - | - |

## Filters

### Prefix-lists

#### Prefix-lists Summary

##### PL-LOOPBACKS-EVPN-OVERLAY

| Sequence | Action |
| -------- | ------ |
| 10 | permit 10.0.0.0/24 eq 32 |

#### Prefix-lists Device Configuration

```eos
!
ip prefix-list PL-LOOPBACKS-EVPN-OVERLAY
   seq 10 permit 10.0.0.0/24 eq 32
```

### Route-maps

#### Route-maps Summary

##### RM-CONN-2-BGP

| Sequence | Type | Match | Set | Sub-Route-Map | Continue |
| -------- | ---- | ----- | --- | ------------- | -------- |
| 10 | permit | ip address prefix-list PL-LOOPBACKS-EVPN-OVERLAY | - | - | - |

#### Route-maps Device Configuration

```eos
!
route-map RM-CONN-2-BGP permit 10
   match ip address prefix-list PL-LOOPBACKS-EVPN-OVERLAY
```

## VRF Instances

### VRF Instances Summary

| VRF Name | IP Routing |
| -------- | ---------- |
| MGMT | disabled |

### VRF Instances Device Configuration

```eos
!
vrf instance MGMT
```

## EOS CLI

```eos
!
agent KernelFib environment KERNELFIB_PROGRAM_ALL_ECMP='true'

```
