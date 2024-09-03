#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .utils import Utilities
from .schemas import Credential
import requests


class AuthManager:
    def __init__(self, credential: Credential):
        self.region: str = credential.region
        self.domain_name: str = credential.domain_name
        self.project_id: str = credential.project_id
        self.username: str = credential.username
        self.password: str = credential.password
        self.identity_url: str = "https://identity.{region}.cloud.global.fujitsu.com/v3/auth/tokens".format(
            region=self.region
        )
        self.token: str = self.get_token()


    def get_token(self):
        headers = {"Content-Type": "application/json", "Accept": "application/json"}
        data = {
            "auth": {
                "identity": {
                    "methods": ["password"],
                    "password": {
                        "user": {
                            "domain": {"name": self.domain_name},
                            "name": self.username,
                            "password": self.password,
                        }
                    }
                },
                "scope": {"project": {"id": self.project_id}},
            }
        }

        response = Utilities.post(self.identity_url, headers=headers, json_data=data)
        token: str = response.headers["X-Subject-Token"]

        return token


    def validate_token(self):
        headers = {"X-Auth-Token": self.token}
        response = requests.get(self.identity_url, headers=headers)

        return response