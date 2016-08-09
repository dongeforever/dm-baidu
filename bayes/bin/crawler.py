#!/bin/env python
#-*- coding: utf-8 -*-
import sys
import threading
import urllib2
from optparse import OptionParser

import nav_miner
import title_miner

def get_page(url) :
    req = urllib2.Request(url)
    sock = urllib2.urlopen(req, timeout=3000)
    if sock.getcode() != 200:                                                                                     
        print >>sys.stderr,"error code:",page_content.getcode(),url
        return ""
    value = sock.read()
    sock.close()
    return value

def thread_main():
    global url_list,index
    global url_list_lock,file_write_lock
    global output_file,error_file
    while True:
        url_list_lock.acquire()
        if index >= len(url_list):
            url_list_lock.release()
            return 
        url = url_list[index]
        index = index+1
        url_list_lock.release()
        try:
            page_data = get_page(prefix + url)
            print "get page data success"
            mine_data = title_miner.mining(page_data)
            print "get nav data success:",mine_data
            if len(mine_data) == 0:
                continue
            file_write_lock.acquire()
            output_file.write(url+"$$"+mine_data+"\n")
            output_file.flush()
            file_write_lock.release()
        except:
            info = sys.exc_info() 
            print info[0],":",info[1]
            file_write_lock.acquire()
            error_file.write("error:"+url+"\n")
            error_file.flush()
            file_write_lock.release()

def load_stop_url(file_name):
    if file_name == "null":
        return
    f_input = open(file_name,"r")
    try:
        while True:
            line = f_input.readline()
            if len(line) == 0:
                break
            line = line.strip()
            if len(line) == 0:
                continue
            if not stop_url_list.has_key(line):
                stop_url_list[line] = 1
    finally:
        f_input.close()
def load_crawl_url(file_name):
    if file_name == "null":
        return
    f_input = open(file_name,"r")
    try:
        while True:
            line = f_input.readline()
            if len(line) == 0:
                break
            line = line.strip()
            if len(line) == 0:
                continue
            if not stop_url_list.has_key(line):
                url_list.append(line)
    finally:
        f_input.close()

def start(thread_num):
    threads = []
    for i in range(0,thread_num):
        threads.append(threading.Thread(target=thread_main))
    for t in threads:
        t.start()
    for t in threads:
        t.join()


#here start the global 
url_list = []
stop_url_list = {}
index = 0
url_list_lock = threading.Lock()
file_write_lock = threading.Lock()
online_prefix = "http://m.baidu.com/l=3/tc?srd=1&dict=21&nocache=1&tc_source=1&src="

opt_parser = OptionParser("usage: %prog [options]")
opt_parser.add_option("-t", "--thread_number", dest="thread_number", default="5",help="the thread number")
opt_parser.add_option("-s", "--stop_file_name", dest="stop_file_name", default="null",help="the stop file name,the site in it will be ignored")
opt_parser.add_option("-c", "--crawl_file_name", dest="crawl_file_name", default="null",help="the crawl file name,the site in it will be crawled")
opt_parser.add_option("-p", "--prefix", dest="prefix", default=""+online_prefix,help="the prefix")
(options, args) = opt_parser.parse_args()
if len(args) > 0 :
    opt_parser.print_help()
    sys.exit()
thread_num = int(options.thread_number)
stop_file_name = options.stop_file_name
crawl_file_name = options.crawl_file_name
prefix = options.prefix


load_stop_url(stop_file_name)
load_crawl_url(crawl_file_name)

if len(url_list) == 0:
    print "it has no url"
    sys.exit()
else :
    print "it has",len(url_list),"urls in",thread_num,"threads"

output_file = open("crawl_output.txt", 'w+')
error_file = open("crawl_error.txt", 'w+')

start(thread_num)

output_file.close()
error_file.close()

