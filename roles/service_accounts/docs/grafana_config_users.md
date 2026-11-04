# `grafana_config_users`

> Not implemented yet.
> Needs support!

```yaml
grafana_config_users:
  # disable user signup / registration
  allow_sign_up: true

  # Allow non admin users to create organizations
  allow_org_create: true

  # Set to true to automatically assign new users to the default organization (id 1)
  auto_assign_org: true

  # Set this value to automatically add new users to the provided organization (if auto_assign_org above is set to true)
  auto_assign_org_id: 1

  # Default role new users will be automatically assigned (if disabled above is set to true)
  auto_assign_org_role: Viewer

  # Require email validation before sign up completes
  verify_email_enabled: false

  # Background text for the user field on the login page
  login_hint: email or username
  password_hint: password

  # Default UI theme ("dark" or "light")
  default_theme: dark

  # Default locale (supported IETF language tag, such as en-US)
  default_locale: en-US

  # Path to a custom home page. Users are only redirected to this if the default home dashboard is used.
  # It should match a frontend route and contain a leading slash.
  home_page: ""

  # External user management, these options affect the organization users view
  external_manage_link_url: ""
  external_manage_link_name: ""
  external_manage_info: ""

  # Viewers can edit/inspect dashboard settings in the browser. But not save the dashboard.
  viewers_can_edit: false

  # Editors can administrate dashboard, folders and teams they create
  editors_can_admin: false

  # The duration in time a user invitation remains valid before expiring.
  # This setting should be expressed as a duration. Examples: 6h (hours), 2d (days), 1w (week). Default is 24h (24 hours).
  # The minimum supported duration is 15m (15 minutes).
  user_invite_max_lifetime_duration: 24h

  # Enter a comma-separated list of users login to hide them in the Grafana UI. These users are shown to Grafana admins and themselves.
  # hidden_users: ""
```
