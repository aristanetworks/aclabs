# ATD Dual DC

!!! Warning "Container Requirements"

    :fontawesome-solid-microchip: CPUs: 16  
    :fontawesome-solid-memory: Memory: 64 GB  
    :fontawesome-solid-hard-drive: Storage: 128 GB  

    :material-alert-circle-outline:{ .heartbeat } Please request high spec Codespace machines from [Github support](https://support.github.com/) first!

## How To Run The Lab

Please read the [Quickstart guide](https://ankudinov.github.io/aclabs/quickstart/) before using the lab.

You can run the lab on [Github Codespaces](https://codespaces.new/{{gh.repository}}/tree/{{gh.branch}}?quickstart=1&devcontainer_path=.devcontainer%2Fatd-atd-dual-dc%2Fdevcontainer.json) or your own machine.

[Start :octicons-play-16: "ATD Dual DC" in Codespace :octicons-mark-github-24:](https://codespaces.new/{{gh.repository}}/tree/{{gh.branch}}?quickstart=1&devcontainer_path=.devcontainer%2Fatd-atd-dual-dc%2Fdevcontainer.json){ .md-button .md-button--primary target=_blank}

To run the lab on your own machine, you can download all required files using the button below.

[Download all required lab files](https://{{gh.org_name}}.github.io/aclabs/lab_archives/atd-atd-dual-dc.tar.gz){ .md-button .md-button--primary target=_blank}

> WARNING: Currently only x86 hosts are supported. cEOS-lab for ARM is not yet available and it's not possible to start the lab on your MacBook yet.

!!! info "Environment variables and secrets"

    This lab requires following environment variables and secrets to be set.

    `ARISTA_TOKEN` - the token required to download cEOS-lab image from [arista.com](https://arista.com).

    When starting the lab on Github Codespaces, the required data can be provided via `Create codespace` form if not yet associated with the repository. When running the lab on your own machine - set corresponding environment variables **BEFORE** :warning: opening the VSCode.

???+ Tip "Wait until the lab is ready"

    When lab container starts, the `postCreate.sh` takes care of cEOS-lab image download and making some last minute changes in the lab environment. After that, `make start` shortcut is executed to start the lab.
    This requires a some time. :stopwatch: Please be patient. :coffee: :croissant:
    Sometimes cEOS-lab image download may fail. For example, due to incorrect token. In that case `postCreate.sh` script will fail and the lab will not be started.  
    You can confirm if image was imported correctly with `docker image ls`.  

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

## Last Updated

!!! Info "Last reviewed: 22/11/2025"

    Demos and labs reviewed over 6 month age may be outdated.

# Lab Topology

![lab topology](assets/img/atd-atd-dual-dc/atd-topo-dual-dc.png)

!!! Warning "Lab Documents Not Finished"

    DO NOT ENTER! :skull_and_crossbones:{ .heartbeat }

    ![stay back](assets/img/pexels-danne-555709.jpg)

    This document is created from a template.
    If you see this message - the lab is not finished and likely published for testing purposes.
    Don't use it unless you are the author or helping to test it.
