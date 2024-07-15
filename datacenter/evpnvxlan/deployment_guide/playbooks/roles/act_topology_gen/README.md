# act_topology_gen

## Overview

**act_topology_gen** is a role that generates an Arista Clout Test topology file based on AVD fabric.

The **act_topology_gen** role:

- Designed to create valid ACT topology file based on your AVD network model.

### Tasks

1. Create lab topology folder
2. Collect host variables
3. Generate ACT topology file

### Role Variables

```yaml
# vEOS Image and parameters to use
veos_version: < valid EOS version supported in ACT, default -> 4.28.0F >
act_veos_username: < veos username, default -> cvpadmin >
act_veos_password: < veos password, default -> arista123 >

# Options to add cvp, ansible node and connected nodes to topology
act_add_cvp: < true | false, default -> true >
act_add_ansible_node: < true | false, default -> true >

# Generic node options
act_generic_user: < generic node username, default -> cvpadmin >
act_generic_password: < generic node password, default -> arista123 >
act_generic_os_version: < valid act generic node os, default -> Rocky-8.5 >
act_ansible_node_ip: < ansible node ip, default -> 192.168.0.6 >

# CVP node options
act_cvp_version: < valid act cvp node version, default -> 2022.2.1 >
act_cvp_user: < cvp root user, default -> root >
act_cvp_password: < cvp root password, default -> cvproot >
act_cvp_ip: < cvp node tun0 ip, default -> 192.168.0.5 >
```

### Example Playbooks

Inserted into basic AVD fabric deployment playbook

```yaml
---

- name: Build Switch configuration
  hosts: branch_a_fabric
  connection: local
  gather_facts: false
  collections:
    - arista.avd

  tasks:

    - name: Generate AVD intended variables
      import_role:
        name: arista.avd.eos_designs

    - name: Generate device intended config and documentation
      import_role:
        name: eos_cli_config_gen

    - name: Build an ACT topolgy
      import_role:
        name: arista.avd.act_topology_gen
      vars:

```
