#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Time-stamp: <2014-11-14 22:33:08 Friday by work>

# @version 1.0
# @author shaoyuanhua shaoyuanhua@baidu.com  

import re
import string
import Queue
import mine_time 
import traceback
#from FrameLog import *

#时间状态基类
class base_fsm:
    #处理下一个输入
    def re_init(self):
        return {}
    def reset(self):
        return {}
    def enter_state(self, obj):
        pass
    def get_state(self):
        return self.state_str
    #查找输入对应的处理逻辑
    def keep_state(self):
        pass
    def exec_state(self, obj):
        #1：状态
        if obj.has_key('cont') and obj['cont'] != 'null':
            if self.state_dict.has_key(obj['cont']):
                next_state = self.state_dict[obj['cont']]
            else:
                next_state = 'start_fsm' 
            return next_state
        elif obj.has_key('char'):
            next_state = ''
            if self.char_dict.has_key(obj['char']):
                next_state = self.char_dict[obj['char']]
            if len(next_state) < 1:
                next_state = self.get_state()
            return next_state
    #结束当前的状态
    def exit_state(self, obj):
        pass
    def stop_state(self, list1, tmp_dict ):
        pass
    def copy_day_s(self, d_dict, o_dict):
        d_dict['year_s'] = o_dict['year_s']
        d_dict['mon_s'] = o_dict['mon_s']
        d_dict['day_s'] = o_dict['day_s']
    def copy_time_s(self, d_dict, o_dict):
        d_dict['hour_s'] = o_dict['hour_s']
        d_dict['min_s'] = o_dict['min_s']
        d_dict['sec_s'] = o_dict['sec_s']
    def copy_day_s2s(self, d_dict, o_dict):
        d_dict['year_s'] = o_dict['year_s']
        d_dict['mon_s'] = o_dict['mon_s']
        d_dict['day_s'] = o_dict['day_s']
    def copy_day_s2e(self, d_dict, o_dict):
        d_dict['year_e'] = o_dict['year_s']
        d_dict['mon_e'] = o_dict['mon_s']
        d_dict['day_e'] = o_dict['day_s']
    def copy_day_e2e(self, d_dict, o_dict):
        d_dict['year_e'] = o_dict['year_e']
        d_dict['mon_e'] = o_dict['mon_e']
        d_dict['day_e'] = o_dict['day_e']
    def copy_time_s2s(self, d_dict, o_dict):
        d_dict['hour_s'] = o_dict['hour_s']
        d_dict['min_s'] = o_dict['min_s']
        d_dict['sec_s'] = o_dict['sec_s']
    def copy_time_s2e(self, d_dict, o_dict):
        d_dict['hour_e'] = o_dict['hour_s']
        d_dict['min_e'] = o_dict['min_s']
        d_dict['sec_e'] = o_dict['sec_s']
    def copy_time_e2e(self, d_dict, o_dict):
        d_dict['hour_e'] = o_dict['hour_e']
        d_dict['min_e'] = o_dict['min_e']
        d_dict['sec_e'] = o_dict['sec_e']
    def copy_s2e(self, d_dict, o_dict):
        if o_dict['year_s'] != 'XXXX':
            d_dict['year_e'] = o_dict['year_s'] 
        if o_dict['mon_s'] != 'XX':
            d_dict['mon_e'] = o_dict['mon_s'] 
        if o_dict['day_s'] != 'XX':
            d_dict['day_e'] = o_dict['day_s'] 
        if o_dict['hour_s'] != 'XX':
            d_dict['hour_e'] = o_dict['hour_s'] 
        if o_dict['min_s'] != 'XX':
            d_dict['min_e'] = o_dict['min_s'] 
        if o_dict['sec_s'] != 'XX':
            d_dict['sec_e'] = o_dict['sec_s'] 
        if len(o_dict['cond_cont']) > 0 and o_dict is not d_dict:
            for i in o_dict['cond_cont']:
                d_dict['cond_cont'].append(i)
        if o_dict['after_s'] != 'XX' and d_dict['after_e'] == 'XX':
            d_dict['after_e'] = o_dict['after_s']

    def copy(self, d_dict, o_dict):
        if o_dict['year_s'] != 'XXXX':
            d_dict['year_s'] = o_dict['year_s'] 
        if o_dict['year_e'] != 'XXXX':
            d_dict['year_e'] = o_dict['year_e'] 
        if o_dict['mon_s'] != 'XX':
            d_dict['mon_s'] = o_dict['mon_s'] 
        if o_dict['mon_e'] != 'XX':
            d_dict['mon_e'] = o_dict['mon_e'] 
        if o_dict['day_s'] != 'XX':
            d_dict['day_s'] = o_dict['day_s'] 
        if o_dict['day_e'] != 'XX':
            d_dict['day_e'] = o_dict['day_e'] 
        if o_dict['hour_s'] != 'XX':
            d_dict['hour_s'] = o_dict['hour_s'] 
        if o_dict['hour_e'] != 'XX':
            d_dict['hour_e'] = o_dict['hour_e'] 
        if o_dict['min_s'] != 'XX':
            d_dict['min_s'] = o_dict['min_s'] 
        if o_dict['min_e'] != 'XX':
            d_dict['min_e'] = o_dict['min_e'] 
        if o_dict['sec_s'] != 'XX':
            d_dict['sec_s'] = o_dict['sec_s'] 
        if o_dict['sec_e'] != 'XX':
            d_dict['sec_e'] = o_dict['sec_e'] 
        if len(o_dict['cond_cont']) > 0 and o_dict is not d_dict:
            for i in o_dict['cond_cont']:
                d_dict['cond_cont'].append(i)
        if o_dict['after_s'] != 'XX' and d_dict['after_s'] == 'XX':
            d_dict['after_s'] = o_dict['after_s']
        if o_dict['after_e'] != 'XX' and d_dict['after_e'] == 'XX':
            d_dict['after_e'] = o_dict['after_e']
    def get_format(self, tmp_dict):
        ret = {}
        if len(tmp_dict) < 1:
            return ret
        ret = tmp_dict[0]
        for i in tmp_dict:
            self.copy(ret,i)
        return ret
    def get_format_point(self, tmp_dict):
        ret = {}
        if len(tmp_dict) == 1:
            return tmp_dict[0]
        else:
            ret = tmp_dict[0]
            if tmp_dict[1]['cont'] is 'DAY':
                #self.copy_day_s(ret, tmp_dict[1])
                self.copy(ret, tmp_dict[1])
            if tmp_dict[1]['cont'] is 'TIME':
                #self.copy_time_s2s(ret, tmp_dict[1]) 
                self.copy(ret, tmp_dict[1])
            return ret
    def get_format_mei(self, tmp_dict):
        ret = {}
        if len(tmp_dict) < 1:
            return ret
        else:
            ret = tmp_dict[0]
            x_list = tmp_dict[0]['cond_str'].split(' ')
            for i in x_list:
                ii = i.strip()
                if len(ii) < 1:
                    continue
                ret['cond_cont'].append(i)
            tmp_dict[0]['cond_str'] = ''
            return ret
    def get_format_dur(self, tmp_dict):
        ret = {}
        if len(tmp_dict) < 2:
            return ret
        else:
            ret = tmp_dict[0]
        time_num = 0
        day_num = 0
        for i in tmp_dict:
            if 'cont' not in i.keys():
                continue
            if i['cont'] == 'TIME':
                if time_num == 0:
                    #self.copy_time_s2s(ret, i)
                    self.copy(ret, i)  
                elif time_num == 1:
                    #self.copy_time_s2e(ret, i)
                    self.copy_s2e(ret, i) 
                time_num += 1
            elif i['cont'] == 'DAY':
                if day_num == 0:
                    #self.copy_day_s2s(ret, i)
                    self.copy(ret, i)
                elif day_num == 1:
                    #self.copy_day_s2e(ret, i)
                    self.copy_s2e(ret, i)
                day_num += 1
            elif i['cont'] == 'TIME_TIME':
                self.copy(ret, i)
                #self.copy_time_s2s(ret, i)
                #self.copy_time_e2e(ret, i)
            elif i['cont'] == 'DAY_DAY':
                self.copy(ret, i)
                #self.copy_day_s2s(ret, i)
                #self.copy_day_e2e(ret, i) 
            elif i['cont'] == 'DAY_TIME':
                self.copy_s2e(ret, i)
                #self.copy_day_s2e(ret, i)
                #self.copy_time_s2e(ret, i) 
        return ret
    def get_format_all_all(self, tmp_dict):
        ret = {}
        if len(tmp_dict) < 1:
            return ret
        ret = tmp_dict[0]
        if len(tmp_dict) < 2:
            return ret
        if tmp_dict[-1]['cont'] is 'TIME_TIME':
            self.copy(ret, tmp_dict[-1])
        elif tmp_dict[-1]['cont'] is 'TIME':
            if tmp_dict[0]['cont'] is 'DAY_DAY':
                self.copy(ret, tmp_dict[-1])
            else:
                self.copy_s2e(ret, tmp_dict[-1])
        else:
            self.copy_s2e(ret, tmp_dict[-1]) 
        return ret

