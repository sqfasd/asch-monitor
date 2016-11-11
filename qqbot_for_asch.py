#!/bin/env python
# coding:utf-8

from qqbot import QQBot
from lib.blocks import Blocks
from lib.delegates import Delegates
import requests
import json


class AschQQBot(QQBot):
    def onPollComplete(self, msgType, from_uin, buddy_uin, message):
        if message.find('@Asch小妹') == 0:
            if message == '@Asch小妹 price':
                res = self.price()
            elif message.find('@Asch小妹 delegate') == 0:
                res = self.delegate(message)
            elif message == '@Asch小妹 getheight':
                res = self.getheight()
            else:
                res = self.usage()
            print res
            self.send(msgType, from_uin, res)

    def price(self):
        url = 'http://www.jubi.com/api/v1/ticker?coin=xas'
        res = json.loads(requests.get(url).text)
        res = "\t".join(['jubi.com', "最新成交价："+ str(round(float(res['last']), 3)),"24小时成交量："+
                         str(int(res['vol']))])
        return res

    def delegate(self, message):
        m_li = message.split()
        if len(m_li) == 3:
            delegate_name = m_li[2].strip()
            payload = {'username': delegate_name}
            dres = Delegates().get_info(payload)
            if dres['success']:
                delegate = dres['delegate']
                res = [delegate_name, delegate['rate'], delegate['productivity'], delegate['rewards']/10**8]
            else:
                res = '受托人'+delegate_name+'不存在'
        else:
            res = self.usage()
        return str(res)

    def getheight(self):
        res = Blocks().get_height()
        if res['success']:
            height = res['height']
        return '当前区块高度为：' + str(height)

    def usage(self):
        usage = '''
         目前支持的用法：
         1.price，查询asch的价格
         2.delegate 受托人名字，查询受托人的出块情况
         3.getheight，查询当前区块链高度

         举例：@Asch小妹 price，可以获取到asch当前的价格
         广告位：没事了可以给zhenxi投票玩~ ~
         '''
        return usage


def main():
    myqqbot = AschQQBot()
    myqqbot.Login()
    myqqbot.Run()

if __name__ == "__main__":
    main()
