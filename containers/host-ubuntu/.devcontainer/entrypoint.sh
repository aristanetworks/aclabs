#!/bin/bash

# set admin password for SSH access
if [ -z "${SSH_PASSWORD}" ]; then
  SSH_PASSWORD='admin'
fi

echo "admin:${SSH_PASSWORD}" | chpasswd

# start SSH server
sudo service ssh start

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

    ip link set eth1 down
    ip link set eth2 down

    ip link add ${UPLINK} type bond mode 802.3ad

    ip link set eth1 master ${UPLINK}
    ip link set eth2 master ${UPLINK}

    # RAND_HEX_1=$(openssl rand -hex 1)
    # RAND_HEX_2=$(openssl rand -hex 1)
    # BOND_MAC="c0:d6:82:00:${RAND_HEX_1}:${RAND_HEX_2}"
    # ip link set dev ${UPLINK} address $BOND_MAC
    ip link set dev ${UPLINK} address "c0:d6:82:00:$(openssl rand -hex 1):$(openssl rand -hex 1)"
    ip link set ${UPLINK} up

elif ! [ -z "${PHONE}" ] ; then

    UPLINK='br0'

    # Create br0
    ip link add name br0 type bridge

    # RAND_HEX_1=$(openssl rand -hex 1)
    # RAND_HEX_2=$(openssl rand -hex 1)
    # BOND_MAC="30:86:2d:00:${RAND_HEX_1}:${RAND_HEX_2}"
    # ip link set ${UPLINK} address $BOND_MAC
    ip link set dev ${UPLINK} address "30:86:2d:00:$(openssl rand -hex 1):$(openssl rand -hex 1)"

    # Disable STP, provide add'l visibility
    ip link set ${UPLINK} type bridge stp_state 0
    ip link set ${UPLINK} type bridge vlan_stats_per_port 1

    # Bring up Bridge Interface and add eth1 & eth2 (Note: eths must be UP to add)
    ip link set dev ${UPLINK} up
    ip link set eth1 master ${UPLINK}
    ip link set eth2 master ${UPLINK}

    # Add Simple Multicast Support
    #sysctl net.ipv4.conf.br0.mc_forwarding=1
    #sysctl net.ipv6.conf.br0.mc_forwarding=1
    ip link set ${UPLINK} type bridge mcast_stats_enabled 1

    # Customize LLDP
    # lldpcli configure ports eth1,eth2,br0 lldp status rx-only
fi

# configure IP addresses and routes
if ! [ -z "${IPV4}" ]; then
    ip addr add ${IPV4} dev ${UPLINK}
fi

if ! [ -z "${IPV6}" ]; then
    ip -6 addr add ${IPV6} dev ${UPLINK}
fi

if ! [ -z "${GW}" ]; then
    # add static routes
    ip route add ${STATIC_ROUTE} via ${GW} dev ${UPLINK}
    ip route add 224.0.0.0/4 via ${GW} dev ${UPLINK}
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
