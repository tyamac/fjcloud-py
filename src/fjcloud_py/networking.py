#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .auth import AuthManager
from .utils import Utilities


class NetworkingAPI:
    def __init__(self, client: AuthManager):
        self.client: AuthManager = client
        self.token = client.token
        self.region = client.region
        self.base_url: str = "https://networking.{region}.cloud.global.fujitsu.com".format(region=self.region)
        self.headers: dict = {"Accept": "application/json", "X-Auth-Token": self.token}


    def list_networks(self):
        uri = "/v2.0/networks"
        endpoint = self.base_url + uri
        response = Utilities.get(endpoint, headers=self.headers)

        return response.json()


    def show_network_details(self, network_id: str):
        uri = "/v2.0/networks/{network_id}".format(network_id=network_id)
        endpoint = self.base_url + uri
        response = Utilities.get(endpoint, headers=self.headers)

        return response.json()


    def create_network(self, request_parameters: dict = None):
        uri = "/v2.0/networks"
        endpoint = self.base_url + uri
        if request_parameters is None:
            request_data = {"network": {}}
        else: # 引数にパラメータが与えられたときにチェックする
            request_data = request_parameters

        response = Utilities.post(endpoint, headers=self.headers, json_data=request_data)

        return response.json()


    def update_network(self, network_id: str, request_parameters: dict = None):
        uri = "/v2.0/networks/{network_id}".format(network_id=network_id)
        endpoint = self.base_url + uri
        if request_parameters is None:
            request_data = {"network": {}}
        else:
            request_data = request_parameters

        response = Utilities.put(endpoint, headers=self.headers, json_data=request_data)

        return response.json()


    def delete_network(self, network_id: str):
        uri = "/v2.0/networks/{network_id}".format(network_id=network_id)
        endpoint = self.base_url + uri
        response = Utilities.delete(endpoint, headers=self.headers)

        if response.status_code == 204:
            return None
        else:
            return response


    '''def bulc_create_networks(self, request_parameters: list):
        uri = "/v2.0/networks"
        endpoint = self.base_url + uri
        parameters_list = [params for params in request_parameters]
        request_data = {"networks": parameters_list}
        response = Utilities.post(endpoint, headers=self.headers, json_data=request_data)

        return response.json()
    '''