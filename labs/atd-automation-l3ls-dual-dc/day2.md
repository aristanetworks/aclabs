# Day 2 Operations

Our multi-site L3LS network is working great. But, before too long, it will be time to change
our configurations. Lucky for us, that time is today!

## Cleaning Up

Before going any further, let's ensure we have a clean repo by committing the changes we've made
up to this point. The CLI commands below can accomplish this, but the VS Code Source Control GUI
can be used as well.

```bash
git add .
git commit -m 'Your message here'
```

## Login Banner

When we initially deployed our multi-site topology, we should have included a login banner on all our switches.
Let's take a look at the **[AVD documentation site](https://avd.arista.com/6.5/ansible_collections/arista/avd/roles/eos_designs/docs/data-models.html#other-management-settings)** to see what the
data model is for this configuration.

The banner on all of our switches will be the same. After reviewing the AVD documentation, we know we can accomplish this by defining the `banners` input variable
in our `global_vars/global_dc_vars.yml` file.

Add the code block below to `global_vars/global_dc_vars.yml`.

```yaml
management_settings:
  banners:
    motd: You shall not pass. Unless you are authorized. Then you shall pass.
```

Next, let's build the configurations and documentation associated with this change.

```bash
make build-site-1 build-site-2
```

Please take a minute to review the results of our five lines of YAML. When finished reviewing the changes, let's commit them.

As usual, there are a few ways of doing this, but the CLI commands below will get the job done:

```bash
git add .
git commit -m 'add banner'
```

## Syslog Server

Our next Day 2 change is adding a syslog server configuration to all of our switches. Once again, we'll take a look at the `logging_settings` within the **[management settings](https://avd.arista.com/6.5/ansible_collections/arista/avd/roles/eos_designs/docs/data-models.html#logging)** data models.

Like our banner operation, the syslog server configuration will be consistent on all our switches. Because of this, we can also put this into
our `global_vars/global_dc_vars.yml` file.

Add the code block below to [global_vars/global_dc_vars.yml](global_vars/global_dc_vars.yml).

```yaml
# Syslog
logging_settings:
  hosts:
    - name: 10.200.0.108
    - name: 10.200.1.108
```

Finally, let's build our configurations.

```bash
make build-site-1 build-site-2
```

Take a minute, using the source control feature in VS Code, to review what has changed as a result
of our work.

At this point, our banner and syslog configurations are in place. Commit these changes before deploying them:

```bash
git add .
git commit -m 'add syslog'
```

Finally, let's deploy our changes.

```bash
make deploy-site-1 deploy-site-2
```

Once completed, we should see our banner when logging into any switch. The output of the `show logging` command
should also have our newly defined syslog servers.

## Adding Additional VLANs

One of the many benefits of AVD is the ability to deploy new services very quickly and efficiently by modifying a small part of the data model. Lets add some new VLANs to our fabric.

For this we will need to modify the two `NETWORK_SERVICES.yml` data model variable files. To keep things simple we will add two new VLANs, **30** and **40**.

Copy the following data model entries and paste them directly below the last VLAN entry, in both [SITE1_NETWORK_SERVICES.yml](sites/site_1/group_vars/SITE1_NETWORK_SERVICES.yml) and [SITE2_NETWORK_SERVICES.yml](sites/site_2/group_vars/SITE2_NETWORK_SERVICES.yml).  Ensure the `-id:` entries all line up.

```yaml
          - id: 30
            name: 'Thirty'
            enabled: true
            ip_address_virtual: 10.30.30.1/24
          - id: 40
            name: 'Forty'
            enabled: true
            ip_address_virtual: 10.40.40.1/24
```

When complete, your variable files should look like this.


SITE1_NETWORK_SERVICES.yml:

```yaml
---
tenants:
  - name: DC_TENANT
    mac_vrf_vni_base: 10000
    vrfs:
      - name: OVERLAY
        vrf_vni: 10
        vtep_diagnostic:
          loopback: 10
          loopback_ip_range: 10.1.0.0/24
        svis:
          - id: 10
            name: 'Ten'
            enabled: true
            ip_address_virtual: 10.10.10.1/24
          - id: 20
            name: 'Twenty'
            enabled: true
            ip_address_virtual: 10.20.20.1/24
          - id: 30
            name: 'Thirty'
            enabled: true
            ip_address_virtual: 10.30.30.1/24
          - id: 40
            name: 'Forty'
            enabled: true
            ip_address_virtual: 10.40.40.1/24
```

