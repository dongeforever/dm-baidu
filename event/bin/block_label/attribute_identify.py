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
#from FrameLog import *
path = os.path.dirname(os.path.abspath(__file__))
sys.path += [path + '/../lib/']
import nlp_tool
file_log = open('log_title.txt','w+')
#lock = threading.Lock()
def identify_block(json_block, other):
    '''识别块是不是活动块，并标记属性'''
    if type(json_block) != dict:
        return False
    if json_block.has_key('sem_block_label') == False or json_block['sem_block_label'] != 'ACTIVITY':
        return False
    num = 0
    if json_block.has_key('fields'):
        fields = json_block['fields']
        have_title = False
        for field in fields:
            if field.has_key('key') and field.has_key('value'):
#                if field['key'] == 'title':
#                    num = num | 1
                if have_title == False and is_title_attr(field['key'], field['value'], other):
                    have_title = True
                    #field['attr_type'] = 'title'
                    num = num | 1
                elif is_date_attr(field['key'], field['value']):
                    #field['attr_type'] = 'date'
                    num = num | 2
                elif is_loc_attr(field['key'], field['value']):
                    #field['attr_type'] = 'loc'
                    num = num | 4
                else:
                    field['attr_type'] = 'unknown'
        if num == 7:
            json_block['is_event'] = num
            return True
        else:
            json_block['is_event'] = num
            return False

def identify_page(json_page):
    other = {'title':'NONE', 'url':'NONE'}
    if type(json_page) != dict:
        return
    if json_page.has_key('page_title'):
        other['title'] = json_page['page_title']
        other['title'] = other['title'].replace('\n', ' ')
    if json_page.has_key('url'):
        other['url'] = json_page['url']
    if json_page.has_key('blocks'):
        blocks = json_page['blocks']
        for block in blocks:
            identify_block(block, other)

def title_file_log(have_title, status, len_lcs, page_url, page_title, value):
    fcntl.flock(file_log.fileno(), fcntl.LOCK_EX)
    out_file_data = have_title+'\t'+str(status)+'\t'+str(len_lcs)+'\t'+page_url.encode('utf-8')+'\t'+page_title.encode('utf-8')+'\t'+value.encode('utf-8')+'\n'
    file_log.write(out_file_data)
    fcntl.flock(file_log.fileno(), fcntl.LOCK_UN)

def head_sub_title(head, title):
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


def is_title_attr(key, value, other):
    page_title = other['title']
    page_url = other['url']
    ans = False
#    if key == 'title':
#        ans = True
    if len(page_title) > 0:
        len_lcs = LCS(page_title, value)
        value = value.replace('\n',' ')
        if len(value) > len(page_title) or len(value) > 55 or len(value) < 2:
            title_file_log('no_title', 1, len_lcs, page_url, page_title, value)
            return ans
        if value[0] == u'#' and value[len(value)-1] == u'#':
            title_file_log('no_title', 1, len_lcs, page_url, page_title, value)
            return ans
        if page_title.find(value) != -1:
            if len_lcs < 4:
                title_file_log('no_title', 21, len_lcs, page_url, page_title, value)
                return ans
            elif len_lcs < 9:
                if head_sub_title(page_title, value):
                    title_file_log('yes_title', 22, len_lcs, page_url, page_title, value)
                    return True
                else:
                    title_file_log('no_title', 23, len_lcs, page_url, page_title, value)
                    return ans
            title_file_log('yes_title', 2, len_lcs, page_url, page_title, value)
            return True

        if len_lcs > 16:
            title_file_log('yes_title', 3, len_lcs, page_url, page_title, value)
            return True
        title_file_log('no_title', 5, len_lcs, page_url, page_title, value)
    return ans

def LCS(xxx, yyy):
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

def is_date_attr(key, value):
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

def is_loc_attr(key, value):
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
    print LCS(u'五十里堡羽毛球活动（大众）[东兴军健羽毛球馆]六人行-结伴活动平台',u'[主题聚会]文艺青年正当时-深圳奥伦达部落读字聚落活动公告')
#    page_data = raw_input()
#    print page_data
#    page_data = json.loads(page_data.decode('utf-8'))
#    identify_page(page_data)
#    str_data = json.dumps(page_data)
#    print str_data.encode('utf-8')
#    file_log.close()



#
#/* vim: set expandtab ts=4 sw=4 sts=4 tw=100: */
