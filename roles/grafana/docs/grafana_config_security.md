# `grafana_config_security`

```yaml
grafana_config_security:
  disable_initial_admin_creation: false
  admin_user: admin
  admin_password: admin
  secret_key: SW2YcwTIb9zpOOhoPsMm
  encryption_provider: ""                         # secretKey.v1
  available_encryption_providers: []              # (Enterprise only) list of configured key providers, e.g., awskms.v1 azurekv.v1
  disable_gravatar: true                          # false
  data_source_proxy_whitelist: []                 # data source proxy whitelist (ip_or_domain:port separated by spaces)
  disable_brute_force_login_protection: ""        # false
  cookie_secure: ""                               # set to true if you host Grafana behind HTTPS. default is false.
  cookie_samesite: ""                             # defaults to `lax`. can be set to "lax", "strict", "none" and "disabled"
  allow_embedding: ""                             # false
  strict_transport_security: ""                   # false
  strict_transport_security_max_age_seconds: ""   # 86400
  strict_transport_security_preload: ""           # false
  strict_transport_security_subdomains: ""        # false
  x_content_type_options: ""                      # true
  x_xss_protection: ""                            # true
  content_security_policy: ""                     # false
  content_security_policy_template:
    script-src:
      - self
      - unsafe-eval
      - unsafe-inline
      - strict-dynamic
      - "$NONCE"
    object-src:
      - none
    font-src:
      - self
    style-src:
      - self
      - unsafe-inline
      - "blob:"
    img-src:
      - "*"
      - "data:"
    base-uri:
      - self
    connect-src:
      - self
      - grafana.com
      - ws://$ROOT_PATH
      - wss://$ROOT_PATH
    manifest-src:
      - self
    media-src:
      - none
    form-action:
      - self
  angular_support_enabled: ""                     # true - This will be disabled by default in future release
  csrf_trusted_origins: []
  csrf_additional_headers: []
  encryption:
    data_keys_cache_ttl: ""                       # 15m
    data_keys_cache_cleanup_interval: ""          # 1m
```
