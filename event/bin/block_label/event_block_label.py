#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Time-stamp: <2014-11-14 22:33:08 Friday by work>

# @version 1.0
# @author liuzhendong01  liuzhendong01@baidu.com  

import block_label_base
import json
import os

class EventBlockLabel(block_label_base.BlockLabelBase):

    def label(self, blocks, page_json):
        print "EventBlockLabel process"
        return []

if __name__ == "__main__":
    test = EventBlockLabel()
    test.label([], {})


