#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# (c) 2022, Bodo Schulz <bodo@boone-schulz.de>

from __future__ import absolute_import, division, print_function
from ansible.module_utils.basic import AnsibleModule

import re


class GrafanaCLI(object):
    """
    """

    def __init__(self, module):
        """
          Initialize all needed Variables
        """
        self.module = module

        self.command = module.params.get("command")
        self.plugins_dir = module.params.get("plugins_dir")
        self.plugins = module.params.get("plugins")

        self._grafana_cli = module.get_bin_path("grafana-cli", True)

    def run(self):
        """
          runner
        """
        result = dict(
            rc=0,
            failed=False,
            changed=False,
            msg="Grafana Plugins ..."
        )

        if self.command == "list":
            return self._list()

        if self.command == "install":
            return self._install()

        return result

    def _list(self):
        """
          # grafana-cli plugins ls --help
          NAME:

             Grafana CLI plugins ls - list all installed plugins

          USAGE:
             Grafana CLI plugins ls [command options] [arguments...]
        """
        _failed = True
        _changed = False
        # _msg = "grafana plugin ls"

        args = []

        args.append(self._grafana_cli)

        if self.plugins_dir:
            args.append("--pluginsDir")
            args.append(self.plugins_dir)

        args.append("plugins")
        args.append("ls")

        rc, out, err = self.__exec(args)

        plugin_list = self.__filter_plugins(out)

        if rc == 0:
            _failed = False

        return dict(
            failed = _failed,
            changed = _changed,
            installed = plugin_list
        )

    def _list_remote(self):
        """
          # grafana-cli plugins list-remote --help
          NAME:
             Grafana CLI plugins list-remote - list remote available plugins

          USAGE:
             Grafana CLI plugins list-remote [command options] [arguments...]
        """
        pass

    def _list_versions(self):
        """
          # grafana-cli plugins list-versions --help
          NAME:
             Grafana CLI plugins list-versions - list-versions <plugin id>

          USAGE:
             Grafana CLI plugins list-versions [command options] [arguments...]
        """
        pass

    def _update(self):
        """
          # grafana-cli plugins update --help
          NAME:
             Grafana CLI plugins update - update <plugin id>

          USAGE:
             Grafana CLI plugins update [command options] [arguments...]
        """
        pass

    def _update_all(self):
        """
          # grafana-cli plugins update-all --help
          NAME:
             Grafana CLI plugins update-all - update all your installed plugins

          USAGE:
             Grafana CLI plugins update-all [command options] [arguments...]
        """
        pass

    def _install(self):
        """
          # grafana-cli plugins install --help
          NAME:
             Grafana CLI plugins install - install <plugin id> <plugin version (optional)>

          USAGE:
             Grafana CLI plugins install [command options] [arguments...]
        """
        # _failed = True
        # _changed = False
        # _msg = "grafana plugin install"

        if len(self.plugins) == 0:
            return dict(
                failed = True,
                changed =False,
                msg = "Missing a list of Plugins to install."
            )

        plugin_list = self._list()

        installed_plugins = plugin_list.get("installed")
        installed_plugin_list = [i for s in [d.keys() for d in installed_plugins] for i in s]

        result_state = []

        args = []

        args.append(self._grafana_cli)

        if self.plugins_dir:
            args.append("--pluginsDir")
            args.append(self.plugins_dir)

        args.append("plugins")
        args.append("install")

        copy_args = args.copy()

        for p in self.plugins:
            if p in installed_plugin_list:
                """
                """
                v = {v.get("version") for m in installed_plugins for k, v in m.items() if k == p}
                plugin_version = next(iter(v))

                res = {}
                res[p] = dict(
                    failed = False,
                    changed = False,
                    state=f"already in version {plugin_version} installed."
                )
                result_state.append(res)

            else:
                copy_args = args.copy()
                copy_args.append(p)

                rc, out, err = self.__exec(copy_args)

                pattern = re.compile(r"Downloaded.((?P<plugin>.*) v(?P<version>.*)) zip.*")

                if rc == 0:
                    re_result = re.search(pattern, out)
                    # plugin_string = re_result.group('plugin')
                    version_string = re_result.group('version')

                    res = {}
                    res[p] = dict(
                        failed = False,
                        changed = True,
                        state=f"version {version_string} successfuly installed."
                    )
                    result_state.append(res)
                else:
                    res = {}
                    res[p] = dict(
                        state=err,
                        failed=True
                    )
                    result_state.append(res)

        # define changed for the running tasks
        # migrate a list of dict into dict
        combined_d = {key: value for d in result_state for key, value in d.items()}

        # find all changed and define our variable
        changed = (len({k: v for k, v in combined_d.items() if v.get('changed')}) > 0)
        # find all failed and define our variable
        failed = (len({k: v for k, v in combined_d.items() if v.get('failed')}) > 0)

        #
        result_msg = {k: v.get('state') for k, v in combined_d.items()}

        # self.module.log(msg=f"  result_state : '{result_state}'")
        # self.module.log(msg=f"  combined_d   : '{combined_d}'")
        # self.module.log(msg=f"  changed      : '{changed}'")
        # self.module.log(msg=f"  failed       : '{failed}'")
        # self.module.log(msg=f"  result_msg   : '{result_msg}'")

        return dict(
            failed = failed,
            changed = changed,
            msg = result_msg
        )

    def _uninstall(self):
        """
          # grafana-cli plugins uninstall --help
          NAME:
             Grafana CLI plugins uninstall - uninstall <plugin id>

          USAGE:
             Grafana CLI plugins uninstall [command options] [arguments...]
        """
        pass

    def __filter_plugins(self, data):
        """
          data:
            String

          return:
            [
              {'grafana-clock-panel': {'version': '2.1.0'}},
              {'raintank-worldping-app': {'version': '1.2.9'}}
            ]
        """
        result = []

        plugins_array = '|'.join(data.splitlines())
        plugins_array = plugins_array.split('|')

        # deprecation_warning = [x for x in plugins_array if "Deprecation warning" in x]
        plugins_array = [x for x in plugins_array if "@" in x]

        # remove empty strings
        # plugins_array = list(filter(None, plugins_array))
        # remove last element ('Please restart Grafana after installing plugins. Refer to Grafana documentation for instructions if necessary.')
        # plugins_array.pop()

        if len(plugins_array) > 0:
            """
            """
            # remove first element ('installed plugins:')
            # plugins_array.pop(0)
            # self.module.log(msg=f"  plugins_array   : {plugins_array}")
            pattern = re.compile(r"((?P<plugin>.*) @ (?P<version>.*))")

        for plugin in plugins_array:
            """
            """
            res = {}
            re_result = re.search(pattern, plugin)

            if re_result:
                plugin_string = re_result.group('plugin')
                version_string = re_result.group('version')

                res[plugin_string] = dict(
                    version=version_string
                )

                result.append(res)

        return result

    def __exec(self, commands, check_rc=True):
        """
          execute shell program
        """
        rc, out, err = self.module.run_command(commands, check_rc=check_rc)
        # self.module.log(msg=f"  rc : '{rc}'")
        # self.module.log(msg=f"  out: '{out}'")
        # self.module.log(msg=f"  err: '{err}'")
        return rc, out, err

