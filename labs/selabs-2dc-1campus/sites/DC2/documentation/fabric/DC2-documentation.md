# DC2

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
| DC2_POD | l3leaf | dc2-brdr1 | 192.168.0.200/24 | 7280R3 | Provisioned | - |
| DC2_POD | l3leaf | dc2-brdr2 | 192.168.0.201/24 | 7280R3 | Provisioned | - |
| DC2_POD | l3leaf | dc2-leaf1 | 192.168.0.22/24 | 7050X3 | Provisioned | - |
| DC2_POD | l3leaf | dc2-leaf2 | 192.168.0.23/24 | 7050X3 | Provisioned | - |
| DC2_POD | l3leaf | dc2-leaf3 | 192.168.0.24/24 | 7050X3 | Provisioned | - |
| DC2_POD | l3leaf | dc2-leaf4 | 192.168.0.25/24 | 7050X3 | Provisioned | - |
| DC2 | spine | dc2-spine1 | 192.168.0.20/24 | 7500R3 | Provisioned | - |
| DC2 | spine | dc2-spine2 | 192.168.0.21/24 | 7500R3 | Provisioned | - |

> Provision status is based on Ansible inventory declaration and do not represent real status from CloudVision.

### Fabric Switches with inband Management IP

| POD | Type | Node | Management IP | Inband Interface |
| --- | ---- | ---- | ------------- | ---------------- |

## Fabric Topology

| Type | Node | Node Interface | Peer Type | Peer Node | Peer Interface |
| ---- | ---- | -------------- | --------- | --------- | -------------- |
| l3leaf | dc2-brdr1 | Ethernet49/1 | spine | dc2-spine1 | Ethernet1/1 |
| l3leaf | dc2-brdr1 | Ethernet50/1 | spine | dc2-spine2 | Ethernet1/1 |
| l3leaf | dc2-brdr1 | Ethernet51/1 | mlag_peer | dc2-brdr2 | Ethernet51/1 |
| l3leaf | dc2-brdr1 | Ethernet52/1 | mlag_peer | dc2-brdr2 | Ethernet52/1 |
| l3leaf | dc2-brdr2 | Ethernet49/1 | spine | dc2-spine1 | Ethernet1/2 |
| l3leaf | dc2-brdr2 | Ethernet50/1 | spine | dc2-spine2 | Ethernet1/2 |
| l3leaf | dc2-leaf1 | Ethernet49/1 | spine | dc2-spine1 | Ethernet1/3 |
| l3leaf | dc2-leaf1 | Ethernet50/1 | spine | dc2-spine2 | Ethernet1/3 |
| l3leaf | dc2-leaf1 | Ethernet51/1 | mlag_peer | dc2-leaf2 | Ethernet51/1 |
| l3leaf | dc2-leaf1 | Ethernet52/1 | mlag_peer | dc2-leaf2 | Ethernet52/1 |
| l3leaf | dc2-leaf2 | Ethernet49/1 | spine | dc2-spine1 | Ethernet1/4 |
| l3leaf | dc2-leaf2 | Ethernet50/1 | spine | dc2-spine2 | Ethernet1/4 |
| l3leaf | dc2-leaf3 | Ethernet49/1 | spine | dc2-spine1 | Ethernet1/5 |
| l3leaf | dc2-leaf3 | Ethernet50/1 | spine | dc2-spine2 | Ethernet1/5 |
| l3leaf | dc2-leaf3 | Ethernet51/1 | mlag_peer | dc2-leaf4 | Ethernet51/1 |
| l3leaf | dc2-leaf3 | Ethernet52/1 | mlag_peer | dc2-leaf4 | Ethernet52/1 |
| l3leaf | dc2-leaf4 | Ethernet49/1 | spine | dc2-spine1 | Ethernet1/6 |
| l3leaf | dc2-leaf4 | Ethernet50/1 | spine | dc2-spine2 | Ethernet1/6 |

## Fabric IP Allocation

### Fabric Point-To-Point Links

| Uplink IPv4 Pool | Available Addresses | Assigned addresses | Assigned Address % |
| ---------------- | ------------------- | ------------------ | ------------------ |
| 10.102.0.0/24 | 256 | 24 | 9.38 % |

