#!/bin/env python
#-*- coding: utf-8 -*-
import sys
from optparse import OptionParser
import string
import json
import urllib
import urllib2
import time

#post_url = "http://localhost/api"
post_url = "http://localhost:8080/futureinst/api"

post_num = 0
post_time = 0
def post(origin_query):
    global post_num,post_time
    start = time.time()
    query_json = json.loads(origin_query,"utf-8")
    data_json = {}
    if "method" in query_json and "type" in query_json and "query" in query_json:
        data_json["method"] = query_json["method"][0]
        data_json["type"] = query_json["type"][0]
        data_json["query"] = (string)(query_json["query"][0]).encode("utf-8")
    data = urllib.urlencode(data_json)
    req = urllib2.Request(post_url, data)
    response = urllib2.urlopen(req)
    the_page = response.read()
    reslen = len(the_page)
    end = time.time()
    post_num = post_num + 1
    post_time = post_time + (end - start)
    print "%s\t%d\t%d" % (method, end - start, reslen)

method_name_dict = {
        "add_article":"添加文章",
        "update_article":"更新文章",
        "operate_article":"操作文章（阅读、点赞、打赏等）", 
        "add_comment_for_article":"给文章添加评论", 
        "query_comment_for_article":"查看观点的评论", 
        "query_user_article":"查看用户发表的文章",
        "query_top_article":"查看发现栏目的观点",
        "peer_info_query_user_article":"查看他人发表的文章",
        "query_user_news":"查看动态",
        "add_comment":"添加评论",
        "add_download":"下载",
        "add_event_feed":"添加征集事件",
        "add_feedback":"添加反馈",
        "add_order":"添加订单",
        "get_faq":"查看常见问题",
        "get_rank":"查看排名",
        "peer_info_query_event_clear":"查看别人战绩列表",
        "peer_info_query_event_trade":"查看别人预测中事件",
        "peer_info_query_follow_me":"查看关注他的人",
        "peer_info_query_me_follow":"查看他关注的人",
        "peer_info_query_user_record":"查看他人主页",
        "peer_info_query_user_tag_record":"查看他人战绩概览",
        "query_comment":"查看事件的评论",
        "query_event":"查看事件列表【老版】",
        "query_event_all":"查看事件列表",
        "query_event_clear":"查看我的战绩列表",
        "query_event_feed":"查看我的征集事件列表",
        "query_follow":"查看关注的事件列表",
        "query_follow_me":"查看我关注的人",
        "query_gift":"查看礼物列表",
        "query_me_follow":"查看关注我的人",
        "query_order":"查看我的订单",
        "query_single_event":"查看事件详情页",
        "query_single_gift":"查看礼物详情页",
        "query_user_check":"查看对账单",
        "query_user_exchange":"查看兑换记录",
        "query_user_record":"查看我的主页",
        "query_user_tag_record":"查看我的战绩概览",
}

while True:
    line = str(sys.stdin.readline())
    if len(line) == 0 :
        break
    items = line.split('\t')
    if len(items) < 11:
        print "len(items):",len(items)
        continue
    method = items[2]
    if not method in method_name_dict:
        continue
    query = items[10] 
    post(query)

print post_num,post_time,(post_time)/(post_num) 
