# /usr/bin/env python
# coding=utf8

from http_api import HttpApi


class Delegates:
    """
    受托人delegates相关的api
    """
    def __init__(self):
        self.api = HttpApi()

    def execute(self, method, api, payload):
        return self.api.execute(method, api, payload)

    def get_voters(self, payload):
        """
        谁给我投了票
        """
        api = '/api/delegates/voters'
        return self.execute('get', api, payload)

    def get_info(self, payload):
        """
        通过公钥或者用户名获取受托人信息
        """
        api = '/api/delegates/get'
        return self.execute('get', api, payload)

    def get_delegates(self, payload):
        """
        获取受托人列表
        """
        api = '/api/delegates'
        return self.execute('get', api, payload)

if __name__ == "__main__":
        delegate = Delegates()
        payload = {'publicKey': '4207a6f842e6b52f85a701e0eea31e197bbfc47a26734c62a5bb3d61ee1f5cd6'}
        print 'get_voters:', delegate.get_voters(payload)
        payload = {'limit': 100,
                   'orderBy': 'approval:desc'
                   }
        print 'res:', delegate.get_delegates(payload)
