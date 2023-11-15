# python 3 headers, required if submitting to Ansible

from __future__ import (absolute_import, print_function)
__metaclass__ = type

from ansible.utils.display import Display

display = Display()


class FilterModule(object):
    """
        Ansible file jinja2 tests
    """

    def filters(self):
        return {
            'sub_directories': self.reduce_path,
            'dashboard_hash': self.hash,
        }

    def reduce_path(self, data, path_reduce, uniq=True):
        """
        """
        file_list = []

        if isinstance(data, dict):
            files = data.get("files")

            if isinstance(files, list):
                for f in files:
                    file_list.append(
                        f.get("path", None).replace(f"{path_reduce}/", '').split('/')[0]
                    )

        if uniq:
            output = set()

            for x in file_list:
                output.add(x)

            file_list = []
            file_list = list(output)

        _ = file_list.sort()

        display.v(f"= result: {file_list}")

        return file_list

    def hash(self, data, path):
        """
        """
        string = f"{data}/{path}"
        import hashlib
        _bytes = string.encode('utf-8')
        hash = hashlib.sha256(_bytes)
        return hash.hexdigest()
