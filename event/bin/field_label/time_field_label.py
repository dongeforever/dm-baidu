#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Time-stamp: <2014-11-14 22:33:08 Friday by work>

# @version 1.0
# @author liuzhendong01  liuzhendong01@baidu.com  

import json
import global_obj
import wordseg
import field_label_base
import re
import check_time
from FrameLog import *

class TimeFieldLabel(field_label_base.FieldLabelBase):
    def __init__(self):
        self.check = check_time.CheckTime()
        self.key_list= [u'时间', u'日期']
        self.error_list = [u'注册', u'发布']
        curr_dir = os.path.split(os.path.realpath(__file__))[0]
        self.low_dict = {}
        self.height_dict = {}
        #dict_file = curr_dir + '/key_dict.txt'
        dict_file = curr_dir + '/../../conf/time_sem_key.conf'
        low_file = open(dict_file , 'r')
        try:
            while True:
                line = low_file.readline()
                line = line.strip()
                if len(line) == 0:
                    break
                line = unicode(line, 'utf8')
                items = line.split('\t')
                if len(items) < 2:
                    continue
                #key = unicode(items[0], 'utf8')
                key = items[0]
                if items[1] == '<':
                    self.height_dict[key] = items[2]
                elif items[1] == '>':
                    self.low_dict[key] = items[2]
        finally:
            low_file.close()


    def in_key_list(self, cur_str):
        for i in self.key_list:
            if i in cur_str:
                return True
        return False
    def in_error_list(self, cur_str):
        for i in self.error_list:
            if i in cur_str:
                return True
        return False

    def is_date_attr(self, key, value):
        res = wordseg.seg(key)
        if len(key) > 100 or len(value) > 100:
            return False
        re_rule_date_key = r'(.*?)(日(.{0,5})期|时(.{0,5})间)(.*?)'
        re_rule_date_value = r'(.*?)(每天|星期|(年|月)(.{1,6})(年|月|日))(.*?)'
        key = key.encode('utf-8')
        value = value.encode('utf-8')
        if re.search(re_rule_date_key,key):
            return True
        elif re.search(re_rule_date_value, value):
            return True
        else:
            return False

    def total_key(self, key, value, url):
        if len(key) < 1 or key == 'normal_text':
            return '' 
        if len(value) < 1:
            value = 'no'
        #ret_str = '$' + '0' + '$' + key + '$' + value 
        ret_str = '$' + '0' + '$' + key
        return ret_str

    def get_key_mess(self, fields):
        ret_dict = {}
        for i in range(len(fields)):
            field = fields[i]
            if not "key" in field or not "value" in field:
                continue
            if self.in_key_list(field['key']) and not self.in_error_list(field['key']):
                ret_dict[i] = field['key']
        return ret_dict
    
    #ret=0:相等 ret>0: str1>str2 ret<0: str1<str2
    def which_height(self, str1, str2):
        ret = 0
        while len(str1) != len(str2):
            if len(str1) < len(str2):
                str1.append('none')
            else:
                str2.append('none')
        num = len(str2)

        for i in range(0,num):
            if self.low_dict.has_key(str1[i]) and not self.low_dict.has_key(str2[i]): 
                ret = 1
                return ret
            elif not self.low_dict.has_key(str1[i]) and self.low_dict.has_key(str2[i]):
                ret = -1
                return ret
            elif not self.low_dict.has_key(str1[i]) and not self.low_dict.has_key(str2[i]):
                ret = 0
                return ret
            if str2[i] in self.low_dict[str1[i]]:
                ret = 1
            if str1[i] in self.low_dict[str2[i]]:
                ret = -1
                    
        return ret

    def find_best_time(self, big_num, key_wordseg):
        may_be_dict = {}
        while True:
            for (k,v) in key_wordseg.items():
                if len(may_be_dict) == 0:
                    may_be_dict[k] = v
                    del key_wordseg[k]
                    continue
                for (kk, vv) in may_be_dict.items():
                    vv_str = ''
                    v_str = ''
                    for i in vv:
                        vv_str += i
                    for i in v:
                        v_str += i

                    core = self.which_height(vv, v)
                    if core == 0:
                        #不影响最后插入
                        pass
                    elif core > 0:
                        del key_wordseg[k]
                        break;
                    elif core < 0:
                        #最终也可以插入
                        del may_be_dict[kk]
                if key_wordseg.has_key(k):
                    may_be_dict[k] = key_wordseg[k]
                    del key_wordseg[k]
            if len(key_wordseg) == 0:
                break;
        return may_be_dict



    def label(self,fields,block_json,page_json={}):
        #print 'label'
        #for i in range(len(fields)):
        #    field = fields[i]
        #    print 'key:' + field['key'].encode('utf8')
        #    print 'value:' + field['value'].encode('utf8')
        indexs = []
        url = page_json.get('url', 'no_url')

        log_str = url
        for i in range(len(fields)):
            field = fields[i]
            if not "key" in field or not "value" in field:
                continue
            cur_str = self.total_key(field['key'], field['value'], url)
            log_str = log_str + cur_str
        log_str = log_str.replace(' ', '')
        log_str = log_str.replace(u'　', '')

        key_mess = self.get_key_mess(fields)
        if len(key_mess) == 0:
            LOG_TRACE('TIME_SEM_no_time url: %s log: %s', url, log_str)
            return indexs
        if len(key_mess) == 1:
            for (k,v) in key_mess.items():
                indexs.append(k)
            LOG_TRACE('TIME_SEM_one_time url: %s time: %s log: %s', url, v, log_str)
            return indexs
        more_time_str = '$'
        for (k,v) in key_mess.items():
            more_time_str += v + '$'
        more_time_str = more_time_str.replace(' ', '')
        more_time_str = more_time_str.replace(u'　', '')
        #LOG_TRACE('TIME_SEM_more_time url: %s more_time_str: %s log: %s', url, more_time_str, log_str)
        key_wordseg = {}
        big_num = 0
        for (k,v) in key_mess.items():
            try:
                res = wordseg.seg(v)
            except:
                continue
            res_dict = res
            if not 'basic' in res_dict:
                continue
            list = res_dict['basic']
            if len(list) < 1:
                continue
            new_list = []
            for ll in list[::-1]:
                if len(ll) < 2 or self.in_key_list(ll):
                    continue
                new_list.append(ll)
            if len(new_list) == 0:
                new_list.append('none')
            key_wordseg[k] = new_list
            if len(new_list) > big_num:
                big_num = len(new_list)
        out_dict = self.find_best_time(big_num, key_wordseg)
        out_dict_str = '$'
        for (k,v) in out_dict.items():
            for vi in v:
                out_dict_str += vi
            out_dict_str += '$'
        if len(out_dict) != 1:
            LOG_TRACE('TIME_SEM_error url: %s out_dict_str: %s more_time_str: %s log: %s', url, out_dict_str, more_time_str, log_str)
            year_dict, year_num = self.check.get_all_year(fields, out_dict)
            check_log_str = '$'
            for (k,v) in out_dict.items():
                check_log_str += fields[k]['key'] + ':' + fields[k]['value'] + '$'
            check_log_str = check_log_str.replace(' ', '')
            check_log_str = check_log_str.replace(u'　', '')
            if year_num == 1:
                for (k,v) in year_dict.items():
                    if len(v) > 0:
                        indexs.append(k)
                        key = fields[k]['key'].replace(' ', '')
                        key = key.replace(u'　', '')
                        value = fields[k]['value'].replace(' ', '')
                        value = value.replace(u'　', '')
                        LOG_TRACE('TIME_SEM_check_one_time url %s k: %s value: %s log: %s', url, key, value, check_log_str)
                        break
            else:
                check_same , num = self.check.same_year(year_dict)
                if check_same:
                    indexs.append(num)
                    key = fields[num]['key'].replace(' ', '')
                    key = key.replace(u'　', '')
                    value = fields[num]['value'].replace(' ', '')
                    value = value.replace(u'　', '')
                    LOG_TRACE('TIME_SEM_check_same_time url %s k: %s value: %s log: %s', url, key, value, check_log_str)
                else:
                    LOG_TRACE('TIME_SEM_check_error url %s log: %s', url, check_log_str)
        else:
            for (k,v) in out_dict.items():
                indexs.append(k)
            LOG_TRACE('TIME_SEM_ok url: %s out_dict_str: %s more_time_str: %s log: %s', url, out_dict_str, more_time_str, log_str)
        return indexs