SITE2_NETWORK_SERVICES.yml:

```yaml
---
tenants:
  - name: DC_TENANT
    mac_vrf_vni_base: 10000
    vrfs:
      - name: OVERLAY
        vrf_vni: 10
        vtep_diagnostic:
          loopback: 10
          loopback_ip_range: 10.2.0.0/24
        svis:
          - id: 10
            name: 'Ten'
            enabled: true
            ip_address_virtual: 10.10.10.1/24
          - id: 20
            name: 'Twenty'
            enabled: true
            ip_address_virtual: 10.20.20.1/24
          - id: 30
            name: 'Thirty'
            enabled: true
            ip_address_virtual: 10.30.30.1/24
          - id: 40
            name: 'Forty'
            enabled: true
            ip_address_virtual: 10.40.40.1/24
```

Finally, let's build and deploy our configurations.

```bash
make all
```

### Verification

Now lets jump into one of the nodes, `s1-leaf1`, and check that our new VLAN SVIs were configured, as well as what we see in the VXLAN interface and EVPN table for both local and remote VTEPs.

1. Check that the VLAN SVIs were configured.

    **Command**

    ```console
    show ip interface brief
    ```

    **Expected Output**

    ```console
    s1-leaf1#show ip interface brief
                                                                                    Address
    Interface         IP Address            Status       Protocol            MTU    Owner
    ----------------- --------------------- ------------ -------------- ----------- -------
    Ethernet2         172.16.1.1/31         up           up                 9214
    Ethernet3         172.16.1.3/31         up           up                 9214
    Loopback0         10.250.1.3/32         up           up                65535
    Loopback1         10.255.1.3/32         up           up                65535
    Loopback10        10.1.0.3/32           up           up                65535
    Management1       192.168.0.12/24       up           up                 1500
    Vlan10            10.10.10.1/24         up           up                 1500
    Vlan20            10.20.20.1/24         up           up                 1500
    Vlan30            10.30.30.1/24         up           up                 1500
    Vlan40            10.40.40.1/24         up           up                 1500
    Vlan3009          10.252.1.0/31         up           up                 9214
    Vlan4093          10.252.1.0/31         up           up                 9214
    Vlan4094          10.251.1.0/31         up           up                 9214
    Vlan4097          unassigned            up           up                 9164
    ```

2. Lets check the `VXLAN 1` interface and see what changes were made there.

    **Command**

    ```console
    show run interface vxlan 1
    ```

    **Expected Output**

    ```console
    s1-leaf1#show run interface vxlan 1
    interface Vxlan1
      description s1-leaf1_VTEP
      vxlan source-interface Loopback1
      vxlan virtual-router encapsulation mac-address mlag-system-id
      vxlan udp-port 4789
      vxlan vlan 10 vni 10010
      vxlan vlan 20 vni 10020
      vxlan vlan 30 vni 10030
      vxlan vlan 40 vni 10040
      vxlan vrf OVERLAY vni 10
    ```

    **Command**

    ```console
    show interface vxlan 1
    ```

    **Expected Output**

    ```console
    s1-leaf1#show interface vxlan 1
    Vxlan1 is up, line protocol is up (connected)
      Hardware is Vxlan
      Description: s1-leaf1_VTEP
      Source interface is Loopback1 and is active with 10.255.1.3
      Listening on UDP port 4789
      Replication/Flood Mode is headend with Flood List Source: EVPN
      Remote MAC learning via EVPN
      VNI mapping to VLANs
      Static VLAN to VNI mapping is
        [10, 10010]       [20, 10020]       [30, 10030]       [40, 10040]

      Dynamic VLAN to VNI mapping for 'evpn' is
        [1199, 10]
      Note: All Dynamic VLANs used by VCS are internal VLANs.
            Use 'show vxlan vni' for details.
      Static VRF to VNI mapping is
      [OVERLAY, 10]
      Headend replication flood vtep list is:
        10 10.255.1.5      10.255.1.7
        20 10.255.1.5      10.255.1.7
        30 10.255.1.5      10.255.1.7
        40 10.255.1.5      10.255.1.7
      MLAG Shared Router MAC is 021c.73c0.c612
    ```

