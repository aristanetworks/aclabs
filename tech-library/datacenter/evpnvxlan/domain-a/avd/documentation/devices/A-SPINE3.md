# A-SPINE3

## Table of Contents

- [Management](#management)
  - [Management Interfaces](#management-interfaces)
  - [DNS Domain](#dns-domain)
  - [IP Name Servers](#ip-name-servers)
  - [Domain Lookup](#domain-lookup)
  - [Clock Settings](#clock-settings)
  - [NTP](#ntp)
  - [Management SSH](#management-ssh)
  - [IP Client Source Interfaces](#ip-client-source-interfaces)
  - [Management API HTTP](#management-api-http)
- [Authentication](#authentication)
  - [Local Users](#local-users)
  - [Enable Password](#enable-password)
  - [AAA Authorization](#aaa-authorization)
- [Spanning Tree](#spanning-tree)
  - [Spanning Tree Summary](#spanning-tree-summary)
  - [Spanning Tree Device Configuration](#spanning-tree-device-configuration)
- [Internal VLAN Allocation Policy](#internal-vlan-allocation-policy)
  - [Internal VLAN Allocation Policy Summary](#internal-vlan-allocation-policy-summary)
  - [Internal VLAN Allocation Policy Device Configuration](#internal-vlan-allocation-policy-device-configuration)
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
  - [Static Routes](#static-routes)
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

## Management

### Management Interfaces

#### Management Interfaces Summary

##### IPv4

| Management Interface | Description | Type | VRF | IP Address | Gateway |
| -------------------- | ----------- | ---- | --- | ---------- | ------- |
| Management0 | OOB_MANAGEMENT | oob | MGMT | 172.100.100.103/24 | 172.100.100.1 |

##### IPv6

| Management Interface | Description | Type | VRF | IPv6 Address | IPv6 Gateway |
| -------------------- | ----------- | ---- | --- | ------------ | ------------ |
| Management0 | OOB_MANAGEMENT | oob | MGMT | - | - |

#### Management Interfaces Device Configuration

```eos
!
interface Management0
   description OOB_MANAGEMENT
   no shutdown
   vrf MGMT
   ip address 172.100.100.103/24
```

### DNS Domain

DNS domain: aclabs.lab

#### DNS Domain Device Configuration

```eos
dns domain aclabs.lab
!
```

### IP Name Servers

#### IP Name Servers Summary

| Name Server | VRF | Priority |
| ----------- | --- | -------- |
| 8.8.8.8 | MGMT | - |

#### IP Name Servers Device Configuration

```eos
ip name-server vrf MGMT 8.8.8.8
```

### Domain Lookup

#### DNS Domain Lookup Summary

| Source interface | vrf |
| ---------------- | --- |
| Management0 | MGMT |

#### DNS Domain Lookup Device Configuration

```eos
ip domain lookup vrf MGMT source-interface Management0
```

### Clock Settings

#### Clock Timezone Settings

Clock Timezone is set to **America/Detroit**.

#### Clock Device Configuration

```eos
!
clock timezone America/Detroit
```

### NTP

#### NTP Summary

##### NTP Local Interface

| Interface | VRF |
| --------- | --- |
| Management0 | MGMT |

##### NTP Servers

| Server | VRF | Preferred | Burst | iBurst | Version | Min Poll | Max Poll | Local-interface | Key |
| ------ | --- | --------- | ----- | ------ | ------- | -------- | -------- | --------------- | --- |
| time.apple.com | MGMT | False | - | True | - | - | - | - | - |
| time.google.com | MGMT | True | - | True | - | - | - | - | - |
| time.windows.com | MGMT | False | - | True | - | - | - | - | - |

#### NTP Device Configuration

```eos
!
ntp local-interface vrf MGMT Management0
ntp server vrf MGMT time.apple.com iburst
ntp server vrf MGMT time.google.com prefer iburst
ntp server vrf MGMT time.windows.com iburst
```

### Management SSH

#### SSH Timeout and Management

| Idle Timeout | SSH Management |
| ------------ | -------------- |
| default | Enabled |

#### Max number of SSH sessions limit and per-host limit

| Connection Limit | Max from a single Host |
| ---------------- | ---------------------- |
| - | - |

#### Ciphers and Algorithms

| Ciphers | Key-exchange methods | MAC algorithms | Hostkey server algorithms |
|---------|----------------------|----------------|---------------------------|
| default | default | default | default |

#### VRFs

| VRF | Status |
| --- | ------ |
| default | Enabled |
| MGMT | Enabled |

#### Management SSH Device Configuration

```eos
!
management ssh
   !
   vrf default
      no shutdown
   !
   vrf MGMT
      no shutdown
```

### IP Client Source Interfaces

| IP Client | VRF | Source Interface Name |
| --------- | --- | --------------------- |
| HTTP | MGMT | Management0 |
| SSH | MGMT | Management0 |

#### IP Client Source Interfaces Device Configuration

```eos
!
ip http client local-interface Management0 vrf MGMT
ip ssh client source-interface Management0 vrf MGMT
 ```

### Management API HTTP

#### Management API HTTP Summary

| HTTP | HTTPS | UNIX-Socket | Default Services |
| ---- | ----- | ----------- | ---------------- |
| False | True | - | - |

#### Management API VRF Access

| VRF Name | IPv4 ACL | IPv6 ACL |
| -------- | -------- | -------- |
| MGMT | - | - |

#### Management API HTTP Device Configuration

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
| arista | 15 | network-admin | False | - |

#### Local Users Device Configuration

```eos
!
username admin privilege 15 role network-admin secret sha512 <removed>
username arista privilege 15 role network-admin secret sha512 <removed>
```

### Enable Password

Enable password has been disabled

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

### Internal VLAN Allocation Policy Device Configuration

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

#### Switchport Default Device Configuration

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

| Interface | Description | Channel Group | IP Address | VRF |  MTU | Shutdown | ACL In | ACL Out |
| --------- | ----------- | ------------- | ---------- | ----| ---- | -------- | ------ | ------- |
| Ethernet1 | P2P_A-LEAF1_Ethernet3 | - | 192.168.0.4/31 | default | 9214 | False | - | - |
| Ethernet2 | P2P_A-LEAF2_Ethernet3 | - | 192.168.0.12/31 | default | 9214 | False | - | - |
| Ethernet3 | P2P_A-LEAF3_Ethernet3 | - | 192.168.0.20/31 | default | 9214 | False | - | - |
| Ethernet4 | P2P_A-LEAF4_Ethernet3 | - | 192.168.0.28/31 | default | 9214 | False | - | - |
| Ethernet5 | P2P_A-LEAF5_Ethernet3 | - | 192.168.0.36/31 | default | 9214 | False | - | - |
| Ethernet6 | P2P_A-LEAF6_Ethernet3 | - | 192.168.0.44/31 | default | 9214 | False | - | - |
| Ethernet7 | P2P_A-LEAF7_Ethernet3 | - | 192.168.0.52/31 | default | 9214 | False | - | - |
| Ethernet8 | P2P_A-LEAF8_Ethernet3 | - | 192.168.0.60/31 | default | 9214 | False | - | - |

#### Ethernet Interfaces Device Configuration

```eos
!
interface Ethernet1
   description P2P_A-LEAF1_Ethernet3
   no shutdown
   mtu 9214
   no switchport
   ip address 192.168.0.4/31
   pim ipv4 sparse-mode
!
interface Ethernet2
   description P2P_A-LEAF2_Ethernet3
   no shutdown
   mtu 9214
   no switchport
   ip address 192.168.0.12/31
   pim ipv4 sparse-mode
!
interface Ethernet3
   description P2P_A-LEAF3_Ethernet3
   no shutdown
   mtu 9214
   no switchport
   ip address 192.168.0.20/31
   pim ipv4 sparse-mode
!
interface Ethernet4
   description P2P_A-LEAF4_Ethernet3
   no shutdown
   mtu 9214
   no switchport
   ip address 192.168.0.28/31
   pim ipv4 sparse-mode
!
interface Ethernet5
   description P2P_A-LEAF5_Ethernet3
   no shutdown
   mtu 9214
   no switchport
   ip address 192.168.0.36/31
   pim ipv4 sparse-mode
!
interface Ethernet6
   description P2P_A-LEAF6_Ethernet3
   no shutdown
   mtu 9214
   no switchport
   ip address 192.168.0.44/31
   pim ipv4 sparse-mode
!
interface Ethernet7
   description P2P_A-LEAF7_Ethernet3
   no shutdown
   mtu 9214
   no switchport
   ip address 192.168.0.52/31
   pim ipv4 sparse-mode
!
interface Ethernet8
   description P2P_A-LEAF8_Ethernet3
   no shutdown
   mtu 9214
   no switchport
   ip address 192.168.0.60/31
   pim ipv4 sparse-mode
```

### Loopback Interfaces

#### Loopback Interfaces Summary

##### IPv4

| Interface | Description | VRF | IP Address |
| --------- | ----------- | --- | ---------- |
| Loopback0 | Globally Unique Address | default | 1.1.1.203/32 |

##### IPv6

| Interface | Description | VRF | IPv6 Address |
| --------- | ----------- | --- | ------------ |
| Loopback0 | Globally Unique Address | default | - |

#### Loopback Interfaces Device Configuration

```eos
!
interface Loopback0
   description Globally Unique Address
   no shutdown
   ip address 1.1.1.203/32
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

### Static Routes

#### Static Routes Summary

| VRF | Destination Prefix | Next Hop IP | Exit interface | Administrative Distance | Tag | Route Name | Metric |
| --- | ------------------ | ----------- | -------------- | ----------------------- | --- | ---------- | ------ |
| MGMT | 0.0.0.0/0 | 172.100.100.1 | - | 1 | - | - | - |

#### Static Routes Device Configuration

```eos
!
ip route vrf MGMT 0.0.0.0/0 172.100.100.1
```

### ARP

Global ARP timeout: 1500

#### ARP Device Configuration

```eos
!
arp aging timeout default 1500
```

### Router BGP

ASN Notation: asplain

#### Router BGP Summary

| BGP AS | Router ID |
| ------ | --------- |
| 65100 | 1.1.1.203 |

| BGP Tuning |
| ---------- |
| graceful-restart restart-time 300 |
| graceful-restart |
| update wait-install |
| no bgp default ipv4-unicast |
| distance bgp 20 200 200 |
| maximum-paths 4 ecmp 4 |

#### Router BGP Peer Groups

##### LOCAL-EVPN-PEERS

| Settings | Value |
| -------- | ----- |
| Address Family | evpn |
| Next-hop unchanged | True |
| Source | Loopback0 |
| BFD | True |
| Ebgp multihop | 3 |
| Send community | all |
| Maximum routes | 0 (no limit) |

##### LOCAL-IPV4-PEERS

| Settings | Value |
| -------- | ----- |
| Address Family | ipv4 |
| Send community | all |
| Maximum routes | 12000 |

#### BGP Neighbors

| Neighbor | Remote AS | VRF | Shutdown | Send-community | Maximum-routes | Allowas-in | BFD | RIB Pre-Policy Retain | Route-Reflector Client | Passive | TTL Max Hops |
| -------- | --------- | --- | -------- | -------------- | -------------- | ---------- | --- | --------------------- | ---------------------- | ------- | ------------ |
| 1.1.1.1 | 65112 | default | - | Inherited from peer group LOCAL-EVPN-PEERS | Inherited from peer group LOCAL-EVPN-PEERS | - | Inherited from peer group LOCAL-EVPN-PEERS | - | - | - | - |
| 1.1.1.2 | 65112 | default | - | Inherited from peer group LOCAL-EVPN-PEERS | Inherited from peer group LOCAL-EVPN-PEERS | - | Inherited from peer group LOCAL-EVPN-PEERS | - | - | - | - |
| 1.1.1.3 | 65134 | default | - | Inherited from peer group LOCAL-EVPN-PEERS | Inherited from peer group LOCAL-EVPN-PEERS | - | Inherited from peer group LOCAL-EVPN-PEERS | - | - | - | - |
| 1.1.1.4 | 65134 | default | - | Inherited from peer group LOCAL-EVPN-PEERS | Inherited from peer group LOCAL-EVPN-PEERS | - | Inherited from peer group LOCAL-EVPN-PEERS | - | - | - | - |
| 1.1.1.5 | 65156 | default | - | Inherited from peer group LOCAL-EVPN-PEERS | Inherited from peer group LOCAL-EVPN-PEERS | - | Inherited from peer group LOCAL-EVPN-PEERS | - | - | - | - |
| 1.1.1.6 | 65156 | default | - | Inherited from peer group LOCAL-EVPN-PEERS | Inherited from peer group LOCAL-EVPN-PEERS | - | Inherited from peer group LOCAL-EVPN-PEERS | - | - | - | - |
| 1.1.1.7 | 65178 | default | - | Inherited from peer group LOCAL-EVPN-PEERS | Inherited from peer group LOCAL-EVPN-PEERS | - | Inherited from peer group LOCAL-EVPN-PEERS | - | - | - | - |
| 1.1.1.8 | 65178 | default | - | Inherited from peer group LOCAL-EVPN-PEERS | Inherited from peer group LOCAL-EVPN-PEERS | - | Inherited from peer group LOCAL-EVPN-PEERS | - | - | - | - |
| 192.168.0.5 | 65112 | default | - | Inherited from peer group LOCAL-IPV4-PEERS | Inherited from peer group LOCAL-IPV4-PEERS | - | - | - | - | - | - |
| 192.168.0.13 | 65112 | default | - | Inherited from peer group LOCAL-IPV4-PEERS | Inherited from peer group LOCAL-IPV4-PEERS | - | - | - | - | - | - |
| 192.168.0.21 | 65134 | default | - | Inherited from peer group LOCAL-IPV4-PEERS | Inherited from peer group LOCAL-IPV4-PEERS | - | - | - | - | - | - |
| 192.168.0.29 | 65134 | default | - | Inherited from peer group LOCAL-IPV4-PEERS | Inherited from peer group LOCAL-IPV4-PEERS | - | - | - | - | - | - |
| 192.168.0.37 | 65156 | default | - | Inherited from peer group LOCAL-IPV4-PEERS | Inherited from peer group LOCAL-IPV4-PEERS | - | - | - | - | - | - |
| 192.168.0.45 | 65156 | default | - | Inherited from peer group LOCAL-IPV4-PEERS | Inherited from peer group LOCAL-IPV4-PEERS | - | - | - | - | - | - |
| 192.168.0.53 | 65178 | default | - | Inherited from peer group LOCAL-IPV4-PEERS | Inherited from peer group LOCAL-IPV4-PEERS | - | - | - | - | - | - |
| 192.168.0.61 | 65178 | default | - | Inherited from peer group LOCAL-IPV4-PEERS | Inherited from peer group LOCAL-IPV4-PEERS | - | - | - | - | - | - |

#### Router BGP EVPN Address Family

##### EVPN Peer Groups

| Peer Group | Activate | Route-map In | Route-map Out | Encapsulation | Next-hop-self Source Interface |
| ---------- | -------- | ------------ | ------------- | ------------- | ------------------------------ |
| LOCAL-EVPN-PEERS | True |  - | - | default | - |

#### Router BGP Device Configuration

```eos
!
router bgp 65100
   router-id 1.1.1.203
   update wait-install
   no bgp default ipv4-unicast
   distance bgp 20 200 200
   graceful-restart restart-time 300
   graceful-restart
   maximum-paths 4 ecmp 4
   neighbor LOCAL-EVPN-PEERS peer group
   neighbor LOCAL-EVPN-PEERS next-hop-unchanged
   neighbor LOCAL-EVPN-PEERS update-source Loopback0
   neighbor LOCAL-EVPN-PEERS bfd
   neighbor LOCAL-EVPN-PEERS ebgp-multihop 3
   neighbor LOCAL-EVPN-PEERS password 7 <removed>
   neighbor LOCAL-EVPN-PEERS send-community
   neighbor LOCAL-EVPN-PEERS maximum-routes 0
   neighbor LOCAL-IPV4-PEERS peer group
   neighbor LOCAL-IPV4-PEERS password 7 <removed>
   neighbor LOCAL-IPV4-PEERS send-community
   neighbor LOCAL-IPV4-PEERS maximum-routes 12000
   neighbor 1.1.1.1 peer group LOCAL-EVPN-PEERS
   neighbor 1.1.1.1 remote-as 65112
   neighbor 1.1.1.1 description A-LEAF1_Loopback0
   neighbor 1.1.1.2 peer group LOCAL-EVPN-PEERS
   neighbor 1.1.1.2 remote-as 65112
   neighbor 1.1.1.2 description A-LEAF2_Loopback0
   neighbor 1.1.1.3 peer group LOCAL-EVPN-PEERS
   neighbor 1.1.1.3 remote-as 65134
   neighbor 1.1.1.3 description A-LEAF3_Loopback0
   neighbor 1.1.1.4 peer group LOCAL-EVPN-PEERS
   neighbor 1.1.1.4 remote-as 65134
   neighbor 1.1.1.4 description A-LEAF4_Loopback0
   neighbor 1.1.1.5 peer group LOCAL-EVPN-PEERS
   neighbor 1.1.1.5 remote-as 65156
   neighbor 1.1.1.5 description A-LEAF5_Loopback0
   neighbor 1.1.1.6 peer group LOCAL-EVPN-PEERS
   neighbor 1.1.1.6 remote-as 65156
   neighbor 1.1.1.6 description A-LEAF6_Loopback0
   neighbor 1.1.1.7 peer group LOCAL-EVPN-PEERS
   neighbor 1.1.1.7 remote-as 65178
   neighbor 1.1.1.7 description A-LEAF7_Loopback0
   neighbor 1.1.1.8 peer group LOCAL-EVPN-PEERS
   neighbor 1.1.1.8 remote-as 65178
   neighbor 1.1.1.8 description A-LEAF8_Loopback0
   neighbor 192.168.0.5 peer group LOCAL-IPV4-PEERS
   neighbor 192.168.0.5 remote-as 65112
   neighbor 192.168.0.5 description A-LEAF1_Ethernet3
   neighbor 192.168.0.13 peer group LOCAL-IPV4-PEERS
   neighbor 192.168.0.13 remote-as 65112
   neighbor 192.168.0.13 description A-LEAF2_Ethernet3
   neighbor 192.168.0.21 peer group LOCAL-IPV4-PEERS
   neighbor 192.168.0.21 remote-as 65134
   neighbor 192.168.0.21 description A-LEAF3_Ethernet3
   neighbor 192.168.0.29 peer group LOCAL-IPV4-PEERS
   neighbor 192.168.0.29 remote-as 65134
   neighbor 192.168.0.29 description A-LEAF4_Ethernet3
   neighbor 192.168.0.37 peer group LOCAL-IPV4-PEERS
   neighbor 192.168.0.37 remote-as 65156
   neighbor 192.168.0.37 description A-LEAF5_Ethernet3
   neighbor 192.168.0.45 peer group LOCAL-IPV4-PEERS
   neighbor 192.168.0.45 remote-as 65156
   neighbor 192.168.0.45 description A-LEAF6_Ethernet3
   neighbor 192.168.0.53 peer group LOCAL-IPV4-PEERS
   neighbor 192.168.0.53 remote-as 65178
   neighbor 192.168.0.53 description A-LEAF7_Ethernet3
   neighbor 192.168.0.61 peer group LOCAL-IPV4-PEERS
   neighbor 192.168.0.61 remote-as 65178
   neighbor 192.168.0.61 description A-LEAF8_Ethernet3
   redistribute connected route-map RM-CONN-2-BGP
   !
   address-family evpn
      neighbor LOCAL-EVPN-PEERS activate
   !
   address-family ipv4
      no neighbor LOCAL-EVPN-PEERS activate
      neighbor LOCAL-IPV4-PEERS activate
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

#### PIM Sparse Mode Enabled Interfaces

| Interface Name | VRF Name | IP Version | Border Router | DR Priority | Local Interface |
| -------------- | -------- | ---------- | ------------- | ----------- | --------------- |
| Ethernet1 | - | IPv4 | - | - | - |
| Ethernet2 | - | IPv4 | - | - | - |
| Ethernet3 | - | IPv4 | - | - | - |
| Ethernet4 | - | IPv4 | - | - | - |
| Ethernet5 | - | IPv4 | - | - | - |
| Ethernet6 | - | IPv4 | - | - | - |
| Ethernet7 | - | IPv4 | - | - | - |
| Ethernet8 | - | IPv4 | - | - | - |

## Filters

### Prefix-lists

#### Prefix-lists Summary

##### PL-LOOPBACKS-EVPN-OVERLAY

| Sequence | Action |
| -------- | ------ |
| 10 | permit 1.1.1.0/24 eq 32 |

#### Prefix-lists Device Configuration

```eos
!
ip prefix-list PL-LOOPBACKS-EVPN-OVERLAY
   seq 10 permit 1.1.1.0/24 eq 32
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
