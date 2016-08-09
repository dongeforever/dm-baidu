#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Time-stamp: <2014-09-21 22:33:08 Sunday by work>

# @version 1.0
# @author liuzhendong01  liuzhendong01@baidu.com  

import json
import urllib2
import get_nlp_result as nlp
import sys
import threading

def mining(page_data):
    if len(page_data) == 0:
        return ""
    page_json = json.loads("".join(page_data.split('\n')))
    #print page_json
    terms = {}
    if "page_title" in page_json:
        words = nlp.word_seg(page_json["page_title"].encode("utf-8")).post_data()
        terms["page_title"] = words
    page_str = ""
    if "blocks" in page_json:
        for i in range(len(page_json["blocks"])):
            if page_json["blocks"][i] and "type" in  page_json["blocks"][i] and "data_value" in page_json["blocks"][i]:
                page_str = page_str + page_json["blocks"][i]["data_value"]
                #name = page_json["blocks"][i]["type"] + "_" + ("%d" % i)
                #value = page_json["blocks"][i]["data_value"]
                #words = nlp.word_seg(value.encode("utf-8")).post_data()
                #terms[name] = words
    words = nlp.word_seg(page_str.encode("utf-8")).post_data()
    terms["blocks"] = words
    return terms

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
        items = line.split("$$")
        if len(items) < 2:
            continue
        str = items[0]
        try:
            terms = mining(items[1])
            if len(terms) == 0:
                print >>stderr,"error_no_terms:",items[0]
                continue
            for (k,v) in terms.items():
                for word in v:
                    word = word.replace(" ","")
                    if len(word) >= 2:
                        str = str + "$$" + word.encode("utf-8")
            read_lock.acquire()
            print str
            read_lock.release()
        except:
            str = ""

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
#mine_data()
start(10)