#初始状态，接受任何输入
class start_fsm(base_fsm):
    def __init__(self):
        self.state_str = 'start_fsm'
        self.char_dict = {}
        #~:\u007E' ～:\uFF5E   每：\u6BCF
        self.char_dict[u'\u002D'] = 'qu_jian_fsm'
        self.char_dict[u'\u6BCF'] = 'mei_fsm'
        self.state_dict = {}
        self.state_dict['DAY'] = 'day_fsm'
        self.state_dict['TIME'] = 'time_fsm'
        self.state_dict['DAY_DAY'] = 'day_day_fsm'
        self.state_dict['TIME_TIME'] = 'time_time_fsm'
        self.state_dict['DAY_TIME'] = 'day_time_fsm'
        self.state_dict['MEI_TIAN'] = 'mei_tian_fsm'
        self.state_dict['MEI_YUE'] = 'mei_yue_fsm'
        self.state_dict['MEI_ZHOU'] = 'mei_zhou_fsm'
        self.state_dict['MEI_TIME'] = 'mei_time_fsm'
        self.state_dict['MEI_DAY'] = 'mei_day_fsm'
        self.state_dict['MEI_ALL'] = 'mei_all_fsm'
        self.state_dict['ALL_ALL'] = 'all_all_fsm'
        self.state_dict['ALL_SET'] = 'all_set_fsm'
    #处理下一个输入
    def enter_state(self, obj):
        self.data = obj

