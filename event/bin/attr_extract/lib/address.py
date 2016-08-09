#!/usr/bin/env python
# coding=utf-8

# Time-stamp: <2014-09-21 22:33:08 Sunday by work>

# @version 1.0
# @author liuzhendong01  liuzhendong01@baidu.com  

import json
import os
import urllib2
import sys
import threading
import nlp_tool as nlp
import traceback
import time

class Addr:
    def __init__(self):
        self.__level = ""
        self.__addr_map = {}
        self.__province = {}
        self.__city = {}
        self.__county = {}
        self.__addr_map["province"] = self.__province
        self.__addr_map["city"] = self.__city
        self.__addr_map["county"] = self.__county
        curr_dir = os.path.split(os.path.realpath(__file__))[0]
        self.addr_keys = {}
        self.full_keys = {}
        self.load(curr_dir + "/../../../conf/address_names.utf8.conf")
        
        #以下地方有歧义
        self.stop_words = [u"河南",u"河北",u"海南"] 
        #以下城市可根据区简称直接判断
        self.prior_citys = [u"北京市",u"上海市",u"深圳市",u"广州市"] 
        #以下符号忽略
        self.skip_words = [u"(",u")",u"（",u"）"]
    def load(self,file_name):
        f = open(file_name)
        while True:
            try:
                line = f.readline()
                line = line.strip()
                if len(line) == 0:
                    break
                line = line.decode("utf-8")
                self.parse_line(line)
            except:
                print traceback.print_exc()

    def check(self):
        key_num = 0
        for item in self.addr_keys:
            key_num = key_num + self.addr_keys[item]
            #if self.addr_keys[item] != 1:
            #    print item.encode("utf-8"),self.addr_keys[item]
        nums = []
        for item in self.__addr_map:
            print item.encode("utf-8"),len(item),len(self.__addr_map[item]),type(self.__addr_map[item])
            #nums.append(len(item))
            num = 0
            for addr in self.__addr_map[item]:
                num = num + len(self.__addr_map[item][addr])
            nums.append(num)
        print "all_key_num",key_num
        for num in nums:
            print "NUM:",num
        print "all_full_key_num",len(self.full_keys)
    def parse_line(self,line):
        if u"[" in line:
            line = line.split(u"[")[0]
            return self.parse_line(line)
        if u"@" in line:
            self.__sign = line.replace("@","")
            if not self.__sign in self.__addr_map[self.__level]:
                self.__addr_map[self.__level][self.__sign] = {}
            return 0 
        if u"#" in line:
            self.__level = line[1:].split(u":")[0]
            return 0 
        items = line.split(" ")
        if len(items) != 2:
            raise SyntaxError("Format Error!!!")
        name = items[0]
        if name in self.addr_keys:
            self.addr_keys[name] = self.addr_keys[name] + 1
        else:
            self.addr_keys[name] = 1
        value = items[1]
        values = []
        for a in value.split(u"|"):
            if len(a) == 0:
                continue
            values.extend(a.split(u"/")) 
        full_name = name + values[0]
        if full_name in self.full_keys:
            raise SyntaxError("Full keys already have!!!")
        else:
            self.full_keys[full_name] = values
        if self.__level == u"province":
            if len(values) == 1:
                if name in self.__province[self.__sign]:
                    print "province already have",line.encode("utf-8")
                else:
                    self.__province[self.__sign][name] = values
            else:
                raise SyntaxError("Format Error!!!")
        elif self.__level == u"city":
            if len(values) == 2:
                if name in self.__city[self.__sign]:
                    print "city already have",line.encode("utf-8")
                else:
                    self.__city[self.__sign][name] = values
            else:
                raise SyntaxError("Format Error!!!")
        elif self.__level == u"county":
            if (len(values) - 1)%2 == 0:
                if name in self.__county[self.__sign]:
                    print "county already have",line.encode("utf-8")
                else:
                    self.__county[self.__sign][name] = values
            else:
                raise SyntaxError("Format Error!!!")
        else:
            raise SyntaxError("Format Error!!!")
    def print_map(self):
        print json.dumps(self.__province,ensure_ascii=False).encode("utf-8")
        print json.dumps(self.__city,ensure_ascii=False).encode("utf-8")
        #print json.dumps(self.__county,ensure_ascii=False).encode("utf-8")

    def add_to_res(self,a, b):
        if b in a:
            a[b] = a[b] + 1
        else:
            a[b] = 1
    def is_skip_word(self,str):
        if len(str) == 0:
            return True
        for item in self.skip_words:
            if item == str:
                return True
        return False
    def parse_word(self,word,post_fix,parse_res,amb_list,word_res):
        has_parsed = False
        #for (level,level_dict) in self.__addr_map.items():
        for level in ("province","city","county"):
            for (prefix,pre_list) in self.__addr_map[level].items():
                if not pre_list.has_key(word):
                    continue
                #先解析带后缀的
                if len(post_fix) > 0 and post_fix == pre_list[word][0]:
                    if level != "county" or len(pre_list[word]) == 3:
                        has_parsed = True
                        parse_res.append(word+pre_list[word][0])
                        parse_res.append(level)
                        word_res.extend(pre_list[word])
                        #print "len(word_res)",len(word_res)
                        break
                #再解析没有歧义的
                if self.addr_keys[word] == 1 and level != "county":
                    has_parsed = True
                    parse_res.append(word+pre_list[word][0])
                    parse_res.append(level)
                    word_res.extend(pre_list[word])
                    #print "len(word_res)",len(word_res)
                    break
                #剩余的都是有歧义的
                amb_list.append(pre_list[word])
            if has_parsed:
                break
        return has_parsed

    def parse_address(self,input_str):
        parse_res = []
        if len(input_str) == 0:
            return parse_res
        no_key = True
        for key in self.addr_keys.keys():
            if key in input_str:
                no_key = False
        if no_key:
            return []
        #print input_str.encode("utf-8")
        words = nlp.word_seg_post(input_str)
        #print words
        #print json.dumps(words,ensure_ascii=False).encode("utf-8")
        if not "basic" in words:
            return result
        words = words["basic"]
        for i in range(0,len(words)):
            word = words[i].strip()
            if self.is_skip_word(word):
                continue
            if len(parse_res) >= 2 and word in parse_res[len(parse_res) - 2]:
                continue
            post_fix = ""
            if i != len(words) - 1:
                post_fix = words[i+1].strip()
            amb_list = [] 
            word_res = []
            if self.parse_word(word,post_fix,parse_res,amb_list,word_res):
                #助上消歧
                #print word.encode("utf-8"),post_fix.encode("utf-8"),len(word_res),len(parse_res)
                if len(parse_res) >= 4 and parse_res[len(parse_res) - 3] == "AMB":
                    for i in range(1,len(word_res)):
                        if parse_res[len(parse_res) - 4] in word_res[i]:
                            parse_res[len(parse_res) - 4] = word_res[i]
                            if i % 2 == 1:
                                parse_res[len(parse_res) - 3] = "province"
                            else:
                                parse_res[len(parse_res) - 3] = "city"
                continue
            #借上消歧
            if len(amb_list) == 0:
                parse_res.append(word)
                parse_res.append("UNK")
                continue
            if len(parse_res) < 2:
                parse_res.append(word)
                parse_res.append("AMB")
                continue
            last_sign = parse_res[len(parse_res) - 1]
            last_word = parse_res[len(parse_res) - 2]
            level = ""
            post_fix = ""
            #print "len(amb_list)",len(amb_list)
            #print "last_word",last_word.encode("utf-8")
            for item in amb_list:
                if not last_word in item:
                    continue
                post_fix = item[0]
                if len(item) == 1:
                    level = "province"
                elif len(item) == 2:
                    level = "city"
                else:
                    level = "county"
                break
            if len(level) > 0:
                parse_res.append(word+post_fix)
                parse_res.append(level)
            else:
                parse_res.append(word)
                parse_res.append("AMB")
        return parse_res
 
    def parse_city(self,input_str):
        if len(input_str) > 1024 * 4:
            return ("","STR_TOO_LONG")
        res_list = self.parse_address(input_str)
        if len(res_list) == 0:
            return ("","NO_CITY")
        if len(res_list) % 2 != 0:
            return ("","PARSE_ERROR")
        result = {"province":{},"city":{}}
        index = 1
        while index <= len(res_list) - 1:
            if res_list[index] == "province":
                self.add_to_res(result["province"],res_list[index - 1])
            elif res_list[index] == "city":
                self.add_to_res(result["city"],res_list[index - 1])
            elif res_list[index] == "county":
                if index - 3 >= 0 and res_list[index - 2] == "city":
                    index = index + 2
                    continue
                values = self.full_keys[res_list[index - 1]]
                if len(values) == 3:
                    if len(values[1]) > 0:
                        self.add_to_res(result["province"],values[1])
                    if len(values[2]) > 0:
                        self.add_to_res(result["city"],values[2])
                elif index - 3 >= 0 and res_list[index - 2] == "province":
                    for i in range(len(values)):
                        if values[i] == res_list[index - 3]:
                            self.add_to_res(result["city"],values[i + 1])
            index = index + 2
        #print input_str.encode("utf-8")
        tmp_province = []
        for city in result["city"]:
            province = self.full_keys[city][1]
            if len(province) > 0:
                tmp_province.append(province)
        for province in result["province"].keys():
            if not province in tmp_province:
                return ("","TOO_MUCH_PROVINCE")
        #print json.dumps(result,ensure_ascii=False).encode("utf-8")
        if len(result["city"]) > 1:
            #print >>sys.stderr,"TOO MUCH CITY"
            return ("","TOO_MUCH_CITY")
        elif len(result["city"]) == 0:
            #print >>sys.stderr,"NO CITY"
            return ("","NO_CITY")
        else:
            return (result["city"].items()[0][0],"")


