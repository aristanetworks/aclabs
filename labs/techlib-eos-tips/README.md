# Arista EOS Tips for Network Operators

> [!IMPORTANT]
> The average deployment time for this lab is ~5 minutes. Please wait until the `postCreateCommand` process has finished before interacting with the lab.

This pre-configured lab is intended to be used as a sandbox companion to the [EOS Tips for Network Operators Guide](https://tech-library.arista.com/eos/eos_ops/) in [Arista's Tech Library](https://tech-library.arista.com/).

It has been built and validated with:

- cEOS-lab: **4.33.2F**
- Containerlab: **0.67.0**
- Codespace Machine Type:
  - CPUs: **4**
  - Memory: **16 GB**
  - Storage: **32 GB**

Last reviewed: April 4th, 2025

## Topology

<img src="images/eos-tips-topo.png" width="1080"/>

## Credentials

Username: `admin`

Password: `admin`

## Accessing the Lab

Accessing the nodes in the topology is accomplished via the ContainerLab VSCode Extension.

Begin by opening the extension by clicking the icon found on the lefthand side of the Codespace:

![ContainerLab Extension](images/cLabextension.png)

Once opened, expand the topology by using the dropdown button next to the topology name:

![ContainerLab Extension Dropdown](images/clabextension2.png)

Next, right-click on any node in the topology and select `Connect to SSH`

![ContainerLab Extension Connect SSH](images/clabextension3.png)

A new terminal tab will be opened, with a prompt requesting the password for the node. Enter `admin` to connect:

![ContainerLab Extension Connect SSH](images/clabextension4.png)

Happy Labbing!