3. Now, lets check the EVPN table. We can filter the routes to only the new VLANs by specifying the new VNIs, **10030** and **10040**.

    **Command**

    ```console
    show bgp evpn vni 10030
    ```

    **Expected Output**

    ```console
    s1-leaf1#sho bgp evpn vni 10030
    BGP routing table information for VRF default
    Router identifier 10.250.1.3, local AS number 65101
    Route status codes: * - valid, > - active, S - Stale, E - ECMP head, e - ECMP
                        c - Contributing to ECMP, % - Pending best path selection
    Origin codes: i - IGP, e - EGP, ? - incomplete
    AS Path Attributes: Or-ID - Originator ID, C-LST - Cluster List, LL Nexthop - Link Local Nexthop

              Network                Next Hop              Metric  LocPref Weight  Path
    * >      RD: 10.250.1.3:10030 imet 10.255.1.3
                                    -                     -       -       0       i
    * >Ec    RD: 10.250.1.5:10030 imet 10.255.1.5
                                    10.255.1.5            -       100     0       65100 65102 i
    *  ec    RD: 10.250.1.5:10030 imet 10.255.1.5
                                    10.255.1.5            -       100     0       65100 65102 i
    * >Ec    RD: 10.250.1.6:10030 imet 10.255.1.5
                                    10.255.1.5            -       100     0       65100 65102 i
    *  ec    RD: 10.250.1.6:10030 imet 10.255.1.5
                                    10.255.1.5            -       100     0       65100 65102 i
    * >Ec    RD: 10.250.1.7:10030 imet 10.255.1.7
                                    10.255.1.7            -       100     0       65100 65103 i
    *  ec    RD: 10.250.1.7:10030 imet 10.255.1.7
                                    10.255.1.7            -       100     0       65100 65103 i
    * >Ec    RD: 10.250.1.8:10030 imet 10.255.1.7
                                    10.255.1.7            -       100     0       65100 65103 i
    *  ec    RD: 10.250.1.8:10030 imet 10.255.1.7
                                    10.255.1.7            -       100     0       65100 65103 i
    ```

    **Command**

    ```console
    show bgp evpn vni 10040
    ```

    **Expected Output**

    ```console
    s1-leaf1#sho bgp evpn vni 10040
    BGP routing table information for VRF default
    Router identifier 10.250.1.3, local AS number 65101
    Route status codes: * - valid, > - active, S - Stale, E - ECMP head, e - ECMP
                        c - Contributing to ECMP, % - Pending best path selection
    Origin codes: i - IGP, e - EGP, ? - incomplete
    AS Path Attributes: Or-ID - Originator ID, C-LST - Cluster List, LL Nexthop - Link Local Nexthop

              Network                Next Hop              Metric  LocPref Weight  Path
    * >      RD: 10.250.1.3:10040 imet 10.255.1.3
                                    -                     -       -       0       i
    * >Ec    RD: 10.250.1.5:10040 imet 10.255.1.5
                                    10.255.1.5            -       100     0       65100 65102 i
    *  ec    RD: 10.250.1.5:10040 imet 10.255.1.5
                                    10.255.1.5            -       100     0       65100 65102 i
    * >Ec    RD: 10.250.1.6:10040 imet 10.255.1.5
                                    10.255.1.5            -       100     0       65100 65102 i
    *  ec    RD: 10.250.1.6:10040 imet 10.255.1.5
                                    10.255.1.5            -       100     0       65100 65102 i
    * >Ec    RD: 10.250.1.7:10040 imet 10.255.1.7
                                    10.255.1.7            -       100     0       65100 65103 i
    *  ec    RD: 10.250.1.7:10040 imet 10.255.1.7
                                    10.255.1.7            -       100     0       65100 65103 i
    * >Ec    RD: 10.250.1.8:10040 imet 10.255.1.7
                                    10.255.1.7            -       100     0       65100 65103 i
    *  ec    RD: 10.250.1.8:10040 imet 10.255.1.7
                                    10.255.1.7            -       100     0       65100 65103 i
    ```

