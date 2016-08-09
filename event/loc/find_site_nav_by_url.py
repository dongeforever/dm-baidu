#!/bin/env python
import sys
import os
import random
from optparse import OptionParser

def print_hash(a):
    for (k,v) in a.items():
        print k,v
    print "========================"


def load_match_site_list(file_name):
    f_input = open(file_name,"r")
    try:
        while True:
            line = f_input.readline()
            line = line.strip()
            if(len(line) == 0):
                break
            #print line
            if not match_site_list.has_key(line):
                match_site_list[line] = 1 
            #print "========================"
    finally:
        f_input.close()

def match(file_name):
    global all_match
    f_input = open(file_name,"r")
    try:
        while True:
            line = f_input.readline()
            line = line.strip()
            if(len(line) == 0):
                break
            #print line
            items = line.split("\t")
            if len(items) <= 1: 
                continue
            url = items[0]
            if all_match:
                if match_site_list.has_key(url) and match_site_list[url] == 1:
                    #match_site_list[url] = 0
                    print line
                elif len(items) >= 2:
                    url = items[1]
                    if match_site_list.has_key(url) and match_site_list[url] == 1:
                        match_site_list[url] = 0
                        print line
            else:
                match = 0
                for (k,v) in match_site_list.items():
                    if v == 0:
                        continue
                    if url in k or k in url:
                        match =  1
                        v = 0
                        break
                if match == 1:
                    print line
            #print "========================"
    finally:
        f_input.close()

def no_match(file_name):
    no_match_list = {}
    f_input = open(file_name,"r")
    try:
        while True:
            line = f_input.readline()
            line = line.strip()
            if(len(line) == 0):
                break
            #print line
            items = line.split("$$")
            if len(items) < 1: 
                continue
            url = items[0]
            if not match_site_list.has_key(url) and not no_match_list.has_key(url):
                no_match_list[url] = 0
                print line
            #print "========================"
    finally:
        f_input.close()


#main start here
opt_parser = OptionParser("usage: %prog [options]")
opt_parser.add_option("-s", "--source_file", dest="source_file", default="null",help="the source file")
opt_parser.add_option("-m", "--match_file", dest="match_file", default="null",help="the macth file name")
opt_parser.add_option("-n", "--no_match", action = "store_true", dest="no_match", default=False,help="display the no match record")
opt_parser.add_option("-a", "--all_match",action = "store_true", dest="all_match", default=False,help="display the all_match record")
(options, args) = opt_parser.parse_args()
if len(args) > 0 :
    opt_parser.print_help()
    sys.exit()

source_file = options.source_file
match_file = options.match_file
no_match = options.no_match
all_match = options.all_match

if source_file == "null" or match_file == "null":
    opt_parser.print_help()
    sys.exit()

match_site_list = {}
load_match_site_list(match_file)


if no_match:
    no_match(source_file)
else:
    match(source_file)
