# campus-spine1

## Table of Contents

- [Management](#management)
  - [Banner](#banner)
  - [Management Interfaces](#management-interfaces)
  - [DNS Domain](#dns-domain)
  - [IP Name Servers](#ip-name-servers)
  - [Clock Settings](#clock-settings)
  - [NTP](#ntp)
  - [Management API HTTP](#management-api-http)
- [Authentication](#authentication)
  - [Local Users](#local-users)
  - [Enable Password](#enable-password)
  - [AAA Authorization](#aaa-authorization)
- [Monitoring](#monitoring)
  - [TerminAttr Daemon](#terminattr-daemon)
  - [SFlow](#sflow)
- [MLAG](#mlag)
  - [MLAG Summary](#mlag-summary)
  - [MLAG Device Configuration](#mlag-device-configuration)
- [Spanning Tree](#spanning-tree)
  - [Spanning Tree Summary](#spanning-tree-summary)
  - [Spanning Tree Device Configuration](#spanning-tree-device-configuration)
- [Internal VLAN Allocation Policy](#internal-vlan-allocation-policy)
  - [Internal VLAN Allocation Policy Summary](#internal-vlan-allocation-policy-summary)
  - [Internal VLAN Allocation Policy Device Configuration](#internal-vlan-allocation-policy-device-configuration)
- [VLANs](#vlans)
  - [VLANs Summary](#vlans-summary)
  - [VLANs Device Configuration](#vlans-device-configuration)
- [Interfaces](#interfaces)
  - [Ethernet Interfaces](#ethernet-interfaces)
  - [Port-Channel Interfaces](#port-channel-interfaces)
  - [Loopback Interfaces](#loopback-interfaces)
  - [VLAN Interfaces](#vlan-interfaces)
- [Routing](#routing)
  - [Service Routing Protocols Model](#service-routing-protocols-model)
  - [Virtual Router MAC Address](#virtual-router-mac-address)
  - [IP Routing](#ip-routing)
  - [IPv6 Routing](#ipv6-routing)
  - [Static Routes](#static-routes)
  - [Router OSPF](#router-ospf)
  - [Router BGP](#router-bgp)
- [Multicast](#multicast)
  - [IP IGMP Snooping](#ip-igmp-snooping)
- [Filters](#filters)
  - [Prefix-lists](#prefix-lists)
  - [Route-maps](#route-maps)
- [VRF Instances](#vrf-instances)
  - [VRF Instances Summary](#vrf-instances-summary)
  - [VRF Instances Device Configuration](#vrf-instances-device-configuration)

## Management

### Banner

#### MOTD Banner

```text
0 to Hero network
EOF
```

### Management Interfaces

#### Management Interfaces Summary

##### IPv4

| Management Interface | Description | Type | VRF | IP Address | Gateway |
| -------------------- | ----------- | ---- | --- | ---------- | ------- |
| Management1 | OOB_MANAGEMENT | oob | MGMT | 192.168.0.30/24 | 192.168.0.1 |

##### IPv6

| Management Interface | Description | Type | VRF | IPv6 Address | IPv6 Gateway | ND RA Disabled | ND RA RX Accept | ND Managed Config Flag | ND Other Config Flag | ND Cache | ND RA DNS Servers |
| -------------------- | ----------- | ---- | --- | ------------ | ------------ | -------------- | --------------- | ---------------------- | -------------------- | -------- | ----------------- |
| Management1 | OOB_MANAGEMENT | oob | MGMT | - | - | - | - | - | - | - | - |

#### Management Interfaces Device Configuration

```eos
!
interface Management1
   description OOB_MANAGEMENT
   no shutdown
   vrf MGMT
   ip address 192.168.0.30/24
```

### DNS Domain

DNS domain: demo.lab

#### DNS Domain Device Configuration

```eos
dns domain demo.lab
!
```

### IP Name Servers

#### IP Name Servers Summary

| Name Server | VRF | Priority |
| ----------- | --- | -------- |
| 8.8.8.8 | MGMT | - |
| 8.8.4.4 | MGMT | - |

#### IP Name Servers Device Configuration

```eos
ip name-server vrf MGMT 8.8.4.4
ip name-server vrf MGMT 8.8.8.8
```

### Clock Settings

#### Clock Timezone Settings

Clock Timezone is set to **EST**.

#### Clock Device Configuration

```eos
!
clock timezone EST
```

### NTP

#### NTP Summary

##### NTP Local Interface

| Interface | VRF |
| --------- | --- |
| Management1 | MGMT |

##### NTP Servers

NTP servers VRF: MGMT

| Server | Preferred | Burst | iBurst | Version | Min Poll | Max Poll | Local-interface | Source Address | Key |
| ------ | --------- | ----- | ------ | ------- | -------- | -------- | --------------- | -------------- | --- |
| 0.north-america.pool.ntp.org | True | - | - | - | - | - | - | - | - |
| 1.north-america.pool.ntp.org | - | - | - | - | - | - | - | - | - |

#### NTP Device Configuration

```eos
!
ntp local-interface vrf MGMT Management1
ntp server vrf MGMT 0.north-america.pool.ntp.org prefer
ntp server vrf MGMT 1.north-america.pool.ntp.org
```

### Management API HTTP

#### Management API HTTP Summary

| HTTP | HTTPS | UNIX-Socket | Default Services | Session Timeout |
| ---- | ----- | ----------- | ---------------- | --------------- |
| False | True | - | - | 1440 minutes |

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
| cvpadmin | 15 | network-admin | False | - |

#### Local Users Device Configuration

```eos
!
username cvpadmin privilege 15 role network-admin secret sha512 <removed>
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

## Monitoring

### TerminAttr Daemon

#### TerminAttr Daemon Summary

| CV Compression | CloudVision Servers | VRF | Authentication | Smash Excludes | Ingest Exclude | Bypass AAA |
| -------------- | ------------------- | --- | -------------- | -------------- | -------------- | ---------- |
| gzip | apiserver.arista.io:443 | MGMT | token-secure,/tmp/cv-onboarding-token | ale,flexCounter,hardware,kni,pulse,strata | - | True |

#### TerminAttr Daemon Device Configuration

```eos
!
daemon TerminAttr
   exec /usr/bin/TerminAttr -cvaddr=apiserver.arista.io:443 -cvauth=token-secure,/tmp/cv-onboarding-token -cvvrf=MGMT -disableaaa -smashexcludes=ale,flexCounter,hardware,kni,pulse,strata -taillogs -sflowaddr=default/127.0.0.1:6343 -cvsourceintf=Management1
   no shutdown
```

### SFlow

#### SFlow Summary

| VRF | SFlow Source | SFlow Destination | Port |
| --- | ------------ | ----------------- | ---- |
| default | - | 127.0.0.1 | 6343 |
| default | Loopback0 | - | - |

sFlow Sample Rate: 10

sFlow Polling Interval: 50

sFlow is enabled.

#### SFlow Interfaces

| Interface | Ingress Enabled | Egress Enabled |
| --------- | --------------- | -------------- |
| Port-Channel11 | True | - |
| Port-Channel13 | True | - |
| Port-Channel15 | True | - |
| Port-Channel21 | True | - |

#### SFlow Device Configuration

```eos
!
sflow sample 10
sflow polling-interval 50
sflow destination 127.0.0.1 6343
sflow source-interface Loopback0
sflow run
```

## MLAG

### MLAG Summary

| Domain-id | Local-interface | Peer-address | Peer-link |
| --------- | --------------- | ------------ | --------- |
| SPINES | Vlan4094 | 10.101.255.1 | Port-Channel21 |

Dual primary detection is enabled. The detection delay is 5 seconds.

### MLAG Device Configuration

```eos
!
mlag configuration
   domain-id SPINES
   local-interface Vlan4094
   peer-address 10.101.255.1
   peer-address heartbeat 192.168.0.31 vrf MGMT
   peer-link Port-Channel21
   dual-primary detection delay 5 action errdisable all-interfaces
   reload-delay mlag 300
   reload-delay non-mlag 330
```

## Spanning Tree

### Spanning Tree Summary

STP mode: **mstp**

#### MSTP Instance and Priority

| Instance(s) | Priority |
| -------- | -------- |
| 0 | 4096 |

#### Global Spanning-Tree Settings

- Spanning Tree disabled for VLANs: **4093-4094**

### Spanning Tree Device Configuration

```eos
!
spanning-tree mode mstp
no spanning-tree vlan-id 4093-4094
spanning-tree mst 0 priority 4096
```

## Internal VLAN Allocation Policy

### Internal VLAN Allocation Policy Summary

| Policy Allocation | Range Beginning | Range Ending |
| ----------------- | --------------- | ------------ |
| ascending | 1006 | 1199 |

### Internal VLAN Allocation Policy Device Configuration

```eos
!
vlan internal order ascending range 1006 1199
```

## VLANs

### VLANs Summary

| VLAN ID | Name | Trunk Groups |
| ------- | ---- | ------------ |
| 1000 | DC_edge_Blue | - |
| 1001 | DC_edge_Green | - |
| 1110 | vlan_1110 | - |
| 1120 | vlan_1120 | - |
| 4093 | MLAG_L3 | MLAG |
| 4094 | MLAG | MLAG |

### VLANs Device Configuration

```eos
!
vlan 1000
   name DC_edge_Blue
!
vlan 1001
   name DC_edge_Green
!
vlan 1110
   name vlan_1110
!
vlan 1120
   name vlan_1120
!
vlan 4093
   name MLAG_L3
   trunk group MLAG
!
vlan 4094
   name MLAG
   trunk group MLAG
```

## Interfaces

### Ethernet Interfaces

#### Ethernet Interfaces Summary

##### L2

| Interface | Description | Mode | VLANs | Native VLAN | Trunk Group | Channel-Group |
| --------- | ----------- | ---- | ----- | ----------- | ----------- | ------------- |
| Ethernet1/1 | L2_campus-brdr1_Ethernet49/1 | *trunk | *1000-1001,1110,1120 | *- | *- | 11 |
| Ethernet1/2 | L2_campus-brdr2_Ethernet49/1 | *trunk | *1000-1001,1110,1120 | *- | *- | 11 |
| Ethernet1/3 | L2_campus-leaf1_Ethernet49 | *trunk | *1110,1120 | *- | *- | 13 |
| Ethernet1/4 | L2_campus-leaf2_Ethernet49 | *trunk | *1110,1120 | *- | *- | 13 |
| Ethernet1/5 | L2_campus-leaf3_Ethernet49 | *trunk | *1110,1120 | *- | *- | 15 |
| Ethernet1/6 | L2_campus-leaf4_Ethernet49 | *trunk | *1110,1120 | *- | *- | 15 |
| Ethernet2/1 | MLAG_campus-spine2_Ethernet2/1 | *trunk | *- | *- | *MLAG | 21 |
| Ethernet2/2 | MLAG_campus-spine2_Ethernet2/2 | *trunk | *- | *- | *MLAG | 21 |

*Inherited from Port-Channel Interface

#### Ethernet Interfaces Device Configuration

```eos
!
interface Ethernet1/1
   description L2_campus-brdr1_Ethernet49/1
   no shutdown
   channel-group 11 mode active
!
interface Ethernet1/2
   description L2_campus-brdr2_Ethernet49/1
   no shutdown
   channel-group 11 mode active
!
interface Ethernet1/3
   description L2_campus-leaf1_Ethernet49
   no shutdown
   channel-group 13 mode active
!
interface Ethernet1/4
   description L2_campus-leaf2_Ethernet49
   no shutdown
   channel-group 13 mode active
!
interface Ethernet1/5
   description L2_campus-leaf3_Ethernet49
   no shutdown
   channel-group 15 mode active
!
interface Ethernet1/6
   description L2_campus-leaf4_Ethernet49
   no shutdown
   channel-group 15 mode active
!
interface Ethernet2/1
   description MLAG_campus-spine2_Ethernet2/1
   no shutdown
   channel-group 21 mode active
!
interface Ethernet2/2
   description MLAG_campus-spine2_Ethernet2/2
   no shutdown
   channel-group 21 mode active
```

### Port-Channel Interfaces

#### Port-Channel Interfaces Summary

##### L2

| Interface | Description | Mode | VLANs | Native VLAN | Trunk Group | LACP Fallback Timeout | LACP Fallback Mode | MLAG ID | EVPN ESI |
| --------- | ----------- | ---- | ----- | ----------- | ----------- | --------------------- | ------------------ | ------- | -------- |
| Port-Channel11 | L2_BORDER_POD_Port-Channel491 | trunk | 1000-1001,1110,1120 | - | - | - | - | 11 | - |
| Port-Channel13 | L2_POD1_Port-Channel49 | trunk | 1110,1120 | - | - | - | - | 13 | - |
| Port-Channel15 | L2_POD2_Port-Channel49 | trunk | 1110,1120 | - | - | - | - | 15 | - |
| Port-Channel21 | MLAG_campus-spine2_Port-Channel21 | trunk | - | - | MLAG | - | - | - | - |

#### Port-Channel Interfaces Device Configuration

```eos
!
interface Port-Channel11
   description L2_BORDER_POD_Port-Channel491
   no shutdown
   switchport trunk allowed vlan 1000-1001,1110,1120
   switchport mode trunk
   switchport
   mlag 11
   sflow enable
!
interface Port-Channel13
   description L2_POD1_Port-Channel49
   no shutdown
   switchport trunk allowed vlan 1110,1120
   switchport mode trunk
   switchport
   mlag 13
   sflow enable
!
interface Port-Channel15
   description L2_POD2_Port-Channel49
   no shutdown
   switchport trunk allowed vlan 1110,1120
   switchport mode trunk
   switchport
   mlag 15
   sflow enable
!
interface Port-Channel21
   description MLAG_campus-spine2_Port-Channel21
   no shutdown
   switchport mode trunk
   switchport trunk group MLAG
   switchport
   sflow enable
```

### Loopback Interfaces

#### Loopback Interfaces Summary

##### IPv4

| Interface | Description | VRF | IP Address |
| --------- | ----------- | --- | ---------- |
| Loopback0 | ROUTER_ID | default | 10.98.1.129/32 |

##### IPv6

| Interface | Description | VRF | IPv6 Addresses |
| --------- | ----------- | --- | -------------- |
| Loopback0 | ROUTER_ID | default | - |

#### Loopback Interfaces Device Configuration

```eos
!
interface Loopback0
   description ROUTER_ID
   no shutdown
   ip address 10.98.1.129/32
   ip ospf area 0.0.0.0
```

### VLAN Interfaces

#### VLAN Interfaces Summary

| Interface | Description | VRF | MTU | Shutdown |
| --------- | ----------- | --- | --- | -------- |
| Vlan1000 | DC_edge_Blue | default | - | False |
| Vlan1001 | DC_edge_Green | default | - | False |
| Vlan1110 | vlan_1110 | default | - | False |
| Vlan1120 | vlan_1120 | default | - | False |
| Vlan4093 | MLAG_L3 | default | 1500 | False |
| Vlan4094 | MLAG | default | 1500 | False |

##### IPv4

| Interface | VRF | IP Address | IP Address Virtual | IP Router Virtual Address | ACL In | ACL Out |
| --------- | --- | ---------- | ------------------ | ------------------------- | ------ | ------- |
| Vlan1000 | default | 172.16.254.2/29 | - | 172.16.254.1 | - | - |
| Vlan1001 | default | 172.16.254.10/29 | - | 172.16.254.9 | - | - |
| Vlan1110 | default | 10.10.110.2/24 | - | 10.10.110.1 | - | - |
| Vlan1120 | default | 10.10.120.2/24 | - | 10.10.120.1 | - | - |
| Vlan4093 | default | 10.101.254.0/31 | - | - | - | - |
| Vlan4094 | default | 10.101.255.0/31 | - | - | - | - |

##### OSPF

| Interface | OSPF Network Point to Point | OSPF Area | OSPF Cost | OSPF Authentication | IPv6 OSPF Process ID | IPv6 OSPF Area | IPv6 OSPF Network Point to Point |
| --------- | --------------------------- | --------- | --------- | ------------------- | -------------------- | -------------- | -------------------------------- |
| Vlan4093 | True | 0.0.0.0 | - | - | - | - | - |

#### VLAN Interfaces Device Configuration

```eos
!
interface Vlan1000
   description DC_edge_Blue
   no shutdown
   ip address 172.16.254.2/29
   ip virtual-router address 172.16.254.1
!
interface Vlan1001
   description DC_edge_Green
   no shutdown
   ip address 172.16.254.10/29
   ip virtual-router address 172.16.254.9
!
interface Vlan1110
   description vlan_1110
   no shutdown
   ip address 10.10.110.2/24
   ip virtual-router address 10.10.110.1
!
interface Vlan1120
   description vlan_1120
   no shutdown
   ip address 10.10.120.2/24
   ip virtual-router address 10.10.120.1
!
interface Vlan4093
   description MLAG_L3
   no shutdown
   mtu 1500
   ip address 10.101.254.0/31
   ip ospf network point-to-point
   ip ospf area 0.0.0.0
!
interface Vlan4094
   description MLAG
   no shutdown
   mtu 1500
   no autostate
   ip address 10.101.255.0/31
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

Virtual Router MAC Address: 00:1c:73:00:00:98

#### Virtual Router MAC Address Device Configuration

```eos
!
ip virtual-router mac-address 00:1c:73:00:00:98
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
| MGMT | 0.0.0.0/0 | 192.168.0.1 | - | 1 | - | - | - |

#### Static Routes Device Configuration

```eos
!
ip route vrf MGMT 0.0.0.0/0 192.168.0.1
```

### Router OSPF

#### Router OSPF Summary

| Process ID | Router ID | Default Passive Interface | No Passive Interface | BFD | Max LSA | Default Information Originate | Log Adjacency Changes Detail | Auto Cost Reference Bandwidth | Maximum Paths | MPLS LDP Sync Default | Distribute List In |
| ---------- | --------- | ------------------------- | -------------------- | --- | ------- | ----------------------------- | ---------------------------- | ----------------------------- | ------------- | --------------------- | ------------------ |
| 100 | 10.98.1.129 | enabled | Vlan4093 | disabled | 12000 | disabled | disabled | - | - | - | - |

#### Router OSPF Router Redistribution

| Process ID | Source Protocol | Include Leaked | Route Map |
| ---------- | --------------- | -------------- | --------- |
| 100 | connected | disabled | - |

#### OSPF Interfaces

| Interface | Area | Cost | Point To Point |
| -------- | -------- | -------- | -------- |
| Vlan4093 | 0.0.0.0 | - | True |
| Loopback0 | 0.0.0.0 | - | - |

#### Router OSPF Device Configuration

```eos
!
router ospf 100
   router-id 10.98.1.129
   passive-interface default
   no passive-interface Vlan4093
   redistribute connected
   max-lsa 12000
   graceful-restart
```

### Router BGP

ASN Notation: asplain

#### Router BGP Summary

| BGP AS | Router ID |
| ------ | --------- |
| 63000 | 10.98.1.129 |

| BGP Tuning |
| ---------- |
| graceful-restart restart-time 300 |
| graceful-restart |
| no bgp default ipv4-unicast |
| distance bgp 20 200 200 |
| maximum-paths 4 |

#### BGP Neighbors

| Neighbor | Remote AS | VRF | Shutdown | Send-community | Maximum-routes | Allowas-in | BFD | RIB Pre-Policy Retain | Route-Reflector Client | Passive | TTL Max Hops |
| -------- | --------- | --- | -------- | -------------- | -------------- | ---------- | --- | --------------------- | ---------------------- | ------- | ------------ |
| 172.16.254.5 | 65103 | default | - | - | - | - | - | - | - | - | - |
| 172.16.254.6 | 65103 | default | - | - | - | - | - | - | - | - | - |
| 172.16.254.13 | 65103 | default | - | - | - | - | - | - | - | - | - |
| 172.16.254.14 | 65103 | default | - | - | - | - | - | - | - | - | - |

#### Router BGP VRFs

| VRF | Route-Distinguisher | Redistribute | Graceful Restart |
| --- | ------------------- | ------------ | ---------------- |
| default | - | connected<br>ospf | - |

#### Router BGP Device Configuration

```eos
!
router bgp 63000
   router-id 10.98.1.129
   no bgp default ipv4-unicast
   distance bgp 20 200 200
   graceful-restart restart-time 300
   graceful-restart
   maximum-paths 4
   neighbor 172.16.254.5 remote-as 65103
   neighbor 172.16.254.5 next-hop-self
   neighbor 172.16.254.6 remote-as 65103
   neighbor 172.16.254.6 next-hop-self
   neighbor 172.16.254.13 remote-as 65103
   neighbor 172.16.254.13 next-hop-self
   neighbor 172.16.254.14 remote-as 65103
   neighbor 172.16.254.14 next-hop-self
   !
   address-family ipv4
      neighbor 172.16.254.5 activate
      neighbor 172.16.254.6 activate
      neighbor 172.16.254.13 activate
      neighbor 172.16.254.14 activate
   !
   vrf default
      redistribute connected
      redistribute ospf
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

##### PL-CAMPUS-NETWORK

| Sequence | Action |
| -------- | ------ |
| 10 | permit 10.10.110.0/24 |
| 20 | permit 10.10.120.0/24 |

#### Prefix-lists Device Configuration

```eos
!
ip prefix-list PL-CAMPUS-NETWORK
   seq 10 permit 10.10.110.0/24
   seq 20 permit 10.10.120.0/24
```

### Route-maps

#### Route-maps Summary

##### RM-CAMPUS-RT-OUT

| Sequence | Type | Match | Set | Sub-Route-Map | Continue |
| -------- | ---- | ----- | --- | ------------- | -------- |
| 10 | permit | ip address prefix-list PL-CAMPUS-NETWORK | - | - | - |

#### Route-maps Device Configuration

```eos
!
route-map RM-CAMPUS-RT-OUT permit 10
   match ip address prefix-list PL-CAMPUS-NETWORK
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
