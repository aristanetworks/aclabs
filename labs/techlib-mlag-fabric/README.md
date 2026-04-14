<!-- lab-dashboard:metadata-start -->

# Arista MLAG Fabric with VXLAN Flood and Learn

_Welcome! This pre-configured lab matches the [MLAG Fabric Deployment Guide](https://tech-library.arista.com/data_center/evpnvxlan/deployment_guide/domain_a/) on [Arista's Tech Library](https://arista.com/en/tech-library)._

> [!WARNING]
> This lab is in preview. It's fully functional, but breaking changes can happen. We are working hard on building the best lab collection and your feedback is always appreciated.

📖 **Deployment Guide:** [Tech Library](https://tech-library.arista.com/data_center/mlag-fabric/deployment_guide/)

🔐 **Credentials**

| Username | Password |
|----------|----------|
| `admin` | `admin` |

<!-- lab-dashboard:metadata-end -->

## Interacting with the Lab

> [!TIP]
> Quickly validate reachability between hosts in the lab by opening an SSH session to any Linux end host in the topology and running the following the command in the terminal window:
>
> ```bash
>pingcheck.sh
>```

### Topology Viewer

The [ContainerLab VS Code Extension](https://containerlab.dev/manual/vsc-extension/) is pre-installed in the lab. For the best experience, it's recommended to use the [Topology Viewer](https://containerlab.dev/manual/vsc-extension/#topoviewer) to interact with the lab.

Topology Viewer can be opened by selecting the ContainerLab extension icon and then the lab.

<figure>
    <img src="assets/images/topo-extension.png"
         alt="Topology Viewer"
         width="325">
</figure>

### SSH

Once in the Topology viewer, SSH to a node by right-clicking it and selecting `SSH`. This will open up a new terminal window containing the SSH session to the node.

<figure>
    <img src="assets/images/topo-ssh.png"
         alt="Topology Viewer"
         width="250">
</figure>

### Packet Capture

Start a data-plane packet capture by right-clicking on a link and selecting the Wireshark icon associated with the link you'd like to capture

<figure>
    <img src="assets/images/topo-pcap.png"
         alt="Topology Viewer"
         width="450">
</figure>

Additional information related to navigating the Topology Viewer UI can be found by selecting the `Shortcuts` icon from within the UI

<figure>
    <img src="assets/images/topo-shortcuts.png"
         alt="Topology Viewer"
         width="350">
</figure>

### AVD

The [AVD](https://avd.arista.com) data models used to render the configuration in the lab are included within the `avd` directory. The [AVD ansible galaxy collection](https://galaxy.ansible.com/ui/repo/published/arista/avd/) is pre-installed in the lab environment, and can be used to initiate a build, deploy, or validation of the topology.

#### Build

```bash
make build
```
#### Deploy

```bash
make deploy
```

#### Validate

```bash
make validate
```

Happy Labbing! 🥳🧪

Last reviewed: March 12th, 2026
