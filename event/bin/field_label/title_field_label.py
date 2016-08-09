#encoding=utf-8
#/***************************************************************************
# * 
# * Copyright (c) 2014 Baidu.com, Inc. All Rights Reserved
# * 
# **************************************************************************/
# 
# 
# 
#/**
# * @file attribute_identify.py
# * @author wuhonghuan(com@baidu.com)
# * @date 2014/11/14 11:40:54
# * @brief 
# *  
# **/
import sys
import json
import re
import os
import fcntl
import threading
import field_label_base
from FrameLog import *

class TitleFieldLabel(field_label_base.FieldLabelBase):
    def __init__(self):
        self.file_log = open('log_title.txt', 'w+')
        self.title = 'NONE'
        self.url = 'NONE'

    def label(self, fields, block_json, page_json={}):
        '''识别块是不是活动块，并标记属性'''
        title_index = []
        title_pos = -1
        have_title = False
        self.get_page_data(page_json)
        for field in fields:
            title_pos = title_pos + 1
            if field.has_key('key') == False or field.has_key('value') == False:
                continue
            if have_title == False and self.is_title_attr(field['key'], field['value']):
                have_title = True
                field['attr_type'] = 'title'
                title_index.append(title_pos)
                return title_index
        return title_index
    
    def get_page_data(self, json_page):
        if type(json_page) != dict:
            return
        if json_page.has_key('page_title'):
            self.page_title = json_page['page_title']
            self.page_title = self.page_title.replace('\n', ' ')
        if json_page.has_key('url'):
            self.url = json_page['url']
    
    def title_file_log(self, have_title, status, len_lcs, page_url, page_title, value):
        fcntl.flock(self.file_log.fileno(), fcntl.LOCK_EX)
        out_file_data = have_title+'\t'+str(status)+'\t'+str(len_lcs)+'\t'+page_url.encode('utf-8')+'\t'+page_title.encode('utf-8')+'\t'+value.encode('utf-8')+'\n'
        self.file_log.write(out_file_data)
        fcntl.flock(self.file_log.fileno(), fcntl.LOCK_UN)
    
    def head_sub_title(self, head, title):
        '''title是不是head的头子集'''
        title = title.strip()
        head = head.strip()
        tlen = len(title)
        hlen = len(head)
        if hlen < tlen:
            return False
        for i in range(tlen):
            if head[i] != title[i]:
                return False
        return True
    def is_sub_set(self, page_title, title):
        if page_title.find(title) != -1:
            return True
        page_title = page_title.replace(' ','')
        page_title = page_title.replace('&lt;','')
        page_title = page_title.replace('&gt;','')
        page_title = page_title.replace('<','')
        page_title = page_title.replace('>','')
        title = title.replace(' ','')
        title = title.replace('&lt;','')
        title = title.replace('&gt;','')
        title = title.replace('<','')
        title = title.replace('>','')
        if page_title.find(title) != -1:
            return True
        return False
    
    def is_title_attr(self, key, value):
        page_title = self.page_title
        page_url = self.url
        ans = False
        if len(page_title) > 0:
            len_lcs = self.LCS(page_title, value)
            value = value.replace('\n',' ')
            if  len(value) > 105 or len(value) < 2:
                self.title_file_log('no_title', 1, len_lcs, page_url, page_title, value)
                return ans
            if value[0] == u'#' and value[len(value)-1] == u'#':
                self.title_file_log('no_title', 1, len_lcs, page_url, page_title, value)
                return ans
            if self.is_sub_set(page_title, value) == True:
#            if page_title.find(value) != -1:
                if len_lcs < 4:
                    self.title_file_log('no_title', 21, len_lcs, page_url, page_title, value)
                    return ans
                elif len_lcs < 9:
                    if self.head_sub_title(page_title, value):
                        self.title_file_log('yes_title', 22, len_lcs, page_url, page_title, value)
                        return True
                    else:
                        self.title_file_log('no_title', 23, len_lcs, page_url, page_title, value)
                        return ans
                self.title_file_log('yes_title', 2, len_lcs, page_url, page_title, value)
                return True
    
            if len_lcs > 16:
                self.title_file_log('yes_title', 3, len_lcs, page_url, page_title, value)
                return True
            self.title_file_log('no_title', 5, len_lcs, page_url, page_title, value)
        return ans
    
    def LCS(self, xxx, yyy):
        xxx = xxx.replace(u' ','')
        xxx = xxx.replace(u'】','')
        xxx = xxx.replace(u'）','')
        xxx = xxx.replace(u'【','')
        xxx = xxx.replace(u'（','')
        yyy = yyy.replace(u' ','')
        yyy = yyy.replace(u'】','')
        yyy = yyy.replace(u'）','')
        yyy = yyy.replace(u'【','')
        yyy = yyy.replace(u'（','')
        xlen = len(xxx)
        ylen = len(yyy)
        if xlen >ylen:
            dplen = xlen+1
        else:
            dplen = ylen+1
        dp = [0]*dplen
        for i in range(xlen):
            temp = 0
            for j in range(ylen):
                if xxx[i] == yyy[j]:
                    t2 = dp[j]
                    dp[j] = temp + 1
                    if t2 > temp:
                        temp = t2
                else:
                    if dp[j]>temp:
                        temp = dp[j]
        ans = 0
        for item in dp:
            if ans < item:
                ans = item
        return ans
    
    def is_date_attr(self, key, value):
        if len(key) > 100 or len(value) > 100:
            return False
        re_rule_date_key = r'(.*?)(日(.{0,5})期|时(.{0,5})间)(.*?)'
        re_rule_date_value = r'(.*?)(每天|星期|(年|月)(.{1,6})(年|月|日))(.*?)'
        key = key.encode('utf-8')
        value = value.encode('utf-8')
    #    value = r'2014年5月25日'
    #    print type(key)
    #    print re_rule_date_key,'---------------------',key
        if re.search(re_rule_date_key,key):
            return True
        elif re.search(re_rule_date_value, value):
            return True
        else:
            return False
    
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
    
if __name__ == "__main__":
    pass
    #titleidf = TitleIdf()
    #page_data = raw_input().split('\t')
    #page_data = json.loads(page_data[1].decode('utf-8'))
    #titleidf.identify_page(page_data)
#    identify_page(page_data)
#    str_data = json.dumps(page_data)
#    print str_data.encode('utf-8')
#    file_log.close()
    


#
#/* vim: set expandtab ts=4 sw=4 sts=4 tw=100: */
