# coding: utf-8
from __future__ import unicode_literals

from ansible.parsing.dataloader import DataLoader
from ansible.template import Templar

import json
import pytest
import os

import testinfra.utils.ansible_runner

HOST = 'instance'

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts(HOST)


def pp_json(json_thing, sort=True, indents=2):
    if type(json_thing) is str:
        print(json.dumps(json.loads(json_thing), sort_keys=sort, indent=indents))
    else:
        print(json.dumps(json_thing, sort_keys=sort, indent=indents))
    return None


def base_directory():
    """
    """
    cwd = os.getcwd()

    if 'group_vars' in os.listdir(cwd):
        directory = "../.."
        molecule_directory = "."
    else:
        directory = "."
        molecule_directory = f"molecule/{os.environ.get('MOLECULE_SCENARIO_NAME')}"

    return directory, molecule_directory


def read_ansible_yaml(file_name, role_name):
    """
    """
    read_file = None

    for e in ["yml", "yaml"]:
        test_file = f"{file_name}.{e}"
        if os.path.isfile(test_file):
            read_file = test_file
            break

    return f"file={read_file} name={role_name}"


@pytest.fixture()
def get_vars(host):
    """
        parse ansible variables
        - defaults/main.yml
        - vars/main.yml
        - vars/${DISTRIBUTION}.yaml
        - molecule/${MOLECULE_SCENARIO_NAME}/group_vars/all/vars.yml
    """
    base_dir, molecule_dir = base_directory()
    distribution = host.system_info.distribution
    operation_system = None

    if distribution in ['debian', 'ubuntu']:
        operation_system = "debian"
    elif distribution in ['redhat', 'ol', 'centos', 'rocky', 'almalinux']:
        operation_system = "redhat"
    elif distribution in ['arch', 'artix']:
        operation_system = f"{distribution}linux"

    file_defaults = read_ansible_yaml(f"{base_dir}/defaults/main", "role_defaults")
    file_vars = read_ansible_yaml(f"{base_dir}/vars/main", "role_vars")
    role_distribution = read_ansible_yaml(f"{base_dir}/vars/{operation_system}", "role_distribution")
    file_molecule = read_ansible_yaml(f"{molecule_dir}/group_vars/all/vars", "test_vars")
    # file_host_molecule = read_ansible_yaml("{}/host_vars/{}/vars".format(base_dir, HOST), "host_vars")

    defaults_vars = host.ansible("include_vars", file_defaults).get("ansible_facts").get("role_defaults")
    vars_vars = host.ansible("include_vars", file_vars).get("ansible_facts").get("role_vars")
    distibution_vars = host.ansible("include_vars", role_distribution).get("ansible_facts").get("role_distribution")
    molecule_vars = host.ansible("include_vars", file_molecule).get("ansible_facts").get("test_vars")
    # host_vars          = host.ansible("include_vars", file_host_molecule).get("ansible_facts").get("host_vars")

    ansible_vars = defaults_vars
    ansible_vars.update(vars_vars)
    ansible_vars.update(distibution_vars)
    ansible_vars.update(molecule_vars)
    # ansible_vars.update(host_vars)

    templar = Templar(loader=DataLoader(), variables=ansible_vars)
    result = templar.template(ansible_vars, fail_on_undefined=False)

    return result


def local_facts(host):
    """
      return local facts
    """
    return host.ansible("setup").get("ansible_facts").get("ansible_local").get("promtail")


def test_package(host, get_vars):
    """
    """
    version = local_facts(host).get("version")

    install_dir = get_vars.get("promtail_install_path")
    defaults_dir = get_vars.get("promtail_defaults_directory")
    config_dir = get_vars.get("promtail_config_dir")

    if 'latest' in install_dir:
        install_dir = install_dir.replace('latest', version)

    files = []
    files.append("/usr/bin/promtail")

    if install_dir:
        files.append(f"{install_dir}/promtail")
    if defaults_dir:
        files.append(f"{defaults_dir}/promtail")
    if config_dir:
        files.append(f"{config_dir}/promtail.yml")

    print(files)

    packages = get_vars.get("promtail_packages")
    install_path = get_vars.get("promtail_install_path")

    for pack in packages:
        f = host.file(f"{install_path}/{pack}")
        assert f.exists
        assert f.is_file


@pytest.mark.parametrize("dirs", [
    "/etc/promtail",
])
def test_directories(host, dirs):
    d = host.file(dirs)
    assert d.is_directory
    assert d.exists


@pytest.mark.parametrize("files", [
    "/etc/promtail/promtail.yml"
])
def test_files(host, files):
    f = host.file(files)
    assert f.exists
    assert f.is_file


def test_user(host):
    assert host.group("promtail").exists
    assert host.user("promtail").exists
    assert "promtail" in host.user("promtail").groups
    assert host.user("promtail").home == "/nonexistent"


def test_service(host, get_vars):
    service = host.service("promtail")
    assert service.is_enabled
    assert service.is_running


def test_open_port(host, get_vars):
    for i in host.socket.get_listening_sockets():
        print(i)

    # pp_json(get_vars)

    server = get_vars.get("promtail_server")
    listen_address = None

    print(server)

    if isinstance(server, dict):
        listen = server.get("http", {}).get("listen", {})

        listen_address = listen.get("address", "127.0.0.1")
        listen_port = listen.get("port", 9080)

        listen_address = f"{listen_address}:{listen_port}"

    if not listen_address:
        listen_address = "127.0.0.1:9080"

    service = host.socket(f"tcp://{listen_address}")
    assert service.is_listening
