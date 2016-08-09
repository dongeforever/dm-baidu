#!/bin/env python
#-*- coding: utf-8 -*-
import sys
from optparse import OptionParser
import string

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
        "add_user_by_phone":"手机注册",
        "exchange_gift":"兑换礼品",
        "get_faq":"查看常见问题",
        "get_rank":"查看排名",
        "operate_follow":"关注或分享事件",
        "operation_peer_follow":"关注与取消",
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
        "send_smscode":"发送验证码",
        "sign_in_by_phone":"登录",
        "update_order":"修改订单（撤销）",
        "update_permit":"修改隐私权限",
        "update_user":"修改用户信息",
        "uploadImage":"上传图片"
}

method_pv = {}
ip_dict = {}
all_pv = 0
for name in method_name_dict:
    method_pv[name] = 0

while True:
    line = str(sys.stdin.readline())
    if len(line) == 0 :
        break
    items = line.split('\t')
    name = items[2]
    ip = items[8]
    if name == "query_single_event":
       query = items[10] 
       if query.find("price")  ==  -1:
           continue
    if name in method_pv:
        method_pv[name] = method_pv[name] + 1
        all_pv = all_pv + 1
    if ip in ip_dict:
        ip_dict[ip] = ip_dict[ip] + 1
    else:
        ip_dict[ip] = 1

print "%s\t%d" % ("独立IP数",len(ip_dict))
print "%s\t%d" % ("访问请求数",all_pv)
for item in sorted(method_pv.items(),key = lambda a:a[1], reverse=True):
    print  "%d\t%s\t%s" % (item[1], method_name_dict[item[0]], item[0])


