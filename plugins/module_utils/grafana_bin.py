#!/usr/bin/python3

import re

from ansible.module_utils.basic import AnsibleModule


def grafana_binary(module: AnsibleModule) -> tuple[str, str]:
    """
        return a tuble od grafana binaries:
            server, cli
    """

    _bin_grafana: str = "grafana"
    _bin_grafana_server: str = f"{_bin_grafana}-server"
    _bin_grafana_cli: str = f"{_bin_grafana}-cli"

    _bin_detected_grafana = module.get_bin_path(_bin_grafana, required=False)
    _bin_detected_grafana_server = module.get_bin_path(_bin_grafana_server, required=False)
    _bin_detected_grafana_cli = module.get_bin_path(_bin_grafana_cli, required=False)

    module.log(f"  - detected : {_bin_detected_grafana} | obsolete: {_bin_detected_grafana_server}, {_bin_detected_grafana_cli}")

    if _bin_detected_grafana:
        return (_bin_detected_grafana, _bin_detected_grafana)

    return (_bin_detected_grafana_server, _bin_detected_grafana_cli)


def grafana_detect_version(module: AnsibleModule, grafana: str | None, grafana_server: str | None = None) -> bool:
    """
        return True if grafana-server obsolete
    """
    module.log(f"grafana_detect_version(module, grafana: {grafana}, grafana_server: {grafana_server})")

    # grafana_version = None
    # result = {"failed": True, "changed": False, "version": grafana_version}

    if not grafana_server:
        module.log("`grafana-server` is no longer available. `grafana` is used instead.")
        return True

    args = []
    args.append(grafana)
    args.append("--version")

    _, out, _ = module.run_command(args, check_rc=True)

    pattern = re.compile(r"^Deprecation warning:.*Please update all uses of.*")

    match = re.search(pattern, out)

    if match:
        module.log(msg=f"value: {match}")
        return True

    return False
