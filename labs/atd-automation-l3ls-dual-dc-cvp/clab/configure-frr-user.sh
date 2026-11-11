#!/bin/sh

set -eu

LABUSERNAME="${LABUSERNAME:-arista}"
LABPASSPHRASE="${LABPASSPHRASE:-arista}"

# Use a Linux shell so the shared startup readiness check can execute pwd.
if ! id -u "$LABUSERNAME" >/dev/null 2>&1; then
    adduser -D -s /bin/sh -G frr "$LABUSERNAME"
fi

case " $(id -Gn "$LABUSERNAME") " in
    *" frrvty "*) ;;
    *) addgroup "$LABUSERNAME" frrvty ;;
esac

printf '%s:%s\n' "$LABUSERNAME" "$LABPASSPHRASE" | chpasswd
