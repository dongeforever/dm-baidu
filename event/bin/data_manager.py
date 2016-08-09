#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Time-stamp: <2014-11-14 22:33:08 Friday by work>

# @version 1.0
# @author liuzhendong01  liuzhendong01@baidu.com  
from FrameLog import *
import json

'''外挂抽取器对外输出的管理类'''
class DataWrap:
    def log_out(self, res_json):
        '''keywords_check 为 1 表示整页判断为活动块, 0 表示判断失败，-1表示没有走该过程'''
        keywords_check = -1
        '''block_label_num 表示走过块标记模块后剩余的块个数，目前就是PA中标记为ACTIVITY的个数'''
        block_label_num = 0
        '''field_label_num 表示字段标记过后剩余的块个数，所有字段均有的块才算'''
        field_label_num = 0
        '''attr_extract_num 表示类型化抽取之后剩余的块个数，所有属性类型都有的块才算'''
        attr_extract_num = 0
        if "keywords_check" in res_json:
            keywords_check = res_json["keywords_check"]
        if "block_label_num" in res_json:
            block_label_num = res_json["block_label_num"]
        if "field_label_num" in res_json:
            field_label_num = res_json["field_label_num"]
        if "attr_extract_num" in res_json:
            attr_extract_num = res_json["attr_extract_num"]
        url = res_json["url"]
        format_count_str = "COUNT\tkeywords_check:%d block_label_num:%d field_label_num:%d attr_extract_num:%d url:%s"
        print format_count_str % (keywords_check, block_label_num, field_label_num, attr_extract_num, url)
        LOG_NOTICE(format_count_str + "\n", keywords_check, block_label_num, field_label_num, attr_extract_num, url)
        prefix = "NO"
        if field_label_num > 0:
            prefix = "YES"
        res_str =  json.dumps(res_json, ensure_ascii=False)
        LOG_DEBUG("res:\t%s\t%s\t%s\n", prefix, res_json["url"], res_str)
        #打平输出
        self.log_plain_output(res_json)

    def log_plain_output(self, res_json):
        '''打平输出给PM看的格式'''
        if not "event_blocks" in res_json:
            return
        url = res_json["url"]
        host = res_json["host"]
        pattern = res_json["pattern"]
        for block in res_json["event_blocks"]:
            if not "extract_status" in block or block["extract_status"] != 7:
                continue
            if not "attrs" in block or len(block["attrs"]) == 0:
                continue
            status = block["extract_status"]
            o_title = ''
            o_date = ''
            o_loc = ''
            title = ''
            date = ''
            loc = ''
            loc_level = ''
            date_ori = ''
            attrs = block['attrs']
            for attr in attrs:
                if attr.has_key('type') == False:
                    continue
                if attr['type'] == 'title':
                    if attr.has_key('origin_value'):
                        if len(title) == 0:
                            title = attr['origin_value']
                        else:
                            title = title + '$' + attr['origin_value']
                elif attr['type'] == 'date':
                    if attr.has_key('origin_value'):
                        date_ori = attr['origin_value']
                    if attr.has_key('format_value') and attr['format_value'].has_key('str'):
                        date = attr['format_value']['str']
                elif attr['type'] == 'loc':
                    if attr.has_key('status') == False:
                        continue
                    if attr['status'] == 0:
                        if "only_city" in attr and attr["only_city"] == 1:
                            loc = attr["city"]
                        else:
                            loc = attr['format_value']['result']['formatted_address']
                            loc = loc + '$' + attr['format_value']['poi_name']
                            loc_level = attr['format_value']['level']
                    elif attr['status'] == -1:
                        if attr.has_key('error_info'):
                            loc = attr['error_info']
            for field in block['fields']:
                if field.has_key('attr_type') and field.has_key('value'):
                    if field['attr_type'] == 'title':
                        if len(o_title) == 0:
                            o_title = field['value']
                        else:
                            o_title = o_title + '$' + field['value']
                    elif field['attr_type'] == 'date':
                        if o_date == '':
                            o_date = field['value']
                        else:
                            o_date = o_date+'$'+ field['value']
                    elif field['attr_type'] == 'loc':
                        if o_loc == '':
                            o_loc = field['value']
                        else:
                            o_loc = o_loc + '$' + field['value']
            if len(o_title) == 0:
                o_title = 'NONE'
            if len(o_date) == 0:
                o_date = 'NONE'
            if len(o_loc) == 0:
                o_loc = 'NONE'
            if len(title) == 0:
                title = 'NONE'
            if len(date) == 0:
                date = 'NONE'
            if len(loc) == 0:
                loc = 'NONE'
            if len(loc_level) == 0:
                loc_level = 'NONE'
            if len(date_ori) == 0:
                date_ori = 'NONE'
            try:
                out_data = host +'\t'+pattern+'\t'+url+'\t'+str(status)+'\t'+o_title+'\t'+o_date+'\t'+o_loc
                out_data = out_data + '\t'+title+'\t'+date_ori+'\t'+date+'\t'+loc+'\t'+loc_level
                out_data = out_data.replace('\n', ' ') 
                print "EVENT_OUTPUT:\t%s" % out_data.encode("utf-8")
                LOG_NOTICE("EVENT_OUTPUT:\t%s\n", out_data)
            except:
                print "EVENT_OUTPUT_ERROR:\t%s" % url
                LOG_WARING("EVENT_OUTPUT_ERROR:\t%s\n", url)
                traceback.print_exc()
  


