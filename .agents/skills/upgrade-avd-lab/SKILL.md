---
name: upgrade-avd-lab
description: Upgrade an AVD-based lab in this repository by following the repo's local upgrade guardrails. Use when bumping arista.avd, cEOS/containerlab versions, devcontainer lab-base image tags, management interface mappings, validation playbooks, or matching README/docs/slides for a lab under labs/.
---

# Upgrade AVD Lab

Use this skill when a user asks to upgrade an AVD lab in this repo.

Keep the workflow tight:

1. Identify the target lab and read the live files first:
   - `labs/<lab>/README.md`
   - `docs/<lab>.md` when present
   - `slides/<lab>.md` when present
   - `.devcontainer/<lab>/devcontainer.json` when present
   - `labs/<lab>/avd_inventory/group_vars/all.yml`
   - `labs/<lab>/avd_inventory/playbooks/avd_validate.yml`
   - `labs/<lab>/avd_inventory/ansible.cfg`
   - `labs/<lab>/clab/topology.clab.yml`
   - `labs/<lab>/clab/init-configs/*.cfg`

2. Read [references/repo-upgrade-guardrails.md](references/repo-upgrade-guardrails.md) before editing if the lab uses Containerlab, cEOS, CVaaS, or `ansible_connection: httpapi`.

3. Upgrade versions consistently across code and docs. Do not bump only one layer.
   - Update the lab devcontainer image tag in `.devcontainer/<lab>/devcontainer.json`.
   - Update tested versions in `labs/<lab>/README.md`.
   - Update matching `docs/` and `slides/` content, including AVD doc links and review dates.
   - If the upgrade needs a newer shared base image behavior, update shared devcontainer settings only when the change is broadly required.

4. Apply the repo upgrade guardrails.
   - For AVD 6.1 style cEOS labs in this repo, use `Management1`, not `Management0`.
   - If management moved to `Management1`, update all related places together:
     - `group_vars/all.yml` `mgmt_interface`
     - `clab/init-configs/*.cfg` interface definitions
     - `clab/init-configs/*.cfg` NTP local-interface lines
     - `clab/interface_mapping.json`
     - `clab/topology.clab.yml` bind mount for `/mnt/flash/EosIntfMapping.json`
   - If the lab deploys through `httpapi`, ensure `management_eapi` is enabled on the `MGMT` VRF.
   - Replace legacy validation playbooks with the current AVD-compatible role used by this repo. In this repo, the current pattern is `arista.avd.anta_runner`.
   - Remove stale compatibility overrides unless the target version still requires them. In this repo that has included:
      - `avd_data_validation_mode: error`
      - `jinja2_extensions` in `ansible.cfg`
   - If lab startup depends on VS Code automatic tasks, confirm `containers/lab-base/.devcontainer/settings.json` allows them.

5. Reconcile the operator workflow after the version bump.
   - Re-read `Makefile`, task definitions, or README command sequences if present.
   - Remove or update deprecated steps instead of preserving outdated instructions.

6. Validate with focused searches before broader testing.
   - Search for stale `Management0`, `eos_validate_state`, `avd_data_validation_mode`, and `jinja2_extensions`.
   - Search docs for old AVD version strings and outdated URLs.
   - If feasible, run the lab's lightweight validation path after edits.

## Common Errors To Avoid

- Updating `mgmt_interface` but forgetting `clab/init-configs` or interface mapping.
- Switching to `httpapi` or keeping it enabled without configuring `management_eapi`.
- Updating the lab README but not the devcontainer image tag.
- Updating the collection version but leaving old AVD documentation links behind.
- Keeping obsolete validation or workflow steps because they "used to work" on the previous AVD release.

## Notes

- In this repo, tracked repo-local skills belong under `.agents/skills`. Do not store repo skills under `.codex/skills`, because `.gitignore` ignores that path.
- Keep edits minimal and aligned with the target lab. Only touch shared files when the upgrade genuinely requires shared behavior changes.
