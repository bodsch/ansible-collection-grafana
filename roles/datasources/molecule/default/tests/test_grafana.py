# coding: utf-8

from __future__ import annotations, unicode_literals

import os

import pytest
from packaging.version import Version
import testinfra.utils.ansible_runner
from helper.molecule import get_vars, infra_hosts, local_facts

testinfra_hosts = infra_hosts(host_name="instance")

# --- tests -----------------------------------------------------------------


@pytest.mark.parametrize("dirs", [
    "/etc/grafana",
    "/var/lib/grafana",
    "/usr/share/grafana",
    "/opt/grafana",
])
def test_directories(host, dirs):
    d = host.file(dirs)
    assert d.is_directory
    assert d.exists


def test_files(host, get_vars):
    """
    """
    distribution = host.system_info.distribution
    release = host.system_info.release

    version = local_facts(host=host, fact="grafana").get("version")
    version = version.get("full_version")
    defaults_dir = get_vars.get("grafana_defaults_directory")
    config_dir = get_vars.get("grafana_config_dir")

    files = []

    grafana_bin = "grafana"

    if (Version(version) <= Version("13")):
        grafana_bin = "grafana-server"
        files.append("/usr/sbin/grafana-server")
        files.append("/usr/sbin/grafana-cli")
    else:
        files.append("/usr/sbin/grafana")

    if defaults_dir and not distribution == "artix":
        files.append(f"{defaults_dir}/grafana-server")

    if config_dir:
        files.append(f"{config_dir}/grafana.ini")

    print(files)

    for _file in files:
        f = host.file(_file)
        assert f.exists
        assert f.is_file
