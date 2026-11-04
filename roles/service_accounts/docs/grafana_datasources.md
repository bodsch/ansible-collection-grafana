# `grafana_datasources`

Supported datasource types are:

- prometheus
- loki
- graphite
- influxdb

```yaml
grafana_datasources:
  prometheus:
    state: present
    datasource:
      type: "prometheus"
      # access: "proxy"
      url: "http://prometheus.mydomain"
    # basic_auth:
    #   # Auth: true
    #   username: "admin"
    #   password: "password"
    default: true
    # json_data:
    #   tlsAuth: false
    #   tlsAuthWithCACert: false
    #   tlsSkipVerify: true

  loki:
    datasource:
      type: "loki"
      url: "http://loki.mydomain"
    editable: true
```

## Examples

### Prometheus

```yaml
grafana_datasources:
  prometheus:
    state: absent
    datasource:
      type: "prometheus"
      access: "proxy"
      url: "http://prometheus.mydomain"
    basic_auth:
      username: "admin"
      password: "password"
    default: true
    json_data:
      tlsAuth: false
      tlsAuthWithCACert: false
      tlsSkipVerify: true
```

### InfluxDB v1

```yaml
grafana_datasources:
  InfluxDB:
    state: present
    editable: true
    datasource:
      type: "influxdb"
      access: "proxy"
      url: "http://influxdb:8086"
    default: true
    database: molecule
    user: admin
    json_data:
      httpMode: GET
    secure_json_data:
      password: "{{ vault__influxdb.molecule }}"
```

### InfluxDB v2 - Flux

```yaml
grafana_datasources:
  InfluxDB:
    datasource:
      type: influxdb
      access: proxy
      url: http://localhost:8086
    json_data:
      version: Flux
      organization: organization
      defaultBucket: bucket
      tlsSkipVerify: true
    secure_json_data:
      token: token
```

### InfluxDB v2 - InfluxQL

```yaml
grafana_datasources:
  InfluxDB:
    datasource:
      type: influxdb
      access: proxy
      url: http://localhost:8086
    # This database should be mapped to a bucket
    database: site
    json_data:
      httpMode: GET
      httpHeaderName1: 'Authorization'
    secure_json_data:
      httpHeaderValue1: 'Token <token>'
```

### Loki

```yaml
grafana_datasources:
  loki: {}
```

### Graphite

```yaml
grafana_datasources:
  graphite: {}
```
