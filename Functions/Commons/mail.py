
import smtplib
from email.mime.text import MIMEText
from email.header import Header

def main_user(data):
    # 第三方 SMTP 服务
    mail_host = "smtp.qq.com"  # 设置服务器
    mail_user = "19********1@qq.com"  # 用户名
    mail_pass = "lp*********bgmbgbc"  # 口令

    sender = '19********1@qq.com'
    receivers = ['1628****871@qq.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
    #发送内容
    mail_msg = '<a href=" '+data+'     ">最新漏洞情报</a>'
    print(mail_msg)
    print(mail_msg[43])
    #文本格式：plain
    message = MIMEText( mail_msg, 'html', 'utf-8')
    message['From'] = Header("CVE小助手", 'utf-8')
    message['To'] = Header("测试", 'utf-8')
    if mail_msg[43] == 'c':

        subject = '最新CNNVD漏洞情报邮件通知'
        message['Subject'] = Header(subject, 'utf-8')
    elif mail_msg[43] == 'm':
        subject = '最新微软官方漏洞情报邮件通知'
        message['Subject'] = Header(subject, 'utf-8')

    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host, 25)  # 25 为 SMTP 端口号
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        print("邮件发送成功")
    except smtplib.SMTPException:
        print("Error: 无法发送邮件")


