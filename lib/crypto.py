#! /bin/env python
# coding=utf-8


from Crypto.Hash import SHA256
from ed25519 import _ed25519 as raw
from binascii import hexlify, unhexlify


class AschCrypto:
    def __init__(self, data):
        self.data = data
        self.seed = self.encrypto()

    def encrypto(self):
        hh = SHA256.new()
        hh.update(self.data)
        res = hh.digest()
        return res

    def keypair(self):
        raw_pub = raw.publickey(self.seed)
        # raw_pri = raw.
        pub = hexlify(raw_pub[0])
        keypair = {"privatekey": self.data, "publickey": pub}
        return keypair

    def getid(self):
        print self.seed[0:8]
        temp = self.seed[0:8][::-1]
        print temp, type(temp), hexlify(temp)
        # return int(temp)
        # 得到的结果和nodejs不一致
        return int(hexlify(temp), 16)


if __name__ == "__main__":
    pri = "lounge barrel episode lock bounce power club boring slush disorder cluster client"
    AC = AschCrypto(pri)
    print AC.keypair()
    addr = AC.getid()
    print addr



