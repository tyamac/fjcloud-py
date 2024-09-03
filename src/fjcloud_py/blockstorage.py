#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .auth import AuthManager
from .utils import Utilities, to_dict_without_none, get_current_api_version
from .schemas import CreateBackupRequest


class BlockstorageAPI:
    def __init__(self, client: AuthManager):
        self.token: str = client.token
        self.region: str = client.region
        self.project_id: str = client.project_id
        self.base_url: str = "https://blockstorage.{region}.cloud.global.fujitsu.com".format(
            region=self.region
        )

        self.headers: dict = {"Accept": "application/json", "X-Auth-Token": self.token}

        self.current_api_version: str = self.list_api_versions().current_api_version


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
                return str(self.api_versions)

            def __str__(self):
                return str(self.api_versions)

            def __repr__(self):
                return f"CurrentApiVersion(api_versions={self.api_versions}, current_api_version={self.current_api_version})"

        uri: str = "/"
        endpoint = self.base_url + uri
        response = Utilities.get(endpoint, headers=self.headers)

        return CurrentApiVersion(response.json())


    def list_accessible_volumes(self):
        class VolumeList:
            def __init__(self, response_json):
                self.response_json = response_json

            @property
            def volumes(self):
                return self.response_json

            @property
            def ids(self):
                return [volume['id'] for volume in self.volumes['volumes']]

            def __iter__(self):
                return iter(self.volumes)

            def __str__(self):
                return str(self.volumes)

            def __repr__(self):
                return f"VolumeList(volumes={self.volumes}, ids={self.ids})"

        uri: str = "/v3/{project_id}/volumes".format(project_id=self.project_id)
        endpoint: str = self.base_url + uri
        response = Utilities.get(endpoint, headers=self.headers)

        return VolumeList(response.json())


    def list_backups(self):
        class BackupList:
            def __init__(self, response_json):
                self.response_json = response_json

            @property
            def backups(self):
                return self.response_json

            @property
            def ids(self):
                return [backup['id'] for backup in self.backups['backups']]

            def __iter__(self):
                return iter(self.backups)

            def __str__(self):
                return str(self.backups)

            def __repr__(self):
                return f"BackupList(backups={self.backups}, ids={self.ids})"

        uri: str = "/v3/{project_id}/backups".format(project_id=self.project_id)
        endpoint: str = self.base_url + uri
        response = Utilities.get(endpoint, headers=self.headers)

        return BackupList(response.json())


    def list_backups_detail(self):
        uri: str = "/v3/{project_id}/backups/detail".format(project_id=self.project_id)
        endpoint: str = self.base_url + uri
        response = Utilities.get(endpoint, headers=self.headers)

        return response.json()


    def show_backup_detail(self, backup_id: str):
        uri: str = "/v3/{project_id}/backups/{backup_id}".format(
            project_id = self.project_id,
            backup_id = backup_id
        )
        endpoint: str = self.base_url + uri
        response = Utilities.get(endpoint, headers=self.headers)

        return response.json()

    def delete_backup(self, backup_id: str):
        uri: str = "/v3/{project_id}/backups/{backup_id}".format(
            project_id=self.project_id,
            backup_id=backup_id
        )
        endpoint: str = self.base_url + uri
        response = Utilities.delete(endpoint, headers=self.headers)

        return response


    def create_backup(self, request_parameters: CreateBackupRequest):
        if request_parameters is None:
            raise ValueError("request_parameters must be provided")
        uri: str = "/v3/{project_id}/backups".format(project_id=self.project_id)
        endpoint: str = self.base_url + uri
        # metadataを含むリクエストには最新のマイクロバージョンを指定する必要がある
        headers =  {"Accept": "application/json", "X-Auth-Token": self.token, "OpenStack-API-Version": "volume {}".format(self.current_api_version)}
        print(headers)

        # Noneを削除したあとのrequest_parametersをbackupキーを含むリクエストに変換
        request_dict: dict = {"backup": to_dict_without_none(request_parameters)}

        response = Utilities.post(endpoint, headers=headers, json_data=request_dict)

        return response.json()
