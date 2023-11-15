
# Ansible Role:  `promtail`

Ansible role to setup [promtail](https://grafana.com/docs/loki/latest/clients/promtail/).


[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/bodsch/ansible-promtail/main.yml?branch=main)][ci]
[![GitHub issues](https://img.shields.io/github/issues/bodsch/ansible-promtail)][issues]
[![GitHub release (latest by date)](https://img.shields.io/github/v/release/bodsch/ansible-promtail)][releases]
[![Ansible Quality Score](https://img.shields.io/ansible/quality/50067?label=role%20quality)][quality]

[ci]: https://github.com/bodsch/ansible-promtail/actions
[issues]: https://github.com/bodsch/ansible-promtail/issues?q=is%3Aopen+is%3Aissue
[releases]: https://github.com/bodsch/ansible-promtail/releases
[quality]: https://galaxy.ansible.com/bodsch/promtail

If `latest` is set for `promtail_version`, the role tries to install the latest release version.  
**Please use this with caution, as incompatibilities between releases may occur!**

The binaries are installed below `/usr/local/bin/promtail/${promtail_version}` and later linked to `/usr/bin`. 
This should make it possible to downgrade relatively safely.

The downloaded archive is stored on the Ansible controller, unpacked and then the binaries are copied to the target system.
The cache directory can be defined via the environment variable `CUSTOM_LOCAL_TMP_DIRECTORY`. 
By default it is `${HOME}/.cache/ansible/promtail`.
If this type of installation is not desired, the download can take place directly on the target system. 
However, this must be explicitly activated by setting `promtail_direct_download` to `true`.


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


### Operating systems

Tested on

* Arch Linux
* Debian based
    - Debian 10 / 11 / 12
    - Ubuntu 20.04 / 22.04

> **RedHat-based systems are no longer officially supported! May work, but does not have to.**


## usage

### default configuration

```yaml
promtail_version: "2.7.2"
promtail_release_download_url: https://github.com/grafana/loki/releases

promtail_system_user: promtail
promtail_system_group: promtail
promtail_config_dir: /etc/promtail
promtail_storage_dir: /var/lib/promtail

promtail_additional_groups:
  - adm

promtail_direct_download: false

promtail_runtime: {}

promtail_systemd: {}

promtail_server: {}

promtail_clients: []

promtail_positions: {}

promtail_targets: {}

promtail_limits: {}

promtail_tracing: {}

promtail_scrape_configs: []
```

### `promtail_runtime`

Runtime configuration of promtail.

The command line parameters of the service are configured here.

Normally this should not be necessary, as all parameters can also be adjusted via the configuration file.

```yaml
promtail_runtime:
  client:
    batch_size_bytes: ""                            # (deprecated). (default 1048576)
    batch_wait: ""                                  # (deprecated). (default 1s)
    max_backoff: ""                                 # (deprecated). (default 5m0s)
    max_retries: ""                                 # (deprecated). (default 10)
    min_backoff: ""                                 # (deprecated). (default 500ms)
    tenant_id: ""                                   # (deprecated).
    timeout: ""                                     # (default 10s)
    url: ""                                         # (deprecated)
  config:
    expand_env: {}                                  # Expands ${var} in config according to the values of the environment variables.
    file: "{{ promtail_config_dir }}/promtail.yml"  # yaml file to load
  limit:
    readline_burst: ""                              # (default 10000)
    readline_rate: ""                               # (default 10000)
    readline_rate_drop: ""                          # (default true)
    readline_rate_enabled: ""                       # true | false
  log:
    config_reverse_order: ""                        # true | false
    format: ""                                      # [logfmt, json] (default logfmt)
    level: info                                     # [debug, info, warn, error] (default info)
  positions:
    file: ""                                        # (default "/var/log/positions.yaml")
    ignore_invalid_yaml: ""                         # whether to ignore & later overwrite positions files that are corrupted
    sync_period: ""                                 # Period with this to sync the position file. (default 10s)
  server:
    disable: ""                                     # Disable the http and grpc server.
    graceful_shutdown_timeout: ""                   # Timeout for graceful shutdowns (default 30s)
    grpc:
      conn_limit: ""                                # Maximum number of simultaneous grpc connections, <=0 to disable
      listen_address: ""                            # gRPC server listen address.
      listen_network: ""                            # gRPC server listen network (default "tcp")
      listen_port: ""                               # gRPC server listen port. (default 9095)
      max_concurrent_streams: ""                    # Limit on the number of concurrent streams for gRPC calls (0 = unlimited) (default 100)
      max_recv_msg_size_bytes: ""                   # Limit on the size of a gRPC message this server can receive (bytes). (default 4194304)
      max_send_msg_size_bytes: ""                   # Limit on the size of a gRPC message this server can send (bytes). (default 4194304)
      tls:
        ca_path: ""                                 # GRPC TLS Client CA path.
        cert_path: ""                               # GRPC TLS server cert path.
        client_auth: ""                             # GRPC TLS Client Auth type.
        key_path: ""                                # GRPC TLS server key path.
      keepalive:
        max_connection_age: ""                      # The inst for the maximum amount of time a connection may exist before it will be closed. Default: infinity (default 2562047h47m16.854775807s)
        max_connection_age_grace: ""                # An additive period after max-connection-age after which the connection will be forcibly closed. Default: infinity (default 2562047h47m16.854775807s)
        max_connection_idle: ""                     # The: ""  # after which an idle connection should be closed. Default: infinity (default 2562047h47m16.854775807s)
        min_time_between_pings: ""                  # Minimum amount of time a client should wait before sending a keepalive ping. If client sends keepalive ping more often, server will send GOAWAY and close the connection. (default 5m0s)
        ping_without_stream_allowed: ""             # If true, server allows keepalive pings even when there are no active streams(RPCs). If false, and client sends ping when there are no active streams, server will send GOAWAY and close the connection.
        time: ""                                    # Duration after which a keepalive probe is sent in case of no activity over the connection., Default: 2h (default 2h0m0s)
        timeout: ""                                 # After having pinged for keepalive check, the: ""  # after which an idle connection should be closed, Default: 20s (default 20s)
    http:
      conn_limit: ""                                # Maximum number of simultaneous http connections, <=0 to disable
      idle_timeout: ""                              # Idle timeout for HTTP server (default 2m0s)
      listen_address: ""                            # HTTP server listen address.
      listen_network: ""                            # HTTP server listen network, default tcp (default "tcp")
      listen_port: ""                               # HTTP server listen port. (default 80)
      read_timeout: ""                              # Read timeout for HTTP server (default 30s)
      tls:
        ca_path: ""                                 # HTTP TLS Client CA path.
        cert_path: ""                               # HTTP server cert path.
        client_auth: ""                             # HTTP TLS Client Auth type.
        key_path: ""                                # HTTP server key path.
      write_timeout: ""                             # Write timeout for HTTP server (default 30s)
    log:
      request_at_info_level_enabled: ""             # Optionally log requests at info level instead of debug level.
      source:
        ips_enabled: ""                             # Optionally log the source IPs.
        ips_header: ""                              # Header field storing the source IPs. Only used if server.log-source-ips-enabled is true. If not set the default Forwarded, X-Real-IP and X-Forwarded-For headers are used
        ips_regex: ""                               # Regex for matching the source IPs. Only used if server.log-source-ips-enabled is true. If not set the default Forwarded, X-Real-IP and X-Forwarded-For headers are used
    path_prefix: ""                                 # Base path to serve all API routes from (e.g. /v1/)
    register_instrumentation: ""                    # Register the instrumentation handlers (/metrics etc). (default true)
  target:
    sync_period: ""                                 # Period to resync directories being watched and files being tailed. (default 10s)
```

### `promtail_systemd`

Enables the automatic restart of the service via systemd.

```yaml
promtail_systemd:
  restart: false
  max_runtime: 7d
```

### `promtail_server`

[promtail dokumentation](https://grafana.com/docs/loki/latest/clients/promtail/configuration/#server)


```yaml
promtail_server:
  http:
    listen:
      network: ""                                 # tcp
      address: "127.0.0.1"
      port: 9080                                  # 80
      conn_limit: ""                              # 0
    tls:
      cert_file: ""
      key_file: ""
      client:
        auth_type: ""
        ca_file: ""
    server:
      timeouts:
        read: ""                                  # 30s
        write: ""                                 # 30s
        idle: ""                                  # 2m0s
  grpc:
    listen:
      network: ""                                 # tcp
      address: ""
      port: 9096                                  # 9095
      conn_limit: ""                              # 0
    tls:
      cert_file: ""
      key_file: ""
      client:
        auth_type: ""
        ca_file: ""
    server:
      msg_size:
        max_recv: ""                              # 4194304
        max_send: ""                              # 4194304
      max_concurrent_streams: ""                  # 100
      max_connection:
        idle: ""                                  # 2562047h47m16.854775807s
        age: ""                                   # 2562047h47m16.854775807s
        age_grace: ""                             # 2562047h47m16.854775807s
      keepalive:
        time: ""                                  # 2h0m0s
        timeout: ""                               # 20s
      min_time_between_pings: ""                  # 5m0s
      ping_without_stream_allowed: ""             # false
  tls:
    cipher_suites: ""
    min_version: ""
  register_instrumentation: ""                    # true
  graceful_shutdown_timeout: ""                   # 30s
  log:
    format: ""                                    # logfmt
    level: ""                                     # info
    source:
      ips_enabled: ""                             # false
      ips_header: ""
      ips_regex: ""
    request_at_info_level_enabled: ""             # false
  http_path_prefix: ""
  external_url: ""
  health_check_target: ""                         # false
  disable: ""                                     # false
  enable_runtime_reload: ""                       # false
```

### `promtail_clients`

[promtail dokumentation](https://grafana.com/docs/loki/latest/clients/promtail/configuration/#clients)

```yaml
promtail_clients:
  - url: "http://loki.monitoring.tld"
    batchwait: 1s
    batchsize: 1048576
    follow_redirects: false
    enable_http2: false
    backoff_config:
      min_period: 500ms
      max_period: 5m0s
      max_retries: 10
    timeout: 10s
    tenant_id: ""
    stream_lag_labels: ""  
  - url: "http://127.0.0.1:3100/loki/api/v1/push"
```

### `promtail_positions`

[promtail dokumentation](https://grafana.com/docs/loki/latest/clients/promtail/configuration/#positions)

```yaml
promtail_positions:
  sync_period: 10s
  filename: "/var/cache/promtail/positions.yml"
  ignore_invalid_yaml: false
```

### `promtail_targets`

[promtail dokumentation](https://grafana.com/docs/loki/latest/clients/promtail/configuration/#target_config)

```yaml
promtail_targets:
  sync_period: "10s"
  stdin: false
```

### `promtail_limits`

[promtail dokumentation](https://grafana.com/docs/loki/latest/clients/promtail/configuration/#limits_config)

```yaml
promtail_limits:
  readline_rate: 10000
  readline_burst: 10000
  readline_rate_drop: true
  max_streams: 0
```

### `promtail_tracing`

[promtail dokumentation](https://grafana.com/docs/loki/latest/clients/promtail/configuration/#ttracing)

```yaml
promtail_tracing:
  enabled: false
```

### `promtail_scrape_configs:`

[promtail dokumentation](https://grafana.com/docs/loki/latest/clients/promtail/configuration/#scrape_configs)

```yaml
promtail_scrape_configs:
  # file_sd
  - job_name: file_sd
    file_sd_configs:
      - files:
        - "{{ promtail_config_dir }}//file_sd/*.yml"
        - "{{ promtail_config_dir }}//file_sd/*.yaml"
        - "{{ promtail_config_dir }}//file_sd/*.json"
  #
  - job_name: system
    static_configs:
      - targets:
          - localhost
        labels:
          job: varlogs
          host: "{{ ansible_fqdn }}"
          agent: promtail
          __path__: /var/log/*.log
  # example syslog config
  - job_name: syslog
    syslog:
      listen_address: 0.0.0.0:1514
      labels:
        job: "syslog"
    relabel_configs:
      - source_labels:
          - __syslog_message_hostname
        target_label: 'host'

  - job_name: nginx_access
    static_configs:
      - targets:
          - localhost
        labels:
          job: nginx
          host: "{{ ansible_fqdn }}"
          log_level: access
          agent: promtail
          __path__: /var/log/nginx/*access.log
    pipeline_stages:
      # anonymisier latest octet
      - replace:
          expression: '(?:[0-9]{1,3}\.){3}([0-9]{1,3})'
          replace: '***'
```

For a more comprehensive example, please check out the [molecule](molecule/defaults/group_vars/all/vars.yml) tests!



## Contribution

Please read [Contribution](CONTRIBUTING.md)

## Development,  Branches (Git Tags)

The `master` Branch is my *Working Horse* includes the "latest, hot shit" and can be complete broken!

If you want to use something stable, please use a [Tagged Version](https://github.com/bodsch/ansible-promtail/tags)!

---

## Author and License

- Bodo Schulz

## License

[Apache](LICENSE)

**FREE SOFTWARE, HELL YEAH!**
