#!/bin/env python
# coding:utf-8

from qqbot import QQBot
from lib.blocks import Blocks
from lib.delegates import Delegates
from monitor import Monitor
import requests
import json


# class MiniMonitor(Monitor):
#     def latest_time(self):
#

class AschQQBot(QQBot):
    def onPollComplete(self, msgType, from_uin, buddy_uin, message):
        if message.find('@Asch小妹') == 0:
            if message == '@Asch小妹 price':
                res = self.price()
            elif message.find('@Asch小妹 delegate') == 0:
                res = self.delegate(message)
            elif message == '@Asch小妹 getheight':
                res = self.getheight()
            elif message == '@Asch小妹 info':
                res = self.info()
            else:
                res = self.usage()
            print res
            self.send(msgType, from_uin, res)

    def price(self):
        url = 'http://www.jubi.com/api/v1/ticker?coin=xas'
        res = json.loads(requests.get(url).text)
        res = "\t".join(['jubi.com', "最新成交价："+ str(round(float(res['last']), 3))+'CNY',"24小时成交量："+
                         str(int(res['vol']))+'XAS'])
        return res

    def delegate(self, message):
        m_li = message.split()
        if len(m_li) == 3:
            delegate_name = m_li[2].strip()
            payload = {'username': delegate_name}
            dres = Delegates().get_info(payload)
            if dres['success']:
                delegate = dres['delegate']
                pubkey = delegate['publicKey']
                mt = Monitor()
                data = mt.check_block(pubkey)
                if data['success']:
                    if len(data['blocks']) > 0:
                        last_block_time = data['blocks'][0]['timestamp']
                        # 这个是自asch主链创世块生成时间以来经历的秒数
                        difftime = mt.check_time(last_block_time)/60
                else:
                    print "warings:api返回成功但貌似没有数据", data
                res = [delegate_name, delegate['rate'], delegate['productivity'], delegate['rewards']/10**8,
                       str(difftime)+' minutes ago']
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

    def info(self):
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

    def usage(self):
        usage = '''
         Asch小妹目前可以实现的功能：
         1、price，查询asch的价格
         2、delegate 受托人名字，查询受托人的出块情况
         3、getheight，查询当前区块链高度
         4、info，asch相关介绍，如官网、github等

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
