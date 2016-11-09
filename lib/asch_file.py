#!/usr/bin/env python
# -*- coding:utf8 -*-
import time


class AschFile:
    def __init__(self, logfile):
        # self.loglevel = loglevel
        # self.text = text
        self.logfile = logfile

    def to_log_time(self, loglevel, text):
        now = time.strftime("%Y-%m-%d %H:%M:%S")
        tt = "[" + loglevel + "]\t" + str(now) + "\t" + str(text) + "\n"
        f = open(self.logfile, 'a+')
        f.write(tt)
        f.close()

    def to_log(self, text):
        tt = str(text) + "\n"
        f = open(self.logfile, 'a+')
        f.write(tt)
        f.close()