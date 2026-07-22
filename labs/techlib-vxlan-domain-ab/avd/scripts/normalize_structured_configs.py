#!/usr/bin/env python3
"""Normalize AVD structured configs for startup-config line parity.

PARITY-LEDGER class 9: eos_designs hardcodes `shutdown: false` on every
interface it generates (27 setter sites, no fabric knob in 6.3.0), and
eos_cli_config_gen renders that as an explicit `no shutdown` — a line a
switch never saves (default state). This script strips `shutdown: false`
from interface lists in the structured-config YAMLs between the
eos_designs and eos_cli_config_gen roles (the role re-reads the files:
`read_structured_config_from_file` defaults true).

Deliberately narrow:
- ONLY the interface lists named below.
- ONLY deletes the key when its value is exactly False.
- `shutdown: true` (a genuinely disabled interface) is PRESERVED.
- Management API / SSH `no shutdown` (the guide's 56 legit lines) render
  from management_* keys, untouched here.

Usage: normalize_structured_configs.py <structured_configs_dir>
"""
import sys
from pathlib import Path

import yaml

INTERFACE_LISTS = (
    "ethernet_interfaces",
    "port_channel_interfaces",
    "loopback_interfaces",
    "vlan_interfaces",
    "management_interfaces",
    "tunnel_interfaces",
    "dps_interfaces",
)


def normalize(doc: dict) -> int:
    stripped = 0
    for key in INTERFACE_LISTS:
        for intf in doc.get(key) or []:
            if isinstance(intf, dict) and intf.get("shutdown") is False:
                del intf["shutdown"]
                stripped += 1
    return stripped


def main() -> int:
    target = Path(sys.argv[1])
    total_files = total_stripped = 0
    for f in sorted(target.glob("*.yml")):
        doc = yaml.safe_load(f.read_text())
        if not isinstance(doc, dict):
            continue
        n = normalize(doc)
        if n:
            f.write_text(yaml.safe_dump(doc, sort_keys=False, width=120))
            total_files += 1
            total_stripped += n
    print(f"normalize_structured_configs: stripped {total_stripped} "
          f"default shutdown keys across {total_files} files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
