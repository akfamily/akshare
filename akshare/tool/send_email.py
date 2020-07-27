# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2020/5/4 13:58
Desc: 发送提醒邮件邮件
"""
import smtplib
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email(msg: str, from_email: str, password: str, to_email: str, host: str, port: str, attach_name=False,
               attach_root: bool = False, ssl: bool = False):
    """
    发送提醒邮件
    :param msg: string 邮件的主题
    :param from_email: string 发送邮件的邮箱
    :param password: string 发送邮件的密码
    :param to_email: string 接收邮件的邮箱
    :param host: string 邮箱服务器地址(邮箱服务商查询)
    :param port: string 端口(邮箱服务商查询)
    :param attach_name: string 单个附件名字 / list 多个附件名字列表
    :param attach_root: 附件本机目录
    :param ssl: bool 是否使用ssl加密协议(QQ邮箱需要使用)
    :return: None
    """
    message = MIMEMultipart()
    message['From'] = from_email
    message['To'] = to_email
    message['Subject'] = Header(msg)

    if bool(attach_name) and bool(attach_root):
        if isinstance(attach_name, str):
            part = MIMEText(open(attach_root + attach_name, 'rb').read(), 'base64', 'utf-8')
            part.add_header('Content-Disposition', 'attachment', filename=attach_name)
            message.attach(part)
        elif isinstance(attach_name, list):
            for name in attach_name:
                part = MIMEText(open(attach_root + name, 'rb').read(), 'base64', 'utf-8')
                part.add_header('Content-Disposition', 'attachment', filename=name)
                message.attach(part)
    if ssl:
        smtp_obj = smtplib.SMTP_SSL()
    else:
        smtp_obj = smtplib.SMTP()
    smtp_obj.connect(host, port)
    smtp_obj.login(from_email, password)
    smtp_obj.sendmail(from_email, to_email, message.as_string())


if __name__ == "__main__":
    send_email()
