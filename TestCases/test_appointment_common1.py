#-*-coding:utf-8 -*-
#@Time :2021/4/25 16:30
#@Author :daiqiuqin
#@File  :test_appointment_common.py

import jsonpath
import unittest
from Common.myddt import ddt,data
from Common.RWexcel  import ReadExcel,Wexcel
from Common.requestLib import res
from Common.handle_data import pre_data,replace_mark_with_data
from Common.EvnData import EnvData,clear_EnvData_attrs
from Common.logger import log
import os
from Common.handle_path import datas_dir,reports_dir
from Common.conf import conf
from Common.CheckPoint import CheckPoint
import random
import time
import re
import datetime
from chinese_calendar import is_holiday

# 读取测试用例
readExcelName=conf.getOption("excel","readExcelName")
readExcel = os.path.join(datas_dir,readExcelName)
readSheet = '预约挂号流程（固定取值）'
excel = ReadExcel(readExcel, readSheet)
titles = excel.read_titles()
alldatas = excel.read_all_datas()
maxRow = excel.get_max_row() - 1

@ddt
class test_appointment_common(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.Cookie='sessionPocket=session-34-oyiqKw9PAQqllUAqJhJ-D_G_Dejc'
        cls.row=1

        #执行testCase前先清除环境变量
        clear_EnvData_attrs()
        log.info("测试套件开始执行,共有{}条用例".format(maxRow))

    @classmethod
    def tearDownClass(cls) -> None:
        log.info("测试套件执行完毕")

    def setUp(self) -> None:
        log.info("用例开始执行")

    def tearDown(self) -> None:
        log.info("用例结束执行")

    @data(*alldatas)
    def test_appointment_common(self,data):
        # 判断是否跳过用例
        isexcute = pre_data(data['isexcute'])
        if isexcute=="n":
            self.skipTest("跳过这个用例")

        # 读取cookie
        Cookie = self.Cookie

        #替换参数
        if data['title'] == "预提交成功":
            spell=getattr(EnvData,"spell")
            pattern = re.compile(r'(.*?)-')
            res_spell = pattern.findall(str(spell))
            now_time = datetime.datetime.now()
            date_time = now_time + datetime.timedelta(days=+7)
            while is_holiday(date_time):
                date_time = date_time + datetime.timedelta(days=+1)
            orderDatetime =date_time.strftime("%Y-%m-%d")+" "+res_spell[0]+":00"
            setattr(EnvData,"orderDatetime",orderDatetime)

        if data['title'] == "排班信息,随机提取一个排班信息及后置数据":
            now_time = datetime.datetime.now()
            date_time = now_time + datetime.timedelta(days=+7)
            while is_holiday(date_time):
                date_time = date_time + datetime.timedelta(days=+1)
            scheduleDate = date_time.strftime("%Y-%m-%d")
            print(scheduleDate)
            setattr(EnvData,"scheduleDate",scheduleDate)

        data = replace_mark_with_data(data)

        # 读取数据
        id = pre_data(data['id'])
        title =pre_data (data['title'])
        protocal = pre_data(data['protocal'])
        method = pre_data(data['method'])
        host = pre_data(data['host'])
        path = pre_data(data['path'])
        request_data = pre_data(data['request_data'])
        files = pre_data(data['files'])
        extract_data = pre_data(data['extract_data'])
        expected =pre_data (data['expected'])

        if title == "预提交成功":
            totalFee = getattr(EnvData, "totalFee")
            sourceNo = getattr(EnvData, "sourceNo")
            print("====totalFee:{}=====".format(type(totalFee)))
            print("====sourceNo:{}=====".format(type(sourceNo)))

        headers = {
            "accept": "application/json,text/plain,*/*",
            "accept-encoding": "gzip,deflate,br",
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36 QBCore/4.0.1316.400 QQBrowser/9.0.2524.400 Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2875.116 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat",
            "Cookie":Cookie,
            "content-type": "application/json;charset=UTF-8"
            }

        if not files:
            files=None

        url=protocal+"://"+host+path
        print(request_data)
        response=res(method,url,request_data,headers,files)
        response_text = response.text
        response_json = response.json()
        request_url=response.request.url
        request_headers=response.headers
        request_body = response.request.body
        if not isinstance(request_body,bytes) and request_body!=None:
            request_body = "requestbody非bytes格式,不记录"

        #####后置处理#####
        if extract_data:
            extract_data_list = extract_data.split(",")
            count = 0
            for item in extract_data_list:
                extract_data_list = item.split("=")
                extract_name = extract_data_list[0]
                extract_formula = extract_data_list[1]
                try:
                    if data["title"] == "科室查询,随机提取一个科室":
                        extract_value = "0"
                        while extract_value == "0":
                            # 随机提取一个科室id
                            c = len(jsonpath.jsonpath(response_json, extract_formula))
                            r = random.randint(0, c)
                            extract_value = jsonpath.jsonpath(response_json, extract_formula)[r]

                    elif data["title"] == "排班概述,随机提取一个排班及其它后置数据":
                        # 随机提取一个排班及其它后置数据
                        if count == 0:
                            ex = jsonpath.jsonpath(response_json, extract_formula)
                            resp3 = ex
                            if isinstance(ex, list):
                                c = len(ex)
                                max = c - 1
                                r = random.randint(0, max)
                                resp3 = jsonpath.jsonpath(response_json, extract_formula)[r]
                                count += 1
                        extract_value = jsonpath.jsonpath(resp3, extract_formula)
                        if isinstance(extract_value, list):
                            extract_value = jsonpath.jsonpath(resp3, extract_formula)[0]
                            if type(extract_value) != "str":
                                extract_value = str(extract_value)
                    elif data["title"] == "排班信息,随机提取一个排班信息及后置数据":
                        # 随机提取一个排班信息及后置数据
                        if count == 0:
                            ex = jsonpath.jsonpath(response_json, extract_formula)
                            resp3 = ex
                            if isinstance(ex, list):
                                c = len(ex)
                                max = c - 1
                                r = random.randint(0, max)
                                resp3 = jsonpath.jsonpath(response_json, extract_formula)[r]
                                count += 1
                        extract_value = jsonpath.jsonpath(resp3, extract_formula)
                        if isinstance(extract_value, list):
                            extract_value = jsonpath.jsonpath(resp3, extract_formula)[0]
                            if type(extract_value) != "str":
                                extract_value = str(extract_value)

                    elif data["title"] == "根据排班信息,获取号源详情":
                        # 随机提取一个号源及其它后置数据
                        if count == 0:
                            ex = jsonpath.jsonpath(response_json, extract_formula)
                            resp3 = ex
                            if isinstance(ex, list):
                                c = len(ex)
                                max = c - 1
                                r = random.randint(0, max)
                                resp3 = jsonpath.jsonpath(response_json, extract_formula)[r]
                                count += 1
                        extract_value = jsonpath.jsonpath(resp3, extract_formula)
                        if isinstance(extract_value, list):
                            extract_value = jsonpath.jsonpath(resp3, extract_formula)[0]
                            if type(extract_value) != "str":
                                extract_value = str(extract_value)
                    else:
                        extract_value = jsonpath.jsonpath(response_json, extract_formula)[0]
                    print("提取{}：{}".format(extract_name, extract_value))
                    setattr(EnvData, extract_name, extract_value)
                except TypeError as e:
                    print("未提取到数据，错误原因:{}".format(e))

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
                test_appointment_common.row += 1
            except IOError as e:
                print(e)

if __name__=='__main__':
    unittest.main()