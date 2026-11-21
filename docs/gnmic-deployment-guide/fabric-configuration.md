# **Fabric Configuration**

## **Spine**

!!! info
    The example Spine configuration snippets below are all taken from `spine1`.

### **Global Defaults (Spine)**

```
no enable password
no aaa root
!
vlan internal order ascending range 1006 1199
!
transceiver qsfp default-mode 4x10G
!
service routing protocols model multi-agent
!
hostname om-spine1
!
spanning-tree mode mstp
```

### **Enable Routing (Spine)**

```
ip routing
no ip routing vrf MGMT
```

### **Interfaces (Spine)**

The four downlinks toward the leaves are P2P routed interfaces from the `172.31.255.0/24` underlay pool, each a /31. `Loopback0` is the BGP router-id and next-hop for the EVPN overlay.

```
interface Ethernet1
   description P2P_om-pe11_Ethernet1
   no shutdown
   mtu 9214
   no switchport
   ip address 172.31.255.0/31
!
interface Ethernet2
   description P2P_om-pe12_Ethernet1
   no shutdown
   mtu 9214
   no switchport
   ip address 172.31.255.4/31
!
interface Loopback0
   description ROUTER_ID
   no shutdown
   ip address 192.168.255.1/32
!
interface Management0
   description OOB_MANAGEMENT
   no shutdown
   vrf MGMT
   ip address 172.144.100.2/24
```

### **Prefix Lists (Spine)**

Used by the `RM-CONN-2-BGP` route-map to redistribute Loopback0 addresses into the underlay so leaves learn each other's EVPN next-hops.

```
ip prefix-list PL-LOOPBACKS-EVPN-OVERLAY
   seq 10 permit 192.168.255.0/24 eq 32
```

### **Route Maps (Spine)**

```
route-map RM-CONN-2-BGP permit 10
   match ip address prefix-list PL-LOOPBACKS-EVPN-OVERLAY
```

### **BGP: Underlay (Spine)**

eBGP over the P2P interfaces to each leaf. Each leaf has its own ASN (`65101`–`65104`); the spine advertises Loopback0 via `redistribute connected`.

```
router bgp 65001
   router-id 192.168.255.1
   no bgp default ipv4-unicast
   distance bgp 20 200 200
   maximum-paths 4 ecmp 4
   neighbor IPv4-UNDERLAY-PEERS peer group
   neighbor IPv4-UNDERLAY-PEERS password 7 AQQvKeimxJu+uGQ/yYvv9w==
   neighbor IPv4-UNDERLAY-PEERS send-community
   neighbor IPv4-UNDERLAY-PEERS maximum-routes 12000
   neighbor 172.31.255.1 peer group IPv4-UNDERLAY-PEERS
   neighbor 172.31.255.1 remote-as 65101
   neighbor 172.31.255.1 description om-pe11_Ethernet1
   neighbor 172.31.255.5 peer group IPv4-UNDERLAY-PEERS
   neighbor 172.31.255.5 remote-as 65102
   neighbor 172.31.255.5 description om-pe12_Ethernet1
   redistribute connected route-map RM-CONN-2-BGP
   !
   address-family ipv4
      no neighbor EVPN-OVERLAY-PEERS activate
      neighbor IPv4-UNDERLAY-PEERS activate
```

### **BGP: Overlay (Spine)**