class qu_jian_fsm(base_fsm):
    def __init__(self):
        self.state_str = 'qu_jian_fsm'
        self.char_dict = {}
        self.state_dict = {}
    def enter_state(self, obj):
        self.data = obj
    def stop_state(self, list1, tmp_dict):
        self.data['cont'] = 'QU_JIAN'
        list1.append(self.data)

class mei_fsm(base_fsm):
    def __init__(self):
        self.state_str = 'mei_fsm'
        self.char_dict = {}
        #天：\u5929 月：\u6708 周：\u5468
        self.char_dict[u'\u5929'] = 'mei_tian_fsm'
        self.char_dict[u'\u6708'] = 'mei_yue_fsm'
        self.char_dict[u'\u5468'] = 'mei_zhou_fsm'
        self.state_dict = {}
    def exec_state(self, obj):
        #1：状态
        if obj.has_key('cont') and obj['cont'] != 'null':
            if self.state_dict.has_key(obj['cont']):
                next_state = self.state_dict[obj['cont']]
            else:
                next_state = 'start_fsm' 
            return next_state
        elif obj.has_key('char'):
            next_state = ''
            if self.char_dict.has_key(obj['char']):
                next_state = self.char_dict[obj['char']]
            if len(next_state) < 1:
                next_state = 'start_fsm' 
            return next_state
    def enter_state(self, obj):
        self.data = obj
    def stop_state(self, list1, tmp_dict):
        pass

class mei_time_fsm(base_fsm):
    def __init__(self):
        self.state_str = 'mei_time_fsm'
        self.char_dict = {}
        self.state_dict = {}
        self.state_dict['DAY_DAY'] = 'mei_all_fsm'
    def enter_state(self, obj):
        self.data = obj
    def exit_state(self, tmp_dict):
        tmp_dict.append(self.data)
    def stop_state(self, list1, tmp_dict):
        format = self.get_format(tmp_dict)
        format['cont'] = 'MEI_TIME'
        list1.append(format)

class mei_day_fsm(base_fsm):
    def __init__(self):
        self.state_str = 'mei_day_fsm'
        self.char_dict = {}
        self.state_dict = {}
        self.state_dict['TIME_TIME'] = 'mei_all_fsm'
    def enter_state(self, obj):
        self.data = obj
    def exit_state(self, tmp_dict):
        tmp_dict.append(self.data)
    def stop_state(self, list1, tmp_dict):
        format = self.get_format(tmp_dict)
        format['cont'] = 'MEI_DAY'
        list1.append(format)

class mei_all_fsm(base_fsm):
    def __init__(self):
        self.state_str = 'mei_all_fsm'
        self.char_dict = {}
        self.state_dict = {}
    def enter_state(self, obj):
        self.data = obj
    def exit_state(self, tmp_dict):
        tmp_dict.append(self.data)
    def stop_state(self, list1, tmp_dict):
        format = self.get_format(tmp_dict)
        format['cont'] = 'MEI_all'
        list1.append(format)
class mei_tian_fsm(base_fsm):
    def __init__(self):
        self.state_str = 'mei_tian_fsm'
        self.char_dict = {}
        self.state_dict = {}
    def re_init(self):
        self.state_dict['TIME_TIME'] = 'mei_all_fsm'
    def reset(self):
        self.state_dict['TIME_TIME'] = 'start_fsm'
    def enter_state(self, obj):
        self.data = obj
    def exit_state(self, tmp_dict):
        tmp_dict.append(self.data)
    def stop_state(self, list1, tmp_dict):
        self.data['cont'] = 'MEI_TIAN'
        list1.append(self.data)
