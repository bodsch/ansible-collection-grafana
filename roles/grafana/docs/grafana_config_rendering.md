# `grafana_config_rendering`

> Not implemented yet.
> Needs support!

```yaml
grafana_config_rendering:
  # Options to configure a remote HTTP image rendering service, e.g. using https://github.com/grafana/grafana-image-renderer.
  # URL to a remote HTTP image renderer service, e.g. http://localhost:8081/render, will enable Grafana to render panels and dashboards to PNG-images using HTTP requests to an external service.
  server_url: ""
  # If the remote HTTP image renderer service runs on a different server than the Grafana server you may have to configure this to a URL where Grafana is reachable, e.g. http://grafana.domain/.
  callback_url: ""
  # Concurrent render request limit affects when the /render HTTP endpoint is used. Rendering many images at the same time can overload the server,
  # which this setting can help protect against by only allowing a certain amount of concurrent requests.
  concurrent_render_request_limit: 30
```