if __name__ == "__main__":
    print os.path.split(os.path.realpath(__file__))[0]
    address = Addr()
    #address.check()
    addrs = []
    addrs.append(u"(北京)人民大会堂")
    addrs.append(u"(北京)朝阳区")
    addrs.append(u"(北京)朝阳")
    addrs.append(u"北京海淀")
    addrs.append(u"海淀")
    addrs.append(u"详见内页")
    addrs.append(u"河南省洛阳")
    addrs.append(u"阿拉善左")
    addrs.append(u"清浦区")
    addrs.append(u"西安区")
    addrs.append(u"黑龙江西安区")
    addrs.append(u"朝阳")
    addrs.append(u"河南")
    addrs.append(u"河南洛阳")
    addrs.append(u"朝阳")
    addrs.append(u"北京朝阳")
    addrs.append(u"辽宁朝阳")
    addrs.append(u"长春朝阳")
    addrs.append(u"湖北崇阳")
    addrs.append(u"崇阳")
    addrs.append(u"河北）裕华区 青园街塔南路交口北行100米路东“登瀛楼酒店”地下")
    addrs.append(u"详见内页")
    addrs.append(u"北京）河北省张家口市崇礼县太子城梧桐大道 查看地图")
    addrs.append(u"北京）北京市朝阳区百子湾路今日美术馆")
    addrs.append(u"湖北 河北省张家口市崇礼县太子城梧桐大道 查看地图")
    start = time.time()
    for addr in addrs:
        #parse_res = address.parse_address(addr)
        parse_res = address.parse_city(addr)
        result = {}
        result[addr] = parse_res
        print json.dumps(result,ensure_ascii=False).encode("utf-8")
    end = time.time()
    print "time_count:", end - start, len(addrs), (end - start)/(len(addrs) + 0.1) 





