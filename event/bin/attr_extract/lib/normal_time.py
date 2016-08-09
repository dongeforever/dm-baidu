#!/usr/bin/env python
#coding=utf-8

# Time-stamp: <2014-11-17 22:33:08 >

# @version 1.0
# @author shaoyuanhua shaoyuanhua@baidu.com  
import re
import string
import Queue
import mine_time 
import traceback

class Time:
    def make_same(self,s,e):
        if 'XX' in s and 'XX' not in e:
            s = e
        if 'XX' in e and 'XX' not in s:
            e = s
        return s,e
    def process_dur(self,list_time,dict):
        ret_str =''
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
        cond_cont=[]
        for i in range(0, len(list_time)):
            if list_time[i][1]['cont'] == 'Dur_ALL_S':
                year_s = list_time[i][1]['year']
                mon_s = list_time[i][1]['mon']
                day_s = list_time[i][1]['day']
                hour_s = list_time[i][1]['hour']
                min_s = list_time[i][1]['min']
                sec_s = list_time[i][1]['sec']
                dict['year_s'] = list_time[i][1]['year']
                dict['mon_s'] = list_time[i][1]['mon']
                dict['day_s'] = list_time[i][1]['day']
                dict['hour_s'] = list_time[i][1]['hour']
                dict['min_s'] = list_time[i][1]['min']
                dict['sec_s'] = list_time[i][1]['sec']
            if list_time[i][1]['cont'] == 'Dur_ALL_E':
                dict['year_e'] = list_time[i][1]['year']
                dict['mon_e'] = list_time[i][1]['mon']
                dict['day_e'] = list_time[i][1]['day']
                dict['hour_e'] = list_time[i][1]['hour']
                dict['min_e'] = list_time[i][1]['min']
                dict['sec_e'] = list_time[i][1]['sec']
            if list_time[i][1]['cont'] == 'Dur_DAY_S':
                dict['year_s'] = list_time[i][1]['year']
                dict['mon_s'] = list_time[i][1]['mon']
                dict['day_s'] = list_time[i][1]['day']
            if list_time[i][1]['cont'] == 'Dur_DAY_E':
                dict['year_e'] = list_time[i][1]['year']
                dict['mon_e'] = list_time[i][1]['mon']
                dict['day_e'] = list_time[i][1]['day']
            if list_time[i][1]['cont'] == 'DAY' and year_s == 'XXXX' and mon_s == 'XX' and day_s == 'XX':
                dict['year_s'] = list_time[i][1]['year']
                dict['mon_s'] = list_time[i][1]['mon']
                dict['day_s'] = list_time[i][1]['day']
            if list_time[i][1]['cont'] == 'DAY' and year_e == 'XXXX' and mon_e == 'XX' and day_e == 'XX':
                dict['year_e'] = list_time[i][1]['year']
                dict['mon_e'] = list_time[i][1]['mon']
                dict['day_e'] = list_time[i][1]['day']
            if list_time[i][1]['cont'] == 'Dur_TIME_S':
                dict['hour_s'] = list_time[i][1]['hour']
                dict['min_s'] = list_time[i][1]['min']
                dict['sec_s'] = list_time[i][1]['sec']
            if list_time[i][1]['cont'] == 'Dur_TIME_E':
                dict['hour_e'] = list_time[i][1]['hour']
                dict['min_e'] = list_time[i][1]['min']
                dict['sec_e'] = list_time[i][1]['sec']
            if list_time[i][1]['cont'] == 'TIME' and hour_s == 'XX' and min_s == 'XX' and sec_s == 'XX':
                dict['hour_s'] = list_time[i][1]['hour']
                dict['min_s'] = list_time[i][1]['min']
                dict['sec_s'] = list_time[i][1]['sec']
            if list_time[i][1]['cont'] == 'TIME' and hour_e == 'XX' and min_e == 'XX' and sec_e == 'XX':
                dict['hour_e'] = list_time[i][1]['hour']
                dict['min_e'] = list_time[i][1]['min']
                dict['sec_e'] = list_time[i][1]['sec']
        return '' 
    def process_set(self, list_time, dict):
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
        cond_cont = []
        for i in range(0, len(list_time)):
            if list_time[i][1]['cont'] == 'DUR':
                dict['cond'] = list_time[i][1]['cond_cont']
            if list_time[i][1]['cont'] == 'Dur_ALL_S':
                dict['year_s'] = list_time[i][1]['year']
                dict['mon_s'] = list_time[i][1]['mon']
                dict['day_s'] = list_time[i][1]['day']
                dict['hour_s'] = list_time[i][1]['hour']
                dict['min_s'] = list_time[i][1]['min']
                dict['sec_s'] = list_time[i][1]['sec']
            if list_time[i][1]['cont'] == 'Dur_ALL_E':
                dict['year_e'] = list_time[i][1]['year']
                dict['mon_e'] = list_time[i][1]['mon']
                dict['day_e'] = list_time[i][1]['day']
                dict['hour_e'] = list_time[i][1]['hour']
                dict['min_e'] = list_time[i][1]['min']
                dict['sec_e'] = list_time[i][1]['sec']
            if list_time[i][1]['cont'] == 'Dur_DAY_S':
                dict['year_s'] = list_time[i][1]['year']
                dict['mon_s'] = list_time[i][1]['mon']
                dict['day_s'] = list_time[i][1]['day']
            if list_time[i][1]['cont'] == 'Dur_DAY_E':
                dict['year_e'] = list_time[i][1]['year']
                dict['mon_e'] = list_time[i][1]['mon']
                dict['day_e'] = list_time[i][1]['day']
            if list_time[i][1]['cont'] == 'DAY' and year_s == 'XXXX' and mon_s == 'XX' and day_s == 'XX':
                dict['year_s'] = list_time[i][1]['year']
                dict['mon_s'] = list_time[i][1]['mon']
                dict['day_s'] = list_time[i][1]['day']
            if list_time[i][1]['cont'] == 'DAY' and year_e == 'XXXX' and mon_e == 'XX' and day_e == 'XX':
                dict['year_e'] = list_time[i][1]['year']
                dict['mon_e'] = list_time[i][1]['mon']
                dict['day_e'] = list_time[i][1]['day']
            if list_time[i][1]['cont'] == 'Dur_TIME_S':
                dict['hour_s'] = list_time[i][1]['hour']
                dict['min_s'] = list_time[i][1]['min']
                dict['sec_s'] = list_time[i][1]['sec']
            if list_time[i][1]['cont'] == 'Dur_TIME_E':
                dict['hour_e'] = list_time[i][1]['hour']
                dict['min_e'] = list_time[i][1]['min']
                dict['sec_e'] = list_time[i][1]['sec']
            if list_time[i][1]['cont'] == 'TIME' and hour_s == 'XX' and min_s == 'XX' and sec_s == 'XX':
                dict['hour_s'] = list_time[i][1]['hour']
                dict['min_s'] = list_time[i][1]['min']
                dict['sec_s'] = list_time[i][1]['sec']
            if list_time[i][1]['cont'] == 'TIME' and hour_e == 'XX' and min_e == 'XX' and sec_e == 'XX':
                dict['hour_e'] = list_time[i][1]['hour']
                dict['min_e'] = list_time[i][1]['min']
                dict['sec_e'] = list_time[i][1]['sec']
        dict['year_s'],dict['year_e'] = self.make_same(dict['year_s'], dict['year_e'])
        dict['mon_s'],dict['mon_e'] = self.make_same(dict['mon_s'],dict['mon_e'])
        dict['day_s'],dict['day_e'] = self.make_same(dict['day_s'],dict['day_e'])
        dict['hour_s'],dict['hour_e'] = self.make_same(dict['hour_s'],dict['hour_e'])
        dict['min_s'],dict['min_e'] = self.make_same(dict['min_s'],dict['min_e'])
        dict['sec_s'], dict['sec_e'] = self.make_same(dict['sec_s'], dict['sec_e'])
        return '' 
    def process_point(self, list_time, dict):
        ret_str = ''
        for i in range(0, len(list_time)):
            if list_time[i][1]['cont'] == 'DAY':
                dict['year_s'] = list_time[i][1]['year']
                dict['mon_s'] = list_time[i][1]['mon']  
                dict['day_s'] = list_time[i][1]['day']  
                continue
            if list_time[i][1]['cont'] == 'TIME':
                dict['hour_s'] = list_time[i][1]['hour']
                dict['min_s'] = list_time[i][1]['min']  
                dict['sec_s'] = list_time[i][1]['sec']  
                continue
            if list_time[i][1]['cont'] == 'ALL':
                dict['year_s'] = list_time[i][1]['year']
                dict['mon_s'] = list_time[i][1]['mon']  
                dict['day_s'] = list_time[i][1]['day']  
                dict['hour_s'] = list_time[i][1]['hour']
                dict['min_s'] = list_time[i][1]['min']  
                dict['sec_s'] = list_time[i][1]['sec']  
                continue
        return '' 

    def unite_time(self, list_time, line):
        time_num = 0
        is_dur_time = 0
        is_dur_day = 0
        is_same_day = 0
        is_dur_all = 0
        is_dur_freq = 0
        is_set = 0
        for i in range(0, len(list_time)):
            j = i + 1
            while(1):
                if j >= len(list_time):
                    break
                #DUR与FREQ合并
                if list_time[i][1]['cont'] == 'DUR' and list_time[j][1]['cont'] == 'FREQ':
                    for ii in list_time[j][1]['cond_cont']:
                        list_time[i][1]['cond_cont'].append(ii)
                    del list_time[j]
                    continue
                elif list_time[i][1]['cont'] != 'DUR' and list_time[j][1]['cont'] == 'FREQ':
                    del list_time[j]
                    continue
                else:
                    break

        for i in range(0, len(list_time)):
            j = i + 1
            if j < len(list_time):
                if list_time[i][1]['cont'] == 'DAY' and list_time[j][1]['cont'] == 'DAY' and list_time[i][1]['site2'] < list_time[j][1]['site1']:
                    if list_time[i][1]['site2'] +1  == list_time[j][1]['site1']-1:
                        dis_line = line[list_time[i][1]['site2']+1]
                    else:
                        dis_line = line[list_time[i][1]['site2']+1:list_time[j][1]['site1']-1]
                    new_dis = dis_line.replace(' ','')
                    new_dis = new_dis.replace(',','')
                    new_dis = new_dis.replace('\n','')
                    if len(new_dis) > 0:
                        if list_time[i][1]['year'] == list_time[j][1]['year'] and list_time[i][1]['mon'] == list_time[j][1]['mon']  and list_time[i][1]['day'] == list_time[j][1]['day']:
                            del list_time[j]
                        else:
                            list_time[i][1]['cont'] = 'Dur_DAY_S'
                            list_time[j][1]['cont'] = 'Dur_DAY_E'
                            is_dur_day = 1
                            i = j
                        continue
                if list_time[i][1]['cont'] == 'TIME' and list_time[j][1]['cont'] == 'TIME' and list_time[i][1]['site2'] < list_time[j][1]['site1']:
                    if list_time[i][1]['site2'] +1  == list_time[j][1]['site1']-1:
                        dis_line = line[list_time[i][1]['site2']+1]
                    else:
                        dis_line = line[list_time[i][1]['site2']+1:list_time[j][1]['site1']-1]
                    #table = string.maketrans('\t\n\u0020\u002c ','')
                    #new_dis = dis_line.translate(table)
                    new_dis = dis_line.replace(' ','')
                    new_dis = new_dis.replace(',','')
                    new_dis = new_dis.replace('\n','')
                    if len(new_dis) > 0:
                        list_time[i][1]['cont'] = 'Dur_TIME_S'
                        list_time[j][1]['cont'] = 'Dur_TIME_E'
                        if list_time[i][1]['after'] == 'after':
                            list_time[j][1]['after'] = 'after'
                        is_dur_time = 1
                        i = j
                    
        for i in range(0, len(list_time)):
            j = i + 1
            if j < len(list_time):
                if list_time[i][1]['cont'] == 'DAY' and list_time[j][1]['cont'] == 'TIME':
                    list_time[i][1]['cont'] = 'ALL'
                    list_time[j][1]['cont'] = 'none'
                    list_time[i][1]['hour'] = list_time[j][1]['hour'] 
                    list_time[i][1]['min'] = list_time[j][1]['min'] 
                    list_time[i][1]['sec'] = list_time[j][1]['sec'] 
                    list_time[i][1]['site2'] = list_time[j][1]['site2']
                    del list_time[j]
                continue
        for i in range(0, len(list_time)):
            j = i + 1
            if j < len(list_time):
                if list_time[i][1]['cont'] == 'ALL' and list_time[j][1]['cont'] == 'ALL' and list_time[i][1]['site2'] < list_time[j][1]['site1']:
                    if list_time[i][1]['site2'] +1  == list_time[j][1]['site1']-1:
                        dis_line = line[list_time[i][1]['site2']+1]
                    else:
                        dis_line = line[list_time[i][1]['site2']+1:list_time[j][1]['site1']-1]
                    new_dis = dis_line.replace(' ','')
                    new_dis = new_dis.replace(',','')
                    new_dis = new_dis.replace('\n','')
                    if len(new_dis) > 0:
                        list_time[i][1]['cont'] = 'Dur_ALL_S'
                        list_time[j][1]['cont'] = 'Dur_ALL_E'
                        is_dur_all = 1
                        i = j
                        continue
        for i in range(0, len(list_time)):
            #下\u4E0B
            #print list_time[i][1]['after'].encode('utf8')
            if list_time[i][1]['after'] == u'\u4e0b':
                h = int(list_time[i][1]['hour']) 
                if h < 12 and h > 0:
                    list_time[i][1]['hour'] = str(h+12)
            #晚\u665A
            if list_time[i][1]['after'] == u'\u665a':
                h = int(list_time[i][1]['hour']) 
                if h < 12 and h > 3:
                    list_time[i][1]['hour'] = str(h+12)
                    
            if list_time[i][1]['cont'] == 'ALL' or list_time[i][1]['cont'] == 'DAY' or list_time[i][1]['cont'] == 'TIME':
                time_num += 1
                continue
            if list_time[i][1]['cont'] == 'DUR':
                is_dur_freq = 1
            if list_time[i][1]['cont'] == 'Dur_DAY_S':
                is_dur_day = 1
            if list_time[i][1]['cont'] == 'Dur_TIME_S':
                is_dur_time = 1
            if list_time[i][1]['cont'] == 'Dur_DAY_S' or list_time[i][1]['cont'] == 'Dur_TIME_S': 
                j = i + 2
                time_num += 1
                if j < len(list_time) and ( list_time[j][1]['cont'] == 'Dur_DAY_S' or list_time[j][1]['cont'] == 'Dur_TIME_S') and list_time[j][1]['cont'] != list_time[i][1]['cont']:
                    i = i+3
                else:
                    i = i+1
                continue
            if list_time[i][1]['cont'] == 'Dur_ALL_S' or list_time[i][1]['cont'] == 'Dur_ALL_S':
                time_num += 1
                i = i+1
                continue
        is_dur = {}
        is_dur['is_dur_time'] = is_dur_time
        is_dur['is_dur_day'] = is_dur_day 
        is_dur['is_same_day'] = is_same_day 
        is_dur['is_dur_all'] = is_dur_all 
        if (is_dur_time == 1 and is_dur_day == 1 and is_same_day == 0) or is_dur_freq > 0:
            is_set = 1
        is_dur['is_set'] = is_set
        #print 'is_dur_time:%d is_dur_day:%d is_same_day:%d is_dur_all:%d is_set:%d time_num:%d)'%(is_dur_time,is_dur_day,is_same_day,is_dur_all,is_set, time_num)
        #print list_time
        return is_dur,list_time

    def new_dict(self):
        dict = {}
        dict['year_s'] = ''
        dict['year_e'] = ''
        dict['mon_s'] = '' 
        dict['mon_e'] = '' 
        dict['day_s'] = '' 
        dict['day_e'] = '' 
        dict['hour_s'] = '' 
        dict['hour_e'] = '' 
        dict['min_s'] = '' 
        dict['min_e'] = '' 
        dict['sec_s'] = '' 
        dict['sec_e'] = '' 
        dict['cond']= ''
        return dict


    def get_time(self,line):
        print 'begin get_time:', line.encode('utf-8')
        #output_file = open('middle.txt' , 'a+')
        try:
            queue = Queue.Queue()
            site = Queue.Queue()
            out = ""
            line = line.strip()
            if len(line) == 0:
                return {} 
            #code_line = unicode(line, 'utf8')
            #queue.put(code_line)
            queue.put(line)
            site.put(0)
            ret_time = {}
            while queue.empty() == False:
                one_line = queue.get()
                one_site = site.get()
                flag,pos,out = mine_time.process(one_line)	
                if flag == 0:
                    continue
                if pos[0] > 0:
                    queue.put(one_line[0:pos[0]])
                    site.put(one_site)
                if pos[1] < len(one_line) - 1:
                    queue.put(one_line[pos[1]+1:])
                    site.put(one_site + pos[1]+1)
                site1 = pos[0] + one_site
                site2 = pos[1] + one_site
                for x in range(0,len(out)):
                    out[x]['site1'] = site1
                    out[x]['site2'] = site2
                    site1 += 1
                    key = out[x]['site1']
                    ret_time[key] = out[x]
            sort_out = sorted(ret_time.items(), key=lambda ret_time:ret_time[0])
            if len(sort_out) < 1:
                return {}
            ret_str = ''
            ret_dict = self.new_dict()
            is_dur,ret_time = self.unite_time(sort_out, line) 
            if len(ret_time) > 0:
                if is_dur['is_set'] == 1:
                    ret_str = self.process_set(ret_time, ret_dict)
                elif is_dur['is_dur_time'] == 1 or is_dur['is_dur_day'] == 1 or is_dur['is_dur_all']:
                    ret_str = self.process_dur(ret_time, ret_dict)
                else:
                    ret_str = self.process_point(ret_time, ret_dict)
            #output_file.write(ret_str +'\n')
            #output_file.flush()    
            return ret_dict 
        except:
            print 'time except'
            traceback.print_exc()
            return {} 
