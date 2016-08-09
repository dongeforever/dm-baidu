#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Time-stamp: <2014-11-14 22:33:08 Friday by work>

# @version 1.0
# @author liuzhendong01  liuzhendong01@baidu.com  

from block_label import event_block_label

class BlockLabelModule:
    def __init__(self):
        self.block_label = event_block_label.EventBlockLabel() 
    def process(self,input_json):
        event_blocks = []
        for block in input_json["blocks"]:
            if not "sem_block_label" in block or block["sem_block_label"] != "ACTIVITY":
                continue
            event_blocks.append(block)
        if len(event_blocks) == 0:
            return -2
        input_json["event_blocks"] = event_blocks
        input_json["block_label_num"] = len(input_json["event_blocks"])
        return 0


if __name__ == "__main__":
    block_label_module = BlockLabelModule()
    block_label_module.process({})


