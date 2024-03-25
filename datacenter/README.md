# Datacenter AVD Models

## Project directory structure
```
── datacenter
│   ├── Makefile
│   ├── README.md
│   ├── act-inventory.yml
│   ├── ansible.cfg
│   ├── backbone
│   │   ├── group_vars
│   │   │   ├── ACT.yml
│   │   │   ├── BACKBONE.yml
│   │   │   └── FABRIC.yml
│   │   ├── host_vars
│   │   │   ├── BB1.yml
│   │   │   └── BB2.yml
│   │   └── inventory.yml
│   ├── domain-a
│   │   ├── group_vars
│   │   │   ├── ACT.yml
│   │   │   ├── CONNECTED_ENDPOINTS.yml
│   │   │   ├── DOMAIN_A.yml
│   │   │   ├── DOMAIN_A_EVPNGW.yml
│   │   │   ├── DOMAIN_A_L3_LEAVES.yml
│   │   │   ├── DOMAIN_A_SPINES.yml
│   │   │   └── FABRIC.yml
│   │   └── inventory.yml
│   ├── domain-b
│   │   ├── group_vars
│   │   │   ├── ACT.yml
│   │   │   ├── CONNECTED_ENDPOINTS.yml
│   │   │   ├── DOMAIN_B.yml
│   │   │   ├── DOMAIN_B_EVPNGW.yml
│   │   │   ├── DOMAIN_B_L2_SW.yml
│   │   │   ├── DOMAIN_B_L3_LEAVES.yml
│   │   │   ├── DOMAIN_B_SPINES.yml
│   │   │   └── FABRIC.yml
│   │   ├── host_vars
│   │   │   ├── B-LEAF7.yml
│   │   │   └── B-LEAF8.yml
│   │   └── inventory.yml
│   ├── domain-c
│   │   ├── group_vars
│   │   │   ├── ACT.yml
│   │   │   ├── CONNECTED_ENDPOINTS.yml
│   │   │   ├── DOMAIN_C.yml
│   │   │   ├── DOMAIN_C_EVPNGW.yml
│   │   │   ├── DOMAIN_C_L3_LEAVES.yml
│   │   │   ├── DOMAIN_C_SPINES.yml
│   │   │   └── FABRIC.yml
│   │   ├── host_vars
│   │   │   ├── C-LEAF7.yml
│   │   │   └── C-LEAF8.yml
│   │   └── inventory.yml
│   ├── domain-d
│   │   ├── group_vars
│   │   │   ├── ACT.yml
│   │   │   ├── CONNECTED_ENDPOINTS.yml
│   │   │   ├── DOMAIN_D.yml
│   │   │   ├── DOMAIN_D_EVPNGW.yml
│   │   │   ├── DOMAIN_D_L3_LEAVES.yml
│   │   │   ├── DOMAIN_D_SPINES.yml
│   │   │   └── FABRIC.yml
│   │   └── inventory.yml
│   ├── global_vars
│   │   ├── avd_defaults
│   │   │   ├── node-types.yml
│   │   │   └── variable-options.yml
│   │   ├── evpn_vxlan
│   │   │   └── NETWORK_SERVICES.yml
│   │   └── fabric_defaults
│   │       ├── management.yml
│   │       ├── routing-defaults.yml
│   │       └── switching-defaults.yml
│   ├── playbooks
│   │   ├── fabric-build.yml
│   │   ├── fabric-deploy-cv-ci.yml
│   │   ├── fabric-deploy-cvp.yml
│   │   ├── fabric-deploy-eapi.yml
│   │   ├── fabric-validate-state.yml
│   │   ├── server-deploy-eapi.yml
│   │   └── templates
│   │       ├── af-evpn.j2
│   │       └── vxlan-mcast-overlay.j2
│   ├── scripts
│   │   └── convert_inventory.py
│   └── tl-act-topology.yml
```

## Update inventory

Update domain-x inventory `ansible_host` IP's with ACT Lab inventory `ansible_host` IP's
```
make replace-domain-<domain>-inventory
```
## Build

Build specific domain
```
make build-domain-<domain>
```

Build all
```
make build-domain-a build-domain-b build-domain-c build-domain-d build-domain-backbone
```
## Deploy

Deploy using eapi
```
make deploy-eapi-domain-<domain>
```

Deploy using cvp
```
make deploy-cvp-domain-<domain>
```
