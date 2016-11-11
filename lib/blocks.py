# /usr/bin/env python
# coding=utf8

from http_api import HttpApi


class Blocks:
    """
    受托人delegates相关的api
    """

    def __init__(self):
        self.api = HttpApi()

    def execute(self, method, api, payload=None):
        return self.api.execute(method, api, payload)

    def get_blocks(self, payload):
        """
        获取block详情，不加参数则获取全网区块详情
        """
        api = '/api/blocks'
        return self.execute('get', api, payload)

    def get_height(self):
        """
        获取blockchain高度
        :return:block chain height
        """
        api = '/api/blocks/getHeight'
        return self.execute('get', api)


if __name__ == "__main__":
    block = Blocks()
    payload = {'generatorPublicKey': '4207a6f842e6b52f85a701e0eea31e197bbfc47a26734c62a5bb3d61ee1f5cd6',
               'limit': 1,
               'orderBy': 'height:desc'
               }
    print 'res:', block.get_blocks(payload)
