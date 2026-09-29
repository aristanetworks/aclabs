# Initial Deployment - Day 0

## AVD Lab Guide Overview

The AVD Lab Guide is a follow-along set of instructions to deploy a dual data center L3LS EVPN VXLAN fabric design. The data model overview and details can be found [here](overview.md). In the following steps, we will explore updating the data models to add services, ports, and DCI links to our fabrics and test traffic between sites.

In this example, the ATD lab is used to create the L3LS Dual Data Center topology below. The DCI Network cloud (orange area) is pre-provisioned and is comprised of the core nodes in the ATD topology. Our focus will be creating the L3LS AVD data models to build and deploy configurations for Site 1 and Site 2 (blue areas) and connect them to the DCI Network.

![Dual DC Topology](images/l3ls_dualdc_topo.png)

### Host Addresses

| Host     |  IP Address  |
|:--------:|:------------:|
| s1-host1 | 10.10.10.100 |
| s1-host2 | 10.20.20.100 |
| s2-host1 | 10.10.10.200 |
| s2-host2 | 10.20.20.200 |

## Step 1 - Prepare Lab Environment

### TODO: Access the ATD Lab and Git Initialization 


Connect to your ATD Lab and start the Programmability IDE. Next, open a new Terminal.

Initialize Git and configure your global Git settings.

```bash
git init -b main
```

``` bash
git config --global user.name "FirstName LastName"
```

``` bash
git config --global user.email "name@example.com"
```

### TODO: Reword, already configured on startup, Prepare DCI Network and Test Hosts

The last step in preparing your lab is to push pre-defined configurations to the DCI Network (cloud) and the four hosts used to test traffic. The border leafs from each site will connect to their specified peer with P2P links. The hosts (two per site) have port-channels to the leaf pairs and are pre-configured with an IP address and route to reach the other hosts.

Run the following to push the configs.

``` bash
make preplab
```

## Step 2 - Deployment Overview

This section will review and update the existing L3LS data model. We will add features to enable VLANs, SVIs, connected endpoints, and P2P links to the DCI Network. After the lab, you will have enabled an L3LS EVPN VXLAN dual data center network through automation with AVD. YAML data models and Ansible playbooks will be used to generate EOS CLI configurations and deploy them to each site. We will start by focusing on building out Site 1 and then repeat similar steps for Site 2. Then, we will enable connectivity to the DCI Network to allow traffic to pass between sites. Finally, we will enable EVPN gateway functionality on the border leafs.

### Summary of Steps

- Build and Deploy `Site 1`
- Build and Deploy `Site 2`
- Connect sites to DCI Network
- Verify routing
- Enable EVPN gateway functionality
- Test traffic

## Step 3 - Site 1

### Build and Deploy Initial Fabric

The initial fabric data model key/value pairs have been pre-populated in the following group_vars files in the `sites/site_1/group_vars/` directory.

- SITE1_CONNECTED_ENDPOINTS.yml
- SITE1_NETWORK_SERVICES.yml
- SITE1_FABRIC.yml
- SITE1_LEAFS.yml
- SITE1_SPINES.yml

Review these files to understand how they relate to the topology above.

At this point, we can build our initial configurations for the topology.

``` bash
make build-site-1
```

> Feel free to run `git add` and `git commit` to create a snapshot of the current build state. This will help you view the differences between steps in the workshop..

``` bash
git add .
git commit -m "saving snapshot"
```

AVD creates a separate markdown and EOS configuration file per switch. In addition, you can review the files in the `documentation` and `intended` folders per site.

![Docs and Configs](images/docs-configs.png)

Now, deploy the configurations to Site 1 switches.

``` bash
make deploy-site-1
```

#### Verification

Now, lets login to some switches to verify the current configs (`show run`) match the ones created in `intended/configs` folder. We can also check the current state for MLAG, interfaces, BGP peerings for IPv4 underlay, and BGP EVPN overlay peerings.

You can connect to devices in two ways:

- Clicking a node in the ATD lab topology image.
- Running `ssh arista@s1-spine1` or entering `s1-spine1` directly from the terminal.

These outputs were taken from `s1-leaf1`:

1. Check MLAG status.

    **Command**

    ``` bash
    show mlag
    ```

    **Expected Output**

    ``` text
    s1-leaf1#show mlag
    MLAG Configuration:
    domain-id                          :            S1_RACK1
    local-interface                    :            Vlan4094
    peer-address                       :          10.251.1.1
    peer-link                          :       Port-Channel1
    hb-peer-address                    :             0.0.0.0
    peer-config                        :          consistent

    MLAG Status:
    state                              :              Active
    negotiation status                 :           Connected
    peer-link status                   :                  Up
    local-int status                   :                  Up
    system-id                          :   02:1c:73:c0:c6:12
    dual-primary detection             :            Disabled
    dual-primary interface errdisabled :               False

    MLAG Ports:
    Disabled                           :                   0
    Configured                         :                   0
    Inactive                           :                   0
    Active-partial                     :                   0
    Active-full                        :                   0
    ```