4. Finally, lets check from `s1-brdr1` for the remote EVPN gateway.

    **Command**

    ```console
    show bgp evpn vni 10030
    ```

    **Expected Output**

    ```console
    s1-brdr1#  sho bgp evpn vni 10030
    BGP routing table information for VRF default
    Router identifier 10.250.1.7, local AS number 65103
    Route status codes: * - valid, > - active, S - Stale, E - ECMP head, e - ECMP
                        c - Contributing to ECMP, % - Pending best path selection
    Origin codes: i - IGP, e - EGP, ? - incomplete
    AS Path Attributes: Or-ID - Originator ID, C-LST - Cluster List, LL Nexthop - Link Local Nexthop

              Network                Next Hop              Metric  LocPref Weight  Path
    * >Ec    RD: 10.250.1.3:10030 imet 10.255.1.3
                                    10.255.1.3            -       100     0       65100 65101 i
    *  ec    RD: 10.250.1.3:10030 imet 10.255.1.3
                                    10.255.1.3            -       100     0       65100 65101 i
    * >Ec    RD: 10.250.1.4:10030 imet 10.255.1.3
                                    10.255.1.3            -       100     0       65100 65101 i
    *  ec    RD: 10.250.1.4:10030 imet 10.255.1.3
                                    10.255.1.3            -       100     0       65100 65101 i
    * >Ec    RD: 10.250.1.5:10030 imet 10.255.1.5
                                    10.255.1.5            -       100     0       65100 65102 i
    *  ec    RD: 10.250.1.5:10030 imet 10.255.1.5
                                    10.255.1.5            -       100     0       65100 65102 i
    * >Ec    RD: 10.250.1.6:10030 imet 10.255.1.5
                                    10.255.1.5            -       100     0       65100 65102 i
    *  ec    RD: 10.250.1.6:10030 imet 10.255.1.5
                                    10.255.1.5            -       100     0       65100 65102 i
    * >      RD: 10.250.1.7:10030 imet 10.255.1.7
                                    -                     -       -       0       i
    * >      RD: 10.250.1.7:10030 imet 10.255.1.7 remote
                                    -                     -       -       0       i
    * >      RD: 10.250.2.7:10030 imet 10.255.2.7 remote
                                    10.255.2.7            -       100     0       65203 i
    ```

    **Command**

    ```console
    show bgp evpn vni 10040
    ```

    **Expected Output**

    ```console
    s1-brdr1#  sho bgp evpn vni 10040
    BGP routing table information for VRF default
    Router identifier 10.250.1.7, local AS number 65103
    Route status codes: * - valid, > - active, S - Stale, E - ECMP head, e - ECMP
                        c - Contributing to ECMP, % - Pending best path selection
    Origin codes: i - IGP, e - EGP, ? - incomplete
    AS Path Attributes: Or-ID - Originator ID, C-LST - Cluster List, LL Nexthop - Link Local Nexthop

              Network                Next Hop              Metric  LocPref Weight  Path
    * >Ec    RD: 10.250.1.3:10040 imet 10.255.1.3
                                    10.255.1.3            -       100     0       65100 65101 i
    *  ec    RD: 10.250.1.3:10040 imet 10.255.1.3
                                    10.255.1.3            -       100     0       65100 65101 i
    * >Ec    RD: 10.250.1.4:10040 imet 10.255.1.3
                                    10.255.1.3            -       100     0       65100 65101 i
    *  ec    RD: 10.250.1.4:10040 imet 10.255.1.3
                                    10.255.1.3            -       100     0       65100 65101 i
    * >Ec    RD: 10.250.1.5:10040 imet 10.255.1.5
                                    10.255.1.5            -       100     0       65100 65102 i
    *  ec    RD: 10.250.1.5:10040 imet 10.255.1.5
                                    10.255.1.5            -       100     0       65100 65102 i
    * >Ec    RD: 10.250.1.6:10040 imet 10.255.1.5
                                    10.255.1.5            -       100     0       65100 65102 i
    *  ec    RD: 10.250.1.6:10040 imet 10.255.1.5
                                    10.255.1.5            -       100     0       65100 65102 i
    * >      RD: 10.250.1.7:10040 imet 10.255.1.7
                                    -                     -       -       0       i
    * >      RD: 10.250.1.7:10040 imet 10.255.1.7 remote
                                    -                     -       -       0       i
    * >      RD: 10.250.2.7:10040 imet 10.255.2.7 remote
                                    10.255.2.7            -       100     0       65203 i
    ```

