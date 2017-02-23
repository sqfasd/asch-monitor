# /usr/bin/env python
# coding=utf8

from http_api import HttpApi


class Accounts:
    """
    账户accounts相关的api
    """

    def __init__(self):
        self.api = HttpApi()

    def open(self, payload):
        """
        登陆
        :param
        """
        api = '/api/accounts/open/'
        return self.api.execute('post', api, payload)

    def accounts(self, payload):
        """
        查询账户信息
        """
        api = '/api/accounts'
        return self.api.execute('get', api, payload)

    def balance(self, payload):
        """
        :param payload:
        :return:
        """
        api = '/api/accounts/getBalance'
        return self.api.execute('get', api, payload)

    def vote(self, payload):
        """
        给受托人投票
        """
        api = '/api/accounts/delegates'
        return self.api.execute('put', api, payload)

    def voters(self, payload):
        """
        该账户为谁投了票
        """
        api = '/api/accounts/delegates'
        return self.api.execute('get', api, payload)

    def top(self, payload):
        """
        获取top账户
        :return:
        """
        api = '/api/accounts/top'
        return self.api.execute('get', api, payload)


if __name__ == "__main__":
        ac = Accounts()
        password = 'lounge barrel episode lock bounce power club boring slush disorder cluster client'

        payload = {'secret': password}
        print 'open', ac.open(payload)

        payload = {'address': '16358246403719868041'}
        print 'accounts', ac.accounts(payload)

        payload = {'secret': password,
                   'delegates': ["+11f4bd3e56c26d46465f68bdedef2570e6592a4ee041d471a2d5f3531c9c403c",
                                 "+8892024a6fa039cb7e973b4e5f20a10fdafab7731534064fc8f2946baaa79306"]
                   }
        print 'vote', ac.vote(payload)

        payload = {'address': '3472613124807570233'}
        print 'voters', ac.voters(payload)