2. Check routed interface configurations.

    **Command**

    ``` bash
    show ip interface brief
    ```

    **Expected Output**

    ``` text
    s1-leaf1#show ip interface brief
                                                                                    Address
    Interface         IP Address            Status       Protocol            MTU    Owner
    ----------------- --------------------- ------------ -------------- ----------- -------
    Ethernet2         172.16.1.1/31         up           up                 1500
    Ethernet3         172.16.1.3/31         up           up                 1500
    Loopback0         10.250.1.3/32         up           up                65535
    Loopback1         10.255.1.3/32         up           up                65535
    Management0       192.168.0.12/24       up           up                 1500
    Vlan4093          10.252.1.0/31         up           up                 1500
    Vlan4094          10.251.1.0/31         up           up                 1500
    ```

3. Check eBGP/iBGP peerings for IPv4 underlay routing.

    **Commands**

    ``` bash
    show ip bgp summary
    ```

    **Expected Output**

    ``` text
    s1-leaf1#show ip bgp summary
    BGP summary information for VRF default
    Router identifier 10.250.1.3, local AS number 65101
    Neighbor Status Codes: m - Under maintenance
      Description              Neighbor   V AS           MsgRcvd   MsgSent  InQ OutQ  Up/Down State   PfxRcd PfxAcc
      s1-leaf2                 10.252.1.1 4 65101             15        14    0    0 00:02:29 Estab   10     10
      s1-spine1_Ethernet2      172.16.1.0 4 65100             13        18    0    0 00:02:30 Estab   7      7
      s1-spine2_Ethernet2      172.16.1.2 4 65100             15        14    0    0 00:02:29 Estab   7      7
    ```

4. Check eBGP/iBGP peerings for the EVPN overlay.

    **Commands**

    ``` bash
    show bgp evpn summary
    ```

    **Expected Output**

    ``` text
    s1-leaf1#show bgp evpn summary
    BGP summary information for VRF default
    Router identifier 10.250.1.3, local AS number 65101
    Neighbor Status Codes: m - Under maintenance
      Description              Neighbor   V AS           MsgRcvd   MsgSent  InQ OutQ  Up/Down State   PfxRcd PfxAcc
      s1-spine1                10.250.1.1 4 65100              5         5    0    0 00:01:39 Estab   0      0
      s1-spine2                10.250.1.2 4 65100              5         6    0    0 00:01:40 Estab   0      0
    ```

> The basic fabric with MLAG peers, P2P routed links between leaf and spines, eBGP/iBGP IPv4 underlay peerings, and eBGP/iBGP EVPN overlay peerings is now created. Next up, we will add VLAN and SVI services to the fabric.

### Add Services to the Fabric

The next step is to add VLANs and SVIs to the fabric. The services data model file `SITE1_NETWORK_SERVICES.yml` is pre-populated with VLANs and SVIs `10` and `20` in the **OVERLAY** VRF.

Open `sites/site_1/group_vars/SITE1_NETWORK_SERVICES.yml` and uncomment lines 1-16, then run the build & deploy process again.

> In VS Code, you can toggle comments on/off by selecting the text and pressing `ctrl + /` or `cmd + /`.

**Build the Configs**

``` text
make build-site-1
```

**Deploy the Configs**

``` text
make deploy-site-1
```

#### Verification

Now lets go back to node `s1-leaf1` and verify the new SVIs exist, their IP addresses, any changes to the EVPN overlay and corresponding VXLAN configurations, as well as the EVPN control-plane now that we have some layer 3 data interfaces.

1. Verify VLAN SVIs **10** and **20** exist.

    **Command**

    ``` text
    show ip interface brief
    ```

    **Expected Output**

    ``` text
    s1-leaf1#show ip interface brief
                                                                                Address
    Interface         IP Address            Status       Protocol            MTU    Owner
    ----------------- --------------------- ------------ -------------- ----------- -------
    Ethernet2         172.16.1.1/31         up           up                 1500
    Ethernet3         172.16.1.3/31         up           up                 1500
    Loopback0         10.250.1.3/32         up           up                65535
    Loopback1         10.255.1.3/32         up           up                65535
    Management0       192.168.0.12/24       up           up                 1500
    Vlan10            10.10.10.1/24         up           up                 1500
    Vlan20            10.20.20.1/24         up           up                 1500
    Vlan1199          unassigned            up           up                 9164
    Vlan3009          10.252.1.0/31         up           up                 1500
    Vlan4093          10.252.1.0/31         up           up                 1500
    Vlan4094          10.251.1.0/31         up           up                 1500
    ```

    ???+ abstract "Where did those VLANs come from?"
        You should notice some VLANs that we didn't define anywhere in the `_NETWORK_SERVICES.yml` data model which aren't related to **MLAG**.  Specifically, these will be VLAN SVIs ***Vlan1199*** and ***Vlan3009***.

        ***Vlan1199*** is dynamically created and assigned for the **OVERLAY** vrf to VNI mapping under the VXLAN interface.  You can verify this by looking at the **show interface vxlan 1** output.  Remember, we defined **VNI 10** as the `vrf_vni` in our data model.
        ``` text
        Dynamic VLAN to VNI mapping for 'evpn' is
        [1199, 10]
        ```

        ***Vlan3009*** was also auto-configured by AVD for an iBGP peering between `s1-leaf1` and `s1-leaf2` in the **OVERLAY** vrf.  You can verify this by looking at the interface configuration, and BGP peering for that vrf.

        **Interface Configuration**
        ``` text
        s1-leaf1#show run interface vlan 3009
        interface Vlan3009
          description MLAG_PEER_L3_iBGP: vrf OVERLAY
          mtu 1500
          vrf OVERLAY
          ip address 10.252.1.0/31
        ```

        **Overlay vrf BGP Peering**
        ``` text
        s1-leaf1#show ip bgp summary vrf OVERLAY
        BGP summary information for VRF OVERLAY
        Router identifier 10.250.1.3, local AS number 65101
        Neighbor Status Codes: m - Under maintenance
          Description              Neighbor   V AS           MsgRcvd   MsgSent  InQ OutQ  Up/Down State   PfxRcd PfxAcc
          s1-leaf2                 10.252.1.1 4 65101             19        20    0    0 00:11:30 Estab   5      5
        ```

