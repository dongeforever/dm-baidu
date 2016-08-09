#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Time-stamp: <2014-11-14 22:33:08 Friday by work>

# @version 1.0
# @author liuzhendong01  liuzhendong01@baidu.com  

class BlockLabelBase:

    """
    @blocks[in] 待标记的块对象数组
    @page_json[in]  对应的整页json对象，不能修改此对象
    @return 数组，被标记的块的索引 
    """
    def label(self, blocks, page_json):
        print "BlockLabelBase process"
        return []

if __name__ == "__main__":
    block_label_base = BlockLabelBase()
    block_label_base.label([],{})


