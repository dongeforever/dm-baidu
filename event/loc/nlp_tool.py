#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Time-stamp: <2014-09-19 16:31:00 Friday by work>

# @version 1.0
# @author zhangguhua
import urllib
import urllib2
import commands
import os
import json
import string


post_addres = "http://nlpc.baidu.com:8080/wordseg3_0_16/"
get_addres = "http://nlpc.baidu.com/?method=wordseg&encoding=utf8&query="

def word_seg_post(data):
    result = {}
    cmd = "wget --post-data '{" + '"query":"'+ self.data.encode("utf-8")+'", "scw_out_flag":0, "langid":0, "lang_para":0}' + "' http://nlpc.baidu.com:8080/wordseg3_0_16/utf8 -q -O -"
    output = os.popen(cmd)
    content = output.read()
    if not 'SegmentResult' in content:
        return {}
    info_dict = json.loads(content)
    segment = []
    if 'SegmentResult' in info_dict:
        for i in range(0, len(info_dict['SegmentResult'])):
            if info_dict['SegmentResult'][i] and 'buffer' in info_dict['SegmentResult'][i]:
                segment.append(info_dict['SegmentResult'][i]['buffer'])
                #print info_dict['SegmentResult'][i]['buffer'].encode('utf-8')
    basic = []
    if 'BasicWordResult' in info_dict:
        for i in range(0, len(info_dict['BasicWordResult'])):
            if info_dict['BasicWordResult'][i] and 'buffer' in info_dict['BasicWordResult'][i]:
                basic.append(info_dict['BasicWordResult'][i]['buffer'])
                #print info_dict['SegmentResult'][i]['buffer'].encode('utf-8')
    result["segment"] = segment
    result["basic"] = basic
    return result

def get_page(url):
    req = urllib2.Request(url)
    sock = urllib2.urlopen(req, timeout=3000)
    value = ""
    if sock.getcode() != 200:                                                                                     
        print >>sys.stderr,"error code:",page_content.getcode(),url
    else:
        value = sock.read()
    sock.close()
    return value
def word_seg_get(data):
    output = get_page(get_addres + urllib2.quote(data.encode("utf-8")))
    if not 'SegmentResult' in output:
        return {}
    result = {}
    output = output.decode("gbk").encode("utf-8")
    #print output
    output = output.translate(string.maketrans('\n',' '))
    info_dict = json.loads(output)
    segment = []
    if 'SegmentResult' in info_dict:
        for i in range(0, len(info_dict['SegmentResult'])):
            if info_dict['SegmentResult'][i] and 'buffer' in info_dict['SegmentResult'][i]:
                segment.append(info_dict['SegmentResult'][i]['buffer'])
                #print info_dict['SegmentResult'][i]['buffer'].encode('utf-8')
    basic = []
    if 'BasicWordResult' in info_dict:
        for i in range(0, len(info_dict['BasicWordResult'])):
            if info_dict['BasicWordResult'][i] and 'buffer' in info_dict['BasicWordResult'][i]:
                basic.append(info_dict['BasicWordResult'][i]['buffer'])
                #print info_dict['SegmentResult'][i]['buffer'].encode('utf-8')
    result["segment"] = segment
    result["basic"] = basic
    return result


if __name__ == "__main__":
    #sample = word_seg("交通事故,劳动纠纷,工伤赔偿,人身损害,房产纠纷,不当竞争,刑事辩护,行政复议,破产解散,常年顾问")
    sample = word_seg_get(u"详见内页")
    print json.dumps(sample,ensure_ascii=False).encode("utf-8")

