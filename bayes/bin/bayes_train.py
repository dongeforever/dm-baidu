#!/bin/env python
# coding=utf-8
import sys
import os
import random
from optparse import OptionParser
import string

def print_attr(a):
    for item in a :
        str = "{label:"+item["label"] +",url:" + item["url"] 
        for (k,v) in item.items():
            if k == "url" or k == "label":
                continue
            else:
                str = str + "," + k + ":" + "%d"%v
        str = str + "}"
        print str
    print "========================"

def print_matrix():
    f = open("prior_prob.res.tmp","w+")
    global is_debug_mode
    try:
        table_head = "word"
        for item in sorted(sign_id_map.items(),key = lambda a:a[1]):
            table_head = table_head + "\t" + item[0]
        f.write(table_head + "\n")
        print table_head
        word_array = [0] * len(word_list)
        for (k,v) in word_list.items():
            print k,v,len(word_array)
            word_array[v] = k
        for i in range(len(word_list)):
            prefix = ""
            if is_debug_mode == 1 and prob_matrix[i][0] < prob_matrix[i][1] * 1.1:
                prefix = "STOP\t"
            prefix = prefix + word_array[i] + "\t" + "%f"%prob_matrix[i][0] + "\t" + "%f"%prob_matrix[i][1]
            print prefix
            f.write(prefix + "\n")
        print "========================"
    finally:
        f.close()


def print_hash(a):
    for (k,v) in a.items():
        print k,v

def load_word_list(file_name,word_list):
    f_input = open(file_name,"r")
    try:
        while True:
            line = f_input.readline()
            line = line.strip()
            if(len(line) == 0):
                break
            #print line
            if not  word_list.has_key(line):
                last_word_num = len(word_list)
                word_list[line] = last_word_num
    finally:
        f_input.close()

def create_input_matrix(file_name):
    f_input = open(file_name,"r")
    try:
        while True:
            line = f_input.readline()
            line = line.strip()
            if(len(line) == 0):
                break
            items = line.split("$$")
            if len(items) <= 2 :
                continue
            doc = {}
            sign = items[0]
            doc["label"] = items[0]
            doc["url"] = items[1]
            if not sign_id_map.has_key(sign):
                last_sign_num = len(sign_id_map)
                sign_id_map[sign] = last_sign_num
                sign_num_map[sign] = 1
            else:
                sign_num_map[sign] = sign_num_map[sign] + 1
            for i in range(2,len(items)) :
                if word_list.has_key(items[i]):
                    if not doc.has_key(items[i]):
                        doc[items[i]] = 1
                    else:
                        doc[items[i]] = doc[items[i]] + 1
            attr_matrix.append(doc)
    finally:
        f_input.close()

def create_output_matrix():
    for item in attr_matrix:
        for (k,v) in item.items():
            if k == "label" or k == "url":
                continue
            i = word_list[k]
            j = sign_id_map[item["label"]]
            prob_matrix[i][j] = prob_matrix[i][j] + 1

    w_size = len(word_list)
    t = smooth_rate
    for n in range(0,word_size):
        for (k,v) in sign_id_map.items():
            prob_matrix[n][v] = (prob_matrix[n][v] + t)/(sign_num_map[k] + t*w_size)

#main starts here            
opt_parser = OptionParser("usage: %prog [options]")
opt_parser.add_option("-w", "--word_list_file", dest="word_list_file", default="null",help="the word in it is the feature")
opt_parser.add_option("-t", "--train_file_name", dest="train_file_name", default="null",help="the train file name")
opt_parser.add_option("-m", "--main_class_name", dest="main_class_name", default="null",help="main_class_name")
opt_parser.add_option("-d", "--debug_mode", dest="is_debug_mode", default=0,help="the debug mode")
opt_parser.add_option("-s", "--smooth_rate", dest="smooth_rate", default= 0 ,help="the smooth rate")
(options, args) = opt_parser.parse_args()
if len(args) > 0 :
    opt_parser.print_help()
    sys.exit()

word_list_file = options.word_list_file
train_file_name = options.train_file_name
m_class = options.main_class_name
is_debug_mode = options.is_debug_mode
smooth_rate = string.atof(options.smooth_rate)

if word_list_file == "null" or train_file_name == "null":
    opt_parser.print_help()
    sys.exit()

#input_file = "input.txt"
sign_id_map = {}
sign_num_map = {}
doc_num = 0
stop_word_list = {}
word_list = {}
attr_matrix = []

load_word_list(word_list_file,word_list)
print_hash(word_list)


#process the input
if m_class != "null":
    sign_id_map[m_class] = 0
    sign_num_map[m_class] = 1
create_input_matrix(train_file_name)
print_attr(attr_matrix)
sign_num_map["NOR"] = sign_num_map["NOR"] * 2 + sign_num_map["NOR"]/2
print sign_id_map
print sign_num_map

#process the output
word_size = len(word_list)
prob_matrix = [([0.0]*len(sign_id_map)) for i in range(word_size)]
create_output_matrix()
print_matrix()


