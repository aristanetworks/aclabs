# Repo Upgrade Guardrails

Use this as the local baseline for avoiding common AVD lab upgrade mistakes in this repo.

## What Changed

- Bumped the lab devcontainer image from an AVD 5.7 / Python 3.11 image to an AVD 6.1 / Python 3.12 image.
- Updated lab documentation, README, and slides to match the new tested versions and current review date.
- Reduced stale or obsolete configuration carried over from older AVD versions.

## Guardrails

### 1. Management interface moved from `Management0` to `Management1`

When this repo moved its CVaaS AVD lab to the newer pattern, all of these had to move together:

- `labs/cvaas-cvaas-and-avd-demo--evpn-mlag/avd_inventory/group_vars/all.yml`
- `labs/cvaas-cvaas-and-avd-demo--evpn-mlag/clab/init-configs/*.cfg`
- `labs/cvaas-cvaas-and-avd-demo--evpn-mlag/clab/interface_mapping.json`
- `labs/cvaas-cvaas-and-avd-demo--evpn-mlag/clab/topology.clab.yml`

If you change only `mgmt_interface` and miss the startup configs or interface mapping, the lab will be inconsistent.

### 2. Containerlab needed explicit interface mapping

This repo added `clab/interface_mapping.json` and mounted it into cEOS:

- `interface_mapping.json:/mnt/flash/EosIntfMapping.json:ro`

Without this, cEOS management interface numbering can drift from what the inventory expects.

### 3. `httpapi` labs needed management eAPI enabled

This repo's current pattern includes:

- `management_eapi.enabled: true`
- HTTPS enabled
- MGMT VRF enabled for eAPI

This matches the lab's `ansible_connection: httpapi` flow. If `httpapi` stays enabled and `management_eapi` is missing, automation will fail even if the rest of the inventory looks correct.

### 4. Validation had to move to the current AVD role

This repo replaced the older validation pattern with:

- `ansible.builtin.import_role`
- `name: arista.avd.anta_runner`

Do not assume legacy validation roles are still correct after a major AVD bump.

### 5. Older compatibility settings were removed

This repo removed stale overrides such as:

- `avd_data_validation_mode: error`
- `jinja2_extensions = jinja2.ext.loopcontrols,jinja2.ext.do,jinja2.ext.i18n`

Treat old overrides as suspicious during an upgrade. Keep them only if the target version still requires them.

### 6. Operator workflow and docs changed too

The repo-wide upgrade pattern also includes:

- updated the README/doc/slides AVD version references
- updated the AVD docs URL from the old versioned path to `6.1`
- simplified the documented validation flow
- enabled VS Code automatic tasks in the shared lab-base devcontainer settings

Do not stop after inventory changes. Finish the operator-facing cleanup.

## Fast Search Checklist

Run targeted searches after editing:

```bash
rg -n "Management0|eos_validate_state|avd_data_validation_mode|jinja2_extensions" \
  labs/<lab> docs/<lab>.md slides/<lab>.md .devcontainer/<lab>/devcontainer.json
```

Also search for stale version strings and old AVD doc URLs in the lab README, docs, and slides.
