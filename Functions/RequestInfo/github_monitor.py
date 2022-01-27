#!/usr/bin/python3
# -*- coding:utf-8 -*-
# @Author : 小艾、reader-l

import datetime


#自定义推送内容
def wechat_data(touser,toparty,agentid,text,msg,cve_url):
    year = str(datetime.datetime.now().year)
    month = str(datetime.datetime.now().month)
    day = str(datetime.datetime.now().day)
    data = {
        # "chatid" : "xxx",
         "touser" : touser,   # 向这些用户账户发送
        "toparty": toparty,  # 向群聊部门发送
        # "msgtype" : "text",
        "agentid": agentid,  # 应用的 id 号
        # "text" : {
        #     "content" : "一看到你，我就泛起微笑^_^。"
        # },
        "msgtype": "textcard",
        "textcard": {
            "title": "GitHub有人发布CVE相关信息啦",
            "description": "<div class=\"gray\">"+year+"年"+month+"月"+day+"日</div> <div class=\"normal\">"+text+"</div><div class=\"highlight\">"+msg+"</div>",
            "url": cve_url,
            "btntxt": "获取GitHub最新CVE资料"
        },
        "safe": 0
    }
    return data


