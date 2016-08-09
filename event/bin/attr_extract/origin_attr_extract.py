#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Time-stamp: <2014-11-14 22:33:08 Friday by work>

# @version 1.0
# @author liuzhendong01  liuzhendong01@baidu.com  

import sys
import attr_extract_base
import json

class OriginAttrExtract(attr_extract_base.AttrExtractBase):
    def extract(self,fields,block_json,page_json):
        if len(fields) == 0 or len(block_json) == 0:
            return {}
        origin_text = self.get_field_value_text(fields) 
        res = {"status":0}
        res["origin_value"] = origin_text
        res["format_value"] = origin_text
        return res

if __name__ == "__main__":
    print "OriginAttrExtract"


