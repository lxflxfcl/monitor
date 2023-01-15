# -*- coding:utf-8 -*-
import configparser
import sys
import datetime
import os
import dominate
from dominate.tags import *

cfg=configparser.ConfigParser()
cfg.read('config.ini',encoding='utf-8')   #读取配置文件 防止乱码
cfg.defaults()						  #默认配置的内容 可以当字典用
list(cfg)
linux_path = cfg['linuxpath']['path']
#保存文件的路径
if sys.platform == "win32":
    dir_mon = "{home}\\data\\".format(home=os.path.expanduser('~'))
else:
    dir_mon = linux_path
   
# 创建excel生成静态html页面的函数
def list_diction_to_html_cnnvd(list_work):
    # 用dominate函数生成静态html页面
    doc = dominate.document(title='最新CVE列表')
    # 写在头部的 css 可以自定义自己的想要用的css文件， （重要： meta一定要加 要不会在打开html时乱码，因为html默认不是utf-8编码）
    with doc.head:
        #stylesheet
        #Perconnel / static / css / style.css
        link(href='style.css', rel='stylesheet', type='text/css')
        meta(charset='utf-8')
    # 创建一个table，将获取到的数据通过遍历添加进去对应的位置
    with doc:
        with div(id='excel_table').add(table(id="qgg-table",border="1px solid #ccc" ,cellspacing="0", cellpadding="0")):
            with thead():
                dict = list_work[0]
                for key in dict.keys():
                    table_header = td()
                    table_header.add(p(key))
            for dict2 in list_work:
                if dict2['危害等级'] == '高危':
                    table_row = tr(cls='excel_table_row',bgcolor='#FF0000')
                elif dict2['危害等级'] == '超危':
                    table_row = tr(cls='excel_table_row',bgcolor='#FF0000')
                else:
                    table_row = tr(cls='excel_table_row')
                for key in dict2:
                    with table_row.add(td()):
                        p(dict2[key])
    return str(doc)
# 创建excel生成静态html页面的函数
def list_diction_to_html_ms(list_work):
    # 用dominate函数生成静态html页面
    doc = dominate.document(title='最新微软CVE列表')
    # 写在头部的 css 可以自定义自己的想要用的css文件， （重要： meta一定要加 要不会在打开html时乱码，因为html默认不是utf-8编码）
    with doc.head:
        #stylesheet
        #Perconnel / static / css / style.css
        link(href='style.css', rel='stylesheet', type='text/css')
        meta(charset='utf-8')
    # 创建一个table，将获取到的数据通过遍历添加进去对应的位置
    with doc:
        with div(id='excel_table').add(table(id="qgg-table",border="1px solid #ccc" ,cellspacing="0", cellpadding="0")):
            with thead():
                dict = list_work[0]
                for key in dict.keys():
                    table_header = td()
                    table_header.add(p(key))
            for dict2 in list_work:
                table_row = tr(cls='excel_table_row')
                for key in dict2:
                    with table_row.add(td()):
                        p(dict2[key])
    return str(doc)

#保存HTML文件
def save_dom_to_html_cnnvd(dom):
    today_time = str(datetime.datetime.now().date()) + "_cnnvd"
    filepath = os.path.abspath(dir_mon+str(today_time)+".html")
    print(filepath)
    htmfile = open(filepath, "w",encoding='utf-8')
    htmfile.write(str(dom))
    htmfile.close()

def save_dom_to_html_ms(dom):
    today_time = str(datetime.datetime.now().date()) + "_ms"
    filepath = os.path.abspath(dir_mon+str(today_time)+".html")
    print(filepath)
    htmfile = open(filepath, "w",encoding='utf-8')
    htmfile.write(str(dom))
    htmfile.close()