# ===========================================
# Module execution.
#


def main():

    module = AnsibleModule(
        argument_spec=dict(
            command=dict(
                default="list",
                choices=["install", "list-remote", "list-versions", "update", "upgrade", "update-all", "upgrade-all", "list", "uninstall", "remove"]
            ),
            plugins_dir=dict(
                required=False,
                type="str"
            ),
            plugins=dict(
                required=False,
                type="list"
            ),
        ),
        supports_check_mode=False,
    )

    o = GrafanaCLI(module)
    result = o.run()

    module.log(msg=f"= result: {result}")

    module.exit_json(**result)


# import module snippets
if __name__ == '__main__':
    main()


"""
# grafana-cli plugins --help
NAME:
   Grafana CLI plugins - Manage plugins for grafana

USAGE:
   Grafana CLI plugins command [command options] [arguments...]

COMMANDS:
   install                  install <plugin id> <plugin version (optional)>
   list-remote              list remote available plugins
   list-versions            list-versions <plugin id>
   update, upgrade          update <plugin id>
   update-all, upgrade-all  update all your installed plugins
   ls                       list all installed plugins
   uninstall, remove        uninstall <plugin id>
   help, h                  Shows a list of commands or help for one command

OPTIONS:
   --help, -h  show help (default: false)
"""
