# gNMIc Prometheus Grafana Lab

> [!IMPORTANT]
> The average deployment time for this lab is five minutes.
> Issue the `make inspect` command at the terminal to check on the deployment status of the lab.
> Please wait until all nodes are in a `running` state prior to interacting with the lab.

This lab is tested for:

  cEOS-lab version: 4.34.2F
  Containerlab Version: 0.72.1
  Codespace Container Size
    CPUs: 4
    memory: 16 GB
    storage: 48 GB

Last reviewed: 10/12/2025

> Lab Credentials
&nbsp;&nbsp;&nbsp;&nbsp;Username: arista
&nbsp;&nbsp;&nbsp;&nbsp;Password: arista

Please check the lab materials:

- [Lab Documentation](https://{{gh.org_name}}.github.io/{{gh.repo_name}}/telemetry)

## Lab Inventory

This lab has following devices:

| Hostname | Type | OS | Management Address | Username | Password |
| -------- | ---- | -- | ------------------ | -------- | -------- |
| spine1 | switch | cEOS-lab, 4.34.2F | 172.144.100.2 | arista | arista |
| spine2 | switch | cEOS-lab, 4.34.2F | 172.144.100.3 | arista | arista |
| pe11 | switch | cEOS-lab, 4.34.2F | 172.144.100.4 | arista | arista |
| pe12 | switch | cEOS-lab, 4.34.2F | 172.144.100.5 | arista | arista |
| pe21 | switch | cEOS-lab, 4.34.2F | 172.144.100.6 | arista | arista |
| pe22 | switch | cEOS-lab, 4.34.2F | 172.144.100.7 | arista | arista |
| client1 | host | cEOS-lab, 4.34.2F | 172.144.100.8 | arista | arista |
| client2 | host | cEOS-lab, 4.34.2F | 172.144.100.9 | arista | arista |
| client3 | host | cEOS-lab, 4.34.2F | 172.144.100.10 | arista | arista |
| client4 | host | cEOS-lab, 4.34.2F | 172.144.100.11 | arista | arista |

> To access any device, use `ssh <username>@<hostname>` or simply type `<hostname>` to use the SSH alias.
