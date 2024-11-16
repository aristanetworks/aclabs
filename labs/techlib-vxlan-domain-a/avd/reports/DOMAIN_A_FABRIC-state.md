# Validate State Report

**Table of Contents:**

- [Validate State Report](validate-state-report)
  - [Test Results Summary](#test-results-summary)
  - [Failed Test Results Summary](#failed-test-results-summary)
  - [All Test Results](#all-test-results)

## Test Results Summary

### Summary Totals

| Total Tests | Total Tests Passed | Total Tests Failed | Total Tests Skipped |
| ----------- | ------------------ | ------------------ | ------------------- |
| 766 | 718 | 0 | 48 |

### Summary Totals Device Under Test

| Device Under Test | Total Tests | Tests Passed | Tests Failed | Tests Skipped | Categories Failed | Categories Skipped |
| ------------------| ----------- | ------------ | ------------ | ------------- | ----------------- | ------------------ |
| A-LEAF1 | 71 | 67 | 0 | 4 | - | Hardware |
| A-LEAF2 | 71 | 67 | 0 | 4 | - | Hardware |
| A-LEAF3 | 73 | 69 | 0 | 4 | - | Hardware |
| A-LEAF4 | 73 | 69 | 0 | 4 | - | Hardware |
| A-LEAF5 | 68 | 64 | 0 | 4 | - | Hardware |
| A-LEAF6 | 68 | 64 | 0 | 4 | - | Hardware |
| A-LEAF7 | 75 | 71 | 0 | 4 | - | Hardware |
| A-LEAF8 | 75 | 71 | 0 | 4 | - | Hardware |
| A-SPINE1 | 48 | 44 | 0 | 4 | - | Hardware |
| A-SPINE2 | 48 | 44 | 0 | 4 | - | Hardware |
| A-SPINE3 | 48 | 44 | 0 | 4 | - | Hardware |
| A-SPINE4 | 48 | 44 | 0 | 4 | - | Hardware |

### Summary Totals Per Category

| Test Category | Total Tests | Tests Passed | Tests Failed | Tests Skipped |
| ------------- | ----------- | ------------ | ------------ | ------------- |
| BGP | 140 | 140 | 0 | 0 |
| Connectivity | 240 | 240 | 0 | 0 |
| Hardware | 48 | 0 | 0 | 48 |
| Interfaces | 198 | 198 | 0 | 0 |
| MLAG | 8 | 8 | 0 | 0 |
| Routing | 108 | 108 | 0 | 0 |
| System | 24 | 24 | 0 | 0 |

## Failed Test Results Summary

| ID | Device Under Test | Categories | Test | Description | Inputs | Result | Messages |
| -- | ----------------- | ---------- | ---- | ----------- | ------ | -------| -------- |

## All Test Results

| ID | Device Under Test | Categories | Test | Description | Inputs | Result | Messages |
| -- | ----------------- | ---------- | ---- | ----------- | ------ | -------| -------- |
| 1 | A-LEAF1 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s). | BGP EVPN Peer: A-SPINE1 (IP: 1.1.1.201) | PASS | - |
| 2 | A-LEAF1 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s). | BGP EVPN Peer: A-SPINE2 (IP: 1.1.1.202) | PASS | - |
| 3 | A-LEAF1 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s). | BGP EVPN Peer: A-SPINE3 (IP: 1.1.1.203) | PASS | - |
| 4 | A-LEAF1 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s). | BGP EVPN Peer: A-SPINE4 (IP: 1.1.1.204) | PASS | - |
| 5 | A-LEAF1 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s). | BGP IPv4 Unicast Peer: A-LEAF2 (IP: 192.0.0.1) | PASS | - |
| 6 | A-LEAF1 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s). | BGP IPv4 Unicast Peer: A-SPINE1 (IP: 192.168.0.0) | PASS | - |
| 7 | A-LEAF1 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s). | BGP IPv4 Unicast Peer: A-SPINE2 (IP: 192.168.0.2) | PASS | - |
| 8 | A-LEAF1 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s). | BGP IPv4 Unicast Peer: A-SPINE3 (IP: 192.168.0.4) | PASS | - |
| 9 | A-LEAF1 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s). | BGP IPv4 Unicast Peer: A-SPINE4 (IP: 192.168.0.6) | PASS | - |
| 10 | A-LEAF1 | Connectivity | VerifyLLDPNeighbors | Verifies that the provided LLDP neighbors are connected properly. | Local: Ethernet1 - Remote: A-SPINE1 Ethernet1 | PASS | - |
| 11 | A-LEAF1 | Connectivity | VerifyLLDPNeighbors | Verifies that the provided LLDP neighbors are connected properly. | Local: Ethernet2 - Remote: A-SPINE2 Ethernet1 | PASS | - |
| 12 | A-LEAF1 | Connectivity | VerifyLLDPNeighbors | Verifies that the provided LLDP neighbors are connected properly. | Local: Ethernet3 - Remote: A-SPINE3 Ethernet1 | PASS | - |
| 13 | A-LEAF1 | Connectivity | VerifyLLDPNeighbors | Verifies that the provided LLDP neighbors are connected properly. | Local: Ethernet4 - Remote: A-SPINE4 Ethernet1 | PASS | - |
| 14 | A-LEAF1 | Connectivity | VerifyLLDPNeighbors | Verifies that the provided LLDP neighbors are connected properly. | Local: Ethernet5 - Remote: A-LEAF2 Ethernet5 | PASS | - |
| 15 | A-LEAF1 | Connectivity | VerifyLLDPNeighbors | Verifies that the provided LLDP neighbors are connected properly. | Local: Ethernet6 - Remote: A-LEAF2 Ethernet6 | PASS | - |
| 16 | A-LEAF1 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: Loopback0 (IP: 1.1.1.1) - Destination: A-LEAF1 Loopback0 (IP: 1.1.1.1) | PASS | - |
| 17 | A-LEAF1 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: Loopback0 (IP: 1.1.1.1) - Destination: A-LEAF2 Loopback0 (IP: 1.1.1.2) | PASS | - |
| 18 | A-LEAF1 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: Loopback0 (IP: 1.1.1.1) - Destination: A-LEAF3 Loopback0 (IP: 1.1.1.3) | PASS | - |
| 19 | A-LEAF1 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: Loopback0 (IP: 1.1.1.1) - Destination: A-LEAF4 Loopback0 (IP: 1.1.1.4) | PASS | - |
| 20 | A-LEAF1 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: Loopback0 (IP: 1.1.1.1) - Destination: A-LEAF5 Loopback0 (IP: 1.1.1.5) | PASS | - |
| 21 | A-LEAF1 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: Loopback0 (IP: 1.1.1.1) - Destination: A-LEAF6 Loopback0 (IP: 1.1.1.6) | PASS | - |
| 22 | A-LEAF1 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: Loopback0 (IP: 1.1.1.1) - Destination: A-LEAF7 Loopback0 (IP: 1.1.1.7) | PASS | - |
| 23 | A-LEAF1 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: Loopback0 (IP: 1.1.1.1) - Destination: A-LEAF8 Loopback0 (IP: 1.1.1.8) | PASS | - |
| 24 | A-LEAF1 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: Loopback0 (IP: 1.1.1.1) - Destination: A-SPINE1 Loopback0 (IP: 1.1.1.201) | PASS | - |
| 25 | A-LEAF1 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: Loopback0 (IP: 1.1.1.1) - Destination: A-SPINE2 Loopback0 (IP: 1.1.1.202) | PASS | - |
| 26 | A-LEAF1 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: Loopback0 (IP: 1.1.1.1) - Destination: A-SPINE3 Loopback0 (IP: 1.1.1.203) | PASS | - |
| 27 | A-LEAF1 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: Loopback0 (IP: 1.1.1.1) - Destination: A-SPINE4 Loopback0 (IP: 1.1.1.204) | PASS | - |
| 28 | A-LEAF1 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: P2P Interface Ethernet1 (IP: 192.168.0.1) - Destination: A-SPINE1 Ethernet1 (IP: 192.168.0.0) | PASS | - |
| 29 | A-LEAF1 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: P2P Interface Ethernet2 (IP: 192.168.0.3) - Destination: A-SPINE2 Ethernet1 (IP: 192.168.0.2) | PASS | - |
| 30 | A-LEAF1 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: P2P Interface Ethernet3 (IP: 192.168.0.5) - Destination: A-SPINE3 Ethernet1 (IP: 192.168.0.4) | PASS | - |
| 31 | A-LEAF1 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: P2P Interface Ethernet4 (IP: 192.168.0.7) - Destination: A-SPINE4 Ethernet1 (IP: 192.168.0.6) | PASS | - |
| 32 | A-LEAF1 | Hardware | VerifyEnvironmentCooling | Verifies the status of power supply fans and all fan trays. | Accepted States: 'ok' | SKIPPED | VerifyEnvironmentCooling test is not supported on cEOSLab. |
| 33 | A-LEAF1 | Hardware | VerifyEnvironmentPower | Verifies the power supplies status. | Accepted States: 'ok' | SKIPPED | VerifyEnvironmentPower test is not supported on cEOSLab. |
| 34 | A-LEAF1 | Hardware | VerifyTemperature | Verifies the device temperature. | - | SKIPPED | VerifyTemperature test is not supported on cEOSLab. |
| 35 | A-LEAF1 | Hardware | VerifyTransceiversManufacturers | Verifies if all transceivers come from approved manufacturers. | Accepted Manufacturers: 'Arista Networks', 'Arastra, Inc.', 'Not Present' | SKIPPED | VerifyTransceiversManufacturers test is not supported on cEOSLab. |
| 36 | A-LEAF1 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Ethernet1 - P2P_A-SPINE1_Ethernet1 = 'up' | PASS | - |
| 37 | A-LEAF1 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Ethernet2 - P2P_A-SPINE2_Ethernet1 = 'up' | PASS | - |
| 38 | A-LEAF1 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Ethernet3 - P2P_A-SPINE3_Ethernet1 = 'up' | PASS | - |
| 39 | A-LEAF1 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Ethernet4 - P2P_A-SPINE4_Ethernet1 = 'up' | PASS | - |
| 40 | A-LEAF1 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Ethernet5 - MLAG_A-LEAF2_Ethernet5 = 'up' | PASS | - |
| 41 | A-LEAF1 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Ethernet6 - MLAG_A-LEAF2_Ethernet6 = 'up' | PASS | - |
| 42 | A-LEAF1 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Ethernet7 - SERVER_HostA1_eth1 = 'up' | PASS | - |
| 43 | A-LEAF1 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Ethernet8 - SERVER_HostA2_eth1 = 'up' | PASS | - |
| 44 | A-LEAF1 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Loopback0 - Globally Unique Address = 'up' | PASS | - |
| 45 | A-LEAF1 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Loopback1 - VTEP IP = 'up' | PASS | - |
| 46 | A-LEAF1 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Loopback101 - Per-VRF Unique Loopback = 'up' | PASS | - |
| 47 | A-LEAF1 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Port-Channel1000 - MLAG_A-LEAF2_Port-Channel1000 = 'up' | PASS | - |
| 48 | A-LEAF1 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Port-Channel7 - SERVER_HostA1 = 'up' | PASS | - |
| 49 | A-LEAF1 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Port-Channel8 - SERVER_HostA2 = 'up' | PASS | - |
| 50 | A-LEAF1 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Vlan10 - Blue Network = 'up' | PASS | - |
| 51 | A-LEAF1 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Vlan30 - Orange Network = 'up' | PASS | - |
| 52 | A-LEAF1 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Vlan3001 - MLAG_L3_VRF_PROD = 'up' | PASS | - |
| 53 | A-LEAF1 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Vlan4093 - MLAG_L3 = 'up' | PASS | - |
| 54 | A-LEAF1 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Vlan4094 - MLAG = 'up' | PASS | - |
| 55 | A-LEAF1 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Vxlan1 = 'up' | PASS | - |
| 56 | A-LEAF1 | MLAG | VerifyMlagStatus | Verifies the health status of the MLAG configuration. | - | PASS | - |
| 57 | A-LEAF1 | Routing | VerifyRoutingProtocolModel | Verifies the configured routing protocol model. | Routing protocol model: multi-agent | PASS | - |
| 58 | A-LEAF1 | Routing | VerifyRoutingTableEntry | Verifies that the provided routes are present in the routing table of a specified VRF. | Route: 1.1.1.1 - Peer: A-LEAF1 | PASS | - |
| 59 | A-LEAF1 | Routing | VerifyRoutingTableEntry | Verifies that the provided routes are present in the routing table of a specified VRF. | Route: 1.1.1.2 - Peer: A-LEAF2 | PASS | - |
| 60 | A-LEAF1 | Routing | VerifyRoutingTableEntry | Verifies that the provided routes are present in the routing table of a specified VRF. | Route: 1.1.1.201 - Peer: A-SPINE1 | PASS | - |
| 61 | A-LEAF1 | Routing | VerifyRoutingTableEntry | Verifies that the provided routes are present in the routing table of a specified VRF. | Route: 1.1.1.202 - Peer: A-SPINE2 | PASS | - |
| 62 | A-LEAF1 | Routing | VerifyRoutingTableEntry | Verifies that the provided routes are present in the routing table of a specified VRF. | Route: 1.1.1.203 - Peer: A-SPINE3 | PASS | - |
| 63 | A-LEAF1 | Routing | VerifyRoutingTableEntry | Verifies that the provided routes are present in the routing table of a specified VRF. | Route: 1.1.1.204 - Peer: A-SPINE4 | PASS | - |
| 64 | A-LEAF1 | Routing | VerifyRoutingTableEntry | Verifies that the provided routes are present in the routing table of a specified VRF. | Route: 1.1.1.3 - Peer: A-LEAF3 | PASS | - |
| 65 | A-LEAF1 | Routing | VerifyRoutingTableEntry | Verifies that the provided routes are present in the routing table of a specified VRF. | Route: 1.1.1.4 - Peer: A-LEAF4 | PASS | - |
| 66 | A-LEAF1 | Routing | VerifyRoutingTableEntry | Verifies that the provided routes are present in the routing table of a specified VRF. | Route: 1.1.1.5 - Peer: A-LEAF5 | PASS | - |
| 67 | A-LEAF1 | Routing | VerifyRoutingTableEntry | Verifies that the provided routes are present in the routing table of a specified VRF. | Route: 1.1.1.6 - Peer: A-LEAF6 | PASS | - |
| 68 | A-LEAF1 | Routing | VerifyRoutingTableEntry | Verifies that the provided routes are present in the routing table of a specified VRF. | Route: 1.1.1.7 - Peer: A-LEAF7 | PASS | - |
| 69 | A-LEAF1 | Routing | VerifyRoutingTableEntry | Verifies that the provided routes are present in the routing table of a specified VRF. | Route: 1.1.1.8 - Peer: A-LEAF8 | PASS | - |
| 70 | A-LEAF1 | System | VerifyNTP | Verifies if NTP is synchronised. | - | PASS | - |
| 71 | A-LEAF1 | System | VerifyReloadCause | Verifies the last reload cause of the device. | - | PASS | - |
| 72 | A-LEAF2 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s). | BGP EVPN Peer: A-SPINE1 (IP: 1.1.1.201) | PASS | - |
| 73 | A-LEAF2 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s). | BGP EVPN Peer: A-SPINE2 (IP: 1.1.1.202) | PASS | - |
| 74 | A-LEAF2 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s). | BGP EVPN Peer: A-SPINE3 (IP: 1.1.1.203) | PASS | - |
| 75 | A-LEAF2 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s). | BGP EVPN Peer: A-SPINE4 (IP: 1.1.1.204) | PASS | - |
| 76 | A-LEAF2 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s). | BGP IPv4 Unicast Peer: A-LEAF1 (IP: 192.0.0.0) | PASS | - |
| 77 | A-LEAF2 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s). | BGP IPv4 Unicast Peer: A-SPINE1 (IP: 192.168.0.8) | PASS | - |
| 78 | A-LEAF2 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s). | BGP IPv4 Unicast Peer: A-SPINE2 (IP: 192.168.0.10) | PASS | - |
| 79 | A-LEAF2 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s). | BGP IPv4 Unicast Peer: A-SPINE3 (IP: 192.168.0.12) | PASS | - |
| 80 | A-LEAF2 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s). | BGP IPv4 Unicast Peer: A-SPINE4 (IP: 192.168.0.14) | PASS | - |
| 81 | A-LEAF2 | Connectivity | VerifyLLDPNeighbors | Verifies that the provided LLDP neighbors are connected properly. | Local: Ethernet1 - Remote: A-SPINE1 Ethernet2 | PASS | - |
| 82 | A-LEAF2 | Connectivity | VerifyLLDPNeighbors | Verifies that the provided LLDP neighbors are connected properly. | Local: Ethernet2 - Remote: A-SPINE2 Ethernet2 | PASS | - |
| 83 | A-LEAF2 | Connectivity | VerifyLLDPNeighbors | Verifies that the provided LLDP neighbors are connected properly. | Local: Ethernet3 - Remote: A-SPINE3 Ethernet2 | PASS | - |
| 84 | A-LEAF2 | Connectivity | VerifyLLDPNeighbors | Verifies that the provided LLDP neighbors are connected properly. | Local: Ethernet4 - Remote: A-SPINE4 Ethernet2 | PASS | - |
| 85 | A-LEAF2 | Connectivity | VerifyLLDPNeighbors | Verifies that the provided LLDP neighbors are connected properly. | Local: Ethernet5 - Remote: A-LEAF1 Ethernet5 | PASS | - |
| 86 | A-LEAF2 | Connectivity | VerifyLLDPNeighbors | Verifies that the provided LLDP neighbors are connected properly. | Local: Ethernet6 - Remote: A-LEAF1 Ethernet6 | PASS | - |
| 87 | A-LEAF2 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: Loopback0 (IP: 1.1.1.2) - Destination: A-LEAF1 Loopback0 (IP: 1.1.1.1) | PASS | - |
| 88 | A-LEAF2 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: Loopback0 (IP: 1.1.1.2) - Destination: A-LEAF2 Loopback0 (IP: 1.1.1.2) | PASS | - |
| 89 | A-LEAF2 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: Loopback0 (IP: 1.1.1.2) - Destination: A-LEAF3 Loopback0 (IP: 1.1.1.3) | PASS | - |
| 90 | A-LEAF2 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: Loopback0 (IP: 1.1.1.2) - Destination: A-LEAF4 Loopback0 (IP: 1.1.1.4) | PASS | - |
| 91 | A-LEAF2 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: Loopback0 (IP: 1.1.1.2) - Destination: A-LEAF5 Loopback0 (IP: 1.1.1.5) | PASS | - |
| 92 | A-LEAF2 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: Loopback0 (IP: 1.1.1.2) - Destination: A-LEAF6 Loopback0 (IP: 1.1.1.6) | PASS | - |
| 93 | A-LEAF2 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: Loopback0 (IP: 1.1.1.2) - Destination: A-LEAF7 Loopback0 (IP: 1.1.1.7) | PASS | - |
| 94 | A-LEAF2 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: Loopback0 (IP: 1.1.1.2) - Destination: A-LEAF8 Loopback0 (IP: 1.1.1.8) | PASS | - |
| 95 | A-LEAF2 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: Loopback0 (IP: 1.1.1.2) - Destination: A-SPINE1 Loopback0 (IP: 1.1.1.201) | PASS | - |
| 96 | A-LEAF2 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: Loopback0 (IP: 1.1.1.2) - Destination: A-SPINE2 Loopback0 (IP: 1.1.1.202) | PASS | - |
| 97 | A-LEAF2 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: Loopback0 (IP: 1.1.1.2) - Destination: A-SPINE3 Loopback0 (IP: 1.1.1.203) | PASS | - |
| 98 | A-LEAF2 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: Loopback0 (IP: 1.1.1.2) - Destination: A-SPINE4 Loopback0 (IP: 1.1.1.204) | PASS | - |
| 99 | A-LEAF2 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: P2P Interface Ethernet1 (IP: 192.168.0.9) - Destination: A-SPINE1 Ethernet2 (IP: 192.168.0.8) | PASS | - |
| 100 | A-LEAF2 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: P2P Interface Ethernet2 (IP: 192.168.0.11) - Destination: A-SPINE2 Ethernet2 (IP: 192.168.0.10) | PASS | - |
| 101 | A-LEAF2 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: P2P Interface Ethernet3 (IP: 192.168.0.13) - Destination: A-SPINE3 Ethernet2 (IP: 192.168.0.12) | PASS | - |
| 102 | A-LEAF2 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: P2P Interface Ethernet4 (IP: 192.168.0.15) - Destination: A-SPINE4 Ethernet2 (IP: 192.168.0.14) | PASS | - |
| 103 | A-LEAF2 | Hardware | VerifyEnvironmentCooling | Verifies the status of power supply fans and all fan trays. | Accepted States: 'ok' | SKIPPED | VerifyEnvironmentCooling test is not supported on cEOSLab. |
| 104 | A-LEAF2 | Hardware | VerifyEnvironmentPower | Verifies the power supplies status. | Accepted States: 'ok' | SKIPPED | VerifyEnvironmentPower test is not supported on cEOSLab. |
| 105 | A-LEAF2 | Hardware | VerifyTemperature | Verifies the device temperature. | - | SKIPPED | VerifyTemperature test is not supported on cEOSLab. |
| 106 | A-LEAF2 | Hardware | VerifyTransceiversManufacturers | Verifies if all transceivers come from approved manufacturers. | Accepted Manufacturers: 'Arista Networks', 'Arastra, Inc.', 'Not Present' | SKIPPED | VerifyTransceiversManufacturers test is not supported on cEOSLab. |
| 107 | A-LEAF2 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Ethernet1 - P2P_A-SPINE1_Ethernet2 = 'up' | PASS | - |
| 108 | A-LEAF2 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Ethernet2 - P2P_A-SPINE2_Ethernet2 = 'up' | PASS | - |
| 109 | A-LEAF2 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Ethernet3 - P2P_A-SPINE3_Ethernet2 = 'up' | PASS | - |
| 110 | A-LEAF2 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Ethernet4 - P2P_A-SPINE4_Ethernet2 = 'up' | PASS | - |
| 111 | A-LEAF2 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Ethernet5 - MLAG_A-LEAF1_Ethernet5 = 'up' | PASS | - |
| 112 | A-LEAF2 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Ethernet6 - MLAG_A-LEAF1_Ethernet6 = 'up' | PASS | - |
| 113 | A-LEAF2 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Ethernet7 - SERVER_HostA1_eth2 = 'up' | PASS | - |
| 114 | A-LEAF2 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Ethernet8 - SERVER_HostA2_eth2 = 'up' | PASS | - |
| 115 | A-LEAF2 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Loopback0 - Globally Unique Address = 'up' | PASS | - |
| 116 | A-LEAF2 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Loopback1 - VTEP IP = 'up' | PASS | - |
| 117 | A-LEAF2 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Loopback101 - Per-VRF Unique Loopback = 'up' | PASS | - |
| 118 | A-LEAF2 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Port-Channel1000 - MLAG_A-LEAF1_Port-Channel1000 = 'up' | PASS | - |
| 119 | A-LEAF2 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Port-Channel7 - SERVER_HostA1 = 'up' | PASS | - |
| 120 | A-LEAF2 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Port-Channel8 - SERVER_HostA2 = 'up' | PASS | - |
| 121 | A-LEAF2 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Vlan10 - Blue Network = 'up' | PASS | - |
| 122 | A-LEAF2 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Vlan30 - Orange Network = 'up' | PASS | - |
| 123 | A-LEAF2 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Vlan3001 - MLAG_L3_VRF_PROD = 'up' | PASS | - |
| 124 | A-LEAF2 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Vlan4093 - MLAG_L3 = 'up' | PASS | - |
| 125 | A-LEAF2 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Vlan4094 - MLAG = 'up' | PASS | - |
| 126 | A-LEAF2 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Vxlan1 = 'up' | PASS | - |
| 127 | A-LEAF2 | MLAG | VerifyMlagStatus | Verifies the health status of the MLAG configuration. | - | PASS | - |
| 128 | A-LEAF2 | Routing | VerifyRoutingProtocolModel | Verifies the configured routing protocol model. | Routing protocol model: multi-agent | PASS | - |
| 129 | A-LEAF2 | Routing | VerifyRoutingTableEntry | Verifies that the provided routes are present in the routing table of a specified VRF. | Route: 1.1.1.1 - Peer: A-LEAF1 | PASS | - |
| 130 | A-LEAF2 | Routing | VerifyRoutingTableEntry | Verifies that the provided routes are present in the routing table of a specified VRF. | Route: 1.1.1.2 - Peer: A-LEAF2 | PASS | - |
| 131 | A-LEAF2 | Routing | VerifyRoutingTableEntry | Verifies that the provided routes are present in the routing table of a specified VRF. | Route: 1.1.1.201 - Peer: A-SPINE1 | PASS | - |
| 132 | A-LEAF2 | Routing | VerifyRoutingTableEntry | Verifies that the provided routes are present in the routing table of a specified VRF. | Route: 1.1.1.202 - Peer: A-SPINE2 | PASS | - |
| 133 | A-LEAF2 | Routing | VerifyRoutingTableEntry | Verifies that the provided routes are present in the routing table of a specified VRF. | Route: 1.1.1.203 - Peer: A-SPINE3 | PASS | - |
| 134 | A-LEAF2 | Routing | VerifyRoutingTableEntry | Verifies that the provided routes are present in the routing table of a specified VRF. | Route: 1.1.1.204 - Peer: A-SPINE4 | PASS | - |
| 135 | A-LEAF2 | Routing | VerifyRoutingTableEntry | Verifies that the provided routes are present in the routing table of a specified VRF. | Route: 1.1.1.3 - Peer: A-LEAF3 | PASS | - |
| 136 | A-LEAF2 | Routing | VerifyRoutingTableEntry | Verifies that the provided routes are present in the routing table of a specified VRF. | Route: 1.1.1.4 - Peer: A-LEAF4 | PASS | - |
| 137 | A-LEAF2 | Routing | VerifyRoutingTableEntry | Verifies that the provided routes are present in the routing table of a specified VRF. | Route: 1.1.1.5 - Peer: A-LEAF5 | PASS | - |
| 138 | A-LEAF2 | Routing | VerifyRoutingTableEntry | Verifies that the provided routes are present in the routing table of a specified VRF. | Route: 1.1.1.6 - Peer: A-LEAF6 | PASS | - |
| 139 | A-LEAF2 | Routing | VerifyRoutingTableEntry | Verifies that the provided routes are present in the routing table of a specified VRF. | Route: 1.1.1.7 - Peer: A-LEAF7 | PASS | - |
| 140 | A-LEAF2 | Routing | VerifyRoutingTableEntry | Verifies that the provided routes are present in the routing table of a specified VRF. | Route: 1.1.1.8 - Peer: A-LEAF8 | PASS | - |
| 141 | A-LEAF2 | System | VerifyNTP | Verifies if NTP is synchronised. | - | PASS | - |
| 142 | A-LEAF2 | System | VerifyReloadCause | Verifies the last reload cause of the device. | - | PASS | - |
| 143 | A-LEAF3 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s). | BGP EVPN Peer: A-SPINE1 (IP: 1.1.1.201) | PASS | - |
| 144 | A-LEAF3 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s). | BGP EVPN Peer: A-SPINE2 (IP: 1.1.1.202) | PASS | - |
| 145 | A-LEAF3 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s). | BGP EVPN Peer: A-SPINE3 (IP: 1.1.1.203) | PASS | - |
| 146 | A-LEAF3 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s). | BGP EVPN Peer: A-SPINE4 (IP: 1.1.1.204) | PASS | - |
| 147 | A-LEAF3 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s). | BGP IPv4 Unicast Peer: A-LEAF4 (IP: 192.0.0.1) | PASS | - |
| 148 | A-LEAF3 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s). | BGP IPv4 Unicast Peer: A-SPINE1 (IP: 192.168.0.16) | PASS | - |
| 149 | A-LEAF3 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s). | BGP IPv4 Unicast Peer: A-SPINE2 (IP: 192.168.0.18) | PASS | - |
| 150 | A-LEAF3 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s). | BGP IPv4 Unicast Peer: A-SPINE3 (IP: 192.168.0.20) | PASS | - |
| 151 | A-LEAF3 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s). | BGP IPv4 Unicast Peer: A-SPINE4 (IP: 192.168.0.22) | PASS | - |
| 152 | A-LEAF3 | Connectivity | VerifyLLDPNeighbors | Verifies that the provided LLDP neighbors are connected properly. | Local: Ethernet1 - Remote: A-SPINE1 Ethernet3 | PASS | - |
| 153 | A-LEAF3 | Connectivity | VerifyLLDPNeighbors | Verifies that the provided LLDP neighbors are connected properly. | Local: Ethernet2 - Remote: A-SPINE2 Ethernet3 | PASS | - |
| 154 | A-LEAF3 | Connectivity | VerifyLLDPNeighbors | Verifies that the provided LLDP neighbors are connected properly. | Local: Ethernet3 - Remote: A-SPINE3 Ethernet3 | PASS | - |
| 155 | A-LEAF3 | Connectivity | VerifyLLDPNeighbors | Verifies that the provided LLDP neighbors are connected properly. | Local: Ethernet4 - Remote: A-SPINE4 Ethernet3 | PASS | - |
| 156 | A-LEAF3 | Connectivity | VerifyLLDPNeighbors | Verifies that the provided LLDP neighbors are connected properly. | Local: Ethernet5 - Remote: A-LEAF4 Ethernet5 | PASS | - |
| 157 | A-LEAF3 | Connectivity | VerifyLLDPNeighbors | Verifies that the provided LLDP neighbors are connected properly. | Local: Ethernet6 - Remote: A-LEAF4 Ethernet6 | PASS | - |
| 158 | A-LEAF3 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: Loopback0 (IP: 1.1.1.3) - Destination: A-LEAF1 Loopback0 (IP: 1.1.1.1) | PASS | - |
| 159 | A-LEAF3 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: Loopback0 (IP: 1.1.1.3) - Destination: A-LEAF2 Loopback0 (IP: 1.1.1.2) | PASS | - |
| 160 | A-LEAF3 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: Loopback0 (IP: 1.1.1.3) - Destination: A-LEAF3 Loopback0 (IP: 1.1.1.3) | PASS | - |
| 161 | A-LEAF3 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: Loopback0 (IP: 1.1.1.3) - Destination: A-LEAF4 Loopback0 (IP: 1.1.1.4) | PASS | - |
| 162 | A-LEAF3 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: Loopback0 (IP: 1.1.1.3) - Destination: A-LEAF5 Loopback0 (IP: 1.1.1.5) | PASS | - |
| 163 | A-LEAF3 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: Loopback0 (IP: 1.1.1.3) - Destination: A-LEAF6 Loopback0 (IP: 1.1.1.6) | PASS | - |
| 164 | A-LEAF3 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: Loopback0 (IP: 1.1.1.3) - Destination: A-LEAF7 Loopback0 (IP: 1.1.1.7) | PASS | - |
| 165 | A-LEAF3 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: Loopback0 (IP: 1.1.1.3) - Destination: A-LEAF8 Loopback0 (IP: 1.1.1.8) | PASS | - |
| 166 | A-LEAF3 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: Loopback0 (IP: 1.1.1.3) - Destination: A-SPINE1 Loopback0 (IP: 1.1.1.201) | PASS | - |
| 167 | A-LEAF3 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: Loopback0 (IP: 1.1.1.3) - Destination: A-SPINE2 Loopback0 (IP: 1.1.1.202) | PASS | - |
| 168 | A-LEAF3 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: Loopback0 (IP: 1.1.1.3) - Destination: A-SPINE3 Loopback0 (IP: 1.1.1.203) | PASS | - |
| 169 | A-LEAF3 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: Loopback0 (IP: 1.1.1.3) - Destination: A-SPINE4 Loopback0 (IP: 1.1.1.204) | PASS | - |
| 170 | A-LEAF3 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: P2P Interface Ethernet1 (IP: 192.168.0.17) - Destination: A-SPINE1 Ethernet3 (IP: 192.168.0.16) | PASS | - |
| 171 | A-LEAF3 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: P2P Interface Ethernet2 (IP: 192.168.0.19) - Destination: A-SPINE2 Ethernet3 (IP: 192.168.0.18) | PASS | - |
| 172 | A-LEAF3 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: P2P Interface Ethernet3 (IP: 192.168.0.21) - Destination: A-SPINE3 Ethernet3 (IP: 192.168.0.20) | PASS | - |
| 173 | A-LEAF3 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: P2P Interface Ethernet4 (IP: 192.168.0.23) - Destination: A-SPINE4 Ethernet3 (IP: 192.168.0.22) | PASS | - |
| 174 | A-LEAF3 | Hardware | VerifyEnvironmentCooling | Verifies the status of power supply fans and all fan trays. | Accepted States: 'ok' | SKIPPED | VerifyEnvironmentCooling test is not supported on cEOSLab. |
| 175 | A-LEAF3 | Hardware | VerifyEnvironmentPower | Verifies the power supplies status. | Accepted States: 'ok' | SKIPPED | VerifyEnvironmentPower test is not supported on cEOSLab. |
| 176 | A-LEAF3 | Hardware | VerifyTemperature | Verifies the device temperature. | - | SKIPPED | VerifyTemperature test is not supported on cEOSLab. |
| 177 | A-LEAF3 | Hardware | VerifyTransceiversManufacturers | Verifies if all transceivers come from approved manufacturers. | Accepted Manufacturers: 'Arista Networks', 'Arastra, Inc.', 'Not Present' | SKIPPED | VerifyTransceiversManufacturers test is not supported on cEOSLab. |
| 178 | A-LEAF3 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Ethernet1 - P2P_A-SPINE1_Ethernet3 = 'up' | PASS | - |
| 179 | A-LEAF3 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Ethernet2 - P2P_A-SPINE2_Ethernet3 = 'up' | PASS | - |
| 180 | A-LEAF3 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Ethernet3 - P2P_A-SPINE3_Ethernet3 = 'up' | PASS | - |
| 181 | A-LEAF3 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Ethernet4 - P2P_A-SPINE4_Ethernet3 = 'up' | PASS | - |
| 182 | A-LEAF3 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Ethernet5 - MLAG_A-LEAF4_Ethernet5 = 'up' | PASS | - |
| 183 | A-LEAF3 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Ethernet6 - MLAG_A-LEAF4_Ethernet6 = 'up' | PASS | - |
| 184 | A-LEAF3 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Ethernet7 - SERVER_HostA3_eth1 = 'up' | PASS | - |
| 185 | A-LEAF3 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Ethernet8 - SERVER_HostA4_eth1 = 'up' | PASS | - |
| 186 | A-LEAF3 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Loopback0 - Globally Unique Address = 'up' | PASS | - |
| 187 | A-LEAF3 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Loopback1 - VTEP IP = 'up' | PASS | - |
| 188 | A-LEAF3 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Loopback101 - Per-VRF Unique Loopback = 'up' | PASS | - |
| 189 | A-LEAF3 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Loopback102 - Per-VRF Unique Loopback = 'up' | PASS | - |
| 190 | A-LEAF3 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Port-Channel1000 - MLAG_A-LEAF4_Port-Channel1000 = 'up' | PASS | - |
| 191 | A-LEAF3 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Port-Channel8 - SERVER_HostA4 = 'up' | PASS | - |
| 192 | A-LEAF3 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Vlan10 - Blue Network = 'up' | PASS | - |
| 193 | A-LEAF3 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Vlan30 - Orange Network = 'up' | PASS | - |
| 194 | A-LEAF3 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Vlan3001 - MLAG_L3_VRF_PROD = 'up' | PASS | - |
| 195 | A-LEAF3 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Vlan3002 - MLAG_L3_VRF_DEV = 'up' | PASS | - |
| 196 | A-LEAF3 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Vlan4093 - MLAG_L3 = 'up' | PASS | - |
| 197 | A-LEAF3 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Vlan4094 - MLAG = 'up' | PASS | - |
| 198 | A-LEAF3 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Vlan50 - Yellow Network = 'up' | PASS | - |
| 199 | A-LEAF3 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Vxlan1 = 'up' | PASS | - |
| 200 | A-LEAF3 | MLAG | VerifyMlagStatus | Verifies the health status of the MLAG configuration. | - | PASS | - |
| 201 | A-LEAF3 | Routing | VerifyRoutingProtocolModel | Verifies the configured routing protocol model. | Routing protocol model: multi-agent | PASS | - |
| 202 | A-LEAF3 | Routing | VerifyRoutingTableEntry | Verifies that the provided routes are present in the routing table of a specified VRF. | Route: 1.1.1.1 - Peer: A-LEAF1 | PASS | - |
| 203 | A-LEAF3 | Routing | VerifyRoutingTableEntry | Verifies that the provided routes are present in the routing table of a specified VRF. | Route: 1.1.1.2 - Peer: A-LEAF2 | PASS | - |
| 204 | A-LEAF3 | Routing | VerifyRoutingTableEntry | Verifies that the provided routes are present in the routing table of a specified VRF. | Route: 1.1.1.201 - Peer: A-SPINE1 | PASS | - |
| 205 | A-LEAF3 | Routing | VerifyRoutingTableEntry | Verifies that the provided routes are present in the routing table of a specified VRF. | Route: 1.1.1.202 - Peer: A-SPINE2 | PASS | - |
| 206 | A-LEAF3 | Routing | VerifyRoutingTableEntry | Verifies that the provided routes are present in the routing table of a specified VRF. | Route: 1.1.1.203 - Peer: A-SPINE3 | PASS | - |
| 207 | A-LEAF3 | Routing | VerifyRoutingTableEntry | Verifies that the provided routes are present in the routing table of a specified VRF. | Route: 1.1.1.204 - Peer: A-SPINE4 | PASS | - |
| 208 | A-LEAF3 | Routing | VerifyRoutingTableEntry | Verifies that the provided routes are present in the routing table of a specified VRF. | Route: 1.1.1.3 - Peer: A-LEAF3 | PASS | - |
| 209 | A-LEAF3 | Routing | VerifyRoutingTableEntry | Verifies that the provided routes are present in the routing table of a specified VRF. | Route: 1.1.1.4 - Peer: A-LEAF4 | PASS | - |
| 210 | A-LEAF3 | Routing | VerifyRoutingTableEntry | Verifies that the provided routes are present in the routing table of a specified VRF. | Route: 1.1.1.5 - Peer: A-LEAF5 | PASS | - |
| 211 | A-LEAF3 | Routing | VerifyRoutingTableEntry | Verifies that the provided routes are present in the routing table of a specified VRF. | Route: 1.1.1.6 - Peer: A-LEAF6 | PASS | - |
| 212 | A-LEAF3 | Routing | VerifyRoutingTableEntry | Verifies that the provided routes are present in the routing table of a specified VRF. | Route: 1.1.1.7 - Peer: A-LEAF7 | PASS | - |
| 213 | A-LEAF3 | Routing | VerifyRoutingTableEntry | Verifies that the provided routes are present in the routing table of a specified VRF. | Route: 1.1.1.8 - Peer: A-LEAF8 | PASS | - |
| 214 | A-LEAF3 | System | VerifyNTP | Verifies if NTP is synchronised. | - | PASS | - |
| 215 | A-LEAF3 | System | VerifyReloadCause | Verifies the last reload cause of the device. | - | PASS | - |
| 216 | A-LEAF4 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s). | BGP EVPN Peer: A-SPINE1 (IP: 1.1.1.201) | PASS | - |
| 217 | A-LEAF4 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s). | BGP EVPN Peer: A-SPINE2 (IP: 1.1.1.202) | PASS | - |
| 218 | A-LEAF4 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s). | BGP EVPN Peer: A-SPINE3 (IP: 1.1.1.203) | PASS | - |
| 219 | A-LEAF4 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s). | BGP EVPN Peer: A-SPINE4 (IP: 1.1.1.204) | PASS | - |
| 220 | A-LEAF4 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s). | BGP IPv4 Unicast Peer: A-LEAF3 (IP: 192.0.0.0) | PASS | - |
| 221 | A-LEAF4 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s). | BGP IPv4 Unicast Peer: A-SPINE1 (IP: 192.168.0.24) | PASS | - |
| 222 | A-LEAF4 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s). | BGP IPv4 Unicast Peer: A-SPINE2 (IP: 192.168.0.26) | PASS | - |
| 223 | A-LEAF4 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s). | BGP IPv4 Unicast Peer: A-SPINE3 (IP: 192.168.0.28) | PASS | - |
| 224 | A-LEAF4 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s). | BGP IPv4 Unicast Peer: A-SPINE4 (IP: 192.168.0.30) | PASS | - |
| 225 | A-LEAF4 | Connectivity | VerifyLLDPNeighbors | Verifies that the provided LLDP neighbors are connected properly. | Local: Ethernet1 - Remote: A-SPINE1 Ethernet4 | PASS | - |
| 226 | A-LEAF4 | Connectivity | VerifyLLDPNeighbors | Verifies that the provided LLDP neighbors are connected properly. | Local: Ethernet2 - Remote: A-SPINE2 Ethernet4 | PASS | - |
| 227 | A-LEAF4 | Connectivity | VerifyLLDPNeighbors | Verifies that the provided LLDP neighbors are connected properly. | Local: Ethernet3 - Remote: A-SPINE3 Ethernet4 | PASS | - |
| 228 | A-LEAF4 | Connectivity | VerifyLLDPNeighbors | Verifies that the provided LLDP neighbors are connected properly. | Local: Ethernet4 - Remote: A-SPINE4 Ethernet4 | PASS | - |
| 229 | A-LEAF4 | Connectivity | VerifyLLDPNeighbors | Verifies that the provided LLDP neighbors are connected properly. | Local: Ethernet5 - Remote: A-LEAF3 Ethernet5 | PASS | - |
| 230 | A-LEAF4 | Connectivity | VerifyLLDPNeighbors | Verifies that the provided LLDP neighbors are connected properly. | Local: Ethernet6 - Remote: A-LEAF3 Ethernet6 | PASS | - |
| 231 | A-LEAF4 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: Loopback0 (IP: 1.1.1.4) - Destination: A-LEAF1 Loopback0 (IP: 1.1.1.1) | PASS | - |
| 232 | A-LEAF4 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: Loopback0 (IP: 1.1.1.4) - Destination: A-LEAF2 Loopback0 (IP: 1.1.1.2) | PASS | - |
| 233 | A-LEAF4 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: Loopback0 (IP: 1.1.1.4) - Destination: A-LEAF3 Loopback0 (IP: 1.1.1.3) | PASS | - |
| 234 | A-LEAF4 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: Loopback0 (IP: 1.1.1.4) - Destination: A-LEAF4 Loopback0 (IP: 1.1.1.4) | PASS | - |
| 235 | A-LEAF4 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: Loopback0 (IP: 1.1.1.4) - Destination: A-LEAF5 Loopback0 (IP: 1.1.1.5) | PASS | - |
| 236 | A-LEAF4 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: Loopback0 (IP: 1.1.1.4) - Destination: A-LEAF6 Loopback0 (IP: 1.1.1.6) | PASS | - |
| 237 | A-LEAF4 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: Loopback0 (IP: 1.1.1.4) - Destination: A-LEAF7 Loopback0 (IP: 1.1.1.7) | PASS | - |
| 238 | A-LEAF4 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: Loopback0 (IP: 1.1.1.4) - Destination: A-LEAF8 Loopback0 (IP: 1.1.1.8) | PASS | - |
| 239 | A-LEAF4 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: Loopback0 (IP: 1.1.1.4) - Destination: A-SPINE1 Loopback0 (IP: 1.1.1.201) | PASS | - |
| 240 | A-LEAF4 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: Loopback0 (IP: 1.1.1.4) - Destination: A-SPINE2 Loopback0 (IP: 1.1.1.202) | PASS | - |
| 241 | A-LEAF4 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: Loopback0 (IP: 1.1.1.4) - Destination: A-SPINE3 Loopback0 (IP: 1.1.1.203) | PASS | - |
| 242 | A-LEAF4 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: Loopback0 (IP: 1.1.1.4) - Destination: A-SPINE4 Loopback0 (IP: 1.1.1.204) | PASS | - |
| 243 | A-LEAF4 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: P2P Interface Ethernet1 (IP: 192.168.0.25) - Destination: A-SPINE1 Ethernet4 (IP: 192.168.0.24) | PASS | - |
| 244 | A-LEAF4 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: P2P Interface Ethernet2 (IP: 192.168.0.27) - Destination: A-SPINE2 Ethernet4 (IP: 192.168.0.26) | PASS | - |
| 245 | A-LEAF4 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: P2P Interface Ethernet3 (IP: 192.168.0.29) - Destination: A-SPINE3 Ethernet4 (IP: 192.168.0.28) | PASS | - |
| 246 | A-LEAF4 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: P2P Interface Ethernet4 (IP: 192.168.0.31) - Destination: A-SPINE4 Ethernet4 (IP: 192.168.0.30) | PASS | - |
| 247 | A-LEAF4 | Hardware | VerifyEnvironmentCooling | Verifies the status of power supply fans and all fan trays. | Accepted States: 'ok' | SKIPPED | VerifyEnvironmentCooling test is not supported on cEOSLab. |
| 248 | A-LEAF4 | Hardware | VerifyEnvironmentPower | Verifies the power supplies status. | Accepted States: 'ok' | SKIPPED | VerifyEnvironmentPower test is not supported on cEOSLab. |
| 249 | A-LEAF4 | Hardware | VerifyTemperature | Verifies the device temperature. | - | SKIPPED | VerifyTemperature test is not supported on cEOSLab. |
| 250 | A-LEAF4 | Hardware | VerifyTransceiversManufacturers | Verifies if all transceivers come from approved manufacturers. | Accepted Manufacturers: 'Arista Networks', 'Arastra, Inc.', 'Not Present' | SKIPPED | VerifyTransceiversManufacturers test is not supported on cEOSLab. |
| 251 | A-LEAF4 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Ethernet1 - P2P_A-SPINE1_Ethernet4 = 'up' | PASS | - |
| 252 | A-LEAF4 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Ethernet2 - P2P_A-SPINE2_Ethernet4 = 'up' | PASS | - |
| 253 | A-LEAF4 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Ethernet3 - P2P_A-SPINE3_Ethernet4 = 'up' | PASS | - |
| 254 | A-LEAF4 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Ethernet4 - P2P_A-SPINE4_Ethernet4 = 'up' | PASS | - |
| 255 | A-LEAF4 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Ethernet5 - MLAG_A-LEAF3_Ethernet5 = 'up' | PASS | - |
| 256 | A-LEAF4 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Ethernet6 - MLAG_A-LEAF3_Ethernet6 = 'up' | PASS | - |
| 257 | A-LEAF4 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Ethernet7 - SERVER_HostA5_eth1 = 'up' | PASS | - |
| 258 | A-LEAF4 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Ethernet8 - SERVER_HostA4_eth2 = 'up' | PASS | - |
| 259 | A-LEAF4 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Loopback0 - Globally Unique Address = 'up' | PASS | - |
| 260 | A-LEAF4 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Loopback1 - VTEP IP = 'up' | PASS | - |
| 261 | A-LEAF4 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Loopback101 - Per-VRF Unique Loopback = 'up' | PASS | - |
| 262 | A-LEAF4 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Loopback102 - Per-VRF Unique Loopback = 'up' | PASS | - |
| 263 | A-LEAF4 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Port-Channel1000 - MLAG_A-LEAF3_Port-Channel1000 = 'up' | PASS | - |
| 264 | A-LEAF4 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Port-Channel8 - SERVER_HostA4 = 'up' | PASS | - |
| 265 | A-LEAF4 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Vlan10 - Blue Network = 'up' | PASS | - |
| 266 | A-LEAF4 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Vlan30 - Orange Network = 'up' | PASS | - |
| 267 | A-LEAF4 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Vlan3001 - MLAG_L3_VRF_PROD = 'up' | PASS | - |
| 268 | A-LEAF4 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Vlan3002 - MLAG_L3_VRF_DEV = 'up' | PASS | - |
| 269 | A-LEAF4 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Vlan4093 - MLAG_L3 = 'up' | PASS | - |
| 270 | A-LEAF4 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Vlan4094 - MLAG = 'up' | PASS | - |
| 271 | A-LEAF4 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Vlan50 - Yellow Network = 'up' | PASS | - |
| 272 | A-LEAF4 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Vxlan1 = 'up' | PASS | - |
| 273 | A-LEAF4 | MLAG | VerifyMlagStatus | Verifies the health status of the MLAG configuration. | - | PASS | - |
| 274 | A-LEAF4 | Routing | VerifyRoutingProtocolModel | Verifies the configured routing protocol model. | Routing protocol model: multi-agent | PASS | - |
| 275 | A-LEAF4 | Routing | VerifyRoutingTableEntry | Verifies that the provided routes are present in the routing table of a specified VRF. | Route: 1.1.1.1 - Peer: A-LEAF1 | PASS | - |
| 276 | A-LEAF4 | Routing | VerifyRoutingTableEntry | Verifies that the provided routes are present in the routing table of a specified VRF. | Route: 1.1.1.2 - Peer: A-LEAF2 | PASS | - |
| 277 | A-LEAF4 | Routing | VerifyRoutingTableEntry | Verifies that the provided routes are present in the routing table of a specified VRF. | Route: 1.1.1.201 - Peer: A-SPINE1 | PASS | - |
| 278 | A-LEAF4 | Routing | VerifyRoutingTableEntry | Verifies that the provided routes are present in the routing table of a specified VRF. | Route: 1.1.1.202 - Peer: A-SPINE2 | PASS | - |
| 279 | A-LEAF4 | Routing | VerifyRoutingTableEntry | Verifies that the provided routes are present in the routing table of a specified VRF. | Route: 1.1.1.203 - Peer: A-SPINE3 | PASS | - |
| 280 | A-LEAF4 | Routing | VerifyRoutingTableEntry | Verifies that the provided routes are present in the routing table of a specified VRF. | Route: 1.1.1.204 - Peer: A-SPINE4 | PASS | - |
| 281 | A-LEAF4 | Routing | VerifyRoutingTableEntry | Verifies that the provided routes are present in the routing table of a specified VRF. | Route: 1.1.1.3 - Peer: A-LEAF3 | PASS | - |
| 282 | A-LEAF4 | Routing | VerifyRoutingTableEntry | Verifies that the provided routes are present in the routing table of a specified VRF. | Route: 1.1.1.4 - Peer: A-LEAF4 | PASS | - |
| 283 | A-LEAF4 | Routing | VerifyRoutingTableEntry | Verifies that the provided routes are present in the routing table of a specified VRF. | Route: 1.1.1.5 - Peer: A-LEAF5 | PASS | - |
| 284 | A-LEAF4 | Routing | VerifyRoutingTableEntry | Verifies that the provided routes are present in the routing table of a specified VRF. | Route: 1.1.1.6 - Peer: A-LEAF6 | PASS | - |
| 285 | A-LEAF4 | Routing | VerifyRoutingTableEntry | Verifies that the provided routes are present in the routing table of a specified VRF. | Route: 1.1.1.7 - Peer: A-LEAF7 | PASS | - |
| 286 | A-LEAF4 | Routing | VerifyRoutingTableEntry | Verifies that the provided routes are present in the routing table of a specified VRF. | Route: 1.1.1.8 - Peer: A-LEAF8 | PASS | - |
| 287 | A-LEAF4 | System | VerifyNTP | Verifies if NTP is synchronised. | - | PASS | - |
| 288 | A-LEAF4 | System | VerifyReloadCause | Verifies the last reload cause of the device. | - | PASS | - |
| 289 | A-LEAF5 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s). | BGP EVPN Peer: A-SPINE1 (IP: 1.1.1.201) | PASS | - |
| 290 | A-LEAF5 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s). | BGP EVPN Peer: A-SPINE2 (IP: 1.1.1.202) | PASS | - |
| 291 | A-LEAF5 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s). | BGP EVPN Peer: A-SPINE3 (IP: 1.1.1.203) | PASS | - |
| 292 | A-LEAF5 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s). | BGP EVPN Peer: A-SPINE4 (IP: 1.1.1.204) | PASS | - |
| 293 | A-LEAF5 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s). | BGP IPv4 Unicast Peer: A-LEAF6 (IP: 192.0.0.1) | PASS | - |
| 294 | A-LEAF5 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s). | BGP IPv4 Unicast Peer: A-SPINE1 (IP: 192.168.0.32) | PASS | - |
| 295 | A-LEAF5 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s). | BGP IPv4 Unicast Peer: A-SPINE2 (IP: 192.168.0.34) | PASS | - |
| 296 | A-LEAF5 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s). | BGP IPv4 Unicast Peer: A-SPINE3 (IP: 192.168.0.36) | PASS | - |
| 297 | A-LEAF5 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s). | BGP IPv4 Unicast Peer: A-SPINE4 (IP: 192.168.0.38) | PASS | - |
| 298 | A-LEAF5 | Connectivity | VerifyLLDPNeighbors | Verifies that the provided LLDP neighbors are connected properly. | Local: Ethernet1 - Remote: A-SPINE1 Ethernet5 | PASS | - |
| 299 | A-LEAF5 | Connectivity | VerifyLLDPNeighbors | Verifies that the provided LLDP neighbors are connected properly. | Local: Ethernet2 - Remote: A-SPINE2 Ethernet5 | PASS | - |
| 300 | A-LEAF5 | Connectivity | VerifyLLDPNeighbors | Verifies that the provided LLDP neighbors are connected properly. | Local: Ethernet3 - Remote: A-SPINE3 Ethernet5 | PASS | - |
| 301 | A-LEAF5 | Connectivity | VerifyLLDPNeighbors | Verifies that the provided LLDP neighbors are connected properly. | Local: Ethernet4 - Remote: A-SPINE4 Ethernet5 | PASS | - |
| 302 | A-LEAF5 | Connectivity | VerifyLLDPNeighbors | Verifies that the provided LLDP neighbors are connected properly. | Local: Ethernet5 - Remote: A-LEAF6 Ethernet5 | PASS | - |
| 303 | A-LEAF5 | Connectivity | VerifyLLDPNeighbors | Verifies that the provided LLDP neighbors are connected properly. | Local: Ethernet6 - Remote: A-LEAF6 Ethernet6 | PASS | - |
| 304 | A-LEAF5 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: Loopback0 (IP: 1.1.1.5) - Destination: A-LEAF1 Loopback0 (IP: 1.1.1.1) | PASS | - |
| 305 | A-LEAF5 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: Loopback0 (IP: 1.1.1.5) - Destination: A-LEAF2 Loopback0 (IP: 1.1.1.2) | PASS | - |
| 306 | A-LEAF5 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: Loopback0 (IP: 1.1.1.5) - Destination: A-LEAF3 Loopback0 (IP: 1.1.1.3) | PASS | - |
| 307 | A-LEAF5 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: Loopback0 (IP: 1.1.1.5) - Destination: A-LEAF4 Loopback0 (IP: 1.1.1.4) | PASS | - |
| 308 | A-LEAF5 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: Loopback0 (IP: 1.1.1.5) - Destination: A-LEAF5 Loopback0 (IP: 1.1.1.5) | PASS | - |
| 309 | A-LEAF5 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: Loopback0 (IP: 1.1.1.5) - Destination: A-LEAF6 Loopback0 (IP: 1.1.1.6) | PASS | - |
| 310 | A-LEAF5 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: Loopback0 (IP: 1.1.1.5) - Destination: A-LEAF7 Loopback0 (IP: 1.1.1.7) | PASS | - |
| 311 | A-LEAF5 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: Loopback0 (IP: 1.1.1.5) - Destination: A-LEAF8 Loopback0 (IP: 1.1.1.8) | PASS | - |
| 312 | A-LEAF5 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: Loopback0 (IP: 1.1.1.5) - Destination: A-SPINE1 Loopback0 (IP: 1.1.1.201) | PASS | - |
| 313 | A-LEAF5 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: Loopback0 (IP: 1.1.1.5) - Destination: A-SPINE2 Loopback0 (IP: 1.1.1.202) | PASS | - |
| 314 | A-LEAF5 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: Loopback0 (IP: 1.1.1.5) - Destination: A-SPINE3 Loopback0 (IP: 1.1.1.203) | PASS | - |
| 315 | A-LEAF5 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: Loopback0 (IP: 1.1.1.5) - Destination: A-SPINE4 Loopback0 (IP: 1.1.1.204) | PASS | - |
| 316 | A-LEAF5 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: P2P Interface Ethernet1 (IP: 192.168.0.33) - Destination: A-SPINE1 Ethernet5 (IP: 192.168.0.32) | PASS | - |
| 317 | A-LEAF5 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: P2P Interface Ethernet2 (IP: 192.168.0.35) - Destination: A-SPINE2 Ethernet5 (IP: 192.168.0.34) | PASS | - |
| 318 | A-LEAF5 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: P2P Interface Ethernet3 (IP: 192.168.0.37) - Destination: A-SPINE3 Ethernet5 (IP: 192.168.0.36) | PASS | - |
| 319 | A-LEAF5 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: P2P Interface Ethernet4 (IP: 192.168.0.39) - Destination: A-SPINE4 Ethernet5 (IP: 192.168.0.38) | PASS | - |
| 320 | A-LEAF5 | Hardware | VerifyEnvironmentCooling | Verifies the status of power supply fans and all fan trays. | Accepted States: 'ok' | SKIPPED | VerifyEnvironmentCooling test is not supported on cEOSLab. |
| 321 | A-LEAF5 | Hardware | VerifyEnvironmentPower | Verifies the power supplies status. | Accepted States: 'ok' | SKIPPED | VerifyEnvironmentPower test is not supported on cEOSLab. |
| 322 | A-LEAF5 | Hardware | VerifyTemperature | Verifies the device temperature. | - | SKIPPED | VerifyTemperature test is not supported on cEOSLab. |
| 323 | A-LEAF5 | Hardware | VerifyTransceiversManufacturers | Verifies if all transceivers come from approved manufacturers. | Accepted Manufacturers: 'Arista Networks', 'Arastra, Inc.', 'Not Present' | SKIPPED | VerifyTransceiversManufacturers test is not supported on cEOSLab. |
| 324 | A-LEAF5 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Ethernet1 - P2P_A-SPINE1_Ethernet5 = 'up' | PASS | - |
| 325 | A-LEAF5 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Ethernet2 - P2P_A-SPINE2_Ethernet5 = 'up' | PASS | - |
| 326 | A-LEAF5 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Ethernet3 - P2P_A-SPINE3_Ethernet5 = 'up' | PASS | - |
| 327 | A-LEAF5 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Ethernet4 - P2P_A-SPINE4_Ethernet5 = 'up' | PASS | - |
| 328 | A-LEAF5 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Ethernet5 - MLAG_A-LEAF6_Ethernet5 = 'up' | PASS | - |
| 329 | A-LEAF5 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Ethernet6 - MLAG_A-LEAF6_Ethernet6 = 'up' | PASS | - |
| 330 | A-LEAF5 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Ethernet7 - SERVER_HostA6_eth1 = 'up' | PASS | - |
| 331 | A-LEAF5 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Loopback0 - Globally Unique Address = 'up' | PASS | - |
| 332 | A-LEAF5 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Loopback1 - VTEP IP = 'up' | PASS | - |
| 333 | A-LEAF5 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Loopback102 - Per-VRF Unique Loopback = 'up' | PASS | - |
| 334 | A-LEAF5 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Port-Channel1000 - MLAG_A-LEAF6_Port-Channel1000 = 'up' | PASS | - |
| 335 | A-LEAF5 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Port-Channel7 - SERVER_HostA6 = 'up' | PASS | - |
| 336 | A-LEAF5 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Vlan3002 - MLAG_L3_VRF_DEV = 'up' | PASS | - |
| 337 | A-LEAF5 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Vlan4093 - MLAG_L3 = 'up' | PASS | - |
| 338 | A-LEAF5 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Vlan4094 - MLAG = 'up' | PASS | - |
| 339 | A-LEAF5 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Vlan70 - Brown Network = 'up' | PASS | - |
| 340 | A-LEAF5 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Vxlan1 = 'up' | PASS | - |
| 341 | A-LEAF5 | MLAG | VerifyMlagStatus | Verifies the health status of the MLAG configuration. | - | PASS | - |
| 342 | A-LEAF5 | Routing | VerifyRoutingProtocolModel | Verifies the configured routing protocol model. | Routing protocol model: multi-agent | PASS | - |
| 343 | A-LEAF5 | Routing | VerifyRoutingTableEntry | Verifies that the provided routes are present in the routing table of a specified VRF. | Route: 1.1.1.1 - Peer: A-LEAF1 | PASS | - |
| 344 | A-LEAF5 | Routing | VerifyRoutingTableEntry | Verifies that the provided routes are present in the routing table of a specified VRF. | Route: 1.1.1.2 - Peer: A-LEAF2 | PASS | - |
| 345 | A-LEAF5 | Routing | VerifyRoutingTableEntry | Verifies that the provided routes are present in the routing table of a specified VRF. | Route: 1.1.1.201 - Peer: A-SPINE1 | PASS | - |
| 346 | A-LEAF5 | Routing | VerifyRoutingTableEntry | Verifies that the provided routes are present in the routing table of a specified VRF. | Route: 1.1.1.202 - Peer: A-SPINE2 | PASS | - |
| 347 | A-LEAF5 | Routing | VerifyRoutingTableEntry | Verifies that the provided routes are present in the routing table of a specified VRF. | Route: 1.1.1.203 - Peer: A-SPINE3 | PASS | - |
| 348 | A-LEAF5 | Routing | VerifyRoutingTableEntry | Verifies that the provided routes are present in the routing table of a specified VRF. | Route: 1.1.1.204 - Peer: A-SPINE4 | PASS | - |
| 349 | A-LEAF5 | Routing | VerifyRoutingTableEntry | Verifies that the provided routes are present in the routing table of a specified VRF. | Route: 1.1.1.3 - Peer: A-LEAF3 | PASS | - |
| 350 | A-LEAF5 | Routing | VerifyRoutingTableEntry | Verifies that the provided routes are present in the routing table of a specified VRF. | Route: 1.1.1.4 - Peer: A-LEAF4 | PASS | - |
| 351 | A-LEAF5 | Routing | VerifyRoutingTableEntry | Verifies that the provided routes are present in the routing table of a specified VRF. | Route: 1.1.1.5 - Peer: A-LEAF5 | PASS | - |
| 352 | A-LEAF5 | Routing | VerifyRoutingTableEntry | Verifies that the provided routes are present in the routing table of a specified VRF. | Route: 1.1.1.6 - Peer: A-LEAF6 | PASS | - |
| 353 | A-LEAF5 | Routing | VerifyRoutingTableEntry | Verifies that the provided routes are present in the routing table of a specified VRF. | Route: 1.1.1.7 - Peer: A-LEAF7 | PASS | - |
| 354 | A-LEAF5 | Routing | VerifyRoutingTableEntry | Verifies that the provided routes are present in the routing table of a specified VRF. | Route: 1.1.1.8 - Peer: A-LEAF8 | PASS | - |
| 355 | A-LEAF5 | System | VerifyNTP | Verifies if NTP is synchronised. | - | PASS | - |
| 356 | A-LEAF5 | System | VerifyReloadCause | Verifies the last reload cause of the device. | - | PASS | - |
| 357 | A-LEAF6 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s). | BGP EVPN Peer: A-SPINE1 (IP: 1.1.1.201) | PASS | - |
| 358 | A-LEAF6 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s). | BGP EVPN Peer: A-SPINE2 (IP: 1.1.1.202) | PASS | - |
| 359 | A-LEAF6 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s). | BGP EVPN Peer: A-SPINE3 (IP: 1.1.1.203) | PASS | - |
| 360 | A-LEAF6 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s). | BGP EVPN Peer: A-SPINE4 (IP: 1.1.1.204) | PASS | - |
| 361 | A-LEAF6 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s). | BGP IPv4 Unicast Peer: A-LEAF5 (IP: 192.0.0.0) | PASS | - |
| 362 | A-LEAF6 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s). | BGP IPv4 Unicast Peer: A-SPINE1 (IP: 192.168.0.40) | PASS | - |
| 363 | A-LEAF6 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s). | BGP IPv4 Unicast Peer: A-SPINE2 (IP: 192.168.0.42) | PASS | - |
| 364 | A-LEAF6 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s). | BGP IPv4 Unicast Peer: A-SPINE3 (IP: 192.168.0.44) | PASS | - |
| 365 | A-LEAF6 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s). | BGP IPv4 Unicast Peer: A-SPINE4 (IP: 192.168.0.46) | PASS | - |
| 366 | A-LEAF6 | Connectivity | VerifyLLDPNeighbors | Verifies that the provided LLDP neighbors are connected properly. | Local: Ethernet1 - Remote: A-SPINE1 Ethernet6 | PASS | - |
| 367 | A-LEAF6 | Connectivity | VerifyLLDPNeighbors | Verifies that the provided LLDP neighbors are connected properly. | Local: Ethernet2 - Remote: A-SPINE2 Ethernet6 | PASS | - |
| 368 | A-LEAF6 | Connectivity | VerifyLLDPNeighbors | Verifies that the provided LLDP neighbors are connected properly. | Local: Ethernet3 - Remote: A-SPINE3 Ethernet6 | PASS | - |
| 369 | A-LEAF6 | Connectivity | VerifyLLDPNeighbors | Verifies that the provided LLDP neighbors are connected properly. | Local: Ethernet4 - Remote: A-SPINE4 Ethernet6 | PASS | - |
| 370 | A-LEAF6 | Connectivity | VerifyLLDPNeighbors | Verifies that the provided LLDP neighbors are connected properly. | Local: Ethernet5 - Remote: A-LEAF5 Ethernet5 | PASS | - |
| 371 | A-LEAF6 | Connectivity | VerifyLLDPNeighbors | Verifies that the provided LLDP neighbors are connected properly. | Local: Ethernet6 - Remote: A-LEAF5 Ethernet6 | PASS | - |
| 372 | A-LEAF6 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: Loopback0 (IP: 1.1.1.6) - Destination: A-LEAF1 Loopback0 (IP: 1.1.1.1) | PASS | - |
| 373 | A-LEAF6 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: Loopback0 (IP: 1.1.1.6) - Destination: A-LEAF2 Loopback0 (IP: 1.1.1.2) | PASS | - |
| 374 | A-LEAF6 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: Loopback0 (IP: 1.1.1.6) - Destination: A-LEAF3 Loopback0 (IP: 1.1.1.3) | PASS | - |
| 375 | A-LEAF6 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: Loopback0 (IP: 1.1.1.6) - Destination: A-LEAF4 Loopback0 (IP: 1.1.1.4) | PASS | - |
| 376 | A-LEAF6 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: Loopback0 (IP: 1.1.1.6) - Destination: A-LEAF5 Loopback0 (IP: 1.1.1.5) | PASS | - |
| 377 | A-LEAF6 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: Loopback0 (IP: 1.1.1.6) - Destination: A-LEAF6 Loopback0 (IP: 1.1.1.6) | PASS | - |
| 378 | A-LEAF6 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: Loopback0 (IP: 1.1.1.6) - Destination: A-LEAF7 Loopback0 (IP: 1.1.1.7) | PASS | - |
| 379 | A-LEAF6 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: Loopback0 (IP: 1.1.1.6) - Destination: A-LEAF8 Loopback0 (IP: 1.1.1.8) | PASS | - |
| 380 | A-LEAF6 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: Loopback0 (IP: 1.1.1.6) - Destination: A-SPINE1 Loopback0 (IP: 1.1.1.201) | PASS | - |
| 381 | A-LEAF6 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: Loopback0 (IP: 1.1.1.6) - Destination: A-SPINE2 Loopback0 (IP: 1.1.1.202) | PASS | - |
| 382 | A-LEAF6 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: Loopback0 (IP: 1.1.1.6) - Destination: A-SPINE3 Loopback0 (IP: 1.1.1.203) | PASS | - |
| 383 | A-LEAF6 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: Loopback0 (IP: 1.1.1.6) - Destination: A-SPINE4 Loopback0 (IP: 1.1.1.204) | PASS | - |
| 384 | A-LEAF6 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: P2P Interface Ethernet1 (IP: 192.168.0.41) - Destination: A-SPINE1 Ethernet6 (IP: 192.168.0.40) | PASS | - |
| 385 | A-LEAF6 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: P2P Interface Ethernet2 (IP: 192.168.0.43) - Destination: A-SPINE2 Ethernet6 (IP: 192.168.0.42) | PASS | - |
| 386 | A-LEAF6 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: P2P Interface Ethernet3 (IP: 192.168.0.45) - Destination: A-SPINE3 Ethernet6 (IP: 192.168.0.44) | PASS | - |
| 387 | A-LEAF6 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: P2P Interface Ethernet4 (IP: 192.168.0.47) - Destination: A-SPINE4 Ethernet6 (IP: 192.168.0.46) | PASS | - |
| 388 | A-LEAF6 | Hardware | VerifyEnvironmentCooling | Verifies the status of power supply fans and all fan trays. | Accepted States: 'ok' | SKIPPED | VerifyEnvironmentCooling test is not supported on cEOSLab. |
| 389 | A-LEAF6 | Hardware | VerifyEnvironmentPower | Verifies the power supplies status. | Accepted States: 'ok' | SKIPPED | VerifyEnvironmentPower test is not supported on cEOSLab. |
| 390 | A-LEAF6 | Hardware | VerifyTemperature | Verifies the device temperature. | - | SKIPPED | VerifyTemperature test is not supported on cEOSLab. |
| 391 | A-LEAF6 | Hardware | VerifyTransceiversManufacturers | Verifies if all transceivers come from approved manufacturers. | Accepted Manufacturers: 'Arista Networks', 'Arastra, Inc.', 'Not Present' | SKIPPED | VerifyTransceiversManufacturers test is not supported on cEOSLab. |
| 392 | A-LEAF6 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Ethernet1 - P2P_A-SPINE1_Ethernet6 = 'up' | PASS | - |
| 393 | A-LEAF6 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Ethernet2 - P2P_A-SPINE2_Ethernet6 = 'up' | PASS | - |
| 394 | A-LEAF6 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Ethernet3 - P2P_A-SPINE3_Ethernet6 = 'up' | PASS | - |
| 395 | A-LEAF6 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Ethernet4 - P2P_A-SPINE4_Ethernet6 = 'up' | PASS | - |
| 396 | A-LEAF6 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Ethernet5 - MLAG_A-LEAF5_Ethernet5 = 'up' | PASS | - |
| 397 | A-LEAF6 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Ethernet6 - MLAG_A-LEAF5_Ethernet6 = 'up' | PASS | - |
| 398 | A-LEAF6 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Ethernet7 - SERVER_HostA6_eth2 = 'up' | PASS | - |
| 399 | A-LEAF6 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Loopback0 - Globally Unique Address = 'up' | PASS | - |
| 400 | A-LEAF6 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Loopback1 - VTEP IP = 'up' | PASS | - |
| 401 | A-LEAF6 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Loopback102 - Per-VRF Unique Loopback = 'up' | PASS | - |
| 402 | A-LEAF6 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Port-Channel1000 - MLAG_A-LEAF5_Port-Channel1000 = 'up' | PASS | - |
| 403 | A-LEAF6 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Port-Channel7 - SERVER_HostA6 = 'up' | PASS | - |
| 404 | A-LEAF6 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Vlan3002 - MLAG_L3_VRF_DEV = 'up' | PASS | - |
| 405 | A-LEAF6 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Vlan4093 - MLAG_L3 = 'up' | PASS | - |
| 406 | A-LEAF6 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Vlan4094 - MLAG = 'up' | PASS | - |
| 407 | A-LEAF6 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Vlan70 - Brown Network = 'up' | PASS | - |
| 408 | A-LEAF6 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Vxlan1 = 'up' | PASS | - |
| 409 | A-LEAF6 | MLAG | VerifyMlagStatus | Verifies the health status of the MLAG configuration. | - | PASS | - |
| 410 | A-LEAF6 | Routing | VerifyRoutingProtocolModel | Verifies the configured routing protocol model. | Routing protocol model: multi-agent | PASS | - |
| 411 | A-LEAF6 | Routing | VerifyRoutingTableEntry | Verifies that the provided routes are present in the routing table of a specified VRF. | Route: 1.1.1.1 - Peer: A-LEAF1 | PASS | - |
| 412 | A-LEAF6 | Routing | VerifyRoutingTableEntry | Verifies that the provided routes are present in the routing table of a specified VRF. | Route: 1.1.1.2 - Peer: A-LEAF2 | PASS | - |
| 413 | A-LEAF6 | Routing | VerifyRoutingTableEntry | Verifies that the provided routes are present in the routing table of a specified VRF. | Route: 1.1.1.201 - Peer: A-SPINE1 | PASS | - |
| 414 | A-LEAF6 | Routing | VerifyRoutingTableEntry | Verifies that the provided routes are present in the routing table of a specified VRF. | Route: 1.1.1.202 - Peer: A-SPINE2 | PASS | - |
| 415 | A-LEAF6 | Routing | VerifyRoutingTableEntry | Verifies that the provided routes are present in the routing table of a specified VRF. | Route: 1.1.1.203 - Peer: A-SPINE3 | PASS | - |
| 416 | A-LEAF6 | Routing | VerifyRoutingTableEntry | Verifies that the provided routes are present in the routing table of a specified VRF. | Route: 1.1.1.204 - Peer: A-SPINE4 | PASS | - |
| 417 | A-LEAF6 | Routing | VerifyRoutingTableEntry | Verifies that the provided routes are present in the routing table of a specified VRF. | Route: 1.1.1.3 - Peer: A-LEAF3 | PASS | - |
| 418 | A-LEAF6 | Routing | VerifyRoutingTableEntry | Verifies that the provided routes are present in the routing table of a specified VRF. | Route: 1.1.1.4 - Peer: A-LEAF4 | PASS | - |
| 419 | A-LEAF6 | Routing | VerifyRoutingTableEntry | Verifies that the provided routes are present in the routing table of a specified VRF. | Route: 1.1.1.5 - Peer: A-LEAF5 | PASS | - |
| 420 | A-LEAF6 | Routing | VerifyRoutingTableEntry | Verifies that the provided routes are present in the routing table of a specified VRF. | Route: 1.1.1.6 - Peer: A-LEAF6 | PASS | - |
| 421 | A-LEAF6 | Routing | VerifyRoutingTableEntry | Verifies that the provided routes are present in the routing table of a specified VRF. | Route: 1.1.1.7 - Peer: A-LEAF7 | PASS | - |
| 422 | A-LEAF6 | Routing | VerifyRoutingTableEntry | Verifies that the provided routes are present in the routing table of a specified VRF. | Route: 1.1.1.8 - Peer: A-LEAF8 | PASS | - |
| 423 | A-LEAF6 | System | VerifyNTP | Verifies if NTP is synchronised. | - | PASS | - |
| 424 | A-LEAF6 | System | VerifyReloadCause | Verifies the last reload cause of the device. | - | PASS | - |
| 425 | A-LEAF7 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s). | BGP EVPN Peer: A-SPINE1 (IP: 1.1.1.201) | PASS | - |
| 426 | A-LEAF7 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s). | BGP EVPN Peer: A-SPINE2 (IP: 1.1.1.202) | PASS | - |
| 427 | A-LEAF7 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s). | BGP EVPN Peer: A-SPINE3 (IP: 1.1.1.203) | PASS | - |
| 428 | A-LEAF7 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s). | BGP EVPN Peer: A-SPINE4 (IP: 1.1.1.204) | PASS | - |
| 429 | A-LEAF7 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s). | BGP IPv4 Unicast Peer: 172.16.1.0 | PASS | - |
| 430 | A-LEAF7 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s). | BGP IPv4 Unicast Peer: 172.16.1.4 | PASS | - |
| 431 | A-LEAF7 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s). | BGP IPv4 Unicast Peer: A-LEAF8 (IP: 192.0.0.1) | PASS | - |
| 432 | A-LEAF7 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s). | BGP IPv4 Unicast Peer: A-SPINE1 (IP: 192.168.0.48) | PASS | - |
| 433 | A-LEAF7 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s). | BGP IPv4 Unicast Peer: A-SPINE2 (IP: 192.168.0.50) | PASS | - |
| 434 | A-LEAF7 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s). | BGP IPv4 Unicast Peer: A-SPINE3 (IP: 192.168.0.52) | PASS | - |
| 435 | A-LEAF7 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s). | BGP IPv4 Unicast Peer: A-SPINE4 (IP: 192.168.0.54) | PASS | - |
| 436 | A-LEAF7 | Connectivity | VerifyLLDPNeighbors | Verifies that the provided LLDP neighbors are connected properly. | Local: Ethernet1 - Remote: A-SPINE1 Ethernet7 | PASS | - |
| 437 | A-LEAF7 | Connectivity | VerifyLLDPNeighbors | Verifies that the provided LLDP neighbors are connected properly. | Local: Ethernet2 - Remote: A-SPINE2 Ethernet7 | PASS | - |
| 438 | A-LEAF7 | Connectivity | VerifyLLDPNeighbors | Verifies that the provided LLDP neighbors are connected properly. | Local: Ethernet3 - Remote: A-SPINE3 Ethernet7 | PASS | - |
| 439 | A-LEAF7 | Connectivity | VerifyLLDPNeighbors | Verifies that the provided LLDP neighbors are connected properly. | Local: Ethernet4 - Remote: A-SPINE4 Ethernet7 | PASS | - |
| 440 | A-LEAF7 | Connectivity | VerifyLLDPNeighbors | Verifies that the provided LLDP neighbors are connected properly. | Local: Ethernet5 - Remote: A-LEAF8 Ethernet5 | PASS | - |
| 441 | A-LEAF7 | Connectivity | VerifyLLDPNeighbors | Verifies that the provided LLDP neighbors are connected properly. | Local: Ethernet6 - Remote: A-LEAF8 Ethernet6 | PASS | - |
| 442 | A-LEAF7 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: Loopback0 (IP: 1.1.1.7) - Destination: A-LEAF1 Loopback0 (IP: 1.1.1.1) | PASS | - |
| 443 | A-LEAF7 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: Loopback0 (IP: 1.1.1.7) - Destination: A-LEAF2 Loopback0 (IP: 1.1.1.2) | PASS | - |
| 444 | A-LEAF7 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: Loopback0 (IP: 1.1.1.7) - Destination: A-LEAF3 Loopback0 (IP: 1.1.1.3) | PASS | - |
| 445 | A-LEAF7 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: Loopback0 (IP: 1.1.1.7) - Destination: A-LEAF4 Loopback0 (IP: 1.1.1.4) | PASS | - |
| 446 | A-LEAF7 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: Loopback0 (IP: 1.1.1.7) - Destination: A-LEAF5 Loopback0 (IP: 1.1.1.5) | PASS | - |
| 447 | A-LEAF7 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: Loopback0 (IP: 1.1.1.7) - Destination: A-LEAF6 Loopback0 (IP: 1.1.1.6) | PASS | - |
| 448 | A-LEAF7 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: Loopback0 (IP: 1.1.1.7) - Destination: A-LEAF7 Loopback0 (IP: 1.1.1.7) | PASS | - |
| 449 | A-LEAF7 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: Loopback0 (IP: 1.1.1.7) - Destination: A-LEAF8 Loopback0 (IP: 1.1.1.8) | PASS | - |
| 450 | A-LEAF7 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: Loopback0 (IP: 1.1.1.7) - Destination: A-SPINE1 Loopback0 (IP: 1.1.1.201) | PASS | - |
| 451 | A-LEAF7 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: Loopback0 (IP: 1.1.1.7) - Destination: A-SPINE2 Loopback0 (IP: 1.1.1.202) | PASS | - |
| 452 | A-LEAF7 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: Loopback0 (IP: 1.1.1.7) - Destination: A-SPINE3 Loopback0 (IP: 1.1.1.203) | PASS | - |
| 453 | A-LEAF7 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: Loopback0 (IP: 1.1.1.7) - Destination: A-SPINE4 Loopback0 (IP: 1.1.1.204) | PASS | - |
| 454 | A-LEAF7 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: P2P Interface Ethernet1 (IP: 192.168.0.49) - Destination: A-SPINE1 Ethernet7 (IP: 192.168.0.48) | PASS | - |
| 455 | A-LEAF7 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: P2P Interface Ethernet2 (IP: 192.168.0.51) - Destination: A-SPINE2 Ethernet7 (IP: 192.168.0.50) | PASS | - |
| 456 | A-LEAF7 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: P2P Interface Ethernet3 (IP: 192.168.0.53) - Destination: A-SPINE3 Ethernet7 (IP: 192.168.0.52) | PASS | - |
| 457 | A-LEAF7 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: P2P Interface Ethernet4 (IP: 192.168.0.55) - Destination: A-SPINE4 Ethernet7 (IP: 192.168.0.54) | PASS | - |
| 458 | A-LEAF7 | Hardware | VerifyEnvironmentCooling | Verifies the status of power supply fans and all fan trays. | Accepted States: 'ok' | SKIPPED | VerifyEnvironmentCooling test is not supported on cEOSLab. |
| 459 | A-LEAF7 | Hardware | VerifyEnvironmentPower | Verifies the power supplies status. | Accepted States: 'ok' | SKIPPED | VerifyEnvironmentPower test is not supported on cEOSLab. |
| 460 | A-LEAF7 | Hardware | VerifyTemperature | Verifies the device temperature. | - | SKIPPED | VerifyTemperature test is not supported on cEOSLab. |
| 461 | A-LEAF7 | Hardware | VerifyTransceiversManufacturers | Verifies if all transceivers come from approved manufacturers. | Accepted Manufacturers: 'Arista Networks', 'Arastra, Inc.', 'Not Present' | SKIPPED | VerifyTransceiversManufacturers test is not supported on cEOSLab. |
| 462 | A-LEAF7 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Ethernet1 - P2P_A-SPINE1_Ethernet7 = 'up' | PASS | - |
| 463 | A-LEAF7 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Ethernet2 - P2P_A-SPINE2_Ethernet7 = 'up' | PASS | - |
| 464 | A-LEAF7 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Ethernet3 - P2P_A-SPINE3_Ethernet7 = 'up' | PASS | - |
| 465 | A-LEAF7 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Ethernet4 - P2P_A-SPINE4_Ethernet7 = 'up' | PASS | - |
| 466 | A-LEAF7 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Ethernet5 - MLAG_A-LEAF8_Ethernet5 = 'up' | PASS | - |
| 467 | A-LEAF7 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Ethernet6 - MLAG_A-LEAF8_Ethernet6 = 'up' | PASS | - |
| 468 | A-LEAF7 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Ethernet7 - P2P_BB1_Ethernet1 = 'up' | PASS | - |
| 469 | A-LEAF7 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Ethernet8 - P2P_BB2_Ethernet1 = 'up' | PASS | - |
| 470 | A-LEAF7 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Loopback0 - Globally Unique Address = 'up' | PASS | - |
| 471 | A-LEAF7 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Loopback1 - VTEP IP = 'up' | PASS | - |
| 472 | A-LEAF7 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Loopback101 - Per-VRF Unique Loopback = 'up' | PASS | - |
| 473 | A-LEAF7 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Loopback102 - Per-VRF Unique Loopback = 'up' | PASS | - |
| 474 | A-LEAF7 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Port-Channel1000 - MLAG_A-LEAF8_Port-Channel1000 = 'up' | PASS | - |
| 475 | A-LEAF7 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Vlan10 - Blue Network = 'up' | PASS | - |
| 476 | A-LEAF7 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Vlan30 - Orange Network = 'up' | PASS | - |
| 477 | A-LEAF7 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Vlan3001 - MLAG_L3_VRF_PROD = 'up' | PASS | - |
| 478 | A-LEAF7 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Vlan3002 - MLAG_L3_VRF_DEV = 'up' | PASS | - |
| 479 | A-LEAF7 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Vlan4093 - MLAG_L3 = 'up' | PASS | - |
| 480 | A-LEAF7 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Vlan4094 - MLAG = 'up' | PASS | - |
| 481 | A-LEAF7 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Vlan50 - Yellow Network = 'up' | PASS | - |
| 482 | A-LEAF7 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Vlan70 - Brown Network = 'up' | PASS | - |
| 483 | A-LEAF7 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Vxlan1 = 'up' | PASS | - |
| 484 | A-LEAF7 | MLAG | VerifyMlagStatus | Verifies the health status of the MLAG configuration. | - | PASS | - |
| 485 | A-LEAF7 | Routing | VerifyRoutingProtocolModel | Verifies the configured routing protocol model. | Routing protocol model: multi-agent | PASS | - |
| 486 | A-LEAF7 | Routing | VerifyRoutingTableEntry | Verifies that the provided routes are present in the routing table of a specified VRF. | Route: 1.1.1.1 - Peer: A-LEAF1 | PASS | - |
| 487 | A-LEAF7 | Routing | VerifyRoutingTableEntry | Verifies that the provided routes are present in the routing table of a specified VRF. | Route: 1.1.1.2 - Peer: A-LEAF2 | PASS | - |
| 488 | A-LEAF7 | Routing | VerifyRoutingTableEntry | Verifies that the provided routes are present in the routing table of a specified VRF. | Route: 1.1.1.201 - Peer: A-SPINE1 | PASS | - |
| 489 | A-LEAF7 | Routing | VerifyRoutingTableEntry | Verifies that the provided routes are present in the routing table of a specified VRF. | Route: 1.1.1.202 - Peer: A-SPINE2 | PASS | - |
| 490 | A-LEAF7 | Routing | VerifyRoutingTableEntry | Verifies that the provided routes are present in the routing table of a specified VRF. | Route: 1.1.1.203 - Peer: A-SPINE3 | PASS | - |
| 491 | A-LEAF7 | Routing | VerifyRoutingTableEntry | Verifies that the provided routes are present in the routing table of a specified VRF. | Route: 1.1.1.204 - Peer: A-SPINE4 | PASS | - |
| 492 | A-LEAF7 | Routing | VerifyRoutingTableEntry | Verifies that the provided routes are present in the routing table of a specified VRF. | Route: 1.1.1.3 - Peer: A-LEAF3 | PASS | - |
| 493 | A-LEAF7 | Routing | VerifyRoutingTableEntry | Verifies that the provided routes are present in the routing table of a specified VRF. | Route: 1.1.1.4 - Peer: A-LEAF4 | PASS | - |
| 494 | A-LEAF7 | Routing | VerifyRoutingTableEntry | Verifies that the provided routes are present in the routing table of a specified VRF. | Route: 1.1.1.5 - Peer: A-LEAF5 | PASS | - |
| 495 | A-LEAF7 | Routing | VerifyRoutingTableEntry | Verifies that the provided routes are present in the routing table of a specified VRF. | Route: 1.1.1.6 - Peer: A-LEAF6 | PASS | - |
| 496 | A-LEAF7 | Routing | VerifyRoutingTableEntry | Verifies that the provided routes are present in the routing table of a specified VRF. | Route: 1.1.1.7 - Peer: A-LEAF7 | PASS | - |
| 497 | A-LEAF7 | Routing | VerifyRoutingTableEntry | Verifies that the provided routes are present in the routing table of a specified VRF. | Route: 1.1.1.8 - Peer: A-LEAF8 | PASS | - |
| 498 | A-LEAF7 | System | VerifyNTP | Verifies if NTP is synchronised. | - | PASS | - |
| 499 | A-LEAF7 | System | VerifyReloadCause | Verifies the last reload cause of the device. | - | PASS | - |
| 500 | A-LEAF8 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s). | BGP EVPN Peer: A-SPINE1 (IP: 1.1.1.201) | PASS | - |
| 501 | A-LEAF8 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s). | BGP EVPN Peer: A-SPINE2 (IP: 1.1.1.202) | PASS | - |
| 502 | A-LEAF8 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s). | BGP EVPN Peer: A-SPINE3 (IP: 1.1.1.203) | PASS | - |
| 503 | A-LEAF8 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s). | BGP EVPN Peer: A-SPINE4 (IP: 1.1.1.204) | PASS | - |
| 504 | A-LEAF8 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s). | BGP IPv4 Unicast Peer: 172.16.1.2 | PASS | - |
| 505 | A-LEAF8 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s). | BGP IPv4 Unicast Peer: 172.16.1.6 | PASS | - |
| 506 | A-LEAF8 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s). | BGP IPv4 Unicast Peer: A-LEAF7 (IP: 192.0.0.0) | PASS | - |
| 507 | A-LEAF8 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s). | BGP IPv4 Unicast Peer: A-SPINE1 (IP: 192.168.0.56) | PASS | - |
| 508 | A-LEAF8 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s). | BGP IPv4 Unicast Peer: A-SPINE2 (IP: 192.168.0.58) | PASS | - |
| 509 | A-LEAF8 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s). | BGP IPv4 Unicast Peer: A-SPINE3 (IP: 192.168.0.60) | PASS | - |
| 510 | A-LEAF8 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s). | BGP IPv4 Unicast Peer: A-SPINE4 (IP: 192.168.0.62) | PASS | - |
| 511 | A-LEAF8 | Connectivity | VerifyLLDPNeighbors | Verifies that the provided LLDP neighbors are connected properly. | Local: Ethernet1 - Remote: A-SPINE1 Ethernet8 | PASS | - |
| 512 | A-LEAF8 | Connectivity | VerifyLLDPNeighbors | Verifies that the provided LLDP neighbors are connected properly. | Local: Ethernet2 - Remote: A-SPINE2 Ethernet8 | PASS | - |
| 513 | A-LEAF8 | Connectivity | VerifyLLDPNeighbors | Verifies that the provided LLDP neighbors are connected properly. | Local: Ethernet3 - Remote: A-SPINE3 Ethernet8 | PASS | - |
| 514 | A-LEAF8 | Connectivity | VerifyLLDPNeighbors | Verifies that the provided LLDP neighbors are connected properly. | Local: Ethernet4 - Remote: A-SPINE4 Ethernet8 | PASS | - |
| 515 | A-LEAF8 | Connectivity | VerifyLLDPNeighbors | Verifies that the provided LLDP neighbors are connected properly. | Local: Ethernet5 - Remote: A-LEAF7 Ethernet5 | PASS | - |
| 516 | A-LEAF8 | Connectivity | VerifyLLDPNeighbors | Verifies that the provided LLDP neighbors are connected properly. | Local: Ethernet6 - Remote: A-LEAF7 Ethernet6 | PASS | - |
| 517 | A-LEAF8 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: Loopback0 (IP: 1.1.1.8) - Destination: A-LEAF1 Loopback0 (IP: 1.1.1.1) | PASS | - |
| 518 | A-LEAF8 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: Loopback0 (IP: 1.1.1.8) - Destination: A-LEAF2 Loopback0 (IP: 1.1.1.2) | PASS | - |
| 519 | A-LEAF8 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: Loopback0 (IP: 1.1.1.8) - Destination: A-LEAF3 Loopback0 (IP: 1.1.1.3) | PASS | - |
| 520 | A-LEAF8 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: Loopback0 (IP: 1.1.1.8) - Destination: A-LEAF4 Loopback0 (IP: 1.1.1.4) | PASS | - |
| 521 | A-LEAF8 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: Loopback0 (IP: 1.1.1.8) - Destination: A-LEAF5 Loopback0 (IP: 1.1.1.5) | PASS | - |
| 522 | A-LEAF8 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: Loopback0 (IP: 1.1.1.8) - Destination: A-LEAF6 Loopback0 (IP: 1.1.1.6) | PASS | - |
| 523 | A-LEAF8 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: Loopback0 (IP: 1.1.1.8) - Destination: A-LEAF7 Loopback0 (IP: 1.1.1.7) | PASS | - |
| 524 | A-LEAF8 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: Loopback0 (IP: 1.1.1.8) - Destination: A-LEAF8 Loopback0 (IP: 1.1.1.8) | PASS | - |
| 525 | A-LEAF8 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: Loopback0 (IP: 1.1.1.8) - Destination: A-SPINE1 Loopback0 (IP: 1.1.1.201) | PASS | - |
| 526 | A-LEAF8 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: Loopback0 (IP: 1.1.1.8) - Destination: A-SPINE2 Loopback0 (IP: 1.1.1.202) | PASS | - |
| 527 | A-LEAF8 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: Loopback0 (IP: 1.1.1.8) - Destination: A-SPINE3 Loopback0 (IP: 1.1.1.203) | PASS | - |
| 528 | A-LEAF8 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: Loopback0 (IP: 1.1.1.8) - Destination: A-SPINE4 Loopback0 (IP: 1.1.1.204) | PASS | - |
| 529 | A-LEAF8 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: P2P Interface Ethernet1 (IP: 192.168.0.57) - Destination: A-SPINE1 Ethernet8 (IP: 192.168.0.56) | PASS | - |
| 530 | A-LEAF8 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: P2P Interface Ethernet2 (IP: 192.168.0.59) - Destination: A-SPINE2 Ethernet8 (IP: 192.168.0.58) | PASS | - |
| 531 | A-LEAF8 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: P2P Interface Ethernet3 (IP: 192.168.0.61) - Destination: A-SPINE3 Ethernet8 (IP: 192.168.0.60) | PASS | - |
| 532 | A-LEAF8 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: P2P Interface Ethernet4 (IP: 192.168.0.63) - Destination: A-SPINE4 Ethernet8 (IP: 192.168.0.62) | PASS | - |
| 533 | A-LEAF8 | Hardware | VerifyEnvironmentCooling | Verifies the status of power supply fans and all fan trays. | Accepted States: 'ok' | SKIPPED | VerifyEnvironmentCooling test is not supported on cEOSLab. |
| 534 | A-LEAF8 | Hardware | VerifyEnvironmentPower | Verifies the power supplies status. | Accepted States: 'ok' | SKIPPED | VerifyEnvironmentPower test is not supported on cEOSLab. |
| 535 | A-LEAF8 | Hardware | VerifyTemperature | Verifies the device temperature. | - | SKIPPED | VerifyTemperature test is not supported on cEOSLab. |
| 536 | A-LEAF8 | Hardware | VerifyTransceiversManufacturers | Verifies if all transceivers come from approved manufacturers. | Accepted Manufacturers: 'Arista Networks', 'Arastra, Inc.', 'Not Present' | SKIPPED | VerifyTransceiversManufacturers test is not supported on cEOSLab. |
| 537 | A-LEAF8 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Ethernet1 - P2P_A-SPINE1_Ethernet8 = 'up' | PASS | - |
| 538 | A-LEAF8 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Ethernet2 - P2P_A-SPINE2_Ethernet8 = 'up' | PASS | - |
| 539 | A-LEAF8 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Ethernet3 - P2P_A-SPINE3_Ethernet8 = 'up' | PASS | - |
| 540 | A-LEAF8 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Ethernet4 - P2P_A-SPINE4_Ethernet8 = 'up' | PASS | - |
| 541 | A-LEAF8 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Ethernet5 - MLAG_A-LEAF7_Ethernet5 = 'up' | PASS | - |
| 542 | A-LEAF8 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Ethernet6 - MLAG_A-LEAF7_Ethernet6 = 'up' | PASS | - |
| 543 | A-LEAF8 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Ethernet7 - P2P_BB1_Ethernet1 = 'up' | PASS | - |
| 544 | A-LEAF8 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Ethernet8 - P2P_BB2_Ethernet1 = 'up' | PASS | - |
| 545 | A-LEAF8 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Loopback0 - Globally Unique Address = 'up' | PASS | - |
| 546 | A-LEAF8 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Loopback1 - VTEP IP = 'up' | PASS | - |
| 547 | A-LEAF8 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Loopback101 - Per-VRF Unique Loopback = 'up' | PASS | - |
| 548 | A-LEAF8 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Loopback102 - Per-VRF Unique Loopback = 'up' | PASS | - |
| 549 | A-LEAF8 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Port-Channel1000 - MLAG_A-LEAF7_Port-Channel1000 = 'up' | PASS | - |
| 550 | A-LEAF8 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Vlan10 - Blue Network = 'up' | PASS | - |
| 551 | A-LEAF8 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Vlan30 - Orange Network = 'up' | PASS | - |
| 552 | A-LEAF8 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Vlan3001 - MLAG_L3_VRF_PROD = 'up' | PASS | - |
| 553 | A-LEAF8 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Vlan3002 - MLAG_L3_VRF_DEV = 'up' | PASS | - |
| 554 | A-LEAF8 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Vlan4093 - MLAG_L3 = 'up' | PASS | - |
| 555 | A-LEAF8 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Vlan4094 - MLAG = 'up' | PASS | - |
| 556 | A-LEAF8 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Vlan50 - Yellow Network = 'up' | PASS | - |
| 557 | A-LEAF8 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Vlan70 - Brown Network = 'up' | PASS | - |
| 558 | A-LEAF8 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Vxlan1 = 'up' | PASS | - |
| 559 | A-LEAF8 | MLAG | VerifyMlagStatus | Verifies the health status of the MLAG configuration. | - | PASS | - |
| 560 | A-LEAF8 | Routing | VerifyRoutingProtocolModel | Verifies the configured routing protocol model. | Routing protocol model: multi-agent | PASS | - |
| 561 | A-LEAF8 | Routing | VerifyRoutingTableEntry | Verifies that the provided routes are present in the routing table of a specified VRF. | Route: 1.1.1.1 - Peer: A-LEAF1 | PASS | - |
| 562 | A-LEAF8 | Routing | VerifyRoutingTableEntry | Verifies that the provided routes are present in the routing table of a specified VRF. | Route: 1.1.1.2 - Peer: A-LEAF2 | PASS | - |
| 563 | A-LEAF8 | Routing | VerifyRoutingTableEntry | Verifies that the provided routes are present in the routing table of a specified VRF. | Route: 1.1.1.201 - Peer: A-SPINE1 | PASS | - |
| 564 | A-LEAF8 | Routing | VerifyRoutingTableEntry | Verifies that the provided routes are present in the routing table of a specified VRF. | Route: 1.1.1.202 - Peer: A-SPINE2 | PASS | - |
| 565 | A-LEAF8 | Routing | VerifyRoutingTableEntry | Verifies that the provided routes are present in the routing table of a specified VRF. | Route: 1.1.1.203 - Peer: A-SPINE3 | PASS | - |
| 566 | A-LEAF8 | Routing | VerifyRoutingTableEntry | Verifies that the provided routes are present in the routing table of a specified VRF. | Route: 1.1.1.204 - Peer: A-SPINE4 | PASS | - |
| 567 | A-LEAF8 | Routing | VerifyRoutingTableEntry | Verifies that the provided routes are present in the routing table of a specified VRF. | Route: 1.1.1.3 - Peer: A-LEAF3 | PASS | - |
| 568 | A-LEAF8 | Routing | VerifyRoutingTableEntry | Verifies that the provided routes are present in the routing table of a specified VRF. | Route: 1.1.1.4 - Peer: A-LEAF4 | PASS | - |
| 569 | A-LEAF8 | Routing | VerifyRoutingTableEntry | Verifies that the provided routes are present in the routing table of a specified VRF. | Route: 1.1.1.5 - Peer: A-LEAF5 | PASS | - |
| 570 | A-LEAF8 | Routing | VerifyRoutingTableEntry | Verifies that the provided routes are present in the routing table of a specified VRF. | Route: 1.1.1.6 - Peer: A-LEAF6 | PASS | - |
| 571 | A-LEAF8 | Routing | VerifyRoutingTableEntry | Verifies that the provided routes are present in the routing table of a specified VRF. | Route: 1.1.1.7 - Peer: A-LEAF7 | PASS | - |
| 572 | A-LEAF8 | Routing | VerifyRoutingTableEntry | Verifies that the provided routes are present in the routing table of a specified VRF. | Route: 1.1.1.8 - Peer: A-LEAF8 | PASS | - |
| 573 | A-LEAF8 | System | VerifyNTP | Verifies if NTP is synchronised. | - | PASS | - |
| 574 | A-LEAF8 | System | VerifyReloadCause | Verifies the last reload cause of the device. | - | PASS | - |
| 575 | A-SPINE1 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s). | BGP EVPN Peer: A-LEAF1 (IP: 1.1.1.1) | PASS | - |
| 576 | A-SPINE1 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s). | BGP EVPN Peer: A-LEAF2 (IP: 1.1.1.2) | PASS | - |
| 577 | A-SPINE1 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s). | BGP EVPN Peer: A-LEAF3 (IP: 1.1.1.3) | PASS | - |
| 578 | A-SPINE1 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s). | BGP EVPN Peer: A-LEAF4 (IP: 1.1.1.4) | PASS | - |
| 579 | A-SPINE1 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s). | BGP EVPN Peer: A-LEAF5 (IP: 1.1.1.5) | PASS | - |
| 580 | A-SPINE1 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s). | BGP EVPN Peer: A-LEAF6 (IP: 1.1.1.6) | PASS | - |
| 581 | A-SPINE1 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s). | BGP EVPN Peer: A-LEAF7 (IP: 1.1.1.7) | PASS | - |
| 582 | A-SPINE1 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s). | BGP EVPN Peer: A-LEAF8 (IP: 1.1.1.8) | PASS | - |
| 583 | A-SPINE1 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s). | BGP IPv4 Unicast Peer: A-LEAF1 (IP: 192.168.0.1) | PASS | - |
| 584 | A-SPINE1 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s). | BGP IPv4 Unicast Peer: A-LEAF2 (IP: 192.168.0.9) | PASS | - |
| 585 | A-SPINE1 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s). | BGP IPv4 Unicast Peer: A-LEAF3 (IP: 192.168.0.17) | PASS | - |
| 586 | A-SPINE1 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s). | BGP IPv4 Unicast Peer: A-LEAF4 (IP: 192.168.0.25) | PASS | - |
| 587 | A-SPINE1 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s). | BGP IPv4 Unicast Peer: A-LEAF5 (IP: 192.168.0.33) | PASS | - |
| 588 | A-SPINE1 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s). | BGP IPv4 Unicast Peer: A-LEAF6 (IP: 192.168.0.41) | PASS | - |
| 589 | A-SPINE1 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s). | BGP IPv4 Unicast Peer: A-LEAF7 (IP: 192.168.0.49) | PASS | - |
| 590 | A-SPINE1 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s). | BGP IPv4 Unicast Peer: A-LEAF8 (IP: 192.168.0.57) | PASS | - |
| 591 | A-SPINE1 | Connectivity | VerifyLLDPNeighbors | Verifies that the provided LLDP neighbors are connected properly. | Local: Ethernet1 - Remote: A-LEAF1 Ethernet1 | PASS | - |
| 592 | A-SPINE1 | Connectivity | VerifyLLDPNeighbors | Verifies that the provided LLDP neighbors are connected properly. | Local: Ethernet2 - Remote: A-LEAF2 Ethernet1 | PASS | - |
| 593 | A-SPINE1 | Connectivity | VerifyLLDPNeighbors | Verifies that the provided LLDP neighbors are connected properly. | Local: Ethernet3 - Remote: A-LEAF3 Ethernet1 | PASS | - |
| 594 | A-SPINE1 | Connectivity | VerifyLLDPNeighbors | Verifies that the provided LLDP neighbors are connected properly. | Local: Ethernet4 - Remote: A-LEAF4 Ethernet1 | PASS | - |
| 595 | A-SPINE1 | Connectivity | VerifyLLDPNeighbors | Verifies that the provided LLDP neighbors are connected properly. | Local: Ethernet5 - Remote: A-LEAF5 Ethernet1 | PASS | - |
| 596 | A-SPINE1 | Connectivity | VerifyLLDPNeighbors | Verifies that the provided LLDP neighbors are connected properly. | Local: Ethernet6 - Remote: A-LEAF6 Ethernet1 | PASS | - |
| 597 | A-SPINE1 | Connectivity | VerifyLLDPNeighbors | Verifies that the provided LLDP neighbors are connected properly. | Local: Ethernet7 - Remote: A-LEAF7 Ethernet1 | PASS | - |
| 598 | A-SPINE1 | Connectivity | VerifyLLDPNeighbors | Verifies that the provided LLDP neighbors are connected properly. | Local: Ethernet8 - Remote: A-LEAF8 Ethernet1 | PASS | - |
| 599 | A-SPINE1 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: P2P Interface Ethernet1 (IP: 192.168.0.0) - Destination: A-LEAF1 Ethernet1 (IP: 192.168.0.1) | PASS | - |
| 600 | A-SPINE1 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: P2P Interface Ethernet2 (IP: 192.168.0.8) - Destination: A-LEAF2 Ethernet1 (IP: 192.168.0.9) | PASS | - |
| 601 | A-SPINE1 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: P2P Interface Ethernet3 (IP: 192.168.0.16) - Destination: A-LEAF3 Ethernet1 (IP: 192.168.0.17) | PASS | - |
| 602 | A-SPINE1 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: P2P Interface Ethernet4 (IP: 192.168.0.24) - Destination: A-LEAF4 Ethernet1 (IP: 192.168.0.25) | PASS | - |
| 603 | A-SPINE1 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: P2P Interface Ethernet5 (IP: 192.168.0.32) - Destination: A-LEAF5 Ethernet1 (IP: 192.168.0.33) | PASS | - |
| 604 | A-SPINE1 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: P2P Interface Ethernet6 (IP: 192.168.0.40) - Destination: A-LEAF6 Ethernet1 (IP: 192.168.0.41) | PASS | - |
| 605 | A-SPINE1 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: P2P Interface Ethernet7 (IP: 192.168.0.48) - Destination: A-LEAF7 Ethernet1 (IP: 192.168.0.49) | PASS | - |
| 606 | A-SPINE1 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: P2P Interface Ethernet8 (IP: 192.168.0.56) - Destination: A-LEAF8 Ethernet1 (IP: 192.168.0.57) | PASS | - |
| 607 | A-SPINE1 | Hardware | VerifyEnvironmentCooling | Verifies the status of power supply fans and all fan trays. | Accepted States: 'ok' | SKIPPED | VerifyEnvironmentCooling test is not supported on cEOSLab. |
| 608 | A-SPINE1 | Hardware | VerifyEnvironmentPower | Verifies the power supplies status. | Accepted States: 'ok' | SKIPPED | VerifyEnvironmentPower test is not supported on cEOSLab. |
| 609 | A-SPINE1 | Hardware | VerifyTemperature | Verifies the device temperature. | - | SKIPPED | VerifyTemperature test is not supported on cEOSLab. |
| 610 | A-SPINE1 | Hardware | VerifyTransceiversManufacturers | Verifies if all transceivers come from approved manufacturers. | Accepted Manufacturers: 'Arista Networks', 'Arastra, Inc.', 'Not Present' | SKIPPED | VerifyTransceiversManufacturers test is not supported on cEOSLab. |
| 611 | A-SPINE1 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Ethernet1 - P2P_A-LEAF1_Ethernet1 = 'up' | PASS | - |
| 612 | A-SPINE1 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Ethernet2 - P2P_A-LEAF2_Ethernet1 = 'up' | PASS | - |
| 613 | A-SPINE1 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Ethernet3 - P2P_A-LEAF3_Ethernet1 = 'up' | PASS | - |
| 614 | A-SPINE1 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Ethernet4 - P2P_A-LEAF4_Ethernet1 = 'up' | PASS | - |
| 615 | A-SPINE1 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Ethernet5 - P2P_A-LEAF5_Ethernet1 = 'up' | PASS | - |
| 616 | A-SPINE1 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Ethernet6 - P2P_A-LEAF6_Ethernet1 = 'up' | PASS | - |
| 617 | A-SPINE1 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Ethernet7 - P2P_A-LEAF7_Ethernet1 = 'up' | PASS | - |
| 618 | A-SPINE1 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Ethernet8 - P2P_A-LEAF8_Ethernet1 = 'up' | PASS | - |
| 619 | A-SPINE1 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Loopback0 - Globally Unique Address = 'up' | PASS | - |
| 620 | A-SPINE1 | Routing | VerifyRoutingProtocolModel | Verifies the configured routing protocol model. | Routing protocol model: multi-agent | PASS | - |
| 621 | A-SPINE1 | System | VerifyNTP | Verifies if NTP is synchronised. | - | PASS | - |
| 622 | A-SPINE1 | System | VerifyReloadCause | Verifies the last reload cause of the device. | - | PASS | - |
| 623 | A-SPINE2 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s). | BGP EVPN Peer: A-LEAF1 (IP: 1.1.1.1) | PASS | - |
| 624 | A-SPINE2 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s). | BGP EVPN Peer: A-LEAF2 (IP: 1.1.1.2) | PASS | - |
| 625 | A-SPINE2 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s). | BGP EVPN Peer: A-LEAF3 (IP: 1.1.1.3) | PASS | - |
| 626 | A-SPINE2 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s). | BGP EVPN Peer: A-LEAF4 (IP: 1.1.1.4) | PASS | - |
| 627 | A-SPINE2 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s). | BGP EVPN Peer: A-LEAF5 (IP: 1.1.1.5) | PASS | - |
| 628 | A-SPINE2 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s). | BGP EVPN Peer: A-LEAF6 (IP: 1.1.1.6) | PASS | - |
| 629 | A-SPINE2 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s). | BGP EVPN Peer: A-LEAF7 (IP: 1.1.1.7) | PASS | - |
| 630 | A-SPINE2 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s). | BGP EVPN Peer: A-LEAF8 (IP: 1.1.1.8) | PASS | - |
| 631 | A-SPINE2 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s). | BGP IPv4 Unicast Peer: A-LEAF1 (IP: 192.168.0.3) | PASS | - |
| 632 | A-SPINE2 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s). | BGP IPv4 Unicast Peer: A-LEAF2 (IP: 192.168.0.11) | PASS | - |
| 633 | A-SPINE2 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s). | BGP IPv4 Unicast Peer: A-LEAF3 (IP: 192.168.0.19) | PASS | - |
| 634 | A-SPINE2 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s). | BGP IPv4 Unicast Peer: A-LEAF4 (IP: 192.168.0.27) | PASS | - |
| 635 | A-SPINE2 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s). | BGP IPv4 Unicast Peer: A-LEAF5 (IP: 192.168.0.35) | PASS | - |
| 636 | A-SPINE2 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s). | BGP IPv4 Unicast Peer: A-LEAF6 (IP: 192.168.0.43) | PASS | - |
| 637 | A-SPINE2 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s). | BGP IPv4 Unicast Peer: A-LEAF7 (IP: 192.168.0.51) | PASS | - |
| 638 | A-SPINE2 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s). | BGP IPv4 Unicast Peer: A-LEAF8 (IP: 192.168.0.59) | PASS | - |
| 639 | A-SPINE2 | Connectivity | VerifyLLDPNeighbors | Verifies that the provided LLDP neighbors are connected properly. | Local: Ethernet1 - Remote: A-LEAF1 Ethernet2 | PASS | - |
| 640 | A-SPINE2 | Connectivity | VerifyLLDPNeighbors | Verifies that the provided LLDP neighbors are connected properly. | Local: Ethernet2 - Remote: A-LEAF2 Ethernet2 | PASS | - |
| 641 | A-SPINE2 | Connectivity | VerifyLLDPNeighbors | Verifies that the provided LLDP neighbors are connected properly. | Local: Ethernet3 - Remote: A-LEAF3 Ethernet2 | PASS | - |
| 642 | A-SPINE2 | Connectivity | VerifyLLDPNeighbors | Verifies that the provided LLDP neighbors are connected properly. | Local: Ethernet4 - Remote: A-LEAF4 Ethernet2 | PASS | - |
| 643 | A-SPINE2 | Connectivity | VerifyLLDPNeighbors | Verifies that the provided LLDP neighbors are connected properly. | Local: Ethernet5 - Remote: A-LEAF5 Ethernet2 | PASS | - |
| 644 | A-SPINE2 | Connectivity | VerifyLLDPNeighbors | Verifies that the provided LLDP neighbors are connected properly. | Local: Ethernet6 - Remote: A-LEAF6 Ethernet2 | PASS | - |
| 645 | A-SPINE2 | Connectivity | VerifyLLDPNeighbors | Verifies that the provided LLDP neighbors are connected properly. | Local: Ethernet7 - Remote: A-LEAF7 Ethernet2 | PASS | - |
| 646 | A-SPINE2 | Connectivity | VerifyLLDPNeighbors | Verifies that the provided LLDP neighbors are connected properly. | Local: Ethernet8 - Remote: A-LEAF8 Ethernet2 | PASS | - |
| 647 | A-SPINE2 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: P2P Interface Ethernet1 (IP: 192.168.0.2) - Destination: A-LEAF1 Ethernet2 (IP: 192.168.0.3) | PASS | - |
| 648 | A-SPINE2 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: P2P Interface Ethernet2 (IP: 192.168.0.10) - Destination: A-LEAF2 Ethernet2 (IP: 192.168.0.11) | PASS | - |
| 649 | A-SPINE2 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: P2P Interface Ethernet3 (IP: 192.168.0.18) - Destination: A-LEAF3 Ethernet2 (IP: 192.168.0.19) | PASS | - |
| 650 | A-SPINE2 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: P2P Interface Ethernet4 (IP: 192.168.0.26) - Destination: A-LEAF4 Ethernet2 (IP: 192.168.0.27) | PASS | - |
| 651 | A-SPINE2 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: P2P Interface Ethernet5 (IP: 192.168.0.34) - Destination: A-LEAF5 Ethernet2 (IP: 192.168.0.35) | PASS | - |
| 652 | A-SPINE2 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: P2P Interface Ethernet6 (IP: 192.168.0.42) - Destination: A-LEAF6 Ethernet2 (IP: 192.168.0.43) | PASS | - |
| 653 | A-SPINE2 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: P2P Interface Ethernet7 (IP: 192.168.0.50) - Destination: A-LEAF7 Ethernet2 (IP: 192.168.0.51) | PASS | - |
| 654 | A-SPINE2 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: P2P Interface Ethernet8 (IP: 192.168.0.58) - Destination: A-LEAF8 Ethernet2 (IP: 192.168.0.59) | PASS | - |
| 655 | A-SPINE2 | Hardware | VerifyEnvironmentCooling | Verifies the status of power supply fans and all fan trays. | Accepted States: 'ok' | SKIPPED | VerifyEnvironmentCooling test is not supported on cEOSLab. |
| 656 | A-SPINE2 | Hardware | VerifyEnvironmentPower | Verifies the power supplies status. | Accepted States: 'ok' | SKIPPED | VerifyEnvironmentPower test is not supported on cEOSLab. |
| 657 | A-SPINE2 | Hardware | VerifyTemperature | Verifies the device temperature. | - | SKIPPED | VerifyTemperature test is not supported on cEOSLab. |
| 658 | A-SPINE2 | Hardware | VerifyTransceiversManufacturers | Verifies if all transceivers come from approved manufacturers. | Accepted Manufacturers: 'Arista Networks', 'Arastra, Inc.', 'Not Present' | SKIPPED | VerifyTransceiversManufacturers test is not supported on cEOSLab. |
| 659 | A-SPINE2 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Ethernet1 - P2P_A-LEAF1_Ethernet2 = 'up' | PASS | - |
| 660 | A-SPINE2 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Ethernet2 - P2P_A-LEAF2_Ethernet2 = 'up' | PASS | - |
| 661 | A-SPINE2 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Ethernet3 - P2P_A-LEAF3_Ethernet2 = 'up' | PASS | - |
| 662 | A-SPINE2 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Ethernet4 - P2P_A-LEAF4_Ethernet2 = 'up' | PASS | - |
| 663 | A-SPINE2 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Ethernet5 - P2P_A-LEAF5_Ethernet2 = 'up' | PASS | - |
| 664 | A-SPINE2 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Ethernet6 - P2P_A-LEAF6_Ethernet2 = 'up' | PASS | - |
| 665 | A-SPINE2 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Ethernet7 - P2P_A-LEAF7_Ethernet2 = 'up' | PASS | - |
| 666 | A-SPINE2 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Ethernet8 - P2P_A-LEAF8_Ethernet2 = 'up' | PASS | - |
| 667 | A-SPINE2 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Loopback0 - Globally Unique Address = 'up' | PASS | - |
| 668 | A-SPINE2 | Routing | VerifyRoutingProtocolModel | Verifies the configured routing protocol model. | Routing protocol model: multi-agent | PASS | - |
| 669 | A-SPINE2 | System | VerifyNTP | Verifies if NTP is synchronised. | - | PASS | - |
| 670 | A-SPINE2 | System | VerifyReloadCause | Verifies the last reload cause of the device. | - | PASS | - |
| 671 | A-SPINE3 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s). | BGP EVPN Peer: A-LEAF1 (IP: 1.1.1.1) | PASS | - |
| 672 | A-SPINE3 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s). | BGP EVPN Peer: A-LEAF2 (IP: 1.1.1.2) | PASS | - |
| 673 | A-SPINE3 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s). | BGP EVPN Peer: A-LEAF3 (IP: 1.1.1.3) | PASS | - |
| 674 | A-SPINE3 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s). | BGP EVPN Peer: A-LEAF4 (IP: 1.1.1.4) | PASS | - |
| 675 | A-SPINE3 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s). | BGP EVPN Peer: A-LEAF5 (IP: 1.1.1.5) | PASS | - |
| 676 | A-SPINE3 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s). | BGP EVPN Peer: A-LEAF6 (IP: 1.1.1.6) | PASS | - |
| 677 | A-SPINE3 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s). | BGP EVPN Peer: A-LEAF7 (IP: 1.1.1.7) | PASS | - |
| 678 | A-SPINE3 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s). | BGP EVPN Peer: A-LEAF8 (IP: 1.1.1.8) | PASS | - |
| 679 | A-SPINE3 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s). | BGP IPv4 Unicast Peer: A-LEAF1 (IP: 192.168.0.5) | PASS | - |
| 680 | A-SPINE3 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s). | BGP IPv4 Unicast Peer: A-LEAF2 (IP: 192.168.0.13) | PASS | - |
| 681 | A-SPINE3 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s). | BGP IPv4 Unicast Peer: A-LEAF3 (IP: 192.168.0.21) | PASS | - |
| 682 | A-SPINE3 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s). | BGP IPv4 Unicast Peer: A-LEAF4 (IP: 192.168.0.29) | PASS | - |
| 683 | A-SPINE3 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s). | BGP IPv4 Unicast Peer: A-LEAF5 (IP: 192.168.0.37) | PASS | - |
| 684 | A-SPINE3 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s). | BGP IPv4 Unicast Peer: A-LEAF6 (IP: 192.168.0.45) | PASS | - |
| 685 | A-SPINE3 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s). | BGP IPv4 Unicast Peer: A-LEAF7 (IP: 192.168.0.53) | PASS | - |
| 686 | A-SPINE3 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s). | BGP IPv4 Unicast Peer: A-LEAF8 (IP: 192.168.0.61) | PASS | - |
| 687 | A-SPINE3 | Connectivity | VerifyLLDPNeighbors | Verifies that the provided LLDP neighbors are connected properly. | Local: Ethernet1 - Remote: A-LEAF1 Ethernet3 | PASS | - |
| 688 | A-SPINE3 | Connectivity | VerifyLLDPNeighbors | Verifies that the provided LLDP neighbors are connected properly. | Local: Ethernet2 - Remote: A-LEAF2 Ethernet3 | PASS | - |
| 689 | A-SPINE3 | Connectivity | VerifyLLDPNeighbors | Verifies that the provided LLDP neighbors are connected properly. | Local: Ethernet3 - Remote: A-LEAF3 Ethernet3 | PASS | - |
| 690 | A-SPINE3 | Connectivity | VerifyLLDPNeighbors | Verifies that the provided LLDP neighbors are connected properly. | Local: Ethernet4 - Remote: A-LEAF4 Ethernet3 | PASS | - |
| 691 | A-SPINE3 | Connectivity | VerifyLLDPNeighbors | Verifies that the provided LLDP neighbors are connected properly. | Local: Ethernet5 - Remote: A-LEAF5 Ethernet3 | PASS | - |
| 692 | A-SPINE3 | Connectivity | VerifyLLDPNeighbors | Verifies that the provided LLDP neighbors are connected properly. | Local: Ethernet6 - Remote: A-LEAF6 Ethernet3 | PASS | - |
| 693 | A-SPINE3 | Connectivity | VerifyLLDPNeighbors | Verifies that the provided LLDP neighbors are connected properly. | Local: Ethernet7 - Remote: A-LEAF7 Ethernet3 | PASS | - |
| 694 | A-SPINE3 | Connectivity | VerifyLLDPNeighbors | Verifies that the provided LLDP neighbors are connected properly. | Local: Ethernet8 - Remote: A-LEAF8 Ethernet3 | PASS | - |
| 695 | A-SPINE3 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: P2P Interface Ethernet1 (IP: 192.168.0.4) - Destination: A-LEAF1 Ethernet3 (IP: 192.168.0.5) | PASS | - |
| 696 | A-SPINE3 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: P2P Interface Ethernet2 (IP: 192.168.0.12) - Destination: A-LEAF2 Ethernet3 (IP: 192.168.0.13) | PASS | - |
| 697 | A-SPINE3 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: P2P Interface Ethernet3 (IP: 192.168.0.20) - Destination: A-LEAF3 Ethernet3 (IP: 192.168.0.21) | PASS | - |
| 698 | A-SPINE3 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: P2P Interface Ethernet4 (IP: 192.168.0.28) - Destination: A-LEAF4 Ethernet3 (IP: 192.168.0.29) | PASS | - |
| 699 | A-SPINE3 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: P2P Interface Ethernet5 (IP: 192.168.0.36) - Destination: A-LEAF5 Ethernet3 (IP: 192.168.0.37) | PASS | - |
| 700 | A-SPINE3 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: P2P Interface Ethernet6 (IP: 192.168.0.44) - Destination: A-LEAF6 Ethernet3 (IP: 192.168.0.45) | PASS | - |
| 701 | A-SPINE3 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: P2P Interface Ethernet7 (IP: 192.168.0.52) - Destination: A-LEAF7 Ethernet3 (IP: 192.168.0.53) | PASS | - |
| 702 | A-SPINE3 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: P2P Interface Ethernet8 (IP: 192.168.0.60) - Destination: A-LEAF8 Ethernet3 (IP: 192.168.0.61) | PASS | - |
| 703 | A-SPINE3 | Hardware | VerifyEnvironmentCooling | Verifies the status of power supply fans and all fan trays. | Accepted States: 'ok' | SKIPPED | VerifyEnvironmentCooling test is not supported on cEOSLab. |
| 704 | A-SPINE3 | Hardware | VerifyEnvironmentPower | Verifies the power supplies status. | Accepted States: 'ok' | SKIPPED | VerifyEnvironmentPower test is not supported on cEOSLab. |
| 705 | A-SPINE3 | Hardware | VerifyTemperature | Verifies the device temperature. | - | SKIPPED | VerifyTemperature test is not supported on cEOSLab. |
| 706 | A-SPINE3 | Hardware | VerifyTransceiversManufacturers | Verifies if all transceivers come from approved manufacturers. | Accepted Manufacturers: 'Arista Networks', 'Arastra, Inc.', 'Not Present' | SKIPPED | VerifyTransceiversManufacturers test is not supported on cEOSLab. |
| 707 | A-SPINE3 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Ethernet1 - P2P_A-LEAF1_Ethernet3 = 'up' | PASS | - |
| 708 | A-SPINE3 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Ethernet2 - P2P_A-LEAF2_Ethernet3 = 'up' | PASS | - |
| 709 | A-SPINE3 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Ethernet3 - P2P_A-LEAF3_Ethernet3 = 'up' | PASS | - |
| 710 | A-SPINE3 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Ethernet4 - P2P_A-LEAF4_Ethernet3 = 'up' | PASS | - |
| 711 | A-SPINE3 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Ethernet5 - P2P_A-LEAF5_Ethernet3 = 'up' | PASS | - |
| 712 | A-SPINE3 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Ethernet6 - P2P_A-LEAF6_Ethernet3 = 'up' | PASS | - |
| 713 | A-SPINE3 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Ethernet7 - P2P_A-LEAF7_Ethernet3 = 'up' | PASS | - |
| 714 | A-SPINE3 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Ethernet8 - P2P_A-LEAF8_Ethernet3 = 'up' | PASS | - |
| 715 | A-SPINE3 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Loopback0 - Globally Unique Address = 'up' | PASS | - |
| 716 | A-SPINE3 | Routing | VerifyRoutingProtocolModel | Verifies the configured routing protocol model. | Routing protocol model: multi-agent | PASS | - |
| 717 | A-SPINE3 | System | VerifyNTP | Verifies if NTP is synchronised. | - | PASS | - |
| 718 | A-SPINE3 | System | VerifyReloadCause | Verifies the last reload cause of the device. | - | PASS | - |
| 719 | A-SPINE4 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s). | BGP EVPN Peer: A-LEAF1 (IP: 1.1.1.1) | PASS | - |
| 720 | A-SPINE4 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s). | BGP EVPN Peer: A-LEAF2 (IP: 1.1.1.2) | PASS | - |
| 721 | A-SPINE4 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s). | BGP EVPN Peer: A-LEAF3 (IP: 1.1.1.3) | PASS | - |
| 722 | A-SPINE4 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s). | BGP EVPN Peer: A-LEAF4 (IP: 1.1.1.4) | PASS | - |
| 723 | A-SPINE4 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s). | BGP EVPN Peer: A-LEAF5 (IP: 1.1.1.5) | PASS | - |
| 724 | A-SPINE4 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s). | BGP EVPN Peer: A-LEAF6 (IP: 1.1.1.6) | PASS | - |
| 725 | A-SPINE4 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s). | BGP EVPN Peer: A-LEAF7 (IP: 1.1.1.7) | PASS | - |
| 726 | A-SPINE4 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s). | BGP EVPN Peer: A-LEAF8 (IP: 1.1.1.8) | PASS | - |
| 727 | A-SPINE4 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s). | BGP IPv4 Unicast Peer: A-LEAF1 (IP: 192.168.0.7) | PASS | - |
| 728 | A-SPINE4 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s). | BGP IPv4 Unicast Peer: A-LEAF2 (IP: 192.168.0.15) | PASS | - |
| 729 | A-SPINE4 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s). | BGP IPv4 Unicast Peer: A-LEAF3 (IP: 192.168.0.23) | PASS | - |
| 730 | A-SPINE4 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s). | BGP IPv4 Unicast Peer: A-LEAF4 (IP: 192.168.0.31) | PASS | - |
| 731 | A-SPINE4 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s). | BGP IPv4 Unicast Peer: A-LEAF5 (IP: 192.168.0.39) | PASS | - |
| 732 | A-SPINE4 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s). | BGP IPv4 Unicast Peer: A-LEAF6 (IP: 192.168.0.47) | PASS | - |
| 733 | A-SPINE4 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s). | BGP IPv4 Unicast Peer: A-LEAF7 (IP: 192.168.0.55) | PASS | - |
| 734 | A-SPINE4 | BGP | VerifyBGPSpecificPeers | Verifies the health of specific BGP peer(s). | BGP IPv4 Unicast Peer: A-LEAF8 (IP: 192.168.0.63) | PASS | - |
| 735 | A-SPINE4 | Connectivity | VerifyLLDPNeighbors | Verifies that the provided LLDP neighbors are connected properly. | Local: Ethernet1 - Remote: A-LEAF1 Ethernet4 | PASS | - |
| 736 | A-SPINE4 | Connectivity | VerifyLLDPNeighbors | Verifies that the provided LLDP neighbors are connected properly. | Local: Ethernet2 - Remote: A-LEAF2 Ethernet4 | PASS | - |
| 737 | A-SPINE4 | Connectivity | VerifyLLDPNeighbors | Verifies that the provided LLDP neighbors are connected properly. | Local: Ethernet3 - Remote: A-LEAF3 Ethernet4 | PASS | - |
| 738 | A-SPINE4 | Connectivity | VerifyLLDPNeighbors | Verifies that the provided LLDP neighbors are connected properly. | Local: Ethernet4 - Remote: A-LEAF4 Ethernet4 | PASS | - |
| 739 | A-SPINE4 | Connectivity | VerifyLLDPNeighbors | Verifies that the provided LLDP neighbors are connected properly. | Local: Ethernet5 - Remote: A-LEAF5 Ethernet4 | PASS | - |
| 740 | A-SPINE4 | Connectivity | VerifyLLDPNeighbors | Verifies that the provided LLDP neighbors are connected properly. | Local: Ethernet6 - Remote: A-LEAF6 Ethernet4 | PASS | - |
| 741 | A-SPINE4 | Connectivity | VerifyLLDPNeighbors | Verifies that the provided LLDP neighbors are connected properly. | Local: Ethernet7 - Remote: A-LEAF7 Ethernet4 | PASS | - |
| 742 | A-SPINE4 | Connectivity | VerifyLLDPNeighbors | Verifies that the provided LLDP neighbors are connected properly. | Local: Ethernet8 - Remote: A-LEAF8 Ethernet4 | PASS | - |
| 743 | A-SPINE4 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: P2P Interface Ethernet1 (IP: 192.168.0.6) - Destination: A-LEAF1 Ethernet4 (IP: 192.168.0.7) | PASS | - |
| 744 | A-SPINE4 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: P2P Interface Ethernet2 (IP: 192.168.0.14) - Destination: A-LEAF2 Ethernet4 (IP: 192.168.0.15) | PASS | - |
| 745 | A-SPINE4 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: P2P Interface Ethernet3 (IP: 192.168.0.22) - Destination: A-LEAF3 Ethernet4 (IP: 192.168.0.23) | PASS | - |
| 746 | A-SPINE4 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: P2P Interface Ethernet4 (IP: 192.168.0.30) - Destination: A-LEAF4 Ethernet4 (IP: 192.168.0.31) | PASS | - |
| 747 | A-SPINE4 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: P2P Interface Ethernet5 (IP: 192.168.0.38) - Destination: A-LEAF5 Ethernet4 (IP: 192.168.0.39) | PASS | - |
| 748 | A-SPINE4 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: P2P Interface Ethernet6 (IP: 192.168.0.46) - Destination: A-LEAF6 Ethernet4 (IP: 192.168.0.47) | PASS | - |
| 749 | A-SPINE4 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: P2P Interface Ethernet7 (IP: 192.168.0.54) - Destination: A-LEAF7 Ethernet4 (IP: 192.168.0.55) | PASS | - |
| 750 | A-SPINE4 | Connectivity | VerifyReachability | Test the network reachability to one or many destination IP(s). | Source: P2P Interface Ethernet8 (IP: 192.168.0.62) - Destination: A-LEAF8 Ethernet4 (IP: 192.168.0.63) | PASS | - |
| 751 | A-SPINE4 | Hardware | VerifyEnvironmentCooling | Verifies the status of power supply fans and all fan trays. | Accepted States: 'ok' | SKIPPED | VerifyEnvironmentCooling test is not supported on cEOSLab. |
| 752 | A-SPINE4 | Hardware | VerifyEnvironmentPower | Verifies the power supplies status. | Accepted States: 'ok' | SKIPPED | VerifyEnvironmentPower test is not supported on cEOSLab. |
| 753 | A-SPINE4 | Hardware | VerifyTemperature | Verifies the device temperature. | - | SKIPPED | VerifyTemperature test is not supported on cEOSLab. |
| 754 | A-SPINE4 | Hardware | VerifyTransceiversManufacturers | Verifies if all transceivers come from approved manufacturers. | Accepted Manufacturers: 'Arista Networks', 'Arastra, Inc.', 'Not Present' | SKIPPED | VerifyTransceiversManufacturers test is not supported on cEOSLab. |
| 755 | A-SPINE4 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Ethernet1 - P2P_A-LEAF1_Ethernet4 = 'up' | PASS | - |
| 756 | A-SPINE4 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Ethernet2 - P2P_A-LEAF2_Ethernet4 = 'up' | PASS | - |
| 757 | A-SPINE4 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Ethernet3 - P2P_A-LEAF3_Ethernet4 = 'up' | PASS | - |
| 758 | A-SPINE4 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Ethernet4 - P2P_A-LEAF4_Ethernet4 = 'up' | PASS | - |
| 759 | A-SPINE4 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Ethernet5 - P2P_A-LEAF5_Ethernet4 = 'up' | PASS | - |
| 760 | A-SPINE4 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Ethernet6 - P2P_A-LEAF6_Ethernet4 = 'up' | PASS | - |
| 761 | A-SPINE4 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Ethernet7 - P2P_A-LEAF7_Ethernet4 = 'up' | PASS | - |
| 762 | A-SPINE4 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Ethernet8 - P2P_A-LEAF8_Ethernet4 = 'up' | PASS | - |
| 763 | A-SPINE4 | Interfaces | VerifyInterfacesStatus | Verifies the status of the provided interfaces. | Interface Loopback0 - Globally Unique Address = 'up' | PASS | - |
| 764 | A-SPINE4 | Routing | VerifyRoutingProtocolModel | Verifies the configured routing protocol model. | Routing protocol model: multi-agent | PASS | - |
| 765 | A-SPINE4 | System | VerifyNTP | Verifies if NTP is synchronised. | - | PASS | - |
| 766 | A-SPINE4 | System | VerifyReloadCause | Verifies the last reload cause of the device. | - | PASS | - |
