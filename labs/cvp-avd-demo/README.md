# CVP and AVD Demo, EVPN MLAG

> [!WARNING]
> This lab is in preview. It's fully functional, but breaking changes can happen.
> We are working hard on building the best lab collection and your feedback is always  appreciated.

Last reviewed: 05/10/2026

> Lab Credentials<br>
&nbsp;&nbsp;&nbsp;&nbsp;Username: {{aclabs.lab_username}}<br>
&nbsp;&nbsp;&nbsp;&nbsp;Password: {{aclabs.lab_password}}

This lab intentionally ships without separate docs or slide content.

# How To Access CVP

To access CloudVision UI click [this link]({{aclabs.cvp_url}})

## Lab Inventory

This lab has following devices:

| Hostname | Type | OS | Management Address | Username | Password |
| -------- | ---- | -- | ------------------ | -------- | -------- |
| s01 | switch | cEOS-lab, 4.34.2F | 10.0.1.1 | {{aclabs.lab_username}} | {{aclabs.lab_password}} |
| s02 | switch | cEOS-lab, 4.34.2F | 10.0.1.2 | {{aclabs.lab_username}} | {{aclabs.lab_password}} |
| l01 | switch | cEOS-lab, 4.34.2F | 10.0.2.1 | {{aclabs.lab_username}} | {{aclabs.lab_password}} |
| l02 | switch | cEOS-lab, 4.34.2F | 10.0.2.2 | {{aclabs.lab_username}} | {{aclabs.lab_password}} |
| l03 | switch | cEOS-lab, 4.34.2F | 10.0.2.3 | {{aclabs.lab_username}} | {{aclabs.lab_password}} |
| l04 | switch | cEOS-lab, 4.34.2F | 10.0.2.4 | {{aclabs.lab_username}} | {{aclabs.lab_password}} |
| h01 | host | cEOS-lab, 4.34.2F | 10.0.3.1 | {{aclabs.lab_username}} | {{aclabs.lab_password}} |
| h02 | host | cEOS-lab, 4.34.2F | 10.0.3.2 | {{aclabs.lab_username}} | {{aclabs.lab_password}} |

> To access any device, use `ssh <username>@<hostname>` or simply type `<hostname>` to use the SSH alias.
