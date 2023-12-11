# python 3 headers, required if submitting to Ansible

from __future__ import (absolute_import, print_function)
__metaclass__ = type

from ansible.utils.display import Display

display = Display()


class FilterModule(object):
    """
    """

    def filters(self):
        return {
            'file_list': self.file_list,
        }

    def file_list(self, data):
        """
        """
        result = []
        if isinstance(data, list):
            result = [x.get("path") for x in data if x.get("path")]

        return result
