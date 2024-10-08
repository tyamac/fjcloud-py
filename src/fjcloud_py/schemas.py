#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import Optional, Any


@dataclass
class Credential:
    """
    Credential class for storing authentication information.

    Attributes:
        region (str): The region for the authentication.
        domain_name (str): The domain name for the authentication.
        project_id (str): The project ID for the authentication.
        username (str): The username for the authentication.
        password (str): The password for the authentication.
    """
    region: str
    domain_name: str
    project_id: str
    username: str
    password: str

    @property
    def auth_url(self):
        """
        Constructs the identity URL based on the region.

        Returns:
            str: The identity URL.
        """
        return "https://identity.{region}.cloud.global.fujitsu.com/v3/auth/tokens".format(region=self.region)


#@dataclass
#class CurrentApiVersion:
#    version: str | None
#    endpoint: str | None


@dataclass
class CreateBackupRequest:
    """
    リクエストオブジェクト、バックアップを作成するために使用される。

    Attributes:
        volume_id (str): バックアップ対象のボリュームのID。必須。
        description (Optional[str]): バックアップの説明。デフォルトは None。
        incremental (Optional[bool]): 増分バックアップを行うかどうか。デフォルトは False。
        force (Optional[bool]): 強制的にバックアップを作成するかどうか。デフォルトは False。
        name (Optional[str]): バックアップの名前。デフォルトは None。
        snapshot_id (Optional[str]): スナップショットのID。デフォルトは None。
        metadata (Optional[dict]): バックアップに関連付けるメタデータ。デフォルトは None。

    Note:
        MicroVersion: > 3.43
    """
    volume_id: str = ""
    description: Optional[str] = None
    incremental: Optional[bool] = False
    force: Optional[bool] = False
    name: Optional[str] = None
    snapshot_id: Optional[str] = None
    metadata: Optional[dict] = None
    """MicroVersion: > 3.43"""
