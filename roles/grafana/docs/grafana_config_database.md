# `grafana_config_database`

```yaml
grafana_config_database:
  type: sqlite3                                   # Either "mysql", "postgres" or "sqlite3"
  path: grafana.db                                #
  cache_mode: private                             # For "sqlite3" only. cache mode setting used for connecting to the database. (private, shared)
  host: ""                                        # 127.0.0.1:3306
  name: ""                                        # grafana
  user: ""                                        # root
  password: ""                                    #
  url: ""                                         # e.g. mysql://user:secret@host:port/database
  ssl_mode: disable                               # # For "postgres" only, either "disable", "require" or "verify-full"
  isolation_level: ""                             # For "mysql" use "READ-UNCOMMITTED", "READ-COMMITTED", "REPEATABLE-READ" or "SERIALIZABLE".
  ca_cert_path: ""
  client_key_path: ""
  client_cert_path: ""
  server_cert_name: ""
  max_idle_conn: ""                               # 2
  max_open_conn: ""
  conn_max_lifetime: ""                           # 14400 (means 14400 seconds or 4 hours)
  log_queries: ""
  locking_attempt_timeout_sec: ""                 # 0
```
