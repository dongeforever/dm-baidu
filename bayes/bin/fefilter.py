#!/bin/env python
# coding=utf-8
import sys
import os
import random
from optparse import OptionParser
import string

def print_wordlist(a):
    global m_sign
    size = len(a)
    tmp_list = [0]*size
    for (k,v) in a.items():
        tmp_list[v[0]] = k
    for i in range(0,len(tmp_list)):
        if tmp_list[i] != 0:
            print tmp_list[i],i
    print "========================"
    f_output = open(m_sign+"_word_list.tmp","w")
    try:
        for item in sorted(a.items(),key = lambda a:a[1][1],reverse=True):
            rate =  item[1][1]/(doc_num + 0.1)
            f_output.write(item[0]+"\t"+'%d'%item[1][1]+"\t"+'%f'%rate+"\n")
        #for (k,v) in a.items():
        #    rate = v[1]/(doc_num + 0.1)
        #    f_output.write(k+"\t"+'%d'%v[1]+"\t"+'%f'%rate+"\n")
    finally:
        f_output.close()

def print_prior_prob(a,b):
    global m_sign
    f_output = open(m_sign+"_word_prior_prob.tmp","w")
    try:
        for item in sorted(b.items(),key = lambda b:prob_matrix[b[1][0]][sign_id_map[m_sign]],reverse=True):
            prob_novel = a[item[1][0]]
            novel_prob = prob_matrix[item[1][0]][sign_id_map[m_sign]]
            if novel_prob < 0.01:
                continue
            prefix = ""
            if prob_novel < 0.7 or ((1 - prob_novel)/prob_novel)*novel_prob > 0.02 or novel_prob < 0.01:
                prefix = "STOP\t"
            f_output.write(prefix+item[0]+"\t"+ ("%f" % prob_novel) + "\t" + ("%f" % novel_prob) + "\n")
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
        str = ""
        for i in range(len(item)):
            str = str + "%f"%item[i] + " "
        print str
    print "========================"


def print_hash(a):
    for (k,v) in a.items():
        print k,v

def load_stop_word(file_name):
    if file_name == "null":
        return
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
    if file_name == "null":
        return
    global doc_num,m_sign
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
            if len(m_sign) == 0:
                m_sign = sign
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
    if file_name == "null":
        return
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

def create_sign_prob_matrix():
    print "len(attr_matrix)",len(attr_matrix)
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

def create_prob_sign_matrix(file_name):
    global prior_class_prob
    if file_name == "null":
        return
    f_input = open(file_name,"r")
    index = 0
    try:
        while True:
            line = f_input.readline()
            line = line.strip()
            if(len(line) == 0):
                break
            items = line.split("$$")
            if len(items) <= 1 :
                continue
            doc = {}
            index = index + 1
            for i in range(1,len(items)) :
                if word_list.has_key(items[i]):
                    if not doc.has_key(items[i]):
                        doc[items[i]] = 1
                        prior_probs[word_list[items[i]][0]] = prior_probs[word_list[items[i]][0]] + 1
    finally:
        f_input.close()
        #prior_class_prob = 2000.1/70000
        print index,prior_class_prob
        for i in range(word_size):
            prior_probs[i] = (prior_class_prob * prob_matrix[i][sign_id_map[m_sign]])/((prior_probs[i]+0.1)/index)

#main starts here            
opt_parser = OptionParser("usage: %prog [options]")
opt_parser.add_option("-s", "--stop_file_name", dest="stop_file_name", default="null",help="the stop word file name,the word in it will be ignored")
opt_parser.add_option("-t", "--train_file_name", dest="train_file_name", default="null",help="the train file name")
opt_parser.add_option("-c", "--corpus_file_name", dest="corpus_file_name", default="null",help="the corpus")
opt_parser.add_option("-p", "--prior_class_prob", dest="prior_class_prob", default=0.0286,help="the prior_class_prob")
(options, args) = opt_parser.parse_args()
if len(args) > 0 :
    opt_parser.print_help()
    sys.exit()
stop_file_name = options.stop_file_name
train_file_name = options.train_file_name
corpus_file_name = options.corpus_file_name
prior_class_prob = string.atof(options.prior_class_prob)

if train_file_name == "null":
    opt_parser.print_help()
    sys.exit()

m_sign = "" 
sign_id_map = {}
sign_num_map = {}
doc_num = 0
stop_word_list = {}
word_list = {}
attr_matrix = []

load_stop_word(stop_file_name)
create_wordlist(train_file_name)
print_wordlist(word_list)
print "m_sign:",m_sign
print sign_id_map
print sign_num_map

#process the input
create_input_matrix(train_file_name)
#print_attr(attr_matrix)

#process the output
word_size = len(word_list)
prob_matrix = [([0.0]*len(sign_id_map)) for i in range(word_size)]
create_sign_prob_matrix()
#print_matrix(prob_matrix)

prior_probs = [0] * word_size
create_prob_sign_matrix(corpus_file_name)
print_prior_prob(prior_probs,word_list)

