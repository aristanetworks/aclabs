---
marp: true
theme: default
author: Petr Ankudinov
# size 16:9 1280px 720px
size: 16:9
paginate: true
math: mathjax
style: |
    :root {
      background: linear-gradient(to left, #abbaab, #ffffff);
    }
    img[alt~="custom"] {
      float: right;
    }
    .columns {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 1rem;
    }
    footer {
      font-size: 14px;
    }
    section::after {
      font-size: 14px;
    }
    img {
      background-color: transparent;
    }
    pre {
        background: linear-gradient(to top, #abbaab, #ffffff);
        background-color: transparent;
    }
---

# AVD Provisioning on CVaaS

<!-- Do not add page number on this slide -->
<!--
_paginate: false
-->

```text
Provisioning Workflow Demo
Petr Ankudinov
                                    13/01/2025
```

![bg right fit](assets/img/avd-logo.webp)

---

# Agenda

<style scoped>section {font-size: 22px;}</style>

![bg right ](assets/img/pexels-suzy-hazelwood-1226398.jpg)

- Ansible AVD collection overview
- The demo
- Credits and references

---

# What is Ansible AVD?

<style scoped>section {font-size: 20px;}</style>

![bg right fit](assets/img/cvaas-cvaas-and-avd-demo--evpn-mlag/provisioning-building-blocks.png)

- [AVD](https://avd.arista.com/) stands for Arista Validated Design as it was based on the [EVPN Deployment Guide](https://www.arista.com/custom_data/downloads/?f=/support/download/DesignGuides/EVPN_Deployment_Guide.pdf)
- A very successful community project used to deploy EVPN based Data Center fabrics
  - Over [299 stars on Github](https://github.com/aristanetworks/ansible-avd) and 108 contributors as of Nov 2023
  - The most active Arista collection on [Ansible Galaxy](https://galaxy.ansible.com/arista/avd)
- High level workflow:
  - Define abstracted group/host vars using AVD data model
  - Generate low level device specific variables (aka structured configs)
  - Parse templates, build plain text configs
  - Deliver configs to network devices using Ansible `arista.eos.eos_config`

---

# Facts About CVaaS

<style scoped>section {font-size: 22px;}</style>

- CVaaS is cloud based
- Customers are assigned to a region with disaster recovery plan relying on [availability zones (AZ)](https://cloud.google.com/compute/docs/regions-zones)
- CVaaS backups are multi-region
- CVaaS is maintained by a dedicated Cloud SRE team and is always up to date
- Users authenticate to CVaaS via OAuth/SAML providers: Google, Okta, OneLogin, Microsoft Azure AD and custom SAML/OAuth providers
- The API access for AVD orchestration, etc. is authenticated using service account tokens
- The only traffic required is HTTPS initiated by switch to CVaaS with cert based authentication and HTTPS from AVD host to CVaaS with token based authentication
- References:
  - [CVaaS Configuration Guide](https://www.arista.com/en/cg-cv/cv-cloudvision-as-a-service)
  - [CVaaS Quick Start Guide](https://www.arista.com/assets/data/pdf/qsg/qsg-books/QS_CloudVision_as_a_Service.pdf)
  - [CVaaS Security Whitepaper](https://www.arista.com/assets/data/pdf/Whitepapers/CloudVision-as-a-service-security-Whitepaper.pdf)

---

# The Demo

<style scoped>section {font-size: 20px;}</style>

![bg right fit](assets/img/cvaas-cvaas-and-avd-demo--evpn-mlag/demo-setup.png)

- Start container as Github Codespace (or on any host with dev container supporting tool)
- Start a simple leaf-spine topology in Containerlab
- Build EVPN configuration with `arista.avd` Ansible collection
- Wait until the lab switches will start streaming using a pre-defined token
- Deploy configuration to CVP using `arista.avd` Ansible collection and pre-defined API token
- Create change control, review and execute the change

---

# Credits and References

<style scoped>section {font-size: 12px;}</style>

This repository is based on many awesome open source repositories and some free/commercial Github features:

Tool | Purpose
-----|------------
[VS Code](https://code.visualstudio.com/) | create this repository code
[DevContainers](https://code.visualstudio.com/docs/remote/containers) | our topic for today
[Marpit](https://marp.app/) | Markdown slide deck framework
[Github Actions](https://github.com/features/actions) | build slides and containers
[Github Pages](https://pages.github.com/) | publish slides
[Github Packages](https://github.com/features/packages) | publish containers
[Github Codespaces](https://github.com/features/codespaces) | run the demo container
[Carbon](https://carbon.now.sh/) | code snippets
[Pexels](https://www.pexels.com/) and [Unsplash](https://unsplash.com/) | Excellent free stock photos resources. It's not possible to reference every author individually, but their work is highly appreciated.
[excalidraw](https://github.com/excalidraw/excalidraw), [drawio](https://github.com/jgraph/drawio), [tldraw](https://github.com/tldraw/tldraw) | VSCode plugins to create drawings
[Containerlab](https://containerlab.dev) | Orchestration tool for container based networking labs
[Arista AVD Ansible Collection](https://avd.arista.com/4.3/index.html) | Ansible collection used to build EVPN network
[Ansible](https://www.ansible.com) | Automation for everyone.

---

<style scoped>section {font-size: 45px;}</style>

![bg left opacity:80%](assets/img/pexels-ann-h-7186206.jpg)

# Q&A

- [Ansible AVD](https://avd.arista.com/)
- [This repository](https://github.com/{{gh.repository}})