2. Verify VLANs **10** and **20**, and vrf **OVERLAY** are now mapped to the appropriate VNIs under the `vxlan1` interface.

    ^^Command^^

    ``` text
    show run interface vxlan 1
    ```

    ^^Expected Output^^

    ``` text hl_lines="7-9"
    s1-leaf1#show run int vxlan 1
    interface Vxlan1
      description s1-leaf1_VTEP
      vxlan source-interface Loopback1
      vxlan virtual-router encapsulation mac-address mlag-system-id
      vxlan udp-port 4789
      vxlan vlan 10 vni 10010
      vxlan vlan 20 vni 10020
      vxlan vrf OVERLAY vni 10
    ```

3. Verify we are flooding to the correct remote VTEPs based on what we have learned across the EVPN overlay.

    ^^Command^^

    ``` text
    show interface vxlan1
    ```

    ^^Expected Output^^

    ``` text hl_lines="19 20"
    s1-leaf1#show int vxlan 1
    Vxlan1 is up, line protocol is up (connected)
      Hardware is Vxlan
      Description: s1-leaf1_VTEP
      Source interface is Loopback1 and is active with 10.255.1.3
      Listening on UDP port 4789
      Replication/Flood Mode is headend with Flood List Source: EVPN
      Remote MAC learning via EVPN
      VNI mapping to VLANs
      Static VLAN to VNI mapping is
        [10, 10010]       [20, 10020]
      Dynamic VLAN to VNI mapping for 'evpn' is
        [1199, 10]
      Note: All Dynamic VLANs used by VCS are internal VLANs.
            Use 'show vxlan vni' for details.
      Static VRF to VNI mapping is
      [OVERLAY, 10]
      Headend replication flood vtep list is:
        10 10.255.1.5      10.255.1.7
        20 10.255.1.5      10.255.1.7
      MLAG Shared Router MAC is 021c.73c0.c612
    ```

4. Finally, lets verify we have **IMET** (1) routes for each VLAN and VTEP in the EVPN overlay.
    { .annotate }

    1. IMET, or Type-3 routes are required for Broadcast, Unknown Unicast and Multicast (BUM) traffic delivery across EVPN networks.

    ^^Command^^

    ``` text
    show bgp evpn route-type imet
    ```

    ^^Expected Output^^

    ``` text
    s1-leaf1#show bgp evpn route-type imet
    BGP routing table information for VRF default
    Router identifier 10.250.1.3, local AS number 65101
    Route status codes: * - valid, > - active, S - Stale, E - ECMP head, e - ECMP
                        c - Contributing to ECMP, % - Pending best path selection
    Origin codes: i - IGP, e - EGP, ? - incomplete
    AS Path Attributes: Or-ID - Originator ID, C-LST - Cluster List, LL Nexthop - Link Local Nexthop

              Network                Next Hop              Metric  LocPref Weight  Path
    * >      RD: 10.250.1.3:10010 imet 10.255.1.3
                                    -                     -       -       0       i
    * >      RD: 10.250.1.3:10020 imet 10.255.1.3
                                    -                     -       -       0       i
    * >Ec    RD: 10.250.1.5:10010 imet 10.255.1.5
                                    10.255.1.5            -       100     0       65100 65102 i
    *  ec    RD: 10.250.1.5:10010 imet 10.255.1.5
                                    10.255.1.5            -       100     0       65100 65102 i
    * >Ec    RD: 10.250.1.5:10020 imet 10.255.1.5
                                    10.255.1.5            -       100     0       65100 65102 i
    *  ec    RD: 10.250.1.5:10020 imet 10.255.1.5
                                    10.255.1.5            -       100     0       65100 65102 i
    * >Ec    RD: 10.250.1.6:10010 imet 10.255.1.5
                                    10.255.1.5            -       100     0       65100 65102 i
    *  ec    RD: 10.250.1.6:10010 imet 10.255.1.5
                                    10.255.1.5            -       100     0       65100 65102 i
    * >Ec    RD: 10.250.1.6:10020 imet 10.255.1.5
                                    10.255.1.5            -       100     0       65100 65102 i
    *  ec    RD: 10.250.1.6:10020 imet 10.255.1.5
                                    10.255.1.5            -       100     0       65100 65102 i
    * >Ec    RD: 10.250.1.7:10010 imet 10.255.1.7
                                    10.255.1.7            -       100     0       65100 65103 i
    *  ec    RD: 10.250.1.7:10010 imet 10.255.1.7
                                    10.255.1.7            -       100     0       65100 65103 i
    * >Ec    RD: 10.250.1.7:10020 imet 10.255.1.7
                                    10.255.1.7            -       100     0       65100 65103 i
    *  ec    RD: 10.250.1.7:10020 imet 10.255.1.7
                                    10.255.1.7            -       100     0       65100 65103 i
    * >Ec    RD: 10.250.1.8:10010 imet 10.255.1.7
                                    10.255.1.7            -       100     0       65100 65103 i
    *  ec    RD: 10.250.1.8:10010 imet 10.255.1.7
                                    10.255.1.7            -       100     0       65100 65103 i
    * >Ec    RD: 10.250.1.8:10020 imet 10.255.1.7
                                    10.255.1.7            -       100     0       65100 65103 i
    *  ec    RD: 10.250.1.8:10020 imet 10.255.1.7
                                    10.255.1.7            -       100     0       65100 65103 i
    ```

