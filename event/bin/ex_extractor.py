#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time-stamp: <2014-11-14 22:33:08 Friday by work>
# @version 1.0
# @author liuzhendong01  liuzhendong01@baidu.com  
import os 
import sys
curr_dir = os.path.split(os.path.realpath(__file__))[0]
sys.path.append(curr_dir + "/../lib")

import json
from optparse import OptionParser
import traceback

import global_obj
import global_conf
import pajson_analyze_module
import block_label_module
import field_label_module
import attr_extract_module

import event_page_identify

from FrameLog import *  
import data_manager
import Tools

class ExExtractor:
    def __init__(self):
        self.__block_label_module = block_label_module.BlockLabelModule()
        self.__field_label_module = field_label_module.FieldLabelModule()
        self.__attr_extract_module = attr_extract_module.EventAttrExtractModule()
        self.__page_identify = event_page_identify.EventPageIdentify()
        self.__data_manager = data_manager.DataWrap()
        self.__err_info = {
                "0" : u"抽取成功", 
                "-1" : u"活动页校验失败", 
                "-2" : u"块初筛后无有效块",
                "-3" : u"字段标记失败",
                "-4" : u"属性类型化失败",
                "-400" : u"运行出错",
                }

    def process(self, origin_data, url):
        print "start============================="
        try:
            '''解析PA的数据，如果解析有问题，就起exception'''
            page_json = pajson_analyze_module.process(origin_data, url)
            #print "AfterAnalyze:",json.dumps(page_json,ensure_ascii=False).encode("utf-8")
            '''数据语义处理'''
            res = self.process_data(url, page_json)
            '''数据输出管理'''
            self.__data_manager.log_out(page_json)
        except:
            res = -400
            print traceback.print_exc(), url
            LOG_WARNING("ERROR Encountered:%s\n", url)
        finally:
            host = ''
            pattern = ''

            if "host" in page_json :
                host = page_json["host"].encode("utf-8")

            if "pattern" in page_json:
                pattern = page_json["pattern"].encode("utf-8")

            format_str = "PROCESS_STATUS\t%d\tinfo\t%s\turl\t%s\thost\t%s\tpattern\t%s"

            print format_str % (res, self.__err_info[str(res)].encode("utf-8"),url,host,pattern) 
            LOG_NOTICE(format_str + "\n", res,self.__err_info[str(res)].encode("utf-8"),url,host,pattern )

    def process_data(self, url, page_json):

        '''整页判断，判断一个页面是否是活动页'''
        if global_conf.get_conf("ENABLE_KEYWORDS_CHECK", "0") == "1" and \
                not self.__page_identify.identify_page(page_json):
            return -1
        '''活动块判断，初步判断一个块是否是活动块'''
        if self.__block_label_module.process(page_json):
            LOG_TRACE("Block Label Module Process Fail:%s\n", url)
            return -2

        '''活动字段标记'''
        if self.__field_label_module.process(page_json):
            LOG_TRACE("Field Label Module Process Fail:%s\n", url)
            return -3

        '''属性类型化'''
        if self.__attr_extract_module.process(page_json):
            LOG_TRACE("Attr Extract Module process Fail:%s\n", url)
            return -4
        return 0
    

if __name__ == "__main__":
    ex_extractor = ExExtractor()
    while True:
        try:
            line = sys.stdin.readline()
            if not line:
                break
            line = line.strip()
            if len(line) == 0 :
                print "ERROR Invalid Empty  Input " 
                continue
            items = line.split("\t")
            if len(items) !=2 :
                print "ERROR Invalid Format Input " 
                continue
            url = items[0]
            page_data = items[1]
            ex_extractor.process(page_data, url)
        except:
            print "ERROR" +  "\t" + url
            LOG_FATAL("EX_TRACTOR_ERROR:%s\n", url)
            print >>sys.stderr,traceback.print_exc(), url



