# dc1-l2leaf2

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
  - [VLAN Interfaces](#vlan-interfaces)
- [Routing](#routing)
  - [Service Routing Protocols Model](#service-routing-protocols-model)
  - [IP Routing](#ip-routing)
  - [IPv6 Routing](#ipv6-routing)
- [Multicast](#multicast)
  - [IP IGMP Snooping](#ip-igmp-snooping)
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
| Management1 | OOB_MANAGEMENT | oob | MGMT | 192.168.0.17/24 | - |

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
   ip address 192.168.0.17/24
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
| gzip | apiserver.cv-prod-na-northeast1-b.arista.io:443 | MGMT | token-secure,/tmp/cv-onboarding-token | ale,flexCounter,hardware,kni,pulse,strata | - | True |

#### TerminAttr Daemon Device Configuration

```eos
!
daemon TerminAttr
   exec /usr/bin/TerminAttr -cvaddr=apiserver.cv-prod-na-northeast1-b.arista.io:443 -cvauth=token-secure,/tmp/cv-onboarding-token -cvvrf=MGMT -disableaaa -smashexcludes=ale,flexCounter,hardware,kni,pulse,strata -taillogs -sflowaddr=default/127.0.0.1:6343 -cvsourceintf=Management1
   no shutdown
```

### SFlow

#### SFlow Summary

| VRF | SFlow Source | SFlow Destination | Port |
| --- | ------------ | ----------------- | ---- |
| default | - | 127.0.0.1 | 6343 |
| default | Vlan4094 | - | - |

sFlow Sample Rate: 10

sFlow Polling Interval: 50

sFlow is enabled.

#### SFlow Interfaces

| Interface | Ingress Enabled | Egress Enabled |
| --------- | --------------- | -------------- |
| Port-Channel1 | True | - |
| Port-Channel49 | True | - |
| Port-Channel51 | True | - |

#### SFlow Device Configuration

```eos
!
sflow sample 10
sflow polling-interval 50
sflow destination 127.0.0.1 6343
sflow source-interface Vlan4094
sflow run
```

## MLAG

### MLAG Summary

| Domain-id | Local-interface | Peer-address | Peer-link |
| --------- | --------------- | ------------ | --------- |
| DC1_L2LEAF12 | Vlan4094 | 10.101.255.0 | Port-Channel51 |

Dual primary detection is enabled. The detection delay is 5 seconds.

### MLAG Device Configuration

```eos
!
mlag configuration
   domain-id DC1_L2LEAF12
   local-interface Vlan4094
   peer-address 10.101.255.0
   peer-address heartbeat 192.168.0.16 vrf MGMT
   peer-link Port-Channel51
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
| 0 | 32768 |

#### Global Spanning-Tree Settings

- Spanning Tree disabled for VLANs: **4094**

### Spanning Tree Device Configuration

```eos
!
spanning-tree mode mstp
no spanning-tree vlan-id 4094
spanning-tree mst 0 priority 32768
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
| Ethernet1 | SERVER_dc1-host1_Ethernet2 | *access | *100 | *- | *- | 1 |
| Ethernet49 | L2_dc1-leaf1_Ethernet54/1 | *trunk | *100,102,200 | *- | *- | 49 |
| Ethernet50 | L2_dc1-leaf2_Ethernet54/1 | *trunk | *100,102,200 | *- | *- | 49 |
| Ethernet51 | MLAG_dc1-l2leaf1_Ethernet51 | *trunk | *- | *- | *MLAG | 51 |
| Ethernet52 | MLAG_dc1-l2leaf1_Ethernet52 | *trunk | *- | *- | *MLAG | 51 |

*Inherited from Port-Channel Interface

#### Ethernet Interfaces Device Configuration

```eos
!
interface Ethernet1
   description SERVER_dc1-host1_Ethernet2
   no shutdown
   channel-group 1 mode active
!
interface Ethernet49
   description L2_dc1-leaf1_Ethernet54/1
   no shutdown
   channel-group 49 mode active
!
interface Ethernet50
   description L2_dc1-leaf2_Ethernet54/1
   no shutdown
   channel-group 49 mode active
!
interface Ethernet51
   description MLAG_dc1-l2leaf1_Ethernet51
   no shutdown
   channel-group 51 mode active
!
interface Ethernet52
   description MLAG_dc1-l2leaf1_Ethernet52
   no shutdown
   channel-group 51 mode active
```

### Port-Channel Interfaces

#### Port-Channel Interfaces Summary

##### L2

| Interface | Description | Mode | VLANs | Native VLAN | Trunk Group | LACP Fallback Timeout | LACP Fallback Mode | MLAG ID | EVPN ESI |
| --------- | ----------- | ---- | ----- | ----------- | ----------- | --------------------- | ------------------ | ------- | -------- |
| Port-Channel1 | SERVER_dc1-host1 | access | 100 | - | - | - | - | 1 | - |
| Port-Channel49 | L2_DC1_LEAF1_Port-Channel531 | trunk | 100,102,200 | - | - | - | - | 49 | - |
| Port-Channel51 | MLAG_dc1-l2leaf1_Port-Channel51 | trunk | - | - | MLAG | - | - | - | - |

#### Port-Channel Interfaces Device Configuration

```eos
!
interface Port-Channel1
   description SERVER_dc1-host1
   no shutdown
   switchport access vlan 100
   switchport mode access
   switchport
   mlag 1
   sflow enable
!
interface Port-Channel49
   description L2_DC1_LEAF1_Port-Channel531
   no shutdown
   switchport trunk allowed vlan 100,102,200
   switchport mode trunk
   switchport
   mlag 49
   sflow enable
!
interface Port-Channel51
   description MLAG_dc1-l2leaf1_Port-Channel51
   no shutdown
   switchport mode trunk
   switchport trunk group MLAG
   switchport
   sflow enable
```

### VLAN Interfaces

#### VLAN Interfaces Summary

| Interface | Description | VRF | MTU | Shutdown |
| --------- | ----------- | --- | --- | -------- |
| Vlan4094 | MLAG | default | 9214 | False |

##### IPv4

| Interface | VRF | IP Address | IP Address Virtual | IP Router Virtual Address | ACL In | ACL Out |
| --------- | --- | ---------- | ------------------ | ------------------------- | ------ | ------- |
| Vlan4094 | default | 10.101.255.1/31 | - | - | - | - |

#### VLAN Interfaces Device Configuration

```eos
!
interface Vlan4094
   description MLAG
   no shutdown
   mtu 9214
   no autostate
   ip address 10.101.255.1/31
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
| default | False |
| MGMT | False |

#### IP Routing Device Configuration

```eos
no ip routing vrf MGMT
```

### IPv6 Routing

#### IPv6 Routing Summary

| VRF | Routing Enabled |
| --- | --------------- |
| default | False |
| MGMT | false |

## Multicast

### IP IGMP Snooping

#### IP IGMP Snooping Summary

| IGMP Snooping | Fast Leave | Interface Restart Query | Proxy | Restart Query Interval | Robustness Variable |
| ------------- | ---------- | ----------------------- | ----- | ---------------------- | ------------------- |
| Enabled | - | - | - | - | - |

#### IP IGMP Snooping Device Configuration

```eos
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
