# CAMPUS

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
| CAMPUS | l2leaf | campus-brdr1 | 192.168.0.36/24 | vEOS-lab | Provisioned | - |
| CAMPUS | l2leaf | campus-brdr2 | 192.168.0.37/24 | vEOS-lab | Provisioned | - |
| CAMPUS | l2leaf | campus-leaf1 | 192.168.0.32/24 | vEOS-lab | Provisioned | - |
| CAMPUS | l2leaf | campus-leaf2 | 192.168.0.33/24 | vEOS-lab | Provisioned | - |
| CAMPUS | l2leaf | campus-leaf3 | 192.168.0.34/24 | vEOS-lab | Provisioned | - |
| CAMPUS | l2leaf | campus-leaf4 | 192.168.0.35/24 | vEOS-lab | Provisioned | - |
| CAMPUS | l3spine | campus-spine1 | 192.168.0.30/24 | vEOS-lab | Provisioned | - |
| CAMPUS | l3spine | campus-spine2 | 192.168.0.31/24 | vEOS-lab | Provisioned | - |

> Provision status is based on Ansible inventory declaration and do not represent real status from CloudVision.

### Fabric Switches with inband Management IP

| POD | Type | Node | Management IP | Inband Interface |
| --- | ---- | ---- | ------------- | ---------------- |

## Fabric Topology

| Type | Node | Node Interface | Peer Type | Peer Node | Peer Interface |
| ---- | ---- | -------------- | --------- | --------- | -------------- |
| l2leaf | campus-brdr1 | Ethernet49/1 | l3spine | campus-spine1 | Ethernet1/1 |
| l2leaf | campus-brdr1 | Ethernet50/1 | l3spine | campus-spine2 | Ethernet1/1 |
| l2leaf | campus-brdr1 | Ethernet51/1 | mlag_peer | campus-brdr2 | Ethernet51/1 |
| l2leaf | campus-brdr1 | Ethernet52/1 | mlag_peer | campus-brdr2 | Ethernet52/1 |
| l2leaf | campus-brdr2 | Ethernet49/1 | l3spine | campus-spine1 | Ethernet1/2 |
| l2leaf | campus-brdr2 | Ethernet50/1 | l3spine | campus-spine2 | Ethernet1/2 |
| l2leaf | campus-leaf1 | Ethernet49 | l3spine | campus-spine1 | Ethernet1/3 |
| l2leaf | campus-leaf1 | Ethernet50 | l3spine | campus-spine2 | Ethernet1/3 |
| l2leaf | campus-leaf1 | Ethernet51 | mlag_peer | campus-leaf2 | Ethernet51 |
| l2leaf | campus-leaf1 | Ethernet52 | mlag_peer | campus-leaf2 | Ethernet52 |
| l2leaf | campus-leaf2 | Ethernet49 | l3spine | campus-spine1 | Ethernet1/4 |
| l2leaf | campus-leaf2 | Ethernet50 | l3spine | campus-spine2 | Ethernet1/4 |
| l2leaf | campus-leaf3 | Ethernet49 | l3spine | campus-spine1 | Ethernet1/5 |
| l2leaf | campus-leaf3 | Ethernet50 | l3spine | campus-spine2 | Ethernet1/5 |
| l2leaf | campus-leaf3 | Ethernet51 | mlag_peer | campus-leaf4 | Ethernet51 |
| l2leaf | campus-leaf3 | Ethernet52 | mlag_peer | campus-leaf4 | Ethernet52 |
| l2leaf | campus-leaf4 | Ethernet49 | l3spine | campus-spine1 | Ethernet1/6 |
| l2leaf | campus-leaf4 | Ethernet50 | l3spine | campus-spine2 | Ethernet1/6 |
| l3spine | campus-spine1 | Ethernet2/1 | mlag_peer | campus-spine2 | Ethernet2/1 |
| l3spine | campus-spine1 | Ethernet2/2 | mlag_peer | campus-spine2 | Ethernet2/2 |

## Fabric IP Allocation

### Fabric Point-To-Point Links

| Uplink IPv4 Pool | Available Addresses | Assigned addresses | Assigned Address % |
| ---------------- | ------------------- | ------------------ | ------------------ |

### Point-To-Point Links Node Allocation

| Node | Node Interface | Node IP Address | Peer Node | Peer Interface | Peer IP Address |
| ---- | -------------- | --------------- | --------- | -------------- | --------------- |

### Loopback Interfaces (BGP EVPN Peering)

| Loopback Pool | Available Addresses | Assigned addresses | Assigned Address % |
| ------------- | ------------------- | ------------------ | ------------------ |
| 10.98.1.128/25 | 128 | 2 | 1.57 % |

### Loopback0 Interfaces Node Allocation

| POD | Node | Loopback0 |
| --- | ---- | --------- |
| CAMPUS | campus-spine1 | 10.98.1.129/32 |
| CAMPUS | campus-spine2 | 10.98.1.130/32 |

### VTEP Loopback VXLAN Tunnel Source Interfaces (VTEPs Only)

| VTEP Loopback Pool | Available Addresses | Assigned addresses | Assigned Address % |
| ------------------ | ------------------- | ------------------ | ------------------ |

### VTEP Loopback Node allocation

| POD | Node | Loopback1 |
| --- | ---- | --------- |
