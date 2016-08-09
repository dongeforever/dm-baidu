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
    page_title = page_json["page_title"]
    if len(page_title) == 0:
        print >>sys.stderr,"page_title is zero:",url
        return ""
    else:
        #return page_title
        return page_title.encode("utf-8")

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
