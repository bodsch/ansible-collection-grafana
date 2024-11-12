#!/usr/bin/python3
# -*- coding: utf-8 -*-

# (c) 2022, Bodo Schulz <bodo@boone-schulz.de>

from __future__ import absolute_import, division, print_function
from ansible.module_utils.basic import AnsibleModule

# import os
# from requests.exceptions import ConnectionError
import json
# import requests
# from pathlib import Path

# ---------------------------------------------------------------------------------------

DOCUMENTATION = """
module: loki_verify_config
version_added: 1.1.0
author: "Bodo Schulz (@bodsch) <bodo@boone-schulz.de>"

short_description: TBD

description:
    - TBD
"""

EXAMPLES = """
"""

RETURN = """
"""

# ---------------------------------------------------------------------------------------


class LokiVerifyConfig(object):

    def __init__(self, module):
        """
        """
        self.module = module

        self.log_level = module.params.get("log_level")
        self.config_file = module.params.get("config_file")

        self._loki_cli = module.get_bin_path("loki", True)

    def run(self):
        """
            /usr/bin/loki -verify-config -log.format json -log.level debug -config.file /etc/loki/loki.yml
        """
        result = dict(
            rc=0,
            failed=False,
            changed=False,
            msg="Loki verify config ..."
        )

        _failed = True

        args = []

        args.append(self._loki_cli)
        args.append("-verify-config")

        args.append("-log.format")
        args.append("json")

        if self.log_level:
            args.append("-log.level")
            args.append(self.log_level)

        if self.config_file:
            args.append("-config.file")
            args.append(self.config_file)

        rc, out, err = self.__exec(args, check_rc=False)

        if rc == 0:
            _failed = False

        if isinstance(err, str):
            err = json.loads(err)

        if isinstance(err, dict):
            error_msg = err.get("err", None)
            msg = err.get("msg", None)

            if rc != 0 and error_msg:
                msg = error_msg.split("\n")
        else:
            msg = err

        result = dict(
            failed=_failed,
            changed=False,
            cmd=" ".join(args),
            msg=msg
        )

        return result

    def __exec(self, commands, check_rc=True):
        """
        """
        rc, out, err = self.module.run_command(commands, check_rc=check_rc)
        # self.module.log(msg=f"  rc : '{rc}'")
        # self.module.log(msg=f"  out: '{out}'")
        # self.module.log(msg=f"  err: '{err}'")
        return rc, out, err


def main():
    """
    """
    specs = dict(
        log_level=dict(
            default="info",
            choices=["debug", "info", "warn", "error"]
        ),
        config_file=dict(
            default="/etc/loki/loki.yml",
            type="str",
        ),
    )

    module = AnsibleModule(
        argument_spec=specs,
        supports_check_mode=False,
    )

    o = LokiVerifyConfig(module)
    result = o.run()

    module.log(msg=f"= result: {result}")

    module.exit_json(**result)


if __name__ == '__main__':
    main()
