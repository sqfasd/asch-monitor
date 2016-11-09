# -*- coding: UTF-8 -*-
"""
发送txt文本邮件
"""
import smtplib
from email.mime.text import MIMEText

mailto_list = ['5871562@qq.com', '409040875@qq.com', '2779476373@qq.com', '582072@qq.com', '316367221@qq.com', '634210195@qq.com', '1963836698@qq.com']


mail_host = "smtp.qq.com"  # 设置服务器
mail_user = "409040875"  # 用户名
mail_pass = ""  # 口令,https方式且第三方登陆需要单独授权
mail_postfix = "qq.com"  # 发件箱的后缀

def send_mail(to_list, sub, content):
    me = "AschMonitor" + "<" + mail_user + "@" + mail_postfix + ">"
    msg = MIMEText(content, _subtype='plain', _charset='utf8')
    msg['Subject'] = sub
    msg['From'] = me
    msg['To'] = ";".join(to_list)
    try:
        #server = smtplib.SMTP()
        server = smtplib.SMTP_SSL()
        #server.connect(mail_host)
        server.connect(mail_host,465)
        server.login(mail_user, mail_pass)
        server.sendmail(me, to_list, msg.as_string())
        server.close()
        return True
    except Exception, e:
        print str(e)
        return False


if __name__ == '__main__':
    sub = 'asch_monitor'
    content = 'hello world!'
    if send_mail(mailto_list, sub, content):
        print "发送成功"
    else:
        print "发送失败"
