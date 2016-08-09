#!/bin/env python
#-*- coding: utf-8 -*-
import sys
import os
import random
from optparse import OptionParser
#参数解析
usage = "usage: %prog [options]"
opt_parser = OptionParser(usage)
opt_parser.add_option("-t", "--random_time", dest="random_time", default="2",
        help="the times you random,every time,the left will be 1/10 of the original")
(options, args) = opt_parser.parse_args()
if len(args) > 0 :
    opt_parser.print_help()
    sys.exit()
random_time= int(options.random_time)

lists=[]
for i in range(0,random_time+1):
    lists.append([])

while True:
    line=sys.stdin.readline()
    line=line.strip()
    if len(line)==0:
        continue
    elif line == "END":
        break
    lists[0].append(line)
    for k in range(0,random_time+1):
        if k==random_time:
            break
        if len(lists[k])>=10:
            lists[k+1].append(random.choice(lists[k]))
            lists[k]=[]
        else:
            break

random.shuffle(lists[random_time])
for item in lists[random_time]:
    print item



        
