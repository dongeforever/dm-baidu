#!/usr/bin/env python
#coding=utf-8
import random
import sys
import re

class MineTime():
    def __init__(self):
        self.str1 = u'^(?:(?P<YEAR>\d{2,4})[\u0020]?\u5E74[\u0020]?)?(?:(?P<MON>\d{1,2})[\u0020]?\u6708[\u0020]?)(?:(?P<DAY>\d{1,2})[\u0020]?[\u65E5\u53F7]?)?'
        self.str5 = u'^(?:(?:(?P<YEAR>\d{2,4})[\u0020]?\u5E74)|(?:(?P<MON>\d{1,2})[\u0020]?\u6708)|(?:(?P<DAY>(?:[1-2][0-9]|3[0-1]|0?[1-9]))[\u0020]?[\u65E5\u53F7]))'
        #self.str5 = u'^(?:(?:(?P<YEAR>\d{2,4})[\u0020]?\u5E74)|(?:(?P<MON>\d{1,2})[\u0020]?\u6708)|(?:(?P<DAY>\d{1,2})[\u0020]?[\u65E5\u53F7]{1,2}))'
        #年-月-日
        self.str2 = r'^(?:(?P<YEAR>[0-2]?[0-9]?[0-9]{2})(?P<biaohao>\D{1,3})(?P<MON>0?[1-9]|1[0-2])(?P=biaohao)(?P<DAY>(?:[1-2][0-9]|3[0-1]|0?[1-9])))'
        #月-日 午\u5348 晚\u665A 上\u4E0A
        #月：\u6708 MON与DAY之间不能有除了'月’之外的汉字
        self.str3 = u'^(?:(?P<MON>0?[1-9]|1[0-2])[^\u4e00-\u6707\u6709-\u9fa5\u003A\uFF1A0-9](?P<DAY>[1-2][0-9]|3[0-1]|0?[1-9]))'
        #str3 = u'^(?:(?P<MON>0?[1-9]|1[0-2])\D{1,3}[^\u003A\uFF1A0-9](?P<DAY>[1-2][0-9]|3[0-1]|0?[1-9]))'
        #年-月
        self.str4 = u'^(?:(?P<YEAR>[0-2][0-9]{3})[^\u4e00-\u9fa5](?P<MON>0?[1-9]|1[0-2]))\D'
        #str4 = r'^(?:(?P<YEAR>[0-2][0-9]{3})\D{1,3}(?P<MON>0?[1-9]|1[0-2]))\D'
        #时 点:\u70B9 点钟
        self.time1 = u'^(?:(?:(?P<AFTERNOON>[\u4E0A\u4E0B\u665A])[\u5348\u4E0A]?\D{0,3})?[\u0020]?(?P<HOUR>0?[0-9]|1[0-9]|2[0-4])[\u0020]?(?:\u65F6|\u70B9|\u70B9\u949F)(?:(?P<MIN>[0-6]?[0-9])(?:\D{1,3})?(?P<SEC>[0-6]?[0-9])?)?)'
        #\u5348 午 晚 \u665A 上下\u4E0A\u4E0B
        #time4 = u'(?P<wu>[\u4E0A\u4E0B\u665A])[\u5348\u4E0A]\D{1,3}(?:(?P<HOUR>0?[0-9]|1[0-9]|2[0-4])(?P<biaohao>\D{1,3})(?P<MIN>[0-6]?[0-9])(?:(?P=biaohao)(?P<SEC>[0-6]?[0-9]))?)?'
        #.:\u002E
        self.time4 = u'^(?:(?P<AFTERNOON>[\u4E0A\u4E0B\u665A])[\u5348\u4E0A]?\D{0,3})?[\u0020]?(?P<HOUR>0?[0-9]|1[0-9]|2[0-4])(?:[^\d\u002E]{1,3}(?P<MIN>[0-6]?[0-9]))?[\u0020]?[-—]{1,}[\u0020]?(?P<HOUR1>0?[0-9]|1[0-9]|2[0-4])(?:[^\d\u002E]{1,3}(?P<MIN1>[0-6]?[0-9]))?(?:$|\D)'
        #上：\u4E0B 下：\u4E0A 午：\u5348 晚：\u665A
        self.time2 = u'^(?:(?P<AFTERNOON>[\u4E0A\u4E0B\u665A])[\u5348\u4E0A]?[\u0020]?\D{0,3})?[\u0020]?((?P<HOUR>0?[0-9]|1[0-9]|2[0-4])(?P<biaohao>\u003A|\uFF1A)(?P<MIN>[0-6]?[0-9])(?:(?P=biaohao)(?P<SEC>[0-6]?[0-9]))?)'
        #到：\u5230 至：\u81F3 、:\u3001
        self.time3 = u'^(?:(?P<AFTERNOON>[\u4E0A\u4E0B\u665A])[\u5348\u4E0A]?\D{0,3})?[\u0020]?(?:(?P<HOUR>0?[0-9]|1[0-9]|2[0-4])(?P<biaohao>[^\u4e00-\u9fa5\d\u5230\u81F3\u3001-]{1,3})(?P<MIN>[0-6]?[0-9])(?:(?P=biaohao)(?P<SEC>[0-6]?[0-9]))?)'
        #每\u6BCF 周\u5468 月\u6708 号\u53F7 
        #每\u6BCF 天\u5929
        self.dur1 = u'^\u6BCF(?P<TIAN>\u5929)?'
        #周\u5468 一二三\u4E00\u4E8C\u4E09 四五六\u56DB\u4E94\u516D 日天末\u65E5\u5929\u672B
        self.dur2 = u'^(?:\u5468(?P<ZHOU>[\u5468\u4E00\u4E8C\u4E09\u56DB\u4E94\u516D\u65E5\u5929\u672B]*))|(?:\u6708(?P<YUE>[0-9\u53F7, ]+)\u53F7)'

        #time3 = u'(?<=\u0020)(?:(?P<HOUR>0?[0-9]|1[0-9]|2[0-4])(?P<biaohao>\D{1,3})(?P<MIN>[0-6]?[0-9])(?:(?P=biaohao)(?P<SEC>[0-6]?[0-9]))?)'
        self.pd1 = re.compile(self.dur1,re.I)
        self.pd2 = re.compile(self.dur2,re.I)
        self.p1 = re.compile(self.str1, re.I)
        self.p2 = re.compile(self.str2, re.I)
        self.p3 = re.compile(self.str3, re.I)
        self.p4 = re.compile(self.str4, re.I)
        self.p5 = re.compile(self.str5, re.I)
        self.ptime1 = re.compile(self.time1, re.I)
        self.ptime2 = re.compile(self.time2, re.I)
        self.ptime3 = re.compile(self.time3, re.I)
        self.ptime4 = re.compile(self.time4, re.I)

    def process(self, line):
        ret = ""
        list = []
        cond_list = []
        out = {}
        year = 'XXXX'
        mon = 'XX'
        day = 'XX'
        h = 'XX'
        min = 'XX'
        s = 'XX'
        h1 = 'XX'
        min1 = 'XX'
        cont = "none"
        cond = "none"
        after = "XX"
        after_e = 'XX'
        v =['0','0']
        m = {}
        m = self.p1.search(line)
        flag = 0
        if m:
            flag = 1
            cont = "DAY"
        if flag != 1:
            m = self.pd1.search('') 
            if m:
                flag = 1
                cont = "DUR"
        if flag != 1:
            m = self.pd2.search('') 
            if m:
                flag = 1
                cont = "FREQ"
        if flag != 1:
            m = self.ptime1.search(line)    
            if m:
                flag = 1
                cont = "TIME"
        if flag != 1:
            m = self.ptime4.search(line)    
            if m:
                flag = 1
                cont = "TIME"
        if flag != 1:
            m = self.p2.search(line)
            if m:
                flag = 1
                cont = "DAY"
        if flag != 1:
            m = self.p5.search(line)
            if m:
                flag = 1
                cont = "DAY"
        if flag != 1:
            m = self.p3.search(line)
            if m:
                flag = 1
                cont = "DAY"
        if flag != 1:
            m = self.p4.search(line)
            if m:
                flag = 1
                cont = "DAY"
        if flag != 1:
            m = self.ptime2.search(line)    
            if m:
                flag = 1
                cont = "TIME"
        if flag != 1:
            m = self.ptime3.search(line)    
            if m:
                flag = 1
                cont = "TIME"
        if m and cont == 'DUR':
            v[0] = m.start()
            v[1] = m.end() -1
            for (a,b) in m.groupdict().items():
                if str(a) == 'TIAN' and b == u'\u5929':
                    cond = 'D'
        if m and cont == 'FREQ':
            v[0] = m.start()
            v[1] = m.end() -1
            for (a,b) in m.groupdict().items():
                if str(a) == 'ZHOU' and b != None:
                    if u'\u4E00' in b:
                        cond_list.append('Z1')
                    if u'\u4E8C' in b:
                        cond_list.append('Z2')
                    if u'\u4E09' in b:
                        cond_list.append('Z3')
                    if u'\u56DB' in b:
                        cond_list.append('Z4')
                    if u'\u4E94' in b:
                        cond_list.append('Z5')
                    if u'\u516D' in b:
                        cond_list.append('Z6')
                    if u'\u5929' in b or u'\u65E5' in b: #天 日 
                        cond_list.append('Z7')
                    if u'\u672B' in b:
                        cond_list.append('Z6')
                        cond_list.append('Z7')
                if str(a) == 'YUE' and str(b) != 'None':
                    for i in re.finditer(r'\d+',b):
                        s = 'M' + i.group()
                        cond_list.append(s)
                
                    
        if m and cont == 'DAY':
            v[0] = m.start()
            v[1] = m.end() -1
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
                if str(a) == 'DAY':
                    if str(b) == 'None':
                        day = 'XX'
                    else:
                        day = str(b)
                #ret  =  ret + str(a) + ':' + str(b) + ' '
            #ret = ret + year + '-' + mon + '-' + day 
        if m and cont == "TIME":
            v[0] = m.start()
            v[1] = m.end() - 1
            for (a,b) in m.groupdict().items():
                if str(a) == 'HOUR':
                    if str(b) == 'None':
                        h = 'XX'
                    else:
                        h = str(b)
                if str(a) == 'MIN':
                    if str(b) == 'None':
                        min = 'XX'
                    else:
                        min = str(b)
                if str(a) == 'SEC':
                    if str(b) == 'None':
                    #if str(b).isdigit() == false:
                        s = 'XX'
                    else:
                        s = str(b)
                if str(a) == 'HOUR1' and str(b) != 'None':
                    cont = 'Dur_TIME_S'
                    h1 = str(b)
                if str(a) == 'MIN1' and str(b) != 'None':
                    cont = 'Dur_TIME_S'
                    min1 = str(b)
                if str(a) == 'AFTERNOON':
                    after = b 
                #ret  =  ret + str(a) + ':' + str(b) + ' '
        #   ret = ret + '\t' + h + '-' + m + '-' + s 
        out['cont'] = cont
        out['year_s'] = year 
        out['year_e'] = 'XXXX'
        out['mon_s'] = mon  
        out['mon_e'] = 'XX' 
        out['day_s'] = day 
        out['day_e'] = 'XX'
        out['hour_s'] = h 
        out['hour_e'] = 'XX' 
        out['min_s'] = min 
        out['min_e'] = 'XX' 
        out['sec_s'] = s 
        out['sec_e'] = 'XX' 
        out['after_s'] = after
        out['after_e'] = after_e
        out['cond'] = cond  
        out['cond_cont'] = cond_list
        if h1 != 'XX' or min1 != 'XX':
            out['hour_e'] = h1 
            out['min_e'] = min1
            out['after_e'] = after
            out['cont'] = 'TIME_TIME'
        list.append(out)
        return (flag, v, out)
    

        
