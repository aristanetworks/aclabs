# PARITY-LEDGER — techlib-vxlan-domain-ab AVD rebuild

> **Phase 1 deliverable (2026-07-21):** the diff-class taxonomy from rendering the
> pre-rebuild data models against the shipped startup-configs, with each class's
> **canonical AVD 6.3.0 capability verdict** — read directly from the installed
> pyavd 6.3.0 schema pickles, not from docs or memory. This ledger drives the
> from-scratch rebuild: every class is fixed ONCE in the data model.
>
> Baseline: 27/27 nodes rendered in-sandbox from the round-11 models;
> **0/27 at parity; ~3,058 residual content lines** (descriptions + comments
> excluded per the agreed exemptions). Residual is systematic: ~25 classes.

## Environment (proven working, sandbox + container-portable)

- `pip install pyavd==6.3.0 "ansible-core>=2.16,<2.19" netaddr distlib`
- Collections from GitHub tags (Galaxy not required):
  `ansible-galaxy collection install "git+https://github.com/aristanetworks/avd.git#/ansible_collections/arista/avd/,v6.3.0" --no-deps`
  plus `arista.eos` v9.0.0, `ansible.netcommon` v8.1.0, `ansible.utils` v6.0.0 (all `--no-deps`).
- Build per fabric (fabric_name must be uniform per play):
  `ansible-playbook avd/playbooks/build.yml -i avd/inventory.yml -e target_hosts=<DOMAIN_A_FABRIC|DOMAIN_B_FABRIC|BACKBONE>`

## The classes and their verdicts

Legend: **NATIVE** = eos_designs/eos_cli_config_gen key exists (path given).
**CSC** = custom_structured_configuration reaching a native eos_cli_config_gen
key (sanctioned, documented). **OPEN** = mechanism to be settled during build.

### Structural / design classes

