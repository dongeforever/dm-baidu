#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Time-stamp: <2014-09-21 22:33:08 Sunday by work>

# @version 1.0
# @author liuzhendong01  liuzhendong01@baidu.com  

import json
import urllib2
import sys
import threading
import address
import loc_formater

def mine_data():
    global  addr
    while True:
        read_lock.acquire()
        line = sys.stdin.readline()
        read_lock.release()
        line = line.strip()
        if len(line) == 0:
            break
        line = line.decode("utf-8")
        items = line.split("\t")
        if len(items) < 4:
            continue
        url = items[0]
        name = items[1]
        loc = items[3]
        try:
            city = ""
            #print "LOC_start:",loc.encode("utf-8")
            res = addr.parse_address(loc)
            if len(res["city"]) == 0:
                res = addr.parse_address(name)
                if len(res["city"]) > 0:
                    city = res["city"].items()[0][0]
                    loc = city + " " + loc
                else:
                    print (url + '\t' + loc + '\t' + "NO_CITY\tNONE").encode("utf-8")
                    continue
            else:
                city = res["city"].items()[0][0]
            #print "LOC_end:",loc.encode("utf-8")
            fmt_res = loc_formater.mine(loc,city)
            fmt_address = ""
            if len(fmt_res) > 0:
                fmt_address = fmt_res["result"]["formatted_address"]
            else:
                formatted_address = "NO_CITY\tNONE"
            if "poi_name" in fmt_res:
                fmt_address = fmt_address + "\t" + fmt_res["poi_name"]
            #print formatted_address
            print (url + '\t' +  loc + '\t' + fmt_address).encode("utf-8") 
        except:
            info = sys.exc_info()
            print >>sys.stderr,info[0],":",info[1],url

def start(num):
    threads = []
    for i in range(num):
        threads.append(threading.Thread(target=mine_data))
    for t in threads:
        t.start()
    for t in threads:
        t.join()

read_lock = threading.Lock()
addr = address.Addr()
#mine_data()
start(10)
