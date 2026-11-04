import json
import re
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class Grafana:
    """ """

    def __init__(self, module: any, server: str, auth: Optional[dict] = None):
        """
        Initialisiert die Klasse mit einem Ansible-Modulobjekt, setzt Header und Base-URL.
        """
        self.module = module
        self.module.log(msg=f"Grafana::__init__(server={server}, auth={auth})")

        self.grafana_server = server

        if auth:
            self.grafana_admin_user = auth.get("username", None)
            self.grafana_admin_pass = auth.get("password", None)
            self.grafana_service_account_token = auth.get("token", None)

        self.grafana_settings = None
        self.grafana_version = self.version()

        self.module.log(msg=f"version: {self.grafana_version}")

    def settings(self):
        """ """
        self.module.log(msg="Grafana::settings(self)")

        url = f"{self.grafana_server}/api/frontend/settings"

        return self.__call_url(url=url)

    def version(self):
        """ """
        self.module.log(msg="Grafana::version(self)")

        version = None
        major_version = None

        status_code, self.grafana_settings = self.settings()

        self.module.log(msg=f"  {self.grafana_settings}")

        if self.grafana_settings and isinstance(self.grafana_settings, dict):
            """ """
            # status = self.grafana_settings.get('status')

            if int(status_code) == 200:
                version = self.grafana_settings.get("buildInfo", {}).get(
                    "version", None
                )
                if version:
                    major_version = version.split(".")[0]

            return dict(version=version, major_version=major_version)
        else:
            return self.grafana_settings

    def list_api_keys(self):
        """
        http://127.0.0.1:3000/api/auth/keys
        """
        self.module.log(msg="Grafana::list_api_keys(self)")

        url = f"{self.grafana_server}/api/auth/keys"

        error = True
        output = None

        status_code, output = self.__call_url(url=url)

        if status_code == 200:
            error = False

        self.module.log(msg=f" - error   {error}")
        self.module.log(msg=f" - output  {output}")

        return (status_code, error, output)

    def create_api_key(self, data):
        """ """
        self.module.log(msg=f"Grafana::create_api_key(self, {data})")

        if int(self.grafana_version.get("major_version", 10)) >= 11:

            status_code = 409
            error = True
            msg = "this endpoint has been removed, please use POST /api/serviceaccounts and POST /api/serviceaccounts/{id}/tokens instead"

            return (status_code, error, msg)

        url = f"{self.grafana_server}/api/auth/keys"

        api_name = data.get("name", None)
        api_role = data.get("role", "Viewer")
        api_expiration = data.get("expiration", None)

        if not api_name:
            msg = "missing api name"
            return True, msg

        if api_role not in ["Viewer", "Editor", "Admin"]:
            msg = f"wrong API role '{api_role}'. Can be one of the following values: Viewer, Editor or Admin."
            return True, msg

        payload = dict(name=api_name, role=api_role)

        if api_expiration:
            payload.update({"secondsToLive": api_expiration})

        self.module.log(msg=f" - payload {payload}")

        status_code, text = self.__call_url(url=url, method="POST", data=payload)

        if status_code == 200:
            self.module.log(msg=f" = {text} / {type(text)}")

            key_file = self.save_keyfile(text)

            text.update({"key_file": key_file})
            return False, text
        else:
            return True, text

        pass

    def remove_api_key(self, id):
        """ """
        self.module.log(msg=f"Grafana::remove_api_key(self, {id})")

        url = f"{self.grafana_server}/api/auth/keys/{key_id}"

        status_code, text = self.__call_url(url=url, method="DELETE")

        if status_code == 200:
            return False, text
        else:
            return True, text

    # ---------------------------------------------------------------------------------------------

    def list_service_accounts(self):
        """
        http://127.0.0.1:3000/api/serviceaccounts
        """
        self.module.log(msg="Grafana::list_service_accounts(self)")

        url = f"{self.grafana_server}/api/serviceaccounts/search"

        error = True
        output = None
        total_count = 0
        service_accounts = []

        status_code, output = self.__call_url(url=url)

        if status_code == 200:
            error = False
            total_count = output.get("totalCount", 0)
            service_accounts = output.get("serviceAccounts", [])

        output = dict(count=total_count, service_accounts=service_accounts)

        self.module.log(msg=f" - error   {error}")
        self.module.log(msg=f" - output  {output}")

        return error, output

    def service_tokens(self, present_keys={}):
        """ """
        self.module.log(msg=f"Grafana::service_tokens(self, {present_keys})")

        url = f"{self.grafana_server}/api/serviceaccounts"

        error = True
        output = None

        for key, value in present_keys.items():
            account_id = value

            if account_id:
                _url = f"{url}/{account_id}"
                status_code, output = self.__call_url(url=_url)

        # self.module.log(msg=f"= {error}, {output})")

        return error, output

    def create_token(self, data):
        """
        {
            'id': 7,
            'name': 'sa-export-dashboards',
            'login': 'sa-sa-export-dashboards',
            'orgId': 1,
            'isDisabled': False,
            'role': 'Viewer',
            'tokens': 0,
            'avatarUrl': '',
            'key_file': None
        }
        """
        self.module.log(msg=f"Grafana::create_token(self, {data})")

        url = f"{self.grafana_server}/api/serviceaccounts"

        text = {}

        service_account_id = data.get("id", None)
        service_account_name = data.get("name", None)

        if service_account_id and service_account_name:

            payload = dict(name=service_account_name)

            _url = f"{url}/{service_account_id}/tokens"

            status_code, text = self.__call_url(url=_url, method="POST", data=payload)

            if status_code == 200:
                token = text.get("key", None)

                if token:
                    key_file = self.save_keyfile(text)
                    text.update({"key_file": key_file})

                    return False, text

        return True, text

    def create_service_account(self, data):
        """ """
        # self.module.log(msg=f"Grafana::create_service_account(self, {data})")

        service_account_name = data.get("name", None)
        service_account_role = data.get("role", "Viewer")
        service_account_disabled = data.get("disabled", None)

        if not service_account_name:
            msg = "missing api name"
            return True, msg

        if service_account_role not in ["Viewer", "Editor", "Admin"]:
            msg = f"wrong Service Account role '{service_account_role}'. Can be one of the following values: Viewer, Editor or Admin."
            return True, msg

        payload = dict(name=service_account_name, role=service_account_role)

        if service_account_disabled:
            payload.update({"isDisabled": service_account_disabled})

        # self.module.log(msg=f" - payload {payload}")

        status_code, text = self.__call_url(method="POST", data=payload)

        if status_code == 200 or status_code == 201:
            # self.module.log(msg=f" = {text}")

            key_file = self.save_keyfile(text)

            text.update({"key_file": key_file})
            return False, text
        else:
            return True, text

        pass

    def remove_service_account(self, id):
        """ """
        # self.module.log(msg=f"Grafana::remove_service_account(self, {id})")

        status_code, text = self.__call_url(method="DELETE", key_id=id)

        if status_code == 200:
            return False, text
        else:
            return True, text

    def __call_url(
        self,
        url: str,
        method: str = "GET",
        data: Optional[dict] = None,
        key_id: Optional[str] = None,
    ):
        """ """
        self.module.log(msg=f"Grafana::__call_url(self, {method}, {data}, {key_id})")

        response = None

        headers = {"Accept": "application/json", "Content-Type": "application/json"}

        basic_authentication = None

        if self.grafana_service_account_token:
            headers["Authorization"] = f"Bearer {self.grafana_service_account_token}"

        elif self.grafana_admin_user and self.grafana_admin_pass:
            basic_authentication = (self.grafana_admin_user, self.grafana_admin_pass)

        # uri = f"{self.grafana_url}/api/serviceaccounts"

        # if key_id:
        #    uri += f"/{key_id}"

        self.module.log(
            msg="------------------------------------------------------------------"
        )
        self.module.log(msg=f" url    : {url}")
        self.module.log(msg=f" method : {method}")
        self.module.log(msg=f" data   : {data}")
        self.module.log(msg=f" headers: {headers}")
        self.module.log(
            msg="------------------------------------------------------------------"
        )

        try:

            if method == "POST":
                response = requests.post(
                    url,
                    data=json.dumps(data),
                    headers=headers,
                    auth=basic_authentication,
                )
            elif method == "GET":
                response = requests.get(url, headers=headers, auth=basic_authentication)
            elif method == "DELETE":
                if key_id:
                    response = requests.delete(
                        url, headers=headers, auth=basic_authentication
                    )

            else:
                self.module.log(msg="unsupported")
                pass

            response.raise_for_status()

            # self.module.log(msg=f" text    : {response.text} / {type(response.text)}")
            # self.module.log(msg=f" json    : {response.json()} / {type(response.json())}")
            # self.module.log(msg=f" headers : {response.headers}")
            # self.module.log(msg=f" code    : {response.status_code}")
            # self.module.log(msg="------------------------------------------------------------------")

            return response.status_code, response.json()

        except requests.exceptions.HTTPError as e:
            self.module.log(msg=f"ERROR   : {e}")

            status_code = e.response.status_code
            status_message = e.response.json()
            # self.module.log(msg=f" status_message : {status_message} / {type(status_message)}")
            # self.module.log(msg=f" status_message : {e.response.json()}")

            if status_message.get("message") == "Not found":
                status_message = f"Service Account {key_id} not found."

            return status_code, status_message

        except ConnectionError as e:
            error_text = (
                f"{type(e).__name__} {(str(e) if len(e.args) == 0 else str(e.args[0]))}"
            )
            self.module.log(msg=f"ERROR   : {error_text}")

            self.module.log(
                msg="------------------------------------------------------------------"
            )
            return 500, error_text

        except Exception as e:
            self.module.log(msg=f"ERROR   : {e}")
            # self.module.log(msg=f" text    : {response.text} / {type(response.text)}")
            # self.module.log(msg=f" json    : {response.json()} / {type(response.json())}")
            # self.module.log(msg=f" headers : {response.headers}")
            # self.module.log(msg=f" code    : {response.status_code}")
            # self.module.log(msg="------------------------------------------------------------------")

            return response.status_code, response.json()