class mei_zhou_fsm(base_fsm):
    def __init__(self):
        self.state_str = 'mei_zhou_fsm'
        self.char_dict = {}
        #一：\u4E00 二：\u4E8C 三：\u4E09 四：\u56DB 五：\u4E94
        self.char_dict[u'\u4E00'] = 'mei_zhou_fsm'
        self.char_dict[u'\u4E8C'] = 'mei_zhou_fsm'
        self.char_dict[u'\u4E09'] = 'mei_zhou_fsm'
        self.char_dict[u'\u56DB'] = 'mei_zhou_fsm'
        self.char_dict[u'\u4E94'] = 'mei_zhou_fsm'
        #六：\u516D 七：\u4E03 日：\u65E5 末：\u672B 天:\u5929
        self.char_dict[u'\u516D'] = 'mei_zhou_fsm'
        self.char_dict[u'\u4E03'] = 'mei_zhou_fsm'
        self.char_dict[u'\u65E5'] = 'mei_zhou_fsm'
        self.char_dict[u'\u672B'] = 'mei_zhou_fsm'
        self.char_dict[u'\u5929'] = 'mei_zhou_fsm'
        #周：\u5468 ~：\u007E -：\u002D 到：\u5230 至：\u81F3
        self.char_dict[u'\u5468'] = 'mei_zhou_fsm'
        self.char_dict[u'\u007E'] = 'mei_zhou_fsm'
        self.char_dict[u'\u002D'] = 'mei_zhou_fsm'
        self.char_dict[u'\u5230'] = 'mei_zhou_fsm'
        self.char_dict[u'\u81F3'] = 'mei_zhou_fsm'
        self.state_dict = {}
        self.trans_dict = {u'\u4E00':'Z1', u'\u4E8C':'Z2', u'\u4E09':'Z3', u'\u56DB':'Z4', u'\u4E94':'Z5', u'\u516D':'Z6', u'\u4E03':'Z7', u'\u65E5':'Z7', u'\u672B':'Z6 Z7', u'\u5929':'Z7'}
        self.dur_dict = {u'\u007E':1, u'\u002D':1, u'\u5230':1, u'\u81F3':1}
    def re_init(self):
        self.state_dict['TIME_TIME'] = 'mei_time_fsm'
        self.state_dict['DAY_DAY'] = 'mei_day_fsm'
    def reset(self):
        self.state_dict['TIME_TIME'] = 'start_fsm'
        self.state_dict['DAY_DAY'] = 'start_fsm'
    def enter_state(self, obj):
        self.data = obj
    def exec_state(self, obj):
        #1：状态
        if obj.has_key('cont') and obj['cont'] != 'null':
            if self.state_dict.has_key(obj['cont']):
                next_state = self.state_dict[obj['cont']]
            else:
                next_state = 'start_fsm' 
        elif obj.has_key('char'):
            next_state = ''
            if self.char_dict.has_key(obj['char']):
                next_state = self.char_dict[obj['char']]
            if len(next_state) < 1:
                next_state = self.get_state()
        if next_state != self.get_state() or 'char' not in obj.keys():
            return next_state
        if self.trans_dict.has_key(obj['char']):
            items = self.trans_dict[obj['char']].split(' ')
            if self.data.has_key('dur_flag') and len(self.data['cond_cont']) > 0 and len(items) > 0:
                last_num = string.atoi(filter(lambda x:x.isdigit(), self.data['cond_cont'][-1]))
                first_num = string.atoi(filter(lambda x:x.isdigit(), items[0])) 
                for num in range(last_num + 1, first_num):
                    self.data['cond_cont'].append('Z' + str(num))
            for i in items:
                self.data['cond_cont'].append(i)
        if self.dur_dict.has_key(obj['char']):
            self.data['dur_flag'] = 1
        return next_state
    def exit_state(self, tmp_dict):
        tmp_dict.append(self.data)
    def stop_state(self, list1, tmp_dict):
        self.data['cont'] = 'MEI_ZHOU'
        list1.append(self.data)

class mei_yue_fsm(base_fsm):
    def __init__(self):
        self.state_str = 'mei_yue_fsm'
        self.char_dict = {}
        self.char_dict = {'01':'mei_yue_fsm', '02':'mei_yue_fsm','03':'mei_yue_fsm','04':'mei_yue_fsm',\
                '05':'mei_yue_fsm','06':'mei_yue_fsm','07':'mei_yue_fsm','08':'mei_yue_fsm',\
                '09':'mei_yue_fsm','1':'mei_yue_fsm','2':'mei_yue_fsm','3':'mei_yue_fsm',\
                '4':'mei_yue_fsm','5':'mei_yue_fsm','6':'mei_yue_fsm','7':'mei_yue_fsm',\
                '8':'mei_yue_fsm','9':'mei_yue_fsm', '10':'mei_yue_fsm', '11':'mei_yue_fsm',\
                '12':'mei_yue_fsm','13':'mei_yue_fsm','14':'mei_yue_fsm','15':'mei_yue_fsm',\
                '16':'mei_yue_fsm','17':'mei_yue_fsm','18':'mei_yue_fsm','19':'mei_yue_fsm',\
                '20':'mei_yue_fsm', '21':'mei_yue_fsm','22':'mei_yue_fsm','23':'mei_yue_fsm',\
                '24':'mei_yue_fsm','25':'mei_yue_fsm','26':'mei_yue_fsm','27':'mei_yue_fsm',\
                '28':'mei_yue_fsm','29':'mei_yue_fsm','30':'mei_yue_fsm', '31':'mei_yue_fsm'}
        #号：\u53F7 日：\u65E5 ~：\u007E -：\u002D 到：\u5230 至：\u81F3
        self.char_dict[u'\u53F7'] = 'mei_yue_fsm'
        self.char_dict[u'\u65E5'] = 'mei_yue_fsm'
        self.char_dict[u'\u007E'] = 'mei_yue_fsm'
        self.char_dict[u'\u002D'] = 'mei_yue_fsm'
        self.char_dict[u'\u5230'] = 'mei_yue_fsm'
        self.char_dict[u'\u81F3'] = 'mei_yue_fsm'
        self.state_dict = {}
        self.state_dict['TIME_TIME'] = 'mei_time_fsm'
        self.state_dict['DAY_DAY'] = 'mei_day_fsm'
        self.trans_dict = {'01':'Y1', '02':'Y2','03':'Y3','04':'Y4',\
                '05':'Y5','06':'Y6','07':'Y7','08':'Y8',\
                '09':'Y9','1':'Y1','2':'Y2','3':'Y3',\
                '4':'Y4','5':'Y5','6':'Y6','7':'Y7',\
                '8':'Y8','9':'Y9', '10':'Y10', '11':'Y11',\
                '12':'Y12','13':'Y13','14':'Y14','15':'Y15',\
                '16':'Y16','17':'Y17','18':'Y18','19':'Y19',\
                '20':'Y20', '21':'Y21','22':'Y22','23':'Y23',\
                '24':'Y24','25':'Y25','26':'Y26','27':'Y27',\
                '28':'Y28','29':'Y29','30':'Y30', '31':'Y31'}
        self.dur_dict = {u'\u007E':1, u'\u002D':1, u'\u5230':1, u'\u81F3':1}
    def enter_state(self, obj):
        self.data = obj
    def exec_state(self, obj):
        #1：状态
        if obj.has_key('cont') and obj['cont'] != 'null':
            if self.state_dict.has_key(obj['cont']):
                next_state = self.state_dict[obj['cont']]
            else:
                next_state = 'start_fsm' 
        elif obj.has_key('char'):
            next_state = ''
            if self.char_dict.has_key(obj['char']):
                next_state = self.char_dict[obj['char']]
            if len(next_state) < 1:
                next_state = self.get_state()
        if next_state != self.get_state() or 'char' not in obj.keys():
            return next_state
        if self.trans_dict.has_key(obj['char']):
            items = self.trans_dict[obj['char']].split(' ')
            if self.data.has_key('dur_flag') and len(self.data['cond_cont']) > 0 and len(items) > 0:
                last_num = string.atoi(filter(lambda x:x.isdigit(), self.data['cond_cont'][-1]))
                first_num = string.atoi(filter(lambda x:x.isdigit(), items[0])) 
                for num in range(last_num + 1, first_num):
                    self.data['cond_cont'].append('Y' + str(num))
            for i in items:
                self.data['cond_cont'].append(i)
        if self.dur_dict.has_key(obj['char']):
            self.data['dur_flag'] = 1
        return next_state
    def exit_state(self, tmp_dict):
        tmp_dict.append(self.data)
    def stop_state(self, list1, tmp_dict):
        format = self.get_format_mei(tmp_dict)
        format['cont'] = 'MEI_YUE'
        list1.append(format)
