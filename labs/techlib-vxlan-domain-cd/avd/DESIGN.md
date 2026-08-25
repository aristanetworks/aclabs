# AVD data models — techlib EVPN-VXLAN Deployment Guide, Domains C + D

> AVD **6.3.0** data models that render the lab's startup configurations
> (`startup-configs/clab-arista-evpn-dg-domain-cd/*/startup-config`), which
> in turn mirror the [Domains C & D deployment guide](https://tech-library.arista.com/data_center/evpnvxlan/deployment_guide/domains_c_d/overview/).
>
> Goals, in order — the same contract as the Domain A + B models
> (`labs/techlib-vxlan-domain-ab/avd`): (1) functionally equivalent
> configuration, (2) as little node-specific data as the design allows,
> (3) native AVD keys before structured config, structured config before
> raw CLI. Cosmetic differences (descriptions, ordering, EOS defaults AVD
> writes out explicitly) are accepted and listed below so nothing is
> silently different.

## Toolchain

```bash
python3 -m venv .venv && . .venv/bin/activate
pip install "pyavd[ansible]==6.3.0"
ansible-galaxy collection install "arista.avd:==6.3.0"
```

From the lab root (`labs/techlib-vxlan-domain-cd`):

| Command | What it does |
|---|---|
| `make build` | Renders all three fabrics into `avd/intended/configs/*.cfg` (`build-c`, `build-d`, `build-bb` per fabric) |
| `make parity` | Compares every rendered config with the lab's startup-config and refreshes `avd/PARITY-STATUS.md` |
| `make parity-node NODE=C-LEAF7` | Full missing/extra listing for one node |
| `make deploy` / `make validate` | Push via eAPI / run the ANTA auto-catalogs (`deploy-*`, `validate-*` per fabric) |

Each fabric is its own play because `fabric_name` must be uniform per play.

## Layout

```
avd/
├── inventory.yml                     # fabrics + role groups — no data
├── group_vars/
│   ├── all.yml                       # connectivity, cEOS platform profile, management preamble, BFD timers
│   ├── DCI.yml                       # the nine IPv6 inter-domain p2p links, defined once
│   ├── DOMAIN_C_FABRIC/
│   │   ├── fabric.yml                # IPv6 underlay/overlay, spines, MLAG pods, Gateway pair
│   │   ├── services.yml              # tenant: VRFs, SVIs, IPv4 OISM, MLAG VRF peering
│   │   └── endpoints.yml             # port profiles + hosts
│   ├── DOMAIN_C_LEAFS.yml            # role: standard (MLAG + OISM) leaf
│   ├── DOMAIN_C_GATEWAYS.yml         # role: Gateway (no MLAG, no OISM)
│   ├── DOMAIN_D_FABRIC/{fabric,services,endpoints}.yml
│   ├── DOMAIN_D_LEAFS.yml / DOMAIN_D_GATEWAYS.yml / DOMAIN_D_L2_SWITCHES.yml
│   └── BACKBONE.yml                  # BB1/BB2: IS-IS SR-MPLS + EVPN-MPLS route reflectors
├── playbooks/{build,deploy,validate}.yml
├── scripts/parity_report.py          # rendered-vs-target report (`make parity`)
├── PARITY-STATUS.md                  # `make parity` output
└── intended/, documentation/         # build output (git-ignored)
```

No `host_vars/`. The model is ~2,000 lines including comments.

## How the model is organised

**Fabric files hold the design; role files hold the switches.** Everything
that differs between a standard leaf and a Gateway that AVD cannot derive on
its own is a *role* setting in `group_vars/<ROLE>.yml`: `evpn_multicast` and
`underlay_multicast_pim_sm` (Domain C), the OISM source-loopback pod, the
IPv6-multicast and Multi-VTEP additions, and one boolean, `standard_leaf`.
That boolean gates the MLAG/OISM hooks in the fabric and services models with
plain Jinja: `"{{ x if standard_leaf else none }}"` for scalars and for
dict keys that eos_cli_config_gen renders as a stanza of their own
(`address_family_ipv4`, `layer_2_fec_in_place_update`, `raw_eos_cli` —
`none`, not `{}`, because an empty dict there renders an empty
`address-family ipv4` header), `{}` for the merge-only
`structured_config` inputs of the services model (an empty dict merges
nothing), and `[]` for lists. This is ordinary Ansible variable precedence,
not merge tricks.

> Vars placed *inside* `inventory.yml` rank below `group_vars/` files in
> Ansible's precedence and cannot override a fabric-level setting — hence
> the small per-role files.

**The IPv6-only fabric is AVD's, the link-local underlay is ours.** AVD 6.3's
`underlay_ipv6_numbered` renders the IPv6 loopbacks and VTEP, `vxlan
encapsulation ipv6`, the IPv4 BGP router-id from `router_id_pool`, EVPN
peering over IPv6 and the IPv6 MLAG peer link natively. What it cannot
express is the guide's link-local BGP underlay (`ipv6 enable` + `neighbor
interface … peer-group …` with no addresses on the links): every AVD uplink
would be numbered from a pool and given a numbered neighbor, and the
link-local option (`underlay_rfc5549`) is refused in that mode. So the leafs
carry **no AVD uplinks**. The fabric links and the underlay BGP are stated
once per role in structured config — the cabling is uniform (leaf
Ethernet*n* faces SPINE*n*, spine Ethernet*n* faces LEAF*n*), the spines are
named as EVPN route servers explicitly (`evpn_route_servers`), and no node
carries anything for it.

**Per-node data is identity only.** Every node entry carries `id` and
`mgmt_ip` — and nothing else, except the values below, each forced by the
guide's design:

| Where | Value | Why it cannot be derived |
|---|---|---|
| C-LEAF1..6 | `vtep_loopback_ipv6_address` | Multi-VTEP MLAG: each leaf's *unique* VTEP is Loopback1 (`2001:db8:c1::<id>`); AVD's MLAG model derives the VTEP from the pair's primary id. |
| C-LEAF7/8, D-LEAF7/8 | `structured_config.loopback_interfaces` (Loopback3 address + SR node index) and `structured_config.router_isis` (`net`, `router_id`) | The Gateway's identity in the backbone IGP — a second IS-IS instance next to the fabric's BGP underlay, which AVD cannot model. |
| D-LEAF3 / D-LEAF4 | `filter.tags` | The pair is asymmetric by design (VLAN 60 Red on D-LEAF3, VLAN 70 Brown on D-LEAF4). |

The Gateway ASNs are *not* per-node: `l3leaf.defaults.bgp_as:
'65301-65308'` is indexed by node id (for an MLAG pair, by the primary's
id), which yields 65301/65303/65305 per pod and 65307/65308 on the two
standalone Gateways. Domain D is one ASN (65400) throughout. The spines'
`::201`-style loopbacks are the hex reading of their ids: `loopback_ipv6_offset:
312` (201 + 312 = 513 = 0x201).

Per-pod (node-group) values: the pod's VLAN set (`filter.tags`), the Domain C
shared-VTEP Loopback2 address, the spanning-tree exclusion list for the
pod's MLAG peering VLANs, `ip routing ipv6 interfaces` for the pod's VRFs,
and the pair's Vlan4093 `neighbor interface` line (it has to carry the
pair's ASN — see the AVD gap below). The DCI links live in
`group_vars/DCI.yml`, once.

Two values are derived rather than stated: the I-ESI DF preference from the
hostname (C-LEAF7 / D-LEAF7 win), and the host part of the per-VRF MLAG
neighbor from the node-group order — AVD makes the first node listed in a
node group the MLAG primary and gives it `::1`, so the primary peers with
`::2` and the secondary with `::1` (see the AVD gap below).

## The three fabrics

**Domain C** — IPv6-only underlay with link-local eBGP (spines 65300 with a
`LEAF-AS-RANGE` peer filter, one ASN per MLAG pair), eBGP EVPN between the
IPv6 Loopback0s, VXLAN-in-IPv6, MLAG pairs with Multi-VTEP MLAG (unique
Loopback1, shared Loopback2 from `2001:db8:c2::<pair>`), IPv4 OISM in PROD
(VLAN 10, 30) and DEV (VLAN 50, 70) over an IPv6 PIM underlay (SSM groups
`ff3e::1` / `ff3e::2`), All-Active Gateway pair towards the MPLS backbone
(dual I-ESI `0000:cccc:0007:0008:000{1,2}`, D-PATH `3:3` / `99:99`).

**Domain D** — the same IPv6-only underlay with link-local iBGP in AS 65400
(the spines reflect underlay and overlay, cluster-id `10.0.4.205`,
`next-hop-self` on the underlay group), no MLAG — EVPN All-Active
multihoming everywhere with LACP-derived ESIs and `spanning-tree root
super`, no OISM, PROD (VLAN 10, 20, 40) and DEV (VLAN 60, 70, 80), All-Active
Gateway pair (I-ESI `0000:dddd:0007:0008:000{1,2}`, D-PATH `4:4` / `99:99`),
D-SW1 as an L2-only switch dual-homed to D-LEAF5/6 over an All-Active
segment.

**Backbone** — BB1/BB2 in AS 65000: IPv6 IS-IS SR-MPLS transport (instance
`BACKBONE`, level-2, TI-LFA node protection, node SIDs 1/2) and EVPN-MPLS
route reflectors for the four Gateways (static neighbors to their Loopback3s,
`encapsulation mpls next-hop-self`). Modelled as AVD `spine` nodes with an
`isis-sr` underlay — made MPLS label switch routers with one
`custom_node_type_keys` entry — and an iBGP overlay whose peers are listed in
structured config, because AVD only materialises RR peers it can see in the
same fabric.

The Gateways join the backbone as iBGP from the backbone's point of view
(`local-as 65000 no-prepend replace-as` on `REMOTE-EVPN-MPLS-PEERS`), sourced
from Loopback3, with `encapsulation mpls`.

## Where each guide feature comes from

| Guide feature | Mechanism |
|---|---|
| IPv6-only loopbacks and VTEP, `vxlan encapsulation ipv6`, BGP `router-id` without an IPv4 address, EVPN peering over IPv6 | Native `underlay_ipv6_numbered` + `underlay_ipv6` with `loopback_ipv6_pool`, `vtep_loopback_ipv6_pool`, `router_id_pool` |
| Link-local BGP underlay: `ipv6 enable` on the fabric links, `neighbor interface Ethernet<n> peer-group LOCAL-IPV6-PEERS remote-as 65300` (C leafs), `… peer-filter LEAF-AS-RANGE` (C spines), the `address-family ipv6` activation, `redistribute connected route-map RM-CONN-2-BGP` under `address-family ipv6`, `PL6-LOOPBACKS` | **Structured config per role** — no AVD uplinks (see above); `underlay_filter_redistribute_connected: false` plus a CSC null remove AVD's own `redistribute connected` at the `router bgp` level |
| Domain D's `neighbor interface Ethernet<n> peer-group LOCAL-IPV6-PEERS` (remote-as on the group) and Domain C's Vlan4093 line | Structured `neighbor_interfaces` carrying the group's ASN as well — eos_cli_config_gen only renders `neighbor interface` together with a `remote-as` or a `peer-filter`. Raw CLI is not an option: `router_bgp.eos_cli` renders after the VRF stanzas, where EOS would attach a `neighbor interface` line to the last VRF |
| `ipv6 nd ra interval 5` on every link-local peering interface | **Raw CLI** (interface `eos_cli`) — no AVD 6.3 key |
| Peer tagging on the C leafs (`peer-tag in/out discard SPINES`) | Native cli keys via `l3leaf.defaults.structured_config` (leaf-only on purpose — on a spine the same tags would discard leaf routes) |
| D spines as underlay route reflectors (`remote-as 65400`, `next-hop-self`, `route-reflector-client` on LOCAL-IPV6-PEERS) | Structured config on the spine role |
| MLAG over IPv6 (Vlan4094 `2001:db8:4094::1/::2`, `peer-address`) | Native `mlag_peer_address_family: ipv6` + `mlag_peer_ipv6_pool` with `fabric_ip_addressing.mlag.algorithm: same_subnet` — AVD numbers the pair `::1` / `::2`, exactly as the guide |
| Vlan4093 link-local MLAG L3 peering (`ipv6 enable`, `no autostate`, `neighbor interface Vlan4093 peer-group MLAG-IPV6-PEER`, `address-family ipv4 … next-hop address-family ipv6 originate`) | Native L3 peering SVI with its pool address stripped (`mlag_peer_l3_vlan_structured_config: ipv6_addresses: null`); AVD's numbered neighbor emptied (both `::1` / `::2` candidates, so no node needs to know its side, and `validate_state: false` keeps them out of ANTA); the neighbor-interface line per pod with the pair's ASN; the IPv4 activation structured |
| Per-VRF MLAG peering (Vlan3001/3002 `2001:db8:300x::1/::2`, the VRF neighbor, `MLAG_PEER_VRF_<vrf>` VLAN names) | Native `mlag_ibgp_peering_vlan` + `mlag_ibgp_peering_ipv6_pool`; the neighbor replaced by the peer address derived from the node-group order (AVD gap below); `ipv6 enable`, `mtu 9014`, `no autostate` via the VRF's structured config, gated on `standard_leaf` |
| `RM-CONN-2-BGP-VRFS` + `PL6-MLAG-PEER-VRFS`, `RM-MLAG-PEER-OUT` + the `evpn-imported` extcommunity list | CSC objects on the MLAG leafs; AVD's own peering-subnet filter switched off with `redistribute_mlag_ibgp_peering_vrfs: true` (AVD gap below); `mlag_ibgp_origin_incomplete: false` + `bgp_peer_groups.mlag_ipv4_underlay_peer.structured_config.route_map_out` |
| `ip routing ipv6 interfaces vrf <vrf>` on the MLAG leafs | Structured `vrfs[]` per pod (it takes precedence over `ip routing vrf`) |
| Multi-VTEP MLAG (`vxlan mlag source-interface Loopback2`) | AVD 6.3 enables Multi-VTEP automatically for MLAG + OISM but sources the unique VTEP from Loopback0 and the shared one from the VTEP loopback; the guide's Loopback1/Loopback2 layout is a `source_interface: Loopback1` override (fabric.yml), a `mlag_source_interface: Loopback2` override (the leaf role file) and a per-pod Loopback2 |
| IPv4 OISM (`ip igmp`, `pim ipv4 sparse-mode`, `pim ipv4 local-interface Loopback10x`, `vxlan vrf … multicast group ff3e::x`, `router multicast vrf … ipv4 routing`, `evpn multicast`) | Native `evpn_l3_multicast` (the IPv6 group is accepted as-is) + `vtep_diagnostic.loopback_ip_pools` keyed by `pod_name`; `ip igmp` via the SVI profile's structured config; `address-family ipv4` under `evpn multicast` **raw CLI** |
| IPv6 PIM underlay (`pim ipv6 sparse-mode` on the OISM links, `router multicast ipv6 routing`, `router pim sparse-mode ipv6 make-before-break disabled`) | **Raw CLI** on the interfaces and at the root (`raw_eos_cli`); `router_multicast.ipv6.routing` is a cli key. AVD's OISM insists on `underlay_multicast_pim_sm: true` on the OISM leafs; with no AVD uplinks and `underlay_multicast.pim_sm.mlag: false` it emits no PIM — its only output is the global IPv4 multicast routing block, removed below |
| OISM source loopbacks only on standard leafs | Native `vtep_diagnostic.loopback_ip_pools` keyed by `pod_name` (the Gateway role has no pod → no loopback) |
| `redistribute router-mac [virtual-ip] next-hop vtep primary` on the standard leafs | Structured config (`redistribute_routes` is a free-form list); gated on `standard_leaf` |
| Multi-domain EVPN Gateway (`REMOTE-EVPN-MPLS-PEERS`, `domain remote`, VRF `rd/route-target … domain all`, the stretched VLANs' remote-domain RD/RT) | Native `evpn_gateway` (`remote_peers` with IPv6 addresses, `evpn_l2`, `evpn_l3.mode: rd-rt-rewrite`) + `evpn_l2_multi_domain` per SVI; `local-as`, `update-source Loopback3`, no multihop via the peer group's structured config |
| `encapsulation mpls next-hop-self source-interface Loopback3`, `encapsulation vxlan`, `domain identifier 3:3` / `99:99 remote`, `bgp bestpath d-path`, the two I-ESIs (`domain local` / `domain remote`) | Native cli keys via structured config — AVD 6.3's `all_active_multihoming` models a single `domain all` segment, so it is not used |
| `route type ethernet-segment route-target auto`, `domain identifier <asn>:<asn> attach`, the I-ESI DF election preference | **Raw CLI** (`router_bgp.eos_cli`) — no AVD 6.3 keys; rendered inside the node's own `router bgp <asn>` context |
| Gateway backbone leg (`mpls ip`, Loopback3 with `node-segment ipv6 index`, `router isis BACKBONE`) | Structured config on the Gateway group (per-node NET / router-id) |
| DCI links (`2001:db8:bb<n>:<gw>::<host>/64`, `isis enable BACKBONE`, `isis network point-to-point`) | `l3_edge.p2p_links` with IPv6 addresses; `include_in_underlay_protocol: false` (AVD refuses IPv6 p2p links in a non-ISIS-SR underlay, and the Gateway ends are in BGP fabrics) with the IS-IS interface config on the profile's `ethernet_structured_config` |
| Backbone IS-IS SR-MPLS (`net`, `is-type level-2`, `address-family ipv6 unicast` + TI-LFA, `segment-routing mpls`, the loopback's `node-segment ipv6 index <id>`, `mpls ip`) | Native `underlay_routing_protocol: isis-sr` + `underlay_ipv6` + `isis_ti_lfa.protection: node` + `isis_sr.ipv6_node_sid_index_base: 0`, on a `spine` type made an LSR (`custom_node_type_keys`); `is-hostname` and the IPv6-only trims are structured config |
| Backbone EVPN-MPLS route reflectors (`EVPN-MPLS-GW-PEERS`, static neighbors, `encapsulation mpls next-hop-self source-interface Loopback0`, `bgp cluster-id 10.0.0.0`) | Structured config on the BACKBONE spine defaults; `bgp_cluster_id` native |
| EVPN All-Active host ports (`evpn ethernet-segment identifier auto lacp`, `lacp system-id`, `bgp session tracker`), D-SW1's uplink | Structured config on the port profiles; `uplink_switch_port_channel_structured_config` for D-SW1 |
| `route import match-failure action discard`, `spanning-tree root super`, `spanning-tree mst 0 priority 0` | Native (`evpn_import_pruning`, `spanning_tree_root_super`, `spanning_tree_priority`) |
| `session tracker TRACK-LOCAL-EVPN-PEERS recovery delay 10`, `layer-2 fec in-place update` | Native cli keys via structured config (`session_trackers`, `layer_2_fec_in_place_update`) |
| `bgp cluster-id 10.0.4.205`, `maximum-paths 4 ecmp 4` on the C Gateways | Native `bgp_cluster_id`; structured `router_bgp.maximum_paths` |
| `no ip routing` on D-SW1 | CSC `ip_routing: false` |
| `spanning-tree portfast edge`, `update wait-install` on cEOS, `no service interface inactive port-id allocation disabled` | As in Domains A + B: `eos_config_future.render_spanning_tree_portfast_edge`, the custom `cEOSLab` platform entry, the platform-profile `raw_eos_cli` |

## Rendered vs target

**The target is the lab's `startup-configs`** (`startup-config` is a symlink
to the tracked timestamped copy, last updated by aclabs #226). One
deliberate divergence from them, in the guide's favour:

> **`ipv6 nd ra interval 5` on Vlan4093.** The published guide (tech-library
> `21a0610`, 2026-08-25) applies the link-local-peering mitigation to the
> MLAG L3 underlay SVI as well as to the fabric links; the lab configs
> predate that commit and carry it on the fabric links only. The models
> render the guide's form — six extra lines, one per MLAG leaf. Re-sync the
> lab configs rather than "fixing" the model.

`make parity` compares the rendered configs with the startup-configs as
content sets (ordering is never compared). Exempt as cosmetic: comment
lines, interface/host descriptions, BGP neighbor descriptions, explicit
`no shutdown`. Everything else is listed below with its rationale. The
current tally is in `PARITY-STATUS.md`; at the time of writing it is
**156 missing / 390 extra lines across 27 nodes** (the four C spines, D-SW1
and both backbone nodes have nothing missing; 70 of the 156 are the
`remote-as` suffix class below). Every line belongs to a class below, and every class
is either cosmetic or functionally equivalent — there is no remaining AVD
addition that changes what the switch does. `make parity` is a content-set
comparison; `python3 avd/scripts/parity_report.py --blocks` runs the same
comparison per config stanza (nested by indentation) and shows that every
remaining line sits under the parent the guide has it under — a check the
flat comparison cannot make, and the one that would have caught a raw-CLI
`neighbor interface` line rendered after the VRF stanzas.

### In the target, not rendered (functionally equivalent)

| Lines | Why it is equivalent |
|---|---|
| `neighbor LOCAL-EVPN-PEERS remote-as 65300` (Domain C), `neighbor REMOTE-EVPN-MPLS-PEERS remote-as 65000` (Gateways) | AVD writes `remote-as` on every neighbor instead of on the group. |
| `neighbor interface Ethernet<n> peer-group LOCAL-IPV6-PEERS` (Domain D — eight per spine, four per leaf, 64 in all) and `neighbor interface Vlan4093 peer-group MLAG-IPV6-PEER` (C MLAG leafs, 6) | Rendered with the group's `remote-as` appended (`… remote-as 65400` / `… remote-as 6530x`) — the same ASN the peer group already carries; eos_cli_config_gen has no remote-as-less form. |
| `rd evpn domain all …` / `route-target import|export evpn domain all …` on the Gateways' stretched VLANs 10 and 70 | AVD writes the local form (`rd`, `route-target both`) plus the `evpn domain remote` form with the same values; `domain all` is the union of the two. (The VRFs render the `domain all` form natively.) |
| `no switchport` on port-channel members (MLAG peer link, host port-channels), `switchport` on the All-Active ES members | Member interfaces take their mode from the port-channel. |
| `vxlan vlan 10,30 vni 10010,10030` (ranged) | AVD writes one `vxlan vlan … vni …` line per VLAN; EOS stores the same mapping. |

### Rendered, not in the target (AVD additions — kept, called out)

EOS defaults that AVD writes explicitly (no effect on the box):
`no enable password`, `protocol https` (eAPI), `switchport mode access`,
`transceiver qsfp default-mode 4x10G` (rendered on every node — an addition
on the 25 fabric and Gateway nodes, the backbone targets already carry it; a
no-op on cEOS),
`spanning-tree mode mstp` on the spines (AVD would otherwise write
`spanning-tree mode none`; overridden back to the EOS default the guide
relies on), `spanning-tree mst 0 priority 32768` on the Domain D VTEPs and
D-SW1.

AVD dialect, same behaviour: per-neighbor `remote-as`; per-peer-group
`send-community` (the global `neighbor default send-community` is also
rendered, as in the guide); `router-id` repeated inside each VRF on the
standard leafs (the guide writes it on the Gateways' VRFs only); `vlan
internal order ascending range 1006 1199` on the backbone (AVD's default
range); `PL6-LOOPBACKS seq 30 permit 2001:db8:c2::/48 le 128` on the C
Gateways (nothing is connected in the shared-VTEP range there).

Render-only artefacts of raw CLI — the re-entered context headers
(`address-family evpn`, `evpn multicast`, `evpn ethernet-segment domain
local` / `domain remote`): EOS merges re-entered stanzas at config load, so
the running config is identical.

### Suppressed on purpose

| AVD would render | Why it is removed | Where |
|---|---|---|
| `ip routing` (global) | IPv6-only nodes; IPv4 is routed only inside the tenant VRFs. | `custom_structured_configuration_ip_routing: null` (both fabrics) |
| `redistribute connected` at the `router bgp` level | The guide redistributes under `address-family ipv6`. | `underlay_filter_redistribute_connected: false` + `custom_structured_configuration_router_bgp.redistribute: null` |
| Numbered addresses on Vlan4093 and the numbered MLAG L3 neighbor | The guide peers link-local on Vlan4093. | `mlag_peer_l3_vlan_structured_config.ipv6_addresses: null`; both neighbor candidates emptied in `l3leaf.defaults.structured_config.router_bgp.neighbors` |
| AVD's `RM-CONN-2-BGP-VRFS` / `PL-MLAG-PEER-VRFS` | In an IPv6 fabric AVD's route-map matches `ip address` against an IPv6 prefix-list (never matches); the guide's objects are owned instead. | `redistribute_mlag_ibgp_peering_vrfs: true` on the tenant |
| `router multicast / ipv4 / routing` + `software-forwarding sfe` on the OISM leafs | Underlay multicast is IPv6; IPv4 multicast routing lives in the VRFs. | `custom_structured_configuration_router_multicast.ipv4: null` in `DOMAIN_C_LEAFS.yml` |
| `ip address virtual source-nat vrf … address …` on the OISM leafs | AVD pairs it with `vtep_diagnostic`; the guide does not carry it. | `custom_structured_configuration_virtual_source_nat_vrfs: null` |
| `RM-MLAG-PEER-IN` (inbound `set origin incomplete`) | Replaced by the guide's outbound `RM-MLAG-PEER-OUT` with the `evpn-imported` filter. | `mlag_ibgp_origin_incomplete: false` |
| `maximum-routes 0` on the EVPN peer groups and `256000` on the MLAG group | AVD's protective prefix limit; the guide sets none (EOS applies its own 12,000-prefix default, which `maximum-routes 0` would in fact remove). | `maximum_routes: null` on every `bgp_peer_groups` entry |
| `neighbor REMOTE-EVPN-MPLS-PEERS ebgp-multihop 15` | The Gateway↔backbone session is iBGP (local-as 65000); the guide has no multihop there. | `bgp_peer_groups.evpn_overlay_core.structured_config.ebgp_multihop: null` |
| `spanning-tree mode none` on the spines | The guide leaves EOS at its default (`mstp`). | `spine.defaults.structured_config.spanning_tree.mode` |
| `no neighbor <EVPN-GROUP> activate` under `address-family ipv4` | Redundant with `no bgp default ipv4-unicast`, which every BGP speaker renders. | `avd_design_future.remove_redundant_ipv4_unicast_for_peer_groups: true` (all.yml) |
| Domain D iBGP SOO guard — `RM-EVPN-SOO-IN/OUT`, `ECL-EVPN-SOO`, the per-VTEP SOO stamp and the peer-group attaches | Applied unconditionally to iBGP EVPN clients (no knob); it cannot fire behind route reflectors and the guide runs without it. The guard still computes its site-of-origin from an IPv4 VTEP, so a placeholder `vtep_loopback_ipv4_pool` satisfies the lookup and never renders. | `route_maps: null`, `ip_extcommunity_lists: null`, `route_map_in/out: null` on the Domain D `l3leaf.defaults.structured_config` |
| `update wait-install` on the backbone | The guide runs it on the fabric nodes only; the custom cEOSLab platform entry would render it on BB1/BB2 too. | `bgp_update_wait_install: false` in `BACKBONE.yml` |
| Backbone IS-IS `address-family ipv4 unicast`, `maximum-paths`, `multi-topology`, the SR `router-id` and the IPv4 node SID | The guide runs the IPv6 unicast topology only. | Nulls in `BACKBONE.yml` `spine.defaults.structured_config` |
| Per-interface `mpls ip` on the backbone's DCI links | The guide enables MPLS globally. | `mpls_ip: false` on the `DCI` link profile |
| `switchport default mode routed`, ARP/MAC aging, `PL6-LOOPBACKS` / `RM-CONN-2-BGP` on D-SW1 | An L2 switch carries none of the routed-node baseline. | `DOMAIN_D_L2_SWITCHES.yml` |

## AVD 6.3.0 gaps this design works around

For the next AVD version:

- `underlay_ipv6_numbered` refuses any explicit `underlay_routing_protocol`
  other than `ebgp` (including `none`), numbers every uplink and refuses
  `underlay_rfc5549` — there is no link-local-only IPv6 underlay.
- eos_cli_config_gen renders `neighbor interface … peer-group …` only with a
  `remote-as` or `peer-filter`, and `router_bgp.eos_cli` lands after the VRF
  stanzas — raw CLI cannot stand in for a router-bgp-level neighbor line.
- `evpn_gateway.remote_peers[].ip_address` is schema-declared `format: ipv4`;
  pyavd 6.3.0 validates types only, so the backbone RRs' IPv6 Loopback0s
  pass. A stricter validator would need the peers stated another way.
- The per-VRF MLAG iBGP neighbor is derived from `mlag_ibgp_peering_ipv4_pool`
  even when only `mlag_ibgp_peering_ipv6_pool` is set (it falls back to the
  peer's Vlan4093 address), and `RM-CONN-2-BGP-VRFS` matches `ip address`
  against the IPv6 `PL-MLAG-PEER-VRFS`.
- The iBGP SOO guard needs an IPv4 VTEP address in an IPv6-only fabric.
- `evpn_multicast` requires IPv4 `underlay_multicast_pim_sm`; there are no
  IPv6 PIM keys (`pim ipv6 sparse-mode`, `router pim sparse-mode ipv6`),
  no `ipv6 nd ra interval`, no `route type ethernet-segment route-target
  auto`, no `domain identifier … attach`, no DF election preference on the
  I-ESI, and `all_active_multihoming` models a single `domain all` segment.
- A `spine` cannot be an SR label switch router without
  `custom_node_type_keys`; IPv6 `l3_edge` links cannot join a non-ISIS-SR
  underlay protocol.
- `identifier auto lacp` / `bgp session tracker` on connected endpoints and
  `no service interface inactive port-id allocation disabled` — as in
  Domains A + B.

## History

First build (2026-08-25), modelled on the Domain A + B rebuild of
2026-08-24 (`labs/techlib-vxlan-domain-ab/avd`), which established the
contract, the role-file pattern and the parity tooling reused here. The
directory previously held a placeholder copy of the first Domain A model.
