from __future__ import annotations, unicode_literals

import os

import pytest
import testinfra.utils.ansible_runner
from helper.molecule import get_vars, infra_hosts, local_facts

testinfra_hosts = infra_hosts(host_name="instance")

# --- tests -----------------------------------------------------------------


def test_user(host, get_vars):
    """ """
    system_user = get_vars.get("grafana_system_user", {})

    owner = system_user.get("owner", "grafana")
    group = system_user.get("group", "grafana")

    assert host.group(group).exists
    assert host.user(owner).exists
    assert group in host.user(owner).groups
    assert host.user(owner).home == "/nonexistent"
