# FABRIC

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
| domain-a | l3leaf | A-LEAF1 | 192.168.0.101/24 | vEOS-lab | Provisioned | - |
| domain-a | l3leaf | A-LEAF2 | 192.168.0.102/24 | vEOS-lab | Provisioned | - |
| domain-a | l3leaf | A-LEAF3 | 192.168.0.103/24 | vEOS-lab | Provisioned | - |
| domain-a | l3leaf | A-LEAF4 | 192.168.0.104/24 | vEOS-lab | Provisioned | - |
| domain-a | l3leaf | A-LEAF5 | 192.168.0.105/24 | vEOS-lab | Provisioned | - |
| domain-a | l3leaf | A-LEAF6 | 192.168.0.106/24 | vEOS-lab | Provisioned | - |
| domain-a | l3leaf | A-LEAF7 | 192.168.0.107/24 | vEOS-lab | Provisioned | - |
| domain-a | l3leaf | A-LEAF8 | 192.168.0.108/24 | vEOS-lab | Provisioned | - |
| domain-a | spine | A-SPINE1 | 192.168.0.11/24 | vEOS-lab | Provisioned | - |
| domain-a | spine | A-SPINE2 | 192.168.0.12/24 | vEOS-lab | Provisioned | - |
| domain-a | spine | A-SPINE3 | 192.168.0.13/24 | vEOS-lab | Provisioned | - |
| domain-a | spine | A-SPINE4 | 192.168.0.14/24 | vEOS-lab | Provisioned | - |

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
| 192.168.1.0/24 | 256 | 64 | 25.0 % |

### Point-To-Point Links Node Allocation

| Node | Node Interface | Node IP Address | Peer Node | Peer Interface | Peer IP Address |
| ---- | -------------- | --------------- | --------- | -------------- | --------------- |
| A-LEAF1 | Ethernet1 | 192.168.1.1/31 | A-SPINE1 | Ethernet1 | 192.168.1.0/31 |
| A-LEAF1 | Ethernet2 | 192.168.1.3/31 | A-SPINE2 | Ethernet1 | 192.168.1.2/31 |
| A-LEAF1 | Ethernet3 | 192.168.1.5/31 | A-SPINE3 | Ethernet1 | 192.168.1.4/31 |
| A-LEAF1 | Ethernet4 | 192.168.1.7/31 | A-SPINE4 | Ethernet1 | 192.168.1.6/31 |
| A-LEAF2 | Ethernet1 | 192.168.1.9/31 | A-SPINE1 | Ethernet2 | 192.168.1.8/31 |
| A-LEAF2 | Ethernet2 | 192.168.1.11/31 | A-SPINE2 | Ethernet2 | 192.168.1.10/31 |
| A-LEAF2 | Ethernet3 | 192.168.1.13/31 | A-SPINE3 | Ethernet2 | 192.168.1.12/31 |
| A-LEAF2 | Ethernet4 | 192.168.1.15/31 | A-SPINE4 | Ethernet2 | 192.168.1.14/31 |
| A-LEAF3 | Ethernet1 | 192.168.1.17/31 | A-SPINE1 | Ethernet3 | 192.168.1.16/31 |
| A-LEAF3 | Ethernet2 | 192.168.1.19/31 | A-SPINE2 | Ethernet3 | 192.168.1.18/31 |
| A-LEAF3 | Ethernet3 | 192.168.1.21/31 | A-SPINE3 | Ethernet3 | 192.168.1.20/31 |
| A-LEAF3 | Ethernet4 | 192.168.1.23/31 | A-SPINE4 | Ethernet3 | 192.168.1.22/31 |
| A-LEAF4 | Ethernet1 | 192.168.1.25/31 | A-SPINE1 | Ethernet4 | 192.168.1.24/31 |
| A-LEAF4 | Ethernet2 | 192.168.1.27/31 | A-SPINE2 | Ethernet4 | 192.168.1.26/31 |
| A-LEAF4 | Ethernet3 | 192.168.1.29/31 | A-SPINE3 | Ethernet4 | 192.168.1.28/31 |
| A-LEAF4 | Ethernet4 | 192.168.1.31/31 | A-SPINE4 | Ethernet4 | 192.168.1.30/31 |
| A-LEAF5 | Ethernet1 | 192.168.1.33/31 | A-SPINE1 | Ethernet5 | 192.168.1.32/31 |
| A-LEAF5 | Ethernet2 | 192.168.1.35/31 | A-SPINE2 | Ethernet5 | 192.168.1.34/31 |
| A-LEAF5 | Ethernet3 | 192.168.1.37/31 | A-SPINE3 | Ethernet5 | 192.168.1.36/31 |
| A-LEAF5 | Ethernet4 | 192.168.1.39/31 | A-SPINE4 | Ethernet5 | 192.168.1.38/31 |
| A-LEAF6 | Ethernet1 | 192.168.1.41/31 | A-SPINE1 | Ethernet6 | 192.168.1.40/31 |
| A-LEAF6 | Ethernet2 | 192.168.1.43/31 | A-SPINE2 | Ethernet6 | 192.168.1.42/31 |
| A-LEAF6 | Ethernet3 | 192.168.1.45/31 | A-SPINE3 | Ethernet6 | 192.168.1.44/31 |
| A-LEAF6 | Ethernet4 | 192.168.1.47/31 | A-SPINE4 | Ethernet6 | 192.168.1.46/31 |
| A-LEAF7 | Ethernet1 | 192.168.1.49/31 | A-SPINE1 | Ethernet7 | 192.168.1.48/31 |
| A-LEAF7 | Ethernet2 | 192.168.1.51/31 | A-SPINE2 | Ethernet7 | 192.168.1.50/31 |
| A-LEAF7 | Ethernet3 | 192.168.1.53/31 | A-SPINE3 | Ethernet7 | 192.168.1.52/31 |
| A-LEAF7 | Ethernet4 | 192.168.1.55/31 | A-SPINE4 | Ethernet7 | 192.168.1.54/31 |
| A-LEAF8 | Ethernet1 | 192.168.1.57/31 | A-SPINE1 | Ethernet8 | 192.168.1.56/31 |
| A-LEAF8 | Ethernet2 | 192.168.1.59/31 | A-SPINE2 | Ethernet8 | 192.168.1.58/31 |
| A-LEAF8 | Ethernet3 | 192.168.1.61/31 | A-SPINE3 | Ethernet8 | 192.168.1.60/31 |
| A-LEAF8 | Ethernet4 | 192.168.1.63/31 | A-SPINE4 | Ethernet8 | 192.168.1.62/31 |

