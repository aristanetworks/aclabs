#!/bin/bash
# entrypoint.sh — Ubuntu host container init for aclabs
#
# Configures the container as a lab end-host based on environment variables
# passed in via the containerlab topology file.
#
# Supported environment variables:
#
#   SSH_PASSWORD   admin password for SSH (default 'admin')
#
#   TMODE          'lacp' | 'active-backup' | 'static' | 'none' (default)
#                  Multi-homing mode for eth1+eth2:
#                    lacp           — 802.3ad LAG (negotiated)
#                    active-backup  — active/standby (uses TACTIVE)
#                    static         — balance-xor LAG (no negotiation)
#                    none           — no bonding, single uplink on eth1
#   TACTIVE        'eth1' | 'eth2'   primary slave for active-backup (default eth1)
#   TBACKUP        derived from TACTIVE — do not set manually
#   PHONE          if set non-empty, creates an L2 bridge br0 across eth1+eth2
#                  (emulates an IP phone passthrough scenario)
#
#   UPLINK_MAC     MAC address for the uplink interface (random if unset)
#   IPV4           IPv4 address with prefix length, e.g. 10.40.40.101/24
#   IPV6           IPv6 address with prefix length
#   GW             IPv4 default-gateway address (unicast)
#   STATIC_ROUTE   IPv4 prefix(es) routed via GW. One prefix, or several
#                  separated by spaces and/or commas. e.g. 10.0.0.0/8
#                  or "10.0.0.0/8 172.16.0.0/12" or "10.0.0.0/8,172.16.0.0/12"
#
#   IGMP_VERSION   force IGMP version on the uplink (1|2|3). Leave unset to
#                  keep the kernel default.
#
# Notes:
# - Idempotent where possible. Designed to be safe across container restarts.
# - Multicast egress is configured WITHOUT a unicast gateway. The destination
#   MAC for multicast is derived directly from the group address (e.g.
#   239.0.10.101 -> 01:00:5e:00:0a:65), so adding `via $GW` on the multicast
#   route makes the kernel ARP for the gateway and silently drops every
#   multicast packet if ARP fails.

set -u
set -o pipefail

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
log()      { printf '[entrypoint] %s\n'        "$*" >&2; }
log_warn() { printf '[entrypoint] WARN: %s\n'  "$*" >&2; }
log_err()  { printf '[entrypoint] ERROR: %s\n' "$*" >&2; }
die()      { log_err "$*"; exit 1; }

# ---------------------------------------------------------------------------
# Root re-exec — preserve all documented env vars
# ---------------------------------------------------------------------------
if [[ "$(id -u)" != "0" ]]; then
  exec sudo --preserve-env=TMODE,TACTIVE,TBACKUP,SSH_PASSWORD,UPLINK_MAC,IPV4,IPV6,GW,STATIC_ROUTE,PHONE,IGMP_VERSION "$0" "$@"
fi

# ---------------------------------------------------------------------------
# Defaults & validation
# ---------------------------------------------------------------------------
: "${SSH_PASSWORD:=admin}"
: "${TMODE:=none}"
: "${TACTIVE:=eth1}"
: "${IPV4:=}"
: "${IPV6:=}"
: "${GW:=}"
: "${STATIC_ROUTE:=}"
: "${UPLINK_MAC:=}"
: "${PHONE:=}"
: "${IGMP_VERSION:=}"

case "${TACTIVE}" in
  eth1) TBACKUP=eth2 ;;
  eth2) TBACKUP=eth1 ;;
  *)    die "TACTIVE must be eth1 or eth2 (got '${TACTIVE}')" ;;
esac

case "${TMODE}" in
  none|lacp|active-backup|static) ;;
  *) log_warn "Unknown TMODE='${TMODE}', treating as 'none'"
     TMODE=none ;;
esac

# Loose format checks — catch obvious typos early
if [[ -n "${IPV4}" && ! "${IPV4}" =~ ^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+/[0-9]+$ ]]; then
  die "IPV4='${IPV4}' is not in the form x.x.x.x/prefix"
fi
if [[ -n "${IPV6}" && ! "${IPV6}" =~ ^.+:.+/[0-9]+$ ]]; then
  die "IPV6='${IPV6}' is not in the form xxxx:.../prefix"
