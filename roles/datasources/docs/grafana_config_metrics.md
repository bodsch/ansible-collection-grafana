# `grafana_config_metrics`

```yaml
grafana_config_metrics:
  enabled: false
  interval_seconds: ""                            # 10
  disable_total_stats: ""                         # false
  basic_auth:
    username: ""
    password: ""
  environment_info: {}
  #  exampleLabel1: exampleValue1
  #  exampleLabel2: exampleValue2
  graphite:
    address: ""
    prefix: prod.grafana.%(instance_name)s.
```
