#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# (c) 2022, Bodo Schulz <bodo@boone-schulz.de>

from __future__ import absolute_import, division, print_function
from ansible.module_utils.basic import AnsibleModule
from community.grafana.grafana_datasource import GrafanaInterface

import os
from requests.exceptions import ConnectionError
import json
import requests
from pathlib import Path

class GrafanaDatasources(object):
    """
    """
    def __init__(self, module):
        """
        """
        self.module = module

    def run(self):
        """
        """
        result = dict(
            rc=0,
            failed=False,
            changed=False,
            msg="Grafana datasources  ..."
        )

        return result


def main():
    """
    """
    module = AnsibleModule(
        argument_spec=dict(
            state=dict(
                default="list",
                choices=["list", "manage"]
            ),
            grafana_url=dict(
                required=False,
                type="str",
                default="http://127.0.0.1:3000"
            ),
            grafana_admin=dict(
                required=True,
                type="dict"
            ),
            api_keys=dict(
                required=False,
                type="list"
            ),
        ),
        supports_check_mode=False,
    )

    o = GrafanaDatasources(module)
    result = o.run()

    module.log(msg=f"= result: {result}")

    module.exit_json(**result)


# import module snippets
if __name__ == '__main__':
    main()