## Filtering VLANs with Filter Tags

At the moment, any VLANs defined within network services will be configured on all relevant nodes. We can control where VLANs are deployed by leveraging filter tags. We can try and filter out VLANs 30 and 40 from being deployed to s1-leaf1.

We can start by assigning a tag to s1-leaf1. Add the following under the s1-leaf1 definition within [SITE1_FABRIC.yml](sites/site_1/group_vars/SITE1_FABRIC.yml):

```yaml
  node_groups:
    - group: S1_RACK1
      bgp_as: 65101
      nodes:
        - name: s1-leaf1
          id: 1
          mgmt_ip: 192.168.0.12/24
          uplink_switch_interfaces: [ Ethernet2, Ethernet2 ]
          filter:
            tags: [ "allow_ten" ]
```

We can then add the `allow_ten` tag to VLAN 10 within the [SITE1_NETWORK_SERVICES.yml](sites/site_1/group_vars/SITE1_NETWORK_SERVICES.yml) file:

```yaml
---
tenants:
  - name: DC_TENANT
    mac_vrf_vni_base: 10000
    vrfs:
      - name: OVERLAY
        vrf_vni: 10
        vtep_diagnostic:
          loopback: 10
          loopback_ip_range: 10.1.0.0/24
        svis:
          - id: 10
            name: 'Ten'
            enabled: true
            ip_address_virtual: 10.10.10.1/24
            tags: [ "allow_ten" ]
          - id: 20
            name: 'Twenty'
            enabled: true
            ip_address_virtual: 10.20.20.1/24
          - id: 30
            name: 'Thirty'
            enabled: true
            ip_address_virtual: 10.30.30.1/24
          - id: 40
            name: 'Forty'
            enabled: true
            ip_address_virtual: 10.40.40.1/24
```

We can now build, deploy, and validate our updates on s1-leaf1.

```console
make build-site-1 deploy-site-1
```

```console
s1-leaf1#show ip interface brief
                                                                                Address
Interface         IP Address            Status       Protocol            MTU    Owner
----------------- --------------------- ------------ -------------- ----------- -------
Ethernet2         172.16.1.1/31         up           up                 9214
Ethernet3         172.16.1.3/31         up           up                 9214
Loopback0         10.250.1.3/32         up           up                65535
Loopback1         10.255.1.3/32         up           up                65535
Loopback10        10.1.0.3/32           up           up                65535
Management1       192.168.0.12/24       up           up                 1500
Vlan10            10.10.10.1/24         up           up                 1500
Vlan3009          10.252.1.0/31         up           up                 9214
Vlan4093          10.252.1.0/31         up           up                 9214
Vlan4094          10.251.1.0/31         up           up                 9214
Vlan4097          unassigned            up           up                 9164
```

We can see the only VLAN deployed is 10.

### Filtering with VLANs Only in Use

We have seen how filter tags can be useful to control where network services are provisioned. In a much larger environment this can be tedious. The `only_vlans_in_use` filter creates VLANs and SVIs based on endpoint and downstream Layer 2 switch definitions managed by `eos_designs`, including usage on the MLAG peer. VRFs without retained services are also removed unless explicitly included. This is based on AVD inputs; learned MAC addresses and remote EVPN routes do not mark a VLAN as in use.

We can start by removing the tags we added in the network services file.

```yaml
---
tenants:
  - name: DC_TENANT
    mac_vrf_vni_base: 10000
    vrfs:
      - name: OVERLAY
        vrf_vni: 10
        vtep_diagnostic:
          loopback: 10
          loopback_ip_range: 10.1.0.0/24
        svis:
          - id: 10
            name: 'Ten'
            enabled: true
            ip_address_virtual: 10.10.10.1/24
          - id: 20
            name: 'Twenty'
            enabled: true
            ip_address_virtual: 10.20.20.1/24
          - id: 30
            name: 'Thirty'
            enabled: true
            ip_address_virtual: 10.30.30.1/24
          - id: 40
            name: 'Forty'
            enabled: true
            ip_address_virtual: 10.40.40.1/24
```

