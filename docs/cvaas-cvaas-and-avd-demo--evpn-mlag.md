# CVaaS and AVD Demo, EVPN MLAG

!!! Info "Lab Resource Requirements"

    :fontawesome-solid-tag: **AVD Version:** 6.1.0  
    :fontawesome-solid-microchip: CPUs: 16  
    :fontawesome-solid-gears:  Arch: x86 :material-information-outline:{ title="Works well on ARM if you download the lab to your own machine. Use cEOS-lab ARM image in this case!" }  
    :fontawesome-solid-memory: Memory: 64 GB  
    :fontawesome-solid-hard-drive: Storage: 64 GB  

    :material-alert-circle-outline:{ .heartbeat } Please request high spec Codespace machines from [Github support](https://support.github.com/) first!

[Slides](https://{{gh.org_name}}.github.io/{{gh.repo_name}}/slides/cvaas-cvaas-and-avd-demo--evpn-mlag.html){ target=_blank }  
[PDF Slides](https://{{gh.org_name}}.github.io/{{gh.repo_name}}/pdfs/cvaas-cvaas-and-avd-demo--evpn-mlag.pdf){ target=_blank }

!!! Warning

    Automated CVaaS onboarding support is temporarily removed due to backend change from Codespaces to GCP via [labs.arista.com](https://labs.arista.com/). We are working hard on an improved onboarding feature.
    Onboard the lab manually if required!

## How To Run The Lab

Arista Community Lab is relying on Cloud-based lab environment sponsored by Arista [^1]. To get started, simply sign in at [labs.arista.com](https://labs.arista.com/) and click the button below to launch the lab.

[Start the lab :octicons-play-16:](https://labs.arista.com/launch?lab_type=cvaas-cvaas-and-avd-demo--evpn-mlag&origin=tech-lib){ .md-button .md-button--primary target=_blank}

All lab files are also availble for [download](https://{{gh.org_name}}.github.io/aclabs/lab_archives/cvaas-cvaas-and-avd-demo--evpn-mlag.tar.gz) if you want to run the lab on your own machine. This option is for skilled users only that can manage the environment without extra support.

To run the lab on your own machine, you can download all required files using the button below.

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

## Last Updated

!!! Info "Last reviewed: 21/05/2026"

    Demos and labs reviewed over 6 month age may be outdated.

# Lab Topology

![lab topology](assets/topos/small-l3ls-mlag.png)

# How To Use The Lab

???+ Tip "Wait until all devices will start streaming to CVaaS."

    This may take a while.

```bash
# 1. build configs with AVD
make build
# 2. create CVP change control (1)
make deploy_cvp
# 3. validate the deployment with ANTA
make test
```

1. !!! Tip "Review and execute the change control on CVP when all tasks will be created. If you don't have CVaaS available and prefer to deploy the configuration via eAPI, you can use `make deploy` shortcut instead."

Connect to a host (h01 or h02) and execute `test` alias to confirm connectivity.  
Execute following commands to verify EVPN control plane:

```text
show ip bgp summary
show bgp evpn summary
show bgp evpn route-type ip-prefix ipv4
show bgp evpn route-type mac-ip
```

Do any other testing in the lab.  
You rock! 🚀

[^1]: We removed support for GitHub Codespaces that we used to have in the past due to number of restrictions. Use labs.arista, that is available to any user registered on arista.com!
