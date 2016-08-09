#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Time-stamp: <2014-09-21 22:33:08 Sunday by work>

# @version 1.0
# @author liuzhendong01  liuzhendong01@baidu.com  

import json
import urllib2
import sys
import threading
import loc_formater

def mine_data():
    line = u"北京国贸"
    try:
        print loc_formater.geoencoder
        data = loc_formater.mine(line)
        print  data.encode("utf-8")
    except:
        info = sys.exc_info()
        print >>sys.stderr,info[0],":",info[1]

def start(num):
    threads = []
    for i in range(num):
        threads.append(threading.Thread(target=mine_data))
    for t in threads:
        t.start()
    for t in threads:
        t.join()


read_lock = threading.Lock()
start(1)

