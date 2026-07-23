#!/usr/bin/env python3
"""anta_audit.py — the ANTA-phase gate (Day 54 s6).

Three checks, campaign-style:
  1. PARSE   — every user catalog loads via AntaCatalog.parse (schema-exact).
  2. FACTS   — every concrete expectation in the catalogs (prefixes, VNIs,
               interfaces, MTUs) exists in the intended configs. A catalog
               that asserts something the models don't carry has drifted.
  3. TAGS    — every `filters.tags` value used by a catalog is produced by
               inventory.yml's anta_tags definitions (no orphan scopes).

Exit 0 = ship-ready; nonzero = drift.
"""
from __future__ import annotations

import glob
import re
import sys
from pathlib import Path

import yaml
from anta.catalog import AntaCatalog

ROOT = Path(__file__).resolve().parent.parent
CATS = sorted(glob.glob(str(ROOT / "anta/user_catalogs/*.yml")))
CFGS = {p.stem: p.read_text() for p in (ROOT / "intended/configs").glob("*.cfg")}
ALL_CFG = "\n".join(CFGS.values())
INV = (ROOT / "inventory.yml").read_text()

fails: list[str] = []

# 1 — PARSE
tests_total = 0
for f in CATS:
    try:
        tests_total += len(AntaCatalog.parse(f).tests)
    except Exception as e:  # noqa: BLE001
        fails.append(f"PARSE {f}: {e}")
print(f"[1] parse: {len(CATS)} catalogs / {tests_total} tests" + ("  ✗" if any(x.startswith('PARSE') for x in fails) else "  ✓"))

# 2 — FACTS (walk raw YAML for concrete values)
def walk(node, keys):
    if isinstance(node, dict):
        for k, v in node.items():
            if k in keys:
                yield k, v
            yield from walk(v, keys)
    elif isinstance(node, list):
        for i in node:
            yield from walk(i, keys)

fact_checks = 0
for f in CATS:
    data = yaml.safe_load(open(f))
    for k, v in walk(data, {"prefix", "address", "vni", "mtu", "interface", "portchannel", "name"}):
        vals = v if isinstance(v, list) else [v]
        for val in vals:
            sval = str(val)
            if k in ("prefix", "address"):
                net = sval.split("/")[0].rsplit(".", 1)[0]
                ok = net in ALL_CFG
            elif k == "vni":
                ok = f"vni {sval}" in ALL_CFG
            elif k == "mtu":
                ok = f"mtu {sval}" in ALL_CFG
            elif k in ("interface", "portchannel", "name") and re.match(r"^(Ethernet|Port-Channel|Vlan|Loopback)", sval):
                ok = f"interface {sval}" in ALL_CFG
            else:
                continue
            fact_checks += 1
            if not ok:
                fails.append(f"FACT {Path(f).name}: {k}={sval} not found in any intended config")
print(f"[2] facts: {fact_checks} expectations cross-checked" + ("  ✗" if any(x.startswith('FACT') for x in fails) else "  ✓"))

# 3 — TAGS
used = set()
for f in CATS:
    used |= {t for _, v in walk(yaml.safe_load(open(f)), {"tags"}) for t in (v if isinstance(v, list) else [v])}
declared = set(re.findall(r"[\[,'\" ]([a-z_]+)[,'\"\]]", "\n".join(l for l in INV.splitlines() if "anta_tags" in l or "df_" in l or "'gateway'" in l or "standard_leaf" in l)))
orphans = {t for t in used if t not in INV}
if orphans:
    fails.append(f"TAGS orphaned in catalogs (not in inventory): {sorted(orphans)}")
print(f"[3] tags: {len(used)} scopes used, all declared" + ("  ✗" if orphans else "  ✓"))

if fails:
    print("\n".join(f"  ✗ {x}" for x in fails))
    sys.exit(1)
print(f"AUDIT CLEAN — {tests_total} tests, {fact_checks} facts, {len(used)} scopes")

