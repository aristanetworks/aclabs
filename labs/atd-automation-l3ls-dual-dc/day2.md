# Day 2 Operations

Our multi-site L3Ls network is working great. But, before too long, it will be time to change
our configurations. Lucky for us, that time is today!

## Cleaning Up

Before going any further, let's ensure we have a clean repo by committing the changes we've made
up to this point. The CLI commands below can accomplish this, but the VS Code Source Control GUI
can be used as well.

``` bash
git add .
git commit -m 'Your message here'
```

## Branching Out

Before jumping in and modifying our files, we'll create a branch named **banner-syslog** in our
forked repository to work on our changes. We can create our branch in multiple ways, but we'll use
the `git switch` command with the `-c` parameter to create our new branch.

``` bash
git switch -c banner-syslog
```

After entering this command, we should see our new branch name reflected in the terminal. It will also be
reflected in the status bar in the lower left-hand corner of our VS Code window (you may need to click the refresh icon
before this is shown).

Now we're ready to start working on our changes :sunglasses:.

## Login Banner

When we initially deployed our multi-site topology, we should have included a login banner on all our switches.
Let's take a look at the **[AVD documentation site](https://avd.arista.com/6.4/ansible_collections/arista/avd/roles/eos_designs/docs/data-models.html#other-management-settings)** to see what the
data model is for this configuration.

The banner on all of our switches will be the same. After reviewing the AVD documentation, we know we can accomplish this by defining the `banners` input variable
in our `global_vars/global_dc_vars.yml` file.

Add the code block below to `global_vars/global_dc_vars.yml`.

``` yaml
management_settings:
  banners:
    motd: You shall not pass. Unless you are authorized. Then you shall pass.
```

Next, let's build the configurations and documentation associated with this change.

``` bash
make build-site-1 build-site-2
```

Please take a minute to review the results of our five lines of YAML. When finished reviewing the changes, let's commit them.

As usual, there are a few ways of doing this, but the CLI commands below will get the job done:

``` bash
git add .
git commit -m 'add banner'
```

## Syslog Server

Our next Day 2 change is adding a syslog server configuration to all of our switches. Once again, we'll take a look at the `logging_settings` within the **[management settings](https://avd.arista.com/6.4/ansible_collections/arista/avd/roles/eos_designs/docs/data-models.html#logging)** data models.

Like our banner operation, the syslog server configuration will be consistent on all our switches. Because of this, we can also put this into
our `global_vars/global_dc_vars.yml` file.

Add the code block below to `global_vars/global_dc_vars.yml`.

``` yaml
# Syslog
logging_settings:
  hosts:
    - name: 10.200.0.108
    - name: 10.200.1.108
  vrfs:
    - name: default
```

Finally, let's build our configurations.

``` bash
make build-site-1 build-site-2
```

Take a minute, using the source control feature in VS Code, to review what has changed as a result
of our work.

TODO: Remove upstream push

At this point, we have our Banner and Syslog configurations in place. The configurations look good,
and we're ready to merge our branch to the main branch. Merging allows us to incorporate features or updates we are testing into our main branch.

There are a few ways to publish the `banner-syslog` branch to our forked repository. The commands below will
accomplish this via the CLI:

``` bash
git add .
git commit -m 'add syslog'
git switch main
git merge banner-syslog
```

We can now delete our now defunct **banner-syslog** branch.

``` bash
git branch -D banner-syslog
```

Finally, let's deploy our changes.

``` bash
make deploy-site-1 deploy-site-2
```

Once completed, we should see our banner when logging into any switch. The output of the `show logging` command
should also have our newly defined syslog servers.

## Adding additional VLANs

One of the many benefits of AVD is the ability to deploy new services very quickly and efficiently by modifying a small amount of data model. Lets add some new VLANs to our fabric.

For this we will need to modify the two `NETWORK_SERVICES.yml` data model vars files. To keep things simple we will add two new VLANs, **30** and **40**.

Copy the following pieces of data model, and paste right below the last VLAN entry, in both `SITE1_NETWORK_SERVICES.yml` and `SITE2_NETWORK_SERVICES.yml`.  Ensure the `-id:` entries all line up.

