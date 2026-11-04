# `grafana_config_plugin`

```yaml
grafana_config_plugin:
  grafana_image_renderer:
    rendering:
      timezone: ""
      language: ""
      viewport_device_scale_factor: ""
      ignore_https_errors: ""
      verbose_logging: ""
      dumpio: ""
      args: []
      chrome_bin: ""
      mode: ""
      clustering:
        mode: ""
        max_concurrency: ""
        timeout: ""
      viewport:
        max_width: ""
        max_height: ""
        max_device_scale_factor: ""
    grpc:
      host: ""                                    # Default host is 127.0.0.1
      port: ""                                    # default port is 0 and will automatically assign a port not in use.
```
