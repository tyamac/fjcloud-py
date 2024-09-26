#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .auth import AuthManager
from .utils import Utilities, to_dict_without_none, get_current_api_version
from .schemas import CreateBackupRequest
import sys


class BlockstorageAPI:
    def __init__(self, client: AuthManager):
        self.token: str = client.token
        self.region: str = client.region
        self.project_id: str = client.project_id
        self.base_url: str = "https://blockstorage.{region}.cloud.global.fujitsu.com".format(
            region=self.region
        )

        self.headers: dict = {"Accept": "application/json", "X-Auth-Token": self.token}
        self.current_api_version = get_current_api_version(self._get_current_api_version())
        # microバージョン指定のないAPIもこのヘッダーを付与することで害は無いはずなのでデフォルトで付与しとく
        self.headers["OpenStack-API-Version"] = "volume {}".format(self.current_api_version)


    def _get_current_api_version(self):
        uri: str = "/"
        endpoint = self.base_url + uri
        response = Utilities.get(endpoint, headers=self.headers)
        if response['status'] == 'success':
            return response['data']
        else:
            print("Could not retrieve the Blockstorage API version.")
            print(response['message'])
            sys.exit(1)


    def list_api_versions(self) -> dict:
        uri: str = "/"
        endpoint = self.base_url + uri
        response = Utilities.get(endpoint, headers=self.headers)

        return response


    def list_accessible_volumes(self) -> dict:
        """
        Returns:
            dict: {'status': ['success'|'error'], 'data': [data|None], 'message': [message|None]}
        """
        uri: str = "/v3/{project_id}/volumes".format(project_id=self.project_id)
        endpoint: str = self.base_url + uri
        response = Utilities.get(endpoint, headers=self.headers)

        return response



    def list_backups(self) -> dict:
        """
        Returns:
            dict: {'status': ['success'|'error'], 'data': [data|None], 'message': [message|None]}
        """
        uri: str = "/v3/{project_id}/backups".format(project_id=self.project_id)
        endpoint: str = self.base_url + uri
        response = Utilities.get(endpoint, headers=self.headers)

        return response


    def list_backups_detail(self) -> dict:
        """
        Returns:
            dict: {'status': ['success'|'error'], 'data': [data|None], 'message': [message|None]}
        """
        uri: str = "/v3/{project_id}/backups/detail".format(project_id=self.project_id)
        endpoint: str = self.base_url + uri
        response = Utilities.get(endpoint, headers=self.headers)

        return response


    def show_backup_detail(self, backup_id: str) -> dict:
        """
        Returns:
            dict: {'status': ['success'|'error'], 'data': [data|None], 'message': [message|None]}
        """
        uri: str = "/v3/{project_id}/backups/{backup_id}".format(
            project_id = self.project_id,
            backup_id = backup_id
        )
        endpoint: str = self.base_url + uri
        response = Utilities.get(endpoint, headers=self.headers)

        return response


    def delete_backup(self, backup_id: str) -> dict:
        """
        Returns:
            dict: {'status': ['success'|'error'], 'data': [data|None], 'message': [message|None]}
        """
        uri: str = "/v3/{project_id}/backups/{backup_id}".format(
            project_id=self.project_id,
            backup_id=backup_id
        )
        endpoint: str = self.base_url + uri
        response = Utilities.delete(endpoint, headers=self.headers)

        return response


    def create_backup(self, request_parameters: CreateBackupRequest) -> dict:
        """
        Returns:
            dict: {'status': ['success'|'error'], 'data': [data|None], 'message': [message|None]}
        """
        if request_parameters is None:
            raise ValueError("request_parameters must be provided")
        uri: str = "/v3/{project_id}/backups".format(project_id=self.project_id)
        endpoint: str = self.base_url + uri
        # metadataを含むリクエストには最新のマイクロバージョンを指定する必要がある
        #headers =  {"Accept": "application/json", "X-Auth-Token": self.token, "OpenStack-API-Version": "volume {}".format(self.current_api_version)}
        #print(headers)

        # Noneを削除したあとのrequest_parametersをbackupキーを含むリクエストに変換
        request_dict: dict = {"backup": to_dict_without_none(request_parameters)}

        response = Utilities.post(endpoint, headers=self.headers, json_data=request_dict)

        return response