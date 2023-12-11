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
            'service_account_keyfiles': self.keyfiles,
            'content_security_policy': self.content_security_policy,
        }

    def keyfiles(self, data):
        """
            returns only the 'key_file' part from an dictionary

            input:
               {
                 "failed": false,
                 "changed": false,
                 "result": {
                   "sa-backup": {
                     "token": {
                       "id": 1,
                       "name": "sa-backup",
                       "key": "glsa_No804O5TWYWIPHj10PXh1xAiqc24v4uR_2fc11032",
                       "key_file": "/root/.ansible/cache/grafana/sa-backup.key"
                     },
                     "state": "present",
                     "failed": false
                   },
                   "sa-export-dashboards": {
                     "token": {
                       "id": 2,
                       "name": "sa-export-dashboards",
                       "key": "glsa_LHhBzq9z0Yeac1mss10x7H9EIFoR3lOU_4ad1fdba",
                       "key_file": "/root/.ansible/cache/grafana/sa-export-dashboards.key"
                     },
                     "state": "present",
                     "failed": false
                   }
                 }
               }

                or

               {
                 "failed": false,
                 "changed": false,
                 "result": {
                   "sa-backup": {
                     "msg": "service account for sa-backup already created.",
                     "key_file": "/root/.ansible/cache/grafana/sa-backup.key",
                     "state": "present",
                     "failed": false,
                     "changed": false
                   },
                   "sa-export-dashboards": {
                     "msg": "service account for sa-export-dashboards already created.",
                     "key_file": "/root/.ansible/cache/grafana/sa-export-dashboards.key",
                     "state": "present",
                     "failed": false,
                     "changed": false
                   }
                 }
               }

            output:
               ['/root/.ansible/cache/grafana/sa-backup.key', '/root/.ansible/cache/grafana/sa-export-dashboards.key']
        """
        display.vv(f"keyfiles({data})")

        result = []

        if isinstance(data, dict):
            result = data.get("result")

        """
            when input variant #1
        """
        result = [v.get("token").get("key_file") for k, v in result.items() if isinstance(v, dict) and v.get("token")]

        if len(result) == 0:
            """
                when input variant #2
            """
            result = data.get("result")
            result = [v.get("key_file") for k, v in result.items()]

        display.vv(f"= result: {result}")

        return result


    def content_security_policy(self, data):
        """
        """
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
                _v = []
                for str in value:
                    _value = _string(str)
                    _v.append(_value)

                values = " ".join(_v)
                result += f"{key} {values}; "

        # display.v(f"return : {result}")
        return result