#日期状态，如1987-12-28
class day_fsm(base_fsm):
    def __init__(self):
        self.state_str = 'day_fsm'
        self.char_dict = {}
        #-:\u002D  ~:\u007E －:\uFF0D —:\u2014
        self.char_dict[u'\u002D'] = 'day_2_fsm'
        self.char_dict[u'\u007E'] = 'day_2_fsm'
        self.char_dict[u'\u2014'] = 'day_2_fsm'
        self.char_dict[u'\uFF0D'] = 'time_2_fsm'
        self.state_dict = {}
        self.state_dict['DAY'] = 'start_fsm'
        self.state_dict['TIME'] = 'day_time_fsm'
        self.state_dict['DAY_DAY'] = 'start_fsm'
        self.state_dict['TIME_TIME'] = 'all_all_fsm'
        self.state_dict['ALL_ALL'] = 'start_fsm'
    def enter_state(self, obj):
        self.data = obj
    def exit_state(self, tmp_dict):
        tmp_dict.append(self.data)
    def stop_state(self, list1, tmp_dict):
        format = self.get_format(tmp_dict)
        format['cont'] = 'DAY'
        list1.append(format)

#时间状态，如13：00
class time_fsm(base_fsm):
    def __init__(self):
        self.state_str = 'time_fsm'
        self.char_dict = {}
        #－:\uFF0D
        self.char_dict[u'\u002D'] = 'time_2_fsm'
        self.char_dict[u'\u007E'] = 'time_2_fsm'
        self.char_dict[u'\uFF0D'] = 'time_2_fsm'
        self.state_dict = {}
        self.state_dict['DAY'] = 'start_fsm'
        self.state_dict['TIME'] = 'start_fsm'
        self.state_dict['DAY_DAY'] = 'start_fsm'
        self.state_dict['TIME_TIME'] = 'start_fsm'
        self.state_dict['ALL_ALL'] = 'start_fsm'
    def enter_state(self, obj):
        self.data = obj
    def exit_state(self, tmp_dict):
        tmp_dict.append(self.data)
    def stop_state(self, list1, tmp_dict):
        tmp_dict.append(self.data)
        format = self.get_format_point(tmp_dict)
        format['cont'] = 'TIME'
        list1.append(format)
            
class day_time_2_fsm(base_fsm):
    def __init__(self):
        self.state_str = 'day_time_2_fsm'
        self.char_dict = {}
        self.state_dict = {}
        self.state_dict['DAY_TIME'] = 'all_all_fsm'
        self.state_dict['TIME'] = 'all_all_fsm'
    def enter_state(self, obj):
        self.data = obj
    def exit_state(self, tmp_dict):
        tmp_dict.append(self.data)
    def stop_state(self, list1, tmp_dict):
        format = self.get_format_point(tmp_dict)
        format['cont'] = 'DAY_TIME'
        list1.append(format)