We can then remove the filter from s1-leaf1 and add the `only_vlans_in_use` filter at the node type defaults section.

```yaml
...
# Leaf Switches
l3leaf:
  defaults:
    platform: cEOS
    spanning_tree_mode: mstp
    loopback_ipv4_pool: 10.250.1.0/24
    loopback_ipv4_offset: 2
    vtep_loopback_ipv4_pool: 10.255.1.0/24
    uplink_switches: [ s1-spine1, s1-spine2 ]
    uplink_interfaces: [ Ethernet2, Ethernet3 ]
    uplink_ipv4_pool: 172.16.1.0/24
    mlag_interfaces: [ Ethernet1, Ethernet6 ]
    mlag_peer_ipv4_pool: 10.251.1.0/24
    mlag_peer_l3_ipv4_pool: 10.252.1.0/24
    virtual_router_mac_address: 00:1c:73:00:00:99
    filter:
      only_vlans_in_use: true
...
```

```bash
make build-site-1 deploy-site-1
```

We can now connect to s1-leaf3 and view the difference.

```console
s1-leaf3#show ip interface brief
                                                                                Address
Interface         IP Address            Status       Protocol            MTU    Owner
----------------- --------------------- ------------ -------------- ----------- -------
Ethernet2         172.16.1.9/31         up           up                 9214
Ethernet3         172.16.1.11/31        up           up                 9214
Loopback0         10.250.1.5/32         up           up                65535
Loopback1         10.255.1.5/32         up           up                65535
Loopback10        10.1.0.5/32           up           up                65535
Management1       192.168.0.14/24       up           up                 1500
Vlan20            10.20.20.1/24         up           up                 1500
Vlan3009          10.252.1.4/31         up           up                 9214
Vlan4093          10.252.1.4/31         up           up                 9214
Vlan4094          10.251.1.4/31         up           up                 9214
Vlan4097          unassigned            up           up                 9164
```

We can see VLAN 20 is the only defined SVI that was provisioned for s1-leaf3 since there is an endpoint with that service defined in our connected endpoints file.

```yaml
  - name: s1-host2                                      # Server name
    rack: RACK2                                         # Informational RACK (optional)
    adapters:
      - endpoint_ports: [ eth1, eth2 ]                  # Server port to connect (optional)
        switch_ports: [ Ethernet4, Ethernet4 ]          # Switch port to connect server (required)
        switches: [ s1-leaf3, s1-leaf4 ]                # Switch to connect server (required)
        profile: PP-VLAN20                              # Port profile to apply (required)
        port_channel:
          mode: active
```

## Changing EVPN RD/RT Values with mac_vrf_vni_base

Our network architect has another request: move the tenant's Layer 2 service identifiers into the **20000** range so they follow the organization's allocation plan. We will change `mac_vrf_vni_base` and see how AVD updates the Route Distinguishers (RDs), Route Targets (RTs), and VXLAN VNIs across both sites.

An **RD** makes an EVPN route unique, while an **RT** controls which EVPN instances import that route. In this lab, AVD derives each VLAN's MAC-VRF VNI by adding the VLAN ID to `mac_vrf_vni_base`. With our existing default RD/RT settings and no overrides, AVD also uses that result for the RD's second field and both fields of the RT:

```text
MAC-VRF VNI = mac_vrf_vni_base + VLAN ID
RD          = router ID:MAC-VRF VNI
RT          = MAC-VRF VNI:MAC-VRF VNI
```

Changing this base updates the Layer 2 VNIs as well as the VLAN RD/RT values. The `OVERLAY` VRF's Layer 3 VNI remains `10` because its `vrf_vni` setting is separate.

### Prepare the VLANs for This Exercise

If you completed the `only_vlans_in_use` exercise, set `l3leaf.defaults.filter.only_vlans_in_use` to `false` in [SITE1_FABRIC.yml](sites/site_1/group_vars/SITE1_FABRIC.yml), or remove that filter. This restores all defined VLANs on the Site 1 leaves and border leaves so we can compare their generated configurations. The earlier tag filter should already have been removed.

### Update Both Network Services Files

