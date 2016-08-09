#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Time-stamp: <2014-11-14 22:33:08 Friday by work>

# @version 1.0
# @author liuzhendong01  liuzhendong01@baidu.com  

class AttrExtractBase:

    """
    抽取函数，所有子类应该重写此函数
    @fields[in]  表示所有被标记为对应属性的字段列表
    @block_json[in] 对应的块json对象，不能修改此对象
    @page_json[in]  对应的整页json对象，不能修改此对象
    @return {}  返回对应的属性json对象
    """
    def extract(self,fields,block_json,page_json={}):
        print "AttrExtractBase process"
        return {}
    """
    获取字段列表的value值，并连接起来
    @fields[in] 字段列表
    @return 字符串
    """
    def get_field_value_text(self,fields):
        text =  ""
        for field in fields:
            text = text + " " + field["value"]
        return text

if __name__ == "__main__":
    attr_extract_base = AttrExtractBase()
    attr_extract_base.extract([],{})


