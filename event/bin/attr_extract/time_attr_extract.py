#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Time-stamp: <2014-11-14 22:33:08 Friday by work>

# @version 1.0
# @author shaoyuanhua shaoyuanhua@baidu.com  

import sys
import attr_extract_base
from lib import time_fsm 
from lib import complete_time 
import json
import string
import threading
import datetime
from FrameLog import *


class TimeAttrExtract(attr_extract_base.AttrExtractBase):
    def __init__(self):
        self.time = time_fsm.TimeFsm()
        self.complete = complete_time.Complete()
        #self.lock = threading.Lock()
    def get_field_value_text(self,fields):
        key_value = ''
        key = ''
        text =  ""
        field_shijian = []
        field_jiezhi = []
        i = 0
        #log
        for field in fields:
            if u'注册' in field["key"] or u'发布' in field["key"] or u'更新' in field["key"]:
                continue
            #开始时间 or 
            #if u'\u6D3B\u52A8\u65F6\u95F4' in field["key"] and u'\u62A5\u540D' not in field["key"]:
            if u'活动时间' in field["key"] and u'\u62A5\u540D' not in field["key"]:
                return field["key"],field["value"]
            #活动时间
            elif u'\u6D3B\u52A8\u65F6\u95F4' in field["key"] and u'\u62A5\u540D' not in field["key"]:
                return field["key"],field["value"]
            elif u'时间' in field["key"] or u'日期' in field["key"]:
                if u'\u622A\u6B62' in field["key"] or u'\u62A5\u540D' in field["key"]:
                    field_jiezhi.append(field)
                else:
                    field_shijian.append(field)
        if len(field_shijian) > 0:
            return field_shijian[0]["key"], field_shijian[0]["value"]
        elif len(field_jiezhi) > 0:
            return field_jiezhi[0]["key"], field_jiezhi[0]["value"]
        else:
            for field in fields:
                if u'注册' in field["key"] or u'发布' in field["key"] or u'更新' in field["key"]:
                    continue
                else: 
                    return fields[0]["key"],fields[0]["value"]
        return '', ''

    def extract(self,fields,block_json,page_json):
        url = page_json.get('url', 'no_url')
        key_value = ''
        #log
        for field in fields:
            key_value = key_value + '$' + field['key'] + ':' + field['value'] + '$'
        LOG_TRACE('TIME_enter %s', key_value)
        key_value = key_value.replace(' ','')
        #if len(fields) == 0 or len(block_json) == 0:
        #    return {}
        list = []
        ret = {}
        ret['status'] = -1
        format_value = {}
        block_text = json.dumps(block_json,ensure_ascii=False)
        org_key,origin_text = self.get_field_value_text(fields) 
        res = self.time.begin(origin_text)
        out_str = ''
        #self.lock.acquire()
        #fp = open('{0}'.format('syh.txt'), 'a+')
        if len(res) == 1:
            no_year_flag = False
            for i in range(len(res)):
                #fp.write('{0} {1}\n'.format('$' * 10, res[i]))
                self.pre_process(res[i])
                tmp_origin_text = origin_text.replace(' ','')
                if res[i]['year_s'] is 'XXXX':
                    before_time_str = self.dict2str(res[i])
                    LOG_TRACE('TIME_COM_begin %s %s before: %s url: %s', key_value, tmp_origin_text, before_time_str, url)
                    if self.need_com(res[i]['cond_cont']):
                        mon_flag = res[i]['mon_s']
                        mess = []
                        is_ok,com_str,flag,mess = self.complete.process(res[i], org_key, origin_text, block_json, page_json)
                        com_str = com_str.replace(' ','')
                        mess_str = '$'.join(mess)
                        if is_ok == 'ok':
                            #补全成功了
                            LOG_TRACE('TIME_COM_success %s %s before: %s after: %s url: %s com_str: %s flag: %s mess: %s lack: %s', key_value, tmp_origin_text, before_time_str, self.dict2str(res[i]), url, com_str, flag, mess_str, mess[0])
                        elif is_ok == 'error':
                            if 'no_time' in mess_str and mess[0] is 'lack_mon' and self.maybe_no_year(res[i]):
                                LOG_TRACE('TIME_COM_suc_no_year %s %s before: %s after: %s url: %s com_str: %s flag: %s mess: %s lack: %s', key_value, tmp_origin_text, before_time_str, self.dict2str(res[i]), url, com_str, flag, mess_str, mess[0])
                            else:
                                no_year_flag = True
                                no_time_flag = 1
                                for j in range(1,len(mess)):
                                    if mess[j] != 'no_time':
                                        no_time_flag = 0

                                if no_time_flag == 1:
                                    LOG_TRACE('TIME_COM_error_no_time %s %s before: %s after: %s url: %s com_str: %s flag: %s mess: %s lack: %s', key_value, tmp_origin_text, before_time_str, self.dict2str(res[i]), url, com_str, flag, mess_str, mess[0])
                                else:
                                    LOG_TRACE('TIME_COM_error_more_time %s %s before: %s after: %s url: %s com_str: %s flag: %s mess: %s lack: %s', key_value, tmp_origin_text, before_time_str, self.dict2str(res[i]), url, com_str, flag, mess_str, mess[0])
                    else:
                        LOG_TRACE('TIME_COM_noneed_com %s %s before: %s url: %s', key_value, tmp_origin_text, before_time_str, url)
                                
                if self.process_jiezhi(org_key, res):
                    LOG_TRACE('TIME is_jiezhi %s:%s %s url:%s', org_key, tmp_origin_text, str(res), url)

                self.pre_process(res[i])
                tmp_str = self.dict2str(res[i])
                LOG_TRACE('TimeAttrExtract single' + tmp_origin_text + '   '+ tmp_str + '\t' + url)
                out_str = out_str + ' ' + tmp_str
            list = res
            ret['status'] = 0
            format_value['cont'] = list
            format_value['str'] = out_str
            #年份没有补全, 标记为-1
            if no_year_flag:
                ret['status'] = -1

            #if ret['status'] == 0 and org_key == 'normal_text':
            #    LOG_TRACE('TIME_status is_normal_text')
            #if ret['status'] == 0:
            #    LOG_TRACE('TIME_status not_normal_text')
        ret['origin_value'] = origin_text
        ret['format_value'] = format_value
        #self.lock.release()
        LOG_TRACE('TimeAttrExtract out' + str(ret))
        return ret 
    def pre_process(self, res):
        pre_str = res['year_s'] + res['mon_s'] + res['day_s']
        aft_str = res['year_e'] + res['mon_e'] + res['day_e']
        if pre_str == 'XXXXXXXX' or aft_str == 'XXXXXXXX':
            return
        before = {}
        before = res 
        res['year_s'],res['year_e'] = self.make_same(res['year_s'],res['year_e'])
        res['mon_s'],res['mon_e'] = self.make_same(res['mon_s'],res['mon_e'])
        res['day_s'],res['day_e'] = self.make_same(res['day_s'],res['day_e'])
        if self.dict2str(before) != self.dict2str(res):
            LOG_TRACE('TIME_pre_process %s %s ', self.dict2str(before), self.dict2str(res))

    def make_same(self,s,e):
        if 'XX' in s and 'XX' not in e:
            s = e
        if 'XX' in e and 'XX' not in s:
            e = s
        return s,e

    #有些时间没有年份，只有频率或时间区间
    def maybe_no_year(self, res):
        if len(res['cond_cont']) > 1:
            return True
        if res['hour_s'] != 'XX' and res['hour_e'] != 'XX':
            return True
        return False
            
    def need_com(self, cond):
        if len(cond) == 1:
            if cond[0] == 'MEI_TIAN' or cond[0] == 'MEI_YUE' or cond[0] == 'MEI_ZHOU':
                return False 
        return True 

    def process_jiezhi(self, org_key, res):
        if u'\u622A\u6B62' in org_key and len(res) == 1: 
            if res[0]['cont'] == 'DAY' or res[0]['cont'] == 'DAY_TIME':
                res[0]['year_e'] = res[0]['year_s']
                res[0]['mon_e'] = res[0]['mon_s']
                res[0]['day_e'] = res[0]['day_s']
                res[0]['hour_e'] = res[0]['hour_s']
                res[0]['min_e'] = res[0]['min_s']
                res[0]['sec_e'] = res[0]['sec_s']
                if self.is_old_time(res[0]['year_e'], res[0]['mon_e'], res[0]['day_e']):
                    res[0]['year_s'] = res[0]['year_e'] 
                    res[0]['mon_s'] = res[0]['mon_e']
                    res[0]['day_s'] = res[0]['day_e']
                else:
                    today = datetime.date.today()
                    today_str = today.strftime('%Y-%m-%d')
                    items = today_str.split('-')
                    if len(items) == 3:
                        res[0]['year_s'] = items[0] 
                        res[0]['mon_s'] = items[1]
                        res[0]['day_s'] = items[2]
                    else:
                        res[0]['year_s'] = 'XXXX'
                        res[0]['mon_s'] = 'XX'
                        res[0]['day_s'] = 'XX'
                res[0]['hour_s'] = 'XX'
                res[0]['min_s'] = 'XX'
                res[0]['sec_s'] = 'XX'
                return True
        return False
    def is_old_time(self, year, mon, day):
        if year is 'XXXX':
            return True
        if mon is 'XX':
            time_str = year +'01' + '01'
        else:
            time_str = year + mon + day
        today = datetime.date.today()
        d = datetime.datetime.strptime(time_str, '%Y%m%d').date()
        delta = today - d
        if delta.days < 0:
            return False
        else:
            return True
        
    def dict2str(self, res):
        ret_str = ''
        year_s = 'XXXX'
        year_e = 'XXXX'
        mon_s = 'XX'
        mon_e = 'XX'
        day_s = 'XX'
        day_e = 'XX'
        hour_s = 'XX'
        hour_e = 'XX'
        min_s = 'XX'
        min_e = 'XX'
        sec_s = 'XX'
        sec_e = 'XX'
        if (len(res['year_s']) > 0):
            year_s = res['year_s']
        if (len(res['year_e']) > 0):
            year_e = res['year_e']
        if (len(res['mon_s']) > 0):
            mon_s = res['mon_s']
        if (len(res['mon_e']) > 0):
            mon_e = res['mon_e']
        if (len(res['day_s']) > 0):
            day_s = res['day_s']
        if (len(res['day_e']) > 0):
            day_e = res['day_e']
        if res['hour_s']  != 'XX':
            h = int(res['hour_s'])
            if res['after_s'] == 'afternoon' and h <= 12:
                h = 12 + h
            hour_s = str(h) 
        else:
            hour_s = res['hour_s']
        if res['hour_e']  != 'XX':
            h = int(res['hour_e'])
            if res['after_e'] == 'afternoon' and h <= 12:
                h = 12 + h
            hour_e = str(h) 
        else:
            hour_e = res['hour_e']
        if (len(res['min_s']) > 0):
            min_s = res['min_s']
        if (len(res['min_e']) > 0):
            min_e = res['min_e']
        if (len(res['sec_s']) > 0):
            sec_s = res['sec_s']
        if (len(res['sec_e']) > 0):
            sec_e = res['sec_e']
        if res['cont'] is 'ALL_ALL':
            ret_str = year_s + '-' + mon_s + '-' + day_s + '/' + hour_s + ':' + min_s + ':' + sec_s  + '~' + year_e + '-' + mon_e + '-' + day_e + '/' + hour_e + ':' + min_e + ':' + sec_e
            #ret_str = year_s + '-' + mon_s + '-' + day_s + ' ' + hour_s + ':' + min_s + ':' + sec_s  + ' ~ ' + year_e + '-' + mon_e + '-' + day_e + ' ' + hour_e + ':' + min_e + ':' + sec_e
        else:
            ret_str = year_s + '-' + mon_s + '-' + day_s + '~' + year_e + '-' + mon_e + '-' + day_e + '/' + hour_s + ':' + min_s + ':' + sec_s  + '~' + hour_e + ':' + min_e + ':' + sec_e 
            #ret_str = year_s + '-' + mon_s + '-' + day_s + ' ~ ' + year_e + '-' + mon_e + '-' + day_e + '  ' + hour_s + ':' + min_s + ':' + sec_s  + ' ~ ' + hour_e + ':' + min_e + ':' + sec_e 
        ret_str = ret_str + '('
        #ret_str = ret_str + ' ('
        for i in res['cond_cont']:
            ret_str = ret_str + '/' + i + '/'
            #ret_str = ret_str + ' ' + i + ' '
        ret_str = ret_str + ')'
        return ret_str

if __name__ == "__main__":
	time_extract = TimeAttrExtract()
	f_input = open("../data/time1.txt", 'r')
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
			dict = time_extract.extract(list_uline, {}, {})
			if not dict or dict['status'] != 0:
				print 'error'
			else:
				print type(dict)
				print dict
				print dict["origin_value"]
				output_file.write(dict['format_value']['str'].encode('utf-8'))
			output_file.write('\n')
			output_file.flush()
	finally:
		f_input.close()
		output_file.close()



