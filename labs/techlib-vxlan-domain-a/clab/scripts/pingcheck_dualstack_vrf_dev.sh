while true
do
  echo Ping Check VRF DEV Hosts...
  fping -f /usr/local/bin/dualstack_list_vrf_dev
  sleep 2
  clear
done
