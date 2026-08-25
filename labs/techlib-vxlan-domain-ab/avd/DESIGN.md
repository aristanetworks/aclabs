# AVD data models — techlib EVPN-VXLAN Deployment Guide, Domains A + B

> AVD **6.3.0** data models that render the lab's startup configurations
> (`startup-configs/clab-arista-evpn-dg-domain-ab/*/startup-config`), which
> in turn mirror the [Domains A & B deployment guide](https://mitchv85.github.io/tech-library/data_center/evpnvxlan/deployment_guide/domains_a_b/overview/).
>
> Goals, in order: (1) functionally equivalent configuration, (2) as little
> node-specific data as the design allows, (3) native AVD keys before
> structured config, structured config before raw CLI. Cosmetic differences
> (descriptions, ordering, EOS defaults AVD writes out explicitly) are
> accepted and listed below so nothing is silently different.

## Toolchain

```bash
python3 -m venv .venv && . .venv/bin/activate
pip install "pyavd[ansible]==6.3.0"
ansible-galaxy collection install "arista.avd:==6.3.0"
```

From the lab root (`labs/techlib-vxlan-domain-ab`):

| Command | What it does |
|---|---|
| `make build` | Renders all three fabrics into `avd/intended/configs/*.cfg` (`build-a`, `build-b`, `build-bb` per fabric) |
| `make parity` | Compares every rendered config with the lab's startup-config and refreshes `avd/PARITY-STATUS.md` |
| `make parity-node NODE=A-LEAF7` | Full missing/extra listing for one node |
| `make deploy` / `make validate` | Push via eAPI / run the ANTA catalogs (unchanged) |

Each fabric is its own play because `fabric_name` must be uniform per play.

## Layout

```
avd/
├── inventory.yml                     # fabrics, role groups, ANTA tags — no data
├── group_vars/
│   ├── all.yml                       # connectivity, cEOS platform profile, management preamble
│   ├── DCI.yml                       # the nine inter-domain p2p links, defined once
│   ├── DOMAIN_A_FABRIC/
│   │   ├── fabric.yml                # underlay/overlay, spines, leaf pods, Gateway pair
│   │   ├── services.yml              # tenant: VRFs, SVIs, OISM
│   │   └── endpoints.yml             # port profiles + hosts
│   ├── DOMAIN_A_LEAFS.yml            # role: standard (MLAG + OISM) leaf
│   ├── DOMAIN_A_GATEWAYS.yml         # role: Gateway (no OISM, tuned BFD)
│   ├── DOMAIN_B_FABRIC/{fabric,services,endpoints}.yml
│   ├── DOMAIN_B_LEAFS.yml / DOMAIN_B_GATEWAYS.yml / DOMAIN_B_L2_SWITCHES.yml
│   └── BACKBONE.yml                  # BB1/BB2
├── playbooks/{build,deploy,validate}.yml
├── scripts/parity_report.py          # rendered-vs-target report (`make parity`)
├── scripts/anta_audit.py             # ANTA catalog/tag audit (previous campaign)
├── PARITY-STATUS.md                  # `make parity` output
├── anta/                             # ANTA catalogs (previous campaign, unchanged)
└── intended/, documentation/         # build output (git-ignored)
```

No `host_vars/`. The model is ~1,750 lines including comments (the previous
byte-parity build was ~4,400 lines across 26 files with 17 host_vars files).

## How the model is organised

**Fabric files hold the design; role files hold the switches.** Everything
that differs between a standard leaf and a Gateway that AVD cannot derive on
its own is a *role* setting in `group_vars/<ROLE>.yml`: `evpn_multicast`,
`underlay_multicast_pim_sm`, the Gateway BFD timers (Domain A), the OISM
source-loopback pod, and one boolean, `standard_leaf`. That boolean gates the
raw-CLI hooks in the services model (`svi_profiles` / `vrfs[].raw_eos_cli`
/ `vrfs[].bgp.raw_eos_cli`) with plain Jinja
(`"{{ x if standard_leaf else '' }}"`), so the Gateway pair — which serves
the same VLANs and VRFs but does not run OISM — renders none of the OISM
additions. This is ordinary Ansible variable precedence, not merge tricks.

> Vars placed *inside* `inventory.yml` rank below `group_vars/` files in
> Ansible's precedence and cannot override a fabric-level setting — hence
> the small per-role files.

**Per-node data is identity only.** Every node entry carries `id` and
`mgmt_ip` — and nothing else, except the values below, each forced by the
guide's design. Even the leaf uplinks are derived: `default_interfaces`
states the cabling rule once (leaf `<id>` lands on `Ethernet<id>` of every
spine) and AVD computes each leaf's `uplink_switch_interfaces` from it. The
per-node exceptions:

| Where | Value | Why it cannot be derived |
|---|---|---|
| A-SPINE1..4 | `downlink_pools` (one /28 each) | The guide numbers the p2p links spine-major (spine *n* owns `192.168.0.<16(n-1)>/28`); AVD's default algorithm is leaf-major. |
| A-LEAF1..6 | `vtep_loopback_ipv4_address` | Multi-VTEP MLAG: each leaf's *unique* VTEP is Loopback1 (10.1.1.\<id\>); AVD's MLAG model would derive it from Loopback0. |
| A-LEAF7/8, B-LEAF7/8 | `structured_config.router_bgp.neighbors` (2 each) | The eBGP IPv4 sessions to BB1/BB2 over the DCI links (the backbone side is a dynamic listen range, so the Gateway must initiate). |
| B-LEAF7/8 | `address_family_ipv4.networks` (2 each) | Own Loopback0/Loopback1 advertised into the backbone. |
| B-LEAF3 / B-LEAF4 | `filter.tags`, `raw_eos_cli` (MLD-snooping VLAN list) | The pair is asymmetric by design (VLAN 60 Red on B-LEAF3, VLAN 70 Brown on B-LEAF4). |
| BB1/BB2 | `address_family_ipv4.networks` (1 each) | Own Loopback0 advertised to the transport clients. |

The Gateway ASNs are *not* per-node: `l3leaf.defaults.bgp_as: '65101-65108'`
is indexed by node id (for an MLAG pair, by the primary's id), which yields
65101/65103/65105 per pod and 65107/65108 on the two standalone Gateways.

Per-pod (node-group) values: the pod's VLAN set (`filter.tags`), the Domain A
shared-VTEP Loopback2 address, the MLD-snooping VLAN list, and the
spanning-tree exclusion list for the pod's MLAG peering VLANs.

## The three fabrics

**Domain A** — eBGP underlay (65100 spines, 65101/65103/65105 per pair,
65107/65108 Gateways), eBGP EVPN, MLAG leaf pairs with Multi-VTEP MLAG
(unique Loopback1, shared Loopback2 from `10.2.1.<pair>`), OISM IPv4+IPv6 in
PROD (VLAN 10, 30) and DEV (VLAN 50, 70), All-Active Gateway pair
(I-ESI `0000:aaaa:0007:0008:0000`, D-PATH `1:1` / `99:99`).
Spine-major p2p addressing (`192.168.0.0/24`) comes from per-spine
`downlink_pools`.

**Domain B** — IS-IS level-2 instance `100` with IPv4-unnumbered fabric
links, iBGP EVPN in AS 65200 reflected by the spines (cluster-id
`10.0.2.205`), no MLAG — EVPN All-Active multihoming everywhere with
LACP-derived ESIs and `spanning-tree root super`, OISM IPv4+IPv6 in PROD
(VLAN 10, 20, 40) and DEV (VLAN 60, 70, 80), All-Active Gateway pair
(I-ESI `0000:bbbb:0007:0008:0000`, D-PATH `2:2` / `99:99`), B-SW1 as an
L2-only switch dual-homed to B-LEAF5/6 over an All-Active segment.

**Backbone** — BB1/BB2 in AS 65000: IPv4 transport for the Gateway pairs
(dynamic `bgp listen range 172.16.0.0/16` gated by the `DC-ASN-RANGE` peer
filter) and EVPN route reflectors (`bgp listen range 10.0.0.0/8`). Modelled
as AVD `spine` nodes with the underlay switched off; the two dynamic peer
groups are structured config because AVD only materialises an RR peer group
for statically known clients.

The Gateways join the backbone as iBGP from the backbone's point of view
(`local-as 65000 no-prepend replace-as` on `REMOTE-EVPN-PEERS`).

## Where each guide feature comes from

| Guide feature | Mechanism |
|---|---|
| Multi-domain EVPN Gateway (I-ESI, `domain remote`, D-PATH ids, `bgp bestpath d-path`, VRF `rd/route-target … domain all`) | Native `evpn_gateway` (`all_active_multihoming`, `d_path`, `evpn_l2`, `evpn_l3.mode: rd-rt-rewrite`, `remote_peers`) |
| Multi-domain MAC-VRFs (VLAN 10, 70) vs local VLANs | Native `evpn_l2_multi_domain` per SVI |
| Peer tagging on the leafs (`peer-tag in/out discard SPINES`) | Native cli keys via `l3leaf.defaults.structured_config` (leaf-only on purpose — on a spine the same tags would discard leaf routes) |
| `neighbor default send-community` | `custom_structured_configuration_router_bgp` |
| `PL-LOOPBACKS` / `PL-P2P-UNDERLAY` / `RM-CONN-2-BGP` | `underlay_filter_redistribute_connected: false` + CSC prefix-lists/route-map (AVD's own list would not cover the shared Loopback2) |
| `RM-MLAG-PEER-OUT` + `evpn-imported` extcommunity list | `mlag_ibgp_origin_incomplete: false` + `bgp_peer_groups.mlag_ipv4_underlay_peer.structured_config.route_map_out` + CSC objects (AVD 6.3 only knows the inbound `RM-MLAG-PEER-IN` form) |
| MLAG naming (`MLAG_PEER`, `MLAG_PEER_SYNC`, …), `169.254.0.0/30` sync, `192.0.0.0/31` L3 and per-VRF peering, VLAN 3001/3002 | Native (`trunk_groups`, `mlag_peer_*_name`, `fabric_ip_addressing.mlag.algorithm: same_subnet`, `mlag_ibgp_peering_vlan`; the per-VRF peering pool defaults to `mlag_peer_l3_ipv4_pool`) |
| `no autostate` + `mtu 9014` on the MLAG peering SVIs | Native `mlag_peer_l3_vlan_structured_config` (Vlan4093) and `vrfs[].structured_config.vlan_interfaces` (Vlan3001/3002, gated on `standard_leaf` so no SVI is created on the Gateways) |
| Multi-VTEP MLAG (`vxlan mlag source-interface Loopback2`) | AVD 6.3 enables Multi-VTEP automatically for MLAG + OISM but sources the unique VTEP from Loopback0; the guide's Loopback1/Loopback2 layout is one `source_interface` override plus a per-pod Loopback2 |
| OISM IPv4 (`pim ipv4 sparse-mode`, `pim ipv4 local-interface Loopback10x`, `vxlan vrf … multicast group`, `evpn multicast`, `router multicast vrf … ipv4`) | Native `evpn_l3_multicast` + `vtep_diagnostic` |
| `ip igmp` on the Domain A SVIs | **Structured config** on the SVI profile — AVD's OISM writes `pim ipv4 sparse-mode` on MLAG leafs and `ip igmp` on non-MLAG ones (so Domain B gets it natively); the guide runs both on Domain A |
| OISM source loopbacks only on standard leafs | Native `vtep_diagnostic.loopback_ip_pools` keyed by `pod_name` (the Gateway role has no pod → no loopback) |
| **OISM IPv6** (`mld`, `pim ipv6 sparse-mode`, `mld snooping vlan …`, `vxlan multicast ipv6`, `router multicast vrf … ipv6 routing`, `evpn multicast address-family ipv6`) | **Raw CLI** — no AVD 6.3 keys (SVI `eos_cli`, VRF `raw_eos_cli`, pod `raw_eos_cli`, Vxlan1 `eos_cli`) |
| `redistribute router-mac [virtual-ip] next-hop vtep primary` | **Raw CLI** (`svis[].bgp.raw_eos_cli`) — AVD 6.3 only knows `router-mac system` |
| EVPN All-Active host ports (`evpn ethernet-segment identifier auto lacp`, `lacp system-id`, `bgp session tracker`) | Structured config on the port profile (cli keys exist, no `connected_endpoints` keys); B-SW1's uplink via `uplink_switch_port_channel_structured_config` |
| `session tracker TRACK-LOCAL-EVPN-PEERS recovery delay 10` | Native cli keys via structured config |
| `route type ethernet-segment route-target auto`, `domain identifier <asn>:<asn> attach` | **Raw CLI** (`router_bgp.eos_cli`) — no AVD 6.3 keys |
| I-ESI DF election preference | **Raw CLI** (node `raw_eos_cli`) |
| `layer-2 fec in-place update`, `route import match-failure action discard` | Native (`layer_2_fec_in_place_update`, `evpn_import_pruning`) |
| IS-IS underlay (instance `100`, NET `49.1111.0000.0000.<id>.00`, level-2, p2p) | Native (`underlay_routing_protocol: isis`, `isis_system_id_format: node_id`, `isis_default_*`) |
| **IPv4-unnumbered fabric links** | **Structured config** — AVD 6.3 has no unnumbered option for uplinks; every fabric interface is overridden to `ip address unnumbered Loopback0` by name and the leafs carry a placeholder `uplink_ipv4_pool` that is never rendered |
| B-side `aggregate-address` / `network` into the backbone | Native cli keys via structured config (`aggregate_addresses` renders at the `router bgp` level rather than under `address-family ipv4` — same object on EOS) |
| Backbone listen ranges, peer filter, RR groups, `management ssh`, `interface defaults mtu` | Structured config / CSC |
| `spanning-tree portfast edge` | `eos_config_future.render_spanning_tree_portfast_edge` (CSC) |
| `update wait-install` on cEOS | Custom `cEOSLab` platform entry (AVD's built-in cEOS entry disables it) |
| `no service interface inactive port-id allocation disabled` | Platform-profile `raw_eos_cli` |

## Rendered vs target

**The target is the lab's `startup-configs`, and the guide's published
`full_configs` track them.** Verified after the MTU change of aclabs #226:
17 of the 27 nodes are identical bar the EOS version in the comment header,
and the other ten differ by exactly one line each — the only deliberate
divergence between the two:

> **Session-tracker recovery delay.** The lab runs `recovery delay 10
> seconds` against the guide's `300 seconds`, on the ten nodes that have a
> tracker (A-LEAF7/8, B-LEAF1..8), so a lab user is not left waiting five
> minutes to watch a recovery complete. The models render the lab value.
> Don't "fix" it.

Anything else showing up in a guide-vs-lab diff means one of the two has
moved and the other has not — that is a signal, not noise.

`make parity` compares the rendered configs with the startup-configs as
content sets (ordering is never compared). Exempt as cosmetic: comment
lines, interface/host descriptions, BGP neighbor descriptions, explicit
`no shutdown`. Everything else is listed below with its rationale. The
current tally is in `PARITY-STATUS.md`; at the time of writing it is 137
missing / 536 extra lines across 27 nodes. Every one belongs to a class
below, and every class is either cosmetic or functionally equivalent —
there is no remaining AVD addition that changes what the switch does.

### In the target, not rendered (functionally equivalent)

| Lines | Why it is equivalent |
|---|---|
| `neighbor <GROUP> remote-as …` on `LOCAL-*` / `REMOTE-EVPN-PEERS` | AVD writes `remote-as` on every neighbor instead of on the group. |
| `rd evpn domain all …` / `route-target import export evpn domain all …` on the Gateways' stretched VLANs | AVD writes the local form (`rd`, `route-target both`) plus the `evpn domain remote` form with the same values; `domain all` is the union of the two. |
| VRF `address-family ipv4 / neighbor 192.0.0.x activate` (MLAG per-VRF peering) | The neighbor is a member of `MLAG-IPV4-PEER`, which is activated under the global `address-family ipv4`; AVD relies on the peer-group activation (its standard MLAG VRF-peering design). |
| `ip address 169.254.0.1/30` + `peer-address 169.254.0.2` on Vlan4094 | AVD numbers the MLAG peer VLAN as a /31 (`.0/31` ↔ `.1/31`); consistent on both members. `fabric_ip_addressing.mlag.ipv4_prefix_length` would set /30 but applies to the L3 peering pool as well, where the guide wants /31. |
| `no switchport` on port-channel members, `switchport` on the Gateway ES members | Member interfaces take their mode from the port-channel. |
| `vxlan vlan 10,30 vni 10010,10030` (ranged) | AVD writes one `vxlan vlan … vni …` line per VLAN; EOS stores the same mapping. |
| `aggregate-address` under `address-family ipv4` (B Gateways) | Rendered at the `router bgp` level (cli_config_gen has no per-AF key); same aggregate in IPv4 unicast. |
| `isis circuit-type level-2` on the loopbacks | Redundant with `is-type level-2`; cli_config_gen has no loopback key for it. |
| `no ip routing` on B-SW1 | EOS default (AVD writes only `no ip routing vrf MGMT`). |

### Rendered, not in the target (AVD additions — kept, called out)

EOS defaults that AVD writes explicitly (no effect on the box):
`no enable password`, `protocol https` (eAPI), `switchport mode access`,
`transceiver qsfp default-mode 4x10G` (every node; a no-op on cEOS),
`spanning-tree mode mstp` on the spines (AVD would otherwise write
`spanning-tree mode none`; overridden back to the EOS default the guide
relies on), `spanning-tree mst 0 priority 32768` on the Domain B VTEPs and
B-SW1, `router bfd / multihop interval 300 min-rx 300 multiplier 3` on the
Domain A spines/leafs and the backbone (the EOS default timers — Domain B
and the Domain A Gateways carry the guide's tuned 1000/1000/3).

AVD dialect, same behaviour: per-neighbor `remote-as`; per-peer-group
`send-community` (the global `neighbor default send-community` is also
rendered, as in the guide); `router-id` repeated inside each VRF;
`vlan internal order ascending range 1006 1199` on the spines and backbone
(AVD's default range; the guide's leafs write the same line, and 194 IDs
comfortably exceed the routed-port count here); `isis metric 50` on every
Domain B fabric link (uniform, so no path changes); `maximum-paths 4` under
`router isis / address-family ipv4 unicast` and on the Domain B spines'
`router bgp`; PL-LOOPBACKS `seq 30 permit 10.2.0.0/16 eq 32` on the spines
and Gateways (nothing is connected in that range there).

Render-only artefacts of raw CLI — the re-entered context headers
(`address-family evpn`, `evpn ethernet-segment domain all`, `evpn
multicast`, `router multicast`, `vrf <VRF>`): EOS merges re-entered stanzas
at config load, so the running config is identical.

### Suppressed on purpose

| AVD would render | Why it is removed | Where |
|---|---|---|
| `router multicast / ipv4 / software-forwarding sfe` on every OISM node | Changes the cEOS multicast forwarding path; the guide's lab does not run it. | `custom_structured_configuration_router_multicast` in the `*_LEAFS` role files |
| `neighbor REMOTE-EVPN-PEERS ebgp-multihop 15` | The Gateway↔backbone session is iBGP (local-as 65000); the guide has no multihop there. | `bgp_peer_groups.evpn_overlay_core.structured_config.ebgp_multihop: null` |
| `RM-MLAG-PEER-IN` (inbound `set origin incomplete`) | Replaced by the guide's outbound `RM-MLAG-PEER-OUT` with the `evpn-imported` filter. | `mlag_ibgp_origin_incomplete: false` |
| `spanning-tree mode none` on the spines | The guide leaves EOS at its default (`mstp`). | `spine.defaults.structured_config.spanning_tree.mode` |
| OISM source loopbacks + `virtual source-nat` on the Gateways | The Gateways do not run OISM. | `vtep_diagnostic.loopback_ip_pools` keyed by the leaf pod |
| `no neighbor <EVPN-GROUP> activate` under `address-family ipv4` (and the empty `address-family ipv4` stanza it created on the Domain B nodes) | Redundant with `no bgp default ipv4-unicast`, which every BGP speaker renders — as every target does. AVD writes the per-group deactivation because the EOS default is `bgp default ipv4-unicast`. | `avd_design_future.remove_redundant_ipv4_unicast_for_peer_groups: true` (all.yml) |
| `ipv6 enable` on every dual-stack SVI | AVD adds an EUI-64 link-local as an IPv6 best practice; the guide's validated configs do not carry it. Suppressed to reproduce exactly what the lab runs — a maintainer may prefer AVD's default. | `ipv6_enable: false` on the `TENANT_SVI` profile |
| `ip dhcp relay information option` on the spines | The option is a leaf concern (no relay agent runs on a spine). | Set on the leaf role's `structured_config.ip_dhcp_relay` instead of `general_settings` |
| `maximum-routes 0` on the EVPN peer groups and `256000` on the IPv4/MLAG groups | AVD's protective prefix limit. The guide sets none, and `maximum-routes 0` would in fact *remove* the 12,000-prefix limit EOS applies by default. Not required. | `maximum_routes: null` on every `bgp_peer_groups` entry |
| Domain B iBGP SOO guard — `RM-EVPN-SOO-IN/OUT`, `ECL-EVPN-SOO`, the per-VTEP `set extcommunity soo … additive`, and the peer-group attaches | AVD applies its anti-readvertisement guard unconditionally to iBGP EVPN clients (no input knob). It cannot fire behind route reflectors — an RR never reflects a route back to its originator — and the guide runs without it. Not required. | On the Domain B `l3leaf.defaults.structured_config`: `route_maps: null`, `ip_extcommunity_lists: null` (the SOO objects are the only occupants of both lists on a B node), plus `router_bgp.address_family_evpn.peer_groups[LOCAL-EVPN-PEERS]` with `route_map_in: null` / `route_map_out: null` |
| `ip address virtual source-nat vrf … address …` on the OISM leafs | AVD pairs it with `vtep_diagnostic` so switch-originated traffic on an anycast SVI is sourced from the VRF's OISM loopback. The guide does not carry it. Not required. | `custom_structured_configuration_virtual_source_nat_vrfs: null` in the OISM-leaf role files |

## AVD 6.3.0 gaps this design works around

For the next AVD version: IPv4-unnumbered fabric uplinks; every IPv6 OISM
line; `route type ethernet-segment route-target auto`; `domain identifier …
attach`; the DF election preference on `evpn ethernet-segment domain all`;
`identifier auto lacp` / `bgp session tracker` on connected endpoints; an
outbound-filter variant of the MLAG peer route-map; `aggregate-address`
under an address family; a per-VRF hook for the MLAG peering SVI;
`no service interface inactive port-id allocation disabled`.

## History

The first AVD build of this lab (July 2026) pursued byte-level parity with
the guide and reached it at the cost of ~4,400 lines and 17 host_vars files.
Its ledger of AVD 6.3 landmines (`PARITY-LEDGER.md`, in git history before
this rewrite) remains a useful reference for the merge semantics of
structured config, and its ANTA catalogs under `anta/` are carried over
unchanged.
