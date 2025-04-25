# Arista's Tech Library EVPN/VXLAN Domain A Lab

> [!IMPORTANT]
> The average deployment time for this lab is ~10 minutes. Please wait until the `postCreateCommand` process has finished before interacting with the lab.

## Overview

This lab has been built and validated with:

- cEOS-lab: **4.34.0F**
- AVD: **5.2.3**
- ContainerLab: **0.67.0**
- Codespace Machine Type:
  - CPUs: **16**
  - Memory: **64 GB**
  - Storage: **128 GB**

## Credentials

Username: `admin`

Password: `admin`

## Navigating the Lab

Please refer to the [Arista Community Labs QuickStart Guide](https://aclabs.arista.com/quickstart/) for a step-by-step guide on how to navigate the lab.

Quick Links:

- [Interacting with the Lab](https://aclabs.arista.com/quickstart/#interacting-with-the-lab)
- [Tips and Troubleshooting](https://aclabs.arista.com/quickstart/#tips-and-troubleshooting)

## Building Configurations with AVD

Pre-built AVD data models are located in the `avd/group_vars` directory. These data models will render configurations for the nodes in Domain A as shown in the EVPN/VXLAN Deployment Guide.

Issuing the below command at the terminal will render all configuration and documentation based on the pre-built data models.

```bash
make build
```

> [!TIP]
> Be sure to explore and experiment with the data models! More information on AVD can be found at https://avd.arista.com.

## Deploying Configurations with AVD

Once rendered, the AVD-generated configurations can be deployed to the nodes by issuing the below command at the terminal

```bash
make deploy
```

## Validating the Environment with AVD

The [Arista Network Test Automation (ANTA)](https://anta.arista.com/) framework can be used to validate that the topology is built and operational as defined in the AVD data models.

Issue the below command at the terminal will initiate the validation testing.

```bash
make validate
```

> [!TIP]
> ANTA has an extensive and continually growing [test catalog](https://anta.arista.com/stable/api/tests/). Be sure to explore and test with the available options!

Happy Labbing!

Last reviewed: April 25th, 2025
