#!/usr/bin/env python
# -*- coding: utf-8 -*-
from tokenize import endpats

from .auth import AuthManager
from .utils import Utilities


class VpnServiceAPI:
    def __init__(self, client: AuthManager):
        self.client: AuthManager = client
        self.token = client.token
        self.region = client.region
        self.base_url: str = "https://nfv.{region}.cloud.global.fujitsu.com".format(region=self.region)
        self.headers: dict = {"Accept": "application/json", "X-Auth-Token": self.token}


    """VPN Service
    """
    def list_vpn_services(self):
        uri = "/vpn/nfv/vpnservices"
        endpoint = self.base_url + uri
        response = Utilities.get(endpoint, headers=self.headers, timeout=120)

        return response


    def create_vpn_service(self, request_parameters: dict = None):
        uri = "/vpn/nfv/vpnservices"
        endpoint = self.base_url + uri
        response = Utilities.post(endpoint, headers=self.headers, json_data=request_parameters, timeout=120)

        return response


    def show_vpn_service_details(self, vpnservice_id: str):
        uri = "/vpn/nfv/vpnservices/{vpnservice_id}".format(vpnservice_id=vpnservice_id)
        endpoint = self.base_url + uri
        response = Utilities.get(endpoint, headers=self.headers, timeout=120)

        return response


    def update_vpn_service(self, vpnservice_id: str, request_parameters: dict = None):
        """
        Args:
            vpnservice_id: vpnservice_id(uuid)
            request_parameters: {"vpnservice": {<params>}

        """
        uri = "/vpn/nfv/vpnservices/{vpnservice_id}".format(vpnservice_id=vpnservice_id)
        endpoint = self.base_url + uri
        response = Utilities.put(endpoint, headers=self.headers, json_data=request_parameters, timeout=120)


    def delete_vpn_service(self, vpnservice_id: str):
        uri = f"/vpn/nfv/vpnservices/{vpnservice_id}".format(vpnservice_id=vpnservice_id)
        endpoint = self.base_url + uri
        response = Utilities.delete(endpoint, headers=self.headers, timeout=120)

        return response



    """IPsec Site Connection
    """
    def list_ipsec_site_connections(self):
        uri = "/vpn/nfv/ipsec-site-connections"
        endpoint = self.base_url + uri
        response = Utilities.get(endpoint, headers=self.headers)

        return response


    def show_ipsec_site_connection_details(self, connection_id: str):
       uri = "/vpn/nfv/ipsec-site-connections/{connection_id}".format(connection_id=connection_id)
       endpoint = self.base_url + uri
       response = Utilities.get(endpoint, headers=self.headers)

       return response


    def create_ipsec_site_connection(self, request_parameters: dict = None):
        uri = "/vpn/nfv/ipsec-site-connections"
        endpoint = self.base_url + uri
        response = Utilities.post(endpoint, headers=self.headers, json_data=request_parameters)

        return response


    def update_ipsec_site_connection(self, connection_id: str, request_parameters: dict):
        uri = "/vpn/nfv/ipsec-site-connections/{connection_id}".format(connection_id=connection_id)
        endpoint = self.base_url + uri
        response = Utilities.put(endpoint, headers=self.headers, json_data=request_parameters)

        return response


    def delete_ipsec_site_connection(self, connection_id: str):
        uri = "/vpn/nfv/ipsec-site-connections/{connection_id}".format(connection_id=connection_id)
        endpoint = self.base_url + uri
        response = Utilities.delete(endpoint, headers=self.headers)

        return response



    """IPsec Policy
    """
    def list_ipsec_policies(self):
        uri = "/vpn/nfv/ipsecpolicies"
        endpoint = self.base_url + uri
        response = Utilities.get(endpoint, headers=self.headers)

        return response


    def show_ipsec_policy_details(self, policy_id: str):
        uri = "/vpn/nfv/ipsecpolicies/{policy_id}".format(policy_id=policy_id)
        endpoint = self.base_url + uri
        response = Utilities.get(endpoint, headers=self.headers)

        return response


    def create_ipsec_policy(self, request_parameters: dict = None):
        uri = "/vpn/nfv/ipsecpolicies"
        endpoint = self.base_url + uri
        default_policy: dict = {
            "ipsecpolicy": {
                "name": "",
                "initiator": "bi-directional",
                "transform_protocol": "esp",
                "auth_algorithm": "sha1",
                "encapsulation_mode": "tunnel",
                "encryption_algorithm": "aes-128",
                "pfs": "group5",
                "lifetime": {
                    "units": "seconds",
                    "value": 3600
                }
            }
        }
        if request_parameters is None:
            request_data = default_policy
        else:
            request_data = request_parameters

        response = Utilities.post(endpoint, headers=self.headers, json_data=request_data)
        """TODO
        応答がJSONぽいがJSON形式で取得するとエラーになる
        {"ipsecpolicy": {"id":"1594369",}}
        Utilitiesを使わずに独自で実装した方が良いかも
        """

        return response


    def update_ipsec_policy(self, policy_id: str, request_parameters: dict):
        uri = "/vpn/nfv/ipsecpolicies/{policy_id}".format(policy_id=policy_id)
        endpoint = self.base_url + uri
        response = Utilities.put(endpoint, headers=self.headers, json_data=request_parameters)

        return response


    def delete_ipsec_policy(self, ipsecpolicy_id: str):
        uri = "/vpn/nfv/ipsecpolicies/{ipsecpolicy_id}".format(ipsecpolicy_id=ipsecpolicy_id)
        endpoint = self.base_url + uri
        response = Utilities.delete(endpoint, headers=self.headers)

        return response



    """IKE Policy
    """
    def list_ike_policies(self):
        uri = "/vpn/nfv/ikepolicies"
        endpoint = self.base_url + uri
        response = Utilities.get(endpoint, headers=self.headers)

        return response


    def show_ike_policy_details(self, policy_id: str):
        uri = "/vpn/nfv/ikepolicies/{policy_id}".format(policy_id=policy_id)
        endpoint = self.base_url + uri
        response = Utilities.get(endpoint, headers=self.headers)

        return response


    def create_ike_policy(self, request_parameters: dict = None):
        uri = "/vpn/nfv/ikepolicies"
        endpoint = self.base_url + uri
        default_policy: dict = {
            "ikepolicy": {
                "auth_algorithm": "sha2",
                "description": "",
                "encryption_algorithm": "aes-256",
                "lifetime": {
                    "units": "seconds",
                    "value": 2000
                },
                "name": "",
                "pfs": "group5",
                "phase1_negotiation_mode": "main"
            }
        }
        if request_parameters is None:
            request_data = default_policy
        else:
            request_data = request_parameters
        response = Utilities.post(endpoint, headers=self.headers, json_data=request_data)

        return response


    def update_ike_policy(self, policy_id: str, request_parameters: dict):
        uri = "/vpn/nfv/ikepolicies/{policy_id}".format(policy_id=policy_id)
        endpoint = self.base_url + uri
        response = Utilities.put(endpoint, headers=self.headers, json_data=request_parameters)

        return response


    def delete_ike_policy(self, ikepolicy_id: str):
        uri = "/vpn/nfv/ikepolicies/{ikepolicy_id}".format(ikepolicy_id=ikepolicy_id)
        endpoint = self.base_url + uri
        response = Utilities.delete(endpoint, headers=self.headers)

        return response