### Loopback Interfaces (BGP EVPN Peering)

| Loopback Pool | Available Addresses | Assigned addresses | Assigned Address % |
| ------------- | ------------------- | ------------------ | ------------------ |
| 10.0.0.0/24 | 256 | 12 | 4.69 % |

### Loopback0 Interfaces Node Allocation

| POD | Node | Loopback0 |
| --- | ---- | --------- |
| domain-a | A-LEAF1 | 10.0.0.5/32 |
| domain-a | A-LEAF2 | 10.0.0.6/32 |
| domain-a | A-LEAF3 | 10.0.0.7/32 |
| domain-a | A-LEAF4 | 10.0.0.8/32 |
| domain-a | A-LEAF5 | 10.0.0.9/32 |
| domain-a | A-LEAF6 | 10.0.0.10/32 |
| domain-a | A-LEAF7 | 10.0.0.11/32 |
| domain-a | A-LEAF8 | 10.0.0.12/32 |
| domain-a | A-SPINE1 | 10.0.0.1/32 |
| domain-a | A-SPINE2 | 10.0.0.2/32 |
| domain-a | A-SPINE3 | 10.0.0.3/32 |
| domain-a | A-SPINE4 | 10.0.0.4/32 |

### VTEP Loopback VXLAN Tunnel Source Interfaces (VTEPs Only)

| VTEP Loopback Pool | Available Addresses | Assigned addresses | Assigned Address % |
| --------------------- | ------------------- | ------------------ | ------------------ |
| 10.1.1.0/24 | 256 | 8 | 3.13 % |

### VTEP Loopback Node allocation

| POD | Node | Loopback1 |
| --- | ---- | --------- |
| domain-a | A-LEAF1 | 10.1.1.5/32 |
| domain-a | A-LEAF2 | 10.1.1.5/32 |
| domain-a | A-LEAF3 | 10.1.1.7/32 |
| domain-a | A-LEAF4 | 10.1.1.7/32 |
| domain-a | A-LEAF5 | 10.1.1.9/32 |
| domain-a | A-LEAF6 | 10.1.1.9/32 |
| domain-a | A-LEAF7 | 10.1.1.11/32 |
| domain-a | A-LEAF8 | 10.1.1.11/32 |
