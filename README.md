# Ansible Collection - bodsch.grafana

Documentation for the collection.

## Roles

| Role                                                      | | Description |
|:--------------------------------------------------------- | :---- | :---- |
| [bodsch.grafana.grafana](./roles/grafana/README.md)       |       |       |
| [bodsch.grafana.loki](./roles/loki/README.md)             |       |       |
| [bodsch.grafana.promtail](./roles/promtail/README.md)     |       |       |
| [bodsch.grafana.dashboards](./roles/dashboards/README.md) |       |       |

## Modules

| Name  | Description |
| :---- | :----       |
| `grafana_api_keys`         |             |
| `grafana_plugins`          |             |
| `grafana_service_accounts` |             |
| `sync_dashboards`          |             |

## Filters

| Name  | Description |
| :---- | :----       |
| `sub_directories`          |             |
| `dashboard_hash`           |             |
| `loki_checksum`            |             |
| `loki_tls_certificates`    |             |
| `loki_value`               |             |
| `promtail_checksum`        |             |
| `file_list`                |             |
| `content_security_policy`  |             |
| `compare_list`             |             |
| `validate_attachment_hash` |             |
| `validate_datasource_type` |             |
| `absent_datasources `      |             |
| `non_existing_api`         |             |
| `upgrade`                  |             |
