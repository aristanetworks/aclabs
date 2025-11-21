#!/bin/bash

# preserve environment variables
if [ "$(id -u)" != "0" ]; then
  exec sudo --preserve-env=TMODE,TACTIVE,TBACKUP,SSH_PASSWORD,UPLINK_MAC,IPV4,IPV6,GW,STATIC_ROUTE "$0" "$@"
fi

# set admin password for SSH access
if [ -z "${SSH_PASSWORD}" ]; then
  SSH_PASSWORD='admin'
fi

echo "admin:${SSH_PASSWORD}" | sudo chpasswd

# start SSH server and LLDP
sudo service ssh start && sudo lldpd

UPLINK='eth1'

# TMODE is expected to be set via the containerlab topology file prior to deployment
# Expected values are "lacp" or "static" or "active-backup" which will bond eth1 and eth2
if [ -z "$TMODE" ]; then
  TMODE='none'
fi

# TACTIVE and TBACKUP to be set via the containerlab topology file for active-backup runner
# expected values are "eth1" or "eth2" default is "eth1" active and "eth2" backup
if [ -z "$TACTIVE" ]; then
  TACTIVE='eth1'
  TBACKUP='eth2'
elif [ "$TACTIVE" == 'eth1' ]; then
  TBACKUP='eth2'
elif [ "$TACTIVE" == 'eth2' ]; then
  TBACKUP='eth1'
fi

if [ "$TMODE" == 'lacp' ]; then

    UPLINK='bond0'

    sudo ip link set eth1 down
    sudo ip link set eth2 down

    sudo ip link add ${UPLINK} type bond mode 802.3ad

    sudo ip link set eth1 master ${UPLINK}
    sudo ip link set eth2 master ${UPLINK}

    sudo ip link set ${UPLINK} up

elif ! [ -z "${PHONE}" ] ; then

    UPLINK='br0'

    # Create br0
    sudo ip link add name br0 type bridge

    # Disable STP, provide add'l visibility
    sudo ip link set ${UPLINK} type bridge stp_state 0
    sudo ip link set ${UPLINK} type bridge vlan_stats_per_port 1

    # Bring up Bridge Interface and add eth1 & eth2 (Note: eths must be UP to add)
    sudo ip link set dev ${UPLINK} up
    sudo ip link set eth1 master ${UPLINK}
    sudo ip link set eth2 master ${UPLINK}

    # Add Simple Multicast Support
    #sysctl net.ipv4.conf.br0.mc_forwarding=1
    #sysctl net.ipv6.conf.br0.mc_forwarding=1
    sudo ip link set ${UPLINK} type bridge mcast_stats_enabled 1

    # Customize LLDP
    # lldpcli configure ports eth1,eth2,br0 lldp status rx-only
fi

# configure MAC address, IP addresses and routes
if [ -z "$UPLINK_MAC" ]; then
  UPLINK_MAC="30:86:2d:00:$(openssl rand -hex 1):$(openssl rand -hex 1)"
fi
sudo ip link set ${UPLINK} down
sudo ip link set dev ${UPLINK} address "${UPLINK_MAC}"
sudo ip link set ${UPLINK} up

if ! [ -z "${IPV4}" ]; then
    sudo ip addr add ${IPV4} dev ${UPLINK}
fi

if ! [ -z "${IPV6}" ]; then
    sudo ip -6 addr add ${IPV6} dev ${UPLINK}
fi

if ! [ -z "${GW}" ]; then
    # add static routes
    sudo ip route add ${STATIC_ROUTE} via ${GW} dev ${UPLINK}
    sudo ip route add 224.0.0.0/4 via ${GW} dev ${UPLINK}
fi

# Execute command from docker cli if any.
if [ ${@+True} ]; then
  exec "$@"
# Otherwise just enter sh or zsh.
else
  if [ -f "/bin/zsh" ]; then
    exec zsh
  else
    exec sh
  fi
fi
