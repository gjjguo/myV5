import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

class Email:
    def __init__(self, smtpserver=None, user=None, pwd=None):
        self.user = user
        self.pwd = pwd
        self.smtpserver = smtpserver

    def send_email(self, filepath=None, filename=None, sender=None, revicer=None, content=None, subject=None):
        # 如名字所示Multipart就是分多个部分
        msg = MIMEMultipart()
        msg["Subject"] = subject
        msg["From"] = sender
        msg["To"] = revicer

        # ---这是文字部分---
        part = MIMEText(content)
        msg.attach(part)

        # ---这是附件部分---
        # xlsx类型附件
        part = MIMEApplication(open(filepath, 'rb').read())
        part.add_header('Content-Disposition', 'attachment', filename=filename)
        msg.attach(part)

        s = smtplib.SMTP("smtp.exmail.qq.com", timeout=60)  # 连接smtp邮件服务器,端口默认是25
        s.login(self.user, self.pwd)  # 登陆服务器
        s.sendmail(sender, revicer, msg.as_string())  # 发送邮件
        s.close()


if __name__ == '__main__':
    smtpserver = "smtp.exmail.qq.com"
    user = "guojuanjuan@bjnja.com"
    pwd = "Gjj199312"
    e = Email(smtpserver=smtpserver, user=user, pwd=pwd)
    filepath = r"F:\自动化学习\前程贷接口自动化实战\前程贷项目接口自动化测试\2021-02-09.log"
    filename = '2021-02-09.log'
    sender = 'guojuanjuan@bjnja.com'
    revicer = 'guojuanjuan@bjnja.com'
    content = '测试邮件'
    subject = "测试报告"

    e.send_email(filepath=filepath,
                 filename=filename,
                 sender=sender,
                 revicer=revicer,
                 content=content,
                 subject=subject)
