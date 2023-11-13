# python 3 headers, required if submitting to Ansible

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.utils.display import Display

display = Display()


class FilterModule(object):
    """
      ansible filter
    """

    def filters(self):
        return {
            'compare_list': self.compare_list,
            'validate_attachment_hash': self.validate_attachment_hash,
            'validate_datasource_type': self.validate_datasource_type,
            'absent_datasources': self.absent_datasources,
            'non_existing_api': self.non_existing_api,
            'upgrade': self.upgrade,
        }

    def compare_list(self, data_list, compare_to_list):
        """
        """
        # display.v(f"compare_list({data_list}, {compare_to_list})")

        result = []

        for i in data_list:
            if i in compare_to_list:
                result.append(i)

        # display.v(f"return : {result}")
        return result

    def validate_attachment_hash(self, data, compare_to_list):
        """

        """
        display.v(f"validate_attachment_hash({data}, {compare_to_list})")

        if ':' in data:
            for i in compare_to_list:
                if i[:-1] in data:
                    return True
        else:
            if data in compare_to_list:
                return True

        return False

    def validate_datasource_type(self, data):
        """
        """
        not_supported = []
        ds_error = []

        # valid_datasources = [
        #     "graphite",
        #     "prometheus",
        #     "elasticsearch",
        #     "influxdb",
        #     "opentsdb",
        #     "mysql",
        #     "postgres",
        #     "cloudwatch",
        #     "alexanderzobnin-zabbix-datasource",
        #     "grafana-azure-monitor-datasource",
        #     "sni-thruk-datasource",
        #     "camptocamp-prometheus-alertmanager-datasource",
        #     "loki",
        #     "redis-datasource",
        # ]

        supported_datasources = [
            "graphite",
            "prometheus",
            "influxdb",
            "loki",
        ]

        datasource_types = list(data.keys())

        for d in datasource_types:
            ds_data = data.get(d, {})

            if not ds_data:
                ds_error.append(f"datasource '{d}' are not propper defined.")
                continue

            ds_type = ds_data.get("datasource", {}).get("type", None)
            if not ds_type:
                ds_error.append(f"datasource '{d}' are not propper defined.")
                continue

            if ds_type not in supported_datasources:
                not_supported.append(ds_type)

        if len(not_supported) > 0:
            not_supported = "', '".join(not_supported)
            ds_error.append(f"The datasources '{not_supported}' are not supported!")

        if len(ds_error) > 0:
            return dict(
                valid=False,
                msg="\n".join(ds_error)
            )

        return dict(
            valid = True,
            msg = "All datasources are valid."
        )

    def absent_datasources(self, data):
        """
        """
        result = []

        _data = data.copy()

        for datasource, values in _data.items():
            # res = {}
            if values.get("state", "present") == "absent":
                res = dict(
                    name = datasource,
                    orgId = values.get("org_id", 1)
                )
                result.append(res)

                _ = data.pop(datasource)

        return data, result

    def non_existing_api(self, data, existing_api_keys):
        """
        """
        display.v(f"non_existing_api({data}, {existing_api_keys})")
        display.v(f"  - {type(data)}")
        display.v(f"  - {type(existing_api_keys)}")

        if len(existing_api_keys) == 0:
            """
              no present API data
            """
            return data

        result = []
        names = []

        for d in existing_api_keys:
            names.append(d.get("name"))

        display.v(f"names {names}")

        for e in data:
            _name = e.get("name")
            display.v(f"- name {_name}")

            if _name in names or _name == "VALUE_SPECIFIED_IN_NO_LOG_PARAMETER":
                continue
            else:
                result.append(e)

        display.v(f" = result {result}")

        return result

    def upgrade(self, install_path, bin_path):
        """
        """
        directory = None
        link_to_bin = None

        install_path_stats = install_path.get("stat", None)
        bin_path_stats = bin_path.get("stat", None)
        install_path_exists = install_path_stats.get("exists", False)
        bin_path_exists = bin_path_stats.get("exists", False)

        if install_path_exists:
            directory = install_path_stats.get("isdir", False)

        if bin_path_exists:
            link_to_bin = bin_path_stats.get("islnk", False)

        if bin_path_exists and not link_to_bin:
            result = True
        elif install_path_exists and directory:
            result = False
        else:
            result = False

        display.v(f"return : {result}")
        return result
