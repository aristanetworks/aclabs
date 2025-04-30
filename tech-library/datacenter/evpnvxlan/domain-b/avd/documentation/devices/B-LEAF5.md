# B-LEAF5

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
  - [Router ISIS](#router-isis)
  - [Router BGP](#router-bgp)
- [BFD](#bfd)
  - [Router BFD](#router-bfd)
- [Multicast](#multicast)
  - [IP IGMP Snooping](#ip-igmp-snooping)
  - [Router Multicast](#router-multicast)
  - [PIM Sparse Mode](#pim-sparse-mode)
- [Filters](#filters)
  - [Route-maps](#route-maps)
  - [IP Extended Community Lists](#ip-extended-community-lists)
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
| Management0 | OOB_MANAGEMENT | oob | MGMT | 172.100.100.109/24 | 172.100.100.1 |

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
   ip address 172.100.100.109/24
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
- DHCP Relay is enabled for MLAG peer-link requests

### DHCP Relay Device Configuration

```eos
!
dhcp relay
   tunnel requests disabled
```

## Spanning Tree

### Spanning Tree Summary

STP mode: **mstp**

STP Root Super: **True**

#### MSTP Instance and Priority

| Instance(s) | Priority |
| -------- | -------- |
| 0 | 0 |

### Spanning Tree Device Configuration

```eos
!
spanning-tree mode mstp
spanning-tree root super
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
| 40 | Purple | - |
| 80 | Black | - |

### VLANs Device Configuration

```eos
!
vlan 40
   name Purple
!
vlan 80
   name Black
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
| Ethernet7 | SERVER_B-SW1 | trunk | 40,80 | - | - | - |

*Inherited from Port-Channel Interface

##### IPv4

| Interface | Description | Channel Group | IP Address | VRF |  MTU | Shutdown | ACL In | ACL Out |
| --------- | ----------- | ------------- | ---------- | ----| ---- | -------- | ------ | ------- |
| Ethernet1 | P2P_B-SPINE1_Ethernet5 | - | unnumbered Loopback0 | default | 9214 | False | - | - |
| Ethernet2 | P2P_B-SPINE2_Ethernet5 | - | unnumbered Loopback0 | default | 9214 | False | - | - |
| Ethernet3 | P2P_B-SPINE3_Ethernet5 | - | unnumbered Loopback0 | default | 9214 | False | - | - |
| Ethernet4 | P2P_B-SPINE4_Ethernet5 | - | unnumbered Loopback0 | default | 9214 | False | - | - |

##### ISIS

| Interface | Channel Group | ISIS Instance | ISIS BFD | ISIS Metric | Mode | ISIS Circuit Type | Hello Padding | ISIS Authentication Mode |
| --------- | ------------- | ------------- | -------- | ----------- | ---- | ----------------- | ------------- | ------------------------ |
| Ethernet1 | - | 100 | - | 10 | point-to-point | level-2 | - | - |
| Ethernet2 | - | 100 | - | 10 | point-to-point | level-2 | - | - |
| Ethernet3 | - | 100 | - | 10 | point-to-point | level-2 | - | - |
| Ethernet4 | - | 100 | - | 10 | point-to-point | level-2 | - | - |

##### EVPN Multihoming

####### EVPN Multihoming Summary

| Interface | Ethernet Segment Identifier | Multihoming Redundancy Mode | Route Target |
| --------- | --------------------------- | --------------------------- | ------------ |
| Ethernet7 | 0000:0000:0005:0006:0007 | single-active | 00:05:00:06:00:07 |

####### Designated Forwarder Election Summary

| Interface | Algorithm | Preference Value | Dont Preempt | Hold time | Subsequent Hold Time | Candidate Reachability Required |
| --------- | --------- | ---------------- | ------------ | --------- | -------------------- | ------------------------------- |
| Ethernet7 | preference | 2000 | False | - | - | False |

#### Ethernet Interfaces Device Configuration

```eos
!
interface Ethernet1
   description P2P_B-SPINE1_Ethernet5
   no shutdown
   mtu 9214
   no switchport
   ip address unnumbered Loopback0
   pim ipv4 sparse-mode
   isis enable 100
   isis circuit-type level-2
   isis metric 10
   isis network point-to-point
!
interface Ethernet2
   description P2P_B-SPINE2_Ethernet5
   no shutdown
   mtu 9214
   no switchport
   ip address unnumbered Loopback0
   pim ipv4 sparse-mode
   isis enable 100
   isis circuit-type level-2
   isis metric 10
   isis network point-to-point
!
interface Ethernet3
   description P2P_B-SPINE3_Ethernet5
   no shutdown
   mtu 9214
   no switchport
   ip address unnumbered Loopback0
   pim ipv4 sparse-mode
   isis enable 100
   isis circuit-type level-2
   isis metric 10
   isis network point-to-point
!
interface Ethernet4
   description P2P_B-SPINE4_Ethernet5
   no shutdown
   mtu 9214
   no switchport
   ip address unnumbered Loopback0
   pim ipv4 sparse-mode
   isis enable 100
   isis circuit-type level-2
   isis metric 10
   isis network point-to-point
!
interface Ethernet7
   description SERVER_B-SW1
   no shutdown
   bgp session tracker TRACK-LOCAL-EVPN-PEERS
   switchport trunk allowed vlan 40,80
   switchport mode trunk
   switchport
   !
   evpn ethernet-segment
      identifier 0000:0000:0005:0006:0007
      redundancy single-active
      designated-forwarder election algorithm preference 2000
      route-target import 00:05:00:06:00:07
   spanning-tree portfast
   spanning-tree bpduguard disable
```

### Loopback Interfaces

#### Loopback Interfaces Summary

##### IPv4

| Interface | Description | VRF | IP Address |
| --------- | ----------- | --- | ---------- |
| Loopback0 | Globally Unique Address | default | 1.1.2.5/32 |
| Loopback1 | VTEP IP | default | 2.2.2.5/32 |
| Loopback101 | Unique Loopback for VRF PROD | PROD | 10.101.2.5/32 |
| Loopback102 | Unique Loopback for VRF DEV | DEV | 10.102.2.5/32 |

##### IPv6

| Interface | Description | VRF | IPv6 Address |
| --------- | ----------- | --- | ------------ |
| Loopback0 | Globally Unique Address | default | - |
| Loopback1 | VTEP IP | default | - |
| Loopback101 | Unique Loopback for VRF PROD | PROD | - |
| Loopback102 | Unique Loopback for VRF DEV | DEV | - |

##### ISIS

| Interface | ISIS instance | ISIS metric | Interface mode |
| --------- | ------------- | ----------- | -------------- |
| Loopback0 | 100 | - | passive |
| Loopback1 | 100 | - | passive |

#### Loopback Interfaces Device Configuration

```eos
!
interface Loopback0
   description Globally Unique Address
   no shutdown
   ip address 1.1.2.5/32
   isis enable 100
   isis passive
!
interface Loopback1
   description VTEP IP
   no shutdown
   ip address 2.2.2.5/32
   isis enable 100
   isis passive
!
interface Loopback101
   description Unique Loopback for VRF PROD
   no shutdown
   vrf PROD
   ip address 10.101.2.5/32
!
interface Loopback102
   description Unique Loopback for VRF DEV
   no shutdown
   vrf DEV
   ip address 10.102.2.5/32
```

### VLAN Interfaces

#### VLAN Interfaces Summary

| Interface | Description | VRF |  MTU | Shutdown |
| --------- | ----------- | --- | ---- | -------- |
| Vlan40 | Purple Network | PROD | 9014 | False |
| Vlan80 | Black Network | DEV | 9014 | False |

##### IPv4

| Interface | VRF | IP Address | IP Address Virtual | IP Router Virtual Address | ACL In | ACL Out |
| --------- | --- | ---------- | ------------------ | ------------------------- | ------ | ------- |
| Vlan40 |  PROD  |  -  |  10.40.40.1/24  |  -  |  -  |  -  |
| Vlan80 |  DEV  |  -  |  10.80.80.1/24  |  -  |  -  |  -  |

##### IPv6

| Interface | VRF | IPv6 Address | IPv6 Virtual Addresses | Virtual Router Addresses | ND RA Disabled | Managed Config Flag | Other Config Flag | IPv6 ACL In | IPv6 ACL Out |
| --------- | --- | ------------ | ---------------------- | ------------------------ | -------------- | ------------------- | ----------------- | ----------- | ------------ |
| Vlan40 | PROD | - | 2001:db8:40:40::1/64 | - | - | - | - | - | - |
| Vlan80 | DEV | - | 2001:db8:80:80::1/64 | - | - | - | - | - | - |

#### VLAN Interfaces Device Configuration

```eos
!
interface Vlan40
   description Purple Network
   no shutdown
   mtu 9014
   vrf PROD
   ip igmp
   ipv6 enable
   pim ipv4 local-interface Loopback101
   ip address virtual 10.40.40.1/24
   ipv6 address virtual 2001:db8:40:40::1/64
!
interface Vlan80
   description Black Network
   no shutdown
   mtu 9014
   vrf DEV
   ip igmp
   ipv6 enable
   pim ipv4 local-interface Loopback102
   ip address virtual 10.80.80.1/24
   ipv6 address virtual 2001:db8:80:80::1/64
```

### VXLAN Interface

#### VXLAN Interface Summary

| Setting | Value |
| ------- | ----- |
| Source Interface | Loopback1 |
| UDP port | 4789 |

##### VLAN to VNI, Flood List and Multicast Group Mappings

| VLAN | VNI | Flood List | Multicast Group |
| ---- | --- | ---------- | --------------- |
| 40 | 10040 | - | - |
| 80 | 10080 | - | - |

##### VRF to VNI and Multicast Group Mappings

| VRF | VNI | Multicast Group |
| ---- | --- | --------------- |
| DEV | 50002 | 232.2.2.2 |
| PROD | 50001 | 232.1.1.1 |

#### VXLAN Interface Device Configuration

```eos
!
interface Vxlan1
   description B-LEAF5_VTEP
   vxlan source-interface Loopback1
   vxlan udp-port 4789
   vxlan vlan 40 vni 10040
   vxlan vlan 80 vni 10080
   vxlan vrf DEV vni 50002
   vxlan vrf PROD vni 50001
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

### Router ISIS

#### Router ISIS Summary

| Settings | Value |
| -------- | ----- |
| Instance | 100 |
| Net-ID | 49.1111.0010.0100.2005.00 |
| Type | level-2 |
| Router-ID | 1.1.2.5 |
| Log Adjacency Changes | True |

#### ISIS Interfaces Summary

| Interface | ISIS Instance | ISIS Metric | Interface Mode |
| --------- | ------------- | ----------- | -------------- |
| Ethernet1 | 100 | 10 | point-to-point |
| Ethernet2 | 100 | 10 | point-to-point |
| Ethernet3 | 100 | 10 | point-to-point |
| Ethernet4 | 100 | 10 | point-to-point |
| Loopback0 | 100 | - | passive |
| Loopback1 | 100 | - | passive |

#### ISIS IPv4 Address Family Summary

| Settings | Value |
| -------- | ----- |
| IPv4 Address-family Enabled | True |
| Maximum-paths | 4 |

#### Router ISIS Device Configuration

```eos
!
router isis 100
   net 49.1111.0010.0100.2005.00
   router-id ipv4 1.1.2.5
   is-type level-2
   log-adjacency-changes
   !
   address-family ipv4 unicast
      maximum-paths 4
   !
```

### Router BGP

ASN Notation: asplain

#### Router BGP Summary

| BGP AS | Router ID |
| ------ | --------- |
| 65200 | 1.1.2.5 |

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
| Remote AS | 65200 |
| Source | Loopback0 |
| BFD | True |
| Session tracker | TRACK-LOCAL-EVPN-PEERS |
| Send community | all |
| Maximum routes | 0 (no limit) |

#### BGP Neighbors

| Neighbor | Remote AS | VRF | Shutdown | Send-community | Maximum-routes | Allowas-in | BFD | RIB Pre-Policy Retain | Route-Reflector Client | Passive | TTL Max Hops |
| -------- | --------- | --- | -------- | -------------- | -------------- | ---------- | --- | --------------------- | ---------------------- | ------- | ------------ |
| 1.1.2.201 | Inherited from peer group LOCAL-EVPN-PEERS | default | - | Inherited from peer group LOCAL-EVPN-PEERS | Inherited from peer group LOCAL-EVPN-PEERS | - | Inherited from peer group LOCAL-EVPN-PEERS | - | - | - | - |
| 1.1.2.202 | Inherited from peer group LOCAL-EVPN-PEERS | default | - | Inherited from peer group LOCAL-EVPN-PEERS | Inherited from peer group LOCAL-EVPN-PEERS | - | Inherited from peer group LOCAL-EVPN-PEERS | - | - | - | - |
| 1.1.2.203 | Inherited from peer group LOCAL-EVPN-PEERS | default | - | Inherited from peer group LOCAL-EVPN-PEERS | Inherited from peer group LOCAL-EVPN-PEERS | - | Inherited from peer group LOCAL-EVPN-PEERS | - | - | - | - |
| 1.1.2.204 | Inherited from peer group LOCAL-EVPN-PEERS | default | - | Inherited from peer group LOCAL-EVPN-PEERS | Inherited from peer group LOCAL-EVPN-PEERS | - | Inherited from peer group LOCAL-EVPN-PEERS | - | - | - | - |

#### Router BGP EVPN Address Family

- VPN import pruning is **enabled**
- Layer-2 In-place FEC update operation enabled

##### EVPN Peer Groups

| Peer Group | Activate | Route-map In | Route-map Out | Encapsulation | Next-hop-self Source Interface |
| ---------- | -------- | ------------ | ------------- | ------------- | ------------------------------ |
| LOCAL-EVPN-PEERS | True |  RM-EVPN-SOO-IN | RM-EVPN-SOO-OUT | default | - |

#### Router BGP VLANs

| VLAN | Route-Distinguisher | Both Route-Target | Import Route Target | Export Route-Target | Redistribute |
| ---- | ------------------- | ----------------- | ------------------- | ------------------- | ------------ |
| 40 | 1.1.2.5:10040 | 10040:10040 | - | - | learned |
| 80 | 1.1.2.5:10080 | 10080:10080 | - | - | learned |

#### Router BGP VRFs

| VRF | Route-Distinguisher | Redistribute | Graceful Restart | EVPN Multicast |
| --- | ------------------- | ------------ | ---------------- | -------------- |
| DEV | 1.1.2.5:50002 | connected | - | IPv4: True<br>Transit: False |
| PROD | 1.1.2.5:50001 | connected | - | IPv4: True<br>Transit: False |

#### Router BGP Session Trackers

| Session Tracker Name | Recovery Delay (in seconds) |
| -------------------- | --------------------------- |
| TRACK-LOCAL-EVPN-PEERS | 10 |

#### Router BGP Device Configuration

```eos
!
router bgp 65200
   router-id 1.1.2.5
   update wait-install
   no bgp default ipv4-unicast
   distance bgp 20 200 200
   graceful-restart restart-time 300
   graceful-restart
   maximum-paths 4 ecmp 4
   neighbor LOCAL-EVPN-PEERS peer group
   neighbor LOCAL-EVPN-PEERS remote-as 65200
   neighbor LOCAL-EVPN-PEERS update-source Loopback0
   neighbor LOCAL-EVPN-PEERS bfd
   neighbor LOCAL-EVPN-PEERS session tracker TRACK-LOCAL-EVPN-PEERS
   neighbor LOCAL-EVPN-PEERS password 7 <removed>
   neighbor LOCAL-EVPN-PEERS send-community
   neighbor LOCAL-EVPN-PEERS maximum-routes 0
   neighbor 1.1.2.201 peer group LOCAL-EVPN-PEERS
   neighbor 1.1.2.201 description B-SPINE1_Loopback0
   neighbor 1.1.2.202 peer group LOCAL-EVPN-PEERS
   neighbor 1.1.2.202 description B-SPINE2_Loopback0
   neighbor 1.1.2.203 peer group LOCAL-EVPN-PEERS
   neighbor 1.1.2.203 description B-SPINE3_Loopback0
   neighbor 1.1.2.204 peer group LOCAL-EVPN-PEERS
   neighbor 1.1.2.204 description B-SPINE4_Loopback0
   !
   vlan 40
      rd 1.1.2.5:10040
      route-target both 10040:10040
      redistribute learned
   !
   vlan 80
      rd 1.1.2.5:10080
      route-target both 10080:10080
      redistribute learned
   !
   address-family evpn
      route export ethernet-segment ip mass-withdraw
      route import ethernet-segment ip mass-withdraw
      neighbor LOCAL-EVPN-PEERS activate
      neighbor LOCAL-EVPN-PEERS route-map RM-EVPN-SOO-IN in
      neighbor LOCAL-EVPN-PEERS route-map RM-EVPN-SOO-OUT out
      route import match-failure action discard
      layer-2 fec in-place update
   !
   address-family ipv4
      no neighbor LOCAL-EVPN-PEERS activate
   !
   vrf DEV
      rd 1.1.2.5:50002
      route-target import evpn 50002:50002
      route-target export evpn 50002:50002
      router-id 1.1.2.5
      redistribute connected
      evpn multicast
   !
   vrf PROD
      rd 1.1.2.5:50001
      route-target import evpn 50001:50001
      route-target export evpn 50001:50001
      router-id 1.1.2.5
      redistribute connected
      evpn multicast
   session tracker TRACK-LOCAL-EVPN-PEERS
      recovery delay 10 seconds
   !
   address-family evpn
      route type ethernet-segment route-target auto
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

## Filters

### Route-maps

#### Route-maps Summary

##### RM-EVPN-SOO-IN

| Sequence | Type | Match | Set | Sub-Route-Map | Continue |
| -------- | ---- | ----- | --- | ------------- | -------- |
| 10 | deny | extcommunity ECL-EVPN-SOO | - | - | - |
| 20 | permit | - | - | - | - |

##### RM-EVPN-SOO-OUT

| Sequence | Type | Match | Set | Sub-Route-Map | Continue |
| -------- | ---- | ----- | --- | ------------- | -------- |
| 10 | permit | - | extcommunity soo 2.2.2.5:1 additive | - | - |

#### Route-maps Device Configuration

```eos
!
route-map RM-EVPN-SOO-IN deny 10
   match extcommunity ECL-EVPN-SOO
!
route-map RM-EVPN-SOO-IN permit 20
!
route-map RM-EVPN-SOO-OUT permit 10
   set extcommunity soo 2.2.2.5:1 additive
```

### IP Extended Community Lists

#### IP Extended Community Lists Summary

| List Name | Type | Extended Communities |
| --------- | ---- | -------------------- |
| ECL-EVPN-SOO | permit | soo 2.2.2.5:1 |

#### IP Extended Community Lists Device Configuration

```eos
!
ip extcommunity-list ECL-EVPN-SOO permit soo 2.2.2.5:1
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
| DEV | 10.102.2.5 | - |
| PROD | 10.101.2.5 | - |

### Virtual Source NAT Configuration

```eos
!
ip address virtual source-nat vrf DEV address 10.102.2.5
ip address virtual source-nat vrf PROD address 10.101.2.5
```

## IP DHCP Relay

### IP DHCP Relay Summary

IP DHCP Relay Option 82 is enabled.

### IP DHCP Relay Device Configuration

```eos
!
ip dhcp relay information option
```