eBGP EVPN peerings sourced from Loopback0, `ebgp-multihop 3`, and `next-hop-unchanged` so the spine reflects the original next-hop (each leaf's Loopback1 VTEP) rather than rewriting it to its own Loopback0. RT-Constraint (rt-membership AFI) reduces overlay churn.

```
   neighbor EVPN-OVERLAY-PEERS peer group
   neighbor EVPN-OVERLAY-PEERS next-hop-unchanged
   neighbor EVPN-OVERLAY-PEERS update-source Loopback0
   neighbor EVPN-OVERLAY-PEERS bfd
   neighbor EVPN-OVERLAY-PEERS ebgp-multihop 3
   neighbor EVPN-OVERLAY-PEERS password 7 q+VNViP5i4rVjW1cxFv2wA==
   neighbor EVPN-OVERLAY-PEERS send-community
   neighbor 192.168.255.3 peer group EVPN-OVERLAY-PEERS
   neighbor 192.168.255.3 remote-as 65101
   neighbor 192.168.255.3 description om-pe11_Loopback0
   neighbor 192.168.255.4 peer group EVPN-OVERLAY-PEERS
   neighbor 192.168.255.4 remote-as 65102
   neighbor 192.168.255.4 description om-pe12_Loopback0
   !
   address-family evpn
      neighbor EVPN-OVERLAY-PEERS activate
   !
   address-family rt-membership
      neighbor EVPN-OVERLAY-PEERS activate
      neighbor EVPN-OVERLAY-PEERS default-route-target only
```

### **gNMI Server (Spine)**

Two gRPC transports listen: `default` in the default VRF and `MGMT` on `Management0`. The `provider eos-native` line enables the `eos_native:` YANG tree — without it, any subscription with an `eos_native:` prefix comes back empty. Default port is 6030.

```
management api gnmi
   transport grpc default
      notification timestamp send-time
   !
   transport grpc MGMT
      vrf MGMT
      notification timestamp send-time
   provider eos-native
```

## **Leaf (PE)**

!!! info
    The example Leaf configuration snippets below are all taken from `pe11`.

### **Global Defaults (Leaf)**

Leaves prefer MST with priority 4096 (root-bridge candidate).

```
vlan internal order ascending range 1006 1199
!
transceiver qsfp default-mode 4x10G
!
service routing protocols model multi-agent
!
hostname om-pe11
!
spanning-tree mode mstp
spanning-tree mst 0 priority 4096
```

### **Enable Routing (Leaf)**

```
ip routing
no ip routing vrf MGMT
```

### **Interfaces (Leaf)**

Two uplinks to the spines are routed /31 P2Ps. Two downlinks to servers are LACP members of Port-Channels. `Loopback0` is the router-id and EVPN peering source; `Loopback1` is the VTEP source used by the `Vxlan1` interface.

```
interface Ethernet1
   description P2P_om-spine1_Ethernet1
   no shutdown
   mtu 9214
   no switchport
   ip address 172.31.255.1/31
!
interface Ethernet2
   description P2P_om-spine2_Ethernet1
   no shutdown
   mtu 9214
   no switchport
   ip address 172.31.255.3/31
!
interface Ethernet3
   description SERVER_server01_Eth1
   no shutdown
   channel-group 3 mode active
!
interface Ethernet4
   description SERVER_server02_Eth1
   no shutdown
   channel-group 4 mode active
!
interface Loopback0
   description ROUTER_ID
   no shutdown
   ip address 192.168.255.3/32
!
interface Loopback1
   description VXLAN_TUNNEL_SOURCE
   no shutdown
   ip address 192.168.254.3/32
```

### **Prefix Lists (Leaf)**

Redistributes both the router-id loopback and the VTEP loopback into the underlay so peers can reach the VXLAN tunnel endpoints.

```
ip prefix-list PL-LOOPBACKS-EVPN-OVERLAY
   seq 10 permit 192.168.255.0/24 eq 32
   seq 20 permit 192.168.254.0/24 eq 32
```

### **Route Maps (Leaf)**

```
route-map RM-CONN-2-BGP permit 10
   match ip address prefix-list PL-LOOPBACKS-EVPN-OVERLAY
```

### **BGP: Underlay (Leaf)**

Each leaf peers with both spines (`172.31.255.0`, `172.31.255.2`) at ASN `65001`. `no bgp default ipv4-unicast` keeps the overlay peer-group off the IPv4 AFI so EVPN reachability is not carried in the underlay.

```
router bgp 65101
   router-id 192.168.255.3
   no bgp default ipv4-unicast
   distance bgp 20 200 200
   maximum-paths 4 ecmp 4
   neighbor IPv4-UNDERLAY-PEERS peer group
   neighbor IPv4-UNDERLAY-PEERS password 7 AQQvKeimxJu+uGQ/yYvv9w==
   neighbor IPv4-UNDERLAY-PEERS send-community
   neighbor IPv4-UNDERLAY-PEERS maximum-routes 12000
   neighbor 172.31.255.0 peer group IPv4-UNDERLAY-PEERS
   neighbor 172.31.255.0 remote-as 65001
   neighbor 172.31.255.0 description om-spine1_Ethernet1
   neighbor 172.31.255.2 peer group IPv4-UNDERLAY-PEERS
   neighbor 172.31.255.2 remote-as 65001
   neighbor 172.31.255.2 description om-spine2_Ethernet1
   redistribute connected route-map RM-CONN-2-BGP
```

### **EVPN Multi-Homing (Leaf)**

Each server-facing Port-Channel is an EVPN Ethernet Segment with an explicit ESI and matching LACP system-id. Both leaves in the POD present the same ESI + system-id per bond, so from the client side the two uplinks look like one MLAG bundle, while from the fabric side the MAC/IP is advertised as reachable via the ES (Type-1 Ethernet A-D routes, Type-2 MAC/IP routes).

```
interface Port-Channel3
   description PortChannel3
   no shutdown
   switchport trunk allowed vlan 110
   switchport mode trunk
   switchport
   !
   evpn ethernet-segment
      identifier 0000:0000:0101:0102:0033
      route-target import 01:01:01:02:00:33
   lacp system-id 0101.0102.0033
   spanning-tree portfast
!
interface Port-Channel4
   description PortChannel4
   no shutdown
   switchport trunk allowed vlan 111
   switchport mode trunk
   switchport
   !
   evpn ethernet-segment
      identifier 0000:0000:0101:0102:0044
      route-target import 01:01:01:02:00:44
   lacp system-id 0101.0102.0044
   spanning-tree portfast
```

### **VXLAN Interface (Leaf)**

Single `Vxlan1` interface sourced from Loopback1, one VLAN-to-VNI mapping per tenant network.

```
interface Vxlan1
   description om-pe11_VTEP
   vxlan source-interface Loopback1
   vxlan udp-port 4789
   vxlan vlan 110 vni 10110
   vxlan vlan 111 vni 10111
```

### **BGP: Overlay (Leaf)**

Each leaf peers with both spines' Loopback0 in the EVPN AFI. Per-VLAN `rd` and `route-target` under `router bgp` bind each MAC-VRF to its L2VNI.

```
   neighbor EVPN-OVERLAY-PEERS peer group
   neighbor EVPN-OVERLAY-PEERS update-source Loopback0
   neighbor EVPN-OVERLAY-PEERS bfd
   neighbor EVPN-OVERLAY-PEERS ebgp-multihop 3
   neighbor EVPN-OVERLAY-PEERS password 7 q+VNViP5i4rVjW1cxFv2wA==
   neighbor EVPN-OVERLAY-PEERS send-community
   neighbor 192.168.255.1 peer group EVPN-OVERLAY-PEERS
   neighbor 192.168.255.1 remote-as 65001
   neighbor 192.168.255.1 description om-spine1_Loopback0
   neighbor 192.168.255.2 peer group EVPN-OVERLAY-PEERS
   neighbor 192.168.255.2 remote-as 65001
   neighbor 192.168.255.2 description om-spine2_Loopback0
   !
   address-family evpn
      neighbor EVPN-OVERLAY-PEERS activate
```

### **MAC-VRF (Leaf)**

One MAC-VRF per L2VNI. `redistribute learned` triggers Type-2 MAC/IP advertisement whenever the local FDB learns a new address.

```
   vlan 110
      rd 192.168.255.3:10110
      route-target both 10110:10110
      redistribute learned
   !
   vlan 111
      rd 192.168.255.3:10111
      route-target both 10111:10111
      redistribute learned
```

### **gNMI Server (Leaf)**

Same shape as the spine — two transports, `provider eos-native` for the `eos_native:` tree.

```
management api gnmi
   transport grpc default
      notification timestamp send-time
   !
   transport grpc MGMT
      vrf MGMT
      notification timestamp send-time
   provider eos-native
```

## **Underlay Variant: IS-IS**

!!! info
    Deploy this variant with `ansible-playbook playbooks/fabric-deploy-config.yaml -e underlay_routing_protocol=isis`. In this build the IS-IS blocks below **replace** the [`BGP: Underlay (Spine)`](#bgp-underlay-spine) and [`BGP: Underlay (Leaf)`](#bgp-underlay-leaf) sections above; everything else (interfaces, loopbacks, EVPN overlay peerings, VXLAN, MAC-VRF) is identical to the eBGP variant. The knobs come from `group_vars/OM_FABRIC.yaml` (`isis_area_id: 49.0001`, `isis_default_is_type: level-2`, `isis_advertise_passive_only: false`) and are inert when `underlay_routing_protocol: ebgp`.

    The AVD-generated IS-IS instance is named `EVPN_UNDERLAY` — that is the exact string the [`isis_adjacencies` subscription](telemetry-stack.md#subscriptions-gnmic) targets in `clab/gnmic.yml`.

### **IS-IS Underlay (Spine)**

Level-2, area `49.0001`. `Loopback0` is passive so the router-id is advertised without forming an adjacency on it, and each P2P uplink is a point-to-point IS-IS interface. `authentication mode md5` uses the same key as the eBGP-underlay password so the two variants stay swap-compatible.

```
router isis EVPN_UNDERLAY
   net 49.0001.0000.0000.0001.00
   is-type level-2
   router-id ipv4 192.168.255.1
   log-adjacency-changes
   no hello padding
   authentication mode md5
   authentication key 7 <redacted>
   !
   address-family ipv4 unicast
      maximum-paths 4
!
interface Loopback0
   isis enable EVPN_UNDERLAY
   isis passive
!
interface Ethernet1
   isis enable EVPN_UNDERLAY
   isis network point-to-point
   isis metric 50
!
interface Ethernet2
   isis enable EVPN_UNDERLAY
   isis network point-to-point
   isis metric 50
```

The spine still runs `router bgp 65001` for the [EVPN overlay](#bgp-overlay-spine) — only the underlay peer-group (`IPv4-UNDERLAY-PEERS`) and its neighbors disappear. `redistribute connected` is not needed either; IS-IS floods Loopback0 directly.

### **IS-IS Underlay (Leaf)**

Same pattern. The NET's system-id encodes the AVD node ID (`pe11 → id 1`, encoded as `0000.0000.1001`). Both Loopbacks are passive so they advertise without adjacency; the two spine-facing uplinks form point-to-point Level-2 adjacencies.

```
router isis EVPN_UNDERLAY
   net 49.0001.0000.0000.1001.00
   is-type level-2
   router-id ipv4 192.168.255.3
   log-adjacency-changes
   no hello padding
   authentication mode md5
   authentication key 7 <redacted>
   !
   address-family ipv4 unicast
      maximum-paths 4
!
interface Loopback0
   isis enable EVPN_UNDERLAY
   isis passive
!
interface Loopback1
   isis enable EVPN_UNDERLAY
   isis passive
!
interface Ethernet1
   isis enable EVPN_UNDERLAY
   isis network point-to-point
   isis metric 50
!
interface Ethernet2
   isis enable EVPN_UNDERLAY
   isis network point-to-point
   isis metric 50
```

`Loopback1` (the VTEP source) is also injected into IS-IS as passive — without this, remote VTEPs would be unreachable and Type-2 MAC/IP routes would install with an unresolvable next-hop.

### **Verifying the underlay swap**

On any device:

```
show isis neighbors
show isis interface brief
show ip route isis
```

And from the collector side, the [`isis_adjacencies`](telemetry-stack.md#subscriptions-gnmic) subscription starts returning notifications (it's silent in the eBGP variant):

```bash
docker exec -it gnmic gnmic -a spine1:6030 --insecure -u arista -p arista \
  subscribe --path "/network-instances/network-instance[name=default]/protocols/protocol[name=EVPN_UNDERLAY]/isis" --mode once
```

The EVPN overlay is untouched — `show bgp evpn summary` on any leaf still lists the same two spine peers, and the L3 Telemetry dashboard's `bgp_neighbors` panel keeps showing the overlay session state.


---

**Next:** [Telemetry Stack →](telemetry-stack.md) &nbsp;·&nbsp; [Back to guide index](index.md)

--8<-- "gnmic-deployment-guide/_abbreviations.md"