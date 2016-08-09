#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Time-stamp: <2014-11-14 22:33:08 Friday by work>

# @version 1.0
# @author liuzhendong01  liuzhendong01@baidu.com  

from field_label import loc_field_label
from field_label import time_field_label
from field_label import title_field_label
from FrameLog import *
import Tools
import json
import global_conf 

class FieldLabelModule:
    def __init__(self):
        self.field_labels = {}
        self.field_labels["title"] = title_field_label.TitleFieldLabel()
        self.field_labels["date"] = time_field_label.TimeFieldLabel()
        self.field_labels["loc"] = loc_field_label.LocFieldLabel()
        '''标志位,title 0, date 1, loc 2, 计算时先左移位，类似于PA中的merge flag'''
        self.field_rank = {}
        self.field_rank["title"] =  0
        self.field_rank["date"] =  1
        self.field_rank["loc"] =  2
        '''各字段的优先级顺序'''
        self.field_prior = []
        self.field_prior.append("title")
        self.field_prior.append("date")
        self.field_prior.append("loc")
        self.debug  = global_conf.get_conf("DEBUG_MODE","0")

    def check_field_relation(self, block_json, page_json):
        valid_field_indexs = []
        valid_fields = []
        status = 0
        last_index = 0
        for i in range(len(block_json["fields"])):
            field = block_json["fields"][i]
            if "attr_type" in field and field["attr_type"] in self.field_labels:
                status = status | 1 << self.field_rank[field["attr_type"]]
                valid_field_indexs.append(i)
                valid_field.append(field)
                last_index = i
                continue
            if "key" in field and field["key"] != "normal_text":
                last_index = i
                continue
            if i - last_index <= 2 and i != len(block_json["fields"]) - 1:
                continue
            if status != 7:
                valid_field_indexs = []
                valid_fields = []
            else:
                break

    def label_field(self, block_json, page_json):
        for field in block_json["fields"]:
            field["attr_status"] = 0
        for (k, v) in self.field_labels.items():
            indexs = v.label(block_json["fields"], block_json, page_json)
            for index in indexs:
                if index < 0 or index >= len(block_json["fields"]):
                    continue
                field = block_json["fields"][index]
                field["attr_status"] = field["attr_status"] | 1 << self.field_rank[k]
        #print "label_status", json.dumps(block_json, ensure_ascii = False).encode("utf-8")
        '''如果该字段被多重标记，这里来根据优先级进行判断'''
        all_status = 0
        for field in block_json["fields"]:
            status = field["attr_status"]
            for prior_attr in self.field_prior:
                prior_status =  1 << self.field_rank[prior_attr]
                if status & prior_status == prior_status:
                    field["attr_type"] = prior_attr
                    break
            if "attr_type" in field and field["attr_type"] in self.field_rank:
                all_status = all_status | 1 << self.field_rank[field["attr_type"]]
        #print "label_type", json.dumps(block_json, ensure_ascii = False).encode("utf-8")
        '''校验字段间的关系'''
        if all_status == 7 : 
                status_list = [] ;
                for field in block_json["fields"] :
                    if "attr_type" in field:
                        #status_list.append(field["attr_type"]) 
                        status_list.append(field["value"]) 
                    else:
                        status_list.append("0");
                
                     
                if self.debug == "1":
                    Tools.printObjEx ( status_list,"zhangxian" ) 
        return all_status

    def process(self, input_json):
        event_blocks = []
        for block in input_json["event_blocks"]:
            if not "fields" in block or len(block["fields"]) == 0:
                continue
            status = self.label_field(block, input_json)
            if status == 7:
                event_blocks.append(block)
            else:
                LOG_TRACE("Field Label Status:\t%d\t%s\n", status, input_json["url"])
        if len(event_blocks) == 0:
            input_json["event_blocks"] = []
            return -1
        else:
            input_json["event_blocks"] = event_blocks
            input_json["field_label_num"] = len(input_json["event_blocks"])
            return 0


if __name__ == "__main__":
    field_label_module = FieldLabelModule()
    field_label_module.process({})


