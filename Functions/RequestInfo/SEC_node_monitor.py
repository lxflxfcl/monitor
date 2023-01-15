# -*- coding: UTF-8 -*-
#megaload 2019.05.08
#import requests
import configparser
import re
import urllib.request
import feedparser
import time
import datetime
from bs4 import BeautifulSoup
import datetime as d
import json
#import execjs
from Functions.Commons.wechat_api import wechat_qiye


#get_test = requests.get("https://tttang.com/rss.xml")
SEC_list = []

#奇安信攻防社区文章获取
def get_qax_data(qax_last_time):

    print("奇安信攻防社区监控中。。。")
    qax_list = []
    file_data = feedparser.parse('https://forum.butian.net/Rss')
    #print(file_data)
    data = file_data.entries
    time_published = data[0]['published']
    # 先转换为时间数组
    print(time_published)
    timeArray = time.strptime(time_published, "%Y-%m-%d %H:%M:%S")
    # 转换为时间戳
    timeStamp = int(time.mktime(timeArray))
    print(timeStamp)
    if timeStamp != qax_last_time:
        #推送
        qax_last_time = timeStamp
        data_title = data[0]['title']
        data_link = data[0]['link']
        data_pubDate = data[0]['published']
        qax_list.append(data_title)
        qax_list.append(data_link)
        qax_list.append(data_pubDate)
    return qax_list,qax_last_time

#跳跳糖社区文章获取
def get_ttt_data(ttt_last_time):
    print("跳跳糖社区监控中。。。")
    ttt_list = []
    file_data = feedparser.parse('https://tttang.com/rss.xml')
    #print(file_data)
    data = file_data.entries
    time_data = data[0]['published']
    # 先转换为时间数组
    print(time_data)
    timeArray = time.strptime(time_data, "%a, %d %b %Y %H:%M:%S +0800")
    # 转换为时间戳
    timeStamp = int(time.mktime(timeArray))
    print(timeStamp)
    if timeStamp != ttt_last_time:
        #推送
        ttt_last_time = timeStamp
        data_title = data[0]['title']
        data_link = data[0]['link']
        data_published = data[0]['published']
        ttt_list.append(data_title)
        ttt_list.append(data_link)
        ttt_list.append(data_published)
    return ttt_list,ttt_last_time

#先知社区文章获取

def get_xz_data(xz_last_time):

    print("先知社区监控中。。。")
    xz_list = []
    file_data = feedparser.parse('https://xz.aliyun.com/feed')
    #print(file_data)
    data = file_data.entries
    time_data = data[0]['published']
    # 先转换为时间数组
    print(time_data)
    new_t = datetime.datetime.strptime(time_data, "%Y-%m-%dT%H:%M:%S+08:00").strftime("%Y-%m-%d %H:%M:%S")
    # '2023-1-3 17:36:00'
    timeArray = time.strptime(new_t, "%Y-%m-%d %H:%M:%S")
    # 转换为时间戳
    timeStamp = int(time.mktime(timeArray))
    print(timeStamp)
    if timeStamp != xz_last_time:
        #推送
        xz_last_time = timeStamp
        data_title = data[0]['title']
        data_link = data[0]['link']
        #data_published = data[0]['published']
        xz_list.append(data_title)
        xz_list.append(data_link)
        xz_list.append(new_t)
    return xz_list,xz_last_time
#安全文章推送
def wechat_secnote_data(touser,toparty, agentid,Secret, corpid,ttt_last_time,qax_last_time,zx_last_time):
    # year = str(datetime.datetime.now().year)
    # month = str(datetime.datetime.now().month)
    # day = str(datetime.datetime.now().day)
    #跳跳糖数据
    ttt_data,tttlt = get_ttt_data(ttt_last_time)
    #奇安信社区数据
    qax_data,qaxlt = get_qax_data(qax_last_time)
    #先知社区
    xz_data,xzlt = get_xz_data(zx_last_time)
    #推送奇安信社区文章
    if len(qax_data) != 0:
        data = {
            # "chatid" : "xxx",
            "touser": touser,  # 向这些用户账户发送
            "toparty": toparty,  # 向群聊部门发送
            "msgtype": "text",
            "agentid": agentid,  # 应用的 id 号
            "text": {
                "content": "奇安信攻防社区今日更新\n title: " + qax_data[0] + "\n" + "链接: " + qax_data[
                    1] + "\n" + "时间: " + qax_data[2] + "\n"
            },
            # "msgtype": "textcard",
            #  "textcard": {
            #      "title": "GitHub有人发布CVE相关信息啦",
            #      "description": "<div class=\"gray\">"+year+"年"+month+"月"+day+"日</div> <div class=\"normal\">"+text+"</div><div class=\"highlight\">"+msg+"</div>",
            #      "url": cve_url,
            #      "btntxt": "获取GitHub最新CVE资料"
            #  },
            "safe": 0
        }
        print(data)
        #推送微信
        wechat_qiye(data, Secret, corpid)
    #推送跳跳糖文章
    if len(ttt_data) != 0:
        data = {
            # "chatid" : "xxx",
            "touser": touser,  # 向这些用户账户发送
            "toparty": toparty,  # 向群聊部门发送
            "msgtype": "text",
            "agentid": agentid,  # 应用的 id 号
            "text": {
                "content": "跳跳糖社区今日更新\n title: " + ttt_data[0] + "\n" + "链接: " + ttt_data[
                    1] + "\n" + "时间: " + ttt_data[2] + "\n"
            },
            # "msgtype": "textcard",
            #  "textcard": {
            #      "title": "GitHub有人发布CVE相关信息啦",
            #      "description": "<div class=\"gray\">"+year+"年"+month+"月"+day+"日</div> <div class=\"normal\">"+text+"</div><div class=\"highlight\">"+msg+"</div>",
            #      "url": cve_url,
            #      "btntxt": "获取GitHub最新CVE资料"
            #  },
            "safe": 0
        }
        print(data)
        #推送微信
        wechat_qiye(data, Secret, corpid)

    # 推送先知社区
    if len(xz_data) != 0:
        data = {
            # "chatid" : "xxx",
            "touser": touser,  # 向这些用户账户发送
            "toparty": toparty,  # 向群聊部门发送
            "msgtype": "text",
            "agentid": agentid,  # 应用的 id 号
            "text": {
                "content": "先知社区今日更新\n title: " + xz_data[0] + "\n" + "链接: " + xz_data[
                    1] + "\n" + "时间: " + xz_data[2] + "\n"
            },
            # "msgtype": "textcard",
            #  "textcard": {
            #      "title": "GitHub有人发布CVE相关信息啦",
            #      "description": "<div class=\"gray\">"+year+"年"+month+"月"+day+"日</div> <div class=\"normal\">"+text+"</div><div class=\"highlight\">"+msg+"</div>",
            #      "url": cve_url,
            #      "btntxt": "获取GitHub最新CVE资料"
            #  },
            "safe": 0
        }
        print(data)
        # 推送微信
        wechat_qiye(data, Secret, corpid)
    return tttlt,qaxlt,xzlt
