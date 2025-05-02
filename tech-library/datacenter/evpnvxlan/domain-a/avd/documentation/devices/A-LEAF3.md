# A-LEAF3

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
- [DHCP Relay](#dhcp-relay)
  - [DHCP Relay Summary](#dhcp-relay-summary)
  - [DHCP Relay Device Configuration](#dhcp-relay-device-configuration)
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
- [MAC Address Table](#mac-address-table)
  - [MAC Address Table Summary](#mac-address-table-summary)
  - [MAC Address Table Device Configuration](#mac-address-table-device-configuration)
- [Interfaces](#interfaces)
  - [Switchport Default](#switchport-default)
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
- [IP DHCP Relay](#ip-dhcp-relay)
  - [IP DHCP Relay Summary](#ip-dhcp-relay-summary)
  - [IP DHCP Relay Device Configuration](#ip-dhcp-relay-device-configuration)

## Management

### Management Interfaces

#### Management Interfaces Summary

##### IPv4

| Management Interface | Description | Type | VRF | IP Address | Gateway |
| -------------------- | ----------- | ---- | --- | ---------- | ------- |
| Management0 | OOB_MANAGEMENT | oob | MGMT | 172.100.100.107/24 | 172.100.100.1 |

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
   ip address 172.100.100.107/24
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

## DHCP Relay

### DHCP Relay Summary

- DHCP Relay is disabled for tunnelled requests
- DHCP Relay is disabled for MLAG peer-link requests

### DHCP Relay Device Configuration

```eos
!
dhcp relay
   tunnel requests disabled
   mlag peer-link requests disabled
```

## MLAG

### MLAG Summary

| Domain-id | Local-interface | Peer-address | Peer-link |
| --------- | --------------- | ------------ | --------- |
| POD2 | Vlan4094 | 169.254.0.1 | Port-Channel1000 |

Dual primary detection is disabled.

### MLAG Device Configuration

```eos
!
mlag configuration
   domain-id POD2
   local-interface Vlan4094
   peer-address 169.254.0.1
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

### Internal VLAN Allocation Policy Device Configuration

```eos
!
vlan internal order ascending range 1006 1199
```

## VLANs

### VLANs Summary

| VLAN ID | Name | Trunk Groups |
| ------- | ---- | ------------ |
| 10 | Blue | - |
| 30 | Orange | - |
| 50 | Yellow | - |
| 3001 | MLAG_L3_VRF_PROD | MLAG |
| 3002 | MLAG_L3_VRF_DEV | MLAG |
| 4093 | MLAG_L3 | MLAG |
| 4094 | MLAG | MLAG |

### VLANs Device Configuration

```eos
!
vlan 10
   name Blue
!
vlan 30
   name Orange
!
vlan 50
   name Yellow
!
vlan 3001
   name MLAG_L3_VRF_PROD
   trunk group MLAG
!
vlan 3002
   name MLAG_L3_VRF_DEV
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
| Ethernet5 | MLAG_A-LEAF4_Ethernet5 | *trunk | *- | *- | *MLAG | 1000 |
| Ethernet6 | MLAG_A-LEAF4_Ethernet6 | *trunk | *- | *- | *MLAG | 1000 |
| Ethernet7 | SERVER_HostA3_eth1 | access | 50 | - | - | - |
| Ethernet8 | SERVER_HostA4_eth1 | *access | *10 | *- | *- | 8 |

*Inherited from Port-Channel Interface

##### IPv4

| Interface | Description | Channel Group | IP Address | VRF |  MTU | Shutdown | ACL In | ACL Out |
| --------- | ----------- | ------------- | ---------- | ----| ---- | -------- | ------ | ------- |
| Ethernet1 | P2P_A-SPINE1_Ethernet3 | - | 192.168.0.17/31 | default | 9214 | False | - | - |
| Ethernet2 | P2P_A-SPINE2_Ethernet3 | - | 192.168.0.19/31 | default | 9214 | False | - | - |
| Ethernet3 | P2P_A-SPINE3_Ethernet3 | - | 192.168.0.21/31 | default | 9214 | False | - | - |
| Ethernet4 | P2P_A-SPINE4_Ethernet3 | - | 192.168.0.23/31 | default | 9214 | False | - | - |

#### Ethernet Interfaces Device Configuration

```eos
!
interface Ethernet1
   description P2P_A-SPINE1_Ethernet3
   no shutdown
   mtu 9214
   no switchport
   ip address 192.168.0.17/31
   pim ipv4 sparse-mode
!
interface Ethernet2
   description P2P_A-SPINE2_Ethernet3
   no shutdown
   mtu 9214
   no switchport
   ip address 192.168.0.19/31
   pim ipv4 sparse-mode
!
interface Ethernet3
   description P2P_A-SPINE3_Ethernet3
   no shutdown
   mtu 9214
   no switchport
   ip address 192.168.0.21/31
   pim ipv4 sparse-mode
!
interface Ethernet4
   description P2P_A-SPINE4_Ethernet3
   no shutdown
   mtu 9214
   no switchport
   ip address 192.168.0.23/31
   pim ipv4 sparse-mode
!
interface Ethernet5
   description MLAG_A-LEAF4_Ethernet5
   no shutdown
   channel-group 1000 mode active
!
interface Ethernet6
   description MLAG_A-LEAF4_Ethernet6
   no shutdown
   channel-group 1000 mode active
!
interface Ethernet7
   description SERVER_HostA3_eth1
   no shutdown
   switchport access vlan 50
   switchport mode access
   switchport
   spanning-tree portfast
   spanning-tree bpduguard enable
!
interface Ethernet8
   description SERVER_HostA4_eth1
   no shutdown
   channel-group 8 mode active
```

### Port-Channel Interfaces

#### Port-Channel Interfaces Summary

##### L2

| Interface | Description | Mode | VLANs | Native VLAN | Trunk Group | LACP Fallback Timeout | LACP Fallback Mode | MLAG ID | EVPN ESI |
| --------- | ----------- | ---- | ----- | ----------- | ------------| --------------------- | ------------------ | ------- | -------- |
| Port-Channel8 | SERVER_HostA4 | access | 10 | - | - | - | - | 8 | - |
| Port-Channel1000 | MLAG_A-LEAF4_Port-Channel1000 | trunk | - | - | MLAG | - | - | - | - |

#### Port-Channel Interfaces Device Configuration

```eos
!
interface Port-Channel8
   description SERVER_HostA4
   no shutdown
   switchport access vlan 10
   switchport mode access
   switchport
   mlag 8
   spanning-tree portfast
   spanning-tree bpduguard enable
!
interface Port-Channel1000
   description MLAG_A-LEAF4_Port-Channel1000
   no shutdown
   switchport mode trunk
   switchport trunk group MLAG
   switchport
```

### Loopback Interfaces

#### Loopback Interfaces Summary

##### IPv4

| Interface | Description | VRF | IP Address |
| --------- | ----------- | --- | ---------- |
| Loopback0 | Globally Unique Address | default | 1.1.1.3/32 |
| Loopback1 | VTEP IP | default | 2.2.1.3/32 |
| Loopback101 | Per-VRF Unique Loopback | PROD | 10.101.101.3/32 |
| Loopback102 | Per-VRF Unique Loopback | DEV | 10.102.102.3/32 |

##### IPv6

| Interface | Description | VRF | IPv6 Address |
| --------- | ----------- | --- | ------------ |
| Loopback0 | Globally Unique Address | default | - |
| Loopback1 | VTEP IP | default | - |
| Loopback101 | Per-VRF Unique Loopback | PROD | - |
| Loopback102 | Per-VRF Unique Loopback | DEV | - |

#### Loopback Interfaces Device Configuration

```eos
!
interface Loopback0
   description Globally Unique Address
   no shutdown
   ip address 1.1.1.3/32
!
interface Loopback1
   description VTEP IP
   no shutdown
   ip address 2.2.1.3/32
!
interface Loopback101
   description Per-VRF Unique Loopback
   no shutdown
   vrf PROD
   ip address 10.101.101.3/32
!
interface Loopback102
   description Per-VRF Unique Loopback
   no shutdown
   vrf DEV
   ip address 10.102.102.3/32
```

### VLAN Interfaces

#### VLAN Interfaces Summary

| Interface | Description | VRF |  MTU | Shutdown |
| --------- | ----------- | --- | ---- | -------- |
| Vlan10 | Blue Network | PROD | 9014 | False |
| Vlan30 | Orange Network | PROD | 9014 | False |
| Vlan50 | Yellow Network | DEV | 9014 | False |
| Vlan3001 | MLAG_L3_VRF_PROD | PROD | 9214 | False |
| Vlan3002 | MLAG_L3_VRF_DEV | DEV | 9214 | False |
| Vlan4093 | MLAG_L3 | default | 9214 | False |
| Vlan4094 | MLAG | default | 9214 | False |

##### IPv4

| Interface | VRF | IP Address | IP Address Virtual | IP Router Virtual Address | ACL In | ACL Out |
| --------- | --- | ---------- | ------------------ | ------------------------- | ------ | ------- |
| Vlan10 |  PROD  |  -  |  10.10.10.1/24  |  -  |  -  |  -  |
| Vlan30 |  PROD  |  -  |  10.30.30.1/24  |  -  |  -  |  -  |
| Vlan50 |  DEV  |  -  |  10.50.50.1/24  |  -  |  -  |  -  |
| Vlan3001 |  PROD  |  192.2.2.0/31  |  -  |  -  |  -  |  -  |
| Vlan3002 |  DEV  |  192.2.2.0/31  |  -  |  -  |  -  |  -  |
| Vlan4093 |  default  |  192.0.0.0/31  |  -  |  -  |  -  |  -  |
| Vlan4094 |  default  |  169.254.0.0/31  |  -  |  -  |  -  |  -  |

##### IPv6

| Interface | VRF | IPv6 Address | IPv6 Virtual Addresses | Virtual Router Addresses | ND RA Disabled | Managed Config Flag | Other Config Flag | IPv6 ACL In | IPv6 ACL Out |
| --------- | --- | ------------ | ---------------------- | ------------------------ | -------------- | ------------------- | ----------------- | ----------- | ------------ |
| Vlan10 | PROD | - | 2001:db8:10:10::1/64 | - | - | - | - | - | - |
| Vlan30 | PROD | - | 2001:db8:30:30::1/64 | - | - | - | - | - | - |
| Vlan50 | DEV | - | 2001:db8:50:50::1/64 | - | - | - | - | - | - |

#### VLAN Interfaces Device Configuration

```eos
!
interface Vlan10
   description Blue Network
   no shutdown
   mtu 9014
   vrf PROD
   ipv6 enable
   pim ipv4 sparse-mode
   pim ipv4 local-interface Loopback101
   ip address virtual 10.10.10.1/24
   ipv6 address virtual 2001:db8:10:10::1/64
!
interface Vlan30
   description Orange Network
   no shutdown
   mtu 9014
   vrf PROD
   ipv6 enable
   pim ipv4 sparse-mode
   pim ipv4 local-interface Loopback101
   ip address virtual 10.30.30.1/24
   ipv6 address virtual 2001:db8:30:30::1/64
!
interface Vlan50
   description Yellow Network
   no shutdown
   mtu 9014
   vrf DEV
   ipv6 enable
   pim ipv4 sparse-mode
   pim ipv4 local-interface Loopback102
   ip address virtual 10.50.50.1/24
   ipv6 address virtual 2001:db8:50:50::1/64
!
interface Vlan3001
   description MLAG_L3_VRF_PROD
   no shutdown
   mtu 9214
   vrf PROD
   ip address 192.2.2.0/31
!
interface Vlan3002
   description MLAG_L3_VRF_DEV
   no shutdown
   mtu 9214
   vrf DEV
   ip address 192.2.2.0/31
!
interface Vlan4093
   description MLAG_L3
   no shutdown
   mtu 9214
   ip address 192.0.0.0/31
   pim ipv4 sparse-mode
!
interface Vlan4094
   description MLAG
   no shutdown
   mtu 9214
   no autostate
   ip address 169.254.0.0/31
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
| 10 | 10010 | - | - |
| 30 | 10030 | - | - |
| 50 | 10050 | - | - |

##### VRF to VNI and Multicast Group Mappings

| VRF | VNI | Multicast Group |
| ---- | --- | --------------- |
| DEV | 50002 | 232.2.2.2 |
| PROD | 50001 | 232.1.1.1 |

#### VXLAN Interface Device Configuration

```eos
!
interface Vxlan1
   description A-LEAF3_VTEP
   vxlan source-interface Loopback0
   vxlan virtual-router encapsulation mac-address mlag-system-id
   vxlan udp-port 4789
   vxlan vlan 10 vni 10010
   vxlan vlan 30 vni 10030
   vxlan vlan 50 vni 10050
   vxlan vrf DEV vni 50002
   vxlan vrf PROD vni 50001
   vxlan mlag source-interface Loopback1
   vxlan vrf DEV multicast group 232.2.2.2
   vxlan vrf PROD multicast group 232.1.1.1
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

Virtual Router MAC Address: 00:1c:73:00:00:01

#### Virtual Router MAC Address Device Configuration

```eos
!
ip virtual-router mac-address 00:1c:73:00:00:01
```

### IP Routing

#### IP Routing Summary

| VRF | Routing Enabled |
| --- | --------------- |
| default | True |
| DEV | True |
| MGMT | False |
| PROD | True |

#### IP Routing Device Configuration

```eos
!
ip routing
ip routing vrf DEV
no ip routing vrf MGMT
ip routing vrf PROD
```

### IPv6 Routing

#### IPv6 Routing Summary

| VRF | Routing Enabled |
| --- | --------------- |
| default | False |
| DEV | true |
| MGMT | false |
| PROD | true |

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
| 65134 | 1.1.1.3 |

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

##### MLAG-IPV4-PEER

| Settings | Value |
| -------- | ----- |
| Address Family | ipv4 |
| Remote AS | 65134 |
| Next-hop self | True |
| Send community | all |
| Maximum routes | 12000 |

#### BGP Neighbors

| Neighbor | Remote AS | VRF | Shutdown | Send-community | Maximum-routes | Allowas-in | BFD | RIB Pre-Policy Retain | Route-Reflector Client | Passive | TTL Max Hops |
| -------- | --------- | --- | -------- | -------------- | -------------- | ---------- | --- | --------------------- | ---------------------- | ------- | ------------ |
| 1.1.1.201 | 65100 | default | - | Inherited from peer group LOCAL-EVPN-PEERS | Inherited from peer group LOCAL-EVPN-PEERS | - | Inherited from peer group LOCAL-EVPN-PEERS | - | - | - | - |
| 1.1.1.202 | 65100 | default | - | Inherited from peer group LOCAL-EVPN-PEERS | Inherited from peer group LOCAL-EVPN-PEERS | - | Inherited from peer group LOCAL-EVPN-PEERS | - | - | - | - |
| 1.1.1.203 | 65100 | default | - | Inherited from peer group LOCAL-EVPN-PEERS | Inherited from peer group LOCAL-EVPN-PEERS | - | Inherited from peer group LOCAL-EVPN-PEERS | - | - | - | - |
| 1.1.1.204 | 65100 | default | - | Inherited from peer group LOCAL-EVPN-PEERS | Inherited from peer group LOCAL-EVPN-PEERS | - | Inherited from peer group LOCAL-EVPN-PEERS | - | - | - | - |
| 192.0.0.1 | Inherited from peer group MLAG-IPV4-PEER | default | - | Inherited from peer group MLAG-IPV4-PEER | Inherited from peer group MLAG-IPV4-PEER | - | - | - | - | - | - |
| 192.168.0.16 | 65100 | default | - | Inherited from peer group LOCAL-IPV4-PEERS | Inherited from peer group LOCAL-IPV4-PEERS | - | - | - | - | - | - |
| 192.168.0.18 | 65100 | default | - | Inherited from peer group LOCAL-IPV4-PEERS | Inherited from peer group LOCAL-IPV4-PEERS | - | - | - | - | - | - |
| 192.168.0.20 | 65100 | default | - | Inherited from peer group LOCAL-IPV4-PEERS | Inherited from peer group LOCAL-IPV4-PEERS | - | - | - | - | - | - |
| 192.168.0.22 | 65100 | default | - | Inherited from peer group LOCAL-IPV4-PEERS | Inherited from peer group LOCAL-IPV4-PEERS | - | - | - | - | - | - |
| 192.2.2.1 | Inherited from peer group MLAG-IPV4-PEER | DEV | - | Inherited from peer group MLAG-IPV4-PEER | Inherited from peer group MLAG-IPV4-PEER | - | - | - | - | - | - |
| 192.2.2.1 | Inherited from peer group MLAG-IPV4-PEER | PROD | - | Inherited from peer group MLAG-IPV4-PEER | Inherited from peer group MLAG-IPV4-PEER | - | - | - | - | - | - |

#### Router BGP EVPN Address Family

- VPN import pruning is **enabled**

##### EVPN Peer Groups

| Peer Group | Activate | Route-map In | Route-map Out | Encapsulation | Next-hop-self Source Interface |
| ---------- | -------- | ------------ | ------------- | ------------- | ------------------------------ |
| LOCAL-EVPN-PEERS | True |  - | - | default | - |

#### Router BGP VLANs

| VLAN | Route-Distinguisher | Both Route-Target | Import Route Target | Export Route-Target | Redistribute |
| ---- | ------------------- | ----------------- | ------------------- | ------------------- | ------------ |
| 10 | 1.1.1.3:10010 | 10010:10010 | - | - | learned |
| 30 | 1.1.1.3:10030 | 10030:10030 | - | - | learned |
| 50 | 1.1.1.3:10050 | 10050:10050 | - | - | learned |

#### Router BGP VRFs

| VRF | Route-Distinguisher | Redistribute | Graceful Restart | EVPN Multicast |
| --- | ------------------- | ------------ | ---------------- | -------------- |
| DEV | 1.1.1.3:50002 | connected | - | IPv4: True<br>Transit: False |
| PROD | 1.1.1.3:50001 | connected | - | IPv4: True<br>Transit: False |

#### Router BGP Device Configuration

```eos
!
router bgp 65134
   router-id 1.1.1.3
   update wait-install
   no bgp default ipv4-unicast
   distance bgp 20 200 200
   graceful-restart restart-time 300
   graceful-restart
   maximum-paths 4 ecmp 4
   neighbor LOCAL-EVPN-PEERS peer group
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
   neighbor MLAG-IPV4-PEER peer group
   neighbor MLAG-IPV4-PEER remote-as 65134
   neighbor MLAG-IPV4-PEER next-hop-self
   neighbor MLAG-IPV4-PEER description A-LEAF4
   neighbor MLAG-IPV4-PEER route-map RM-MLAG-PEER-IN in
   neighbor MLAG-IPV4-PEER password 7 <removed>
   neighbor MLAG-IPV4-PEER send-community
   neighbor MLAG-IPV4-PEER maximum-routes 12000
   neighbor 1.1.1.201 peer group LOCAL-EVPN-PEERS
   neighbor 1.1.1.201 remote-as 65100
   neighbor 1.1.1.201 description A-SPINE1_Loopback0
   neighbor 1.1.1.202 peer group LOCAL-EVPN-PEERS
   neighbor 1.1.1.202 remote-as 65100
   neighbor 1.1.1.202 description A-SPINE2_Loopback0
   neighbor 1.1.1.203 peer group LOCAL-EVPN-PEERS
   neighbor 1.1.1.203 remote-as 65100
   neighbor 1.1.1.203 description A-SPINE3_Loopback0
   neighbor 1.1.1.204 peer group LOCAL-EVPN-PEERS
   neighbor 1.1.1.204 remote-as 65100
   neighbor 1.1.1.204 description A-SPINE4_Loopback0
   neighbor 192.0.0.1 peer group MLAG-IPV4-PEER
   neighbor 192.0.0.1 description A-LEAF4_Vlan4093
   neighbor 192.168.0.16 peer group LOCAL-IPV4-PEERS
   neighbor 192.168.0.16 remote-as 65100
   neighbor 192.168.0.16 description A-SPINE1_Ethernet3
   neighbor 192.168.0.18 peer group LOCAL-IPV4-PEERS
   neighbor 192.168.0.18 remote-as 65100
   neighbor 192.168.0.18 description A-SPINE2_Ethernet3
   neighbor 192.168.0.20 peer group LOCAL-IPV4-PEERS
   neighbor 192.168.0.20 remote-as 65100
   neighbor 192.168.0.20 description A-SPINE3_Ethernet3
   neighbor 192.168.0.22 peer group LOCAL-IPV4-PEERS
   neighbor 192.168.0.22 remote-as 65100
   neighbor 192.168.0.22 description A-SPINE4_Ethernet3
   redistribute connected route-map RM-CONN-2-BGP
   !
   vlan 10
      rd 1.1.1.3:10010
      route-target both 10010:10010
      redistribute learned
   !
   vlan 30
      rd 1.1.1.3:10030
      route-target both 10030:10030
      redistribute learned
   !
   vlan 50
      rd 1.1.1.3:10050
      route-target both 10050:10050
      redistribute learned
   !
   address-family evpn
      neighbor LOCAL-EVPN-PEERS activate
      route import match-failure action discard
   !
   address-family ipv4
      no neighbor LOCAL-EVPN-PEERS activate
      neighbor LOCAL-IPV4-PEERS activate
      neighbor MLAG-IPV4-PEER activate
   !
   vrf DEV
      rd 1.1.1.3:50002
      route-target import evpn 50002:50002
      route-target export evpn 50002:50002
      router-id 1.1.1.3
      update wait-install
      neighbor 192.2.2.1 peer group MLAG-IPV4-PEER
      neighbor 192.2.2.1 description A-LEAF4_Vlan3002
      redistribute connected route-map RM-CONN-2-BGP-VRFS
      evpn multicast
   !
   vrf PROD
      rd 1.1.1.3:50001
      route-target import evpn 50001:50001
      route-target export evpn 50001:50001
      router-id 1.1.1.3
      update wait-install
      neighbor 192.2.2.1 peer group MLAG-IPV4-PEER
      neighbor 192.2.2.1 description A-LEAF4_Vlan3001
      redistribute connected route-map RM-CONN-2-BGP-VRFS
      evpn multicast
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

#### IP Router Multicast VRFs

| VRF Name | Multicast Routing |
| -------- | ----------------- |
| DEV | enabled |
| PROD | enabled |

#### Router Multicast Device Configuration

```eos
!
router multicast
   ipv4
      routing
      software-forwarding sfe
   !
   vrf DEV
      ipv4
         routing
   !
   vrf PROD
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
| Vlan10 | PROD | IPv4 | - | - | Loopback101 |
| Vlan30 | PROD | IPv4 | - | - | Loopback101 |
| Vlan50 | DEV | IPv4 | - | - | Loopback102 |
| Vlan4093 | - | IPv4 | - | - | - |

## Filters

### Prefix-lists

#### Prefix-lists Summary

##### PL-LOOPBACKS-EVPN-OVERLAY

| Sequence | Action |
| -------- | ------ |
| 10 | permit 1.1.1.0/24 eq 32 |
| 20 | permit 2.2.1.0/24 eq 32 |

##### PL-MLAG-PEER-VRFS

| Sequence | Action |
| -------- | ------ |
| 10 | permit 192.2.2.0/31 |

#### Prefix-lists Device Configuration

```eos
!
ip prefix-list PL-LOOPBACKS-EVPN-OVERLAY
   seq 10 permit 1.1.1.0/24 eq 32
   seq 20 permit 2.2.1.0/24 eq 32
!
ip prefix-list PL-MLAG-PEER-VRFS
   seq 10 permit 192.2.2.0/31
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
| DEV | enabled |
| MGMT | disabled |
| PROD | enabled |

### VRF Instances Device Configuration

```eos
!
vrf instance DEV
!
vrf instance MGMT
!
vrf instance PROD
```

## Virtual Source NAT

### Virtual Source NAT Summary

| Source NAT VRF | Source NAT IPv4 Address | Source NAT IPv6 Address |
| -------------- | ----------------------- | ----------------------- |
| DEV | 10.102.102.3 | - |
| PROD | 10.101.101.3 | - |

### Virtual Source NAT Configuration

```eos
!
ip address virtual source-nat vrf DEV address 10.102.102.3
ip address virtual source-nat vrf PROD address 10.101.101.3
```

## IP DHCP Relay

### IP DHCP Relay Summary

IP DHCP Relay Option 82 is enabled.

### IP DHCP Relay Device Configuration

```eos
!
ip dhcp relay information option
```
