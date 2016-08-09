#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Time-stamp: <2014-11-14 22:33:08 Friday by work>

# @version 1.0
# @author liuzhendong01  liuzhendong01@baidu.com  

import sys
import json
from optparse import OptionParser
import threading

import ex_extractor
import global_obj
import traceback
   

def thread_main():
    global out_file
    global read_lock
    global filter_node 
    extractor = ex_extractor.ExExtractor(filter_node == 1)
    #while False:
    while True:
        try:
            read_lock.acquire()
            line = sys.stdin.readline()
            read_lock.release()
            if not line:
                break
            line = line.strip()
            if len(line) == 0 :
                continue
            items = line.split("\t")
            url = items[0]
            page_data = items[1] 
            if len(items) != 2:
                out_str = "FORMAT_ERROR" + "\t" + url
                print out_str 
                if out_file != "null":
                    out_file.write(out_str + "\n")
                    out_file.flush()
                continue
            res_json = extractor.process(page_data)
            #if "blocks" in res_json:
            #    res_json["blocks"] = []
            if "event_block_num" in res_json and res_json["event_block_num"] > 0:
                out_prefix =  "YES"
            else:
                out_prefix =  "NO"
            out_str = out_prefix + "\t" + url + "\t" + json.dumps(res_json,ensure_ascii=False).encode("utf-8")
            print out_prefix + "\t" + url
            if out_file != "null":
                out_file.write(out_str + "\n")
                out_file.flush()
        except:
            out_str = "ERROR" + "\t" + line 
            if out_file != "null":
                out_file.write(out_str + "\n")
                out_file.flush()
            print traceback.print_exc()

def start(thread_num):
    threads = []
    for i in range(0,thread_num):
        threads.append(threading.Thread(target=thread_main))
    for t in threads:
        t.start()
    for t in threads:
        t.join()




#here start the global 
opt_parser = OptionParser("usage: %prog [options]")
opt_parser.add_option("-t", "--thread_number", dest="thread_number", default="5",help="the thread number")
opt_parser.add_option("-o", "--save_file_name", dest="save_file_name", default="null",help="the save file name,the output will be saved in it")
opt_parser.add_option("-f", "--filter_node", dest="filter_mode", default=1, help="if the filter node is 1,it will check the keywords")
(options, args) = opt_parser.parse_args()
if len(args) > 0 :
    opt_parser.print_help()
    sys.exit()
thread_num = int(options.thread_number)
save_file_name = options.save_file_name
filter_node = options.filter_mode
read_lock = threading.Lock()

out_file = "null"
if save_file_name != "null":
    out_file = open(save_file_name,"w+")

start(thread_num)

if out_file != "null":
    out_file.close()

    

