# `grafana_config_smtp`

> Not implemented yet.
> Needs support!

```yaml
grafana_config_smtp:
  enabled: false
  host: localhost:25
  user: ""
  # If the password contains # or ; you have to wrap it with triple quotes. Ex """#password;"""
  password: ""
  cert_file: ""
  key_file: ""
  skip_verify: false
  from_address: admin@grafana.localhost
  from_name: Grafana
  # EHLO identity in SMTP dialog (defaults to instance_name)
  ehlo_identity: dashboard.example.com
  # SMTP startTLS policy (defaults to 'OpportunisticStartTLS')
  startTLS_policy: NoStartTLS
```
