#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dataclasses import asdict
from requests.exceptions import HTTPError, Timeout, RequestException
import requests


class Utilities:
    @staticmethod
    def get(url: str, headers: dict = None, params: dict = None):

        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            return response
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')  # 例: 404 Not Found など
            return None
        except Timeout as timeout_err:
            print(f'Timeout error occurred: {timeout_err}')  # タイムアウトが発生
            return None
        except RequestException as req_err:
            print(f'Request exception: {req_err}')  # その他のリクエスト関連のエラー
            return None
        except Exception as err:
            print(f'An error occurred: {err}')  # その他の予期しないエラー
            return None




    @staticmethod
    def post(url: str, headers: dict = None, params: dict = None, json_data :dict = None):

        try:
            response = requests.post(url, params=params, headers=headers, json=json_data)
            response.raise_for_status()
            return response
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')  # 例: 404 Not Found など
            return None
        except Timeout as timeout_err:
            print(f'Timeout error occurred: {timeout_err}')  # タイムアウトが発生
            return None
        except RequestException as req_err:
            print(f'Request exception: {req_err}')  # その他のリクエスト関連のエラー
            return None
        except Exception as err:
            print(f'An error occurred: {err}')  # その他の予期しないエラー
            return None


    @staticmethod
    def put(url: str, headers: dict = None, params: dict = None, json_data: dict = None):
        #response = requests.put(url, headers=headers, params=params, data=json_data)

        try:
            response = requests.put(url, headers=headers, params=params, json=json_data)
            response.raise_for_status()
            return response
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')  # 例: 404 Not Found など
            #return None
            return http_err
        except Timeout as timeout_err:
            print(f'Timeout error occurred: {timeout_err}')  # タイムアウトが発生
            #return None
            return timeout_err
        except RequestException as req_err:
            print(f'Request exception: {req_err}')  # その他のリクエスト関連のエラー
            #return None
            return req_err
        except Exception as err:
            print(f'An error occurred: {err}')  # その他の予期しないエラー
            #return None
            return None



    @staticmethod
    def delete(url: str, headers: dict = None, params: dict = None):
        #response = requests.delete(url, headers=headers, params=params)

        try:
            response = requests.delete(url, headers=headers, params=params)
            response.raise_for_status()
            return response
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')  # 例: 404 Not Found など
            return None
        except Timeout as timeout_err:
            print(f'Timeout error occurred: {timeout_err}')  # タイムアウトが発生
            return None
        except RequestException as req_err:
            print(f'Request exception: {req_err}')  # その他のリクエスト関連のエラー
            return None
        except Exception as err:
            print(f'An error occurred: {err}')  # その他の予期しないエラー
            return None


# Convert dataclass to dict and remove keys with value None
#@staticmethod
def to_dict_without_none(data_class_instance):
    return {k: v for k, v in asdict(data_class_instance).items() if v is not None}



def get_current_api_version(versions_json):
    current_api_version_detail = [
        version for version in versions_json['versions'] if version['status'] == 'CURRENT'
    ]
    if not current_api_version_detail:
        raise ValueError('No current API version found')
    current_api_version = current_api_version_detail[0]['version']
    return current_api_version

