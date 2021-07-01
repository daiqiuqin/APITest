#-*-coding:utf-8 -*-
#@Time :2021/3/31 10:47
#@Author :daiqiuqin
#@File  :test_MedicalRecord_refuse.py


import jsonpath
import unittest
from Common.myddt import ddt,data
from Common.RWexcel  import ReadExcel,Wexcel
from Common.requestLib import res
from Common.handle_data import pre_data,replace_mark_with_data
from Common.EvnData import EnvData,clear_EnvData_attrs
from Common.logger import log
import os
from Common.handle_path import datas_dir,reports_dir,case_dir
from openpyxl.workbook import Workbook
from Common.conf import conf
from Common.CheckPoint import CheckPoint

# 读取测试用例
readExcelName=conf.getOption("excel","readExcelName")
readExcel = os.path.join(datas_dir,readExcelName)
readSheet = '病历复印-不同状态订单审核拒绝'
excel = ReadExcel(readExcel, readSheet)
titles = excel.read_titles()
alldatas = excel.read_all_datas()
maxRow = excel.get_max_row() - 1

@ddt
class test_MedicalRecord_refuse(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.Cookie='sessionPocket=session-34-oyiqKw9PAQqllUAqJhJ-D_G_Dejc'
        cls.row=1
        #执行testCase前先清除环境变量
        clear_EnvData_attrs()
        log.info("test_MedicalRecord_refuse测试套件开始执行,共有{}条用例".format(maxRow))

    @classmethod
    def tearDownClass(cls) -> None:
        log.info("test_MedicalRecord_refuse测试套件执行完毕")

    def setUp(self) -> None:
        log.info("用例开始执行".format(id))

    def tearDown(self) -> None:
        log.info("用例结束执行")

    @data(*alldatas)
    def test_MedicalRecord_refuse(self,data):
        # 判断是否跳过用例
        isexcute = pre_data(data['isexcute'])
        if isexcute=="n":
            self.skipTest("跳过这个用例")

        # 读取cookie
        Cookie = self.Cookie

        #替换参数
        data = replace_mark_with_data(data)
        # 读取数据
        id = pre_data(data['id'])
        title =pre_data (data['title'])
        protocal = pre_data(data['protocal'])
        method = pre_data(data['method'])
        host = pre_data(data['host'])
        path = pre_data(data['path'])
        request_data = pre_data(data['request_data'])
        expected =pre_data (data['expected'])
        extract_data= pre_data(data['extract_data'])


        # 接口请求
        headers = {
            "Connection": "keep - alive",
            "accept": "application/json,text/plain,*/*",
            "accept-encoding": "gzip,deflate",
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36 QBCore/4.0.1316.400 QQBrowser/9.0.2524.400 Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2875.116 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat",
            "content-type": "application/json;charset=UTF-8",
            "Referer":"https://test-pockethospital.rubikstack.com/shulan/index.html?utp=1614131099076&sessionKey=session-34-oyiqKw9PAQqllUAqJhJ-D_G_Dejc&state=34",
            "Accept-Language":"zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.5;q=0.4",
            "cookie":Cookie
            }

        url=protocal+"://"+host+path
        response=res(method,url,request_data,headers)
        response_text = response.text
        response_json = response.json()
        print(response_text)

        # 打印日志
        request_url=response.request.url
        request_headers=response.headers
        request_cookies=response.cookies
        request_body = response.request.body

        #####后置处理#####
        if extract_data:
            # 提取json返回数据存入全局变量
            medicalId=jsonpath.jsonpath(response_json,extract_data)[0]
            setattr(EnvData, "medicalId",medicalId)

        # 断言
        try:
            myassert=CheckPoint()
            myassert.checkAssertIn(expected,response_text,msg=id+"响应结果与预期不符合")
            myassert.checkTestResult()
            testResult = 'Pass'
            log.info('===={}断言成功===='.format(id))
        except Exception as msg:
            testResult = 'Fail'
            log.info('====错误信息：%s===='%msg)
            setattr(EnvData, "gl_IsFailFlag", 1)
            raise
        finally:
            # 打印日志
            log.info("====用例id:{}=====".format(id))
            log.info("====用例标题:{}=====".format(title))
            log.info("====请求url:{}=====".format(request_url))
            log.info("====请求headers:{}=====".format(request_headers))
            log.info("====请求body:{}=====".format(request_body))
            log.info("====预期结果:{}=====".format(expected))
            log.info("====返回结果:{}=====".format(response_text))
            log.info("====测试结果:{}=====".format(testResult))

            # 测试结果存入excel
            try:
                # 用于测试套件执行时的命名，根据配置文件设置+时间戳命名
                gl_excelname = getattr(EnvData, "gl_excelname")
                writeExcelName = gl_excelname
            except:
                # 用于单个用例执行时的命名，根据配置文件设置命名
                writeExcelName = conf.getOption("excel", "writeExcelName", "str")

            output_file = os.path.join(reports_dir, writeExcelName)

            print(writeExcelName)
            try:
                Wexcel(output_file, readSheet, self.row, id, title, method, request_url, request_body, expected,
                       response_text,
                       testResult)
                # 写入的行数加1
                test_MedicalRecord_refuse.row += 1
            except IOError as e:
                print(e)


if __name__=='__main__':
    unittest.main()
