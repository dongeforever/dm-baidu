#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Time-stamp: <2014-09-21 22:33:08 Sunday by work>

# @version 1.0
# @author liuzhendong01  liuzhendong01@baidu.com  

import json
import urllib2

def mining(page_data):
    if len(page_data) == 0:
        return ""
    page_json = json.loads("".join(page_data.split('\n')))
    #print page_json
    blocks = page_json["blocks"]
    if len(blocks) == 0:
        print >>sys.stderr,"blocks is zero:",url
        return ""
    nav_data = []
    for block in blocks:
        if block["type"] != "NAV":
            continue
        nav_items = block["data_value"]["items"]
        if len(nav_items) == 0:
            continue
        for nav_item in nav_items:
            text = nav_item["text"]
            if len(text) > 0:
                filter = "首页".decode("utf-8")
                if not filter in text:
                    nav_data.append(text.encode("utf-8"))
    if len(nav_data) == 0:
        print >>sys.stderr,"nav_data_items is zero:",url 
        return ""
    nav_str = ""
    #print nav_data
    for i in range(0,len(nav_data)-1):
        if i == 0:
            nav_str = nav_str + nav_data[i]
        else:
            nav_str = nav_str + '$$'+ nav_data[i]
    #print nav_str
    return  nav_str

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

#test_url()
