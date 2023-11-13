# Ansible Collection - bodsch.prometheus

Documentation for the collection.

## Roles

| Role                                                                       | | Description |
|:---------------------------------------------------------------------------| :---- | :---- |
| [bodsch.prometheus.alertmanager](./roles/alertmanager/README.md)           |       |       |
| [bodsch.prometheus.am_silence](./roles/am_silence/README.md)               |       |       |
| [bodsch.prometheus.blackbox_exporter](./roles/blackbox_exporter/README.md) |       |       |
| [bodsch.prometheus.docker_sd](./roles/docker_sd/README.md)                 |       |       |
| [bodsch.prometheus.json_exporter](./roles/json_exporter/README.md)         |       |       |
| [bodsch.prometheus.mysql_exporter](./roles/mysql_exporter/README.md)       |       |       |
| [bodsch.prometheus.nginx_exporter](./roles/nginx_exporter/README.md)       |       |       |
| [bodsch.prometheus.node_exporter](./roles/node_exporter/README.md)         |       |       |
| [bodsch.prometheus.mongodb_exporter](./roles/mongodb_exporter/README.md)   |       |       |
| [bodsch.prometheus.promcheck](./roles/promcheck/README.md)                 |       |       |
| [bodsch.prometheus.prometheus](./roles/prometheus/README.md)               |       |       |
| [bodsch.prometheus.pushgateway](./roles/pushgateway/README.md)             |       |       |
| [bodsch.prometheus.trickster](./roles/trickster/README.md)                 |       |       |

## Modules

### `amtool`

| Name  | Description |
| :---- | :---- |
| `bodsch.prometheus.amtool` | |


### `promtool`

| Name  | Description |
| :---- | :---- |
| `bodsch.prometheus.promtool` | |

### `alertmanager_silence`

| Name  | Description |
| :---- | :---- |
| `bodsch.prometheus.alertmanager_silence` | |


### `alertmanager_templates`

| Name  | Description |
| :---- | :---- |
| `bodsch.prometheus.alertmanager_templates` | |


### `prometheus_alert_rule`

| Name  | Description |
| :---- | :---- |
| `bodsch.prometheus.prometheus_alert_rule` | |


### `prometheus_alert_rules`

| Name  | Description |
| :---- | :---- |
| `bodsch.prometheus.prometheus_alert_rules` | |

## Filters

### `mysql_exporter`

| Name  | Description |
| :---- | :---- |
| `bodsch.prometheus.valid_credentials` | |
| `bodsch.prometheus.has_credentials` | |

### `nginx_exporter`


| Name  | Description |
| :---- | :---- |
| `bodsch.prometheus.nginx_exporter_prometheus_labels` | |

### `parse_checksum`

| Name  | Description |
| :---- | :---- |
| `bodsch.prometheus.parse_checksum` | |

### `prometheus`

| Name  | Description |
| :---- | :---- |
| `bodsch.prometheus.validate_file_sd` | |
| `bodsch.prometheus.validate_alertmanager_endpoints` | |
| `bodsch.prometheus.remove_empty_elements` | |
| `bodsch.prometheus.jinja_encode` | |

### `silencer`

| Name  | Description |
| :---- | :---- |
| `bodsch.prometheus.expired` | |
| `bodsch.prometheus.current_datetime` | |
