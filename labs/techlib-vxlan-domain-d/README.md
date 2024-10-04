# TechLibrary EVPN Domain-D Lab

This lab is tested for:  

  cEOS-lab version: 4.32.2.1F  
  Codespace Container Size  
    CPUs: 16  
    memory: 64 GB  
    storage: 128 GB  

Last reviewed: 02/10/2024

To inspect the lab details use `make inspect` shortcut. This will list the host names and management addresses for all lab devices.
To connect to any device use:

```bash
# the password is `admin`
ssh admin@<a-lab-device-hostname>
```

To check connectivity, ssh to any host and use `pingcheck dualstack_vrf_prod` or `pingcheck dualstack_vrf_dev` to start fping to the lab hosts. You have to wait a few minutes after the lab start for ping to be successful.

Enjoy the lab!
