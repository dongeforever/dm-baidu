#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Time-stamp: <2014-11-14 22:33:08 Friday by work>

# @version 1.0
# @author liuzhendong01  liuzhendong01@baidu.com  

import sys
import attr_extract_base
from lib import loc_formater
import json
import address
import global_conf

class LocAttrExtract(attr_extract_base.AttrExtractBase):
    address = address.Addr()
    def __init__(self):
        #self.address = address.Addr()
        pass
    def get_block_text(self,block_json):
        block_text = ""
        if not "fields" in block_json or len(block_json["fields"]) == 0:
            return block_text
        for field in block_json["fields"]:
            if not "key" in field or field["key"] != "title":
                continue
            if "key" in field:
                block_text = block_text + " " + field["key"]
            if "value" in field:
                block_text = block_text + " " + field["value"]
        return block_text
    def extract(self,fields,block_json,page_json):
        if len(fields) == 0 or len(block_json) == 0:
            return {}
        res = {"status":-1}
        block_text = self.get_block_text(block_json) 
        origin_text = self.get_field_value_text(fields) 
        res["origin_value"] = origin_text
        error_info = ""
        city = self.address.parse_city_by_service(origin_text)
        if len(city[0]) == 0:
            error_info = error_info + city[1]
            city = self.address.parse_city_by_service(block_text)
        if len(city[0]) == 0:
            error_info = error_info + " " + city[1]
            res["error_info"] = error_info 
            return res
        res["city"] = city[0]
        if global_conf.get_conf("ENABLE_POI_PARSE", "0") == "1": 
            format_res = loc_formater.mine(origin_text,city[0])
            if len(format_res) > 0:
                res["status"] = 0
                res["format_value"] = format_res
            return res
        else:
            res["status"] = 0
            res["only_city"] = 1
            return res

if __name__ == "__main__":
    loc_extract = LocAttrExtract()
    loc_extract.load({})
    loc_extract.extract([],{})


