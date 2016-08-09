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

class CheckTime():
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

    def get_all_year(self, fields, check):
        ret_dict = {}
        year_num = 0
        for (k,v) in check.items():
            if k < 0 or k >= len(fields):
                continue
            value = fields[k]['value']
            flag, year, v = self.get_year(value, 0)
            if flag == 1:
                ret_dict[k] = year
                year_num += 1
            else:
                ret_dict[k] = {}
        return ret_dict,year_num

    def same_year(self, year_dict):
        num = 0
        total_str = ''
        before_str = ''
        for (k,v) in year_dict.items():
            if len(v) > 0:
                cur_str = v['year'] + v['mon'] + v['day']
                total_str += cur_str +'$'
                if len(before_str) < 1:
                    num = k
                    before_str = cur_str
                else:
                    if before_str[0:4] == 'XXXX' and v['year'] != 'XXXX':
                        before_str = cur_str
                        num = k
                    elif before_str[4:6] == 'XX' and v['mon'] != 'XX':
                        before_str = cur_str
                        num = k
                    elif before_str[6:8] == 'XX' and v['day'] != 'XX':
                        before_str = cur_str
                        num = k
        if len(total_str) < 1:
            return False, num
        if self.is_same(total_str):
            return True, num 
        return False, num 
            

    def is_same(self, str):
        ret_same = 1
        items = str.split('$')
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

