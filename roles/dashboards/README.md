# Ansible Role:  `grafana_dashboards`

Importer for varoius Grafana Dashboards.
Supports folder for an better structure.

A repository with sample dashboards can be viewed [here](https://gitlab.com/coremedia-as-code/monitoring/grafana-dashboards.git).


[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/bodsch/ansible-grafana-dashboards/main.yml?branch=main)][ci]
[![GitHub issues](https://img.shields.io/github/issues/bodsch/ansible-grafana-dashboards)][issues]
[![GitHub release (latest by date)](https://img.shields.io/github/v/release/bodsch/ansible-grafana-dashboards)][releases]
[![Ansible Quality Score](https://img.shields.io/ansible/quality/50067?label=role%20quality)][quality]

[ci]: https://github.com/bodsch/ansible-grafana-dashboards/actions
[issues]: https://github.com/bodsch/ansible-grafana-dashboards/issues?q=is%3Aopen+is%3Aissue
[releases]: https://github.com/bodsch/ansible-grafana-dashboards/releases
[quality]: https://galaxy.ansible.com/bodsch/grafana_dashboards


## Requirements & Dependencies

- rsync

### Operating systems

Tested on

* Arch Linux
* Artix Linux
* Debian based
    - Debian 11 / 12

## configuration

```yaml
grafana_dashboards_upgrade: false

grafana_dashboards_direct_download: false

grafana_dashboards_servername: "{{ ansible_fqdn }}"

grafana_dashboards_git:
  update: true
  url: ""
  version: ""

# vars from grafana role
grafana_provisioning_synced: false
grafana_data_dir: /var/lib/grafana
```

---

## Contribution

Please read [Contribution](CONTRIBUTING.md)

## Development,  Branches (Git Tags)

The `master` Branch is my *Working Horse* includes the "latest, hot shit" and can be complete broken!

If you want to use something stable, please use a [Tagged Version](https://github.com/bodsch/ansible-grafana-dashboards/tags)!


## Author

- Bodo Schulz

## License

[Apache](LICENSE)

**FREE SOFTWARE, HELL YEAH!**
