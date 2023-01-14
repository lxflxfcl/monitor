#!/usr/bin/python3
# -*- coding:utf-8 -*-
# @Author : 小艾、reader-l

import datetime

import requests


ms_url = 'https://api.msrc.microsoft.com/sug/v2.0/zh-CN/vulnerability'
def getMSDATA(ms_url,cve_nums):
    header = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36',
        'Connection': 'keep-alive', }
    json_str = requests.get(ms_url, headers=header, timeout=30).json()
    cve_info_MS = []
    count = json_str['@odata.count']
    #print(count)
    release_date = json_str['value'][cve_nums]['releaseDate']
    cve_info_MS.append(str(release_date))
    #print(release_date)
    cve_number = json_str['value'][cve_nums]['cveNumber']
    cve_info_MS.append(str(cve_number))
    #print(cve_number)
    cve_title = json_str['value'][cve_nums]['cveTitle']
    cve_info_MS.append(str(cve_title))
    #print(cve_title)
    desc = json_str['value'][cve_nums]['description']
    cve_info_MS.append(str(desc))
    #print(desc)
    mitre_url = json_str['value'][cve_nums]['mitreUrl']
    cve_info_MS.append(str(mitre_url))
    #print(mitre_url)
    tag = json_str['value'][cve_nums]['tag']
    cve_info_MS.append(str(tag))
    #print(tag)
    #print(cve_info_MS)
    return cve_info_MS
#自定义推送数据格式和内容
def wechat_MS(touser,toparty,agentid,urls):

    year = str(datetime.datetime.now().year)
    month = str(datetime.datetime.now().month)
    day = str(datetime.datetime.now().day)
    flag = str(datetime.datetime.now().date()) +"_ms"
    data = {
        # "chatid" : "xxx",
        "touser": touser,  # 向这些用户账户发送
         "toparty": toparty,  # 向群聊部门发送
        # "msgtype" : "text",
        "agentid": agentid,  # 应用的 id 号
        # "text" : {
        #     "content" : "一看到你，我就泛起微笑^_^。"
        # },
        "msgtype": "textcard",
        "textcard": {
            "title": "微软官方发布最新的CVE漏洞信息啦",
            "description": "<div class=\"gray\">" + year + "年" + month + "月" + day + "日</div> <div class=\"normal\">最新官方微软漏洞情报</div><div class=\"normal\">请注意查收</div><div class=\"highlight\">新鲜的</div>",
            "url": urls+flag+".html",
            "btntxt": "获取最新"
        },
        "safe": 0
    }
    return data, data['textcard']['title'], data['textcard']['url']