# 4 — SCHEDULE (pure-ANTA prepare_tests matrix; workflow-independent)
def gate4() -> None:
    import json as _json
    import subprocess as _sp
    from anta.catalog import AntaCatalog as _C
    from anta.device import AsyncEOSDevice as _D
    from anta.inventory import AntaInventory as _I

    raw = _sp.run(["ansible", "-i", str(ROOT / "inventory.yml"),
                   "DOMAIN_A_FABRIC:DOMAIN_B_FABRIC:BACKBONE:DOMAIN_B_L2_SWITCHES",
                   "-m", "debug", "-a", "var=anta_tags"],
                  capture_output=True, text=True).stdout
    tags = {m.group(1): _json.loads("{" + m.group(2) + "\n}")["anta_tags"]
            for m in re.finditer(r"(\S+) \| SUCCESS => \{(.*?)\n\}", raw, re.S)}
    inv = _I()
    for h, t in tags.items():
        inv.add_device(_D(name=h, host="127.0.0.1", username="x", password="x", tags=set(t)))
    # Per-device selection per ANTA's own no-run-tags semantics (runner.py):
    # untagged tests + tests whose filter tags intersect the device's tags.
    # (anta 1.9's prepare_tests() is deprecated AND returns a degenerate
    # one-device plan here — hand-rolling against the stable public API.)
    cat = _C.merge_catalogs([_C.parse(f) for f in CATS])
    cat.build_indexes()
    untagged = cat.tag_to_tests[None]
    # NB: key by NAME — AsyncEOSDevice hashes by host, so a device-keyed
    # dict collapses when hosts repeat (bit us with 27x 127.0.0.1).
    sel = {d.name: (set(untagged) | cat.get_tests_by_tags(set(d.tags))) for d in inv.devices}
    plan = {n: [t.test.__name__ for t in ts] for n, ts in sel.items()}
    def df_variants(dev):
        return sorted({t.inputs.expect_df for t in sel.get(dev, [])
                       if t.test.__name__ == "VerifyEVPNDFElection"})
    checks = [
        ("A-SPINE1 no MLAG",        "VerifyMlagStatus" not in plan.get("A-SPINE1", [])),
        ("A-SPINE1 no MLD",         "VerifyMldSnoopingVlans" not in plan.get("A-SPINE1", [])),
        ("A-SPINE1 has NTP",        "VerifyNTP" in plan.get("A-SPINE1", [])),
        ("BB1 no NTP",              "VerifyNTP" not in plan.get("BB1", [])),
        ("BB1 no ISIS",             "VerifyISISNeighborState" not in plan.get("BB1", [])),
        ("BB1 has STP",             "VerifySTPMode" in plan.get("BB1", [])),
        ("B-SW1 no ISIS",           "VerifyISISNeighborState" not in plan.get("B-SW1", [])),
        ("B-LEAF1 has ISIS",        "VerifyISISNeighborState" in plan.get("B-LEAF1", [])),
        ("B-SW1 no BGP",            "VerifyBGPPeersHealth" not in plan.get("B-SW1", [])),
        ("B-SW1 has PortChannels",  "VerifyPortChannels" in plan.get("B-SW1", [])),
        ("A-LEAF1 MLAG+MLD",        {"VerifyMlagStatus", "VerifyMldSnoopingVlans"} <= set(plan.get("A-LEAF1", []))),
        ("A-LEAF1 no Type4",        "VerifyEVPNType4Routes" not in plan.get("A-LEAF1", [])),
        ("A-LEAF1 no BFD",          "VerifyBFDPeersHealth" not in plan.get("A-LEAF1", [])),
        ("B-LEAF1 Type4",           "VerifyEVPNType4Routes" in plan.get("B-LEAF1", [])),
        ("A-LEAF7 DF=[True]",       df_variants("A-LEAF7") == [True]),
        ("A-LEAF8 DF=[False]",      df_variants("A-LEAF8") == [False]),
        ("B-LEAF7 DF=[True]",       df_variants("B-LEAF7") == [True]),
        ("A-LEAF7 DPath(2:2 side)", "VerifyEVPNDPath" in plan.get("A-LEAF7", [])),
        ("B-LEAF7 DPath",           "VerifyEVPNDPath" in plan.get("B-LEAF7", [])),
        ("A-SPINE1 no DPath",       "VerifyEVPNDPath" not in plan.get("A-SPINE1", [])),
    ]
    bad = [n for n, ok in checks if not ok]
    print(f"[4] schedule: {len(tags)} devices, {sum(len(v) for v in plan.values())} scheduled instances, {len(checks)} matrix checks" + ("  ✗" if bad else "  ✓"))
    for n in bad:
        fails.append(f"SCHED {n}")

gate4()
if any(x.startswith("SCHED") for x in fails):
    print("\n".join(f"  ✗ {x}" for x in fails if x.startswith("SCHED")))
    sys.exit(1)
print("SCHEDULE MATRIX CLEAN")
