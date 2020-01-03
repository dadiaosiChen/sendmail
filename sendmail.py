#coding: utf-8
import configparser
import os
import subprocess
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

#获取当前工作目录，用于拼接配置文件目录
workpath = os.getcwd()
#print workpath+'\\config.ini'
cf = configparser.ConfigParser()
cf.read(workpath+os.sep+'config.ini')


mail_to = cf.get("Email", "mail_to")
mail_host = cf.get("Email", "mail_host")
mail_user = cf.get("Email", "mail_user")
mail_pass = cf.get("Email", "mail_pass")
mail_host_port = cf.get("Email", "mail_host_port")




# 注意邮件发送格式中 From 和 To的字段，一定要写成类似于"chenly_163 <xxxxxx@163.com>"  "chenly <xxxxxx@qq.com>"这种格式的，不然会被邮件组识别为非法邮件

# 现只支持单对单发送
def sendmail(mail_to,mail_host,mail_host_port,mail_user,mail_pass,subject,mailmsg):

  encoding="utf-8"
  msg=MIMEText(mailmsg,'html','utf-8')
  #若需要发送附件，必须采用MIMEMultipart()
  # msgRoot里的信息仅用于显示在文本中，如显示发送给谁，实际发送人是sendmail决定的
  # 通过@拆分邮箱名，把邮箱前缀用来作为邮箱昵称
  mail_user_name=mail_user.split('@')[0]
  mail_to_name=mail_to.split('@')[0]
  msgRoot = MIMEMultipart()
  msgRoot['Subject']=Header(subject,encoding)
  msgRoot['From'] = "%s <%s>" % (mail_user_name,mail_user)
  msgRoot['To'] = "%s <%s>" % (mail_to_name,mail_to)
  # msgRoot['Cc'] = mail_user 抄送用
  #添加邮件正文
  msgRoot.attach(msg)
  try:
    smtpObj = smtplib.SMTP()
    if mail_host_port == "":
      smtpObj.connect(mail_host)
      print ("connect success")
      if mail_user != "" and mail_pass != "":
        smtpObj.login(mail_user,mail_pass)
        print ("login success")
    else:
      smtpObj.connect(mail_host,int(mail_host_port))
      print ("connect success")
      if mail_user != "" and mail_pass != "":
        smtpObj.login(mail_user,mail_pass)
        print ("login success")
    smtpObj.sendmail(mail_user,mail_to, msgRoot.as_string())
    smtpObj.close()
    print ("mail send success")
  except smtplib.SMTPException as e:
    print (e)
    print ("Error: can't send mail")


__EMAIL_TEMPLATE = u'\
<html>  \
<head>  \
<meta charset="utf-8">\
<title>邮件html模板</title>\
</head>\
<body>\
    <h1>邮件标题1</h1>\
    <p>邮件段落1</p>\
    <p>自定义参数 %s</p>\
</body>\
</html>'

mailtext=__EMAIL_TEMPLATE % 'hello 2020'

sendmail(mail_to,mail_host,mail_host_port,mail_user,mail_pass,'htmlmail',mailtext)

