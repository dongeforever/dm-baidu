#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Time-stamp: <2014-11-14 22:33:08 Friday by work>

# @version 1.0
# @author liuzhendong01  liuzhendong01@baidu.com  

import field_label_base
import re

class LocFieldLabel(field_label_base.FieldLabelBase):
    def is_loc_attr(self, key, value):
        if len(key) > 30 or len(value) > 50:
            return False
        re_rule_loc_key = r'(.*?)(地(.{0,5})(点|址|区)|场(.{0,5})(地|馆))(.*?)'
        key = key.encode('utf-8')
        value = value.encode('utf-8')
        if re.search(re_rule_loc_key, key):
            return True
        else:
            return False

    def label(self,fields,block_json,page_json={}):
        loc_index = []
        for i in range(len(fields)):
            field = fields[i]
            if not "key" in field or not "value" in field:
                continue
            if self.is_loc_attr(field["key"], field["value"]):
                loc_index.append(i)
        return loc_index 
    
if __name__ == "__main__":
    test = LocFieldLabel()
    test.label([],{},{})


