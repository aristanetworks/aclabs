# DOMAIN_A_FABRIC

## Table of Contents

- [Fabric Switches and Management IP](#fabric-switches-and-management-ip)
  - [Fabric Switches with inband Management IP](#fabric-switches-with-inband-management-ip)
- [Fabric Topology](#fabric-topology)
- [Fabric IP Allocation](#fabric-ip-allocation)
  - [Fabric Point-To-Point Links](#fabric-point-to-point-links)
  - [Point-To-Point Links Node Allocation](#point-to-point-links-node-allocation)
  - [Loopback Interfaces (BGP EVPN Peering)](#loopback-interfaces-bgp-evpn-peering)
  - [Loopback0 Interfaces Node Allocation](#loopback0-interfaces-node-allocation)
  - [VTEP Loopback VXLAN Tunnel Source Interfaces (VTEPs Only)](#vtep-loopback-vxlan-tunnel-source-interfaces-vteps-only)
  - [VTEP Loopback Node allocation](#vtep-loopback-node-allocation)

## Fabric Switches and Management IP

| POD | Type | Node | Management IP | Platform | Provisioned in CloudVision | Serial Number |
| --- | ---- | ---- | ------------- | -------- | -------------------------- | ------------- |
| DOMAIN_A_FABRIC | l3leaf | A-LEAF1 | 172.100.100.105/24 | cEOS-LAB | Provisioned | - |
| DOMAIN_A_FABRIC | l3leaf | A-LEAF2 | 172.100.100.106/24 | cEOS-LAB | Provisioned | - |
| DOMAIN_A_FABRIC | l3leaf | A-LEAF3 | 172.100.100.107/24 | cEOS-LAB | Provisioned | - |
| DOMAIN_A_FABRIC | l3leaf | A-LEAF4 | 172.100.100.108/24 | cEOS-LAB | Provisioned | - |
| DOMAIN_A_FABRIC | l3leaf | A-LEAF5 | 172.100.100.109/24 | cEOS-LAB | Provisioned | - |
| DOMAIN_A_FABRIC | l3leaf | A-LEAF6 | 172.100.100.110/24 | cEOS-LAB | Provisioned | - |
| DOMAIN_A_FABRIC | l3leaf | A-LEAF7 | 172.100.100.111/24 | cEOS-LAB | Provisioned | - |
| DOMAIN_A_FABRIC | l3leaf | A-LEAF8 | 172.100.100.112/24 | cEOS-LAB | Provisioned | - |
| DOMAIN_A_FABRIC | spine | A-SPINE1 | 172.100.100.101/24 | cEOS-LAB | Provisioned | - |
| DOMAIN_A_FABRIC | spine | A-SPINE2 | 172.100.100.102/24 | cEOS-LAB | Provisioned | - |
| DOMAIN_A_FABRIC | spine | A-SPINE3 | 172.100.100.103/24 | cEOS-LAB | Provisioned | - |
| DOMAIN_A_FABRIC | spine | A-SPINE4 | 172.100.100.104/24 | cEOS-LAB | Provisioned | - |

> Provision status is based on Ansible inventory declaration and do not represent real status from CloudVision.

### Fabric Switches with inband Management IP

| POD | Type | Node | Management IP | Inband Interface |
| --- | ---- | ---- | ------------- | ---------------- |

## Fabric Topology

| Type | Node | Node Interface | Peer Type | Peer Node | Peer Interface |
| ---- | ---- | -------------- | --------- | ----------| -------------- |
| l3leaf | A-LEAF1 | Ethernet1 | spine | A-SPINE1 | Ethernet1 |
| l3leaf | A-LEAF1 | Ethernet2 | spine | A-SPINE2 | Ethernet1 |
| l3leaf | A-LEAF1 | Ethernet3 | spine | A-SPINE3 | Ethernet1 |
| l3leaf | A-LEAF1 | Ethernet4 | spine | A-SPINE4 | Ethernet1 |
| l3leaf | A-LEAF1 | Ethernet5 | mlag_peer | A-LEAF2 | Ethernet5 |
| l3leaf | A-LEAF1 | Ethernet6 | mlag_peer | A-LEAF2 | Ethernet6 |
| l3leaf | A-LEAF2 | Ethernet1 | spine | A-SPINE1 | Ethernet2 |
| l3leaf | A-LEAF2 | Ethernet2 | spine | A-SPINE2 | Ethernet2 |
| l3leaf | A-LEAF2 | Ethernet3 | spine | A-SPINE3 | Ethernet2 |
| l3leaf | A-LEAF2 | Ethernet4 | spine | A-SPINE4 | Ethernet2 |
| l3leaf | A-LEAF3 | Ethernet1 | spine | A-SPINE1 | Ethernet3 |
| l3leaf | A-LEAF3 | Ethernet2 | spine | A-SPINE2 | Ethernet3 |
| l3leaf | A-LEAF3 | Ethernet3 | spine | A-SPINE3 | Ethernet3 |
| l3leaf | A-LEAF3 | Ethernet4 | spine | A-SPINE4 | Ethernet3 |
| l3leaf | A-LEAF3 | Ethernet5 | mlag_peer | A-LEAF4 | Ethernet5 |
| l3leaf | A-LEAF3 | Ethernet6 | mlag_peer | A-LEAF4 | Ethernet6 |
| l3leaf | A-LEAF4 | Ethernet1 | spine | A-SPINE1 | Ethernet4 |
| l3leaf | A-LEAF4 | Ethernet2 | spine | A-SPINE2 | Ethernet4 |
| l3leaf | A-LEAF4 | Ethernet3 | spine | A-SPINE3 | Ethernet4 |
| l3leaf | A-LEAF4 | Ethernet4 | spine | A-SPINE4 | Ethernet4 |
| l3leaf | A-LEAF5 | Ethernet1 | spine | A-SPINE1 | Ethernet5 |
| l3leaf | A-LEAF5 | Ethernet2 | spine | A-SPINE2 | Ethernet5 |
| l3leaf | A-LEAF5 | Ethernet3 | spine | A-SPINE3 | Ethernet5 |
| l3leaf | A-LEAF5 | Ethernet4 | spine | A-SPINE4 | Ethernet5 |
| l3leaf | A-LEAF5 | Ethernet5 | mlag_peer | A-LEAF6 | Ethernet5 |
| l3leaf | A-LEAF5 | Ethernet6 | mlag_peer | A-LEAF6 | Ethernet6 |
| l3leaf | A-LEAF6 | Ethernet1 | spine | A-SPINE1 | Ethernet6 |
| l3leaf | A-LEAF6 | Ethernet2 | spine | A-SPINE2 | Ethernet6 |
| l3leaf | A-LEAF6 | Ethernet3 | spine | A-SPINE3 | Ethernet6 |
| l3leaf | A-LEAF6 | Ethernet4 | spine | A-SPINE4 | Ethernet6 |
| l3leaf | A-LEAF7 | Ethernet1 | spine | A-SPINE1 | Ethernet7 |
| l3leaf | A-LEAF7 | Ethernet2 | spine | A-SPINE2 | Ethernet7 |
| l3leaf | A-LEAF7 | Ethernet3 | spine | A-SPINE3 | Ethernet7 |
| l3leaf | A-LEAF7 | Ethernet4 | spine | A-SPINE4 | Ethernet7 |
| l3leaf | A-LEAF7 | Ethernet5 | mlag_peer | A-LEAF8 | Ethernet5 |
| l3leaf | A-LEAF7 | Ethernet6 | mlag_peer | A-LEAF8 | Ethernet6 |
| l3leaf | A-LEAF8 | Ethernet1 | spine | A-SPINE1 | Ethernet8 |
| l3leaf | A-LEAF8 | Ethernet2 | spine | A-SPINE2 | Ethernet8 |
| l3leaf | A-LEAF8 | Ethernet3 | spine | A-SPINE3 | Ethernet8 |
| l3leaf | A-LEAF8 | Ethernet4 | spine | A-SPINE4 | Ethernet8 |

## Fabric IP Allocation

### Fabric Point-To-Point Links

| Uplink IPv4 Pool | Available Addresses | Assigned addresses | Assigned Address % |
| ---------------- | ------------------- | ------------------ | ------------------ |
| 192.168.0.0/24 | 256 | 64 | 25.0 % |

### Point-To-Point Links Node Allocation

| Node | Node Interface | Node IP Address | Peer Node | Peer Interface | Peer IP Address |
| ---- | -------------- | --------------- | --------- | -------------- | --------------- |
| A-LEAF1 | Ethernet1 | 192.168.0.1/31 | A-SPINE1 | Ethernet1 | 192.168.0.0/31 |
| A-LEAF1 | Ethernet2 | 192.168.0.3/31 | A-SPINE2 | Ethernet1 | 192.168.0.2/31 |
| A-LEAF1 | Ethernet3 | 192.168.0.5/31 | A-SPINE3 | Ethernet1 | 192.168.0.4/31 |
| A-LEAF1 | Ethernet4 | 192.168.0.7/31 | A-SPINE4 | Ethernet1 | 192.168.0.6/31 |
| A-LEAF2 | Ethernet1 | 192.168.0.9/31 | A-SPINE1 | Ethernet2 | 192.168.0.8/31 |
| A-LEAF2 | Ethernet2 | 192.168.0.11/31 | A-SPINE2 | Ethernet2 | 192.168.0.10/31 |
| A-LEAF2 | Ethernet3 | 192.168.0.13/31 | A-SPINE3 | Ethernet2 | 192.168.0.12/31 |
| A-LEAF2 | Ethernet4 | 192.168.0.15/31 | A-SPINE4 | Ethernet2 | 192.168.0.14/31 |
| A-LEAF3 | Ethernet1 | 192.168.0.17/31 | A-SPINE1 | Ethernet3 | 192.168.0.16/31 |
| A-LEAF3 | Ethernet2 | 192.168.0.19/31 | A-SPINE2 | Ethernet3 | 192.168.0.18/31 |
| A-LEAF3 | Ethernet3 | 192.168.0.21/31 | A-SPINE3 | Ethernet3 | 192.168.0.20/31 |
| A-LEAF3 | Ethernet4 | 192.168.0.23/31 | A-SPINE4 | Ethernet3 | 192.168.0.22/31 |
| A-LEAF4 | Ethernet1 | 192.168.0.25/31 | A-SPINE1 | Ethernet4 | 192.168.0.24/31 |
| A-LEAF4 | Ethernet2 | 192.168.0.27/31 | A-SPINE2 | Ethernet4 | 192.168.0.26/31 |
| A-LEAF4 | Ethernet3 | 192.168.0.29/31 | A-SPINE3 | Ethernet4 | 192.168.0.28/31 |
| A-LEAF4 | Ethernet4 | 192.168.0.31/31 | A-SPINE4 | Ethernet4 | 192.168.0.30/31 |
| A-LEAF5 | Ethernet1 | 192.168.0.33/31 | A-SPINE1 | Ethernet5 | 192.168.0.32/31 |
| A-LEAF5 | Ethernet2 | 192.168.0.35/31 | A-SPINE2 | Ethernet5 | 192.168.0.34/31 |
| A-LEAF5 | Ethernet3 | 192.168.0.37/31 | A-SPINE3 | Ethernet5 | 192.168.0.36/31 |
| A-LEAF5 | Ethernet4 | 192.168.0.39/31 | A-SPINE4 | Ethernet5 | 192.168.0.38/31 |
| A-LEAF6 | Ethernet1 | 192.168.0.41/31 | A-SPINE1 | Ethernet6 | 192.168.0.40/31 |
| A-LEAF6 | Ethernet2 | 192.168.0.43/31 | A-SPINE2 | Ethernet6 | 192.168.0.42/31 |
| A-LEAF6 | Ethernet3 | 192.168.0.45/31 | A-SPINE3 | Ethernet6 | 192.168.0.44/31 |
| A-LEAF6 | Ethernet4 | 192.168.0.47/31 | A-SPINE4 | Ethernet6 | 192.168.0.46/31 |
| A-LEAF7 | Ethernet1 | 192.168.0.49/31 | A-SPINE1 | Ethernet7 | 192.168.0.48/31 |
| A-LEAF7 | Ethernet2 | 192.168.0.51/31 | A-SPINE2 | Ethernet7 | 192.168.0.50/31 |
| A-LEAF7 | Ethernet3 | 192.168.0.53/31 | A-SPINE3 | Ethernet7 | 192.168.0.52/31 |
| A-LEAF7 | Ethernet4 | 192.168.0.55/31 | A-SPINE4 | Ethernet7 | 192.168.0.54/31 |
| A-LEAF8 | Ethernet1 | 192.168.0.57/31 | A-SPINE1 | Ethernet8 | 192.168.0.56/31 |
| A-LEAF8 | Ethernet2 | 192.168.0.59/31 | A-SPINE2 | Ethernet8 | 192.168.0.58/31 |
| A-LEAF8 | Ethernet3 | 192.168.0.61/31 | A-SPINE3 | Ethernet8 | 192.168.0.60/31 |
| A-LEAF8 | Ethernet4 | 192.168.0.63/31 | A-SPINE4 | Ethernet8 | 192.168.0.62/31 |

### Loopback Interfaces (BGP EVPN Peering)

| Loopback Pool | Available Addresses | Assigned addresses | Assigned Address % |
| ------------- | ------------------- | ------------------ | ------------------ |
| 1.1.1.0/24 | 256 | 12 | 4.69 % |

### Loopback0 Interfaces Node Allocation

| POD | Node | Loopback0 |
| --- | ---- | --------- |
| DOMAIN_A_FABRIC | A-LEAF1 | 1.1.1.1/32 |
| DOMAIN_A_FABRIC | A-LEAF2 | 1.1.1.2/32 |
| DOMAIN_A_FABRIC | A-LEAF3 | 1.1.1.3/32 |
| DOMAIN_A_FABRIC | A-LEAF4 | 1.1.1.4/32 |
| DOMAIN_A_FABRIC | A-LEAF5 | 1.1.1.5/32 |
| DOMAIN_A_FABRIC | A-LEAF6 | 1.1.1.6/32 |
| DOMAIN_A_FABRIC | A-LEAF7 | 1.1.1.7/32 |
| DOMAIN_A_FABRIC | A-LEAF8 | 1.1.1.8/32 |
| DOMAIN_A_FABRIC | A-SPINE1 | 1.1.1.201/32 |
| DOMAIN_A_FABRIC | A-SPINE2 | 1.1.1.202/32 |
| DOMAIN_A_FABRIC | A-SPINE3 | 1.1.1.203/32 |
| DOMAIN_A_FABRIC | A-SPINE4 | 1.1.1.204/32 |

### VTEP Loopback VXLAN Tunnel Source Interfaces (VTEPs Only)

| VTEP Loopback Pool | Available Addresses | Assigned addresses | Assigned Address % |
| ------------------ | ------------------- | ------------------ | ------------------ |
| 2.2.1.0/24 | 256 | 8 | 3.13 % |

### VTEP Loopback Node allocation

| POD | Node | Loopback1 |
| --- | ---- | --------- |
| DOMAIN_A_FABRIC | A-LEAF1 | 2.2.1.1/32 |
| DOMAIN_A_FABRIC | A-LEAF2 | 2.2.1.1/32 |
| DOMAIN_A_FABRIC | A-LEAF3 | 2.2.1.3/32 |
| DOMAIN_A_FABRIC | A-LEAF4 | 2.2.1.3/32 |
| DOMAIN_A_FABRIC | A-LEAF5 | 2.2.1.5/32 |
| DOMAIN_A_FABRIC | A-LEAF6 | 2.2.1.5/32 |
| DOMAIN_A_FABRIC | A-LEAF7 | 2.2.1.7/32 |
| DOMAIN_A_FABRIC | A-LEAF8 | 2.2.1.7/32 |
