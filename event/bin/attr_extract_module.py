#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Time-stamp: <2014-11-14 22:33:08 Friday by work>

# @version 1.0
# @author liuzhendong01  liuzhendong01@baidu.com  

from attr_extract import loc_attr_extract
from attr_extract import origin_attr_extract
from attr_extract import time_attr_extract
import sys
import json
from FrameLog import *

class AttrExtractModule:
    def process(self,input_json):
        print "AttrExtractModule process"

class EventAttrExtractModule(AttrExtractModule):
    def __init__(self):
        self.attr_extracts = {}
        self.attr_list = []
        self.attr_extracts["loc"] = loc_attr_extract.LocAttrExtract()
        self.attr_list.append("loc")
        self.attr_extracts["title"] = origin_attr_extract.OriginAttrExtract()
        self.attr_list.append("title")
        self.attr_extracts["date"] = time_attr_extract.TimeAttrExtract()
        self.attr_list.append("date")
        self.sign_map = {}
        self.sign_map["title"] = 0
        self.sign_map["date"] = 1
        self.sign_map["loc"] = 2

    def process(self,input_json):
        event_succ_num = 0
        for block in input_json["event_blocks"]:
            attrs = {}
            for attr in self.attr_list:
                attrs[attr] = []
            for field in block["fields"]:
                if "attr_type" in field and field["attr_type"] in self.attr_list:
                    attrs[field["attr_type"]].append(field)
            #print "attr_extract_before", json.dumps(attrs,ensure_ascii=False).encode("utf-8")
            extract_status = 0
            for (k,v) in attrs.items():
                if len(v) == 0:
                    continue
                res = self.attr_extracts[k].extract(v,block,input_json)
                if "status" in res and res["status"] == 0:
                    res["type"] = k
                    block["attrs"].append(res)
                    extract_status = extract_status | (1 << self.sign_map[k])
            block["extract_status"] = extract_status 
            LOG_TRACE("ATTR_EXTRACT_STATUS:\t%d\t%s\n", block["extract_status"], input_json["url"])
            if extract_status == 7:
                event_succ_num = event_succ_num + 1
        if "blocks" in input_json:
            input_json["blocks"] = []
        if event_succ_num == 0:
            return -1
        else:
            input_json["attr_extract_num"] = event_succ_num
            return 0

if __name__ == "__main__":
    attr_extract_module = EventAttrExtractModule()
    attr_extract_module.process({})


