# FABRIC_B

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
| FABRIC_B | l2leaf | B-LEAF1 | 192.168.0.113/24 | cEOS-LAB | Provisioned | - |
| FABRIC_B | l2leaf | B-LEAF2 | 192.168.0.114/24 | cEOS-LAB | Provisioned | - |
| FABRIC_B | l2leaf | B-LEAF3 | 192.168.0.115/24 | cEOS-LAB | Provisioned | - |
| FABRIC_B | l2leaf | B-LEAF4 | 192.168.0.116/24 | cEOS-LAB | Provisioned | - |
| FABRIC_B | l3spine | B-SPINE1 | 192.168.0.111/24 | cEOS-LAB | Provisioned | - |
| FABRIC_B | l3spine | B-SPINE2 | 192.168.0.112/24 | cEOS-LAB | Provisioned | - |

> Provision status is based on Ansible inventory declaration and do not represent real status from CloudVision.

### Fabric Switches with inband Management IP

| POD | Type | Node | Management IP | Inband Interface |
| --- | ---- | ---- | ------------- | ---------------- |

## Fabric Topology

| Type | Node | Node Interface | Peer Type | Peer Node | Peer Interface |
| ---- | ---- | -------------- | --------- | ----------| -------------- |
| l2leaf | B-LEAF1 | Ethernet1 | l3spine | B-SPINE1 | Ethernet1 |
| l2leaf | B-LEAF1 | Ethernet2 | l3spine | B-SPINE2 | Ethernet1 |
| l2leaf | B-LEAF1 | Ethernet5 | mlag_peer | B-LEAF2 | Ethernet5 |
| l2leaf | B-LEAF1 | Ethernet6 | mlag_peer | B-LEAF2 | Ethernet6 |
| l2leaf | B-LEAF2 | Ethernet1 | l3spine | B-SPINE1 | Ethernet2 |
| l2leaf | B-LEAF2 | Ethernet2 | l3spine | B-SPINE2 | Ethernet2 |
| l2leaf | B-LEAF3 | Ethernet1 | l3spine | B-SPINE1 | Ethernet3 |
| l2leaf | B-LEAF3 | Ethernet2 | l3spine | B-SPINE2 | Ethernet3 |
| l2leaf | B-LEAF3 | Ethernet5 | mlag_peer | B-LEAF4 | Ethernet5 |
| l2leaf | B-LEAF3 | Ethernet6 | mlag_peer | B-LEAF4 | Ethernet6 |
| l2leaf | B-LEAF4 | Ethernet1 | l3spine | B-SPINE1 | Ethernet4 |
| l2leaf | B-LEAF4 | Ethernet2 | l3spine | B-SPINE2 | Ethernet4 |
| l3spine | B-SPINE1 | Ethernet7 | mlag_peer | B-SPINE2 | Ethernet7 |
| l3spine | B-SPINE1 | Ethernet8 | mlag_peer | B-SPINE2 | Ethernet8 |

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
| 10.254.2.0/24 | 256 | 2 | 0.79 % |

### Loopback0 Interfaces Node Allocation

| POD | Node | Loopback0 |
| --- | ---- | --------- |
| FABRIC_B | B-SPINE1 | 10.254.2.1/32 |
| FABRIC_B | B-SPINE2 | 10.254.2.2/32 |

### VTEP Loopback VXLAN Tunnel Source Interfaces (VTEPs Only)

| VTEP Loopback Pool | Available Addresses | Assigned addresses | Assigned Address % |
| ------------------ | ------------------- | ------------------ | ------------------ |

### VTEP Loopback Node allocation

| POD | Node | Loopback1 |
| --- | ---- | --------- |
| FABRIC_B | B-SPINE1 | 10.255.2.1/32 |
| FABRIC_B | B-SPINE2 | 10.255.2.1/32 |