class day_time_fsm(base_fsm):
    def __init__(self):
        self.state_str = 'day_time_fsm'
        self.char_dict = {}
        self.state_dict = {}
        self.state_dict['QU_JIAN'] = 'day_time_2_fsm'
        #~:\u007E ～:\uFF5E -:\u002D
    def re_init(self):
        self.char_dict[u'\u007E'] = 'day_time_2_fsm'
        self.char_dict[u'\uFF5E'] = 'day_time_2_fsm'
        self.char_dict[u'\u002D'] = 'day_time_2_fsm'
    def reset(self):
        self.char_dict[u'\u007E'] = 'start_fsm'
        self.char_dict[u'\uFF5E'] = 'start_fsm'
        self.char_dict[u'\u002D'] = 'start_fsm'
    def enter_state(self, obj):
        self.data = obj
    def exit_state(self, tmp_dict):
        tmp_dict.append(self.data)
    def stop_state(self, list1, tmp_dict):
        format = self.get_format_point(tmp_dict)
        format['cont'] = 'DAY_TIME'
        list1.append(format)
#日期状态，如1987-12-28
class day_2_fsm(base_fsm):
    def __init__(self):
        self.state_str = 'day_2_fsm'
        self.char_dict = {}
        self.state_dict = {}
        self.state_dict['DAY'] = 'day_day_fsm'
        self.state_dict['TIME'] = 'day_time_fsm'
        self.state_dict['TIME_TIME'] = 'all_all_fsm'
    def enter_state(self, obj):
        self.data = obj
    def exit_state(self, tmp_dict):
        tmp_dict.append(self.data)
    def stop_state(self, list1, tmp_dict):
        format = self.get_format_point(tmp_dict)
        format['cont'] = 'DAY'
        list1.append(format)
class day_day_fsm(base_fsm):
    def __init__(self):
        self.state_str = 'day_day_fsm'
        self.char_dict = {}
        #每：\u6BCF
        self.char_dict[u'\u6BCF'] = 'start_fsm'
        self.state_dict = {}
        self.state_dict['MEI_TIAN'] = 'day_day_fsm'
    def reset(self):
        self.state_dict['MEI_ZHOU'] = 'start_fsm'
        self.state_dict['TIME_TIME'] = 'start_fsm'
        self.state_dict['TIME'] = 'start_fsm'
    def re_init(self):
        self.state_dict['MEI_ZHOU'] = 'mei_day_fsm'
        self.state_dict['TIME_TIME'] = 'all_set_fsm'
        self.state_dict['TIME'] = 'all_set_fsm'
    def enter_state(self, obj):
        self.data = obj
    def exit_state(self, tmp_dict):
        tmp_dict.append(self.data)
    def stop_state(self, list1, tmp_dict):
        tmp_dict.append(self.data)
        format = self.get_format_dur(tmp_dict)
        format['cont'] = 'DAY_DAY'
        list1.append(format)
class time_time_fsm(base_fsm):
    def __init__(self):
        self.state_str = 'time_time_fsm'
        self.char_dict = {}
        #每：\u6BCF
        self.char_dict[u'\u6BCF'] = 'start_fsm'
        self.state_dict = {}
    def reset(self):
        self.state_dict['DAY'] = 'start_fsm'
    def re_init(self):
        self.state_dict['DAY'] = 'all_all_fsm'
    def enter_state(self, obj):
        self.data = obj
    def exit_state(self, tmp_dict):
        tmp_dict.append(self.data)
    def stop_state(self, list1, tmp_dict):
        tmp_dict.append(self.data)
        format = self.get_format_dur(tmp_dict)
        format['cont'] = 'TIME_TIME'
        list1.append(format)

class all_all_fsm(base_fsm):
    def __init__(self):
        self.state_str = 'all_all_fsm'
        self.char_dict = {}
        self.state_dict = {}
    def enter_state(self, obj):
        self.data = obj
    def exit_state(self, tmp_dict):
        tmp_dict.append(self.data)
    def stop_state(self, list1, tmp_dict):
        format = self.get_format_all_all(tmp_dict)
        if len(format) > 0:
            format['cont'] = 'ALL_ALL'
            list1.append(format)

class all_set_fsm(base_fsm):
    def __init__(self):
        self.state_str = 'all_set_fsm'
        self.char_dict = {}
        self.state_dict = {}
    def enter_state(self, obj):
        self.data = obj
    def exit_state(self, tmp_dict):
        tmp_dict.append(self.data)
    def stop_state(self, list1, tmp_dict):
        format = self.get_format_all_all(tmp_dict)
        if len(format) > 0:
            format['cont'] = 'ALL_SET'
            list1.append(format)
class time_2_fsm(base_fsm):
    def __init__(self):
        self.state_str = 'time_2_fsm'
        self.char_dict = {}
        self.state_dict = {}
        self.state_dict['TIME'] = 'time_time_fsm'
    def enter_state(self, obj):
        self.data = obj
    def exit_state(self, tmp_dict):
        tmp_dict.append(self.data)
    def stop_state(self, list1, tmp_dict):
        tmp_dict.append(self.data)
        format = self.get_format_point(tmp_dict)
        format['cont'] = 'TIME'
        list1.append(format)
