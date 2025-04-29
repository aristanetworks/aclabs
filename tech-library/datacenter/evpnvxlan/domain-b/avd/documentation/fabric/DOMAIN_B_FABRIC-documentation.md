# DOMAIN_B_FABRIC

## Table of Contents

- [Fabric Switches and Management IP](#fabric-switches-and-management-ip)
  - [Fabric Switches with inband Management IP](#fabric-switches-with-inband-management-ip)
- [Fabric Topology](#fabric-topology)
- [Fabric IP Allocation](#fabric-ip-allocation)
  - [Fabric Point-To-Point Links](#fabric-point-to-point-links)
  - [Point-To-Point Links Node Allocation](#point-to-point-links-node-allocation)
  - [Loopback Interfaces (BGP EVPN Peering)](#loopback-interfaces-bgp-evpn-peering)
  - [Loopback0 Interfaces Node Allocation](#loopback0-interfaces-node-allocation)
  - [ISIS CLNS interfaces](#isis-clns-interfaces)
  - [VTEP Loopback VXLAN Tunnel Source Interfaces (VTEPs Only)](#vtep-loopback-vxlan-tunnel-source-interfaces-vteps-only)
  - [VTEP Loopback Node allocation](#vtep-loopback-node-allocation)

## Fabric Switches and Management IP

| POD | Type | Node | Management IP | Platform | Provisioned in CloudVision | Serial Number |
| --- | ---- | ---- | ------------- | -------- | -------------------------- | ------------- |
| DOMAIN_B_FABRIC | l3leaf | B-LEAF1 | 172.100.100.105/24 | cEOS-LAB | Provisioned | - |
| DOMAIN_B_FABRIC | l3leaf | B-LEAF2 | 172.100.100.106/24 | cEOS-LAB | Provisioned | - |
| DOMAIN_B_FABRIC | l3leaf | B-LEAF3 | 172.100.100.107/24 | cEOS-LAB | Provisioned | - |
| DOMAIN_B_FABRIC | l3leaf | B-LEAF4 | 172.100.100.108/24 | cEOS-LAB | Provisioned | - |
| DOMAIN_B_FABRIC | l3leaf | B-LEAF5 | 172.100.100.109/24 | cEOS-LAB | Provisioned | - |
| DOMAIN_B_FABRIC | l3leaf | B-LEAF6 | 172.100.100.110/24 | cEOS-LAB | Provisioned | - |
| DOMAIN_B_FABRIC | l3leaf | B-LEAF7 | 172.100.100.111/24 | cEOS-LAB | Provisioned | - |
| DOMAIN_B_FABRIC | l3leaf | B-LEAF8 | 172.100.100.112/24 | cEOS-LAB | Provisioned | - |
| DOMAIN_B_FABRIC | spine | B-SPINE1 | 172.100.100.101/24 | cEOS-LAB | Provisioned | - |
| DOMAIN_B_FABRIC | spine | B-SPINE2 | 172.100.100.102/24 | cEOS-LAB | Provisioned | - |
| DOMAIN_B_FABRIC | spine | B-SPINE3 | 172.100.100.103/24 | cEOS-LAB | Provisioned | - |
| DOMAIN_B_FABRIC | spine | B-SPINE4 | 172.100.100.104/24 | cEOS-LAB | Provisioned | - |
| DOMAIN_B_FABRIC | l2leaf | B-SW1 | 172.100.100.113/24 | cEOS-LAB | Provisioned | - |

> Provision status is based on Ansible inventory declaration and do not represent real status from CloudVision.

### Fabric Switches with inband Management IP

| POD | Type | Node | Management IP | Inband Interface |
| --- | ---- | ---- | ------------- | ---------------- |

## Fabric Topology

| Type | Node | Node Interface | Peer Type | Peer Node | Peer Interface |
| ---- | ---- | -------------- | --------- | ----------| -------------- |
| l3leaf | B-LEAF1 | Ethernet1 | spine | B-SPINE1 | Ethernet1 |
| l3leaf | B-LEAF1 | Ethernet2 | spine | B-SPINE2 | Ethernet1 |
| l3leaf | B-LEAF1 | Ethernet3 | spine | B-SPINE3 | Ethernet1 |
| l3leaf | B-LEAF1 | Ethernet4 | spine | B-SPINE4 | Ethernet1 |
| l3leaf | B-LEAF2 | Ethernet1 | spine | B-SPINE1 | Ethernet2 |
| l3leaf | B-LEAF2 | Ethernet2 | spine | B-SPINE2 | Ethernet2 |
| l3leaf | B-LEAF2 | Ethernet3 | spine | B-SPINE3 | Ethernet2 |
| l3leaf | B-LEAF2 | Ethernet4 | spine | B-SPINE4 | Ethernet2 |
| l3leaf | B-LEAF3 | Ethernet1 | spine | B-SPINE1 | Ethernet3 |
| l3leaf | B-LEAF3 | Ethernet2 | spine | B-SPINE2 | Ethernet3 |
| l3leaf | B-LEAF3 | Ethernet3 | spine | B-SPINE3 | Ethernet3 |
| l3leaf | B-LEAF3 | Ethernet4 | spine | B-SPINE4 | Ethernet3 |
| l3leaf | B-LEAF4 | Ethernet1 | spine | B-SPINE1 | Ethernet4 |
| l3leaf | B-LEAF4 | Ethernet2 | spine | B-SPINE2 | Ethernet4 |
| l3leaf | B-LEAF4 | Ethernet3 | spine | B-SPINE3 | Ethernet4 |
| l3leaf | B-LEAF4 | Ethernet4 | spine | B-SPINE4 | Ethernet4 |
| l3leaf | B-LEAF5 | Ethernet1 | spine | B-SPINE1 | Ethernet5 |
| l3leaf | B-LEAF5 | Ethernet2 | spine | B-SPINE2 | Ethernet5 |
| l3leaf | B-LEAF5 | Ethernet3 | spine | B-SPINE3 | Ethernet5 |
| l3leaf | B-LEAF5 | Ethernet4 | spine | B-SPINE4 | Ethernet5 |
| l3leaf | B-LEAF6 | Ethernet1 | spine | B-SPINE1 | Ethernet6 |
| l3leaf | B-LEAF6 | Ethernet2 | spine | B-SPINE2 | Ethernet6 |
| l3leaf | B-LEAF6 | Ethernet3 | spine | B-SPINE3 | Ethernet6 |
| l3leaf | B-LEAF6 | Ethernet4 | spine | B-SPINE4 | Ethernet6 |
| l3leaf | B-LEAF7 | Ethernet1 | spine | B-SPINE1 | Ethernet7 |
| l3leaf | B-LEAF7 | Ethernet2 | spine | B-SPINE2 | Ethernet7 |
| l3leaf | B-LEAF7 | Ethernet3 | spine | B-SPINE3 | Ethernet7 |
| l3leaf | B-LEAF7 | Ethernet4 | spine | B-SPINE4 | Ethernet7 |
| l3leaf | B-LEAF8 | Ethernet1 | spine | B-SPINE1 | Ethernet8 |
| l3leaf | B-LEAF8 | Ethernet2 | spine | B-SPINE2 | Ethernet8 |
| l3leaf | B-LEAF8 | Ethernet3 | spine | B-SPINE3 | Ethernet8 |
| l3leaf | B-LEAF8 | Ethernet4 | spine | B-SPINE4 | Ethernet8 |

## Fabric IP Allocation

### Fabric Point-To-Point Links

| Uplink IPv4 Pool | Available Addresses | Assigned addresses | Assigned Address % |
| ---------------- | ------------------- | ------------------ | ------------------ |
| 192.168.0.0/24 | 256 | 0 | 0.0 % |

### Point-To-Point Links Node Allocation

| Node | Node Interface | Node IP Address | Peer Node | Peer Interface | Peer IP Address |
| ---- | -------------- | --------------- | --------- | -------------- | --------------- |
| B-LEAF1 | Ethernet1 | unnumbered Loopback0 | B-SPINE1 | Ethernet1 | unnumbered Loopback0 |
| B-LEAF1 | Ethernet2 | unnumbered Loopback0 | B-SPINE2 | Ethernet1 | unnumbered Loopback0 |
| B-LEAF1 | Ethernet3 | unnumbered Loopback0 | B-SPINE3 | Ethernet1 | unnumbered Loopback0 |
| B-LEAF1 | Ethernet4 | unnumbered Loopback0 | B-SPINE4 | Ethernet1 | unnumbered Loopback0 |
| B-LEAF2 | Ethernet1 | unnumbered Loopback0 | B-SPINE1 | Ethernet2 | unnumbered Loopback0 |
| B-LEAF2 | Ethernet2 | unnumbered Loopback0 | B-SPINE2 | Ethernet2 | unnumbered Loopback0 |
| B-LEAF2 | Ethernet3 | unnumbered Loopback0 | B-SPINE3 | Ethernet2 | unnumbered Loopback0 |
| B-LEAF2 | Ethernet4 | unnumbered Loopback0 | B-SPINE4 | Ethernet2 | unnumbered Loopback0 |
| B-LEAF3 | Ethernet1 | unnumbered Loopback0 | B-SPINE1 | Ethernet3 | unnumbered Loopback0 |
| B-LEAF3 | Ethernet2 | unnumbered Loopback0 | B-SPINE2 | Ethernet3 | unnumbered Loopback0 |
| B-LEAF3 | Ethernet3 | unnumbered Loopback0 | B-SPINE3 | Ethernet3 | unnumbered Loopback0 |
| B-LEAF3 | Ethernet4 | unnumbered Loopback0 | B-SPINE4 | Ethernet3 | unnumbered Loopback0 |
| B-LEAF4 | Ethernet1 | unnumbered Loopback0 | B-SPINE1 | Ethernet4 | unnumbered Loopback0 |
| B-LEAF4 | Ethernet2 | unnumbered Loopback0 | B-SPINE2 | Ethernet4 | unnumbered Loopback0 |
| B-LEAF4 | Ethernet3 | unnumbered Loopback0 | B-SPINE3 | Ethernet4 | unnumbered Loopback0 |
| B-LEAF4 | Ethernet4 | unnumbered Loopback0 | B-SPINE4 | Ethernet4 | unnumbered Loopback0 |
| B-LEAF5 | Ethernet1 | unnumbered Loopback0 | B-SPINE1 | Ethernet5 | unnumbered Loopback0 |
| B-LEAF5 | Ethernet2 | unnumbered Loopback0 | B-SPINE2 | Ethernet5 | unnumbered Loopback0 |
| B-LEAF5 | Ethernet3 | unnumbered Loopback0 | B-SPINE3 | Ethernet5 | unnumbered Loopback0 |
| B-LEAF5 | Ethernet4 | unnumbered Loopback0 | B-SPINE4 | Ethernet5 | unnumbered Loopback0 |
| B-LEAF6 | Ethernet1 | unnumbered Loopback0 | B-SPINE1 | Ethernet6 | unnumbered Loopback0 |
| B-LEAF6 | Ethernet2 | unnumbered Loopback0 | B-SPINE2 | Ethernet6 | unnumbered Loopback0 |
| B-LEAF6 | Ethernet3 | unnumbered Loopback0 | B-SPINE3 | Ethernet6 | unnumbered Loopback0 |
| B-LEAF6 | Ethernet4 | unnumbered Loopback0 | B-SPINE4 | Ethernet6 | unnumbered Loopback0 |
| B-LEAF7 | Ethernet1 | unnumbered Loopback0 | B-SPINE1 | Ethernet7 | unnumbered Loopback0 |
| B-LEAF7 | Ethernet2 | unnumbered Loopback0 | B-SPINE2 | Ethernet7 | unnumbered Loopback0 |
| B-LEAF7 | Ethernet3 | unnumbered Loopback0 | B-SPINE3 | Ethernet7 | unnumbered Loopback0 |
| B-LEAF7 | Ethernet4 | unnumbered Loopback0 | B-SPINE4 | Ethernet7 | unnumbered Loopback0 |
| B-LEAF8 | Ethernet1 | unnumbered Loopback0 | B-SPINE1 | Ethernet8 | unnumbered Loopback0 |
| B-LEAF8 | Ethernet2 | unnumbered Loopback0 | B-SPINE2 | Ethernet8 | unnumbered Loopback0 |
| B-LEAF8 | Ethernet3 | unnumbered Loopback0 | B-SPINE3 | Ethernet8 | unnumbered Loopback0 |
| B-LEAF8 | Ethernet4 | unnumbered Loopback0 | B-SPINE4 | Ethernet8 | unnumbered Loopback0 |

### Loopback Interfaces (BGP EVPN Peering)

| Loopback Pool | Available Addresses | Assigned addresses | Assigned Address % |
| ------------- | ------------------- | ------------------ | ------------------ |
| 1.1.2.0/24 | 256 | 12 | 4.69 % |

### Loopback0 Interfaces Node Allocation

| POD | Node | Loopback0 |
| --- | ---- | --------- |
| DOMAIN_B_FABRIC | B-LEAF1 | 1.1.2.1/32 |
| DOMAIN_B_FABRIC | B-LEAF2 | 1.1.2.2/32 |
| DOMAIN_B_FABRIC | B-LEAF3 | 1.1.2.3/32 |
| DOMAIN_B_FABRIC | B-LEAF4 | 1.1.2.4/32 |
| DOMAIN_B_FABRIC | B-LEAF5 | 1.1.2.5/32 |
| DOMAIN_B_FABRIC | B-LEAF6 | 1.1.2.6/32 |
| DOMAIN_B_FABRIC | B-LEAF7 | 1.1.2.7/32 |
| DOMAIN_B_FABRIC | B-LEAF8 | 1.1.2.8/32 |
| DOMAIN_B_FABRIC | B-SPINE1 | 1.1.2.201/32 |
| DOMAIN_B_FABRIC | B-SPINE2 | 1.1.2.202/32 |
| DOMAIN_B_FABRIC | B-SPINE3 | 1.1.2.203/32 |
| DOMAIN_B_FABRIC | B-SPINE4 | 1.1.2.204/32 |

### ISIS CLNS interfaces

| POD | Node | CLNS Address |
| --- | ---- | ------------ |
| DOMAIN_B_FABRIC | B-LEAF1 | 49.1111.0010.0100.2001.00 |
| DOMAIN_B_FABRIC | B-LEAF2 | 49.1111.0010.0100.2002.00 |
| DOMAIN_B_FABRIC | B-LEAF3 | 49.1111.0010.0100.2003.00 |
| DOMAIN_B_FABRIC | B-LEAF4 | 49.1111.0010.0100.2004.00 |
| DOMAIN_B_FABRIC | B-LEAF5 | 49.1111.0010.0100.2005.00 |
| DOMAIN_B_FABRIC | B-LEAF6 | 49.1111.0010.0100.2006.00 |
| DOMAIN_B_FABRIC | B-LEAF7 | 49.1111.0010.0100.2007.00 |
| DOMAIN_B_FABRIC | B-LEAF8 | 49.1111.0010.0100.2008.00 |
| DOMAIN_B_FABRIC | B-SPINE1 | 49.1111.0010.0100.2201.00 |
| DOMAIN_B_FABRIC | B-SPINE2 | 49.1111.0010.0100.2202.00 |
| DOMAIN_B_FABRIC | B-SPINE3 | 49.1111.0010.0100.2203.00 |
| DOMAIN_B_FABRIC | B-SPINE4 | 49.1111.0010.0100.2204.00 |

### VTEP Loopback VXLAN Tunnel Source Interfaces (VTEPs Only)

| VTEP Loopback Pool | Available Addresses | Assigned addresses | Assigned Address % |
| ------------------ | ------------------- | ------------------ | ------------------ |
| 2.2.2.0/24 | 256 | 8 | 3.13 % |

### VTEP Loopback Node allocation

| POD | Node | Loopback1 |
| --- | ---- | --------- |
| DOMAIN_B_FABRIC | B-LEAF1 | 2.2.2.1/32 |
| DOMAIN_B_FABRIC | B-LEAF2 | 2.2.2.2/32 |
| DOMAIN_B_FABRIC | B-LEAF3 | 2.2.2.3/32 |
| DOMAIN_B_FABRIC | B-LEAF4 | 2.2.2.4/32 |
| DOMAIN_B_FABRIC | B-LEAF5 | 2.2.2.5/32 |
| DOMAIN_B_FABRIC | B-LEAF6 | 2.2.2.6/32 |
| DOMAIN_B_FABRIC | B-LEAF7 | 2.2.2.7/32 |
| DOMAIN_B_FABRIC | B-LEAF8 | 2.2.2.8/32 |