| # | Class (evidence) | Verdict |
|---|---|---|
| 1 | IS-IS instance name `100` vs `EVPN_UNDERLAY` (±168 lines) | **NATIVE** `underlay_isis_instance_name: "100"` |
| 2 | Domain B unnumbered p2p — `ip address unnumbered Loopback0` ×64 missing, numbered /31 ×~64 extra | **CSC (merge-by-name)**: no native ipv4-unnumbered key in 6.3.0; group-level `custom_structured_configuration_ethernet_interfaces` merges onto generated interfaces by `name`, setting `ip_address: unnumbered Loopback0` (cli_config_gen renders the string verbatim). Uplink sets are uniform per role → group-level CSC, not per-node |
| 3 | Multi-domain gateway (the round-6 `router_bgp.eos_cli` hand-stitch) | **NATIVE** `evpn_gateway`: `remote_peers[]` (BB sessions), `evpn_l2/evpn_l3.enabled`, `d_path.local_domain_id/remote_domain_id` (the `99:99` stamps), `all_active_multihoming.{enabled, evpn_domain_id_local, evpn_domain_id_remote, evpn_ethernet_segment.identifier/rt_import, …}` — the I-ESI + `domain all` RD/RT model, natively. Round 5+6 hatches die |
| 4 | OISM depth — `pim ipv4 local-interface Loopback0` ×32, `mld` ×26, `vxlan multicast ipv6` ×12, `ip igmp` ×14, v6 AFs | **NATIVE framework** `evpn_l3_multicast` (underlay group pool + offset + PEG) + `evpn_l2_multicast`; per-VLAN/VRF group overrides for the N:1 vs 1:1 illustration + the IPv6 leg explored during build (vlans[] subkeys) |
| 5 | `redistribute router-mac … next-hop vtep primary` paired variant (DESIGN open-item 1) | **NATIVE** `svis[].evpn_redistribute_router_mac_system` (also per-node) |
| 6 | Domain B `spanning-tree root super` (DESIGN open-item 5) | **NATIVE** node key `spanning_tree_root_super: true` |
| 7 | PL-LOOPBACKS naming + content (permits BOTH domains' loopback pools — multi-domain reachability) vs AVD's `PL-LOOPBACKS-EVPN-OVERLAY` | **CSC**: custom `prefix_lists` + `route_maps` with the guide's names; suppress/replace the generated one at the redistribute hook (mechanism finalized during build — likely `underlay_filter_*` or route-map name override; else replace via structured_config) |
| 8 | BGP peer-group names/passwords (`LOCAL-EVPN-PEERS` etc. already customized; startup uses different structure incl. `neighbor default send-community` ×26) | **NATIVE** `bgp_peer_groups.*.name/password/…` + **CSC** `router_bgp.neighbor_default.send_community` (cli_config_gen native key) |

### Default-emission / style classes (AVD says more than a switch saves)

| # | Class | Verdict |
|---|---|---|
| 9 | `no shutdown` ×382 | **EXEMPT (contract amendment, 2026-07-21)** — Mitch accepted the explicit `no shutdown` AVD emits on interfaces as a sanctioned default; no code-around. The interim normalizer (commit 40e1016) was retired the same day |
| 10 | `no enable password` ×27, other global defaults | **NATIVE** `generate_default_config: false` (via structured_config) |
| 11 | `protocol https` ×27 under mgmt api | **NATIVE** management_api_http keys — omit the explicit protocol (default) |
| 12 | `spanning-tree portfast` vs guide's `portfast edge` ×26 | **NATIVE** `eos_config_future.render_spanning_tree_portfast_edge: true` |
| 13 | Global `spanning-tree edge-port bpduguard default` ×17 vs per-intf `bpduguard enable` ×14 | **NATIVE** cli_config_gen `spanning_tree.edge_port` dict (global), drop per-adapter `spanning_tree_bpduguard` |
| 14 | BFD 1000/1000/3 vs AVD default 300/300/3 (±40 lines) | **NATIVE** `bfd_multihop: {interval: 1000, min_rx: 1000, multiplier: 3}`; `router bfd` block emission follows |
| 15 | `isis metric 50` ×64 extra (guide uses default metric) | **NATIVE** `isis_default_metric`-adjacent key (present in schema; exact name confirmed during build) or omit via p2p profile |
| 16 | MLAG trunk group `MLAG_PEER` vs `MLAG` (±48 lines) + peer-vlan naming | **NATIVE expected** — eos_designs `trunk_groups.{mlag,mlag_l3}.name` fabric keys (confirm exact 6.3 path during build; `mlag_peer_vlan` etc. native) |
| 17 | `mtu 9114` extras + backbone 9214 (round-9 territory) | **NATIVE** `p2p_uplinks_mtu` per fabric + l3_edge/backbone interface mtu |
| 18 | cEOSLab platform lines (`software-forwarding sfe` ×12 extra; `no service interface inactive port-id allocation disabled` missing; transceiver line) | **NATIVE** `custom_platform_settings[].feature_support` (incl. `platform_sfe_interface_profile`, transceiver knobs) — build ONE cEOSLab platform profile instead of per-round whack-a-mole |
| 19 | `switchport mode access` ×26 explicit | **NATIVE** — omit explicit mode where default (adapter/profile shaping) |
| 20 | `ipv6 enable` ×38 extra vs guide's v6 style; `vlan internal order` extra; `maximum-paths 4`, `update wait-install`, `no autostate` ×14, `virtual_source_nat` ×14 extra | **NATIVE knobs each** (`ipv6_settings`/underlay ipv6 handling, `vlan_internal_order` omit, `bgp_maximum_paths`, `bgp_update_wait_install`, SVI `autostate`, drop `vtep_diagnostic`) — one-line verdicts finalized at build |

### Exempt (agreed with Mitch)

- Interface descriptions (`description …`) — any format accepted.
- Host descriptions.
- **BGP neighbor descriptions** (`neighbor <X> description <Y>`) —
  contract amendment, 2026-07-22 (Day 54 s2). The guide styles underlay
  peers `<peer>.IPV4`; AVD 6.3.0 has NO underlay peer-description knob
  (schema-verified — only overlay_bgp_peer_description and
  mlag_bgp_peer_description exist), so matching would mean ~64 per-node
  CSC entries of mechanical sprawl for a purely cosmetic string. Mitch
  ruled: exempt. Absorbed at amendment time: 64 missing + 72 extra
  (the 64 underlay pairs + 8 render-side VRF MLAG neighbor descs).
- Comment lines (`! …`) incl. the startup-config modification header.
- **`no shutdown` on interfaces** — accepted AVD default (contract
  amendment, 2026-07-21). AVD emits it explicitly; the guide configs
  don't save it; both are fine.
- **Line ordering** — the parity gate is CONTENT-SET parity: every
  configuration line present on both sides, position not compared.
  (Formally: the multiset diff of non-exempt lines must be empty.)

## Build sequencing (rebuild from scratch, evidence-driven)

1. ~~Class-9 mechanism~~ (exempt per amendment) → the cEOSLab platform profile + foundation knobs — done.
2. `all.yml` foundation (mgmt, defaults suppression, eos_config_future, platform profile, bfd, bgp style).
3. Domain A fabric → services → endpoints (render-diff loop per group).
4. Domain B fabric (IS-IS + unnumbered CSC + iBGP RR) → services (OISM incl. 1:1 group) → endpoints + B-SW1.
5. BACKBONE node_type + gateway `evpn_gateway` wiring on both domains (the native crown jewel).
6. Per-node host_vars scoping; iterate to 0 residual (minus exemptions).
7. ANTA catalog rebuild against the final models.

Prior escape hatches slated for deletion once native equivalents render:
round-5 `domain all` RD/RT CSC, round-6 `router_bgp.eos_cli` gateway lines,
round-7/8/9/11 platform/MTU suppressions (replaced by the platform profile).


---

## Session log — 2026-07-21 (rebuild session 1)

**Shipped this session** (each gated on full/affected-fabric rebuild +
regenerated PARITY-STATUS):

| Commit | Increment | Residual after |
|---|---|---|
| bdfa5d8 | Phase 1: taxonomy + this ledger | 2,943 (baseline) |
| 40e1016 | class-9 normalizer (later retired) | 2,561 |
| 6c13843 | all.yml foundation (cls 10/12/14, 18 partial) | 2,431 |
| 0560591 | contract amendment (no-shutdown + ordering exempt) | 2,429 |
| c9354f4 | parity_report.py — the running tally | 2,429 |
| 0dce0bf | class 1: underlay_isis_instance_name "100" | 2,237 |
| ef42f3a | class 2+15: Domain B unnumbered CSC batch | 2,045 |
| a0d0111 | class 16: MLAG naming dialect (5 native keys) | 1,953 |
| d3bcfe3 | class 8 pt.1: fabric peer-group passwords stripped (6) | 1,905 |

## Session log — rebuild session 2

| Commit | Increment | Residual after |
|---|---|---|
| 1e0c2b8 | class 8 pt.2: peer-group/process dialect (CSC-null attrs + neighbor default send-community) | 1,751 |
| 4d45bf3 | class 8/20: wait-install scoping — per-VRF via vrfs[].bgp.structured_config, BB explicit false | 1,737 |
| 8b6c444 | class 20: maximum-paths map — A leafs 128, B spines suppressed, B isis-AF suppressed | 1,705 |
| 6eb7344 | backbone rewrite: dynamic listen-range RR model (EVPN-GW-PEERS / IP-TRANSPORT-CLIENTS / DC-ASN-RANGE) | 1,597 |
| 7da8ea1 | class 7: PL-LOOPBACKS dialect — knob-false + CSC-owned redistribute objects, POD seq-30 union | 1,499 |
| 370f885 | CROWN JEWEL pt.1 (A-side): native evpn_gateway all_active_multihoming + d_path + rd-rt-rewrite | 1,327 |
| 0336225 | CROWN JEWEL pt.2 (B-side mirror): native model + attach-ASN fix — ALL FOUR password 7 renders dead | 1,293 |
| f522223 | contract amendment: BGP neighbor descriptions exempt (Mitch's ruling; −64 missing / −72 extra) | 1,157 |
| 8b73922 | class 4b: spine PIM dialect — unnumbered local-interface (eos_cli), Et7/8 sparse-mode, Vlan4093 de-PIM | 1,103 |
| 57a15cd | class 4a: MLAG-leaf SVI `ip igmp` (guide runs igmp+sparse-mode; AVD's OISM forks on MLAG) | 1,089 |
| e2e5830 | class 4c: the IPv6/MLD leg — SVI `mld`, global `mld snooping`, `vxlan multicast ipv6`, PROD overlay mapping, router-multicast VRF ipv6 re-entries | 1,029 |
| 446ad25 | remote-as dialect: group remote-as on LOCAL-* (A leafs), per-neighbor kills via node channel + gateway DCI anchors | 949 |
| a8239f8 | sweep S1: member/routed-port `no switchport` ×28 pod-scoped (4 deferred to endpoints refresh) | 921 |
| (this) | sweep S2: `switchport mode access` nulls ×20 on access POs + A3/4 Eth7 (3 deferred to refresh) | **901** |

**Landmines banked (crown jewel):** (1) The models' `platform: cEOS-LAB`
does NOT match AVD 6.3's built-in CEOS platform entry (matcher lacks the
hyphenated form) — nodes silently use the `default` entry. This mismatch
is LOAD-BEARING: the CEOS entry sets bgp_update_wait_install support
False, which would suppress the guide's 24 wait-install lines. Never
"fix" the platform string; the custom_platform_settings entry is the
seam. (2) STALE-RENDER TRAP: when an eos_designs task fails for a host,
the previous intended config REMAINS ON DISK — reading artifacts after a
build whose recap was not verified produces false conclusions (cost us a
full false-positive recon pass). Corollary discipline candidate: *a
render you didn't watch succeed is not evidence; check the PLAY RECAP
before reading artifacts.* (3) `evpn_gateway.evpn_l3.mode: rd-rt-rewrite`
rewrites IP-VRF (L3) RD/RT to domain-all single-form ONLY — MAC-VRF (L2)
domain-all overrides must stay hand-stitched in 6.3.

**Landmine banked (session 2):** `custom_structured_configuration_<key>`
is an ANSIBLE variable — a host_vars definition SHADOWS the group_vars
definition of the same name wholesale (host>group precedence; pyavd only
ever sees one value). The four gateway host_vars define
`custom_structured_configuration_router_bgp`, so fabric-wide router_bgp
dialect knobs must be repeated inside the gateway anchors. pyavd-side
merge order (read from source, `custom_structured_configuration/__init__.py`):
node structured_config → root → nested (role structured_config) →
custom_structured_configuration_* LAST. **Technique proven (session 2):** `underlay_filter_redistribute_connected:
false` kills the generator's loopback prefix-list, its RM-CONN-2-BGP
seq 10, AND detaches the route-map from `redistribute connected` — the
seam for owning the whole redistribute dialect via CSC. List unions by
(name, sequence) across channels are ORDER-INDEPENDENT — a POD-level
seq-30 contribution merges cleanly into a group-CSC 2-seq entry.
Node-type defaults + node_group structured_configs MERGE (both apply),
proven empirically on B-LEAF1 (session-tracker + pod-vlans coexist).

**Technique proven:**
`bgp_peer_groups.<role>.structured_config` merges under
`router_bgp.peer_groups[name=<name>]` only where eos_designs
materializes the group — the create-trap-free CSC-null anchor.

**Techniques proven:** CSC-null (un-sets hardcoded eos_designs
decisions; passed schema + renderer); eos_config_future/cli-gen inputs
must ride INSIDE structured config; merge-by-name interface CSC on
node-type defaults. **Phantom found:** `underlay_ipv4_unnumbered` was
set since the initial build but does not exist in the 6.3.0 schema.

**Landmines banked (remote-as dialect):** (1) A SECOND `structured_config`
key on a node entry is a DUPLICATE YAML KEY — the loader keeps one and
SILENTLY DISCARDS the other (the Gateway node entries already carry
`structured_config` referencing the per-gateway DCI anchors; new node-
channel content for those nodes must merge INTO the referenced anchor,
never add a sibling key). Diagnosis chain that found it: render → 
intended/structured_configs/<node>.yml intermediate (named the losing
layer) → the in-file comment naming the existing reference. (2)
`remote_as: null` in the node channel cleanly deletes the generated
per-neighbor attribute (proven ×6 standard leafs); peer-group
`remote_as` added via the peer-tag anchor merges onto materialized
groups exactly like the tags do.

**Landmines banked (class 4c):** (1) Root `eos_cli` is CHANNEL-SENSITIVE —
set via node/node_group `structured_config` it is SILENTLY DROPPED
(input-valid, never renders); it renders via
`custom_structured_configuration_eos_cli` (scratch-proven) and via
object-level eos_cli (vlan_interfaces[], vxlan1, router_bgp). (2) CSC
root eos_cli REPLACES the platform profile's eos_cli wholesale (string,
last-merge-wins) — platform lines like `no service interface inactive
port-id allocation disabled` must ride inside the CSC literal or vanish
(cost a −1/node hunt). (3) Mid-dict `eos_cli: |` inserts SWALLOW the
mapping's remaining same-indent keys into the literal — the tell is raw
YAML rendered into EOS config (and the A MLAG VTEP source silently moved
to Loopback1); insert literals as the LAST sibling and re-verify the
anchor. (4) `router_multicast.vrfs[].ipv6` does not exist in 6.3 on
either schema side — VRF-level IPv6 multicast routing requires eos_cli
context re-entry; the duplicated `router multicast`/`vrf X` headers are
the accepted cost (+28 fleet-wide). (5)
`vxlan.vrfs[].multicast_group_encap_range` is schema-only — no template
render path in 6.3 (half-landed upstream); the overlay mapping line
rides vxlan1 eos_cli.

## NEXT SESSION — pickup spec (BGP dialect, fully reconned)

The guide's dialect (read from B-SPINE1; verify A/BB during work):
`neighbor default send-community` global; groups carry ONLY peer
group / remote-as / update-source / bfd / route-reflector-client —
NO password, NO maximum-routes, NO per-group send-community, NO
`no neighbor X activate` under ipv4 AF (implicit via `no bgp default
ipv4-unicast`). Guide also has `update wait-install` (x14: Domain B
12 + BB 2) and `distance bgp 20 200 200`.

Mechanism plan (step 1 DONE — 6 fabric-level passwords stripped, -48;
the 4 surviving `password 7` renders are the gateway CSC's, deferred
to the gateway swap):
1. ~~The models' peer-group passwords~~ DONE. Next: the CSC-anchor + send_community live in the CSC
   anchor vars near the top of DOMAIN_A_FABRIC.yml (~lines 40-60) and
   DOMAIN_B_FABRIC.yml (~lines 45-125) — STRIP there.
2. Remaining rendered attrs (maximum-routes, ipv4-AF deactivate) get
   the CSC-null merge-by-name inside those same anchor vars:
   peer_groups[{name, maximum_routes: null, send_community: null}],
   address_family_ipv4.peer_groups[{name, activate: null}].
3. `neighbor default send-community`: router_bgp.neighbor_default.
   send_community — probe the VALUE that renders the bare line
   (try "all" first). Scope: BGP nodes only (place in the node-type
   defaults / anchor vars, NOT all.yml — B-SW1 must not grow a
   router bgp block).
4. bgp_update_wait_install: true (DOMAIN_B_FABRIC + BACKBONE);
   check bgp_distance for 20/200/200.

**Then remaining, in ledger order:** PL-LOOPBACKS naming/content
(class 7), the native evpn_gateway replacement of rounds 5-6 (class
3 — the crown jewel; keys confirmed native), OISM depth incl. IPv6
(class 4), then the per-node sweep (vlan-internal-order 17/27,
switchport mode access, edge-port bpduguard 17-node scope, autostate,
source-nat, transceiver re-add x2, mtu leftovers, ipv6 enable style,
RD/RT scheme) and the services/endpoints/host_vars refresh against
the per-leaf tables in DESIGN.md. ANTA catalog rebuild last.