``` yaml
          - id: 30
            name: 'Thirty'
            enabled: true
            ip_address_virtual: 10.30.30.1/24
          - id: 40
            name: 'Forty'
            enabled: true
            ip_address_virtual: 10.40.40.1/24
```

When complete, your vars file should look like this.

``` yaml
---
tenants:
  - name: S2_FABRIC
    mac_vrf_vni_base: 10000
    vrfs:
      - name: OVERLAY
        vrf_vni: 10
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

``` bash
make all
```

### Verification

Now lets jump into one of the nodes, `s1-leaf1`, and check that our new VLAN SVIs were configured, as well as what we see in the VXLAN interface and EVPN table for both local and remote VTEPs.

1. Check that the VLAN SVIs were configured.

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
    Vlan30            10.30.30.1/24         up           up                 1500
    Vlan40            10.40.40.1/24         up           up                 1500
    Vlan1199          unassigned            up           up                 9164
    Vlan3009          10.252.1.0/31         up           up                 1500
    Vlan4093          10.252.1.0/31         up           up                 1500
    Vlan4094          10.251.1.0/31         up           up                 1500
    ```

2. Lets check the `VXLAN 1` interface and see what changes were made there.

    **Command**

    ``` text
    show run interface vxlan 1
    ```

    **Expected Output**

    ``` text
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

    ``` text
    show interface vxlan 1
    ```

    **Expected Output**

    ``` text
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

    ``` text
    show bgp evpn vni 10030
    ```

    **Expected Output**

    ``` text
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

    ``` text
    show bgp evpn vni 10040
    ```

    **Expected Output**

    ``` text
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

    ``` text
    show bgp evpn vni 10030
    ```

    **Expected Output**

    ``` text
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

    ``` text
    show bgp evpn vni 10040
    ```

    **Expected Output**

    ``` text
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

## Provisioning new Switches

Our network is gaining popularity, and it's time to add a new Leaf pair into the environment! **s1-leaf5** and **s1-leaf6**
are ready to be provisioned, so let's get to it.

### Branch Time

Before jumping in, let's create a new branch for our work. We'll call this branch **add-leafs**.

If you have pending changes to be committed, run `git add .` and `git commit` to save another snapshot.

``` bash
git switch -c add-leafs
```

Now that we have our branch created let's get to work!

### Inventory Update

First, we'll want to add our new switches, named **s1-leaf5** and **s1-leaf6**, into our inventory file. We'll add them
as members of the `SITE1_LEAFS` group.

Add the following two lines under `s1-brdr2` in `sites/site_1/inventory.yml`.

``` yaml
            s1-leaf5:
            s1-leaf6:
```

The `sites/site_1/inventory.yml` file should now look like the example below:

``` yaml hl_lines="21-22"
---
SITE1:
  children:
    CVP:
      hosts:
        cvp:
    SITE1_FABRIC:
      children:
        SITE1_SPINES:
          hosts:
            s1-spine1:
            s1-spine2:
        SITE1_LEAFS:
          hosts:
            s1-leaf1:
            s1-leaf2:
            s1-leaf3:
            s1-leaf4:
            s1-brdr1:
            s1-brdr2:
            s1-leaf5:
            s1-leaf6:
    SITE1_NETWORK_SERVICES:
      children:
        SITE1_SPINES:
        SITE1_LEAFS:
    SITE1_CONNECTED_ENDPOINTS:
      children:
        SITE1_SPINES:
        SITE1_LEAFS:
```

Next, let's add our new Leaf switches into `sites/site_1/group_vars/SITE1_FABRIC.yml`.

These new switches will go into **S1_RACK4**, leverage MLAG for multi-homing and use BGP ASN# **65104**.

Just like the other Leaf switches, interfaces `Ethernet2` and `Ethernet3` will be used to connect to the spines.

On the spines, interface `Ethernet9` will be used to connect to `s1-leaf5`, while `Ethernet10`
will be used to connect to `s1-leaf6`.

Add the following code block after the border nodes in `sites/site_1/group_vars/SITE1_FABRIC.yml`.

