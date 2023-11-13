
# Ansible Role:  `grafana`

Ansible role to install and configure [grafana](https://github.com/grafana/grafana).

[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/bodsch/ansible-grafana/main.yml?branch=main)][ci]
[![GitHub issues](https://img.shields.io/github/issues/bodsch/ansible-grafana)][issues]
[![GitHub release (latest by date)](https://img.shields.io/github/v/release/bodsch/ansible-grafana)][releases]
[![Ansible Quality Score](https://img.shields.io/ansible/quality/50067?label=role%20quality)][quality]

[ci]: https://github.com/bodsch/ansible-grafana/actions
[issues]: https://github.com/bodsch/ansible-grafana/issues?q=is%3Aopen+is%3Aissue
[releases]: https://github.com/bodsch/ansible-grafana/releases
[quality]: https://galaxy.ansible.com/bodsch/grafana


If `latest` is set for `grafana_version`, the role tries to install the latest release version.  
**Please use this with caution, as incompatibilities between releases may occur!**

The binaries are installed below `/opt/grafana/${grafana_version}` and later linked to `/usr/sbin`. 
This should make it possible to downgrade relatively safely.

The Grafana archive is stored on the Ansible controller, unpacked and then the binaries are copied to the target system.
The cache directory can be defined via the environment variable `CUSTOM_LOCAL_TMP_DIRECTORY`. 
By default it is `${HOME}/.cache/ansible/grafana`.  
If this type of installation is not desired, the download can take place directly on the target system. 
However, this must be explicitly activated by setting `grafana_direct_download` to `true`.

## Requirements & Dependencies

Ansible Collections

- [bodsch.core](https://github.com/bodsch/ansible-collection-core)
- [bodsch.scm](https://github.com/bodsch/ansible-collection-scm)

```bash
ansible-galaxy collection install bodsch.core
ansible-galaxy collection install bodsch.scm
```
or
```bash
ansible-galaxy collection install --requirements-file collections.yml
```


## Operating systems

Tested on

* Arch Linux
* Debian based
    - Debian 10 / 11 / 12
    - Ubuntu 20.04 / 22.04

## usage

```yaml
grafana_version: 9.1.1

# enterprise or oss
grafana_edition: oss

grafana_urls:
  releases: https://github.com/grafana/grafana/releases
  downloads: https://dl.grafana.com/{{ grafana_edition }}/release

grafana_system_user: grafana
grafana_system_group: grafana
grafana_config_dir: /etc/grafana
grafana_data_dir: "{{ grafana_config_paths.data }}"
grafana_share_dir: /usr/share/grafana
grafana_log_dir: "{{ grafana_config_paths.logs }}"

grafana_direct_download: false

grafana_provisioning:
  # Should we use the provisioning capability when possible (provisioning require grafana >= 5.0)
  enabled: true
  # Should the provisioning be kept synced.
  # If true, previous provisioned objects will be removed if not referenced anymore.
  keep_synced: false

# The location where the keys should be stored.
# grafana_api_keys_dir: "{{ lookup('env', 'HOME') }}/grafana/keys"

grafana_datasources: {}
grafana_plugins: []
grafana_alert_notifications: {}

grafana_api: {}
grafana_service_accounts: {}

grafana_config_alerting: {}
grafana_config_analytics: {}
grafana_config_annotations: {}
grafana_config_auth: {}
grafana_config_aws: {}
grafana_config_azure: {}
grafana_config_dashboards: {}
grafana_config_database: {}
grafana_config_dataproxy: {}
grafana_config_datasources: {}
grafana_config_date_formats: {}
grafana_config_emails: {}
grafana_config_enterprise: {}
grafana_config_explore: {}
grafana_config_expressions: {}
grafana_config_external_image_storage: {}
grafana_config_feature_toggles: {}
grafana_config_general: {}
grafana_config_geomap: {}
grafana_config_grafana_com: {}
grafana_config_help: {}
grafana_config_live: {}
grafana_config_log: {}
grafana_config_metrics: {}
grafana_config_panels: {}
grafana_config_paths: {}
grafana_config_plugin: {}
grafana_config_plugins: {}
grafana_config_profile: {}
grafana_config_query_history: {}
grafana_config_quota: {}
grafana_config_rbac: {}
grafana_config_remote_cache: {}
grafana_config_rendering: {}
grafana_config_security: {}
grafana_config_server: {}
grafana_config_smtp: {}
grafana_config_snapshots: {}
grafana_config_tracing: {}
grafana_config_unified_alerting: {}
grafana_config_users: {}
grafana_config_ldap: {}
```

## Contribution

Please read [Contribution](CONTRIBUTING.md)

## Development,  Branches (Git Tags)

The `master` Branch is my *Working Horse* includes the "latest, hot shit" and can be complete broken!

If you want to use something stable, please use a [Tagged Version](https://github.com/bodsch/ansible-grafana/tags)!

---

## Author and License

- Bodo Schulz

## License

[Apache](LICENSE)

**FREE SOFTWARE, HELL YEAH!**
