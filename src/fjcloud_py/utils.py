#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dataclasses import asdict
from requests.exceptions import HTTPError, Timeout, RequestException
import requests
import sys



class Utilities:
    @staticmethod
    def get(url: str, headers: dict = None, params: dict = None, timeout: int = 120) -> dict:
        """
        Args:
            url: [require] Endpoint (ServiceEndpoint + URI)
            headers: [require] Headers
            params: [optional] Query parameters
            timeout: [optional] Timeout
        Returns:
            dict: {'status': ['success'|'error'], 'data': [data|None], 'message': [message|None]}
        """
        try:
            response = requests.get(url, headers=headers, params=params, timeout=timeout)
            response.raise_for_status()
            return {
                'status': 'success',
                'data': response.json(),
                'message': None
            }
        except HTTPError as http_err:
            #print(http_err.response.json())
            return {
                'status': 'error',
                'data': None,
                'message': http_err.response.json()
            }
        except Timeout as timeout_err:
            #print(timeout_err.response.json())
            return {
                'status': 'error',
                'data': None,
                'message': timeout_err.response.json()
            }
        except RequestException as req_err:
            #print(req_err.response.json())
            return {
                'status': 'error',
                'data': None,
                'message': req_err.response.json()
            }
        except Exception as err:
            print(f'An error occurred: {err}')  # その他の予期しないエラー
            return {
                'status': 'error',
                'data': None,
                'message': err
            }


    @staticmethod
    def post(url: str, headers: dict = None, params: dict = None, json_data :dict = None, timeout: int = 10) -> dict:
        """
        Args:
            url: [require] Endpoint (ServiceEndpoint + URI)
            headers: [require] Headers
            params: [optional] Query parameters
            json_data: [optional] Request body
            timeout: [optional] Timeout
        Returns:
            dict: "{'status': [success|error], 'data': [data|None], 'message': [message|None]}"
        """
        try:
            response = requests.post(url, params=params, headers=headers, json=json_data, timeout=timeout)
            response.raise_for_status()
            return {
                'status': 'success',
                'data': response.json(),
                'message': None
            }
        except HTTPError as http_err:
            #print(http_err.response.json())
            return {
                'status': 'error',
                'data': None,
                'message': http_err.response.json()
            }
        except Timeout as timeout_err:
            #print(timeout_err.response.json())
            return {
                'status': 'error',
                'data': None,
                'message': timeout_err.response.json()
            }
        except RequestException as req_err:
            #print(req_err.response.json())
            return {
                'status': 'error',
                'data': None,
                'message': req_err.response.json()
            }
        except Exception as err:
            #print(f'An error occurred: {err}')  # その他の予期しないエラー
            return {
                'status': 'error',
                'data': None,
                'message': err
            }


    @staticmethod
    def put(url: str, headers: dict = None, params: dict = None, json_data: dict = None, timeout: int = 10):
        try:
            response = requests.put(url, headers=headers, params=params, json=json_data, timeout=timeout)
            response.raise_for_status()
            return {
                'status': 'success',
                'data': response.json(),
                'message': None
            }
        except HTTPError as http_err:
            #print(http_err.response.json())
            return {
                'status': 'error',
                'data': None,
                #'message': http_err.response.json()
                'message': http_err.response.json() if http_err.response else str(http_err)
            }
        except Timeout as timeout_err:
            #print(timeout_err.response.json())
            return {
                'status': 'error',
                'data': None,
                #'message': timeout_err.response.json()
                'message': timeout_err.response.json() if timeout_err.response else str(timeout_err)
            }
        except RequestException as req_err:
            #print(req_err.response.json())
            return {
                'status': 'error',
                'data': None,
                #'message': req_err.response
                'message': req_err.response.json() if req_err.response else str(req_err)
            }
        except Exception as err:
            #print(f'An error occurred: {err}')  # その他の予期しないエラー
            return {
                'status': 'error',
                'data': None,
                #'message': err
                'message': str(err)
            }


    @staticmethod
    def delete(url: str, headers: dict = None, params: dict = None, timeout: int = 10) -> dict:
        try:
            response = requests.delete(url, headers=headers, params=params, timeout=timeout)
            response.raise_for_status()
            return {
                'status': 'success',
                'data': None,
                'message': None
            }
        except HTTPError as http_err:
            return {
                'status': 'error',
                'data': None,
                'message': http_err.response.json()
            }
        except Timeout as timeout_err:
            return {
                'status': 'error',
                'data': None,
                'message': timeout_err.response.json()
            }
        except RequestException as req_err:
            return {
                'status': 'error',
                'data': None,
                'message': req_err.response.json()
            }
        except Exception as err:
            return {
                'status': 'error',
                'data': None,
                'message': err
            }



# Convert dataclass to dict and remove keys with value None
#@staticmethod
def to_dict_without_none(data_class_instance):
    return {k: v for k, v in asdict(data_class_instance).items() if v is not None}



def get_current_api_version(versions_json: dict):
    current_api_version_detail = [
        version for version in versions_json['versions'] if version['status'] == 'CURRENT'
    ]
    if not current_api_version_detail:
        raise ValueError('No current API version found')
    current_api_version = current_api_version_detail[0]['version']
    return current_api_version

