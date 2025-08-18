# CVaaS and AVD Demo, EVPN MLAG

This lab is tested for:  

  cEOS-lab version: 4.34.2F  
  Containerlab Version: 0.61.0  
  Codespace Container Size  
    CPUs: 8  
    memory: 32 GB  
    storage: 64 GB  

Last reviewed: 13/01/2025  

> Lab Credentials  
&nbsp;&nbsp;&nbsp;&nbsp;Username: arista  
&nbsp;&nbsp;&nbsp;&nbsp;Password: arista  

Please check the lab materials:

- [Lab Documentation](https://{{gh.org_name}}.github.io/{{gh.repo_name}}/cvaas-cvaas-and-avd-demo--evpn-mlag/)
- [HTML Slides](https://{{gh.org_name}}.github.io/{{gh.repo_name}}/slides/cvaas-cvaas-and-avd-demo--evpn-mlag.html)
- [PDF Slides](https://{{gh.org_name}}.github.io/{{gh.repo_name}}/pdfs/cvaas-cvaas-and-avd-demo--evpn-mlag.pdf)

## Lab Inventory

This lab has following devices:

| Hostname | Type | OS | Management Address | Username | Password |
| -------- | ---- | -- | ------------------ | -------- | -------- |
| s01 | switch | cEOS-lab, 4.34.2F | 10.0.1.1 | arista | arista |
| s02 | switch | cEOS-lab, 4.34.2F | 10.0.1.2 | arista | arista |
| l01 | switch | cEOS-lab, 4.34.2F | 10.0.2.1 | arista | arista |
| l02 | switch | cEOS-lab, 4.34.2F | 10.0.2.2 | arista | arista |
| l03 | switch | cEOS-lab, 4.34.2F | 10.0.2.3 | arista | arista |
| l04 | switch | cEOS-lab, 4.34.2F | 10.0.2.4 | arista | arista |
| h01 | host | cEOS-lab, 4.34.2F | 10.0.3.1 | arista | arista |
| h02 | host | cEOS-lab, 4.34.2F | 10.0.3.2 | arista | arista |

> To access any device, use `ssh <username>@<hostname>` or simply type `<hostname>` to use the SSH alias.
