# -*- coding:utf-8 -*-


#企业微信消息推送
import datetime
import json

import requests

access_token = ''
def wechat_qiye(data,Secret,corpid):

    global access_token
    # 自定义应用的 Secret
    #Secret = secret
    # 注册的企业 corpid
    #corpid = corpid
    url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={}&corpsecret={}'

    '''
        先提供Secret以及corpid获取access_token。
    '''
    if access_token == '':

        getr = requests.get(url=url.format(corpid, Secret))
        access_token = getr.json().get('access_token')


    print(access_token)


    r = requests.post(url="https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={}".format(access_token),
                          data=json.dumps(data))
    print(r.text)
    if str(json.loads(r.text)['errmsg']) != 'ok':
        #获取新的access_token
        getr = requests.get(url=url.format(corpid, Secret))
        access_token = getr.json().get('access_token')
        #恢复之前因token过期异常失去的请求
        r = requests.post(url="https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={}".format(access_token),
                          data=json.dumps(data))
        print(r.text)