You can verify the recent configuration session was created.

???+ info
    When the configuration is applied via a configuration session, EOS will create a "checkpoint" of the configuration. This checkpoint is a snapshot
    of the device's running configuration as it was **prior** to the configuration session being committed.

``` bash
show clock
```

``` bash
show configuration sessions detail
```

List the recent checkpoints.

``` bash
show config checkpoints
```

View the contents of the latest checkpoint file.

``` bash
more checkpoint:< filename >
```

See the difference between the running config and the latest checkpoint file.

???+ tip
    This will show the differences between the current device configuration
    and the configuration before we did our `make deploy` command.

``` bash
diff checkpoint:< filename > running-config
```

### Add Ports for Hosts

Let's configure port-channels to our hosts (`s1-host1` and `s1-host2`).

Open `SITE1_CONNECTED_ENDPOINTS.yml` and uncomment lines 17-45, then run the build & deploy process again.

``` bash
make build-site-1
```

``` bash
make deploy-site-1
```

At this point, hosts should be able to ping each other across the fabric.

From `s1-host1`, run a ping to `s1-host2`.

``` bash
ping 10.20.20.100
```

``` text
PING 10.20.20.100 (10.20.20.100) 72(100) bytes of data.
80 bytes from 10.20.20.100: icmp_seq=1 ttl=63 time=30.2 ms
80 bytes from 10.20.20.100: icmp_seq=2 ttl=63 time=29.5 ms
80 bytes from 10.20.20.100: icmp_seq=3 ttl=63 time=28.8 ms
80 bytes from 10.20.20.100: icmp_seq=4 ttl=63 time=24.8 ms
80 bytes from 10.20.20.100: icmp_seq=5 ttl=63 time=26.2 ms
```

???+ success "Success"
    Site 1 fabric is now complete.

## Step 4 - Site 2

Repeat the previous three steps for Site 2.

- Add Services
- Add Ports
- Build and Deploy Configs
- Verify ping traffic between hosts `s2-host1` and `s2-host2`

At this point, you should be able to ping between hosts within a site but not between sites. For this, we need to build connectivity to the `DCI Network`. This is covered in the next section.

## Step 5 - Connect Sites to DCI Network

