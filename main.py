#-*-coding:utf-8 -*-
#@Time :2021/1/26 11:39
#@Author :daiqiuqin
#@File  :main.py.py
import logging
import unittest
from Common.handle_path import case_dir,reports_dir
from BeautifulReport import BeautifulReport
from Common.msg import sendReport
import time
from Common.EvnData import EnvData
from Common.logger import log
from Common.conf import conf

#获取当前时间戳
nt=time.strftime('%Y%m%d%H%M%S')
# 获取配置文件中的写入表格名称
writeExcelName=conf.getOption("excel","writeExcelName","str")
writeExcelName=writeExcelName.split(".")[0]+"_"+nt+"."+writeExcelName.split(".")[1]
# 执行测试套件前，先进行测试结论的初始化
setattr(EnvData, "gl_IsFailFlag",0)
# 执行测试套件前，先进行写入表格名称的初始化
setattr(EnvData, "gl_excelname",writeExcelName)


# 基于路径，将测试用例组合成套件,默认pattern='test*.py'
suite = unittest.defaultTestLoader.discover(start_dir=case_dir,pattern='test_jenkins.py')
suite = unittest.TestLoader.discover(case_dir)
runner=BeautifulReport(suite)

# 输出的测试报告名称及路径
reportname='report_'+nt+'.html'
runner.report(description="接口测试报告" ,filename=reportname,report_dir=reports_dir)


log.info("测试结束，开始发送测试报告邮件")
IsFailFlag = getattr(EnvData, 'gl_IsFailFlag')
if IsFailFlag:
    LastTestResult = "不通过"
else:
    LastTestResult = "通过"

logname=getattr(EnvData,'gl_logname')

excelName=getattr(EnvData,'gl_excelname')

sendReport(reportname, logname,excelName, LastTestResult)



