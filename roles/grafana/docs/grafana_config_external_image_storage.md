# `grafana_config_external_image_storage`

> Not implemented yet.
> Needs support!

```yaml
grafana_config_external_image_storage:
  provider: ""                                    # (s3, webdav, gcs, azure_blob, local)
  s3:
    endpoint: ""
    path_style_access: ""
    bucket: ""
    region: ""
    path: ""
    access_key: ""
    secret_key: ""
  webdav:
    url: ""
    public_url: ""
    username: ""
    password: ""
  gcs:
    key_file: ""
    bucket: ""
    path: ""
  azure_blob:
    account_name: ""
    account_key: ""
    container_name: ""
  local: {}
```
