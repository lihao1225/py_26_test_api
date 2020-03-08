'''
=======================
Author:李浩
时间：2020/3/5:11:57
Email:lihaolh_v@didichuxing.com
=======================
'''

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from commom.myconfig import conf

"""
smtp服务器：
smtp服务器地址：
qq邮箱：smtp.qq.com  端口：465
163邮箱：smtp.163.com  端口：465


账号：969900918@qq.com     
授权码：pxnbupotjqoabdbj


"""

def send_email(file_name,title):

    #第一步：链接邮箱的smtp服务器，并登陆
    smtp =smtplib.SMTP_SSL(host=conf.get("email","host"),port=conf.getint("email","port"))
    smtp.login(user=conf.get("email","user"),password=conf.get("email","pwd"))
    #第二步：构建一封邮件
    #创建一封多组件的邮件
    msg = MIMEMultipart()

    with open(file_name,"rb") as f :
        content = f.read()
    # 创建邮件文本内容
    text_msg = MIMEText(content,_subtype="html",_charset="utf8")
    #添加到多组件的邮件中
    msg.attach(text_msg)
    #创建邮件的附件
    report_file = MIMEApplication(content)
    #截取文件名
    (path,file_name1) = os.path.split(file_name)
    report_file.add_header('content-disposition', 'attachment', filename=file_name1)
    #将附件添加到多组件邮件中
    msg.attach(report_file)
    # 发件主题
    msg["Subject"] = title
    #发件人
    msg["From"] = conf.get("email","from_addr")
    #收件人
    msg["To"] = conf.get("email","to_addr")

    # 第三步发送邮件
    smtp.send_message( msg, from_addr=conf.get("email","from_addr"), to_addrs=conf.get("email","to_addr") )