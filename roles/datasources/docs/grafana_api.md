# `grafana_api`

Multiple API keys with different roles can be created or removed.  
The created API keys are stored on the Ansible controller.

```yaml
grafana_api:
  # API keys to configure
  keys:
    - name: foo
      state: present
      # Can be one of the following values: Viewer, Editor or Admin.
      role: Viewer
      # not implemented yet
      # expiration: '3200'
  # The location where the keys should be stored.
  store_directory: "{{ lookup('env', 'HOME') }}/grafana/api_keys"
```
