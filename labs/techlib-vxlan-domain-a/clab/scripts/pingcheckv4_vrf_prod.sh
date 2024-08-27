while true
do
  echo Ping Check VRF PROD Hosts...
  fping -f /usr/local/bin/ipv4_list_vrf_prod
  sleep 2
  clear
done
