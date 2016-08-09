#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Time-stamp: <2014-11-14 22:33:08 Friday by work>

# @version 1.0
# @author liuzhendong01  liuzhendong01@baidu.com  

class FieldLabelBase:

    """
    字段识别的接口
    @fields 数组对象，待识别的字段列表
    @block_json 这些字段所处的块json
    @page_json 这些字段所处的页面json
    @return 数组对象，被标记的索引
    """
    def label(self,fields,block_json,page_json={}):
        return []
    
if __name__ == "__main__":
    test = FieldLabelBase()
    test.label([],{},{})


