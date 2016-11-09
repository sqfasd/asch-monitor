# /usr/bin/env python
# coding=utf8

import json
import requests


class HttpApi:
    """asch api的基类"""

    def __init__(self):
        self.ip = 'mainnet.asch.so'
        self.port = 80
        self.baseurl = 'http://' + self.ip + ':' + str(self.port)
        self.headers = {'content-type': 'application/json'}

    def execute(self, method, api, payload):
        url = self.baseurl + api
        if method == 'get':
            return self.get(url, payload)
        elif method == 'post':
            return self.post(url, payload)
        elif method == 'put':
            return self.put(url, payload)

    def get(self, url, payload):
        r = requests.get(url, params=payload)
        # return r.url
        return json.loads(r.text)

    def post(self, url, payload):
        r = requests.post(url, data=json.dumps(payload), headers=self.headers)
        return json.loads(r.text)

    def put(self, url, payload):
        r = requests.put(url, data=json.dumps(payload), headers=self.headers)
        return json.loads(r.text)

if __name__ == "__main__":
        httpapi = HttpApi()
        api = '/api/accounts'
        payload = {'address': '3472613124807570233'}
        print httpapi.execute('get', api, payload)
