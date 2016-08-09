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
            url = items[0]
            if match_site_list.has_key(url) and match_site_list[url] == 1:
                match_site_list[url] = 0
                print line
            elif len(items) >= 2:
                url = items[1]
                if match_site_list.has_key(url) and match_site_list[url] == 1:
                    match_site_list[url] = 0
                    print line
            #print "========================"
    finally:
        f_input.close()

#main start here
if len(sys.argv) != 3:
    print "Usage: $0 site_nav_source match_site_list"
    sys.exit()
match_site_list = {}
match_site_list_name = sys.argv[2]
load_match_site_list(match_site_list_name)
#print_hash(match_site_list)

match_file_name = sys.argv[1]

match(match_file_name)
