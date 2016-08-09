#coding=utf-8
#/***************************************************************************
# * 
# * Copyright (c) 2014 Baidu.com, Inc. All Rights Reserved
# * 
# **************************************************************************/
# 
# 
# 
#/**
# * @file json_analyz.py
# * @author wuhonghuan(com@baidu.com)
# * @date 2014/11/12 16:18:34
# * @brief 
# *  
# **/
#
import sys
import json
import string
from FrameLog import *

def process(origin_data, url):
    origin_data = origin_data.translate(string.maketrans('\r\n','  '))
    #print origin_data
    json_data = json.loads(origin_data)
    format_json = format_json_data(json_data, url)
    #print json.dumps(format_json, ensure_ascii=False).encode('utf-8')
    return format_json
    
def format_json_data(json_data, url):
    '''先对关键字段进行校验'''
    if not "host" in json_data:
        LOG_DEBUG("NO HOST:%s\n", url)
        raise SyntaxError("NO HOST")
    if not "url" in json_data:
        LOG_DEBUG("NO URL:%s\n", url)
        raise SyntaxError("NO URL")
    if not "pattern" in json_data:
        LOG_DEBUG("NO PATTERN:%s\n", url)
        raise SyntaxError("NO PATTERN")
    if not "blocks" in json_data or len(json_data["blocks"]) == 0:
        LOG_DEBUG("NO BLOCKS:%s\n", url)
        raise SyntaxError("NO BLOCKS")
    json_data['blocks'] = format_blocks(json_data['blocks'])

    return json_data

def format_blocks(blocks):
    """将块格式化为活动语义的需求"""
#    new_blocks = []
    for block in blocks:
        #print block['type']
        if "attrs" in block:
            block["attrs"] = []
        if "fields" in block:
            continue
        if not block.has_key('data_value') or not block['data_value'].has_key('items'):
            continue
        items = block['data_value']['items']
        new_blocks = []
        for item in items:
            if  not item.has_key('data_value'):
                continue
            item_value = item['data_value']
            #title
            if item_value.has_key('resource_title'):
                for title_item in item_value['resource_title']:
                    if title_item.has_key('data_value') and title_item['data_value'].has_key('text'):
                        title_detail = {}
                        if "type" in title_item and title_item["type"] == "RESOURCE_TITLE_MAIN":
                            title_detail['key'] = 'title'
                        else:
                            title_detail['key'] = 'title_slave'
                        title_detail['value'] = title_item['data_value']['text']
                        if len(title_detail['value']) == 0:
                            continue
                        if title_item['data_value'].has_key('link'):
                            title_detail['href'] = title_item['data_value']['link']
                        #add title to new_blocks
                        new_blocks.append(title_detail)
            #content
            resource_normal = []
            if item_value.has_key('resource_normal'):
                resource_normal = item_value['resource_normal']
            for content_item in resource_normal:
                content_detail = {}
                type = content_item["type"]
                if type == "RESOURCE_KEY_VALUE":
                    #get key
                    if content_item.has_key('key'):
                        key_detail = ''
                        for key_item in content_item['key']:
                            if "text" in key_item:
                                key_detail = key_detail + " " + key_item['text']
                        content_detail['key'] = key_detail
                    #get value
                    if content_item.has_key('value'):
                        value_detail = ''
                        content_value = content_item['value']
                        for value_item in content_value:
                            if value_item.has_key('text'):
                                value_detail = value_detail + " " +value_item['text']
                        content_detail['value'] = value_detail
                elif "items" in content_item:
                    content_detail["key"] = "normal_text"
                    value = ""
                    for value_item in content_item["items"]:
                        if value_item.has_key('text'):
                            value = value + " " +value_item['text']
                    content_detail["value"] = value
                if len(content_detail) > 0:
                    new_blocks.append(content_detail)
        #change data_value
        block['data_value'] = {} 
        block['fields'] = new_blocks
        block['attrs'] = []

    return blocks


if __name__ == "__main__":
    data = raw_input()
    #print data
    process(data)


