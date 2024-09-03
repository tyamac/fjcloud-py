#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .auth import AuthManager
from .utils import Utilities, get_current_api_version


class ComputeAPI:
    def __init__(self, client: AuthManager):
        self.client: AuthManager = client
        self.token = client.token
        self.base_url: str = "https://compute.{region}.cloud.global.fujitsu.com".format(
            region=self.client.region
        )
        self.headers: dict = {"Accept": "application/json", "X-Auth-Token": self.token}

        self.current_api_version = self.list_api_versions().current_api_version


    def list_api_versions(self):
        class CurrentApiVersion:
            def __init__(self, response_json):
                self.response_json = response_json

            @property
            def api_versions(self):
                return self.response_json

            @property
            def current_api_version(self):
                return get_current_api_version(self.api_versions)

            def __iter__(self):
                return iter(str(self.api_versions))

            def __str__(self):
                return str(self.api_versions)

            def __repr__(self):
                return f"CurrentApiVersion(api_versions={self.api_versions}, current_api_version={self.current_api_version})"
        uri = "/"
        endpoint = self.base_url + uri
        response = Utilities.get(endpoint, headers=self.headers)
        #return response.json()
        return CurrentApiVersion(response.json())



    def list_servers(self):
        uri = "/v2.1/{project_id}/servers".format(project_id=self.client.project_id)
        endpoint = self.base_url + uri
        headers = {"Accept": "application/json", "X-Auth-Token": self.token, "OpenStack-API-Version": "compute {}".format(self.current_api_version)}
        response = Utilities.get(endpoint, headers=headers)

        return response.json()

