# ATD Dual DC

> [!WARNING]
> This lab is in preview. It's fully functional, but breaking changes can happen.
> We are working hard on building the best lab collection and your feedback is always  appreciated.

This lab is tested for:  

  cEOS-lab version: 4.34.2F  
  Containerlab Version: 0.71.1  
  Codespace Container Size  
    CPUs: 16  
    memory: 64 GB  
    storage: 128 GB  

Last reviewed: 22/11/2025  

> Lab Credentials  
&nbsp;&nbsp;&nbsp;&nbsp;Username: arista  
&nbsp;&nbsp;&nbsp;&nbsp;Password: arista  

Please check the lab materials:

- [Lab Documentation](https://{{gh.org_name}}.github.io/{{gh.repo_name}}/atd-atd-dual-dc/)
- [HTML Slides](https://{{gh.org_name}}.github.io/{{gh.repo_name}}/slides/atd-atd-dual-dc.html)
- [PDF Slides](https://{{gh.org_name}}.github.io/{{gh.repo_name}}/pdfs/atd-atd-dual-dc.pdf)

## Lab Inventory

This lab has following devices:

| Hostname | Type | OS | Management Address | Username | Password |
| -------- | ---- | -- | ------------------ | -------- | -------- |
| s1-spine1 | switch | cEOS-lab, 4.34.2F | 192.168.0.10 | arista | arista |
| s1-spine2 | switch | cEOS-lab, 4.34.2F | 192.168.0.11 | arista | arista |
| s1-leaf1 | switch | cEOS-lab, 4.34.2F | 192.168.0.12 | arista | arista |
| s1-leaf2 | switch | cEOS-lab, 4.34.2F | 192.168.0.13 | arista | arista |
| s1-leaf3 | switch | cEOS-lab, 4.34.2F | 192.168.0.14 | arista | arista |
| s1-leaf4 | switch | cEOS-lab, 4.34.2F | 192.168.0.15 | arista | arista |
| s1-brdr1 | switch | cEOS-lab, 4.34.2F | 192.168.0.100 | arista | arista |
| s1-brdr2 | switch | cEOS-lab, 4.34.2F | 192.168.0.101 | arista | arista |
| s2-spine1 | switch | cEOS-lab, 4.34.2F | 192.168.0.20 | arista | arista |
| s2-spine2 | switch | cEOS-lab, 4.34.2F | 192.168.0.21 | arista | arista |
| s2-leaf1 | switch | cEOS-lab, 4.34.2F | 192.168.0.22 | arista | arista |
| s2-leaf2 | switch | cEOS-lab, 4.34.2F | 192.168.0.23 | arista | arista |
| s2-leaf3 | switch | cEOS-lab, 4.34.2F | 192.168.0.24 | arista | arista |
| s2-leaf4 | switch | cEOS-lab, 4.34.2F | 192.168.0.25 | arista | arista |
| s2-brdr1 | switch | cEOS-lab, 4.34.2F | 192.168.0.200 | arista | arista |
| s2-brdr2 | switch | cEOS-lab, 4.34.2F | 192.168.0.201 | arista | arista |
| s1-host1 | host | cEOS-lab, 4.34.2F | 192.168.0.16 | arista | arista |
| s1-host2 | host | cEOS-lab, 4.34.2F | 192.168.0.17 | arista | arista |
| s2-host1 | host | cEOS-lab, 4.34.2F | 192.168.0.26 | arista | arista |
| s2-host2 | host | cEOS-lab, 4.34.2F | 192.168.0.27 | arista | arista |

> To access any device, use `ssh <username>@<hostname>` or simply type `<hostname>` to use the SSH alias.
