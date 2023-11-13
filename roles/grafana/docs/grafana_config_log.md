# `grafana_config_log`

```yaml
grafana_config_log:
  mode:                                           # Either "console", "file", "syslog"
    - console
    - file
  level: info                                     # Either "debug", "info", "warn", "error", "critical", default is "info"
  filters: []                                     # Ex filters: sqlstore:debug
  console:
    level: ""
    format: console                               # valid options are text, console and json
  file:
    level: ""
    format: text                                  # valid options are text, console and json
    log_rotate: ""                                # true
    max_lines: ""                                 # 1000000
    max_size_shift: ""                            # default is 28 means 1 << 28, 256MB
    daily_rotate: ""                              # true
    max_days: ""                                  # 7
  syslog:
    level: ""
    format: text                                  # valid options are text, console and json
    network: ""                                   # This can be udp, tcp, or unix
    address: ""
    facility: ""                                  # user, daemon and local0 through local7 are valid
    tag: ""                                       # default, the process' argv[0] is used.
  frontend:
    enabled: false
    provider: ""                                  # Sentry
    sentry_dsn: ""
    custom_endpoint: ""                           # (/log) Default will log the events to stdout.
    sample_rate: ""                               # Rate of events to be reported between 0 (none) and 1 (all), float (!)
    log_endpoint:
      requests_per_second_limit: ""               # 3
      burst_limit: ""                             # 15
    instrumentations:
      errors_enabled: ""                          # true
      console_enabled: ""                         # false
      webvitals_enabled: ""                       # false
    api_key: ""                                   # Api Key, only applies to Grafana Javascript Agent providertest
```
