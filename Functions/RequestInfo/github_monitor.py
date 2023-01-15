#!/usr/bin/python3
# -*- coding:utf-8 -*-
# @Author : 小艾、reader-l

import datetime
import requests
import configparser
from Functions.Commons.translate import get_cve_des_zh
#企业微信API相关配置
from Functions.Commons.wechat_api import wechat_qiye

cfg=configparser.ConfigParser()
cfg.read('config.ini',encoding='utf-8')   #读取配置文件 防止乱码
cfg.defaults()						  #默认配置的内容 可以当字典用
list(cfg)
git_headers = cfg['github']['github_headers']
github_headers = {
    'Authorization': git_headers  # 替换自己的github token     https://github.com/settings/tokens/new
}
#获取GitHub知名issues最新信息
def github_iss_data(projects_owner,projects_name,last_iss_number):

    # 定义列表
    req_iss_list = []
    try:
        # 请求API
        api_issues = "https://api.github.com/repos/{}/{}/issues".format(projects_owner,projects_name)
        req_iss = requests.get(api_issues, headers=github_headers, timeout=10).json()
        req_iss_number = req_iss[0]['number']
       # print(req_iss)


        #判断是否推送
        if req_iss_number != last_iss_number:
            #推送
            last_iss_number = req_iss_number
            #写进列表
            req_iss_url = req_iss[0]['html_url']
            req_iss_title = req_iss[0]['title']
            req_iss_state = req_iss[0]['state']
            req_iss_created_at = req_iss[0]['created_at']
            req_iss_updated_at = req_iss[0]['updated_at']
            req_iss_list.append(req_iss_url)
            req_iss_list.append(req_iss_title)
            req_iss_list.append(req_iss_state)
            req_iss_list.append(req_iss_created_at)
            req_iss_list.append(req_iss_updated_at)
    except Exception:
        print("超时")
    return req_iss_list,last_iss_number

#自定义issues推送内容
def wechat_iss_data(touser,agentid,Secret, corpid,owner,project,last_total_count):
    # year = str(datetime.datetime.now().year)
    # month = str(datetime.datetime.now().month)
    # day = str(datetime.datetime.now().day)

    iss_data,lss = github_iss_data(owner,project,last_total_count)
    if len(iss_data) != 0:
        data = {
            # "chatid" : "xxx",
             "touser" : touser,   # 向这些用户账户发送
            #"toparty": toparty,  # 向群聊部门发送
            "msgtype" : "text",
            "agentid": agentid,  # 应用的 id 号
            "text" : {
                "content" : "github知名项目"+project+"新issue已出现\n issues_url: "+iss_data[0]+"\n"+"title: "+iss_data[1]+"\n"+"状态: "+iss_data[2]+"\n"+"创建时间: "+iss_data[3]+"\n"+"更新时间: "+iss_data[4]+"\n"
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
        wechat_qiye(data, Secret, corpid)

    return lss
#获取GitHub最新cve信息
def github_cve_data(last_total_count):
    github_list = []
    year = datetime.datetime.now().year
    # projects_owner = "spring-projects"
    # projects_name = "spring-boot"
    # 请求API
    try:

        api = "https://api.github.com/search/repositories?q=CVE-{}&sort=updated".format(year)
        req = requests.get(api, headers=github_headers, timeout=10).json()
        total_count = req['total_count']
        #update_time = req['items'][0]['updated_at']
        if total_count != last_total_count:
            # 推送正文内容
            # 推送标题
            last_total_count = total_count
            #text = '新的CVE信息'
            # 获取 cve 名字 ，根据cve 名字，获取描述，并翻译
            cve_name = req['items'][0]['name']
            cve_updated_at = req['items'][0]['updated_at']
            # print(cve_name)
            cve_zh = get_cve_des_zh(cve_name)
            #msg = "CVE编号：" + cve_name + "\r\n" + "CVE描述：" + cve_zh
            url = req['items'][0]['html_url']
            # print(url)
            # url2 = getNews()[0]
            # 推送微信
            # data = wechat_data(text, msg, url)
            # wechat_qiye(data)
            github_list.append(cve_name)
            github_list.append(url)
            github_list.append(cve_zh)
            github_list.append(cve_updated_at)
    except Exception:
        print("超时")#return github_list
    return github_list,last_total_count



#自定义推送内容
def wechat_data_cve(touser,toparty,agentid,Secret,corpid,last_total_count):
    # year = str(datetime.datetime.now().year)
    # month = str(datetime.datetime.now().month)
    # day = str(datetime.datetime.now().day)
    github_list,lll = github_cve_data(last_total_count)
    #如果不为空
    if len(github_list) != 0:
        data = {
            # "chatid" : "xxx",
             "touser" : touser,   # 向这些用户账户发送
            "toparty": toparty,  # 向群聊部门发送
             "msgtype" : "text",
            "agentid": agentid,  # 应用的 id 号
            "text" : {
                "content" : "github新CVE已出现\n CVE编号: "+github_list[0]+"\n"+"CVE相关地址: "+github_list[1]+"\n"+"CVE描述: "+github_list[2]+"\n"+"更新时间: "+github_list[3]+"\n"
            },
            # "msgtype": "textcard",
            # "textcard": {
            #     "title": "GitHub有人发布CVE相关信息啦",
            #     "description": "<div class=\"gray\">"+year+"年"+month+"月"+day+"日</div> <div class=\"normal\">"+text+"</div><div class=\"highlight\">"+msg+"</div>",
            #     "url": cve_url,
            #     "btntxt": "获取GitHub最新CVE资料"
            # },
            "safe": 0
        }
        print(data)
        wechat_qiye(data, Secret, corpid)
    return lll