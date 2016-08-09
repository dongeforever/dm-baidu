#!/usr/bin/env python
#coding=utf-8

# Time-stamp: <2014-09-21 22:33:08 Sunday by work>

# @version 1.0
# @author liuzhendong01  liuzhendong01@baidu.com  

import json
import urllib2
import sys
import threading

geoencoder = "http://api.map.baidu.com/geocoder/v2/?output=json&ak=E6952afaaa527b96ed1b5be87cedc32e&address="
geodecoder = "http://api.map.baidu.com/geocoder/v2/?output=json&ak=E6952afaaa527b96ed1b5be87cedc32e&location="
geosearch = "http://api.map.baidu.com/place/v2/search?page_num=0&output=json&ak=E6952afaaa527b96ed1b5be87cedc32e"

def check_poi(data):
    data_json = json.loads("".join(data.split("\n")))
    if len(data_json["results"]) == 0:
        return {}
    #print "poi_num:",len(data_json["results"])
    first_item = data_json["results"][0]
    if len(data_json["results"]) ==  1:
        return first_item
    #print "first_name:",first_item["name"].encode("utf-8")
    second_item = data_json["results"][1] 
    #print "second_name:",second_item["name"].encode("utf-8")
    split_str = u"（[B"
    print split_str.encode("utf-8")
    print first_item["name"].split(split_str)[0].encode("utf-8")
    print second_item["name"].split(split_str)[0].encode("utf-8")
    if first_item["name"].split(u"(")[0] == second_item["name"].split(u"(")[0]:
        return {}
    elif first_item["name"].split(split_str)[0] == second_item["name"].split(split_str)[0]:
        return {}
    else:
        return first_item

def mine(data):
    global geoencoder, geodecoderi, geosearch
    if len(data) == 0:
        return ""
    #print data
    geoencoder_data = get_page(geoencoder+urllib2.quote(data))
    #print geoencoder_data
    geoencoder_json = json.loads("".join(geoencoder_data.split("\n")))
    if geoencoder_json["status"] != 0:
        return ""
    location = "%f" % geoencoder_json["result"]["location"]["lat"] + "," + "%f" % geoencoder_json["result"]["location"]["lng"] 
    city_level = u"城市"
    district_level = u"区县"
    poi_search = True
    if geoencoder_json["result"]["level"] == city_level or geoencoder_json["result"]["level"] == district_level:
        poi_search = False

    if geoencoder_json["result"]["level"] == "" and geoencoder_json["result"]["precise"] == 0:
        poi_search = False

    geodecoder_data = get_page(geodecoder + location)
    if not "formatted_address" in geodecoder_data:
        return ""       
    geodecoder_json = json.loads("".join(geodecoder_data.split("\n")))
    geodecoder_json["level"] = geoencoder_json["result"]["level"]
    if not poi_search:
        return json.dumps(geodecoder_json,ensure_ascii=False).encode("utf-8")
    #use poi search
    city = geodecoder_json["result"]["addressComponent"]["city"].encode("utf-8")
    q = "&query=" + urllib2.quote(data) + "&region=" + urllib2.quote(city)  
    geosearch_data = get_page(geosearch + q)
    check_res = check_poi(geosearch_data)
    print geosearch + q
    if len(check_res) == 0:
        print "poi search error"
        geodecoder_json["level"] = city_level 
        return json.dumps(geodecoder_json,ensure_ascii=False).encode("utf-8")
    location_2 = "%f" % check_res["location"]["lat"] + "," + "%f" % check_res["location"]["lng"] 
    geodecoder_data_2 = get_page(geodecoder + location_2) 
    geodecoder_json_2 = json.loads("".join(geodecoder_data_2.split("\n")))
    geodecoder_json_2["level"] = geoencoder_json["result"]["level"]
    if not "formatted_address" in geodecoder_data_2:
        return ""
    else:
        return json.dumps(geodecoder_json_2,ensure_ascii=False).encode("utf-8")

def get_page(url):
    req = urllib2.Request(url)
    sock = urllib2.urlopen(req, timeout=3000)
    if sock.getcode() != 200:                                                                                     
        print >>sys.stderr,"error code:",page_content.getcode(),url
    else:
        value = sock.read()
    sock.close()
    return value

def mine_data():
    while True:
        read_lock.acquire()
        line = sys.stdin.readline()
        read_lock.release()
        line = line.strip()
        if len(line) == 0:
            break
        #items = line.split(" ")
        #if len(items) < 2:
        #    print "len:",len(items),line
        #    continue
        #url = items[0]
        try:
            data = mine(line)
            str = "NONE"
            if len(data) > 0:
                data_json = json.loads("".join(data.split("\n")))
                if "precise" in data_json:
                    str = data_json["result"]["addressComponent"]["city"].encode("utf-8")
                else:
                    str = data_json["result"]["formatted_address"].encode("utf-8")
            print line,"      ",str
        except:
            info = sys.exc_info()
            print >>sys.stderr,info[0],":",info[1]

lines = []
lines.append(u"a")
lines.append(u"a/")
lines.append(u"/a")
lines.append(u"aaa//" )
lines.append(u"//aaa" )
#lines.append(u"北京国贸")
#lines.append(u"北京市上地东路" )
#lines.append(u"北京市上地东路鹏寰大厦")
#lines.append(u"北京市海淀区")
#lines.append(u"北京人民大会堂")
#lines.append(u"北京家乐福")
#lines.append(u"北京稻香村")
try:
    for line in lines:
        items = line.split(u"/")
        print items
except:
    info = sys.exc_info()
    print >>sys.stderr,info[0],":",info[1]




