#! /usr/bin/env python
# coding=utf8

import json
import time
from lib.accounts import Accounts
from lib.delegates import Delegates
from lib.blocks import Blocks
from lib.mail import *


class Monitor:
    """
    1.监控top101受托人的丢块信息，超过50分钟未出块视为丢块
    2.监控top101受托人的XAS余额，不足50000或者150000的要报警,已剔除官方账号asch_gxx done
    3.监控top101受托人节点记录的账户余额top100的信息是否一致（随机抽取2个节点在整点的时候进行对比，时间对10取模为0）
    """
    def __init__(self):
        self.delegate = Delegates()
        self.account = Accounts()
        self.blocks = Blocks()

    def get_top_101(self):
        payload = {'limit': 100,
                   'orderBy': 'approval:desc'
                   }
        return self.delegate.get_delegates(payload)

    def check_block(self, publickey):
        payload = {'generatorPublicKey': publickey,
                   'limit': 1,
                   'orderBy': 'height:desc'
                   }
        return self.blocks.get_blocks(payload)

    @staticmethod
    def check_time(last_block_time):
        now = int(time.time()) - 1467057600
        # UTC+8时区-asch创世块生成时间，即asch纪元元年0点(2016/6/28 4:0:0，js时间为UTC(2016, 5, 27, 20, 0, 0, 0) )
        difftime = now - last_block_time
        return difftime

    def check_time_batch(self, top_delegates):
        data = top_delegates
        issuse_delegates = []
        # for delegate in data['delegates'][1:3]:
        for delegate in data['delegates']:
            pubkey = delegate['publicKey']
            data = self.check_block(pubkey)
            if data['success']:
                if len(data['blocks']) > 0:
                    last_block_time = data['blocks'][0]['timestamp']    # 这个是自asch主链创世块生成时间以来经历的秒数
                    difftime = self.check_time(last_block_time)
                    if difftime > 50*60:
                        res = {'username': delegate['username'],
                               'rate': delegate['rate'],
                               'height': data['blocks'][0]['height'],
                               'behind_seconds': difftime}
                        issuse_delegates.append(res)
                else:
                    print "api返回成功但貌似没有数据", data
        return issuse_delegates

    @staticmethod
    def check_balance(top_delegates):
        data = top_delegates
        nsf = []    # 余额不足5万XAS(not sufficient funds)受托人账户列表
        if data['success']:
            for delegate in data['delegates']:
                if delegate['username'].find('asch_g') < 0:
                    if delegate['balance'] < 50000 * 100000000:
                        res = {'username': delegate['username'], 'balance': delegate['balance']/10**8}
                        nsf.append(res)
        return nsf

    @staticmethod
    def send_main(content):
        sub = 'asch_monitor'
        return send_mail(mailto_list, sub, content)


def main():
    time_start = time.time()
    monitor = Monitor()
    # print "pubkeys:", monitor.get_top_101()
    top_delegates = monitor.get_top_101()
    check_balance = monitor.check_balance(top_delegates)
    check_block_produce = monitor.check_time_batch(top_delegates)
    # print "余额不足5万XAS的：", check_balance
    # print "超过50分钟未出块：", check_block_produce
    time_end = time.time()
    time_excute = time_end - time_start
    # print "本次执行时间(秒):", time_excute
    if len(check_balance) > 0 or len(check_block_produce) > 0:
        content = {"check_balance": check_balance,
                   "check_block_produce": check_block_produce,
                   "time_excute_seconds": int(time_excute)}
        print "content:", content
        # res = monitor.send_main(str(json.dumps(content)))
        # print "email发送状态：",res
    else:
        print "没有余额不足或者丢块的受托人！"

if __name__ == "__main__":
    main()
