# `grafana_config_ldap`

```yaml
grafana_config_ldap:
  servers: []
  #   - hosts:
  #       - 127.0.0.1
  #     port: 389
  #     use_ssl: false
  #     start_tls: false
  #     ssl_skip_verify: false
  #     # root_ca_cert = "/path/to/certificate.crt"
  #     # client_cert = "/path/to/client.crt"
  #     # client_key = "/path/to/client.key"
  #     bind_dn: 'cn=admin,dc=grafana,dc=org'
  #     bind_password: grafana
  #     timeout: 10
  #     search_filter: (cn=%s)
  #     search_base_dns:
  #       - 'dc=grafana,dc=org'
  #     # group_search_filter = "(&(objectClass=posixGroup)(memberUid=%s))"
  #     # group_search_base_dns = ["ou=groups,dc=grafana,dc=org"]
  #     # group_search_filter_user_attribute = "uid"
  #     attributes:
  #       name: givenName
  #       surname: sn
  #       username: cn
  #       member_of: memberOf
  #       email: email
  #     group_mappings:
  #       - group_dn: 'cn=admins,ou=groups,dc=grafana,dc=org'
  #         org_role: Admin
  #       - group_dn: 'cn=users,ou=groups,dc=grafana,dc=org'
  #         org_role: Editor
  #       - group_dn: '*'
  #         org_role: Viewer
```
