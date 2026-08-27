# ANTA PSIRT Lab

This lab provides four Arista cEOS switches running EOS 4.33.0F for ANTA and
PSIRT exercises. The ANTA inventory is available at `inventory.yml` in the lab
root.

## Topology

The `eos1`/`eos2` and `eos3`/`eos4` pairs each have two links. Four additional
links fully cross-connect the two pairs.

![network diagram](assets/img/anta-psirt.png)

## Credentials

- Username: `arista`
- Password: `arista`

## Commands

```shell
make start
make inspect
make stop
```

Run ANTA against the inventory with credentials supplied on the command line:

```shell
anta --username "$LABUSERNAME" --password "$LABPASSPHRASE" --insecure --inventory inventory.yml nrfu
```
