#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Crypto.PublicKey.RSA import RsaKey

from .auth import AuthManager
from .utils import Utilities, get_current_api_version
import sys
import base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5


class ComputeAPI:
    def __init__(self, client: AuthManager):
        self.token: str = client.token
        self.region: str = client.region
        self.project_id: str = client.project_id
        self.base_url: str = "https://compute.{region}.cloud.global.fujitsu.com".format(
            region=self.region
        )

        self.headers: dict = {"Accept": "application/json", "X-Auth-Token": self.token}
        self.current_api_version = get_current_api_version(self.list_api_versions())
        # microバージョン指定のないAPIもこのヘッダーを付与することで害は無いはずなのでデフォルトで付与しとく
        self.headers["OpenStack-API-Version"] = "compute {}".format(self.current_api_version)


    def list_api_versions(self):
        uri: str = "/"
        endpoint = self.base_url + uri
        response = Utilities.get(endpoint, headers=self.headers)

        if response['status'] == 'success':
            #return response['data'].json()
            return response['data']
        else:
            print("Could not retrieve the Blockstorage API version.")
            print(response['message'])
            sys.exit(1)


    def list_servers(self):
        uri = "/v2.1/{project_id}/servers".format(project_id=self.project_id)
        endpoint = self.base_url + uri
        headers = {"Accept": "application/json", "X-Auth-Token": self.token, "OpenStack-API-Version": "compute {}".format(self.current_api_version)}
        response = Utilities.get(endpoint, headers=headers)

        return response


    def list_servers_detailed(self):
        uri = "/v2.1/{project_id}/servers/detail".format(project_id=self.project_id)
        endpoint = self.base_url + uri
        headers = {"Accept": "application/json", "X-Auth-Token": self.token, "OpenStack-API-Version": "compute {}".format(self.current_api_version)}
        response = Utilities.get(endpoint, headers=headers)

        return response


    def show_server_password(self, server_id):
        uri: str = "/v2.1/{project_id}/servers/{server_id}/os-server-password".format(
            project_id=self.project_id,
            server_id=server_id
        )
        endpoint = self.base_url + uri
        headers = {"Accept": "application/json", "X-Auth-Token": self.token}
        response = Utilities.get(endpoint, headers=headers)

        return response


    def get_decrypted_password(self, server_id, private_key):
        password_data = self.show_server_password(server_id)
        private_key = RSA.import_key(private_key)
        if password_data['status'] == 'success':
            encrypted_password_bytes = password_data['data']['password']
            # base64 decode
            decoded_encrypted_password_bytes = base64.b64decode(encrypted_password_bytes)

            # RSA decryption
            cipher_rsa = PKCS1_v1_5.new(private_key)
            sentinel = object()
            decrypted_password_bytes = cipher_rsa.decrypt(decoded_encrypted_password_bytes, sentinel)

            if decrypted_password_bytes is sentinel:
                raise ValueError("Decryption failed")

            password = decrypted_password_bytes.decode('utf-8')

            return password
        else:
            print('get password failed')
