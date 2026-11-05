#!/bin/sh
# Select dial-in vs dial-out from the bind-mounted /gnmic-mode file.
# Default is dial-in so a missing or empty file keeps the existing lab behaviour.
set -e
MODE=dial-in
if [ -r /gnmic-mode ]; then
  MODE=$(tr -d ' \t\r\n' < /gnmic-mode)
fi
case "$MODE" in
  dial-out)
    echo "gNMIc: dial-out (gRPC tunnel server :30000)"
    exec /app/gnmic --config /gnmic-dialout.yml --log --use-tunnel-server subscribe
    ;;
  *)
    echo "gNMIc: dial-in (targets :6030)"
    exec /app/gnmic --config /gnmic.yml --log subscribe
    ;;
esac
