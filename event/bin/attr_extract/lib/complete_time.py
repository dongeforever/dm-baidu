3#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''/***************************************************************************
 * 
 * Copyright (c) 2014 Baidu.com, Inc. All Rights Reserved
 * 
 **************************************************************************/
 
 
 
/**
 * @file complete_time.py
 * @author shaoyuanhua(com@baidu.com)
 * @date 2014/12/02 16:37:47
 * @brief 
 *  
 **/'''
import sys
import re
import string
import datetime
#from FrameLog import *

class Complete():
    def __init__(self):
        self.str1 = u'(?:(?P<YEAR>\d{2,4})[\u0020]?\u5E74[\u0020]?)(?:(?P<MON>\d{1,2})[\u0020]?\u6708[\u0020]?)?(?:(?P<DAY>\d{1,2})[\u0020]?[\u65E5\u53F7]?)?'
        #月日
        self.str5 = u'(?:(?P<MON>\d{1,2})[\u0020]?\u6708[\u0020]?)(?:(?P<DAY>\d{1,2})[\u0020]?[\u65E5\u53F7]?)'
        self.str2 = u'(?:(?P<YEAR>[0-2][0-9][0-9]{2})(?P<biaohao>[^\d\u4e00-\u9fa5\u003A\uFF1A]{1,3})(?P<MON>0?[1-9]|1[0-2])(?P=biaohao)(?P<DAY>(?:[1-2][0-9]|3[0-1]|0?[1-9])))'
        self.str3 = u'(?:(?P<YEAR>[0-2][0-9]{3})[^\d\u4e00-\u9fa5](?P<MON>0?[1-9]|1[0-2]))\D'
        self.str4 = u'(?<![a-zA-Z])(?P<YEAR>20[0,1,2][0-9])'
        self.p1 = re.compile(self.str1, re.I)
        self.p2 = re.compile(self.str2, re.I)
        self.p3 = re.compile(self.str3, re.I)
        self.p4 = re.compile(self.str4, re.I)
        self.p5 = re.compile(self.str5, re.I)

    def process(self, res, time_key, time_str, block_json, page_json):
        url = page_json.get('url', 'no_url')

        #待补充状态
        state = 'null'
        if res['year_s'] is 'XXXX' and res['year_e'] is 'XXXX':
            state = 'lack_year'
        else:
            return '','','',[] 
        if res['mon_s'] is 'XX' and res['mon_e'] is 'XX':
            state = 'lack_mon'

        #返回时保存信息
        mess = []
        mess.append(state)

        fields = block_json.get('fields', 'no')
        if fields is 'no':
            return 'error','no_str','no_fields','mess' 

        #从title中得到补全
        for i in fields:
            title = i.get('attr_type', 'no')
            if title is 'title':
                flag,year,v = self.get_year(i.get('value', 'no'), 1)
                title_str = ''
                if flag == 1:
                    title_str = year['year'] + year['mon'] + year['day']
                if self.check_time(title_str, res, state, url):
                    return 'ok',i.get('value', 'no'), 'is_title',mess

        #从page_title中得到调研
        page_title = page_json.get('page_title', 'no')
        flag,year,v = self.get_year(page_title, 1)
        title_str = ''
        if flag == 1:
            title_str = year['year'] + year['mon'] + year['day']
        if self.check_time(title_str, res, state, url):
            return 'ok',page_title, 'is_pagetitle',mess

        '''#调研准确性50%，先不用"
        description = page_json.get('description', 'no')
        flag,year,v = self.get_year(description, 0)
        title_str = ''
        if flag == 1:
            title_str = year['year'] + year['mon'] + year['day']
        if self.check_time(title_str, res, state, url):
            return description, 'is_description'
        '''
        block_before_num = 0
        block_after_num = 0
        page_before_num = 0
        page_after_num = 0
        block_before_str = '$'
        block_after_str = '$'
        page_before_str = '$'
        page_after_str = '$'
        
        #取得block_before,page_before时间str
        #取page_before_str:
        blocks = page_json.get('blocks', 'no')
        if blocks is 'no':
            blocks = []
        block_xpath = block_json.get('xpath', 'no')
        if block_xpath is 'no':
            blocks = []
        
        #def get_before_block(self, fields, time_str, time_key):
        #def get_before_page(self, blocks, block_xpath):
        block_before_str,block_before_num = self.get_before_block(fields, time_str, time_key)
        page_before_str, page_before_num = self.get_before_page(blocks, block_xpath)
        #block_before与page_before一起处理
        before_str = page_before_str + block_before_str
        before_num = page_before_num + block_before_num
        if state is 'lack_year':
            #去掉不带年的时间
            before_str, before_num = self.delete_mon(before_str)
        if before_num == 0:
            mess.append('no_time')
        else:
            c_is_same = self.is_same(before_str, state)
            if c_is_same == 0:
                #补充年或年月日，时间不同则不再进行
                mess.append('more_time' + before_str)
            else:
                #时间内容相同，则尝试进行补充
                if self.check_time(before_str, res, state, url):
                    return 'ok',before_str,'is_before',mess
                else:
                    mess.append('beforeerror:'+before_str)

        #如果是缺少年，则不进行after的处理
        if state is 'lack_mon':
            return 'error', '', '', mess
        #def get_before_block(self, fields, time_str, time_key):
        block_after_str, block_after_num = self.get_after_block(fields, time_str, time_key)
        block_after_str, block_after_num = self.delete_mon(block_after_str)
        if block_after_num == 0:
            mess.append('no_time')
        else:
            c_is_same = self.is_same(block_after_str, state)
            if c_is_same == 0:
                #补充年或年月日，时间不同则不再进行
                mess.append('more_time' + block_after_str)
            elif self.check_for_after(block_after_str, block_after_num):
                #时间内容相同，则尝试进行补充
                if self.check_time(block_after_str, res, state, url):
                    return 'ok',block_after_str,'is_after_block',mess
                else:
                    mess.append('aftererror:'+block_after_str)
            else:
                #针对after的检查失败
                mess.append('aftercheckerror:'+block_after_str)
        #处理page_after
        page_after_str, page_after_num = self.get_after_page(blocks, block_xpath)
        page_after_str, page_after_num = self.delete_mon(page_after_str)
        if page_after_num == 0:
            mess.append('no_time')
        else:
            c_is_same = self.is_same(page_after_str, state)
            if c_is_same == 0:
                #补充年或年月日，时间不同则不再进行
                mess.append('more_time' + page_after_str)
            elif self.check_for_after(page_after_str, page_after_num):
                #时间内容相同，则尝试进行补充
                if self.check_time(page_after_str, res, state, url):
                    return 'ok',page_after_str,'is_after_page',mess
                else:
                    mess.append('aftererror:'+ page_after_str)
            else:
                #针对after的检查失败
                mess.append('aftercheckerror:'+ page_after_str)
        
        return 'error', '', '', mess

    def delete_mon(self, org_str):
        ret_num = 0
        ret_str = ''
        items = org_str.split('$')
        for i in items:
            if len(i) != 8:
                continue
            if i[0:4] == 'XXXX':
                continue
            else:
                ret_num += 1
                ret_str = ret_str + i + '$'
        return ret_str, ret_num

    def get_before_block(self, fields, time_str, time_key):
        block_before_str = ''
        block_before_num = 0
        try_flag = 0
        for i in fields:
            if i.get('value', 'no') is time_str and i.get('key', 'no') is time_key:
                try_str = i.get('key', 'no')
                try_flag = 1 
            else:
                try_str = i.get('value', 'no')
            cur_str = try_str
            while(1):
                flag,year,v = self.get_year(cur_str, 0)
                if flag == 1:
                    block_before_num += 1
                    block_before_str = block_before_str + year['year'] + year['mon'] + year['day'] + '$'
                    cur_str = cur_str[v[1]:]
                else: 
                    break;
            if try_flag == 1: #已处理至时间表达式处
                break;
        return block_before_str, block_before_num

    def get_after_block(self, fields, time_str, time_key):
        block_after_str = ''
        block_after_num = 0
        try_flag = 0 
        for i in fields:
            if i.get('value', 'no') is time_str and i.get('key', 'no') is time_key:
                try_flag = 1 
                continue
            if try_flag == 0:
                continue
            cur_str = i.get('value', 'no') 
            while(1):
                flag,year,v = self.get_year(cur_str, 0)
                if flag == 1:
                    block_after_num += 1
                    block_after_str = block_after_str + year['year'] + year['mon'] + year['day'] + '$'
                    cur_str = cur_str[v[1]:]
                else: 
                    break;
        return block_after_str, block_after_num
    
    def get_before_page(self, blocks, block_xpath):
        page_before_str = ''
        page_before_num = 0
        for i in blocks:
            xpath = i.get('xpath', 'no')
            if xpath is block_xpath:
                #处理到当前块，跳出
                break;
            page_fields = i.get('fields', 'no')
            if page_fields is 'no':
                continue
            for ii in page_fields:
                cur_str = ii.get('value', 'no')
                while(1):
                    flag,year,v = self.get_year(cur_str, 0)
                    if flag == 1:
                        page_before_num += 1
                        page_before_str = page_before_str + year['year'] + year['mon'] + year['day'] + '$'
                        cur_str = cur_str[v[1]:]
                    else: 
                        break;
        return page_before_str, page_before_num

    def get_after_page(self, blocks, block_xpath):
        page_after_str = ''
        page_after_num = 0
        try_flag = 0
        for i in blocks:
            xpath = i.get('xpath', 'no')
            if xpath is block_xpath:
                try_flag = 1
                continue
            if try_flag == 0:
                continue
            page_fields = i.get('fields', 'no')
            if page_fields is 'no':
                continue
            for ii in page_fields:
                cur_str = ii.get('value', 'no')
                while(1):
                    flag,year,v = self.get_year(cur_str, 0)
                    if flag == 1:
                        page_after_num += 1
                        page_after_str = page_after_str + year['year'] + year['mon'] + year['day'] + '$'
                        cur_str = cur_str[v[1]:]
                    else: 
                        break;
        return page_after_str, page_after_num

    def is_same(self, str, state):
        ret_same = 1
        items = str.split('$')
        if state is 'lack_year':
            first_str = ''
            for i in items:
                if len(i) != 8:
                    continue
                if len(first_str) < 1:
                    first_str = i[0:4]
                    continue
                cur = i[0:4]
                if first_str != cur:
                    ret_same = 0
                    break;
        else:
            before = ''
            for i in items:
                if len(i) != 8:
                    continue
                if len(before) < 1:
                    before = i
                if before[0:4] != 'XXXX' and i[0:4] != 'XXXX' and before[0:4] != i[0:4]:
                    ret_same = 0
                    break
                if before[4:6] != 'XX' and i[4:6] != 'XX' and before[4:6] != i[4:6]:
                    ret_same = 0
                    break
                if before[6:8] != 'XX' and i[6:8] != 'XX' and before[6:8] != i[6:8]:
                    ret_same = 0
                    break
                before = i
        return ret_same

    def check_for_after(self, check_str, num):
        #对于afterstr，有两个条件
        #有多个时间
        #有全时间
        if num > 1:
            return True
        items = check_str.split('$')
        for i in items:
            if len(i) != 8:
                continue
            if i[4:6] != 'XX' and i[6:8] != 'XX':
                today = datetime.date.today()
                d = datetime.datetime.strptime(i, '%Y%m%d').date()
                delta = today - d
                if delta.days <= 5*365:
                    return True
        return False

    def check_time(self, year, res, state, url):
        items = year.split('$')
        max_year = 'XXXX'
        max_mon = 'XX'
        max_day = 'XX'
        for i in items:
            if len(i) != 8:
                continue;
            cur_year = i[0:4]
            cur_mon = i[4:6]
            cur_day = i[6:8]
            if state is 'lack_year' and cur_year != 'XXXX':
                res['year_s'] = cur_year
                return True
            if state is 'lack_mon':
                if max_year == 'XXXX' and cur_year != 'XXXX':
                    max_year = cur_year
                if max_mon == 'XX' and cur_mon != 'XX':
                    max_mon = cur_mon
                if max_day == 'XX' and cur_day != 'XX':
                    max_day = cur_day
        if state is 'lack_mon' and max_year != 'XXXX' and max_mon != 'XX':
            res['year_s'] = max_year
            res['mon_s'] = max_mon
            res['day_s'] = max_day
            return True
        return False

    def get_year(self, line, is_title):
        out = {}
        year = 'XXXX'
        mon = 'XX'
        day = 'XX'
        m = {}
        m = self.p1.search(line)
        flag = 0
        v = ['0', '0'] 
        if m:
            flag = 1
            #LOG_TRACE("TIME_COMPLETE p1")
        if flag != 1:
            m = self.p5.search(line)
            if m:
                flag = 1
        if flag != 1:
            m = self.p2.search(line)
            if m:
                flag = 1
                #LOG_TRACE("TIME_COMPLETE p2")
        if flag != 1:
            m = self.p3.search(line)
            if m:
                flag = 1
                #LOG_TRACE("TIME_COMPLETE p3")
        if flag != 1 and is_title == 1:
            m = self.p4.search(line)
            if m:
                flag = 1
                #LOG_TRACE("TIME_COMPLETE p4")
        if m :
            v[0] = m.start()
            v[1] = m.end() - 1
            for (a,b) in m.groupdict().items():
                if str(a) == 'YEAR':
                    if str(b) == 'None':
                        year = 'XXXX'
                    else:
                        year = str(b)
                if str(a) == 'MON':
                    if str(b) == 'None':
                        mon = 'XX'
                    else:
                        mon = str(b)
                        if len(mon) == 1:
                            mon = '0' + mon
                if str(a) == 'DAY':
                    if str(b) == 'None':
                        day = 'XX'
                    else:
                        day = str(b)
                        if len(day) == 1:
                            day = '0' + day
        if year  != 'XXXX' or mon != 'XX':
            out['year'] = year
            out['mon'] = mon
            out['day'] = day 
            flag = 1
        else:
            flag = 0
        return flag,out,v


if __name__ == "__main__":
    time_extract = Complete()
    f_input = open("time.txt", 'r')
    output_file = open("out.txt", 'w+')
    try:
        while True:
            list_uline = []
            line = f_input.readline()
            line = line.strip()
            if len(line) == 0:
                break;
            output_file.write(line + '\t')
            uline =  unicode(line, 'utf8') 
            list_uline.append(uline)
            out = time_extract.get_year(uline, 0)
            out_str = ''
            if len(out) > 0:
                out_str = out['year'] + out['mon'] + out['day'] 
            output_file.write(out_str.encode('utf-8'))
            output_file.write('\n')
            output_file.flush()
    finally:
        f_input.close()
        output_file.close()

