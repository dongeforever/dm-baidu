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
post_addres = "http://nlpc.baidu.com:8080/wordseg3_0_16/"

class word_seg:
    def __init__(self, query):
        self.data = query
    def post_data(self):
        result = {}
        cmd = "wget --post-data '{" + '"query":"'+ self.data+'", "scw_out_flag":0, "langid":0, "lang_para":0}' + "' http://nlpc.baidu.com:8080/wordseg3_0_16/utf8 -q -O -"
        output = os.popen(cmd)
        content = output.read()
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
if __name__ == "__main__":
    sample = word_seg("交通事故,劳动纠纷,工伤赔偿,人身损害,房产纠纷,不当竞争,刑事辩护,行政复议,破产解散,常年顾问")
    print json.dumps(sample.post_data(),ensure_ascii=False).encode("utf-8")

