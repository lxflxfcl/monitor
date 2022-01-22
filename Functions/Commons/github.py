# -*- coding:utf-8 -*-

# 抓取本年cve
import datetime

import requests
github_headers = {
    'Authorization': "ghp_Znu************************t2KhQqN"  # 替换自己的github token     https://github.com/settings/tokens/new
}

def getNews():
    try:
        # 抓取本年的
        year = datetime.datetime.now().year
        api = "https://api.github.com/search/repositories?q=CVE-{}&sort=updated".format(year)
        json_str = requests.get(api, headers=github_headers, timeout=10).json()
        cve_total_count = json_str['total_count']
        cve_description = json_str['items'][0]['description']
        cve_url = json_str['items'][0]['html_url']
        #print(cve_url)
        return cve_total_count, cve_description, cve_url


    except Exception as e:
        print(e, "github链接不通")
        return '', '', ''