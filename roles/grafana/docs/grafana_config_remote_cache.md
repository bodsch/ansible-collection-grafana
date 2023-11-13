# `grafana_config_remote_cache`

```yaml
grafana_config_remote_cache:
  type: database                                  # # Either "redis", "memcached" or "database" default is "database"
  # cache connectionstring options
  # database: will use Grafana primary database.
  # redis:    config like redis server e.g. `addr=127.0.0.1:6379,pool_size=100,db=0,ssl=false`.
  #           Only addr is required. ssl may be 'true', 'false', or 'insecure'.
  # memcache: 127.0.0.1:11211
  connstr: ""
```