#管理所有的状态
class FsmMgr():
    def __init__(self):
        self._fsms = {}
        self._fsms['start_fsm'] = start_fsm()
        self._fsms['day_fsm'] = day_fsm()
        self._fsms['time_fsm'] = time_fsm()
        self._fsms['day_time_fsm'] = day_time_fsm()
        self._fsms['day_day_fsm'] = day_day_fsm()
        self._fsms['day_2_fsm'] = day_2_fsm()
        self._fsms['time_2_fsm'] = time_2_fsm()
        self._fsms['time_time_fsm'] = time_time_fsm()
        self._fsms['all_all_fsm'] = all_all_fsm()
        self._fsms['all_set_fsm'] = all_set_fsm()
        self._fsms['mei_fsm'] = mei_fsm()
        self._fsms['mei_tian_fsm'] = mei_tian_fsm()
        self._fsms['mei_yue_fsm'] = mei_yue_fsm()
        self._fsms['mei_zhou_fsm'] = mei_zhou_fsm()
        self._fsms['mei_time_fsm'] = mei_time_fsm()
        self._fsms['mei_day_fsm'] = mei_day_fsm()
        self._fsms['mei_all_fsm'] = mei_all_fsm()
        self._fsms['qu_jian_fsm'] = qu_jian_fsm()
        self._fsms['day_time_2_fsm'] = day_time_2_fsm()
        self._cur_state = self._fsms['start_fsm'] 

    def reset(self):
        for i in self._fsms:
            self._fsms[i].reset()
        self._fsms['mei_yue_fsm'].reset()
        self._fsms['mei_zhou_fsm'].reset()
        self._fsms['mei_tian_fsm'].reset()
    def re_init(self):
        for i in self._fsms:
            self._fsms[i].re_init()
        self._fsms['mei_yue_fsm'].re_init()
        self._fsms['mei_zhou_fsm'].re_init()
        self._fsms['mei_tian_fsm'].re_init()
    def get_fsm(self, state):
        return self._fsms[state]

#根据当前状态，以及下一个输入，得到新状态并返回
    def frame(self, state, list1, tmp_dict):
        next_state = ''
        next_state = self._cur_state.exec_state(state)
        if self.get_fsm(next_state) != self._cur_state:
            #跳转到下一状态，当前状态保存在tmp_dict
            self._cur_state.exit_state(tmp_dict)
            if next_state is 'start_fsm':
                #下一状态为一新开始，则结束上一个状态，总结出内容并保存
                self._cur_state.stop_state(list1, tmp_dict)
                del tmp_dict[:]
                self._cur_state = self.get_fsm(next_state)  
                next_state = self._cur_state.exec_state(state)
            #更新新状态
            self._cur_state = self.get_fsm(next_state)
            self._cur_state.enter_state(state)
    def stop_frame(self, list1, tmp_dict):     
        self._cur_state.exit_state(tmp_dict) 
        self._cur_state.stop_state(list1, tmp_dict) 
        self._cur_state = self._fsms['start_fsm']
        del tmp_dict[:]
            
