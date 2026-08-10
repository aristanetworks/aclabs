# 📊 ANTA Report <a id="anta-report"></a>

**Table of Contents:**

- [ANTA Report](#anta-report)
  - [Test Results Summary](#test-results-summary)
    - [Summary Totals](#summary-totals)
    - [Summary Totals Device Under Test](#summary-totals-device-under-test)
    - [Summary Totals Per Category](#summary-totals-per-category)
  - [Test Results](#test-results)

## 📉 Test Results Summary <a id="test-results-summary"></a>

### 🔢 Summary Totals <a id="summary-totals"></a>

| Total Tests | ✅&nbsp;Success | ⏭️&nbsp;Skipped | ❌&nbsp;Failure | ❗&nbsp;Error |
| :- | :- | :- | :- | :- |
| 168 | 168 | 0 | 0 | 0 |

### 🔌 Summary Totals Device Under Test <a id="summary-totals-device-under-test"></a>

| Device | Total Tests | ✅&nbsp;Success | ⏭️&nbsp;Skipped | ❌&nbsp;Failure | ❗&nbsp;Error | Categories Skipped | Categories Failed |
| :- | :- | :- | :- | :- | :- | :- | :- |
| **campus-brdr1** | 20 | 20 | 0 | 0 | 0 | - | - |
| **campus-brdr2** | 20 | 20 | 0 | 0 | 0 | - | - |
| **campus-leaf1** | 20 | 20 | 0 | 0 | 0 | - | - |
| **campus-leaf2** | 20 | 20 | 0 | 0 | 0 | - | - |
| **campus-leaf3** | 20 | 20 | 0 | 0 | 0 | - | - |
| **campus-leaf4** | 20 | 20 | 0 | 0 | 0 | - | - |
| **campus-spine1** | 24 | 24 | 0 | 0 | 0 | - | - |
| **campus-spine2** | 24 | 24 | 0 | 0 | 0 | - | - |

### 🗂️ Summary Totals Per Category <a id="summary-totals-per-category"></a>

| Test Category | Total Tests | ✅&nbsp;Success | ⏭️&nbsp;Skipped | ❌&nbsp;Failure | ❗&nbsp;Error |
| :- | :- | :- | :- | :- | :- |
| **BGP** | 2 | 2 | 0 | 0 | 0 |
| **Configuration** | 16 | 16 | 0 | 0 | 0 |
| **Connectivity** | 10 | 10 | 0 | 0 | 0 |
| **Interfaces** | 48 | 48 | 0 | 0 | 0 |
| **MLAG** | 24 | 24 | 0 | 0 | 0 |
| **OSPF** | 4 | 4 | 0 | 0 | 0 |
| **Routing** | 8 | 8 | 0 | 0 | 0 |
| **STP** | 8 | 8 | 0 | 0 | 0 |
| **System** | 48 | 48 | 0 | 0 | 0 |

## 🧪 Test Results <a id="test-results"></a>

| Device | Categories | Test | Description | Result | Messages |
| :- | :- | :- | :- | :- | :- |
| campus-brdr1 | Configuration | VerifyRunningConfigDiffs | Verifies there is no difference between the running-config and the startup-config. | ✅&nbsp;Success | - |
| campus-brdr1 | Configuration | VerifyZeroTouch | Verifies ZeroTouch is disabled. | ✅&nbsp;Success | - |
| campus-brdr1 | Connectivity | VerifyLLDPNeighbors | Verifies the connection status of the specified LLDP (Link Layer Discovery Protocol) neighbors. | ✅&nbsp;Success | - |
| campus-brdr1 | Interfaces | VerifyIllegalLACP | Verifies there are no illegal LACP packets in port channels. | ✅&nbsp;Success | - |
| campus-brdr1 | Interfaces | VerifyInterfaceErrDisabled | Verifies there are no interfaces in the errdisabled state. | ✅&nbsp;Success | - |
| campus-brdr1 | Interfaces | VerifyInterfaceErrors | Verifies that the interfaces error counters are equal to zero. | ✅&nbsp;Success | - |
| campus-brdr1 | Interfaces | VerifyInterfaceUtilization | Verifies that the utilization of interfaces is below a certain threshold. | ✅&nbsp;Success | - |
| campus-brdr1 | Interfaces | VerifyInterfacesStatus | Verifies the operational states of specified interfaces to ensure they match expected configurations. | ✅&nbsp;Success | - |
| campus-brdr1 | Interfaces | VerifyPortChannels | Verifies there are no inactive ports in port channels. | ✅&nbsp;Success | - |
| campus-brdr1 | MLAG | VerifyMlagConfigSanity | Verifies there are no MLAG config-sanity inconsistencies. | ✅&nbsp;Success | - |
| campus-brdr1 | MLAG | VerifyMlagInterfaces | Verifies there are no inactive or active-partial MLAG ports. | ✅&nbsp;Success | - |
| campus-brdr1 | MLAG | VerifyMlagStatus | Verifies the health status of the MLAG configuration. | ✅&nbsp;Success | - |
| campus-brdr1 | Routing | VerifyRoutingProtocolModel | Verifies the configured routing protocol model. | ✅&nbsp;Success | - |
| campus-brdr1 | STP | VerifySTPCounters | Verifies there is no errors in STP BPDU packets. | ✅&nbsp;Success | - |
| campus-brdr1 | System | VerifyAgentLogs | Verifies there are no agent crash reports. | ✅&nbsp;Success | - |
| campus-brdr1 | System | VerifyCoredump | Verifies there are no core dump files. | ✅&nbsp;Success | - |
| campus-brdr1 | System | VerifyFileSystemUtilization | Verifies that no partition is utilizing more than 75% of its disk space. | ✅&nbsp;Success | - |
| campus-brdr1 | System | VerifyMaintenance | Verifies that the device is not currently under or entering maintenance. | ✅&nbsp;Success | - |
| campus-brdr1 | System | VerifyMemoryUtilization | Verifies whether the memory utilization is below 75%. | ✅&nbsp;Success | - |
| campus-brdr1 | System | VerifyReloadCause | Verifies the last reload cause of the device. | ✅&nbsp;Success | - |
| campus-brdr2 | Configuration | VerifyRunningConfigDiffs | Verifies there is no difference between the running-config and the startup-config. | ✅&nbsp;Success | - |
| campus-brdr2 | Configuration | VerifyZeroTouch | Verifies ZeroTouch is disabled. | ✅&nbsp;Success | - |
| campus-brdr2 | Connectivity | VerifyLLDPNeighbors | Verifies the connection status of the specified LLDP (Link Layer Discovery Protocol) neighbors. | ✅&nbsp;Success | - |
| campus-brdr2 | Interfaces | VerifyIllegalLACP | Verifies there are no illegal LACP packets in port channels. | ✅&nbsp;Success | - |
| campus-brdr2 | Interfaces | VerifyInterfaceErrDisabled | Verifies there are no interfaces in the errdisabled state. | ✅&nbsp;Success | - |
| campus-brdr2 | Interfaces | VerifyInterfaceErrors | Verifies that the interfaces error counters are equal to zero. | ✅&nbsp;Success | - |
| campus-brdr2 | Interfaces | VerifyInterfaceUtilization | Verifies that the utilization of interfaces is below a certain threshold. | ✅&nbsp;Success | - |
| campus-brdr2 | Interfaces | VerifyInterfacesStatus | Verifies the operational states of specified interfaces to ensure they match expected configurations. | ✅&nbsp;Success | - |
| campus-brdr2 | Interfaces | VerifyPortChannels | Verifies there are no inactive ports in port channels. | ✅&nbsp;Success | - |
| campus-brdr2 | MLAG | VerifyMlagConfigSanity | Verifies there are no MLAG config-sanity inconsistencies. | ✅&nbsp;Success | - |
| campus-brdr2 | MLAG | VerifyMlagInterfaces | Verifies there are no inactive or active-partial MLAG ports. | ✅&nbsp;Success | - |
| campus-brdr2 | MLAG | VerifyMlagStatus | Verifies the health status of the MLAG configuration. | ✅&nbsp;Success | - |
| campus-brdr2 | Routing | VerifyRoutingProtocolModel | Verifies the configured routing protocol model. | ✅&nbsp;Success | - |
| campus-brdr2 | STP | VerifySTPCounters | Verifies there is no errors in STP BPDU packets. | ✅&nbsp;Success | - |
| campus-brdr2 | System | VerifyAgentLogs | Verifies there are no agent crash reports. | ✅&nbsp;Success | - |
| campus-brdr2 | System | VerifyCoredump | Verifies there are no core dump files. | ✅&nbsp;Success | - |
| campus-brdr2 | System | VerifyFileSystemUtilization | Verifies that no partition is utilizing more than 75% of its disk space. | ✅&nbsp;Success | - |
| campus-brdr2 | System | VerifyMaintenance | Verifies that the device is not currently under or entering maintenance. | ✅&nbsp;Success | - |
| campus-brdr2 | System | VerifyMemoryUtilization | Verifies whether the memory utilization is below 75%. | ✅&nbsp;Success | - |
| campus-brdr2 | System | VerifyReloadCause | Verifies the last reload cause of the device. | ✅&nbsp;Success | - |
| campus-leaf1 | Configuration | VerifyRunningConfigDiffs | Verifies there is no difference between the running-config and the startup-config. | ✅&nbsp;Success | - |
| campus-leaf1 | Configuration | VerifyZeroTouch | Verifies ZeroTouch is disabled. | ✅&nbsp;Success | - |
| campus-leaf1 | Connectivity | VerifyLLDPNeighbors | Verifies the connection status of the specified LLDP (Link Layer Discovery Protocol) neighbors. | ✅&nbsp;Success | - |
| campus-leaf1 | Interfaces | VerifyIllegalLACP | Verifies there are no illegal LACP packets in port channels. | ✅&nbsp;Success | - |
| campus-leaf1 | Interfaces | VerifyInterfaceErrDisabled | Verifies there are no interfaces in the errdisabled state. | ✅&nbsp;Success | - |
| campus-leaf1 | Interfaces | VerifyInterfaceErrors | Verifies that the interfaces error counters are equal to zero. | ✅&nbsp;Success | - |
| campus-leaf1 | Interfaces | VerifyInterfaceUtilization | Verifies that the utilization of interfaces is below a certain threshold. | ✅&nbsp;Success | - |
| campus-leaf1 | Interfaces | VerifyInterfacesStatus | Verifies the operational states of specified interfaces to ensure they match expected configurations. | ✅&nbsp;Success | - |
| campus-leaf1 | Interfaces | VerifyPortChannels | Verifies there are no inactive ports in port channels. | ✅&nbsp;Success | - |
| campus-leaf1 | MLAG | VerifyMlagConfigSanity | Verifies there are no MLAG config-sanity inconsistencies. | ✅&nbsp;Success | - |
| campus-leaf1 | MLAG | VerifyMlagInterfaces | Verifies there are no inactive or active-partial MLAG ports. | ✅&nbsp;Success | - |
| campus-leaf1 | MLAG | VerifyMlagStatus | Verifies the health status of the MLAG configuration. | ✅&nbsp;Success | - |
| campus-leaf1 | Routing | VerifyRoutingProtocolModel | Verifies the configured routing protocol model. | ✅&nbsp;Success | - |
| campus-leaf1 | STP | VerifySTPCounters | Verifies there is no errors in STP BPDU packets. | ✅&nbsp;Success | - |
| campus-leaf1 | System | VerifyAgentLogs | Verifies there are no agent crash reports. | ✅&nbsp;Success | - |
| campus-leaf1 | System | VerifyCoredump | Verifies there are no core dump files. | ✅&nbsp;Success | - |
| campus-leaf1 | System | VerifyFileSystemUtilization | Verifies that no partition is utilizing more than 75% of its disk space. | ✅&nbsp;Success | - |
| campus-leaf1 | System | VerifyMaintenance | Verifies that the device is not currently under or entering maintenance. | ✅&nbsp;Success | - |
| campus-leaf1 | System | VerifyMemoryUtilization | Verifies whether the memory utilization is below 75%. | ✅&nbsp;Success | - |
| campus-leaf1 | System | VerifyReloadCause | Verifies the last reload cause of the device. | ✅&nbsp;Success | - |
| campus-leaf2 | Configuration | VerifyRunningConfigDiffs | Verifies there is no difference between the running-config and the startup-config. | ✅&nbsp;Success | - |
| campus-leaf2 | Configuration | VerifyZeroTouch | Verifies ZeroTouch is disabled. | ✅&nbsp;Success | - |
| campus-leaf2 | Connectivity | VerifyLLDPNeighbors | Verifies the connection status of the specified LLDP (Link Layer Discovery Protocol) neighbors. | ✅&nbsp;Success | - |
| campus-leaf2 | Interfaces | VerifyIllegalLACP | Verifies there are no illegal LACP packets in port channels. | ✅&nbsp;Success | - |
| campus-leaf2 | Interfaces | VerifyInterfaceErrDisabled | Verifies there are no interfaces in the errdisabled state. | ✅&nbsp;Success | - |
| campus-leaf2 | Interfaces | VerifyInterfaceErrors | Verifies that the interfaces error counters are equal to zero. | ✅&nbsp;Success | - |
| campus-leaf2 | Interfaces | VerifyInterfaceUtilization | Verifies that the utilization of interfaces is below a certain threshold. | ✅&nbsp;Success | - |
| campus-leaf2 | Interfaces | VerifyInterfacesStatus | Verifies the operational states of specified interfaces to ensure they match expected configurations. | ✅&nbsp;Success | - |
| campus-leaf2 | Interfaces | VerifyPortChannels | Verifies there are no inactive ports in port channels. | ✅&nbsp;Success | - |
| campus-leaf2 | MLAG | VerifyMlagConfigSanity | Verifies there are no MLAG config-sanity inconsistencies. | ✅&nbsp;Success | - |
| campus-leaf2 | MLAG | VerifyMlagInterfaces | Verifies there are no inactive or active-partial MLAG ports. | ✅&nbsp;Success | - |
| campus-leaf2 | MLAG | VerifyMlagStatus | Verifies the health status of the MLAG configuration. | ✅&nbsp;Success | - |
| campus-leaf2 | Routing | VerifyRoutingProtocolModel | Verifies the configured routing protocol model. | ✅&nbsp;Success | - |
| campus-leaf2 | STP | VerifySTPCounters | Verifies there is no errors in STP BPDU packets. | ✅&nbsp;Success | - |
| campus-leaf2 | System | VerifyAgentLogs | Verifies there are no agent crash reports. | ✅&nbsp;Success | - |
| campus-leaf2 | System | VerifyCoredump | Verifies there are no core dump files. | ✅&nbsp;Success | - |
| campus-leaf2 | System | VerifyFileSystemUtilization | Verifies that no partition is utilizing more than 75% of its disk space. | ✅&nbsp;Success | - |
| campus-leaf2 | System | VerifyMaintenance | Verifies that the device is not currently under or entering maintenance. | ✅&nbsp;Success | - |
| campus-leaf2 | System | VerifyMemoryUtilization | Verifies whether the memory utilization is below 75%. | ✅&nbsp;Success | - |
| campus-leaf2 | System | VerifyReloadCause | Verifies the last reload cause of the device. | ✅&nbsp;Success | - |
| campus-leaf3 | Configuration | VerifyRunningConfigDiffs | Verifies there is no difference between the running-config and the startup-config. | ✅&nbsp;Success | - |
| campus-leaf3 | Configuration | VerifyZeroTouch | Verifies ZeroTouch is disabled. | ✅&nbsp;Success | - |
| campus-leaf3 | Connectivity | VerifyLLDPNeighbors | Verifies the connection status of the specified LLDP (Link Layer Discovery Protocol) neighbors. | ✅&nbsp;Success | - |
| campus-leaf3 | Interfaces | VerifyIllegalLACP | Verifies there are no illegal LACP packets in port channels. | ✅&nbsp;Success | - |
| campus-leaf3 | Interfaces | VerifyInterfaceErrDisabled | Verifies there are no interfaces in the errdisabled state. | ✅&nbsp;Success | - |
| campus-leaf3 | Interfaces | VerifyInterfaceErrors | Verifies that the interfaces error counters are equal to zero. | ✅&nbsp;Success | - |
| campus-leaf3 | Interfaces | VerifyInterfaceUtilization | Verifies that the utilization of interfaces is below a certain threshold. | ✅&nbsp;Success | - |
| campus-leaf3 | Interfaces | VerifyInterfacesStatus | Verifies the operational states of specified interfaces to ensure they match expected configurations. | ✅&nbsp;Success | - |
| campus-leaf3 | Interfaces | VerifyPortChannels | Verifies there are no inactive ports in port channels. | ✅&nbsp;Success | - |
| campus-leaf3 | MLAG | VerifyMlagConfigSanity | Verifies there are no MLAG config-sanity inconsistencies. | ✅&nbsp;Success | - |
| campus-leaf3 | MLAG | VerifyMlagInterfaces | Verifies there are no inactive or active-partial MLAG ports. | ✅&nbsp;Success | - |
| campus-leaf3 | MLAG | VerifyMlagStatus | Verifies the health status of the MLAG configuration. | ✅&nbsp;Success | - |
| campus-leaf3 | Routing | VerifyRoutingProtocolModel | Verifies the configured routing protocol model. | ✅&nbsp;Success | - |
| campus-leaf3 | STP | VerifySTPCounters | Verifies there is no errors in STP BPDU packets. | ✅&nbsp;Success | - |
| campus-leaf3 | System | VerifyAgentLogs | Verifies there are no agent crash reports. | ✅&nbsp;Success | - |
| campus-leaf3 | System | VerifyCoredump | Verifies there are no core dump files. | ✅&nbsp;Success | - |
| campus-leaf3 | System | VerifyFileSystemUtilization | Verifies that no partition is utilizing more than 75% of its disk space. | ✅&nbsp;Success | - |
| campus-leaf3 | System | VerifyMaintenance | Verifies that the device is not currently under or entering maintenance. | ✅&nbsp;Success | - |
| campus-leaf3 | System | VerifyMemoryUtilization | Verifies whether the memory utilization is below 75%. | ✅&nbsp;Success | - |
| campus-leaf3 | System | VerifyReloadCause | Verifies the last reload cause of the device. | ✅&nbsp;Success | - |
| campus-leaf4 | Configuration | VerifyRunningConfigDiffs | Verifies there is no difference between the running-config and the startup-config. | ✅&nbsp;Success | - |
| campus-leaf4 | Configuration | VerifyZeroTouch | Verifies ZeroTouch is disabled. | ✅&nbsp;Success | - |
| campus-leaf4 | Connectivity | VerifyLLDPNeighbors | Verifies the connection status of the specified LLDP (Link Layer Discovery Protocol) neighbors. | ✅&nbsp;Success | - |
| campus-leaf4 | Interfaces | VerifyIllegalLACP | Verifies there are no illegal LACP packets in port channels. | ✅&nbsp;Success | - |
| campus-leaf4 | Interfaces | VerifyInterfaceErrDisabled | Verifies there are no interfaces in the errdisabled state. | ✅&nbsp;Success | - |
| campus-leaf4 | Interfaces | VerifyInterfaceErrors | Verifies that the interfaces error counters are equal to zero. | ✅&nbsp;Success | - |
| campus-leaf4 | Interfaces | VerifyInterfaceUtilization | Verifies that the utilization of interfaces is below a certain threshold. | ✅&nbsp;Success | - |
| campus-leaf4 | Interfaces | VerifyInterfacesStatus | Verifies the operational states of specified interfaces to ensure they match expected configurations. | ✅&nbsp;Success | - |
| campus-leaf4 | Interfaces | VerifyPortChannels | Verifies there are no inactive ports in port channels. | ✅&nbsp;Success | - |
| campus-leaf4 | MLAG | VerifyMlagConfigSanity | Verifies there are no MLAG config-sanity inconsistencies. | ✅&nbsp;Success | - |
| campus-leaf4 | MLAG | VerifyMlagInterfaces | Verifies there are no inactive or active-partial MLAG ports. | ✅&nbsp;Success | - |
| campus-leaf4 | MLAG | VerifyMlagStatus | Verifies the health status of the MLAG configuration. | ✅&nbsp;Success | - |
| campus-leaf4 | Routing | VerifyRoutingProtocolModel | Verifies the configured routing protocol model. | ✅&nbsp;Success | - |
| campus-leaf4 | STP | VerifySTPCounters | Verifies there is no errors in STP BPDU packets. | ✅&nbsp;Success | - |
| campus-leaf4 | System | VerifyAgentLogs | Verifies there are no agent crash reports. | ✅&nbsp;Success | - |
| campus-leaf4 | System | VerifyCoredump | Verifies there are no core dump files. | ✅&nbsp;Success | - |
| campus-leaf4 | System | VerifyFileSystemUtilization | Verifies that no partition is utilizing more than 75% of its disk space. | ✅&nbsp;Success | - |
| campus-leaf4 | System | VerifyMaintenance | Verifies that the device is not currently under or entering maintenance. | ✅&nbsp;Success | - |
| campus-leaf4 | System | VerifyMemoryUtilization | Verifies whether the memory utilization is below 75%. | ✅&nbsp;Success | - |
| campus-leaf4 | System | VerifyReloadCause | Verifies the last reload cause of the device. | ✅&nbsp;Success | - |
| campus-spine1 | BGP | VerifyBGPPeerSession | Verifies the session state of BGP peers. | ✅&nbsp;Success | - |
| campus-spine1 | Configuration | VerifyRunningConfigDiffs | Verifies there is no difference between the running-config and the startup-config. | ✅&nbsp;Success | - |
| campus-spine1 | Configuration | VerifyZeroTouch | Verifies ZeroTouch is disabled. | ✅&nbsp;Success | - |
| campus-spine1 | Connectivity | VerifyLLDPNeighbors | Verifies the connection status of the specified LLDP (Link Layer Discovery Protocol) neighbors. | ✅&nbsp;Success | - |
| campus-spine1 | Connectivity | VerifyReachability | Verifies reachability to BGP neighbors. | ✅&nbsp;Success | - |
| campus-spine1 | Interfaces | VerifyIllegalLACP | Verifies there are no illegal LACP packets in port channels. | ✅&nbsp;Success | - |
| campus-spine1 | Interfaces | VerifyInterfaceErrDisabled | Verifies there are no interfaces in the errdisabled state. | ✅&nbsp;Success | - |
| campus-spine1 | Interfaces | VerifyInterfaceErrors | Verifies that the interfaces error counters are equal to zero. | ✅&nbsp;Success | - |
| campus-spine1 | Interfaces | VerifyInterfaceUtilization | Verifies that the utilization of interfaces is below a certain threshold. | ✅&nbsp;Success | - |
| campus-spine1 | Interfaces | VerifyInterfacesStatus | Verifies the operational states of specified interfaces to ensure they match expected configurations. | ✅&nbsp;Success | - |
| campus-spine1 | Interfaces | VerifyPortChannels | Verifies there are no inactive ports in port channels. | ✅&nbsp;Success | - |
| campus-spine1 | MLAG | VerifyMlagConfigSanity | Verifies there are no MLAG config-sanity inconsistencies. | ✅&nbsp;Success | - |
| campus-spine1 | MLAG | VerifyMlagInterfaces | Verifies there are no inactive or active-partial MLAG ports. | ✅&nbsp;Success | - |
| campus-spine1 | MLAG | VerifyMlagStatus | Verifies the health status of the MLAG configuration. | ✅&nbsp;Success | - |
| campus-spine1 | OSPF | VerifyOSPFMaxLSA | Verifies all OSPF instances did not cross the maximum LSA threshold. | ✅&nbsp;Success | - |
| campus-spine1 | OSPF | VerifyOSPFNeighborState | Verifies all OSPF neighbors are in FULL state. | ✅&nbsp;Success | - |
| campus-spine1 | Routing | VerifyRoutingProtocolModel | Verifies the configured routing protocol model. | ✅&nbsp;Success | - |
| campus-spine1 | STP | VerifySTPCounters | Verifies there is no errors in STP BPDU packets. | ✅&nbsp;Success | - |
| campus-spine1 | System | VerifyAgentLogs | Verifies there are no agent crash reports. | ✅&nbsp;Success | - |
| campus-spine1 | System | VerifyCoredump | Verifies there are no core dump files. | ✅&nbsp;Success | - |
| campus-spine1 | System | VerifyFileSystemUtilization | Verifies that no partition is utilizing more than 75% of its disk space. | ✅&nbsp;Success | - |
| campus-spine1 | System | VerifyMaintenance | Verifies that the device is not currently under or entering maintenance. | ✅&nbsp;Success | - |
| campus-spine1 | System | VerifyMemoryUtilization | Verifies whether the memory utilization is below 75%. | ✅&nbsp;Success | - |
| campus-spine1 | System | VerifyReloadCause | Verifies the last reload cause of the device. | ✅&nbsp;Success | - |
| campus-spine2 | BGP | VerifyBGPPeerSession | Verifies the session state of BGP peers. | ✅&nbsp;Success | - |
| campus-spine2 | Configuration | VerifyRunningConfigDiffs | Verifies there is no difference between the running-config and the startup-config. | ✅&nbsp;Success | - |
| campus-spine2 | Configuration | VerifyZeroTouch | Verifies ZeroTouch is disabled. | ✅&nbsp;Success | - |
| campus-spine2 | Connectivity | VerifyLLDPNeighbors | Verifies the connection status of the specified LLDP (Link Layer Discovery Protocol) neighbors. | ✅&nbsp;Success | - |
| campus-spine2 | Connectivity | VerifyReachability | Verifies reachability to BGP neighbors. | ✅&nbsp;Success | - |
| campus-spine2 | Interfaces | VerifyIllegalLACP | Verifies there are no illegal LACP packets in port channels. | ✅&nbsp;Success | - |
| campus-spine2 | Interfaces | VerifyInterfaceErrDisabled | Verifies there are no interfaces in the errdisabled state. | ✅&nbsp;Success | - |
| campus-spine2 | Interfaces | VerifyInterfaceErrors | Verifies that the interfaces error counters are equal to zero. | ✅&nbsp;Success | - |
| campus-spine2 | Interfaces | VerifyInterfaceUtilization | Verifies that the utilization of interfaces is below a certain threshold. | ✅&nbsp;Success | - |
| campus-spine2 | Interfaces | VerifyInterfacesStatus | Verifies the operational states of specified interfaces to ensure they match expected configurations. | ✅&nbsp;Success | - |
| campus-spine2 | Interfaces | VerifyPortChannels | Verifies there are no inactive ports in port channels. | ✅&nbsp;Success | - |
| campus-spine2 | MLAG | VerifyMlagConfigSanity | Verifies there are no MLAG config-sanity inconsistencies. | ✅&nbsp;Success | - |
| campus-spine2 | MLAG | VerifyMlagInterfaces | Verifies there are no inactive or active-partial MLAG ports. | ✅&nbsp;Success | - |
| campus-spine2 | MLAG | VerifyMlagStatus | Verifies the health status of the MLAG configuration. | ✅&nbsp;Success | - |
| campus-spine2 | OSPF | VerifyOSPFMaxLSA | Verifies all OSPF instances did not cross the maximum LSA threshold. | ✅&nbsp;Success | - |
| campus-spine2 | OSPF | VerifyOSPFNeighborState | Verifies all OSPF neighbors are in FULL state. | ✅&nbsp;Success | - |
| campus-spine2 | Routing | VerifyRoutingProtocolModel | Verifies the configured routing protocol model. | ✅&nbsp;Success | - |
| campus-spine2 | STP | VerifySTPCounters | Verifies there is no errors in STP BPDU packets. | ✅&nbsp;Success | - |
| campus-spine2 | System | VerifyAgentLogs | Verifies there are no agent crash reports. | ✅&nbsp;Success | - |
| campus-spine2 | System | VerifyCoredump | Verifies there are no core dump files. | ✅&nbsp;Success | - |
| campus-spine2 | System | VerifyFileSystemUtilization | Verifies that no partition is utilizing more than 75% of its disk space. | ✅&nbsp;Success | - |
| campus-spine2 | System | VerifyMaintenance | Verifies that the device is not currently under or entering maintenance. | ✅&nbsp;Success | - |
| campus-spine2 | System | VerifyMemoryUtilization | Verifies whether the memory utilization is below 75%. | ✅&nbsp;Success | - |
| campus-spine2 | System | VerifyReloadCause | Verifies the last reload cause of the device. | ✅&nbsp;Success | - |
