#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Time-stamp: <2014-09-21 22:33:08 Sunday by work>

# @version 1.0
# @author liuzhendong01  liuzhendong01@baidu.com  

import json
import urllib2
import sys
import threading
import math
import traceback

ak_list =["4dW5o98eSoWADPoDOXCv833V","YwZD6I4TXaDTBGdLz8GjSYKw","aGLdv7iD5HqXDVRG2okCwc7B","370DpO3lN8e53LkEavyINOPi","1VX2vmMEAtsGl5oSZA7hxeQf","Yc6MG7ZLAmsO5dt1IjwLLbSB","Tm1gIzSGtWZ3f1vzIEUmTH7l","8StDloNACDDQ1rQLjDlLHmQa", "E6952afaaa527b96ed1b5be87cedc32e"]
ak_index = 0
ak = ak_list[ak_index]
geoencoder = "http://api.map.baidu.com/geocoder/v2/?output=json"
geodecoder = "http://api.map.baidu.com/geocoder/v2/?output=json"
geosearch = "http://api.map.baidu.com/place/v2/search?page_num=0&output=json"

def get_distance(_lat1,_lon1,_lat2,_lon2):
    lat1 = (math.pi/180)*_lat1;
    lat2 = (math.pi/180)*_lat2;
    lon1 = (math.pi/180)*_lon1;
    lon2 = (math.pi/180)*_lon2;
    con = math.sin(lat1)*math.sin(lat2)
    con += math.cos(lat1)*math.cos(lat2)*math.cos(lon1 - lon2)
    return round(math.acos(con)*6378137.0/1000,4)

def check_poi(data,query):
    global ak_list, ak_index, ak
    data_json = json.loads("".join(data.split("\n")))
    if not "results" in data_json:
        if ak_index < len(ak_list) - 1:
            ak = ak_list[ak_index]
            ak_index = ak_index + 1
            raise SyntaxError("invalid ak")
        else:
            sys.exit()
    if len(data_json["results"]) == 0:
        return {}
    poi_list = []
    poi_list_name = []
    for item in data_json["results"]:
        name = item["name"]
        if "(" in name:
            name = name.split("(")[0]
        if u"（" in name:
            name = name.split(u"（")[0]
        if name in query:
            poi_list_name.append(name)
            poi_list.append(item)

    if len(poi_list) == 0:
        return {}
    elif len(poi_list) == 1:
        return poi_list[0]
    else:
        if poi_list_name[0] == poi_list_name[1]:
            distance = get_distance(poi_list[0]["location"]["lat"],poi_list[0]["location"]["lng"],poi_list[1]["location"]["lat"],poi_list[1]["location"]["lng"])
            #print distance
            if distance < 2.0:
                return poi_list[0]
            else:
                result = {}
                result["name"] = poi_list_name[0]
                return result
        else:
            return poi_list[0]

    ##print "poi_num:",len(data_json["results"])
    #first_item = data_json["results"][0]
    #if len(data_json["results"]) ==  1:
    #    return first_item
    ##print "first_name:",first_item["name"].encode("utf-8")
    #second_item = data_json["results"][1] 
    ##print "second_name:",second_item["name"].encode("utf-8")
    #split_str = u"（"
    ##print split_str.encode("utf-8")
    ##print first_item["name"].split(split_str)[0].encode("utf-8")
    ##print second_item["name"].split(split_str)[0].encode("utf-8")
    #if first_item["name"].split(u"(")[0] == second_item["name"].split(u"(")[0]:
    #    result["name"] = first_item["name"].split(u"(")[0]
    #    return result
    #elif first_item["name"].split(split_str)[0] == second_item["name"].split(split_str)[0]:
    #    result["name"] = first_item["name"].split(split_str)[0]
    #    return result
    #else:
    #    return first_item

def get_decode_address(location,level,precise,poi_name):
    geodecoder_data = get_page(geodecoder + "&location=" + location + "&ak=" + ak)
    if not "formatted_address" in geodecoder_data:
        return {}       
    geodecoder_json = json.loads("".join(geodecoder_data.split("\n")))
    geodecoder_json["level"] = level
    geodecoder_json["precise"] = precise
    geodecoder_json["poi_name"] = poi_name
    return geodecoder_json

