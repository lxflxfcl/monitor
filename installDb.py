import sqlite3
import os

'''
    @describe: 用于CVE监控工具的数据库的初始化创建以及存放日志的目录创建
'''

step = 1
if os.path.isfile('cve_db.db'):
    step = 2

if step == 1:
    con = sqlite3.connect("cve_db.db")
    cursor = con.cursor()
    cursor.execute('create table cve_info(vuln_name TEXT, url TEXT, cnnvd_num TEXT, danger_level TEXT, cve_num TEXT, vuln_type TEXT, release_time TEXT, thread_type TEXT, updated_time TEXT, company TEXT, vuln_desc TEXT, vuln_announce TEXT, reference_url TEXT, influnce_product TEXT, patch TEXT)')
    cursor.execute('create table cve_info_ms(release_data TEXT,cve_num TEXT,cve_title TEXT,desc TEXT,mitre_url TEXT,tag TEXT)')
    cursor.close()
    con.commit()
    con.close()
    step = 2

if step == 2:
    if os.path.isdir('log'):
        print("log目录已存在！！")
        print("安装完成！！")
    else:
        os.mkdir('log') #创建用于存放日志的目录
        print('创建了log目录！！')
        print("安装完成！！")