In [SITE1_NETWORK_SERVICES.yml](sites/site_1/group_vars/SITE1_NETWORK_SERVICES.yml), change the existing tenant's `mac_vrf_vni_base` from `10000` to `20000`:

```yaml
tenants:
  - name: DC_TENANT
    mac_vrf_vni_base: 20000
    # Keep the existing VRFs and SVIs below this line.
```

Make the same change in [SITE2_NETWORK_SERVICES.yml](sites/site_2/group_vars/SITE2_NETWORK_SERVICES.yml):

```yaml
tenants:
  - name: DC_TENANT
    mac_vrf_vni_base: 20000
    # Keep the existing VRFs and SVIs below this line.
```

Edit only the existing base value in each tenant; retain the VLANs, SVI addresses, and `vrf_vni: 10`. Both sites need matching RTs and VNI mappings for the services we extend between them.

For VLAN 10 on `s1-leaf1`, the expected changes are:

| Setting | Before | After |
| --- | --- | --- |
| Layer 2 VNI | `10010` | `20010` |
| RD | `10.250.1.3:10010` | `10.250.1.3:20010` |
| Import/export RT | `10010:10010` | `20010:20010` |

VLANs 20, 30, and 40 will similarly use `20020`, `20030`, and `20040` for their Layer 2 VNIs and RD suffixes. Their RTs become `20020:20020`, `20030:20030`, and `20040:20040`. Each switch retains its own router ID in the RD.

### Build and Compare the Configurations

Build both sites:

```bash
make build-site-1 build-site-2
```

Use VS Code Source Control to review the differences. In [s1-leaf1.cfg](sites/site_1/intended/configs/s1-leaf1.cfg), the VLAN 10 section under `router bgp 65101` should now contain:

```text
   vlan 10
      rd 10.250.1.3:20010
      route-target both 20010:20010
      redistribute learned
```

Under `interface Vxlan1`, check the updated VLAN mappings:

```text
   vxlan vlan 10 vni 20010
   vxlan vlan 20 vni 20020
   vxlan vlan 30 vni 20030
   vxlan vlan 40 vni 20040
   vxlan vrf OVERLAY vni 10
```

Review the Site 2 configurations as well. For example, `s2-leaf1` should have RD `10.250.2.3:20010` and RT `20010:20010` for VLAN 10. The RDs identify routes from different switches, while the matching RT allows the same service to import them.

On [s1-brdr1.cfg](sites/site_1/intended/configs/s1-brdr1.cfg), also check the VLAN 10 RT used by the EVPN gateway's remote domain:

```text
      route-target import export evpn domain remote 20010:20010
```

Check the corresponding remote-domain RTs on the other border leaves. The `OVERLAY` VRF's RD suffix, RT, and Layer 3 VNI should retain their original values based on `vrf_vni: 10`.

### Deploy and Verify the New Values

Once both sites' generated configurations agree, deploy the change:

```bash
make deploy-site-1 deploy-site-2
```

Expect an interruption to the affected services while the switches transition to the new RTs and VNIs. The services can use the new identifiers once the participating switches in both sites have been updated and EVPN has converged.

Connect to `s1-leaf1` and inspect the deployed configuration and EVPN routes:

```console
show running-config section router bgp
show running-config interface Vxlan1
show bgp evpn vni 20010 detail
```

Confirm that VLAN 10 maps to VNI `20010`, the local VLAN 10 RD is `10.250.1.3:20010`, and the RT is `20010:20010`. The EVPN routes should show the new RD suffixes and RTs; routes originated by other switches will have their own router IDs in the RDs. Repeat these checks on `s2-leaf1`, then check the remote-domain RTs on the border leaves.

Finally, validate both sites and review endpoint reachability:

```bash
make validate-site-1 validate-site-2
```

After reviewing the validation reports, save the change:

```bash
git add .
git commit -m 'update tenant MAC-VRF VNI base and RD/RT values'
```

## Introducing IPv6 in the Underlay with RFC 5549

During our next design review, the network architect has a request: simplify addressing on the leaf-to-spine links and introduce IPv6 into the underlay. As the fabric grows, assigning an IPv4 subnet to every point-to-point link adds work. The architect would like us to use **RFC 5549** so these links can use IPv6 link-local addresses while continuing to advertise IPv4 routes.