'''
    def is_date_attr(self, key, value):
        res = wordseg.seg(key)
        if len(key) > 100 or len(value) > 100:
            return False
        re_rule_date_key = r'(.*?)(日(.{0,5})期|时(.{0,5})间)(.*?)'
        re_rule_date_value = r'(.*?)(每天|星期|(年|月)(.{1,6})(年|月|日))(.*?)'
        key = key.encode('utf-8')
        value = value.encode('utf-8')
        if re.search(re_rule_date_key,key):
            return True
        elif re.search(re_rule_date_value, value):
            return True
        else:
            return False

    def total_key(self, key, value, url):
        if len(key) < 1 or key == 'normal_text':
            return '' 
        if len(value) < 1:
            value = 'no'
        ret_str = '$' + '0' + '$' + key + '$' + value 
        return ret_str


    def label(self,fields,block_json,page_json={}):
        url = page_json.get('url', 'no_url')

        log_str = url
        for i in range(len(fields)):
            field = fields[i]
            if not "key" in field or not "value" in field:
                continue
            cur_str = self.total_key(field['key'], field['value'], url)
            log_str = log_str + cur_str
        log_str = log_str.replace(' ', '')
        LOG_TRACE('TIME_KEY_total %s', log_str)

        indexs = []
        for i in range(len(fields)):
            field = fields[i]
            if not "key" in field or not "value" in field:
                continue
            if self.is_date_attr(field["key"], field["value"]):
                indexs.append(i)
        return indexs 
        '''
    
if __name__ == "__main__":
    test = TimeFieldLabel()
    test.label([],{},{})


