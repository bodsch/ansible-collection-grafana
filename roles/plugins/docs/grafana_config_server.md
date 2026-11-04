# `grafana_config_server`

```yaml
grafana_config_server:
  protocol: http                                  # (http, https, h2, socket)
  http_addr: ""
  http_port: 3000
  domain: localhost
  enforce_domain: false
  root_url: "%(protocol)s://%(domain)s:%(http_port)s/"
  serve_from_sub_path: ""                         # false
  router_logging: ""                              # false
  static_root_path: public
  enable_gzip: false
  cert_file: ""
  cert_key: ""
  socket: ""
  cdn_url: ""
  read_timeout: ""                                # 0
```
