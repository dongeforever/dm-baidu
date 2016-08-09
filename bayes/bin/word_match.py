#!/bin/env python
import sys
import os
import random
from optparse import OptionParser

def print_hash(a):
    size = len(a)
    tmp_list = [0]*size
    for (k,v) in a.items():
        tmp_list[v] = k
    for i in range(0,len(tmp_list)):
        print tmp_list[i],i
    print "========================"

def print_matrix(a):
    for item in a :
        print item[0],item[1]
    print "========================"

def load_wordlist(file_name):
    f_input = open(file_name,"r")
    try:
        while True:
            line = f_input.readline()
            line = line.strip()
            if(len(line) == 0):
                break
            #print line
            if not word_list.has_key(line):
                size = len(word_list)
                word_list[line] = size
            #print "========================"
    finally:
        f_input.close()

def match(file_name):
    f_input = open(file_name,"r")
    try:
        while True:
            line = f_input.readline()
            line = line.strip()
            if(len(line) == 0):
                break
            #print line
            items = line.split("$$")
            if len(items) <= 1:
                continue
            match_words = {}
            for i in range(1,len(items)) :
                if word_list.has_key(items[i]):
                    if not match_words.has_key(items[i]):
                        match_words[items[i]] = 1
            prefix = "NOMATCH "
            if len(match_words) != 0:
                prefix = "MATCH "
            word_str = "["
            for (k,v) in match_words.items():
                word_str = word_str + k + " "
            word_str = word_str + "]"
            print prefix + word_str + "\t" + line
            #print "========================"
    finally:
        f_input.close()

#main start here
if len(sys.argv) != 3:
    print "Usage: $0 wordlist_file_name match_file_name"
    sys.exit()
word_list = {}
wordlist_file_name = sys.argv[1]
load_wordlist(wordlist_file_name)
#print_hash(word_list)

match_file_name = sys.argv[2]

match(match_file_name)
