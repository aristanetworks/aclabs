# **Troubleshooting**

Every layer of the pipeline has a distinct check. Work them in order and the fault is found fast.

## **The dashboard is empty, lagging, or wrong**

Walk backwards from Grafana to the switch. First hop to fail tells you where the bug is.

1. **Grafana.** Does the panel query return data in Prometheus' **Explore** tab? If yes, the bug is in Grafana (query syntax, time range, template variable). If no →
2. **Prometheus.** Does `up{job="gnmic"} == 1` hold? If not, Prometheus can't reach gnmic — check `docker logs prometheus`. If yes →
3. **gnmic `/metrics`.** `docker exec gnmic wget -qO- localhost:9273/metrics | grep <metric>` — is the metric present? If not, either the subscription isn't running or a processor dropped/renamed it. Check `docker logs gnmic`. If yes →
4. **gnmic subscription to the switch.** `G -a <switch>:6030 get --path <path>` — does the switch return data on that path directly? If not, the switch isn't populating it (wrong path, feature not enabled, empty subtree).

## **gnmic can't reach a switch**

Isolate by protocol layer:

1. **TCP port.** From the gnmic container: `docker exec gnmic nc -zv <switch> 6030`. `Connection refused` → server or ACL. `Timeout` → routing.
2. **Server up.** On the switch: `show management api gnmi`. Look for `Enabled: yes` and `Octa: enabled`.
3. **VRF.** `show management api gnmi transport`. Is the transport in the VRF the collector can reach? This lab reaches switches on the MGMT VRF via `Management0`, so the `MGMT` transport must be `no shutdown`.
4. **Auth.** `G -a <switch>:6030 capabilities` on the collector. If TCP is fine but capabilities fails, it's auth (username/password) or TLS.

## **A subscription is running but no data lands in Prometheus**

Two common causes:

- **Path is valid but empty on this platform.** `G -a <switch>:6030 get --path <path>` returns `{}` with no error. The path exists in YANG but the switch has nothing to say about it (feature not configured, no ARP entries yet, `eos_native:` origin blocked). Confirm the path is populated with `Get` before assuming the subscription is broken.
- **A processor dropped or renamed the metric.** Check the `event-processors:` chain in `clab/gnmic.yml`. Grep the `/metrics` endpoint for any variation of the leaf name — you may find it under an unexpected metric name after `trim-prefixes` ran.

## **Set failed, but the leaf I'm changing looks fine**

gNMI `Set` validates the *whole* config transaction, not just the leaves you touched. An unrelated inconsistency elsewhere (e.g. BGP `redistribute static` with no static routes) can fail an innocent interface-description Set. Read the error message — it usually names the offending path.

## **eos_native paths return empty**

The switch is missing `provider eos-native` under `management api gnmi`. Verify with `show management api gnmi` — you should see `Native: enabled`. Without it, any subscription with an `eos_native:` prefix silently returns nothing.

## **openconfig-igmp / openconfig-aft is advertised in Capabilities but returns empty**

Capabilities lists model *support* — not every model is *populated*. For AFT specifically, you need `provider aft` under `management api models`, and the OpenConfig/Octa agent must be restarted (`agent Octa terminate`) after the config change. Verify the mount worked by querying the `afts/state-synced/state` leaves — `ipv4-unicast: true` / `ipv6-unicast: true` proves AFT is feeding.





---

**Previous:** [← Exploring the Lab](exploring-the-lab.md) &nbsp;·&nbsp; [Back to guide index](index.md)

--8<-- "gnmic-deployment-guide/_abbreviations.md"