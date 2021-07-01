# #-*-coding:utf-8 -*-
# #@Time :2021/1/14 17:15
# #@Author :daiqiuqin
# #@File  :msg.py

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time
from Common.conf import Conf
from Common.logger import log
import os
from  Common.handle_path  import reports_dir,logs_dir

class Mail():
    """发送邮件模块类.
     :param testResult:测试结果
     """
    def sendMail(self,reportname,logname,excelname,testResult):
        '''用于发送邮件
        reportname：邮件中附加的报告的名称
        logname：邮件中附加的日志的名称
        excelname:邮件中附加的excel文件名称
        '''
        # 创建Conf类实例
        conf = Conf()
        # 发送邮箱服务器
        smtp_server = conf.getOption('mail', 'smtp_server')
        # 发送邮箱用户名
        smpt_user = conf.getOption('mail', 'smpt_user')
        # 发送邮箱密码
        smpt_password = conf.getOption('mail', 'smpt_password')
        # 发送邮箱
        sender = conf.getOption('mail', 'sender')
        # 接收邮箱
        receiver = conf.getOption('mail', 'receiver')
        # 邮件主题
        subject = conf.getOption('mail', 'subject')
        # 抄送地址
        copyer = conf.getOption('mail', 'copyer')
        # 报告地址
        reportDir =os.path.join(reports_dir,reportname)
        # 日志地址
        logDir =os.path.join(logs_dir,logname)
        # excel文件地址
        excelDir = os.path.join(reports_dir, excelname)

        # 设置文本形式邮件正文
        mail_body='''
        <html>
        <p><font size="4" face="arial" color="Black ">大家好：</p>
        <p><font size="4" face="arial" color="Black ">     本次接口自动化测试已运行完毕，测试结果为：
        <font size="5" face="arial" color="red">'''+testResult+'''
        <p>
        <p><font size="4" face="arial" color="Black ">     附件为详细测试数据，包括测试报告、测试日志、测试用例及结果，请查收。<p>
        <p><font size="4" face="arial" color="Black ">     有任何疑问可以联系测试部：戴秋琴<p>
        </html>
        '''

        body = MIMEText(mail_body, _subtype='html', _charset='utf-8')

        # 设置邮件的文本附件1
        sendfile = open(reportDir, 'rb').read()
        att1 = MIMEText(sendfile, "text/html", 'utf-8')
        att1['Content-Type'] = 'application/octet-stream'
        att1['Content-Disposition'] = 'attachment;filename='+reportname

        # 设置邮件的文本附件2
        sendfile = open(logDir, 'rb').read()
        att2 = MIMEText(sendfile, "text/plain", 'utf-8')
        att2['Content-Type'] = 'application/octet-stream'
        att2['Content-Disposition'] = 'attachment;filename='+logname

        # 设置邮件的excel附件3
        sendfile = open(excelDir, 'rb').read()
        # 将xlsx文件作为内容发送到对方的邮箱读取excel，rb形式读取，对于MIMEText()来说默认的编码形式是base64 对于二进制文件来说没有设置base64，会出现乱码
        att3 = MIMEText(sendfile, 'base64', 'utf-8')
        # 不能用注释中的这种方式添加附件，不然会添加失败
        # att3['Content-Type'] = 'application/octet-stream'
        # att3['Content-Disposition'] = 'attachment;filename='+excelname
        att3.add_header('Content-Disposition', 'attachment', filename=excelname)

        msg = MIMEMultipart('related')
        # 邮件标题
        msg['Subject'] =subject
        # 发件人
        msg['From'] =sender
        # 收件人
        msg['To'] =receiver
        # 抄送地址
        msg['Cc'] =copyer
        msg['date']=time.strftime('%a, %d %b %Y %H:%M:%S %z')

        msg.attach(att1)
        msg.attach(att2)
        msg.attach(att3)
        msg.attach(body)

        smtp = smtplib.SMTP()
        try:
            smtp.connect(smtp_server)
            # smt = smtplib.SMTP_SSL('smtp.exmail.qq.com', '465')
            smtp.login(smpt_user,smpt_password)
            smtp.sendmail(msg['From'], msg['To'].split(';'), msg.as_string())
            log.info("%s：邮件发送成功,查收%s的邮箱" % (smpt_user,receiver))
        except Exception as e:
            print(e)
            log.info("Error 邮件发送失败")
        finally:
            smtp.quit()

def sendReport(reportname,logname,excelname,testResult):
    """封装发送邮件方法,无须创建实例.
     :param testResult:测试结果
     """
    mail=Mail()
    mail.sendMail(reportname,logname,excelname,testResult)

if __name__=="__main__":
    reportname='report_20210226172926.html'
    logname='ApiTest_20210226172924.log'
    excelname='电子发票接口测试结果.xlsx'
    sendReport(reportname,logname,excelname,'不通过')