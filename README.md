# Ansible Collection - bodsch.grafana

A collection of Ansible roles for the Grafana universe. 


[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/bodsch/ansible-collection-grafana/main.yml?branch=main)][ci]
[![GitHub issues](https://img.shields.io/github/issues/bodsch/ansible-collection-grafana)][issues]
[![GitHub release (latest by date)](https://img.shields.io/github/v/release/bodsch/ansible-collection-grafana)][releases]

[ci]: https://github.com/bodsch/ansible-collection-grafana/actions
[issues]: https://github.com/bodsch/ansible-collection-grafana/issues?q=is%3Aopen+is%3Aissue
[releases]: https://github.com/bodsch/ansible-collection-grafana/releases


## supported operating systems

* Arch Linux
* Debian based
    - Debian 12
    - Ubuntu 20.04 / 22.04


## Contribution

Please read [Contribution](CONTRIBUTING.md)

## Development,  Branches (Git Tags)

The `master` Branch is my *Working Horse* includes the "latest, hot shit" and can be complete broken!

If you want to use something stable, please use a [Tagged Version](https://github.com/bodsch/ansible-collection-grafana/tags)!

---

## Roles

| Role                                                      | Build State | Description |
|:--------------------------------------------------------- | :---- | :---- |
| [bodsch.grafana.grafana](./roles/grafana/README.md)       |[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/bodsch/ansible-collection-grafana/grafana.yml?branch=main)][grafana] | Ansible role to install and configure [grafana](https://github.com/grafana/grafana). |
| [bodsch.grafana.loki](./roles/loki/README.md)             |[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/bodsch/ansible-collection-grafana/loki.yml?branch=main)][loki] | Ansible role to install and configure [loki](https://github.com/grafana/loki). |
| [bodsch.grafana.promtail](./roles/promtail/README.md)     |[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/bodsch/ansible-collection-grafana/promtail.yml?branch=main)][promtail] | Ansible role to install and configure [promtail](https://grafana.com/docs/loki/latest/clients/promtail/). |
| [bodsch.grafana.dashboards](./roles/dashboards/README.md) |[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/bodsch/ansible-collection-grafana/dashboards.yml?branch=main)][dashboards] | Ansible role to import varoius Grafana Dashboards. |

[grafana]: https://github.com/bodsch/ansible-collection-grafana/actions/workflows/grafana.yml
[loki]: https://github.com/bodsch/ansible-collection-grafana/actions/workflows/loki.yml
[promtail]: https://github.com/bodsch/ansible-collection-grafana/actions/workflows/promtail.yml
[dashboards]: https://github.com/bodsch/ansible-collection-grafana/actions/workflows/dashboards.yml


## Modules

| Name  | Description |
| :---- | :----       |
| `bodsch.grafana.grafana_api_keys`         |             |
| `bodsch.grafana.grafana_plugins`          |             |
| `bodsch.grafana.grafana_service_accounts` |             |
| `bodsch.grafana.sync_dashboards`          |             |

## Filters

| Name  | Description |
| :---- | :----       |
| `bodsch.grafana.sub_directories`          |             |
| `bodsch.grafana.dashboard_hash`           |             |
| `bodsch.grafana.loki_checksum`            |             |
| `bodsch.grafana.loki_tls_certificates`    |             |
| `bodsch.grafana.loki_value`               |             |
| `bodsch.grafana.promtail_checksum`        |             |
| `bodsch.grafana.file_list`                |             |
| `bodsch.grafana.content_security_policy`  |             |
| `bodsch.grafana.compare_list`             |             |
| `bodsch.grafana.validate_attachment_hash` |             |
| `bodsch.grafana.validate_datasource_type` |             |
| `bodsch.grafana.absent_datasources `      |             |
| `bodsch.grafana.non_existing_api`         |             |
| `bodsch.grafana.upgrade`                  |             |
