#!/usr/bin/python3

# (c) 2020, Bodo Schulz <bodo@boone-schulz.de>

import os
import re

from ansible.module_utils.basic import AnsibleModule

# ----------------------------------------------------------------------

DOCUMENTATION = r"""
---
module: grafana_version
author: Bodo 'bodsch' Schulz <bodo@boone-schulz.de>
version_added: 2.0.0

short_description: Report the installed grafana version.
description:
    - Runs C(grafana --version) and splits the result into its parts.
    - >-
      The grafana role picks its template directory by the short version, so
      this value decides which configuration format is written.
    - The module takes no parameters.
"""

EXAMPLES = r"""
- name: detect installed grafana version
  bodsch.email.grafana_version:
  register: _grafana_version

- name: define grafana_version
  ansible.builtin.set_fact:
    grafana_version: "{{ _grafana_version.versions.full_version }}"
    grafana_short_version: "{{ _grafana_version.versions.short_version }}"
"""

RETURN = r"""
versions:
    description: The installed version, split into its parts.
    returned: always
    type: dict
    sample:
        full_version: "2.4.1-4"
        upstream_version: "2.4.1"
        major_version: "2"
        short_version: "2.4"
"""

# ----------------------------------------------------------------------


class GrafanaVersion:
    """
    Main Class
    """

    module = None

    def __init__(self, module):
        """
        """
        self.module = module
        self.module.log("GrafanaVersion:__init__()")

        self.grafana_binary = module.params.get("grafana_binary")

        self.grafana_bin_detected = module.get_bin_path("grafana", required=False)
        self.grafana_bin_configured = module.get_bin_path(self.grafana_binary, required=False)

        self.module.log(f"  - bin_detected   : {self.grafana_bin_detected}")
        self.module.log(f"  - bin_configured : {self.grafana_bin_configured}")

        # self.config_name = module.params.get("config_name")

    def run(self):
        """
        Read the grafana version and split it into its parts.

            2.4.1-4 (7d8c0e5759)
              full_version     = "2.4.1-4"
              upstream_version = "2.4.1"
              major_version    = "2"
              short_version    = "2.4"

        A distribution may append its own package release to the version, the
        way arch linux prints "2.4.1-4". upstream_version drops it, because
        grafana_config_version only accepts a version grafana itself knows -
        "2.4.1-4" is rejected with "Currently supported versions are: 2.4.0
        2.4.1".

        The grafana role picks its template directory by short_version, so
        that value decides which configuration format is written.
        """
        self.module.log("GrafanaVersion:run()")

        self._detect_deprecated_version()

        grafana_version = None
        result = dict(failed=True, changed=False, version=grafana_version)

        args = []
        args.append(self.grafana_bin_detected)
        args.append("--version")

        rc, out, err = self._exec(args)

        pattern = re.compile(r"(?P<version>\d+(?:\.\d+)+)")

        match = re.search(pattern, out)

        if match:
            # version = re.search(pattern_2, version.group('version'))
            grafana_version = match.group("version")

        self.module.log(msg=f"value: {grafana_version}")

        if grafana_version:
            major_version = None
            minor_version = None
            short_version = None

            version_splitted = grafana_version.split(".")

            major_version = version_splitted[0]

            if len(version_splitted) > 1:
                minor_version = version_splitted[1]

            if minor_version:
                short_version = ".".join([major_version, minor_version])
            else:
                short_version = major_version

            # only the leading digits-and-dots part is grafana's own version,
            # everything after it belongs to the distribution package
            upstream = re.match(r"[0-9]+(?:\.[0-9]+)*", grafana_version)

            version = dict(
                full_version=grafana_version,
                # upstream_version=upstream.group(0) if upstream else grafana_version,
                major_version=major_version,
                short_version=short_version,
            )

        result = dict(
            failed=(rc != 0),
            binary=os.path.basename(self.grafana_bin_detected),
            versions=version,
        )

        return result

    def _detect_deprecated_version(self):
        """
        """
        self.module.log("GrafanaVersion:_detect_deprecated_version()")

        grafana_version = None
        result = dict(failed=True, changed=False, version=grafana_version)

        if not self.grafana_bin_configured:
            self.module.log(f"{self.grafana_binary} is no longer available. `grafana` is used instead.")
            return True

        args = []
        args.append(self.grafana_bin_configured)
        args.append("--version")

        rc, out, err = self._exec(args)

        pattern = re.compile(r"^Deprecation warning:.*Please update all uses of.*")

        match = re.search(pattern, out)

        if match:
            self.module.log(msg=f"value: {match}")
            return True

        return False

    def _exec(self, cmd):
        """
        Run "grafana --version" and return (rc, stdout, stderr).
        """
        rc, out, err = self.module.run_command(cmd, check_rc=True)

        return rc, out, err


# ===========================================
# Module execution.
#


def main():
    """
    Report the installed grafana version, split into full, major and short
    form.
    """
    args = dict(
        grafana_binary=dict(
            required=True,
            type="path"
        )
    )

    module = AnsibleModule(
        argument_spec=args,
        supports_check_mode=True,
    )

    _module = GrafanaVersion(module)
    result = _module.run()

    module.log(msg=f"= result: {result}")

    module.exit_json(**result)


# import module snippets
if __name__ == "__main__":
    main()