With AVD's RFC 5549 design, the underlay eBGP sessions use IPv6 link-local addresses, and IPv4 routes are advertised with IPv6 next hops. Our router-ID and VTEP loopbacks keep their IPv4 addresses, and the EVPN overlay continues to use its existing IPv4 peers. Let's use AVD to make this change across both sites.

### Update the Global Variables

Open [global_vars/global_dc_vars.yml](global_vars/global_dc_vars.yml) and add `underlay_rfc5549: true` immediately below the underlay and overlay routing protocol settings. Keep all three keys at the top level:

```yaml
underlay_routing_protocol: ebgp
overlay_routing_protocol: ebgp
underlay_rfc5549: true
```

Because this file is shared, the setting applies to the spines, leaves, and border leaves in both sites. The existing eBGP underlay meets the requirement for this AVD setting. IPv6 link-local addresses are generated automatically, so we do not need to define an IPv6 address pool for these links.

### Build and Review Both Sites

Generate the configurations before deploying the change:

```bash
make build-site-1 build-site-2
```

Use VS Code Source Control to review the changes in both sites' `intended/configs/` directories. Start with [s1-leaf1.cfg](sites/site_1/intended/configs/s1-leaf1.cfg). Its `Ethernet2` and `Ethernet3` uplinks should now use `ipv6 enable` in place of their IPv4 `/31` addresses. For example:

```text
interface Ethernet2
   description P2P_s1-spine1_Ethernet2
   no shutdown
   mtu 9214
   no switchport
   ipv6 enable
```

The BGP configuration should now define the underlay peers by interface. Under the IPv4 address family, AVD enables IPv6 next hops. The relevant excerpt from `s1-leaf1.cfg` should look like this:

```text
router bgp 65101
   neighbor interface Ethernet2 peer-group IPv4-UNDERLAY-PEERS remote-as 65100
   neighbor interface Ethernet3 peer-group IPv4-UNDERLAY-PEERS remote-as 65100
   !
   address-family ipv4
      neighbor IPv4-UNDERLAY-PEERS activate
      neighbor IPv4-UNDERLAY-PEERS next-hop address-family ipv6 originate
```

The peer-group name remains `IPv4-UNDERLAY-PEERS` because these peers exchange IPv4 routes. Check the corresponding spine configurations and the Site 2 configurations as well. Confirm that the IPv4 router-ID and VTEP loopbacks are still present.

### Deploy the Change

Once the generated configurations look correct, deploy both sites:

```bash
make deploy-site-1 deploy-site-2
```

The underlay sessions will reestablish as the switches transition to interface-based IPv6 peering. Expect a brief interruption while the peers at both ends of each link are updated.

### Verify IPv6 Peering and IPv4 Reachability

Connect to `s1-leaf1` and check the uplinks and their IPv6 neighbors:

```console
show ipv6 interface Ethernet2
show ipv6 interface Ethernet3
show ipv6 neighbors
```

Both uplinks should have IPv6 link-local addresses beginning with `fe80::`. The neighbor table should show the attached spine neighbors on these interfaces. The exact link-local addresses depend on the devices.

Next, check the IPv4 BGP address family and a route to the remote VTEP on the other leaf pair:

```console
show ip bgp summary
show ip route 10.255.1.5
```

The underlay BGP peers should be established over IPv6 link-local addresses. The route to `10.255.1.5/32` should use IPv6 link-local next hops through the spine uplinks. This is the key result: an IPv4 destination is reachable through IPv6 next hops.

Check that the EVPN overlay has also recovered:

```console
show bgp evpn summary
```

The EVPN sessions to `10.250.1.1` and `10.250.1.2` should be established. Repeat these checks on `s2-leaf1`, using `10.255.2.5` for the remote VTEP route and `10.250.2.1` and `10.250.2.2` for the EVPN peers.

Finally, run the existing ANTA validation for both sites to check the deployed fabric and endpoint reachability:

```bash
make validate-site-1 validate-site-2
```

Review the reports, then save the completed scenario:

```bash
git add .
git commit -m 'enable RFC 5549 underlay'
```

Congratulations. You have now successfully completed initial fabric builds and day 2 operational changes with AVD.
