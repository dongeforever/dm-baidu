#!/bin/env python
# coding=utf-8
import sys
import os
import random
from optparse import OptionParser
import string

def print_wordlist(a):
    size = len(a)
    tmp_list = [0]*size
    for (k,v) in a.items():
        tmp_list[v[0]] = k
    for i in range(0,len(tmp_list)):
        if tmp_list[i] != 0:
            print tmp_list[i],i
    print "========================"
    f_output = open("word_list.txt","w")
    try:
        for item in sorted(a.items(),key = lambda a:a[1][1],reverse=True):
            rate =  item[1][1]/(doc_num + 0.1)
            f_output.write(item[0]+"\t"+'%d'%item[1][1]+"\t"+'%f'%rate+"\n")
        #for (k,v) in a.items():
        #    rate = v[1]/(doc_num + 0.1)
        #    f_output.write(k+"\t"+'%d'%v[1]+"\t"+'%f'%rate+"\n")
    finally:
        f_output.close()

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

def print_matrix(a):
    for item in a :
        print item[0],item[1]
    print "========================"


def print_hash(a):
    for (k,v) in a.items():
        print k,v

def load_stop_word(file_name):
    f_input = open(file_name,"r")
    try:
        while True:
            line = f_input.readline()
            line = line.strip()
            if(len(line) == 0):
                break
            #print line
            if not  stop_word_list.has_key(line):
                stop_word_list[line] = 1
    finally:
        f_input.close()
#every item in the wordlist had its NO. and freqs
def create_wordlist(file_name):
    global doc_num
    f_input = open(file_name,"r")
    try:
        while True:
            line = f_input.readline()
            line = line.strip()
            if(len(line) == 0):
                break
            #print line
            items = line.split("$$")
            if len(items) <= 2:
                continue
            doc_num = doc_num + 1
            sign = items[0]
            if not sign_id_map.has_key(sign):
                last_sign_num = len(sign_id_map)
                sign_id_map[sign] = last_sign_num
                sign_num_map[sign] = 1
            sign_num_map[sign] = sign_num_map[sign] + 1
            for i in range(2,len(items)) :
                if stop_word_list.has_key(items[i]):
                    continue
                if not word_list.has_key(items[i]):
                    word_list[items[i]] = [0,1]
                else:
                    word_list[items[i]][1] = word_list[items[i]][1] + 1
            #print "========================"
    finally:
        print "del before",len(word_list)
        min_fencs = doc_num/100
        size = 0
        for (k,v) in word_list.items():
            if v[1] <  2:
                del word_list[k]
            else:
                v[0] = size
                size = size + 1
        print "del after",len(word_list)
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
            doc["label"] = items[0]
            doc["url"] = items[1]
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
            i = word_list[k][0]
            j = sign_id_map[item["label"]]
            prob_matrix[i][j] = prob_matrix[i][j] + 1

    for n in range(0,word_size):
        for (k,v) in sign_id_map.items():
            prob_matrix[n][v] = prob_matrix[n][v]/(sign_num_map[k]+0.1)

def select(wv):
    all_sign_num = 0
    for (k,v) in sign_num_map.items():
        all_sign_num = all_sign_num + sign_num_map[k]
    sign_score = {}
    for (k,v) in sign_num_map.items():
        sign_score[k] = sign_num_map[k]/(all_sign_num + 0.1)
    for (k,v) in sign_id_map.items():
        for i in range(len(wv)):
            if wv[i] == 0:
                sign_score[k] = sign_score[k]*(1 - prob_matrix[i][v])
            else:
                sign_score[k] = sign_score[k]*(prob_matrix[i][v]**wv[i])
    big_score = 0.0
    choice = ""
    for (k,v) in sign_score.items():
        if v >= big_score:
            choice = k
            big_score = v
    return (choice,sign_score)

def test_none():
    wv = [0]*word_size
    print select(wv)

def test_select(file_name):
    f_input = open(file_name,"r")
    try:
        while True:
            line = f_input.readline()
            line = line.strip()
            if(len(line) == 0) :
                break
            items = line.split("$$")
            if len(items) <= 1:
                continue
            wv = [0]*word_size
            key_word_str = "$$["
            for i in range(1,len(items)) :
                if word_list.has_key(items[i]):
                    key_word_str = key_word_str + items[i] + "-"
                    wv[word_list[items[i]][0]] = wv[word_list[items[i]][0]] + 1
            key_word_str = key_word_str + "]"
            #key_word_str = ""
            choice = select(wv)[0]
            print choice + key_word_str + "\t" + line
    finally:
        f_input.close()

#main start here
if len(sys.argv) <= 1:
    print "Usage: $0 train_file_name [test_file_name] [stop_word_file_name]"
    sys.exit()
#input_file = "input.txt"
sign_id_map = {}
sign_num_map = {}
doc_num = 0
stop_word_list = {}
word_list = {}
attr_matrix = []

#pre_process
if len(sys.argv) >= 4:
    stop_word_file_name = sys.argv[3]
    load_stop_word(stop_word_file_name)
    print_hash(stop_word_list)
train_file_name = sys.argv[1]
create_wordlist(train_file_name)
print_wordlist(word_list)
print sign_id_map
print sign_num_map

#process the input
create_input_matrix(train_file_name)
print_attr(attr_matrix)

#process the output
word_size = len(word_list)
prob_matrix = [([0.0]*len(sign_id_map)) for i in range(word_size)]
create_output_matrix()
print_matrix(prob_matrix)

#test the selector
test_none()
if len(sys.argv) >= 3:
    test_file_name = sys.argv[2]
    test_select(test_file_name)

