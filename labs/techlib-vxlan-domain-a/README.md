# TechLibrary EVPN Domain-A Lab

This lab is tested for:  

  cEOS-lab version: 4.32.2.1F  
  Codespace Container Size  
    CPUs: 16  
    memory: 64 GB  
    storage: 128 GB  

## Interactive Lab Toplogy

> [!IMPORTANT]
> Please wait until the postCreate.sh script completes before opening the interactive lab topology link below

[Interactive Lab Topology](https://{{gh.codespace_name}}-8080.app.github.dev/graphite)

To inspect the lab details use `make inspect` shortcut. This will list the host names and management addresses for all lab devices.
To connect to any device use:

```bash
# the password is `admin`
ssh admin@<a-lab-device-hostname>
```

To check connectivity, ssh to any host and use `pingcheck ipv4_vrf_prod` or `pingcheck ipv4_vrf_dev` to start fping to the lab hosts. You have to wait a few minutes after the lab start for ping to be successful.

Enjoy the lab!

Last reviewed: December 2nd, 2024
