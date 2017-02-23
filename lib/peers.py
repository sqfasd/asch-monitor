# /usr/bin/env python
# coding=utf8

from http_api import HttpApi


class Peers:
    """
    账户accounts相关的api
    """

    def __init__(self):
        self.api = HttpApi()

    def peers(self, payload):
        """
        获取全网节点信息
        :param payload
        :type payload: dict
        state	integer	N	节点状态,0: ,1:,2:,3:
        os	string	N	内核版本
        version	string	N	asch版本号
        limit	integer	N	限制结果集个数，最小值：0,最大值：100
        orderBy	string	N
        offset	integer	N	步长，最小值0
        port	integer	N	端口，1~65535
        :return
        """
        api = '/api/peers'
        return self.api.execute('get', api, payload)


if __name__ == '__main__':
    peers = Peers()
    all_peers = peers.peers('')
    print all_peers

