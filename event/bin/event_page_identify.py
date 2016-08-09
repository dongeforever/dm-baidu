#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Time-stamp: <2014-11-14 22:33:08 Friday by work>

# @version 1.0
# @author liuzhendong01  liuzhendong01@baidu.com  

import json
import os
import wordseg 

from FrameLog import * 
from Tools import *

import global_conf



class EventPageIdentify:

    def __init__(self):
        self.__word_lists = []
        self.__signs = []
        self.load()
        
    def load(self):
        curr_dir = os.path.split(os.path.realpath(__file__))[0]
        white_words = self.load_list(curr_dir+"/../conf/event_white_words.conf")
        self.__word_lists.append(white_words)
        self.__signs.append(True)
        black_words = self.load_list(curr_dir+"/../conf/event_black_words.conf")
        self.__word_lists.append(black_words)
        self.__signs.append(False)
    def load_list(self,file_name):
        words = []
        f_input = open(file_name)
        while True:
            line = f_input.readline()
            line = line.strip()
            if len(line) == 0:
                break
            if "START" in line:
                continue
            line = line.decode("utf-8")
            LOG_TRACE("load %s %s" % (file_name,line));
            words.append(line)
        return words
    def check(self):
        data = {}
        data["list"] = self.__word_lists
        data["restrict"] = self.__signs
        #print json.dumps(data,ensure_ascii=False).encode("utf-8")

    def matchList(self,list):
        for item in list :
            if self.match(item ):
                return True
        return False

    def match(self,str):
        if len(str) == 0:
            return False
        res = []
    
        i = 0  
        for list in self.__word_lists:
            in_list = False
            for word in list:
                LOG_TRACE( "PreMatch %s %s %s" , self._url.encode("utf-8"),word.encode("utf-8"),self.__signs[i] );
                LOG_TRACE( "PreMatch str %s" ,  json.dumps(str,ensure_ascii=False).encode("utf-8") );
                if word in str:
                    LOG_TRACE( "Match %s %s %s" , self._url.encode("utf-8"),word.encode("utf-8"),self.__signs[i] );
                    #printStr(word) 
                    #print self.__signs[i]
                    in_list = True
                    break
            res.append(in_list)
            i = i + 1
        #print "les(res),len(signs)",len(res),len(self.__signs)
        if len(res) != len(self.__signs):
            return False
        #print res,self.__signs
        for i in range(len(res)):
            if res[i] != self.__signs[i]:
                return False
        return True

    def getPageTitle(self,page_json):
        """获取页面page_title"""
        if "page_title" in page_json:
            str = page_json["page_title"]
            return str 
        return '' 

    def getPageDiscription(self,page_json):
        """获取meta信息"""
        description = "" 
        if "description"  in page_json : 
            description = page_json["description"]
            return description
        return '' 
    def getPageKeywords(self,page_json ) :
        '''获取meta keywords 内容'''
        if "keywords"  in page_json : 
            return page_json["keywords"]
        return ''
    
    def getPageKeys(self,page_json):
        """获取activity的KV块中所有的K"""
        list = [] 
        if "blocks" in page_json:
            for b in page_json["blocks"] :
                if "sem_block_label" in b and b["sem_block_label"]=="ACTIVITY":
                    if "fields"  in b :  
                        for f  in   b["fields"] : 
                            k  = f["key"]  
                            if k !='normal_text' and k !="title" and k!= "title_slave":
                                list.append(k)
        return list 

    def identify_page(self,page_json):
        """待扫描的文本集合"""
        key_list=[]        
        self._url =  page_json["url"]
        info_str = ''
        list = self.getPageKeys(page_json) 
        info_str = '%s\t%s$$'%(page_json["url"].encode("utf-8"), page_json["url"].encode("utf-8")) 
        """去除空格"""
        if list :
            for item in list: 
                item = item.replace(' ','')
                item = item.replace(u' ','')
                item = item.replace(u'　','')
                key_list.append(item)
                info_str = '%s%s$$'%(info_str, item.encode("utf-8"))
        """黑白名单匹配"""
        res = self.match(key_list) 
        info_str ='%s\ttarget\t%d' % (info_str,res)
        #print info_str
        LOG_TRACE(info_str)
        if res:
            page_json["keywords_check"] = 1
        return res

if __name__ == "__main__":
    test = EventPageIdentify()
    test.check()
    print test.matchList(u"活动行")
    if u"活动" in u"活动行":
        print "YES"
 

