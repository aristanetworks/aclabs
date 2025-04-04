# Arista's Tech Library EVPN/VXLAN Domain A Lab

## Overview
This lab has been validated as fully functional with:

- cEOS-lab: 4.33.2F
- AVD: 5.2.3
- ContainerLab: 0.67.0

## Quick Links

[Interactive Lab Topology](#interactive-lab-toplogy)

[Building Configurations](#building-configurations)

[Deploying Configurations](#deploying-configurations)

[Validating the Topology](#validating-the-topology)

[Topology Status](#topology-status)

[Connecting to Nodes via the Terminal](#connecting-to-nodes-via-terminal)

[Starting the Topology](#starting-the-topology)

[Stopping the Topology](#stopping-the-topology)

## Interactive Lab Toplogy

An interactive topology is available via the link below, and can be used to access the nodes via web SSH. All nodes have a username of `admin` and password of `admin`

> [!IMPORTANT]
> Please wait until the postCreate.sh script completes before opening the interactive lab topology link below

[Interactive Lab Topology](https://{{gh.codespace_name}}-8080.app.github.dev/graphite)

## Building Configurations

Pre-built AVD data models are located in the `avd/group_vars` directory. These data models will render configurations for the nodes in Domain A as shown in the EVPN/VXLAN Deployment Guide.

Issuing the below command at the terminal will render all configuration and documentation based on the pre-built data models.

```bash
make build
```

> [!TIP]
> Be sure to explore and experiment with the data models! More information on AVD can be found at https://avd.arista.com.

## Deploying Configurations

Once rendered, the AVD-generated configurations can be deployed to the nodes by issuing the below command at the terminal

```bash
make deploy
```

## Validating the Topology

The [Arista Network Test Automation (ANTA)](https://anta.arista.com/) framework can be used to validate that the topology is built and operational as defined in the AVD data models.

Issue the below command at the terminal will initiate the validation testing.

```
make validate
```

> [!TIP]
> ANTA has an extensive and continually growing [test catalog](https://anta.arista.com/stable/api/tests/). Be sure to explore and test with the available options!

## Additional Tasks

### Topology Status

The current status of the lab environment can be retrieved at any time by issuing the below command at the terminal.

```bash
make inspect
```

This will list the host names and management addresses for all lab devices.

### Connecting to Nodes via Terminal

As an alternative to the [Interactive Lab Topology](https://{{gh.codespace_name}}-8080.app.github.dev/graphite), all nodes can be accessed via SSH directly from the terminal as shown below.

```bash
# the password is `admin`
ssh admin@<a-lab-device-hostname>
```

### Stopping the topology

If needed, the topology can be stopped by issuing the below command at the terminal:

```
make stop
```

### Starting the topology

> [!IMPORTANT]
> The topology is automatically started upon the initial launch of the Codespace lab.

If the topology is stopped for any reason, either manually or automatically due to the user's configured Codespace idle timeout value, it can be restarted by issuing the below command at the terminal:

```
make start
```

# Enjoy the lab!

Last reviewed: January 4th, 2025
