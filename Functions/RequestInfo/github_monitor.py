#!/usr/bin/python3
# -*- coding:utf-8 -*-
# @Author : 小艾


import datetime


github_headers = {
    'Authorization': "ghp_ZnuvJ************************t2KhQqN"  # 替换自己的github token     https://github.com/settings/tokens/new
}

#自定义推送内容
def wechat_data(text,msg,cve_url):

    data = {
        # "chatid" : "xxx",
        # "touser" : "Li********ng",   # 向这些用户账户发送
        "toparty": "1",  # 向群聊部门发送
        # "msgtype" : "text",
        "agentid": 1000003,  # 应用的 id 号
        # "text" : {
        #     "content" : "一看到你，我就泛起微笑^_^。"
        # },
        "msgtype": "textcard",
        "textcard": {
            "title": "GitHub有人发布CVE相关信息啦",
            "description": "<div class=\"gray\">"+str(datetime.datetime.now().year)+"年"+str(datetime.datetime.now().month)+"月"+str(datetime.datetime.now().day)+"日</div> <div class=\"normal\">"+text+"</div><div class=\"highlight\">"+msg+"</div>",
            "url": cve_url,
            "btntxt": "获取GitHub最新CVE资料"
        },
        "safe": 0
    }
    return data