def format(data,city):
    global geoencoder, geodecoderi, geosearch
    if len(data) == 0 or len(city) == 0:
        return {}
    level = "NONE"
    precise = -1
    poi_name = "NONE"
    location = ""
    #city_sub = city.replace(u"市","")
    #data = data.replace(city,"").replace(city_sub,"")
    q = "&query=" + urllib2.quote(data.encode("utf-8")) + "&region=" + urllib2.quote(city.encode("utf-8"))  
    geosearch_data = get_page(geosearch + "&q=" + q + "&ak=" + ak)
    #print data.encode("utf-8")
    #print geosearch + "&q=" + q + "&ak=" + ak
    #print geosearch_data
    #print ak,ak_index
    poi_res = check_poi(geosearch_data,data)
    #print "check_poi_res:",json.dumps(poi_res,ensure_ascii=False).encode("utf-8")
    #print geosearch + q
    if "name" in poi_res:
        poi_name = poi_res["name"]
        if not "location" in poi_res:
            level = u"城市" 
            geoencoder_str = city
            precise = 0
        else:
            geoencoder_str = city + poi_name
            location =  "%f" % poi_res["location"]["lat"] + "," + "%f" % poi_res["location"]["lng"]
    else:
        geoencoder_str = city + data
    geoencoder_data = get_page(geoencoder + "&address=" + urllib2.quote(geoencoder_str.encode("utf-8")) + "&ak=" + ak)
    geoencoder_json = json.loads("".join(geoencoder_data.split("\n")))
    if geoencoder_json["status"] == 0:
        level = geoencoder_json["result"]["level"]
        precise = geoencoder_json["result"]["precise"]
        if len(location) > 0 and geoencoder_json["result"]["level"] == u"城市":
            level = ""
            precise = 1
        if len(location) == 0:
            location = "%f" % geoencoder_json["result"]["location"]["lat"] + "," + "%f" % geoencoder_json["result"]["location"]["lng"] 
    if len(location) == 0:
        return {}
    return get_decode_address(location,level,precise,poi_name)

    #location_2 = "%f" % check_res["location"]["lat"] + "," + "%f" % check_res["location"]["lng"] 
    ##print data.encode("utf-8")
    #geoencoder_data = get_page(geoencoder+urllib2.quote(data.encode("utf-8")))
    ##print geoencoder_data
    #geoencoder_json = json.loads("".join(geoencoder_data.split("\n")))
    #if geoencoder_json["status"] != 0:
    #    return {}
    #poi_search = True
    #level = geoencoder_json["result"]["level"]
    #precise = geoencoder_json["result"]["precise"] 
    #if level == u"城市" or level == u"区县" or level == u"道路":
    #    poi_search = False
    ##geo-decode
    #location = "%f" % geoencoder_json["result"]["location"]["lat"] + "," + "%f" % geoencoder_json["result"]["location"]["lng"] 
    #geodecoder_json = get_decode_address(location,level,precise,"NONE")
    #if not poi_search:
    #    return geodecoder_json
    ##use poi search
    #city = geodecoder_json["result"]["addressComponent"]["city"]
    #city_sub = city.replace(u"市","")
    #data = data.replace(city,"").replace(city_sub,"")
    #q = "&query=" + urllib2.quote(data.encode("utf-8")) + "&region=" + urllib2.quote(city.encode("utf-8"))  
    #geosearch_data = get_page(geosearch + q)
    #check_res = check_poi(geosearch_data,data)
    ##print geosearch + q
    #if len(check_res) == 0:
    #    if precise == 0:
    #        level = u"区县"
    #    geodecoder_json["level"] = level
    #    geodecoder_json["precise"] = precise 
    #    geodecoder_json["poi_name"] = "NONE"
    #    return geodecoder_json
    #elif not "location" in check_res:
    #    geodecoder_json["level"] = u"城市" 
    #    geodecoder_json["precise"] = 0 
    #    geodecoder_json["poi_name"] = check_res["name"]
    #    return geodecoder_json
    #location_2 = "%f" % check_res["location"]["lat"] + "," + "%f" % check_res["location"]["lng"] 
    #geodecoder_data_2 = get_page(geodecoder + location_2) 
    #if not "formatted_address" in geodecoder_data_2:
    #    return {}
    #geodecoder_json_2 = json.loads("".join(geodecoder_data_2.split("\n")))
    #geodecoder_json_2["level"] = level 
    #geodecoder_json_2["poi_name"] = check_res["name"]
    #geodecoder_json_2["precise"] = 1
    #return geodecoder_json_2

def mine(data,city):
    res = format(data,city)
    if len(res) == 0:
        return res
    if res["level"] == u"城市":
        if u"县级行政" in res["result"]["addressComponent"]["city"]:
            res["result"]["addressComponent"]["city"] = ""
        else:
            res["result"]["addressComponent"]["district"] = ""
        res["result"]["addressComponent"]["street"] = ""
        res["result"]["addressComponent"]["street_number"] = ""
    elif res["level"] == u"区县":
        res["result"]["addressComponent"]["street"] = ""
        res["result"]["addressComponent"]["street_number"] = ""
    elif res["level"] == u"道路" or res["level"] == u"":
        if res["precise"] ==  0:
            res["result"]["addressComponent"]["street_number"] = ""
    fmt_address = ""
    fmt_address = res["result"]["addressComponent"]["province"]
    if fmt_address != res["result"]["addressComponent"]["city"] and len(res["result"]["addressComponent"]["city"]) >0:
        fmt_address  = fmt_address + '$'+ res["result"]["addressComponent"]["city"]
    if len(res["result"]["addressComponent"]["district"]) > 0:
        fmt_address = fmt_address + '$' +res["result"]["addressComponent"]["district"]
    if len(res["result"]["addressComponent"]["street"]) > 0:
        fmt_address = fmt_address + '$' +res["result"]["addressComponent"]["street"]
    if len(res["result"]["addressComponent"]["street_number"]) > 0:
        fmt_address = fmt_address + '$' +res["result"]["addressComponent"]["street_number"]
    res["result"]["formatted_address"] = fmt_address
    return res

def get_page(url):
    req = urllib2.Request(url)
    sock = urllib2.urlopen(req, timeout=3000)
    value = ""
    if sock.getcode() != 200:                                                                                     
        print >>sys.stderr,"error code:",page_content.getcode(),url
    else:
        value = sock.read()
    sock.close()
    return value

def test():
    global ak_index
    lines = []
    #lines.append(u"北京市")
    #lines.append(u"北京 海淀区 万柳")
    #lines.append(u"广州香格里拉酒店")
    #lines.append(u" 北京 海淀区 北京大学")
    #lines.append(u"北京国家会议中心")
    #lines.append(u"北京 东城区 东方剧院")
    lines.append(u"哈尔滨 道里区 后窗精品咖啡馆(中央大街店)")
    for line in lines:
        try:
            print line.encode("utf-8")
            print "ak_index", ak_index
            data = mine(line,u"北京市")
            if len(data) == 0:
                str = "NONE"
            else:
                str = json.dumps(data,ensure_ascii=False).encode("utf-8")
            print str
        except:
            print traceback.print_exc()

if __name__ == "__main__":
    #print get_distance(39.948,116.33,39.965,116.33)
    test()


