#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Time-stamp: <2014-09-21 22:33:08 Sunday by work>

# @version 1.0
# @author liuzhendong01  liuzhendong01@baidu.com  

import json
import urllib2
import sys
import threading

def mine(page_data):
    if len(page_data) == 0:
        return ""
    page_json = json.loads(page_data)
    #print page_json
    loc_num = 0
    loc_data = ""
    for item in page_json["blocks"]:
        if item["label_type"] == "53":
            loc_num = loc_num + 1
            for item_2 in item["data_value"]["items"]:
                for item_3 in  item_2["data_value"]["items"]:
                    loc_data = loc_data + "\t" + item_3["data_value"]["text"].encode("utf-8")
                    #loc_data = loc_data + "\t" + json.dumps(item_3, ensure_ascii=False).encode("utf-8") 
    if loc_num != 1:
        raise ValueError("no expected loc num!")
    return  loc_data

def test_url():
    url = "http://m.baidu.com/l=3/tc?srd=1&dict=21&tc_source=1&src=http://89wx.com"
    url = "http://m.baidu.com/l=3/tc?srd=1&dict=21&tc_source=1&src=http://www.shenmaxiaoshuo.com/"
    req = urllib2.Request(url)
    sock = urllib2.urlopen(req, timeout=3000)
    if sock.getcode() != 200:                                                                                     
        print >>sys.stderr,"error code:",page_content.getcode(),url
    else:
        value = sock.read()
        print mining(value)
    sock.close()

def mine_data():
    while True:
        read_lock.acquire()
        line = sys.stdin.readline()
        read_lock.release()
        line = line.strip()
        if len(line) == 0:
            break
        items = line.split("\t")
        if len(items) < 2:
            continue
        url = items[0]
        try:
            data = mine(items[1])
            print url + data
        except:
            info = sys.exc_info()
            print >>sys.stderr,info[0],":",info[1],line

def start(num):
    threads = []
    for i in range(num):
        threads.append(threading.Thread(target=mine_data))
    for t in threads:
        t.start()
    for t in threads:
        t.join()

#test_url()
read_lock = threading.Lock()
mine_data()
#start(10)
