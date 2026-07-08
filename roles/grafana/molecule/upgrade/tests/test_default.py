from __future__ import annotations, unicode_literals

import os

import pytest
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

    print(f"distribution: {distribution}")
    print(f"release     : {release}")

    version = local_facts(host=host, fact="grafana").get("version")

    install_dir = get_vars.get("grafana_install_path")
    defaults_dir = get_vars.get("grafana_defaults_directory")
    config_dir = get_vars.get("grafana_config_dir")

    if 'latest' in install_dir:
        install_dir = install_dir.replace('latest', version)

    files = []
    files.append("/usr/sbin/grafana-server")
    files.append("/usr/sbin/grafana-cli")

    if install_dir:
        files.append(f"{install_dir}/bin/grafana-server")
    if defaults_dir and not distribution == "artix":
        files.append(f"{defaults_dir}/grafana-server")
    if config_dir:
        files.append(f"{config_dir}/grafana.ini")

    print(files)

    for _file in files:
        f = host.file(_file)
        assert f.exists
        assert f.is_file


def test_user(host, get_vars):
    """
    """
    user = get_vars.get("grafana_system_user", "grafana")
    group = get_vars.get("grafana_system_group", "grafana")

    assert host.group(group).exists
    assert host.user(user).exists
    assert group in host.user(user).groups
    assert host.user(user).home == "/nonexistent"


def test_service(host, get_vars):
    service = host.service("grafana-server")
    assert service.is_enabled
    assert service.is_running


# without configuration, we have no port binding
def test_open_port(host, get_vars):
    """
    """
    listen_address = "0.0.0.0:3000"

    service = host.socket(f"tcp://{listen_address}")
    assert service.is_listening
