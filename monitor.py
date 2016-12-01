#!/usr/bin/env python
# coding=utf8

import time
import random
import requests
import json
from lib.accounts import Accounts
from lib.delegates import Delegates
from lib.blocks import Blocks
from lib.peers import Peers
from lib.mail import *
from lib.format import MyPrint


class Monitor:
    """
    1.监控top101受托人的丢块信息，超过50分钟未出块视为丢块	done
    2.监控top101受托人的XAS余额，不足50000或者150000的要报警,已剔除官方账号asch_g done
    3.监控top101受托人节点记录的账户余额top100的信息是否一致（随机抽取2个节点在整点的时候进行对比，时间对10取模为0）done
    """
    def __init__(self):
        self.delegate = Delegates()
        self.account = Accounts()
        self.blocks = Blocks()
        self.peers = Peers()

    def get_peers(self):
        rs = self.peers.peers('')
        if rs['success']:
            res = rs['peers']
        else:
            res = None
        return res

    def get_top100_balance(self):
        res = self.account.top('')
        return res

    def check_peers(self):
        peers = self.get_peers()
        if peers is not None:
            cnt = len(peers)
            num = random.randint(0, cnt-1)
            ip = peers[num]['ip']
            port = str(peers[num]['port'])
            url = 'http://' + ip + ':' + port + '/api/accounts/top'
            rs = json.loads(requests.get(url).text)
            # print 'rs is:', rs
            rs_official = self.get_top100_balance()
            # print 'rs_official is:', rs_official
            res = []
            if rs['success'] and rs_official['success']:
                for i in range(0, 99):
                    balance = rs['accounts'][i]['balance']
                    balance_official = rs_official['accounts'][i]['balance']
                    # print 'balance:', balance, 'balance_official', balance_official
                    if balance != balance_official:
                        res.append([ip, rs['accounts'][i]['address'], str(balance)+'XAS'])
                        res.append(['mainnet.asch.so', rs_official['accounts'][i]['address'], str(balance_official) +
                                    'XAS'])
                        break
                if len(res) == 0:
                    res.append("The top 100 accounts's balance of "+ip+":"+str(port)+" is same with mainnet.asch.so.")
            return res

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
        issue_delegates = []
        # for delegate in data['delegates'][1:3]:
        for delegate in data['delegates']:
            pubkey = delegate['publicKey']
            data = self.check_block(pubkey)
            if data['success']:
                if len(data['blocks']) > 0:
                    last_block_time = data['blocks'][0]['timestamp']    # 这个是自asch主链创世块生成时间以来经历的秒数
                    difftime = self.check_time(last_block_time)
                    if difftime > 50*60:
                        res = [delegate['username'], str(delegate['rate']), str(data['blocks'][0]['height']),
                               str(round(difftime/60/60, 2))]
                        issue_delegates.append(res)
                else:
                    print "warings:api返回成功但貌似没有数据", data
        return issue_delegates

    @staticmethod
    def check_balance(top_delegates):
        data = top_delegates
        del_150k_xas = open('config/delegate_150k_xas.txt', 'r').readlines()
        nsf = []    # 余额不足5万XAS(not sufficient funds)受托人账户列表
        if data['success']:
            for delegate in data['delegates']:
                name = delegate['username'].strip()
                balance = delegate['balance']/10**8
                if name.find('asch_g') < 0:
                    if name+'\n' in del_150k_xas:    # 需要150k的受托人
                        # print name, balance
                        if balance < 15*10000:
                            res = [name, str(balance)]
                            nsf.append(res)
                    else:                           # 需要50k的受托人
                        if balance < 5*10000:
                            res = [name, str(balance)]
                            nsf.append(res)
        return nsf

    @staticmethod
    def send_mail(content):
        sub = 'asch_monitor'
        return send_mail(mailto_list, sub, content)


def main():
    time_start = time.time()
    now = time.strftime("%Y-%m-%d-%H-%M-%S")
    logname = 'monitor'
    logfile = "logs/%s_%s.log" % (logname, now)
    mp = MyPrint(logfile)
    monitor = Monitor()
    check_top100_balance = monitor.check_peers()
    # print check_top100_balance
    top_delegates = monitor.get_top_101()
    check_balance = monitor.check_balance(top_delegates)
    check_block_produce = monitor.check_time_batch(top_delegates)

    time_end = time.time()
    time_excute = time_end - time_start

    if len(check_top100_balance) == 1:       # 节点ip的前100名用户余额和官方节点不一致
        mp.my_print(check_top100_balance)
    else:
        mp.my_print(["The following peer's balance of top100  is different with mainnet.asch.so."])
        for i in check_top100_balance:
            mp.my_print(i)
    mp.my_print([''])

    if len(check_block_produce) > 0:        # 丢块的受托人
        mp.my_print(["The following delegates are missing block:"])
        mp.my_print(['username', 'rate', 'height', 'behinds_hours'])
        for i in check_block_produce:
            mp.my_print(i)
    else:
        mp.my_print(["There is no delegate of 'top 101' missing block."])
    mp.my_print([''])

    if len(check_balance) > 0:              # 余额不足的受托人
        mp.my_print(['The fllowing delegates have not sufficient funds:'])
        mp.my_print(['username', 'balance'])
        for i in check_balance:
            mp.my_print(i)
    else:
        mp.my_print(["There is no delegate of 'not sufficient funds' exist."])
    mp.my_print([''])

    mp.my_print(['time_excute_seconds:', str(int(time_excute))])

    if len(check_block_produce) > 0 or len(check_balance) > 0 or len(check_top100_balance) > 1:
        content = ''
        lines = open(logfile, 'r').readlines()
        for i in lines:
            content += i
        res = monitor.send_mail(content)
        mp.my_print(["email发送状态：", str(res)])

if __name__ == "__main__":
    main()
