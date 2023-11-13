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
            'file_list': self.file_list,
            'content_security_policy': self.content_security_policy,
        }

    def file_list(self, data):
        """
        """
        # display.v(f"file_list(self, {data})")
        result = []
        if isinstance(data, list):
            result = [x.get("path") for x in data if x.get("path")]

        return result

    def content_security_policy(self, data):
        """
        """
        # display.v(f"content_security_policy(self, {data})")
        def _string(s):
            """
            """
            if s.startswith("$") or s.startswith("ws:") or s.startswith("wss:") or s.endswith(":") or s == "*" or ".com" in s:
                return s
            else:
                return f"'{s}'"

        result = ""
        if isinstance(data, dict):
            """
                script-src 'self' 'unsafe-eval' 'unsafe-inline' 'strict-dynamic' $NONCE;
                object-src 'none';
                font-src 'self';
                style-src 'self' 'unsafe-inline' blob:;
                img-src * data:;
                base-uri 'self';
                connect-src 'self' grafana.com ws://$ROOT_PATH wss://$ROOT_PATH;
                manifest-src 'self';
                media-src 'none';
                form-action 'self';
            """
            for key, value in data.items():
                # display.v(f"  - '{key}' '{value}'")
                _v = []
                for str in value:
                    _value = _string(str)
                    # display.v(f"    - '{_value}'")
                    _v.append(_value)

                values = " ".join(_v)
                result += f"{key} {values}; "

        # display.v(f"return : {result}")
        return result
