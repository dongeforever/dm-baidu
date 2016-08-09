#!/bin/env python
# coding=utf-8
import sys
import os
import random
from optparse import OptionParser
import string

def load_prior_prob(file_name):
    f_input = open(file_name,"r")
    is_first_line = 0
    try:
        while True:
            line = f_input.readline()
            line = line.strip()
            if(len(line) == 0):
                break
            items = line.split("\t")
            if len(items) != 3:
                print "error in the prob file!",len(items),line
                sys.exit()
            if is_first_line == 0:
                sign_id_map[items[1]] = 0
                sign_id_map[items[2]] = 1
                is_first_line = 1
            else:
                word_list[items[0]] = len(prob_matrix)
                prob_matrix.append((string.atof(items[1]),string.atof(items[2]),items[0]))
            #print line
    finally:
        for i in range(len(prob_matrix)):
            if word_list[prob_matrix[i][2]] != i:
                print "load prob error !"
                sys.exit()
        f_input.close()


def select(wv):
    sign_score = {}
    for (k,v) in sign_id_map.items():
        sign_score[k] = 1.0
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
    wv = [0]*len(word_list)
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
            wv = [0]*len(word_list)
            key_word_num = 0
            key_word_str = "$$["
            for i in range(1,len(items)) :
                if word_list.has_key(items[i]):
                    key_word_num = key_word_num + 1
                    key_word_str = key_word_str + items[i] + "-"
                    wv[word_list[items[i]]] = wv[word_list[items[i]]] + 1
            key_word_str = key_word_str + "]"
            if is_debug_mode == 0:
                key_word_str = ""
            if key_word_num == 0:
                print "NOMATCH" + "\t" + line
            else:
                choice = select(wv)[0]
                print choice + key_word_str + "\t" + line
    finally:
        f_input.close()

#main starts here            
opt_parser = OptionParser("usage: %prog [options]")
opt_parser.add_option("-p", "--prior_prob_file", dest="prior_prob_file", default="null",help="the feature prior prob matrix")
opt_parser.add_option("-t", "--test_file", dest="test_file", default="null",help="the item in it will be predicted")
opt_parser.add_option("-d", "--debug_mode", dest="is_debug_mode", default=0,help="the debug mode")
(options, args) = opt_parser.parse_args()
if len(args) > 0 :
    opt_parser.print_help()
    sys.exit()

prior_prob_file = options.prior_prob_file
test_file = options.test_file
is_debug_mode = options.is_debug_mode
if prior_prob_file == "null" or test_file == "null":
    opt_parser.print_help()
    sys.exit()

sign_id_map = {}
word_list = {}
prob_matrix = []


load_prior_prob(prior_prob_file)

#test the selector
test_none()
test_select(test_file)