``` yaml
    - group: S1_RACK4
      bgp_as: 65104
      nodes:
        - name: s1-leaf5
          id: 7
          mgmt_ip: 192.168.0.28/24
          uplink_switch_interfaces: [ Ethernet9, Ethernet9 ]
        - name: s1-leaf6
          id: 8
          mgmt_ip: 192.168.0.29/24
          uplink_switch_interfaces: [ Ethernet10, Ethernet10 ]
```

The `sites/site_1/group_vars/SITE1_FABRIC.yml` file should now look like the example below:

``` yaml
---
fabric_name: SITE1_FABRIC

# Spine Switches
spine:
  defaults:
    platform: cEOS
    loopback_ipv4_pool: 10.250.1.0/24
    bgp_as: 65100
  nodes:
    - name: s1-spine1
      id: 1
      mgmt_ip: 192.168.0.10/24
    - name: s1-spine2
      id: 2
      mgmt_ip: 192.168.0.11/24

# Leaf Switches
l3leaf:
  defaults:
    platform: cEOS
    spanning_tree_priority: 4096
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
  node_groups:
    - group: S1_RACK1
      bgp_as: 65101
      nodes:
        - name: s1-leaf1
          id: 1
          mgmt_ip: 192.168.0.12/24
          uplink_switch_interfaces: [ Ethernet2, Ethernet2 ]
        - name: s1-leaf2
          id: 2
          mgmt_ip: 192.168.0.13/24
          uplink_switch_interfaces: [ Ethernet3, Ethernet3 ]
    - group: S1_RACK2
      bgp_as: 65102
      nodes:
        - name: s1-leaf3
          id: 3
          mgmt_ip: 192.168.0.14/24
          uplink_switch_interfaces: [ Ethernet4, Ethernet4 ]
        - name: s1-leaf4
          id: 4
          mgmt_ip: 192.168.0.15/24
          uplink_switch_interfaces: [ Ethernet5, Ethernet5 ]
    - group: S1_BRDR
      bgp_as: 65103
      evpn_gateway:
        evpn_l2:
          enabled: true
        evpn_l3:
          enabled: true
          inter_domain: true
      nodes:
        - name: s1-brdr1
          id: 5
          mgmt_ip: 192.168.0.100/24
          uplink_switch_interfaces: [ Ethernet7, Ethernet7 ]
          evpn_gateway:
            remote_peers:
              - hostname: s2-brdr1
                bgp_as: 65203
                ip_address: 10.255.2.7
        - name: s1-brdr2
          id: 6
          mgmt_ip: 192.168.0.101/24
          uplink_switch_interfaces: [ Ethernet8, Ethernet8 ]
          evpn_gateway:
            remote_peers:
              - hostname: s2-brdr2
                bgp_as: 65203
                ip_address: 10.255.2.8
    - group: S1_RACK4
      bgp_as: 65104
      nodes:
        - name: s1-leaf5
          id: 7
          mgmt_ip: 192.168.0.28/24
          uplink_switch_interfaces: [ Ethernet9, Ethernet9 ]
        - name: s1-leaf6
          id: 8
          mgmt_ip: 192.168.0.29/24
          uplink_switch_interfaces: [ Ethernet10, Ethernet10 ]
```

Next - Let's build the configuration!

``` bash
make build-site-1
```

> Interfaces `Ethernet9` and `Ethernet10` do not exist on the Spines. Because of this, we will **not** run a deploy command since it would fail.

Please take a moment and review the results of our changes via the source control functionality in VS Code.

Finally, we'll commit our changes to save the snapshot.

``` bash
git add .
git commit -m 'add leafs'
```

## Backing Out Changes

Ruh Roh. As it turns out, we should have added these leaf switches to an entirely new site. Oops! No worries, because
we used our **add-leafs** branch, we can switch back to our main branch and then delete our local copy of the **add-leafs**
branch. No harm or confusion related to this change ever hit the main branch!

``` bash
git switch main
git branch -D add-leafs
```

Congratulations. You have now successfully completed initial fabric builds and day 2 operational changes with AVD.
