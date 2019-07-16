import hmac
from collections import defaultdict
from functools import wraps

import requests

class Error(Exception):
    def __init__(self, status_code, retcode=None):
        self.status_code = status_code
        self.retcode = retcode

def _api_client(url):
    def do_call(**kwargs):
        headers = {}
        resp = requests.post(url, json=kwargs, headers=headers)
        if resp.ok:
            data = resp.json()
            if data.get('status') == 'failed':
                raise Error(resp.status_code, data.get('retcode'))
            return data.get('data')
        raise Error(resp.status_code)
    return do_call

class CQ:
    _api_root='http://127.0.0.1:5600'
    def __getattr__(self, item):
        if self._api_root:
            return _api_client(self._api_root + '/' + item)

