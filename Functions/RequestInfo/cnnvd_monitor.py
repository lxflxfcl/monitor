#!/usr/bin/python3
# -*- coding:utf-8 -*-
# @Author : 小艾、reader-l

import datetime

import dominate
import requests
from bs4 import BeautifulSoup
import re

#该函数用于获取单独的一条漏洞详细信息

def getURLDATA(url):
    header = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36',
        'Connection': 'keep-alive', }
    r = requests.get(url, headers=header, timeout=30)
    html = BeautifulSoup(r.text, 'html.parser')
    link = html.find(class_='detail_xq w770')  # 漏洞信息详情
    vuln_name = link.find('h2').text.lstrip().rstrip() #漏洞名称
    vuln_num = re.findall(r'CNNVD-+\d+-+\d+',str(url))[0] #漏洞编号
    link_introduce = html.find(class_='d_ldjj')  # 漏洞简介
    link_others = html.find_all(class_='d_ldjj m_t_20')  # 其他
    one_cve_info = []
    #漏洞名称
    try:
        one_cve_info.append(str(vuln_name))
    except:
        one_cve_info.append("")
    #漏洞在CNNVD上的链接
    try:
        one_cve_info.append(str(url))
    except:
        one_cve_info.append("")
    #漏洞在CNNVD上的编号
    try:
        one_cve_info.append(vuln_num)
    except:
        one_cve_info.append("")
    # 危害等级
    try:

        one_cve_info.append(str(link.contents[3].contents[5].find('a').text.lstrip().rstrip()))
    except:
        #print("危害等级:is empty")
        one_cve_info.append("")
    #CVE编号
    try:
        one_cve_info.append(str(link.contents[3].contents[7].find('a').text.lstrip().rstrip()))
    except:
        #print("CVE编号:is empty")
        one_cve_info.append("")
    #漏洞类型
    try:
        one_cve_info.append(str(link.contents[3].contents[9].find('a').text.lstrip().rstrip()))

    except:
        #print("漏洞类型:is empty")
        one_cve_info.append("")

    #发布时间
    try:
        one_cve_info.append(str(link.contents[3].contents[11].find('a').text.lstrip().rstrip()))
    except:
       # print("发布时间:is empty")
        one_cve_info.append("")
    #威胁类型
    try:
        one_cve_info.append(str(link.contents[3].contents[13].find('a').text.lstrip().rstrip()))
    except:
        #print("威胁类型:is empty")
        one_cve_info.append("")

    #更新时间
    try:
        one_cve_info.append(str(link.contents[3].contents[15].find('a').text.lstrip().rstrip()))
    except:
        #print("更新时间:is empty")
        one_cve_info.append("")
    #厂商
    try:
        one_cve_info.append(str(link.contents[3].contents[17].find('a').text.lstrip().rstrip()))
    except:
        #print("厂商:is empty")
        one_cve_info.append("")

    #漏洞简介
    try:
        link_introduce_data = BeautifulSoup(link_introduce.decode(), 'html.parser').find_all(name='p')
        s = ""
        for i in range(0, len(link_introduce_data)):
            s = s + str(link_introduce_data[i].text.lstrip().rstrip())
        one_cve_info.append(s)
    except:
        one_cve_info.append("")

    if (len(link_others) != 0):
        try:
            # 漏洞公告
            link_others_data1 = BeautifulSoup(link_others[0].decode(), 'html.parser').find_all(name='p')
            s = ""
            for i in range(0, len(link_others_data1)):
                s = s + str(link_others_data1[i].text.lstrip().rstrip())
            one_cve_info.append(s)
        except:
            one_cve_info.append("")

        try:
            # 参考网址
            link_others_data2 = BeautifulSoup(link_others[1].decode(), 'html.parser').find_all(name='p')
            s = ""
            for i in range(0, len(link_others_data2)):
                s = s + str(link_others_data2[i].text.lstrip().rstrip())

            one_cve_info.append(s)
        except:
            one_cve_info.append("")

        try:
            # 受影响实体
            link_others_data3 = BeautifulSoup(link_others[2].decode(), 'html.parser').find_all('a', attrs={
                'class': 'a_title2'})
            s = ""
            for i in range(0, len(link_others_data3)):
                s = s + str(link_others_data3[i].text.lstrip().rstrip())

            one_cve_info.append(s)
        except:
            one_cve_info.append("")

        try:
            # 补丁
            link_others_data3 = BeautifulSoup(link_others[3].decode(), 'html.parser').find_all('a', attrs={
                'class': 'a_title2'})
            s = ""
            for i in range(0, len(link_others_data3)):
                s = s + str(link_others_data3[i].text.lstrip().rstrip())

            one_cve_info.append(s)
        except:
            one_cve_info.append("")
    else:
        one_cve_info.append("")
        one_cve_info.append("")
        one_cve_info.append("")
        one_cve_info.append("")
    return one_cve_info


def slack_messge():
    pass



#自定义推送数据格式和内容
def wechat_cnnvd(lever_test,touser,toparty,agentid,urls):
    year = str(datetime.datetime.now().year)
    month = str(datetime.datetime.now().month)
    day = str(datetime.datetime.now().day)
    flag = str(datetime.datetime.now().date()) +"_cnnvd"
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
            "title": "今天的CVE到啦",
            "description": "<div class=\"gray\">"+year+"年"+month+"月"+day+"日</div> <div class=\"normal\">最新CNNVD漏洞情报</div><div class=\"highlight\">"+lever_test+"</div><div class=\"highlight\">请注意查收，嘿嘿嘿</div>",
            "url": urls +flag+".html",
            "btntxt": "获取最新CNNVD的文件"
        },
        "safe": 0
    }
    return data, data['textcard']['title'], data['textcard']['url']