### Point-To-Point Links Node Allocation

| Node | Node Interface | Node IP Address | Peer Node | Peer Interface | Peer IP Address |
| ---- | -------------- | --------------- | --------- | -------------- | --------------- |
| dc2-brdr1 | Ethernet49/1 | 10.102.0.1/31 | dc2-spine1 | Ethernet1/1 | 10.102.0.0/31 |
| dc2-brdr1 | Ethernet50/1 | 10.102.0.3/31 | dc2-spine2 | Ethernet1/1 | 10.102.0.2/31 |
| dc2-brdr2 | Ethernet49/1 | 10.102.0.5/31 | dc2-spine1 | Ethernet1/2 | 10.102.0.4/31 |
| dc2-brdr2 | Ethernet50/1 | 10.102.0.7/31 | dc2-spine2 | Ethernet1/2 | 10.102.0.6/31 |
| dc2-leaf1 | Ethernet49/1 | 10.102.0.9/31 | dc2-spine1 | Ethernet1/3 | 10.102.0.8/31 |
| dc2-leaf1 | Ethernet50/1 | 10.102.0.11/31 | dc2-spine2 | Ethernet1/3 | 10.102.0.10/31 |
| dc2-leaf2 | Ethernet49/1 | 10.102.0.13/31 | dc2-spine1 | Ethernet1/4 | 10.102.0.12/31 |
| dc2-leaf2 | Ethernet50/1 | 10.102.0.15/31 | dc2-spine2 | Ethernet1/4 | 10.102.0.14/31 |
| dc2-leaf3 | Ethernet49/1 | 10.102.0.17/31 | dc2-spine1 | Ethernet1/5 | 10.102.0.16/31 |
| dc2-leaf3 | Ethernet50/1 | 10.102.0.19/31 | dc2-spine2 | Ethernet1/5 | 10.102.0.18/31 |
| dc2-leaf4 | Ethernet49/1 | 10.102.0.21/31 | dc2-spine1 | Ethernet1/6 | 10.102.0.20/31 |
| dc2-leaf4 | Ethernet50/1 | 10.102.0.23/31 | dc2-spine2 | Ethernet1/6 | 10.102.0.22/31 |

### Loopback Interfaces (BGP EVPN Peering)

| Loopback Pool | Available Addresses | Assigned addresses | Assigned Address % |
| ------------- | ------------------- | ------------------ | ------------------ |
| 10.99.2.0/25 | 128 | 6 | 4.69 % |
| 10.99.2.128/25 | 128 | 2 | 1.57 % |

### Loopback0 Interfaces Node Allocation

| POD | Node | Loopback0 |
| --- | ---- | --------- |
| DC2_POD | dc2-brdr1 | 10.99.2.1/32 |
| DC2_POD | dc2-brdr2 | 10.99.2.2/32 |
| DC2_POD | dc2-leaf1 | 10.99.2.3/32 |
| DC2_POD | dc2-leaf2 | 10.99.2.4/32 |
| DC2_POD | dc2-leaf3 | 10.99.2.5/32 |
| DC2_POD | dc2-leaf4 | 10.99.2.6/32 |
| DC2 | dc2-spine1 | 10.99.2.129/32 |
| DC2 | dc2-spine2 | 10.99.2.130/32 |

### VTEP Loopback VXLAN Tunnel Source Interfaces (VTEPs Only)

| VTEP Loopback Pool | Available Addresses | Assigned addresses | Assigned Address % |
| ------------------ | ------------------- | ------------------ | ------------------ |
| 10.102.2.0/24 | 256 | 6 | 2.35 % |

### VTEP Loopback Node allocation

| POD | Node | Loopback1 |
| --- | ---- | --------- |
| DC2_POD | dc2-brdr1 | 10.102.2.1/32 |
| DC2_POD | dc2-brdr2 | 10.102.2.1/32 |
| DC2_POD | dc2-leaf1 | 10.102.2.3/32 |
| DC2_POD | dc2-leaf2 | 10.102.2.3/32 |
| DC2_POD | dc2-leaf3 | 10.102.2.5/32 |
| DC2_POD | dc2-leaf4 | 10.102.2.5/32 |
