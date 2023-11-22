# Datacenter AVD Models

## Project directory structure
```
├── backbone
│   ├── group_vars
│   │   ├── BACKBONE.yml
│   │   └── FABRIC.yml
│   └── inventory.yml
├── domain-a
│   ├── group_vars
│   │   ├── ACT.yml
│   │   ├── CONNECTED_ENDPOINTS.yml
│   │   ├── DCI.yml
│   │   ├── DOMAIN_A.yml
│   │   ├── DOMAIN_A_EVPNGW.yml
│   │   ├── DOMAIN_A_L3_LEAVES.yml
│   │   ├── DOMAIN_A_SPINES.yml
│   │   └── FABRIC.yml
│   ├── host_vars
│   └── inventory.yml
├── domain-b
│   ├── group_vars
│   │   ├── ACT.yml
│   │   ├── CONNECTED_ENDPOINTS.yml
│   │   ├── DCI.yml
│   │   ├── DOMAIN_B.yml
│   │   ├── DOMAIN_B_EVPNGW.yml
│   │   ├── DOMAIN_B_L2_SW.yml
│   │   ├── DOMAIN_B_L3_LEAVES.yml
│   │   ├── DOMAIN_B_SPINES.yml
│   │   └── FABRIC.yml
│   ├── host_vars
│   └── inventory.yml
├── domain-c
│   ├── group_vars
│   │   ├── ACT.yml
│   │   ├── CONNECTED_ENDPOINTS.yml
│   │   ├── DCI.yml
│   │   ├── DOMAIN_C.yml
│   │   ├── DOMAIN_C_EVPNGW.yml
│   │   ├── DOMAIN_C_L3_LEAVES.yml
│   │   ├── DOMAIN_C_SPINES.yml
│   │   └── FABRIC.yml
│   ├── host_vars
│   └── inventory.yml
├── global_vars
│   ├── evpn_vxlan
│   │   └── NETWORK_SERVICES.yml
│   ├── management.yml
│   ├── node-types.yml
│   ├── routing-defaults.yml
│   └── switching-defaults.yml
└── playbooks
    ├── fabric-build.yml
    ├── fabric-deploy-cvp.yml
    └── fabric-deploy-eapi.yml
```
## Build

Build specific domain
```
make build-domain-<domain>
```

Build backbone
```
make build-backbone
```

Build all
```
make build-domain-a build-domain-b build-domain-c build-backbone
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