fi
if [[ -n "${UPLINK_MAC}" && ! "${UPLINK_MAC}" =~ ^([0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}$ ]]; then
  die "UPLINK_MAC='${UPLINK_MAC}' is not a valid MAC address"
fi
if [[ -n "${IGMP_VERSION}" && ! "${IGMP_VERSION}" =~ ^[123]$ ]]; then
  die "IGMP_VERSION='${IGMP_VERSION}' must be 1, 2, or 3"
fi

# ---------------------------------------------------------------------------
# SSH password + services
# ---------------------------------------------------------------------------
echo "admin:${SSH_PASSWORD}" | chpasswd

# Both of these are non-idempotent and return non-zero if already running.
# Squelch and move on.
service ssh start >/dev/null 2>&1 || log_warn "ssh service start returned non-zero (already running?)"
lldpd                              || log_warn "lldpd returned non-zero (already running?)"

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
iface_exists() { ip link show "$1" >/dev/null 2>&1; }

create_bond_if_missing() {
  local name=$1; shift
  if iface_exists "$name"; then
    log "${name} already exists — reusing"
  else
    log "Creating ${name} (${*})"
    ip link add "$name" type bond "$@"
  fi
}

enslave() {
  local slave=$1 master=$2
  ip link set "$slave" down
  ip link set "$slave" master "$master"
}

# ---------------------------------------------------------------------------
# Uplink — bond / bridge construction
# ---------------------------------------------------------------------------
UPLINK='eth1'

if [[ "${TMODE}" == 'lacp' ]]; then
  UPLINK='bond0'
  log "Configuring LACP (802.3ad) bond ${UPLINK} from eth1+eth2"
  create_bond_if_missing "${UPLINK}" mode 802.3ad
  enslave eth1 "${UPLINK}"
  enslave eth2 "${UPLINK}"
  ip link set "${UPLINK}" up

elif [[ "${TMODE}" == 'active-backup' ]]; then
  UPLINK='bond0'
  log "Configuring active-backup bond ${UPLINK}: primary=${TACTIVE} backup=${TBACKUP}"
  create_bond_if_missing "${UPLINK}" mode active-backup
  enslave eth1 "${UPLINK}"
  enslave eth2 "${UPLINK}"
  # `primary=` can only be set after slaves are enslaved
  if ! echo "${TACTIVE}" > "/sys/class/net/${UPLINK}/bonding/primary" 2>/dev/null; then
    log_warn "Could not set primary=${TACTIVE} on ${UPLINK}"
  fi
  ip link set "${UPLINK}" up

elif [[ "${TMODE}" == 'static' ]]; then
  UPLINK='bond0'
  log "Configuring static (balance-xor) bond ${UPLINK} from eth1+eth2"
  create_bond_if_missing "${UPLINK}" mode balance-xor xmit_hash_policy layer3+4
  enslave eth1 "${UPLINK}"
  enslave eth2 "${UPLINK}"
  ip link set "${UPLINK}" up

elif [[ -n "${PHONE}" ]]; then
  UPLINK='br0'
  log "Configuring L2 bridge ${UPLINK} from eth1+eth2 (PHONE mode)"
  if ! iface_exists "${UPLINK}"; then
    ip link add name "${UPLINK}" type bridge
  fi
  ip link set "${UPLINK}" type bridge stp_state 0 vlan_stats_per_port 1 mcast_stats_enabled 1
  ip link set dev "${UPLINK}" up
  ip link set eth1 master "${UPLINK}"
  ip link set eth2 master "${UPLINK}"

else
  log "TMODE=none — using ${UPLINK} as the uplink"
fi

if ! iface_exists "${UPLINK}"; then
  die "Uplink ${UPLINK} does not exist after setup — cannot continue"
fi

# ---------------------------------------------------------------------------
# MAC address on the uplink
# ---------------------------------------------------------------------------
if [[ -z "${UPLINK_MAC}" ]]; then
  # 30:86:2d is a locally-administered OUI; randomize the bottom 3 bytes
  # (~16M unique values, ~5800-host birthday-bound)
  HEX=$(openssl rand -hex 3)
  UPLINK_MAC="30:86:2d:${HEX:0:2}:${HEX:2:2}:${HEX:4:2}"
  log "Generated random UPLINK_MAC=${UPLINK_MAC}"
fi

ip link set "${UPLINK}" down
if ! ip link set dev "${UPLINK}" address "${UPLINK_MAC}"; then
  log_warn "Could not set MAC ${UPLINK_MAC} on ${UPLINK} (already this MAC?)"
fi
ip link set "${UPLINK}" up

# ---------------------------------------------------------------------------
# IPv4 / IPv6 addresses (idempotent via `ip addr replace`)
# ---------------------------------------------------------------------------
if [[ -n "${IPV4}" ]]; then
  log "Setting IPv4 ${IPV4} on ${UPLINK}"
  ip addr replace "${IPV4}" dev "${UPLINK}"
fi

if [[ -n "${IPV6}" ]]; then
  log "Setting IPv6 ${IPV6} on ${UPLINK}"
  ip -6 addr replace "${IPV6}" dev "${UPLINK}"
fi

# ---------------------------------------------------------------------------
# Unicast routes
# ---------------------------------------------------------------------------
if [[ -n "${GW}" && -n "${STATIC_ROUTE}" ]]; then
  # STATIC_ROUTE may carry one prefix (the original, common case) or
  # several, separated by spaces and/or commas — e.g.
  #   STATIC_ROUTE: 10.0.0.0/8
  #   STATIC_ROUTE: "10.0.0.0/8 172.16.0.0/12"
  #   STATIC_ROUTE: "10.0.0.0/8,172.16.0.0/12"
  # Commas are normalized to spaces, then word-splitting yields the list.
  # A single prefix is just a one-element list, so existing topologies are
  # unaffected. Each prefix is applied independently (no `set -e`, so a bad
  # entry surfaces via `ip` and the remaining routes still apply).
  for route in ${STATIC_ROUTE//,/ }; do
    log "Adding unicast route ${route} via ${GW} dev ${UPLINK}"
    ip route replace "${route}" via "${GW}" dev "${UPLINK}"
  done
elif [[ -n "${GW}" && -z "${STATIC_ROUTE}" ]]; then
  log_warn "GW='${GW}' set but STATIC_ROUTE is empty — skipping unicast routes"
elif [[ -z "${GW}" && -n "${STATIC_ROUTE}" ]]; then
  log_warn "STATIC_ROUTE='${STATIC_ROUTE}' set but GW is empty — skipping unicast routes"
fi

# ---------------------------------------------------------------------------
# Multicast egress route — NEVER use `via $GW` here.
#
# Multicast destination MACs are derived directly from the group address.
# A `via` clause forces the kernel to ARP for that gateway, which silently
# drops every multicast packet if ARP fails. Always install this as a
# direct on-link route, independent of whether GW is set.
# ---------------------------------------------------------------------------
if [[ -n "${IPV4}" ]]; then
  IPV4_BARE="${IPV4%/*}"
  log "Adding multicast route 224.0.0.0/4 dev ${UPLINK} src ${IPV4_BARE}"
  ip route replace 224.0.0.0/4 dev "${UPLINK}" src "${IPV4_BARE}"
else
  log_warn "No IPV4 set — skipping multicast egress route"
fi

# ---------------------------------------------------------------------------
# Optional: force IGMP version on the uplink
# ---------------------------------------------------------------------------
if [[ -n "${IGMP_VERSION}" ]]; then
  log "Forcing IGMPv${IGMP_VERSION} on ${UPLINK}"
  if ! sysctl -w "net.ipv4.conf.${UPLINK}.force_igmp_version=${IGMP_VERSION}" >/dev/null; then
    log_warn "Could not set force_igmp_version on ${UPLINK}"
  fi
fi

# ---------------------------------------------------------------------------
# Pre-flight diagnostic — verify multicast route looks sane before handoff
# ---------------------------------------------------------------------------
if [[ -n "${IPV4}" ]]; then
  MROUTE_OUT=$(ip route get 239.0.0.1 2>&1 || true)
  if echo "${MROUTE_OUT}" | grep -q ' via '; then
    log_warn "Multicast route lookup includes 'via' — multicast egress may still fail:"
    log_warn "  ${MROUTE_OUT}"
    log_warn "Check 'ip route show' for a conflicting route that takes precedence."
  fi
fi

log "Host setup complete: UPLINK=${UPLINK} IPV4=${IPV4:-unset} IPV6=${IPV6:-unset} TMODE=${TMODE}"

# ---------------------------------------------------------------------------
# Hand off — exec argv if given, otherwise drop into zsh or sh
# ---------------------------------------------------------------------------
if [[ $# -gt 0 ]]; then
  exec "$@"
elif [[ -x /bin/zsh ]]; then
  exec zsh
else
  exec sh
fi