The DCI Network is defined by the `l3_edge` data model. Full data model documentation is located **[here](https://avd.arista.com/5.7/ansible_collections/arista/avd/roles/eos_designs/docs/input-variables.html#l3-edge-and-dci-settings){:target="_blank"}**.

The data model defines P2P links (`/31s`) on the border leafs by using a combination of the ipv4_pool and the node id in the p2p_links section. See details in the graphic below. Each border leaf has a single link to its peer on interface `Ethernet4`.  In the data model, you will notice the parameter for **include_in_underlay_protocol**, which is set to ***true***.  This tells AVD to render the appropriate BGP configurations for route peering.

![Core Interfaces](../assets/l3ls_dci.png)

### Add P2P Links for DCI connectivity for Site 1 and 2

Enable the `l3_edge` dictionary (shown below) by uncommenting it from the `global_vars/global_dc_vars.yml`:

``` yaml
# L3 Edge port definitions. This can be any port in the entire Fabric, where IP interfaces are defined.
l3_edge:
  # Define a new IP pool that will be used to assign IP addresses to L3 Edge interfaces.
  p2p_links_ip_pools:
    - name: S1_to_S2_IP_pool
      ipv4_pool: 172.16.255.0/24
  # Define a new link profile which will match the IP pool, the used ASNs and include the defined interface into underlay routing
  p2p_links_profiles:
    - name: S1_to_S2_profile
      ip_pool: S1_to_S2_IP_pool
      as: [ 65103, 65203 ]
      include_in_underlay_protocol: true
  # Define each P2P L3 link and link the nodes, the interfaces and the profile used.
  p2p_links:
    - id: 1
      nodes: [ s1-brdr1, s2-brdr1 ]
      interfaces: [ Ethernet4, Ethernet4 ]
      profile: S1_to_S2_profile
    - id: 2
      nodes: [ s1-brdr2, s2-brdr2 ]
      interfaces: [ Ethernet5, Ethernet5 ]
      profile: S1_to_S2_profile
```

### Build and Deploy DCI Network Connectivity

``` bash
make all
```

???+ tip
    The `make all` command will run the build and deploy steps in one command.

### Verification

Now that we have built and deployed our configurations for our DCI IPv4 underlay connectivity, lets see what was done. Looking at the data model above, we see we only defined a pool of IP addresses with a **/24** mask which AVD will use to auto-alllocated a subnet per connection.  Additionally, we can see that `s1-brdr1` connects to its peer `s2-brdr1` via interface `Ethernet4`, and `s1-brdr2` connects to its peer `s2-brdr2` via interface `Ethernet5`.  Using that data model, here is what we expect to see configured.  You can verify this by logging into each border leaf and checking with **show ip interface brief**.

| Host     |  Interface   |   IP Address      |
|:--------:|:------------:|:-----------------:|
| s1-brdr1 |   Ethernet4  |  172.16.255.0/31  |
| s2-brdr1 |   Ethernet4  |  172.16.255.1/31  |
| s1-brdr2 |   Ethernet5  |  172.16.255.2/31  |
| s2-brdr2 |   Ethernet5  |  172.16.255.3/31  |

Now lets verify the underlay connectivity and routing across the DCI network.

1. From `s1-brdr1`, check the IPv4 underlay peering to its neighbor at Site 2, `s2-brdr1`.

    ^^Command^^

    ``` text
    show ip bgp summary
    ```

    ^^Expected Output^^

    ``` text hl_lines="9"
    s1-brdr1#show ip bgp summary
    BGP summary information for VRF default
    Router identifier 10.250.1.7, local AS number 65103
    Neighbor Status Codes: m - Under maintenance
      Description              Neighbor     V AS           MsgRcvd   MsgSent  InQ OutQ  Up/Down State   PfxRcd PfxAcc
      s1-brdr2                 10.252.1.9   4 65103            103       100    0    0 01:13:03 Estab   21     21
      s1-spine1_Ethernet7      172.16.1.16  4 65100             98        99    0    0 01:13:03 Estab   7      7
      s1-spine2_Ethernet7      172.16.1.18  4 65100             96        97    0    0 01:13:04 Estab   7      7
      s2-brdr1                 172.16.255.1 4 65203             27        26    0    0 00:14:19 Estab   11     11
    ```

2. From `s1-brdr1`, check its routing table in the default VRF and look for any prefixes learned from peer `172.16.255.1` via interface `Ethernet4`.  We will be looking for anything with a third octet of **.2** which signifies Site 2.

    ^^Command^^

    ``` text
    show ip route
    ```

    ^^Expected Output^^

    ``` text hl_lines="42-57 70-75"
    s1-brdr1#show ip route

    VRF: default
    Source Codes:
          C - connected, S - static, K - kernel,
          O - OSPF, IA - OSPF inter area, E1 - OSPF external type 1,
          E2 - OSPF external type 2, N1 - OSPF NSSA external type 1,
          N2 - OSPF NSSA external type2, B - Other BGP Routes,
          B I - iBGP, B E - eBGP, R - RIP, I L1 - IS-IS level 1,
          I L2 - IS-IS level 2, O3 - OSPFv3, A B - BGP Aggregate,
          A O - OSPF Summary, NG - Nexthop Group Static Route,
          V - VXLAN Control Service, M - Martian,
          DH - DHCP client installed default route,
          DP - Dynamic Policy Route, L - VRF Leaked,
          G  - gRIBI, RC - Route Cache Route,
          CL - CBF Leaked Route

    Gateway of last resort:
    S        0.0.0.0/0 [1/0]
              via 192.168.0.1, Management0

    B E      10.250.1.1/32 [200/0]
              via 172.16.1.16, Ethernet2
    B E      10.250.1.2/32 [200/0]
              via 172.16.1.18, Ethernet3
    B E      10.250.1.3/32 [200/0]
              via 172.16.1.16, Ethernet2
              via 172.16.1.18, Ethernet3
    B E      10.250.1.4/32 [200/0]
              via 172.16.1.16, Ethernet2
              via 172.16.1.18, Ethernet3
    B E      10.250.1.5/32 [200/0]
              via 172.16.1.16, Ethernet2
              via 172.16.1.18, Ethernet3
    B E      10.250.1.6/32 [200/0]
              via 172.16.1.16, Ethernet2
              via 172.16.1.18, Ethernet3
    C        10.250.1.7/32
              directly connected, Loopback0
    B I      10.250.1.8/32 [200/0]
              via 10.252.1.9, Vlan4093
    B E      10.250.2.1/32 [200/0]
              via 172.16.255.1, Ethernet4
    B E      10.250.2.2/32 [200/0]
              via 172.16.255.1, Ethernet4
    B E      10.250.2.3/32 [200/0]
              via 172.16.255.1, Ethernet4
    B E      10.250.2.4/32 [200/0]
              via 172.16.255.1, Ethernet4
    B E      10.250.2.5/32 [200/0]
              via 172.16.255.1, Ethernet4
    B E      10.250.2.6/32 [200/0]
              via 172.16.255.1, Ethernet4
    B E      10.250.2.7/32 [200/0]
              via 172.16.255.1, Ethernet4
    B E      10.250.2.8/32 [200/0]
              via 172.16.255.1, Ethernet4
    C        10.251.1.8/31
              directly connected, Vlan4094
    C        10.252.1.8/31
              directly connected, Vlan4093
    B E      10.255.1.3/32 [200/0]
              via 172.16.1.16, Ethernet2
              via 172.16.1.18, Ethernet3
    B E      10.255.1.5/32 [200/0]
              via 172.16.1.16, Ethernet2
              via 172.16.1.18, Ethernet3
    C        10.255.1.7/32
              directly connected, Loopback1
    B E      10.255.2.3/32 [200/0]
              via 172.16.255.1, Ethernet4
    B E      10.255.2.5/32 [200/0]
              via 172.16.255.1, Ethernet4
    B E      10.255.2.7/32 [200/0]
              via 172.16.255.1, Ethernet4
    C        172.16.1.16/31
              directly connected, Ethernet2
    C        172.16.1.18/31
              directly connected, Ethernet3
    C        172.16.255.0/31
              directly connected, Ethernet4
    C        192.168.0.0/24
              directly connected, Management0
    ```

3. From `s1-brdr2`, check the IPv4 underlay peering to its neighbor at Site 2, `s2-brdr2`.

    ^^Command^^

    ``` text
    show ip bgp summary
    ```

    ^^Expected Output^^

    ``` text hl_lines="9"
    s1-brdr2#show ip bgp summary
    BGP summary information for VRF default
    Router identifier 10.250.1.8, local AS number 65103
    Neighbor Status Codes: m - Under maintenance
      Description              Neighbor     V AS           MsgRcvd   MsgSent  InQ OutQ  Up/Down State   PfxRcd PfxAcc
      s1-brdr1                 10.252.1.8   4 65103            110       113    0    0 01:21:29 Estab   21     21
      s1-spine1_Ethernet8      172.16.1.20  4 65100            107       112    0    0 01:21:30 Estab   7      7
      s1-spine2_Ethernet8      172.16.1.22  4 65100            112       108    0    0 01:21:29 Estab   7      7
      s2-brdr2                 172.16.255.3 4 65203             36        36    0    0 00:22:45 Estab   11     11
    ```

???+ success "DCI Underlay Complete"

    If your BGP peerings match above and you have the correct routes in your routing table, the DCI network is successfully connected!

## Step 6 - Enable EVPN Gateway Functionality

Now that we have built and deployed our fabrics for both data centers, Site 1 and Site 2, we will need to enable EVPN gateway functionality on our border leafs so layer 2 and layer 3 traffic can move between the data centers across the EVPN overlay.

In order to do this, we will need to uncomment the necessary data model to enable EVPN gateway for the border leafs.

Below you will see the data model snippets from `sites/site_1/group_vars/SITE1_FABRIC.yml` and `sites/site_2/group_vars/SITE2_FABRIC.yml`, for the `S1_BRDR` and `S2_BRDR` node groups. To enable EVPN gateway functionality you will need to modify the `SITE1_FABRIC.yml` vars file, and uncomment the below highlighted sections.  Uncomment the same sections from the `SITE2_FABRIC.yml` vars file.

=== "SITE1_FABRIC.yml"

    ``` yaml hl_lines="3-8 14-18 23-27"
    - group: S1_BRDR
      bgp_as: 65103
      # evpn_gateway:
      #   evpn_l2:
      #     enabled: true
      #   evpn_l3:
      #     enabled: true
      #     inter_domain: true
      nodes:
        - name: s1-brdr1
          id: 5
          mgmt_ip: 192.168.0.100/24
          uplink_switch_interfaces: [ Ethernet7, Ethernet7 ]
          # evpn_gateway:
          #   remote_peers:
          #     - hostname: s2-brdr1
          #       bgp_as: 65203
          #       ip_address: 10.250.2.7
        - name: s1-brdr2
          id: 6
          mgmt_ip: 192.168.0.101/24
          uplink_switch_interfaces: [ Ethernet8, Ethernet8 ]
          # evpn_gateway:
          #   remote_peers:
          #     - hostname: s2-brdr2
          #       bgp_as: 65203
          #       ip_address: 10.250.2.8
    ```

=== "SITE2_FABRIC.yml"

    ``` yaml hl_lines="3-8 14-18 23-27"
    - group: S2_BRDR
      bgp_as: 65203
      # evpn_gateway:
      #   evpn_l2:
      #     enabled: true
      #   evpn_l3:
      #     enabled: true
      #     inter_domain: true
      nodes:
        - name: s2-brdr1
          id: 5
          mgmt_ip: 192.168.0.200/24
          uplink_switch_interfaces: [ Ethernet7, Ethernet7 ]
          # evpn_gateway:
          #   remote_peers:
          #     - hostname: s1-brdr1
          #       bgp_as: 65103
          #       ip_address: 10.250.1.7
        - name: s2-brdr2
          id: 6
          mgmt_ip: 192.168.0.201/24
          uplink_switch_interfaces: [ Ethernet8, Ethernet8 ]
          # evpn_gateway:
          #   remote_peers:
          #     - hostname: s1-brdr2
          #       bgp_as: 65103
          #       ip_address: 10.250.1.8
    ```

???+ note "Unified Fabric"

    If deploying a multi-site fabric with AVD, and using a single inventory file to contain all sites, the **evpn_gateway/remote_peers** vars for `bgp_as` and `ip_address` do **NOT** need to be populated. Since AVD will know about all these nodes from the single inventory file, it will know those variables and be able to use them to render the configuration.  Since we have split the sites for complexity sake, we do have to define them here.

### Build and Deploy Changes for EVPN Gateway Functionality

``` bash
make all
```

!!! note
    `make all` is a shortcut to run the build and deploy playbooks for both sites in one command. Once again, the make entries will run sequentially.

    ``` bash
    ########################################################
    # Build and deploy all sites
    ########################################################

    .PHONY: all
    all: build-site-1 build-site-2 deploy-site-1 deploy-site-2
    ```

### Verification

Now lets check and make sure the correct configurations were build and applied, and the EVPN gateways are functioning.

From nodes `s1-brdr1` and `s1-brdr2`, we can check the following show commands.

1. Verify the new BGP configurations were rendered and applied for the remote gateways.

    ^^Command^^

    ``` text
    show run section bgp
    ```

    Look for the below new configurations relevant to the EVPN gateways.

    === "s1-brdr1"

        ``` text
        router bgp 65103
          ...
          neighbor EVPN-OVERLAY-CORE peer group
          neighbor EVPN-OVERLAY-CORE update-source Loopback0
          neighbor EVPN-OVERLAY-CORE bfd
          neighbor EVPN-OVERLAY-CORE ebgp-multihop 15
          neighbor EVPN-OVERLAY-CORE send-community
          neighbor EVPN-OVERLAY-CORE maximum-routes 0
          ...
          neighbor 10.255.2.7 peer group EVPN-OVERLAY-CORE
          neighbor 10.255.2.7 remote-as 65203
          neighbor 10.255.2.7 description s2-brdr1
          ...
          vlan 10
              ...
              route-target import export evpn domain remote 10010:10010
              ...
          !
          vlan 20
              ...
              route-target import export evpn domain remote 10020:10020
              ...
          !
          address-family evpn
              neighbor EVPN-OVERLAY-CORE activate
              neighbor EVPN-OVERLAY-CORE domain remote
              ...
              neighbor default next-hop-self received-evpn-routes route-type ip-prefix inter-domain
        ```

    === "s1-brdr2"

        ``` text
        router bgp 65103
          ...
          neighbor EVPN-OVERLAY-CORE peer group
          neighbor EVPN-OVERLAY-CORE update-source Loopback0
          neighbor EVPN-OVERLAY-CORE bfd
          neighbor EVPN-OVERLAY-CORE ebgp-multihop 15
          neighbor EVPN-OVERLAY-CORE send-community
          neighbor EVPN-OVERLAY-CORE maximum-routes 0
          ...
          neighbor 10.255.2.8 peer group EVPN-OVERLAY-CORE
          neighbor 10.255.2.8 remote-as 65203
          neighbor 10.255.2.8 description s2-brdr2
          ...
          vlan 10
              ...
              route-target import export evpn domain remote 10010:10010
              ...
          !
          vlan 20
              ...
              route-target import export evpn domain remote 10020:10020
              ...
          !
          address-family evpn
              neighbor EVPN-OVERLAY-CORE activate
              neighbor EVPN-OVERLAY-CORE domain remote
              ...
              neighbor default next-hop-self received-evpn-routes route-type ip-prefix inter-domain
        ```

2. Verify the EVPN overlay peerings to Site 2.

    ^^Command^^

    ``` text
    show bgp evpn summary
    ```

    Look for the peerings to the corresponding Site 2 node.

    === "s1-brdr1"

        ``` text hl_lines="8"
        s1-brdr1#show bgp evpn summ
        BGP summary information for VRF default
        Router identifier 10.250.1.7, local AS number 65103
        Neighbor Status Codes: m - Under maintenance
          Description              Neighbor   V AS           MsgRcvd   MsgSent  InQ OutQ  Up/Down State   PfxRcd PfxAcc
          s1-spine1                10.250.1.1 4 65100            151       150    0    0 01:37:10 Estab   20     20
          s1-spine2                10.250.1.2 4 65100            152       151    0    0 01:37:11 Estab   20     20
          s2-brdr1                 10.250.2.7 4 65203             14        14    0    0 00:00:08 Estab   19     19
        ```

    === "s1-brdr2"

        ``` text hl_lines="8"
        s1-brdr2#show bgp evpn summary
        BGP summary information for VRF default
        Router identifier 10.250.1.8, local AS number 65103
        Neighbor Status Codes: m - Under maintenance
          Description              Neighbor   V AS           MsgRcvd   MsgSent  InQ OutQ  Up/Down State   PfxRcd PfxAcc
          s1-spine1                10.250.1.1 4 65100            158       152    0    0 01:38:37 Estab   20     20
          s1-spine2                10.250.1.2 4 65100            156       147    0    0 01:38:37 Estab   20     20
          s2-brdr2                 10.250.2.8 4 65203             15        15    0    0 00:01:35 Estab   19     19
        ```

3. Finally, lets verify which routes we are seeing in the EVPN table from Site 2.  If you recall when we checked this within each site, we had an **IMET** route per VLAN, from each VTEP.  In this instance, since we are using EVPN gateway functionality to summarize the routes from the other site, we should only see 1 **IMET** route per VLAN to the remote EVPN gateway.

    ^^Command^^

    ``` text
    show bgp evpn route-type imet
    ```

    ^^Expected Output^^

    ``` text hl_lines="50-53"
    s1-brdr1#show bgp evpn route-type imet
    BGP routing table information for VRF default
    Router identifier 10.250.1.7, local AS number 65103
    Route status codes: * - valid, > - active, S - Stale, E - ECMP head, e - ECMP
                        c - Contributing to ECMP, % - Pending best path selection
    Origin codes: i - IGP, e - EGP, ? - incomplete
    AS Path Attributes: Or-ID - Originator ID, C-LST - Cluster List, LL Nexthop - Link Local Nexthop

              Network                Next Hop              Metric  LocPref Weight  Path
    * >Ec    RD: 10.250.1.3:10010 imet 10.255.1.3
                                    10.255.1.3            -       100     0       65100 65101 i
    *  ec    RD: 10.250.1.3:10010 imet 10.255.1.3
                                    10.255.1.3            -       100     0       65100 65101 i
    * >Ec    RD: 10.250.1.3:10020 imet 10.255.1.3
                                    10.255.1.3            -       100     0       65100 65101 i
    *  ec    RD: 10.250.1.3:10020 imet 10.255.1.3
                                    10.255.1.3            -       100     0       65100 65101 i
    * >Ec    RD: 10.250.1.4:10010 imet 10.255.1.3
                                    10.255.1.3            -       100     0       65100 65101 i
    *  ec    RD: 10.250.1.4:10010 imet 10.255.1.3
                                    10.255.1.3            -       100     0       65100 65101 i
    * >Ec    RD: 10.250.1.4:10020 imet 10.255.1.3
                                    10.255.1.3            -       100     0       65100 65101 i
    *  ec    RD: 10.250.1.4:10020 imet 10.255.1.3
                                    10.255.1.3            -       100     0       65100 65101 i
    * >Ec    RD: 10.250.1.5:10010 imet 10.255.1.5
                                    10.255.1.5            -       100     0       65100 65102 i
    *  ec    RD: 10.250.1.5:10010 imet 10.255.1.5
                                    10.255.1.5            -       100     0       65100 65102 i
    * >Ec    RD: 10.250.1.5:10020 imet 10.255.1.5
                                    10.255.1.5            -       100     0       65100 65102 i
    *  ec    RD: 10.250.1.5:10020 imet 10.255.1.5
                                    10.255.1.5            -       100     0       65100 65102 i
    * >Ec    RD: 10.250.1.6:10010 imet 10.255.1.5
                                    10.255.1.5            -       100     0       65100 65102 i
    *  ec    RD: 10.250.1.6:10010 imet 10.255.1.5
                                    10.255.1.5            -       100     0       65100 65102 i
    * >Ec    RD: 10.250.1.6:10020 imet 10.255.1.5
                                    10.255.1.5            -       100     0       65100 65102 i
    *  ec    RD: 10.250.1.6:10020 imet 10.255.1.5
                                    10.255.1.5            -       100     0       65100 65102 i
    * >      RD: 10.250.1.7:10010 imet 10.255.1.7
                                    -                     -       -       0       i
    * >      RD: 10.250.1.7:10020 imet 10.255.1.7
                                    -                     -       -       0       i
    * >      RD: 10.250.1.7:10010 imet 10.255.1.7 remote
                                    -                     -       -       0       i
    * >      RD: 10.250.1.7:10020 imet 10.255.1.7 remote
                                    -                     -       -       0       i
    * >      RD: 10.250.2.7:10010 imet 10.255.2.7 remote
                                    10.255.2.7            -       100     0       65203 i
    * >      RD: 10.250.2.7:10020 imet 10.255.2.7 remote
                                    10.255.2.7            -       100     0       65203 i
    ```

> If all your peerings are established and you have the correct IMET routes in the EVPN table, then your EVPN gateways are functioning!  Lets move on to a final connectivity test.

## Final Fabric Test

At this point your full Layer 3 Leaf Spine with EVPN VXLAN and EVPN gateway functionality should be ready to go. Lets perform some final tests to verify everything is working.

From `s1-host1` ping both `s2-host1` & `s2-host2`.

``` bash
# s2-host1
ping 10.10.10.200
```

``` bash
# s2-host2
ping 10.20.20.200
```

???+ success "Great Success!"
    You have built a multi-site L3LS network with an EVPN/VXLAN overlay and EVPN Gateway functionality without touching the CLI on a single switch!

## Onto Day 2 Operations

[Continue to Day 2 Operations Guide](day2.md)