#总驱动，根据原串，使状态转换
class TimeFsm():
    def __init__(self):
        self._fsm_mgr = FsmMgr()
        #到：\u5230 至：\u81F3
        self.trans_dict = {u'\u5230':u'\u002D', u'\u81F3':u'\u002D', u'\u007E':u'\u002D', u'\uFF0D':u'\u002D', u'\u2014':u'\u002D', u'\uFF5E':u'\u002D', u'\u002D':u'\u002D', u'\u2013':u'\u002D', u'\u2015':u'\u002D'}
        #保留字典，如果是下面这些汉字，则不进行正则匹配
        #上：\u4E0A 下:\u4E0B 晚：\u665A
        self.keep_dict = {u'\u4E0A':1, u'\u4E0B':1, u'\u665A':1,}
        self.mine_time = mine_time.MineTime()
    def empty_dict(sefl):
        dict = {}
        dict['year_s'] = 'XXXX'
        dict['year_e'] = 'XXXX'
        dict['mon_s'] = 'XX' 
        dict['mon_e'] = 'XX' 
        dict['day_s'] = 'XX' 
        dict['day_e'] = 'XX' 
        dict['hour_s'] = 'XX' 
        dict['hour_e'] = 'XX' 
        dict['min_s'] = 'XX' 
        dict['min_e'] = 'XX' 
        dict['sec_s'] = 'XX' 
        dict['sec_e'] = 'XX' 
        dict['cond']= ''
        dict['cond_str']= ''
        dict['cond_cont'] = []
        dict['after_s'] = 'XX'
        dict['after_e'] = 'XX'
        return dict

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
            ret_str = year_s + '-' + mon_s + '-' + day_s + ' ' + hour_s + ':' + min_s + ':' + sec_s  + ' ~ ' + year_e + '-' + mon_e + '-' + day_e + ' ' + hour_e + ':' + min_e + ':' + sec_e
        else:
            ret_str = year_s + '-' + mon_s + '-' + day_s + ' ~ ' + year_e + '-' + mon_e + '-' + day_e + '  ' + hour_s + ':' + min_s + ':' + sec_s  + ' ~ ' + hour_e + ':' + min_e + ':' + sec_e 
        ret_str = ret_str + ' ('
        for i in res['cond_cont']:
            ret_str = ret_str + ' ' + i + ' '
        ret_str = ret_str + ')'
        return ret_str

    def is_skip(self, uchar):
        if self.is_chinese(uchar) and uchar not in self.keep_dict:
            return True
        else:
            return False

    def is_chinese(self, uchar):
        """判断一个unicode是否是汉字"""
        if uchar >= u'\u4e00' and uchar<=u'\u9fa5':
            return True
        else:
            return False 
    def begin(self, o_str):
        ret_str = '' 
        self._fsm_mgr.reset()
        #_fsm_mgr = FsmMgr()
        list1 = []
        tmp_dict = [] 
        process_str = o_str 
        while (len(process_str) > 0):
            cur_data = self.empty_dict() 
            if process_str[0] is ' ' or process_str[0] == u'\u0020' :
                process_str = process_str[1:] 
                continue
            flag = 0
            one_char = ''
            out = {}
            if self.trans_dict.has_key(process_str[0]):
                one_char = self.trans_dict[process_str[0]]
            elif self.is_skip(process_str[0]):
                #命中这部分的就不会走正则
                pass
            else:
                flag,pos,out = self.mine_time.process(process_str)
            if flag == 0:
                cur_data['data'] = process_str[0]
                cur_data['cont'] = 'null'
                cur_str = process_str[0]
                split = 1
                if process_str[0].isdigit():
                    for i in range(1, len(process_str)):
                        if process_str[i].isdigit():
                            cur_str += process_str[i]
                        else:
                            split = i
                            break
                cur_data['char'] = cur_str 
                if len(one_char) > 0:
                    cur_data['char'] = one_char
                ret = self._fsm_mgr.frame(cur_data, list1, tmp_dict) 
                #ret = _fsm_mgr.frame(cur_data, list1, tmp_dict) 
                process_str = process_str[split:]
            else:
                #晚：\u665A   下：\u4E0B
                if out['after_s'] == u'\u665A' or out['after_s'] == u'\u4E0B':
                    out['after_s'] = 'afternoon'
                else:
                    out['after_s'] = 'XX'
                if out['after_e'] == u'\u665A' or out['after_e'] == u'\u4E0B':
                    out['after_e'] = 'afternoon'
                else:
                    out['after_e'] = 'XX'
                cur_data = out
                cur_data['state'] = 'unit'
                ret = self._fsm_mgr.frame(cur_data, list1, tmp_dict)
                #ret = _fsm_mgr.frame(cur_data, list1, tmp_dict)
                process_str = process_str[pos[1]+1:]
        self._fsm_mgr.stop_frame(list1, tmp_dict)    
        #_fsm_mgr.stop_frame(list1, tmp_dict)    
        self._fsm_mgr.re_init()
        #_fsm_mgr.re_init()
        list2 = []
        for i in list1:
            #str = self.dict2str(i)
            ret = self._fsm_mgr.frame(i, list2, tmp_dict)
            #ret = _fsm_mgr.frame(i, list2, tmp_dict)
        self._fsm_mgr.stop_frame(list2, tmp_dict)
        #_fsm_mgr.stop_frame(list2, tmp_dict)
        ret_list =[] 
        for i in list2:
            self.make_comp(i)
            if i['cont'] is 'MEI_YUE':
                if len(list2) == 1:
                    i['cond_cont'].append('MEI_YUE')
                else:
                    continue
            if i['cont'] is 'MEI_TIAN':
                if len(list2) == 1:
                    i['cond_cont'].append('MEI_TIAN')
                else:
                    continue
            if i['cont'] is 'MEI_ZHOU':
                if len(list2) == 1:
                    i['cond_cont'].append('MEI_ZHOU')
                else:
                    continue
            ret_list.append(i)
            tmp_str = self.dict2str(i)
            ret_str = ret_str + tmp_str
        #return ret_str
        return ret_list
    def make_comp(self, i):
        if i['cont'] is 'ALL_ALL' or i['cont'] is 'DAY_DAY':
            i['year_s'], i['year_e'] = self.make_same(i['year_s'], i['year_e'])
            i['mon_s'], i['mon_e'] = self.make_same(i['mon_s'], i['mon_e'])
            i['day_s'], i['day_e'] = self.make_same(i['day_s'], i['day_e'])
        i['after_s'], i['after_e'] = self.make_same(i['after_s'], i['after_e'])
    def make_same(self,s,e):
        if 'XX' in s and 'XX' not in e:
            s = e
        if 'XX' in e and 'XX' not in s:
            e = s
        return s,e

if __name__ == "__main__":
    print 'begin'
    timefsm = TimeFsm()
    f_input = open("time.txt", 'r')
    output_file = open("out.txt", 'w+')
    try:
        while True:
            list_uline = []
            line = f_input.readline()
            line = line.strip()
            if len(line) == 0:
                break;
            uline = unicode(line, 'utf8') 
            ret = timefsm.begin(uline) 
#           output_file.write(uline.encode('GBK') + '\t')
#           output_file.write(ret.encode('GBK'))
            output_file.write(line + '\t')
            #output_file.write(ret.encode('utf-8'))
            print ret
            output_file.write('\n')
            output_file.flush()
    finally:
        f_input.close()
        output_file.close()


