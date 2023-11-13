# `grafana_config_snapshots`

> Not implemented yet.
> Needs support!

```yaml
grafana_config_snapshots:
  # snapshot sharing options
  external_enabled: true
  external_snapshot_url: https://snapshots.raintank.io
  external_snapshot_name: Publish to snapshots.raintank.io
  # Set to true to enable this Grafana instance act as an external snapshot server and allow unauthenticated requests for
  # creating and deleting snapshots.
  public_mode: false
  # remove expired snapshot
  snapshot_remove_expired: true
```
