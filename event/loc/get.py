#!/bin/env  python
import  sys

print sys.getdefaultencoding()
while True:
    line = sys.stdin.readline()
    line = line.strip()
    if len(line) == 0:
        break
    items = line.split("$$")
    str = "" + items[len(items)-1]
    for i in range(0,len(items)-1):
        str = str + "$$"+items[i]
    print str


















