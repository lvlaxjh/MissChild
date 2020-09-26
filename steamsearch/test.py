import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
import time
import urllib.request
import json
nowTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
my_sender = '2876363140@qq.com'    # 发件人邮箱账号
my_pass = 'jzalaltaeyuxdhcf'       #发件人邮箱密码(当时申请smtp给的口令)
allError = "###"
#网络连接测试---用来检测网站是否出现意外并停止运行
def webTest():
    url = "http://119.45.211.210/"
    try:
        status = urllib.request.urlopen(url).code
        print(status)
    except Exception as e:
        allError = allError + "###webTestError:" + e

#发送邮件---发用邮件提醒管理员运行状况
def mail():
    res = str(nowTime)+"---send ok"
    try:
        emailListFile = open("emailList.json", "r")
        adminMail = json.loads(emailListFile.read())
        my_userList = adminMail['adminMail']     # 收件人邮箱账号
        emailListFile.close()
        for i in my_userList:
            try:
                msg = MIMEText('填写邮件内容', 'plain', 'utf-8')
                msg['From'] = formataddr(["发件人昵称", my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
                # 括号里的对应收件人邮箱昵称、收件人邮箱账号
                msg['To'] = formataddr(["收件人昵称", i])
                msg['Subject'] = "邮件主题-测试"                # 邮件的主题，也可以说是标题

                server = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器，端口是465
                server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
                # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
                server.sendmail(my_sender, [i, ], msg.as_string())
                server.quit()  # 关闭连接
            except Exception as e:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
                allError = allError + "###sendmailError1(send):" + e
    except Exception as e:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
        allError = allError + "###sendmailError2(other):" + e
    return res


mailres = mail()
print(mailres)
print(allError)






