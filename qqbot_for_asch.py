#!/bin/env python
# coding:utf-8
# at least python 2.7.9

from qqbot import QQBot
from lib.accounts import Accounts
from lib.blocks import Blocks
from lib.delegates import Delegates
from monitor import Monitor
import requests
import json


class AschQQBot(QQBot):
    dsp = '请给受托人zhenxi投票，非常感谢。本广告位租赁价格：100XAS/天'
    delegates = Delegates()
    accounts = Accounts()
    blocks = Blocks()
    mt = Monitor()

    def onPollComplete(self, msgtype, from_uin, buddy_uin, message):
        if message.find('@Asch小妹') == 0:
            if message == '@Asch小妹 price':
                res = self.price()
            elif message.find('@Asch小妹 delegate') == 0:
                res = self.delegate(message)
            elif message.find('@Asch小妹 balance') == 0:
                res = self.balance(message)
            elif message == '@Asch小妹 getheight':
                res = self.getheight()
            elif message == '@Asch小妹 info':
                res = self.info()
            elif message == "@Asch小妹 help":
                res = self.usage()
            else:
                res = ["face", 33]
            print res
            self.send(msgtype, from_uin, res)

    @staticmethod
    def get_price(host, coin):
        url = host + '/api/v1/ticker?coin=' + coin
        res = json.loads(requests.get(url).text)
        # https not verify CA python 2.7.9 SNI
        return res

    def price(self):
        btc_price = float(self.get_price('https://jubi.com', 'btc')['last'])
        res_all = []
        platforms = [('https://btcbox.com', 'BTC'), ('http://jubi.com', 'CNY')]
        for i in platforms:
            host, unit = i
            res = self.get_price(host, 'xas')
            if unit == 'CNY':
                price = str(round(float(res['last']), 3)) + ' CNY'
            elif unit == 'BTC':
                price_btc = res['last']
                price_cny = round(float(price_btc) * btc_price, 3)
                price = str(price_btc) + ' BTC(' + str(price_cny) + 'CNY)'
            res = [host, "最新成交价：" + price, "24小时成交：" + str(int(res['vol']) / 10000) + '万XAS']
            res_all.extend(res)
        res_all = "\n".join(res_all)
        res_all = res_all + "\n\n" + self.dsp
        return res_all

    def delegate(self, message):
        m_li = message.split()
        # ['Asch小妹','delegate','zhenxi']
        if len(m_li) == 3:
            delegate_name = m_li[2].strip()
            payload = {'username': delegate_name}
            dres = self.delegates.get_info(payload)
            if dres['success']:
                delegate = dres['delegate']
                pubkey = delegate['publicKey']
                address = delegate['address']
                balance = self.get_balance(address)
                data = self.mt.check_block(pubkey)
                if data['success']:
                    if len(data['blocks']) > 0:
                        last_block_time = data['blocks'][0]['timestamp']
                        # 这个是自asch主链创世块生成时间以来经历的秒数
                        difftime = str(self.mt.check_time(last_block_time) / 60) + '分钟之前'
                    else:
                        # print "warings:api返回成功但貌似没有数据 or not top101", data
                        difftime = '非前101名，不产块'
                res = ['受托人：' + delegate_name, '排名：' + str(delegate['rate']), '生产率：' +
                       str(delegate['productivity']), '锻造总额：' + str(delegate['rewards'] / 10 ** 8) + 'XAS',
                       '账户余额：' + str(balance) + 'XAS', '最后出块时间：' + difftime]
            else:
                res = ['受托人' + delegate_name + '不存在']
            res.append(self.dsp)
            res = '\n'.join(res)
        else:
            res = self.usage()
        return str(res)

    def getheight(self):
        res = self.blocks.get_height()
        if res['success']:
            height = res['height']
        else:
            height = None
        return '当前区块高度为：' + str(height)

    def get_balance(self, address):
        payload = {'address': address}
        rs = self.accounts.balance(payload)
        if rs['success']:
            balance = round(rs['balance']/10**8, 1)
        else:
            balance = '查询出错'
        return balance

    def balance(self, message):
        m_li = message.split()
        # ['Asch小妹','balance','top101_delegates']
        if len(m_li) == 3:
            address = m_li[2].strip()
            if address == 'top101_delegates':
                pass
            elif address.isdigit():
                balance = self.get_balance(address)
                res = address + '余额为：' + str(balance) + 'XAS'
            else:
                res = self.usage()
        else:
            res = self.usage()
        return res

    @staticmethod
    def info():
        info = '''
        官网：www.asch.so
        白皮书：www.asch.so/asch-whitepaper.pdf
        github：github.com/sqfasd/asch
        asch相关文档：https://github.com/sqfasd/asch_docs
        asch共识机制：http://blog.asch.so/2016/08/11/asch-consensus-and-fault-tolerance/
        QQ群：545183438（开发者）
        社区：forum.asch.so
        '''
        return info

    @staticmethod
    def usage():
        usage = '''
         Asch小妹目前可以实现的功能：
         1、price，查询asch的价格
         2、delegate 受托人名字，查询受托人的出块情况
         3、getheight，查询当前区块链高度
         4、info，asch相关介绍，如官网、github等
         5、help，查看Asch小妹的功能列表

         举例：@Asch小妹 price，可以获取到XAS当前的价格
         '''
        usage = usage + '\t' + AschQQBot.dsp
        return usage


def main():
    myqqbot = AschQQBot()
    myqqbot.Login()
    myqqbot.Run()


if __name__ == "__main__":
    main()
