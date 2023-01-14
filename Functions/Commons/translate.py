# -*- coding:utf-8 -*-

import hashlib
import time
from lxml import etree

import requests

github_headers = {
    'Authorization': "ghp************************2KhQqN"  # 替换自己的github token     https://github.com/settings/tokens/new
}
# 创建md5对象
def nmd5(str):
    m = hashlib.md5()
    b = str.encode(encoding='utf-8')
    m.update(b)
    str_md5 = m.hexdigest()
    return str_md5


# 有道翻译
def translate(word):
    headerstr = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
    bv = nmd5(headerstr)
    lts = str(round(time.time() * 1000))
    salt = lts + '90'

    # 如果翻译失败，{'errorCode': 50}  请查看 fanyi.min.js: https://shared.ydstatic.com/fanyi/newweb/v1.1.7/scripts/newweb/fanyi.min.js
    # 搜索 fanyideskweb   sign: n.md5("fanyideskweb" + e + i + "Y2FYu%TNSbMCxc3t2u^XT")  ，Y2FYu%TNSbMCxc3t2u^XT是否改变，替换即可
    strexample = 'fanyideskweb' + word + salt + 'Y2FYu%TNSbMCxc3t2u^XT'
    sign = nmd5(strexample)

    data = {
        'i': word,
        'from': 'AUTO',
        'to': 'AUTO',
        'smartresult': 'dict',
        'client': 'fanyideskweb',
        'salt': salt,
        'sign': sign,
        'lts': lts,
        'bv': bv,
        'doctype': 'json',
        'version': '2.1',
        'keyfrom': 'fanyi.web',
        'action': 'FY_BY_CLICKBUTTION',
    }
    url = 'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
    #url = 'http://fanyi.youdao.com/translate'

    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
        'Referer': 'http://fanyi.youdao.com/',
        'Origin': 'http://fanyi.youdao.com',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Host': 'fanyi.youdao.com',
        'cookie': '_ntes_nnid=937f1c788f1e087cf91d616319dc536a,1564395185984; OUTFOX_SEARCH_USER_ID_NCOO=; OUTFOX_SEARCH_USER_ID=-10218418@11.136.67.24; JSESSIONID=; ___rl__test__cookies=1'
    }

    res = requests.post(url=url, data=data, headers=header)
    result_dict = res.json()

    result = ""
    for json_str in result_dict['translateResult'][0]:
        tgt = json_str['tgt']
        result += tgt
    return result

# 根据cve 名字，获取描述，并翻译
def get_cve_des_zh(cve):
    query_cve_url = "https://cve.mitre.org/cgi-bin/cvename.cgi?name=" + cve
    response = requests.get(query_cve_url, headers=github_headers, timeout=10)
    html = etree.HTML(response.text)
    if  html.xpath('//*[@id="GeneratedTable"]/table//tr[4]/td/text()'):
        des = html.xpath('//*[@id="GeneratedTable"]/table//tr[4]/td/text()')[0].strip()
    else:
        des = "The CVE number is abnormal "+cve+"Related"
    print(des)
    return translate(des)
