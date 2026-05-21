# CVaaS and AVD Demo, EVPN MLAG

> [!WARNING]
> This lab is in preview. It's fully functional, but breaking changes can happen.
> We are working hard on building the best lab collection and your feedback is always  appreciated.
>
> Automated CloudVision onboarding is temporarily unavailable in the hosted lab environment.
> Use `make build`, `make deploy`, and `make test` for the default workflow.
> Only use `make deploy_cvp` after manually onboarding the switches to CVaaS and exporting `CVURL` and `CV_API_TOKEN`.

Last reviewed: 21/05/2026

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
