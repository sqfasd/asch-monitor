#!/usr/bin/env python
# -*- coding:utf8 -*-
from asch_file import AschFile


class MyPrint:
    def __init__(self, logfile):
        self.logfile = logfile

    def my_print_time(self, li, loglevel='info'):
        res = '\t'.join(li)
        print res
        aschfile = AschFile(self.logfile)
        aschfile.to_log(loglevel, res)

    def my_print(self, li):
        res = '\t'.join(li)
        print res
        aschfile = AschFile(self.logfile)
        aschfile.to_log(res)

if __name__ == "__main__":
    li = ['testxxxxx', 'asfa']
    logfile = 'test.log'
    mp = MyPrint(logfile)
    mp.my_print(li)
