while true
do
  echo Ping Check VRF PROD Hosts...
  fping -f /usr/local/bin/ipv6_list_vrf_dev
  sleep 2
  clear
done
