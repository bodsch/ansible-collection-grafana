# `grafana_config_unified_alerting`

> Not implemented yet.
> Needs support!

```yaml
grafana_config_unified_alerting:
  # Enable the Unified Alerting sub-system and interface.
  # When enabled we'll migrate all of your alert rules and notification channels to the new system.
  # New alert rules will be created and your notification channels will be converted into an Alertmanager configuration.
  # Previous data is preserved to enable backwards compatibility but new data is removed.```
  enabled: false
  # Comma-separated list of organization IDs for which to disable unified alerting. Only supported if unified alerting is enabled.
  disabled_orgs: ""
  # Specify the frequency of polling for admin config changes.
  # The interval string is a possibly signed sequence of decimal numbers, followed by a unit suffix (ms, s, m, h, d), e.g. 30s or 1m.
  admin_config_poll_interval: 60s
  # Specify the frequency of polling for Alertmanager config changes.
  # The interval string is a possibly signed sequence of decimal numbers, followed by a unit suffix (ms, s, m, h, d), e.g. 30s or 1m.
  alertmanager_config_poll_interval: 60s
  # Listen address/hostname and port to receive unified alerting messages for other Grafana instances.
  # The port is used for both TCP and UDP.
  # It is assumed other Grafana instances are also running on the same port.
  # The default value is `0.0.0.0:9094`.
  ha_listen_address: "0.0.0.0:9094"
  # Listen address/hostname and port to receive unified alerting messages for other Grafana instances.
  # The port is used for both TCP and UDP.
  # It is assumed other Grafana instances are also running on the same port.
  # The default value is `0.0.0.0:9094`.
  ha_advertise_address: ""
  # Comma-separated list of initial instances (in a format of host:port) that will form the HA cluster.
  # Configuring this setting will enable High Availability mode for alerting.
  ha_peers: ""
  # Time to wait for an instance to send a notification via the Alertmanager. In HA, each Grafana instance will
  # be assigned a position (e.g. 0, 1). We then multiply this position with the timeout to indicate how long should
  # each instance wait before sending the notification to take into account replication lag.
  # The interval string is a possibly signed sequence of decimal numbers, followed by a unit suffix (ms, s, m, h, d), e.g. 30s or 1m.
  ha_peer_timeout: "15s"
  # The interval between sending gossip messages. By lowering this value (more frequent) gossip messages are propagated
  # across cluster more quickly at the expense of increased bandwidth usage.
  # The interval string is a possibly signed sequence of decimal numbers, followed by a unit suffix (ms, s, m, h, d), e.g. 30s or 1m.
  ha_gossip_interval: "200ms"
  # The interval between gossip full state syncs. Setting this interval lower (more frequent) will increase convergence speeds
  # across larger clusters at the expense of increased bandwidth usage.
  # The interval string is a possibly signed sequence of decimal numbers, followed by a unit suffix (ms, s, m, h, d), e.g. 30s or 1m.
  ha_push_pull_interval: "60s"
  # Enable or disable alerting rule execution. The alerting UI remains visible. This option has a legacy version in the `[alerting]` section that takes precedence.
  execute_alerts: true
  # Alert evaluation timeout when fetching data from the datasource. This option has a legacy version in the `[alerting]` section that takes precedence.
  # The timeout string is a possibly signed sequence of decimal numbers, followed by a unit suffix (ms, s, m, h, d), e.g. 30s or 1m.
  evaluation_timeout: 30s
  # Number of times we'll attempt to evaluate an alert rule before giving up on that evaluation.
  # This option has a legacy version in the `[alerting]` section that takes precedence.
  max_attempts: 3
  # Minimum interval to enforce between rule evaluations.
  # Rules will be adjusted if they are less than this value  or if they are not multiple of the scheduler interval (10s).
  # Higher values can help with resource management as we'll schedule fewer evaluations over time.
  # This option has a legacy version in the `[alerting]` section that takes precedence.
  # The interval string is a possibly signed sequence of decimal numbers, followed by a unit suffix (ms, s, m, h, d), e.g. 30s or 1m.
  min_interval: 10s
  reserved_labels:
    # Comma-separated list of reserved labels added by the Grafana Alerting engine that should be disabled.
    # For example: `disabled_labels=grafana_folder`
    disabled_labels: ""
```
