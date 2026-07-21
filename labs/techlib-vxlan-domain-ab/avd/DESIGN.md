# AVD & ANTA Design for `techlib-vxlan-domain-ab`

> **Purpose:** authoritative design record for the AVD data models and ANTA test suite that render + validate the Domain A and Domain B configurations shown in the [tech-library EVPN-VXLAN Deployment Guide](https://tech-library.arista.com/data_center/evpnvxlan/deployment_guide/) (Section 1: Domains A & B).
>
> **Render target:** line-for-line parity with `docs/data_center/evpnvxlan/deployment_guide/domains_a_b/full_configs/*.cfg` in the `aristanetworks/tech-library` repo.
>
> **Toolchain:** AVD `6.3.0` and the latest ANTA — both baked into the `techlib` container.

---

## Repository layout

```
labs/techlib-vxlan-domain-ab/avd/
├── DESIGN.md                            # This file
├── inventory.yml                        # Two fabrics + backbone group
├── group_vars/
│   ├── all.yml                          # Common (AAA, NTP, DNS, MGMT, MTU, timezone) — reused across everything
│   ├── DOMAIN_A_FABRIC.yml              # Fabric shape for Domain A (eBGP + MLAG standard leafs, A-A Gateway)
│   ├── DOMAIN_A_SERVICES.yml            # Tenants, VRFs, SVIs, OISM groups for Domain A
│   ├── DOMAIN_A_ENDPOINTS.yml           # Servers HostA1..HostA8 (MLAG hosts + Gateway-attached HostA8)
│   ├── DOMAIN_B_FABRIC.yml              # Fabric shape for Domain B (IS-IS + iBGP + A/A everywhere)
│   ├── DOMAIN_B_SERVICES.yml            # Tenants, VRFs, SVIs, OISM groups for Domain B
│   ├── DOMAIN_B_ENDPOINTS.yml           # Servers HostB1..HostB8 + B-SW1 CE switch downstream hosts
│   └── BACKBONE.yml                     # Fabric shape for BB1/BB2 (dedicated backbone node_type)
├── host_vars/
│   ├── A-LEAF1.yml                      # PROD-only overrides
│   ├── A-LEAF2.yml                      # PROD-only overrides
│   ├── A-LEAF3.yml                      # PROD + DEV, dual OISM VRF
│   ├── A-LEAF4.yml                      # PROD + DEV, dual OISM VRF
│   ├── A-LEAF5.yml                      # DEV-only overrides
│   ├── A-LEAF6.yml                      # DEV-only overrides
│   ├── A-LEAF7.yml                      # Gateway: disable OISM, add locally-attached HostA8
│   ├── A-LEAF8.yml                      # Gateway: disable OISM, add locally-attached HostA8
│   ├── B-LEAF1.yml … B-LEAF6.yml        # Per-leaf VRF/VLAN scoping for B (see per-leaf table below)
│   ├── B-LEAF7.yml                      # B Gateway + locally-attached HostB8 + VLAN 60 local
│   ├── B-LEAF8.yml                      # B Gateway + locally-attached HostB8 + VLAN 60 local
│   ├── B-SW1.yml                        # CE switch (L2-only, EVPN A/A downstream, MST)
│   ├── BB1.yml                          # Backbone RR
│   └── BB2.yml                          # Backbone RR
├── intended/                            # AVD-rendered structured configs (git-ignored, artifact of `make build`)
│   └── configs/*.cfg
├── playbooks/
│   ├── build.yml                        # eos_designs + eos_cli_config_gen
│   ├── deploy.yml                       # eos_config_deploy_eapi (already correct)
│   └── validate.yml                     # anta_runner
└── anta/
    ├── catalog.yml                      # Top-level catalog (imports the concern-specific catalogs)
    ├── underlay.yml                     # BGP peerings, BFD, interface state, MTU
    ├── overlay.yml                      # EVPN Type 2/3/5 routes, MAC-VRF/IP-VRF RTs, VXLAN VNIs
    ├── multihoming_gateway.yml          # MLAG, ES, I-ESI, DF election, D-PATH stamp
    ├── oism.yml                         # PIM neighbors, IGMP sources, SBD, Type 6/7/8/10
    └── dataplane.yml                    # Host-to-host ping (intra- and inter-domain)
```

The `custom_structured_configuration_*` pattern (already in use in the existing scaffolding) is our escape hatch for anything AVD 6.3.0 can't natively express. All such usage is documented inline with a `# CSC:` comment explaining *why* it's needed.

---

## Fabric structure

### Domain A — eBGP + MLAG standard leafs + All-Active Gateway

| Attribute | Value |
|---|---|
| `fabric_name` | `DOMAIN_A_FABRIC` |
| Underlay routing | eBGP with per-node ASN (`65100` spines, `65112`/`65134`/`65156`/`65178` leaf pairs, `65107`/`65108` Gateway) |
| Overlay routing | eBGP EVPN, Loopback0 source |
| Multihoming (standard leafs) | MLAG with Multi-VTEP MLAG (Loopback2 shared) |
| Multihoming (Gateway) | All-Active EVPN (I-ESI `0000:aaaa:0007:0008:0000`, DF preference 2000/1000) |
| Distributed IRB | Symmetric, dual-stack IPv4+IPv6 |
| OISM | IPv4 PIM-SSM underlay group `232.1.1.1` (PROD), `232.1.1.2` (DEV); IPv6 EVPN multicast per VRF |
| Gateway ASN model | Distinct per-Gateway (`65107` / `65108`) |
| Loopback0 pool | `10.0.1.0/24` |
| Loopback1 pool (VTEP) | `10.1.1.0/24` |
| Loopback2 pool (MLAG Shared VTEP) | `10.2.1.0/24` |
| MLAG peer-link IP pool | `169.254.0.0/30` (VLAN 4094) |
| MLAG L3 underlay peer pool | `192.0.0.0/31` (VLAN 4093) |
| MLAG per-VRF iBGP pool | `192.0.0.0/31` (VLAN 3001 PROD / VLAN 3002 DEV) — same pool, reused per VRF |
| WAN underlay to BB1/BB2 | `172.16.1.0/24` (numbered /31 on Gateway pair) |
| Spanning-tree | MST, priority 0 on VTEPs |

**Per-leaf VLAN/VRF scoping (Domain A):**

| Leaf pair | PROD VLANs | DEV VLANs | MLAG per-VRF SVIs | OISM VRFs |
|---|---|---|---|---|
| A-LEAF1, A-LEAF2 | 10, 30 | — | 3001 (PROD) | PROD only |
| A-LEAF3, A-LEAF4 | 10, 30 | 50 | 3001 (PROD), 3002 (DEV) | PROD + DEV |
| A-LEAF5, A-LEAF6 | — | 50, 70 | 3002 (DEV) | DEV only |
| A-LEAF7, A-LEAF8 (Gateway) | 10 (multi-domain) | 50 (local), 70 (multi-domain) | — | **OISM disabled on Gateway** |

**Hosts (Domain A):**

| Host | Attachment | VLAN | VRF | Multihoming |
|---|---|---|---|---|
| HostA1 | A-LEAF1/2 Port-Channel 7 | 10 | PROD | MLAG |
| HostA2 | A-LEAF1/2 Port-Channel 8 | 30 | PROD | MLAG |
| HostA3 | A-LEAF3 Ethernet7 | 50 | DEV | Single-homed |
| HostA4 | A-LEAF3/4 Port-Channel 8 | 10 | PROD | MLAG |
| HostA5 | A-LEAF4 Ethernet7 | 30 | PROD | Single-homed |
| HostA6 | A-LEAF5/6 Port-Channel 7 | 70 | DEV | MLAG |
| HostA7 | A-LEAF5 Ethernet8 | 50 | DEV | Single-homed |
| HostA8 | A-LEAF7/8 Port-Channel 9 | 50 | DEV | EVPN A/A (ESI `identifier auto lacp`, LACP system-id `c0d6.8200.0000`) |

### Domain B — IS-IS underlay + single-ASN iBGP + All-Active everywhere

| Attribute | Value |
|---|---|
| `fabric_name` | `DOMAIN_B_FABRIC` |
| Underlay routing | IS-IS L2 only, IPv4 address-family, NET `49.1111.0000.0000.[NodeID].00` |
| Overlay routing | iBGP EVPN in AS `65200`, RR on Spines (cluster-id `10.0.2.205`) |
| Multihoming (standard leafs) | EVPN All-Active (Type-1 auto-ESI, LACP-derived) |
| Multihoming (Gateway) | EVPN All-Active (I-ESI `0000:bbbb:0007:0008:0000`, DF preference 2000/1000) |
| Distributed IRB | Symmetric, dual-stack IPv4+IPv6 |
| OISM | IPv4 PIM-SSM underlay group `232.1.1.1` (PROD), plus a `239.0.20.101` overlay group with dedicated `232.1.1.20` encap (illustrating N:1 vs. 1:1 group mapping); IPv6 EVPN multicast per VRF |
| Gateway ASN model | Shared with fabric (`65200`), iBGP peering |
| Loopback0 pool | `10.0.2.0/24` |
| Loopback1 pool (VTEP) | `10.1.2.0/24` (no Loopback2 — no MLAG) |
| Fabric point-to-point | IPv4 unnumbered (`ip address unnumbered Loopback0`) |
| WAN underlay to BB1/BB2 | `172.16.2.0/24` (numbered /31 on Gateway pair) |
| Spanning-tree | MST, `spanning-tree root super` on all standard leafs AND Gateway pair |

**Per-leaf VLAN/VRF scoping (Domain B):**

| Leaf | VLANs | VRF | OISM VRFs | Hosts attached |
|---|---|---|---|---|
| B-LEAF1 | 20, 40 | PROD | PROD | HostB1 (PC7, vlan 20), HostB2 (PC8, vlan 40) |
| B-LEAF2 | (mirror of B-LEAF1) | PROD | PROD | (partner in ES for HostB1/B2) |
| B-LEAF3 | 10, 40 | PROD | PROD | HostB3 (mirroring B-LEAF3/4 pair) |
| B-LEAF4 | 10, 40 | PROD | PROD | HostB4 |
| B-LEAF5 | 40, 80 | PROD + DEV | PROD + DEV | B-SW1 uplink (trunk 40, 80) |
| B-LEAF6 | 40, 80 | PROD + DEV | PROD + DEV | B-SW1 uplink (trunk 40, 80) |
| B-LEAF7, B-LEAF8 (Gateway) | 10 (multi-domain), 60 (local), 70 (multi-domain) | PROD + DEV | **OISM disabled on Gateway** | HostB8 (PC9, vlan 60, EVPN A/A) |

> **Confirmation needed during first render:** the per-leaf VLAN distribution above is derived from a skim of the tech-library configs. If any specific leaf differs (e.g. B-LEAF3/4 carry a different VLAN set than shown), the host_vars will need adjustment. Flagged for review during first `make build` diff.

**Hosts (Domain B) + D-SW1 downstream:**

| Host | Attachment | VLAN | VRF | Multihoming |
|---|---|---|---|---|
| HostB1 | B-LEAF1/2 Port-Channel 7 | 20 | PROD | EVPN A/A |
| HostB2 | B-LEAF1/2 Port-Channel 8 | 40 | PROD | EVPN A/A |
| HostB3, HostB4 | B-LEAF3/4 similar pattern | (10, 40) | PROD | EVPN A/A |
| HostB5, HostB6 | (attached downstream of B-SW1 via VLAN 40 access) | 40 | PROD | Standard access |
| HostB7 | attached downstream of B-SW1 via VLAN 80 access | 80 | DEV | Standard access |
| HostB8 | B-LEAF7/8 Port-Channel 9 | 60 | DEV | EVPN A/A (LACP system-id `c0d6.8200.0008`) |
| B-SW1 | B-LEAF5/6 uplink Port-Channel 1 | trunk 40, 80 | — | EVPN A/A (VTEP side); LACP port-channel (CE side) |

### Backbone — BB1 + BB2 as dedicated node_type

| Attribute | Value |
|---|---|
| Group | `BACKBONE` |
| `fabric_name` | `BACKBONE` |
| Node type | `backbone_router` (custom key defined in `BACKBONE.yml`) |
| Role | EVPN Route Reflectors + IPv4 transport for Domain A + Domain B Gateway inter-domain sessions |
| ASN | `65000` (iBGP, RR-client to all four Gateway nodes) |
| Loopback0 | `10.0.0.1/32` (BB1), `10.0.0.2/32` (BB2) — EVPN RR source |
| Fabric IP schema | `172.16.1.0/24` (BB↔Domain A p2p), `172.16.2.0/24` (BB↔Domain B p2p) |
| MTU | `9214` on the p2p links (backbone tolerates larger frames than leaf-facing 9114) |

**Why AVD-managed:** the BB1/BB2 configs need to stay consistent with the peer descriptions/passwords/route-map names used by both A and B Gateway configs. Rendering them from AVD means one source of truth for the DCI.

**Node_type_keys entry (in `BACKBONE.yml`):**

```yaml
node_type_keys:
  - key: backbone_router
    type: backbone_router
    default_evpn_role: server        # RR on the backbone
    default_overlay_address_families: [evpn]
    connected_endpoints: false        # no host/server attachments
    default_underlay_routing_protocol: none   # no fabric-wide underlay; peerings from Gateways via l3_edge
    interface_descriptions:
      underlay_ethernet_interface: "{{ peer }}"
    structured_config:
      # Backbone-specific structured overrides (RR cluster-id, VRF-less, mgmt gateway)
```

---

## Custom structured configuration — the escape hatches

AVD 6.3.0 covers most of the deployment guide's design natively. These are the specific places where `custom_structured_configuration` is needed:

| Concern | Why native AVD doesn't cover it | Where the CSC lives |
|---|---|---|
| `redistribute router-mac next-hop vtep primary` (MAC-only variant) | AVD 6.3.0 natively renders the `virtual-ip` variant; the paired MAC-only variant is newer TOI (EOS 4.34.0F) and may or may not be exposed as a native key in 6.3.0 | Per-tenant SVI CSC in `DOMAIN_A_SERVICES.yml` / `DOMAIN_B_SERVICES.yml` — **verify during first render whether AVD 6.3.0 emits both natively via an updated `redistribute_router_mac` schema; if yes, drop the CSC.** |
| Peer-tag `SPINES` (`neighbor ... peer-tag in|out SPINES`) | Peer tagging is a newer EOS 4.34.0F feature; likely not in AVD 6.3.0 native | Peer-group CSC in `DOMAIN_A_FABRIC.yml` under `custom_structured_configuration_router_bgp` |
| WAN-facing eBGP session on Gateway pair (peer-group `REMOTE-IPV4-PEERS`, route-map `RM-AS65000-IPV4-OUT`, PL-GATEWAY-LOOP) | AVD's `evpn_gateway` handles the EVPN peering to remote RRs but doesn't handle the WAN IPv4 underlay session or the prefix-list/route-map filtering the Gateway loopbacks | Existing `custom_evpn_gw_bgp_config` + `custom_evpn_gw_prefix_lists` + `custom_evpn_gw_route_maps` in `DOMAIN_A_FABRIC.yml` (already scaffolded; needs refresh to align with current shipped design) |
| Multi-VTEP MLAG (Loopback2 shared VTEP) | AVD 6.3.0 supports this via `vtep_ipv4_pool` + `mlag_shared_vtep`-adjacent keys; need to verify exact 6.3 schema | `DOMAIN_A_FABRIC.yml` l3leaf defaults |
| `vxlan virtual-router encapsulation mac-address mlag-system-id` | Should be native via `virtual_router_mac_address` or a related key in 6.3.0 | Verify during first render |
| Spanning-tree `root super` (Domain B) | AVD 6.3.0 has native `spanning_tree_root_super` under l3leaf defaults; verify | `DOMAIN_B_FABRIC.yml` l3leaf defaults |
| BB1/BB2 backbone_router node_type | Custom node_type by definition | `BACKBONE.yml` |
| BB1↔BB2 iBGP EVPN RR cluster | Handled via `node_type_keys` + a small CSC for cluster-id + RR-client peer-group config | `BACKBONE.yml` |

**The rule:** every CSC block gets a `# CSC:` comment naming *why* it exists and what would remove it (either "AVD native support pending" or "design-specific, no AVD native equivalent").

---

## ANTA test catalog

Six categories, one file per category, all wired into `catalog.yml`. Each test names its scope (which nodes it applies to) via filters.

### 1. `underlay.yml` — Underlay + BGP peerings

- `VerifyInterfacesStatus` — all uplink/peer-link/host-facing/backbone interfaces up
- `VerifyMTU` — all fabric-facing interfaces at `9114`, backbone p2p at `9214`
- `VerifyBGPIPv4UnicastState` — every Domain A eBGP underlay peering `Established` (spine↔leaf, leaf↔MLAG peer, Gateway↔BB)
- `VerifyBGPEVPNState` — every EVPN peering `Established` (A: eBGP; B: iBGP; Gateway↔BB)
- `VerifyISISNeighbors` — Domain B only, all Level-2 IS-IS adjacencies up
- `VerifyBFDPeersState` — multihop BFD sessions on EVPN peerings `Up`
- `VerifyRoutingProtocolModel` — `multi-agent` everywhere

### 2. `overlay.yml` — EVPN state

- `VerifyEVPNType2` — sample host MAC/IP present at every remote VTEP
- `VerifyEVPNType3` — inclusive multicast (IMET) routes present for every configured L2VNI
- `VerifyEVPNType5` — VRF-scoped IP-Prefix routes present at every remote VTEP for the tenant subnets
- `VerifyRouteTargets` — MAC-VRF and IP-VRF import/export RTs match design
- `VerifyVxlanConfigSanity` — VXLAN interface up, expected VNI mappings present, source-interface = Loopback1 (Loopback2 for MLAG-attached in Domain A)
- `VerifyVxlanVniBinding` — VLAN→VNI + VRF→L3VNI mappings intact

### 3. `multihoming_gateway.yml` — MH + Gateway

- `VerifyMlagStatus` — MLAG state `active` on all A-LEAF pairs (skip Domain B, no MLAG)
- `VerifyMlagInterfaces` — MLAG port-channel members up per host
- `VerifyEVPNEthernetSegment` — ESIs learned from all remote All-Active pairs (Domain B, Gateway pairs on both A and B)
- `VerifyDesignatedForwarder` — DF election deterministic per configured preference (2000 wins on LEAF7)
- `VerifyEVPNRouteType4` — Type-4 ES-Discovery routes present for all I-ESIs and standard-leaf A/A ESIs
- `VerifyDPathIdentifier` — Type-2/Type-5 routes crossing the domain boundary carry the expected `local:local` + `99:99` D-PATH stamp (custom check)

### 4. `oism.yml` — Overlay multicast (OISM)

- `VerifyPIMNeighbors` — PIM adjacencies formed on Spine↔Leaf underlay for A-LEAF1..6 and B-LEAF1..6 (Gateway pairs excluded)
- `VerifyPIMSSMState` — SSM (S,G) tree state for the configured overlay/underlay groups per VRF
- `VerifyIGMPState` — Loopback101/102 IGMP source addresses match the design
- `VerifyEVPNMulticastRoutes` — Type-6 (SMET), Type-7, Type-8, Type-10 (S-PMSI A-D) routes exchanged per VRF
- `VerifyMroute` — mroute state per VRF for both v4 and v6 tenant multicast

### 5. `dataplane.yml` — Host-to-host reachability

- Intra-domain L3 (same VRF, cross-VLAN): HostA1 (VLAN 10 PROD) ↔ HostA5 (VLAN 30 PROD)
- Intra-domain L2 (same VLAN, cross-VTEP): HostA1 ↔ HostA4 (both VLAN 10)
- Inter-domain L2 (shared VLAN 10 across Gateway pairs): HostA1 (VLAN 10 PROD) ↔ HostB3 or HostB4 (VLAN 10 PROD)
- Inter-domain L3 (different VLANs, same PROD VRF across domains): HostA5 (VLAN 30 PROD) ↔ HostB1 (VLAN 20 PROD)
- Inter-domain L3 DEV VRF: HostA7 (VLAN 50 DEV) ↔ HostB8 (VLAN 60 DEV) — validates D-PATH loop prevention with Gateway-attached endpoints
- IPv6 counterpart for at least one pair per scope

Uses `VerifyReachability` with source-interface set to the tenant SVI. Requires the hosts (containerlab `linux` kind nodes) to be reachable from the ANTA runner — same MGMT VRF path used for eAPI on the switches.

### 6. `catalog.yml` — Top-level orchestrator

Imports the five concern-specific catalogs and applies them to `all` with per-test node-filter tags so control-plane tests skip B-SW1 (L2-only, no BGP), OISM tests skip the Gateway pair, etc.

---

## Delivery plan (commits)

Executed in this order, each shippable independently:

1. **Commit 1:** Bank this DESIGN.md.
2. **Commit 2:** Refresh `DOMAIN_A_FABRIC.yml` — align pools/OISM groups with current shipped design, add Multi-VTEP MLAG, correct WAN-facing peer-group tuning.
3. **Commit 3:** Refresh `DOMAIN_A_SERVICES.yml` — correct OISM group IPs, add paired-redistribute-router-mac CSC (if not native in 6.3.0).
4. **Commit 4:** Refresh `DOMAIN_A_ENDPOINTS.yml` — add HostA7, HostA8; correct host attachment for the current shipped design.
5. **Commit 5:** Add per-leaf `host_vars/A-LEAF*.yml` — enforce PROD-only / DEV-only / dual-VRF scoping per the table above.
6. **Commit 6:** Add `BACKBONE.yml` + `host_vars/BB1.yml` + `host_vars/BB2.yml` + wire BB1/BB2 into `inventory.yml` as the new `BACKBONE` group.
7. **Commit 7:** Add `DOMAIN_B_FABRIC.yml` — IS-IS underlay + iBGP overlay + A/A everywhere + spanning-tree root super.
8. **Commit 8:** Add `DOMAIN_B_SERVICES.yml` — B's VRFs, SVIs, OISM (including the illustrative 1:1 group `239.0.20.101`→`232.1.1.20`).
9. **Commit 9:** Add `DOMAIN_B_ENDPOINTS.yml` — HostB1..HostB8 + B-SW1 downstream + B-SW1 host_vars.
10. **Commit 10:** Add per-leaf `host_vars/B-LEAF*.yml`.
11. **Commit 11:** Update `inventory.yml` to include `DOMAIN_B_FABRIC` alongside A + BACKBONE.
12. **Commit 12:** Add `anta/` catalog and the six concern-specific test files.
13. **Commit 13:** Update `Makefile` to add `make build-all`, `make deploy-all`, `make validate-all` targets that iterate across all three groups.
14. **Commit 14:** Iterate on any diffs surfaced by `make build` vs. tech-library `.cfg` reference until parity is achieved.

**Verification loop for each commit that changes rendered output:**
```
make build                                                   # renders intended/configs/*.cfg
for h in <affected-nodes>; do
  diff -u intended/configs/${h}.cfg \
    ~/repos/tech-library/docs/data_center/evpnvxlan/deployment_guide/domains_a_b/full_configs/${h}.cfg
done
```
Iterate on `custom_structured_configuration_*` until diff is empty.

---

## Open items to confirm during first render

Flagged for verification when Mitch first runs `make build` and diffs the output:

1. **AVD 6.3.0 native support for paired `redistribute router-mac ... next-hop vtep primary`** — if native, drop the CSC and use the native key.
2. **AVD 6.3.0 native support for peer-tag** — if native, drop the CSC.
3. **`vxlan virtual-router encapsulation mac-address mlag-system-id`** — verify native key exists.
4. **Multi-VTEP MLAG (Loopback2)** — verify `vtep_loopback` + `mlag_shared_vtep`-adjacent 6.3 schema keys.
5. **Domain B `spanning-tree root super`** — verify native key.
6. **BB1/BB2 backbone_router node_type_keys** — first render will surface any schema mismatch.
7. **B-LEAF3/B-LEAF4 exact VLAN set** — the design here assumes VLANs 10, 40 (PROD); verify against tech-library `B-LEAF3.cfg`.
8. **Whether HostA5, HostA7, HostB5, HostB6, HostB7 as containerlab `linux` nodes are reachable from the ANTA runner** — required for dataplane tests. If not, add a MGMT VRF hop or move dataplane tests to a separate catalog gated on an env var.

---

**Ownership:** Mitch Vaughan (`mitch@arista.com`), aclabs precedent — no `Co-authored-by: Claude` trailer on tech-library-adjacent commits.
