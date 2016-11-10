# /usr/bin/env python
# coding=utf8

import json
import time
from lib.accounts import *
from lib.delegates import *


class Vote:
    """
    投票相关api返回数据处理
    """
    def __init__(self, password, second_password):
        self.pwd = password
        self.second_pwd = second_password
        self.account = Accounts()
        self.delegate = Delegates()
        self.address, self.publickey = self.login()

    def login(self):
        payload = {'secret': self.pwd}
        ac_login = self.account.open(payload)['account']
        # ac_login = json.loads(ac_login)['account']
        address = ac_login['address']
        publickey = ac_login['publicKey']
        return [address, publickey]

    def get_vote_me(self):
        """
        谁给我投了票，只返回投票人中是受托人且余额大于1000XAS的公钥、用户名字典
        """
        payload = {'publicKey': self.publickey}
        res = self.delegate.get_voters(payload)['accounts']
        voteme_dict = {}
        for account in res:
            if account['username'] != '':
                if account['balance'] > 1000 * 100000000:
                    voteme_dict[account['publicKey']] = account['username']
        return voteme_dict

    def get_me_vote(self):
        """
        我给谁投了票
        """
        payload = {'address': self.address}
        res = self.account.voters(payload)
        mevote_dict = {}
        for delegate in res['delegates']:
            mevote_dict[delegate['publicKey']] = delegate['username']
        return mevote_dict

    def voteback_for_voteme(self):
        """
        找出给我投票了，但我没投，增加投票；
        """
        voteme_dict = self.get_vote_me()
        mevote_dict = self.get_me_vote()
        voteme_set = set(voteme_dict.keys())
        mevote_set = set(mevote_dict.keys())

        need_vote_add = voteme_set - mevote_set
        need_vote_pubkey_list = []
        need_vote_add_user_list = []

        for pub in need_vote_add:
            # 投票列表和用户名列表
            need_vote_pubkey_list.append('+' + pub)
            need_vote_add_user_list.append(voteme_dict[pub])
        return need_vote_pubkey_list

    def cancel_for_novoteme(self):
        """
        我投票了，但他没投我，取消投票；
        """
        voteme_dict = self.get_vote_me()
        mevote_dict = self.get_me_vote()
        voteme_set = set(voteme_dict.keys())
        mevote_set = set(mevote_dict.keys())

        need_vote_del = mevote_set - voteme_set
        need_vote_pubkey_list = []
        need_vote_del_user_list = []

        for pub in need_vote_del:
            # 取消投票列表和对应的用户列表
            need_vote_pubkey_list.append('-' + pub)
            need_vote_del_user_list.append(mevote_dict[pub])
        return need_vote_pubkey_list

    def vote_all(self, delegates_list):
        """
        投票：增加或者取消，根据传参（带+、-号）自动投票
        delegates_list:待投票列表
        """
        if len(delegates_list) > 0:
            if len(delegates_list) <= 33:
                if len(self.second_pwd) == 0:
                    payload = {'secret': self.pwd, 'delegates': delegates_list}
                else:
                    payload = {'secret': self.pwd, 'delegates': delegates_list, 'secondSecret': self.second_pwd}
            else:
                if len(self.second_pwd) == 0:
                    payload = {'secret': self.pwd, 'delegates': delegates_list[0:32]}
                else:
                    payload = {'secret': self.pwd, 'delegates': delegates_list[0:32], 'secondSecret': self.second_pwd}
            return self.account.vote(payload)
        else:
            return []

if __name__ == "__main__":
    pwd = raw_input("please input your asch's password:")
    second_pwd = raw_input("please input your asch's second password，if have not please enter directly:")
    vote = Vote(pwd, second_pwd)
    while True:
        # print 'get_vote_me', vote.get_vote_me()
        # print 'get_me_vote', vote.get_me_vote()
        delegates = vote.voteback_for_voteme()
        # print 'voteback_for_voteme', delegates
        print 'vote_add', vote.vote_all(delegates)
        delegates = vote.cancel_for_novoteme()
        print 'vote_cancel', vote.vote_all(delegates)
        time.sleep(100)

