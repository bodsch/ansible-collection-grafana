
from ansible.parsing.dataloader import DataLoader
from ansible.template import Templar
import pytest
import os
import testinfra.utils.ansible_runner

import pprint
pp = pprint.PrettyPrinter()

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def base_directory():
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
    file_distibution = read_ansible_yaml(f"{base_dir}/vars/{operation_system}", "role_distibution")
    file_molecule = read_ansible_yaml(f"{molecule_dir}/group_vars/all/vars", "test_vars")
    # file_host_molecule = read_ansible_yaml(f"{base_dir}/host_vars/{HOST}/vars", "host_vars")

    defaults_vars = host.ansible("include_vars", file_defaults).get("ansible_facts").get("role_defaults")
    vars_vars = host.ansible("include_vars", file_vars).get("ansible_facts").get("role_vars")
    distibution_vars = host.ansible("include_vars", file_distibution).get("ansible_facts").get("role_distibution")
    molecule_vars = host.ansible("include_vars", file_molecule).get("ansible_facts").get("test_vars")

    ansible_vars = defaults_vars
    ansible_vars.update(vars_vars)
    ansible_vars.update(distibution_vars)
    ansible_vars.update(molecule_vars)

    templar = Templar(loader=DataLoader(), variables=ansible_vars)
    result = templar.template(ansible_vars, fail_on_undefined=False)

    return result


@pytest.mark.parametrize("dirs", [
    "/var/lib/grafana/dashboards/backend",
    "/var/lib/grafana/dashboards/frontend",
    "/var/lib/grafana/dashboards/delivery",
    "/var/lib/grafana/dashboards/licenses",
    "/var/lib/grafana/dashboards/dba-backend",
    "/var/lib/grafana/dashboards/dba-frontend",
    "/var/lib/grafana/dashboards/overviews",
])
def test_directories(host, dirs):
    d = host.file(dirs)
    assert d.is_directory
    assert d.group == "grafana"
    assert d.mode == 0o755


@pytest.mark.parametrize("files", [
    "/etc/grafana/provisioning/dashboards/backend.yml",
    "/etc/grafana/provisioning/dashboards/frontend.yml",
    "/etc/grafana/provisioning/dashboards/delivery.yml",
    "/etc/grafana/provisioning/dashboards/licenses.yml",
    "/etc/grafana/provisioning/dashboards/dba-backend.yml",
    "/etc/grafana/provisioning/dashboards/dba-frontend.yml",
    "/etc/grafana/provisioning/dashboards/overviews.yml",
])
def test_files(host, files):
    f = host.file(files)

    # print(
    #    host.ansible("file", "path=/etc/grafana/provisioning/dashboards/overviews.yml")
    # )

    assert f.is_file
    assert f.group == "grafana"
    assert f.mode == 0o644
