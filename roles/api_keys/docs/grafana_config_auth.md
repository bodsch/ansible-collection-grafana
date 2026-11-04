# `grafana_config_auth`

```yaml
grafana_config_auth:
  login_cookie_name: grafana_session
  login_maximum_inactive_lifetime_duration: ""
  login_maximum_lifetime_duration: ""
  token_rotation_interval_minutes: ""             # 10
  disable_login_form: ""                          # false
  disable_signout_menu: ""                        # false
  signout_redirect_url: ""
  oauth_auto_login: ""                            # false
  oauth_state_cookie_max_age: ""                  # 600
  oauth_skip_org_role_update_sync: ""             # false
  api_key_max_seconds_to_live: ""                 # -1
  sigv4_auth_enabled: ""                          # false
  sigv4_verbose_logging: ""                       # false
  azure_auth_enabled: ""                          # false

  anonymous:
    enabled: false
    org_name: Main Org.
    org_role: Viewer
    hide_version: false

  github:
    enabled: false
    allow_sign_up: true
    client_id: ""                                 # some_id
    client_secret: ""                             # some_secret
    scopes: []                                    # [user:email, read:org]
    auth_url: https://github.com/login/oauth/authorize
    token_url: https://github.com/login/oauth/access_token
    api_url: https://api.github.com/user
    allowed_domains: ""
    team_ids: ""
    allowed_organizations: ""

  gitlab:
    enabled: false
    allow_sign_up: true
    client_id: ""                                 # some_id
    client_secret: ""                             # some_secret
    scopes: ""                                    # api
    auth_url: https://gitlab.com/oauth/authorize
    token_url: https://gitlab.com/oauth/token
    api_url: https://gitlab.com/api/v4
    allowed_domains: ""
    allowed_groups: ""

  google:
    enabled: false
    allow_sign_up: true
    client_id: ""                                 # some_client_id
    client_secret: ""                             # some_client_secret
    scopes: []                                    # [https://www.googleapis.com/auth/userinfo.profile, https://www.googleapis.com/auth/userinfo.email]
    auth_url: https://accounts.google.com/o/oauth2/auth
    token_url: https://accounts.google.com/o/oauth2/token
    api_url: https://www.googleapis.com/oauth2/v1/userinfo
    allowed_domains: ""
    hosted_domain: ""

  grafana_com:
    enabled: false
    allow_sign_up: true
    client_id: ""                                 # some_id
    client_secret: ""                             # some_secret
    scopes: ""                                    # user:email
    allowed_organizations: ""

  azuread:
    name: Azure AD
    enabled: false
    allow_sign_up: true
    client_id: ""                                 # some_client_id
    client_secret: ""                             # some_client_secret
    scopes: ""                                    # openid email profile
    auth_url: https://login.microsoftonline.com/<tenant-id>/oauth2/v2.0/authorize
    token_url: https://login.microsoftonline.com/<tenant-id>/oauth2/v2.0/token
    allowed_domains: ""
    allowed_groups: ""
    role_attribute_strict: false

  okta:
    name: Okta
    enabled: false
    allow_sign_up: true
    client_id: ""                                 # some_id
    client_secret: ""                             # some_secret
    scopes: []                                    # [openid, profile, email, groups]
    auth_url: https://<tenant-id>.okta.com/oauth2/v1/authorize
    token_url: https://<tenant-id>.okta.com/oauth2/v1/token
    api_url: https://<tenant-id>.okta.com/oauth2/v1/userinfo
    allowed_domains: ""
    allowed_groups: ""
    role_attribute_path: ""
    role_attribute_strict: false

  generic_oauth:
    enabled: false
    name: OAuth
    allow_sign_up: true
    client_id: ""                                 # some_id
    client_secret: ""                             # some_secret
    scopes: []                                    # user:email,read:org
    empty_scopes: false
    email_attribute_name: ""                      # email:primary
    email_attribute_path: ""
    login_attribute_path: ""
    name_attribute_path: ""
    id_token_attribute_name: ""
    auth_url: https://foo.bar/login/oauth/authorize
    token_url: https://foo.bar/login/oauth/access_token
    api_url: https://foo.bar/user
    teams_url: ""
    allowed_domains: ""
    team_ids: ""
    allowed_organizations: ""
    role_attribute_path: ""
    role_attribute_strict: false
    groups_attribute_path: ""
    team_ids_attribute_path: ""
    tls_skip_verify_insecure: false
    tls_client_cert: ""
    tls_client_key: ""
    tls_client_ca: ""
    use_pkce: false
    auth_style: ""

  basic:
    enabled: false

  proxy:
    enabled: false
    header_name: ""                               # X-WEBAUTH-USER
    header_property: ""                           # username
    auto_sign_up: true
    sync_ttl: ""                                  # 60
    whitelist: []                                 # [192.168.1.1, 192.168.2.1]
    headers: []                                   # [Email:X-User-Email, Name:X-User-Name]
    headers_encoded: false
    enable_login_token: false

  jwt:
    enabled: false
    header_name: ""                               # X-JWT-Assertion
    email_claim: ""                               # sub
    username_claim: ""                            # sub
    jwk_set_url: ""                               # https://foo.bar/.well-known/jwks.json
    jwk_set_file: ""                              # /path/to/jwks.json
    cache_ttl: ""                                 # 60m
    expected_claims: ""                           # '{"aud": ["foo", "bar"]}'
    key_file: ""                                  # /path/to/key/file
    auto_sign_up: false

  ldap:
    enabled: false
    config_file: /etc/grafana/ldap.toml
    allow_sign_up: true
    # LDAP background sync (Enterprise only)
    # At 1 am every day
    sync_cron: "0 1 * * *"
    active_sync_enabled: true
```
