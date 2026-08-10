# dc1-brdr2

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
  - [VXLAN Interface](#vxlan-interface)
- [Routing](#routing)
  - [Service Routing Protocols Model](#service-routing-protocols-model)
  - [Virtual Router MAC Address](#virtual-router-mac-address)
  - [IP Routing](#ip-routing)
  - [IPv6 Routing](#ipv6-routing)
  - [Static Routes](#static-routes)
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
| Management1 | OOB_MANAGEMENT | oob | MGMT | 192.168.0.101/24 | 192.168.0.1 |

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
   ip address 192.168.0.101/24
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
| Ethernet47 | True | - |
| Ethernet48 | True | - |
| Ethernet49/1 | True | - |
| Ethernet50/1 | True | - |
| Port-Channel511 | True | - |

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
| DC1_BORDER_LEAF1 | Vlan4094 | 10.101.255.0 | Port-Channel511 |

Dual primary detection is enabled. The detection delay is 5 seconds.

### MLAG Device Configuration

```eos
!
mlag configuration
   domain-id DC1_BORDER_LEAF1
   local-interface Vlan4094
   peer-address 10.101.255.0
   peer-address heartbeat 192.168.0.100 vrf MGMT
   peer-link Port-Channel511
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
| 100 | BLUE_VLAN_100 | - |
| 102 | BLUE_VLAN_102 | - |
| 200 | GREEN_VLAN_200 | - |
| 1000 | DC_edge_Blue | - |
| 1001 | DC_edge_Green | - |
| 3500 | MLAG_L3_VRF_BLUE | MLAG |
| 3501 | MLAG_L3_VRF_GREEN | MLAG |
| 4093 | MLAG_L3 | MLAG |
| 4094 | MLAG | MLAG |

### VLANs Device Configuration

```eos
!
vlan 100
   name BLUE_VLAN_100
!
vlan 102
   name BLUE_VLAN_102
!
vlan 200
   name GREEN_VLAN_200
!
vlan 1000
   name DC_edge_Blue
!
vlan 1001
   name DC_edge_Green
!
vlan 3500
   name MLAG_L3_VRF_BLUE
   trunk group MLAG
!
vlan 3501
   name MLAG_L3_VRF_GREEN
   trunk group MLAG
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
| Ethernet47 | campus-brdr2 | trunk | 1000-1001 | - | - | - |
| Ethernet51/1 | MLAG_dc1-brdr1_Ethernet51/1 | *trunk | *- | *- | *MLAG | 511 |
| Ethernet52/1 | MLAG_dc1-brdr1_Ethernet52/1 | *trunk | *- | *- | *MLAG | 511 |

*Inherited from Port-Channel Interface

##### IPv4

| Interface | Description | Channel Group | IP Address | VRF | MTU | Shutdown | ACL In | ACL Out |
| --------- | ----------- | ------------- | ---------- | --- | --- | -------- | ------ | ------- |
| Ethernet48 | P2P_dc2-brdr2_Ethernet48 | - | 172.16.255.2/31 | default | 1500 | False | - | - |
| Ethernet49/1 | P2P_dc1-spine1_Ethernet1/2 | - | 10.101.0.5/31 | default | 1500 | False | - | - |
| Ethernet50/1 | P2P_dc1-spine2_Ethernet1/2 | - | 10.101.0.7/31 | default | 1500 | False | - | - |

#### Ethernet Interfaces Device Configuration

```eos
!
interface Ethernet47
   description campus-brdr2
   no shutdown
   switchport trunk allowed vlan 1000,1001
   switchport mode trunk
   switchport
   sflow enable
!
interface Ethernet48
   description P2P_dc2-brdr2_Ethernet48
   no shutdown
   mtu 1500
   no switchport
   ip address 172.16.255.2/31
   sflow enable
!
interface Ethernet49/1
   description P2P_dc1-spine1_Ethernet1/2
   no shutdown
   mtu 1500
   no switchport
   ip address 10.101.0.5/31
   sflow enable
!
interface Ethernet50/1
   description P2P_dc1-spine2_Ethernet1/2
   no shutdown
   mtu 1500
   no switchport
   ip address 10.101.0.7/31
   sflow enable
!
interface Ethernet51/1
   description MLAG_dc1-brdr1_Ethernet51/1
   no shutdown
   channel-group 511 mode active
!
interface Ethernet52/1
   description MLAG_dc1-brdr1_Ethernet52/1
   no shutdown
   channel-group 511 mode active
```

### Port-Channel Interfaces

#### Port-Channel Interfaces Summary

##### L2

| Interface | Description | Mode | VLANs | Native VLAN | Trunk Group | LACP Fallback Timeout | LACP Fallback Mode | MLAG ID | EVPN ESI |
| --------- | ----------- | ---- | ----- | ----------- | ----------- | --------------------- | ------------------ | ------- | -------- |
| Port-Channel511 | MLAG_dc1-brdr1_Port-Channel511 | trunk | - | - | MLAG | - | - | - | - |

#### Port-Channel Interfaces Device Configuration

```eos
!
interface Port-Channel511
   description MLAG_dc1-brdr1_Port-Channel511
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
| Loopback0 | ROUTER_ID | default | 10.99.1.2/32 |
| Loopback1 | VXLAN_TUNNEL_SOURCE | default | 10.101.1.1/32 |
| Loopback101 | DIAG_VRF_BLUE | BLUE | 10.0.10.66/32 |
| Loopback102 | DIAG_VRF_GREEN | GREEN | 10.0.10.130/32 |

##### IPv6

| Interface | Description | VRF | IPv6 Addresses |
| --------- | ----------- | --- | -------------- |
| Loopback0 | ROUTER_ID | default | - |
| Loopback1 | VXLAN_TUNNEL_SOURCE | default | - |
| Loopback101 | DIAG_VRF_BLUE | BLUE | - |
| Loopback102 | DIAG_VRF_GREEN | GREEN | - |

#### Loopback Interfaces Device Configuration

```eos
!
interface Loopback0
   description ROUTER_ID
   no shutdown
   ip address 10.99.1.2/32
!
interface Loopback1
   description VXLAN_TUNNEL_SOURCE
   no shutdown
   ip address 10.101.1.1/32
!
interface Loopback101
   description DIAG_VRF_BLUE
   no shutdown
   vrf BLUE
   ip address 10.0.10.66/32
!
interface Loopback102
   description DIAG_VRF_GREEN
   no shutdown
   vrf GREEN
   ip address 10.0.10.130/32
```

### VLAN Interfaces

#### VLAN Interfaces Summary

| Interface | Description | VRF | MTU | Shutdown |
| --------- | ----------- | --- | --- | -------- |
| Vlan100 | BLUE_VLAN_100 | BLUE | - | False |
| Vlan102 | BLUE_VLAN_102 | BLUE | - | False |
| Vlan200 | GREEN_VLAN_200 | GREEN | - | False |
| Vlan1000 | DC_edge_Blue | BLUE | - | False |
| Vlan1001 | DC_edge_Green | GREEN | - | False |
| Vlan3500 | MLAG_L3_VRF_BLUE | BLUE | 1500 | False |
| Vlan3501 | MLAG_L3_VRF_GREEN | GREEN | 1500 | False |
| Vlan4093 | MLAG_L3 | default | 1500 | False |
| Vlan4094 | MLAG | default | 1500 | False |

##### IPv4

| Interface | VRF | IP Address | IP Address Virtual | IP Router Virtual Address | ACL In | ACL Out |
| --------- | --- | ---------- | ------------------ | ------------------------- | ------ | ------- |
| Vlan100 | BLUE | - | 10.10.100.1/24 | - | - | - |
| Vlan102 | BLUE | - | 192.168.2.1/24 | - | - | - |
| Vlan200 | GREEN | - | 10.10.200.1/24 | - | - | - |
| Vlan1000 | BLUE | 172.16.254.6/29 | - | 172.16.254.4 | - | - |
| Vlan1001 | GREEN | 172.16.254.14/29 | - | 172.16.254.12 | - | - |
| Vlan3500 | BLUE | 10.101.254.1/31 | - | - | - | - |
| Vlan3501 | GREEN | 10.101.254.1/31 | - | - | - | - |
| Vlan4093 | default | 10.101.254.1/31 | - | - | - | - |
| Vlan4094 | default | 10.101.255.1/31 | - | - | - | - |

#### VLAN Interfaces Device Configuration

```eos
!
interface Vlan100
   description BLUE_VLAN_100
   no shutdown
   vrf BLUE
   ip address virtual 10.10.100.1/24
!
interface Vlan102
   description BLUE_VLAN_102
   no shutdown
   vrf BLUE
   ip address virtual 192.168.2.1/24
!
interface Vlan200
   description GREEN_VLAN_200
   no shutdown
   vrf GREEN
   ip address virtual 10.10.200.1/24
!
interface Vlan1000
   description DC_edge_Blue
   no shutdown
   vrf BLUE
   ip address 172.16.254.6/29
   ip virtual-router address 172.16.254.4
!
interface Vlan1001
   description DC_edge_Green
   no shutdown
   vrf GREEN
   ip address 172.16.254.14/29
   ip virtual-router address 172.16.254.12
!
interface Vlan3500
   description MLAG_L3_VRF_BLUE
   no shutdown
   mtu 1500
   vrf BLUE
   ip address 10.101.254.1/31
!
interface Vlan3501
   description MLAG_L3_VRF_GREEN
   no shutdown
   mtu 1500
   vrf GREEN
   ip address 10.101.254.1/31
!
interface Vlan4093
   description MLAG_L3
   no shutdown
   mtu 1500
   ip address 10.101.254.1/31
!
interface Vlan4094
   description MLAG
   no shutdown
   mtu 1500
   no autostate
   ip address 10.101.255.1/31
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
| 100 | 10100 | - | - |
| 102 | 10102 | - | - |
| 200 | 10200 | - | - |

##### VRF to VNI and Multicast Group Mappings

| VRF | VNI | Overlay Multicast Group to Encap Mappings |
| --- | --- | ----------------------------------------- |
| BLUE | 501 | - |
| GREEN | 502 | - |

#### VXLAN Interface Device Configuration

```eos
!
interface Vxlan1
   description dc1-brdr2_VTEP
   vxlan source-interface Loopback1
   vxlan virtual-router encapsulation mac-address mlag-system-id
   vxlan udp-port 4789
   vxlan vlan 100 vni 10100
   vxlan vlan 102 vni 10102
   vxlan vlan 200 vni 10200
   vxlan vrf BLUE vni 501
   vxlan vrf GREEN vni 502
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

Virtual Router MAC Address: 00:1c:73:00:00:99

#### Virtual Router MAC Address Device Configuration

```eos
!
ip virtual-router mac-address 00:1c:73:00:00:99
```

### IP Routing

#### IP Routing Summary

| VRF | Routing Enabled |
| --- | --------------- |
| default | True |
| BLUE | True |
| GREEN | True |
| MGMT | False |

#### IP Routing Device Configuration

```eos
!
ip routing
ip routing vrf BLUE
ip routing vrf GREEN
no ip routing vrf MGMT
```

### IPv6 Routing

#### IPv6 Routing Summary

| VRF | Routing Enabled |
| --- | --------------- |
| default | False |
| BLUE | false |
| GREEN | false |
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

### Router BGP

ASN Notation: asplain

#### Router BGP Summary

| BGP AS | Router ID |
| ------ | --------- |
| 65103 | 10.99.1.2 |

| BGP Tuning |
| ---------- |
| graceful-restart restart-time 300 |
| graceful-restart |
| no bgp default ipv4-unicast |
| distance bgp 20 200 200 |
| maximum-paths 4 |

#### Router BGP Peer Groups

##### EVPN-OVERLAY-CORE

| Settings | Value |
| -------- | ----- |
| Address Family | evpn |
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
| Maximum routes | 256000 |

##### MLAG-IPv4-UNDERLAY-PEER

| Settings | Value |
| -------- | ----- |
| Address Family | ipv4 |
| Remote AS | 65103 |
| Next-hop self | True |
| Send community | all |
| Maximum routes | 256000 |

#### BGP Neighbors

| Neighbor | Remote AS | VRF | Shutdown | Send-community | Maximum-routes | Allowas-in | BFD | RIB Pre-Policy Retain | Route-Reflector Client | Passive | TTL Max Hops |
| -------- | --------- | --- | -------- | -------------- | -------------- | ---------- | --- | --------------------- | ---------------------- | ------- | ------------ |
| 10.99.1.129 | 65000 | default | - | Inherited from peer group EVPN-OVERLAY-PEERS | Inherited from peer group EVPN-OVERLAY-PEERS | - | Inherited from peer group EVPN-OVERLAY-PEERS | - | - | - | - |
| 10.99.1.130 | 65000 | default | - | Inherited from peer group EVPN-OVERLAY-PEERS | Inherited from peer group EVPN-OVERLAY-PEERS | - | Inherited from peer group EVPN-OVERLAY-PEERS | - | - | - | - |
| 10.99.2.2 | 64103 | default | - | Inherited from peer group EVPN-OVERLAY-CORE | Inherited from peer group EVPN-OVERLAY-CORE | - | Inherited from peer group EVPN-OVERLAY-CORE | - | - | - | - |
| 10.101.0.4 | 65000 | default | - | Inherited from peer group IPv4-UNDERLAY-PEERS | Inherited from peer group IPv4-UNDERLAY-PEERS | - | True | - | - | - | - |
| 10.101.0.6 | 65000 | default | - | Inherited from peer group IPv4-UNDERLAY-PEERS | Inherited from peer group IPv4-UNDERLAY-PEERS | - | True | - | - | - | - |
| 10.101.254.0 | Inherited from peer group MLAG-IPv4-UNDERLAY-PEER | default | - | Inherited from peer group MLAG-IPv4-UNDERLAY-PEER | Inherited from peer group MLAG-IPv4-UNDERLAY-PEER | - | - | - | - | - | - |
| 172.16.255.3 | 64103 | default | - | Inherited from peer group IPv4-UNDERLAY-PEERS | Inherited from peer group IPv4-UNDERLAY-PEERS | - | - | - | - | - | - |
| 10.101.254.0 | Inherited from peer group MLAG-IPv4-UNDERLAY-PEER | BLUE | - | Inherited from peer group MLAG-IPv4-UNDERLAY-PEER | Inherited from peer group MLAG-IPv4-UNDERLAY-PEER | - | - | - | - | - | - |
| 172.16.254.2 | 63000 | BLUE | - | - | - | - | - | - | - | - | - |
| 172.16.254.3 | 63000 | BLUE | - | - | - | - | - | - | - | - | - |
| 10.101.254.0 | Inherited from peer group MLAG-IPv4-UNDERLAY-PEER | GREEN | - | Inherited from peer group MLAG-IPv4-UNDERLAY-PEER | Inherited from peer group MLAG-IPv4-UNDERLAY-PEER | - | - | - | - | - | - |
| 172.16.254.10 | 63000 | GREEN | - | - | - | - | - | - | - | - | - |
| 172.16.254.11 | 63000 | GREEN | - | - | - | - | - | - | - | - | - |

#### Router BGP EVPN Address Family

##### EVPN Peer Groups

| Peer Group | Activate | Route-map In | Route-map Out | Peer-tag In | Peer-tag Out | Encapsulation | Next-hop-self Source Interface |
| ---------- | -------- | ------------ | ------------- | ----------- | ------------ | ------------- | ------------------------------ |
| EVPN-OVERLAY-CORE | True | - | - | - | - | default | - |
| EVPN-OVERLAY-PEERS | True | - | - | - | - | default | - |

##### EVPN DCI Gateway Summary

| Settings | Value |
| -------- | ----- |
| Remote Domain Peer Groups | EVPN-OVERLAY-CORE |
| L3 Gateway Configured | True |
| L3 Gateway Inter-domain | True |

#### Router BGP VLANs

| VLAN | Route-Distinguisher | Both Route-Target | Import Route Target | Export Route-Target | Redistribute |
| ---- | ------------------- | ----------------- | ------------------- | ------------------- | ------------ |
| 100 | 10.99.1.2:10100 | 10100:10100<br>remote 10100:10100 | - | - | learned |
| 102 | 10.99.1.2:10102 | 10102:10102<br>remote 10102:10102 | - | - | learned |
| 200 | 10.99.1.2:10200 | 10200:10200<br>remote 10200:10200 | - | - | learned |

#### Router BGP VRFs

| VRF | Route-Distinguisher | Redistribute | Graceful Restart |
| --- | ------------------- | ------------ | ---------------- |
| BLUE | 10.99.1.2:501 | connected | - |
| GREEN | 10.99.1.2:502 | connected | - |

#### Router BGP Device Configuration

```eos
!
router bgp 65103
   router-id 10.99.1.2
   no bgp default ipv4-unicast
   distance bgp 20 200 200
   graceful-restart restart-time 300
   graceful-restart
   maximum-paths 4
   neighbor EVPN-OVERLAY-CORE peer group
   neighbor EVPN-OVERLAY-CORE update-source Loopback0
   neighbor EVPN-OVERLAY-CORE bfd
   neighbor EVPN-OVERLAY-CORE ebgp-multihop 15
   neighbor EVPN-OVERLAY-CORE send-community
   neighbor EVPN-OVERLAY-CORE maximum-routes 0
   neighbor EVPN-OVERLAY-PEERS peer group
   neighbor EVPN-OVERLAY-PEERS update-source Loopback0
   neighbor EVPN-OVERLAY-PEERS bfd
   neighbor EVPN-OVERLAY-PEERS ebgp-multihop 3
   neighbor EVPN-OVERLAY-PEERS send-community
   neighbor EVPN-OVERLAY-PEERS maximum-routes 0
   neighbor IPv4-UNDERLAY-PEERS peer group
   neighbor IPv4-UNDERLAY-PEERS password 7 <removed>
   neighbor IPv4-UNDERLAY-PEERS send-community
   neighbor IPv4-UNDERLAY-PEERS maximum-routes 256000
   neighbor MLAG-IPv4-UNDERLAY-PEER peer group
   neighbor MLAG-IPv4-UNDERLAY-PEER remote-as 65103
   neighbor MLAG-IPv4-UNDERLAY-PEER next-hop-self
   neighbor MLAG-IPv4-UNDERLAY-PEER description dc1-brdr1
   neighbor MLAG-IPv4-UNDERLAY-PEER route-map RM-MLAG-PEER-IN in
   neighbor MLAG-IPv4-UNDERLAY-PEER send-community
   neighbor MLAG-IPv4-UNDERLAY-PEER maximum-routes 256000
   neighbor 10.99.1.129 peer group EVPN-OVERLAY-PEERS
   neighbor 10.99.1.129 remote-as 65000
   neighbor 10.99.1.129 description dc1-spine1_Loopback0
   neighbor 10.99.1.130 peer group EVPN-OVERLAY-PEERS
   neighbor 10.99.1.130 remote-as 65000
   neighbor 10.99.1.130 description dc1-spine2_Loopback0
   neighbor 10.99.2.2 peer group EVPN-OVERLAY-CORE
   neighbor 10.99.2.2 remote-as 64103
   neighbor 10.99.2.2 description dc2-brdr2
   neighbor 10.101.0.4 peer group IPv4-UNDERLAY-PEERS
   neighbor 10.101.0.4 remote-as 65000
   neighbor 10.101.0.4 bfd
   neighbor 10.101.0.4 description dc1-spine1_Ethernet1/2
   neighbor 10.101.0.6 peer group IPv4-UNDERLAY-PEERS
   neighbor 10.101.0.6 remote-as 65000
   neighbor 10.101.0.6 bfd
   neighbor 10.101.0.6 description dc1-spine2_Ethernet1/2
   neighbor 10.101.254.0 peer group MLAG-IPv4-UNDERLAY-PEER
   neighbor 10.101.254.0 description dc1-brdr1_Vlan4093
   neighbor 172.16.255.3 peer group IPv4-UNDERLAY-PEERS
   neighbor 172.16.255.3 remote-as 64103
   neighbor 172.16.255.3 description dc2-brdr2
   redistribute connected route-map RM-CONN-2-BGP
   !
   vlan 100
      rd 10.99.1.2:10100
      rd evpn domain remote 10.99.1.2:10100
      route-target both 10100:10100
      route-target import export evpn domain remote 10100:10100
      redistribute learned
   !
   vlan 102
      rd 10.99.1.2:10102
      rd evpn domain remote 10.99.1.2:10102
      route-target both 10102:10102
      route-target import export evpn domain remote 10102:10102
      redistribute learned
   !
   vlan 200
      rd 10.99.1.2:10200
      rd evpn domain remote 10.99.1.2:10200
      route-target both 10200:10200
      route-target import export evpn domain remote 10200:10200
      redistribute learned
   !
   address-family evpn
      neighbor EVPN-OVERLAY-CORE activate
      neighbor EVPN-OVERLAY-CORE domain remote
      neighbor EVPN-OVERLAY-PEERS activate
      neighbor default next-hop-self received-evpn-routes route-type ip-prefix inter-domain
   !
   address-family ipv4
      no neighbor EVPN-OVERLAY-CORE activate
      no neighbor EVPN-OVERLAY-PEERS activate
      neighbor IPv4-UNDERLAY-PEERS activate
      neighbor MLAG-IPv4-UNDERLAY-PEER activate
   !
   vrf BLUE
      rd 10.99.1.2:501
      route-target import evpn 501:501
      route-target export evpn 501:501
      router-id 10.99.1.2
      neighbor 10.101.254.0 peer group MLAG-IPv4-UNDERLAY-PEER
      neighbor 10.101.254.0 description dc1-brdr1_Vlan3500
      neighbor 172.16.254.2 remote-as 63000
      neighbor 172.16.254.3 remote-as 63000
      redistribute connected route-map RM-CONN-2-BGP-VRFS
      !
      address-family ipv4
         neighbor 172.16.254.2 activate
         neighbor 172.16.254.3 activate
   !
   vrf GREEN
      rd 10.99.1.2:502
      route-target import evpn 502:502
      route-target export evpn 502:502
      router-id 10.99.1.2
      neighbor 10.101.254.0 peer group MLAG-IPv4-UNDERLAY-PEER
      neighbor 10.101.254.0 description dc1-brdr1_Vlan3501
      neighbor 172.16.254.10 remote-as 63000
      neighbor 172.16.254.11 remote-as 63000
      redistribute connected route-map RM-CONN-2-BGP-VRFS
      !
      address-family ipv4
         neighbor 172.16.254.10 activate
         neighbor 172.16.254.11 activate
```

## BFD

### Router BFD

#### Router BFD Multihop Summary

| Interval | Minimum RX | Multiplier |
| -------- | ---------- | ---------- |
| 1200 | 1200 | 3 |

#### Router BFD Device Configuration

```eos
!
router bfd
   multihop interval 1200 min-rx 1200 multiplier 3
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
| 10 | permit 10.99.1.0/25 eq 32 |
| 20 | permit 10.101.1.0/24 eq 32 |

##### PL-MLAG-PEER-VRFS

| Sequence | Action |
| -------- | ------ |
| 10 | permit 10.101.254.0/31 |

#### Prefix-lists Device Configuration

```eos
!
ip prefix-list PL-LOOPBACKS-EVPN-OVERLAY
   seq 10 permit 10.99.1.0/25 eq 32
   seq 20 permit 10.101.1.0/24 eq 32
!
ip prefix-list PL-MLAG-PEER-VRFS
   seq 10 permit 10.101.254.0/31
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
| BLUE | enabled |
| GREEN | enabled |
| MGMT | disabled |

### VRF Instances Device Configuration

```eos
!
vrf instance BLUE
!
vrf instance GREEN
!
vrf instance MGMT
```

## Virtual Source NAT

### Virtual Source NAT Summary

| Source NAT VRF | Source NAT IPv4 Address | Source NAT IPv6 Address |
| -------------- | ----------------------- | ----------------------- |
| BLUE | 10.0.10.66 | - |
| GREEN | 10.0.10.130 | - |

### Virtual Source NAT Configuration

```eos
!
ip address virtual source-nat vrf BLUE address 10.0.10.66
ip address virtual source-nat vrf GREEN address 10.0.10.130
```
