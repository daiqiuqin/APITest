#-*-coding:utf-8 -*-
#@Time :2021/5/20 13:14
#@Author :daiqiuqin
#@File  :test_telext_common.py

import requests
import jsonpath
import unittest
from Common.myddt import ddt,data
from Common.RWexcel  import ReadExcel,Wexcel
from TestCases.login import hospital_tr_login
from Common.requestLib import res
from Common.handle_data import pre_data,replace_mark_with_data
from Common.EvnData import EnvData,clear_EnvData_attrs
from Common.logger import log
import os
from Common.handle_path import datas_dir,reports_dir
from Common.conf import conf
from Common.CheckPoint import CheckPoint
import random


# 读取测试用例
readExcel = os.path.join(datas_dir,'智慧服务接口测试.xlsx')
print(readExcel)
readSheet = '在线问诊流程（免费）'
excel = ReadExcel(readExcel, readSheet)
titles = excel.read_titles()
alldatas = excel.read_all_datas()
maxRow = excel.get_max_row() - 1

@ddt
class test_telext_common(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.token=hospital_tr_login()
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
    def test_telext_common(self,data):
        # 判断是否跳过用例
        isexcute = pre_data(data['isexcute'])
        if isexcute=="n":
            self.skipTest("跳过这个用例")

        #####前置处理#####
        # 读取token
        token = self.token

        #数据准备
        hospitalId=conf.getOption("tr-hospital", "hospitalId", "str")
        groupHospitalName = conf.getOption("tr-hospital", "groupHospitalName", "str")
        groupHospitalId = conf.getOption("tr-hospital", "groupHospitalId", "str")
        doctorName=conf.getOption("tr-doctor", "doctorName", "str")
        doctorId=conf.getOption("tr-doctor","doctorId","str")
        doctorJgId=conf.getOption("tr-doctor","doctorJgId","str")
        doctoriuid=conf.getOption("tr-doctor","doctoriuid","str")
        contactId=conf.getOption("tr-patient","contactId","str")
        contactJgId=conf.getOption("tr-patient","contactJgId","str")
        patientiuid=conf.getOption("tr-patient","patientiuid","str")
        patientPhone=conf.getOption("tr-patient","patientPhone","str")
        patientName = conf.getOption("tr-patient", "patientName", "str")

        setattr(EnvData, "hospitalId", hospitalId)
        setattr(EnvData, "groupHospitalName", groupHospitalName)
        setattr(EnvData, "groupHospitalId", groupHospitalId)
        setattr(EnvData, "doctorName", doctorName)
        setattr(EnvData, "doctorId", doctorId)
        setattr(EnvData, "doctorJgId", doctorJgId)
        setattr(EnvData, "doctoriuid", doctoriuid)
        setattr(EnvData, "contactId", contactId)
        setattr(EnvData, "contactJgId", contactJgId)
        setattr(EnvData, "patientiuid", patientiuid)
        setattr(EnvData, "patientPhone", patientPhone)
        setattr(EnvData, "patientName", patientName)

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
        files = pre_data(data['files'])
        extract_data = pre_data(data['extract_data'])
        expected =pre_data (data['expected'])

        if not files:
            files=None

        # 接口请求
        url=protocal+"://"+host+path
        if  "/ms-doctor/" in path:
            headers={
                "content-type": "application/json;charset=UTF-8",
                "Authorization":token
            }
            response = res(method, url, request_data, headers, files)

        elif title == "患者成功取消订单":
            headers = {
                "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8"
            }
            response = requests.put(url=url, params=request_data, headers=headers, verify=False)

        else:
            headers = {
                "content-type": "application/json;charset=UTF-8"
            }
            response = res(method, url, request_data, headers, files)

        response_text = response.text
        print(response_text)
        response_json = response.json()
        request_url=response.request.url
        request_headers=response.headers
        request_body = response.request.body
        if not isinstance(request_body,bytes) and request_body!=None:
            request_body = "requestbody非bytes格式,不记录"

        #####后置处理#####
        if extract_data:
            extract_data_list = extract_data.split(",")
            for item in extract_data_list:
                extract_data_list = item.split("=")
                extract_name = extract_data_list[0]
                extract_formula = extract_data_list[1]
                try:
                    if title == "获取评论标签并取随机值":
                        extract_value = "0"
                        while extract_value == "0":
                            # 随机提取一个科室id
                            c = len(jsonpath.jsonpath(response_json, extract_formula))
                            r = random.randint(0, c)
                            extract_value = jsonpath.jsonpath(response_json, extract_formula)[r]
                    else:
                        extract_value = jsonpath.jsonpath(response_json, extract_formula)[0]

                    print("提取{}：{}".format(extract_name, extract_value))
                    setattr(EnvData, extract_name, extract_value)

                except TypeError as e:
                    print("未提取到数据，错误原因:{}".format(e))

        # 断言
        try:
            if title == "【前置条件】服务设置：获取医生基础信息详情，验证在线问诊开启成功":
                teletextFee1 = getattr(EnvData, "teletextFee1")
                myassert = CheckPoint()
                myassert.checkAssertIn(expected, response_text, msg=id + "响应结果与预期不符合")
                myassert.checkAssertEqual(teletextFee1, "0.00", msg=id + "响应结果与预期不符合")
                myassert.checkTestResult()
                testResult = 'Pass'
                log.info('===={}断言成功===='.format(id))

            if title == "患者端-我的问诊，能查询到问诊单且数据正确-未就医,未确诊":
                helpTip1 = getattr(EnvData, "helpTip1")
                helpContent1 = getattr(EnvData, "helpContent1")
                isAlreadyComeToHospital1 = getattr(EnvData, "isAlreadyComeToHospital1")
                isDiseaseDiagnosed1 = getattr(EnvData, "isDiseaseDiagnosed1")

                myassert = CheckPoint()
                myassert.checkAssertIn(expected, response_text, msg=id + "响应结果与预期不符合")
                myassert.checkAssertEqual(helpTip1, "病情咨询,挂号咨询,检查报告解读",
                                          msg=id + "响应结果与预期不符合")
                myassert.checkAssertEqual(helpContent1,
                                          "病情描述,自动化测试专用数据。病情描述,自动化测试专用数据。从3月12日开始，出现有打喷嚏鼻塞的情况，朋友说这是属于流感的症状，头痛发烧。123456ABVDE，腹泻难受。",
                                          msg=id + "响应结果与预期不符合")
                myassert.checkAssertEqual(isAlreadyComeToHospital1, False, msg=id + "响应结果与预期不符合")
                myassert.checkAssertEqual(isDiseaseDiagnosed1, False, msg=id + "响应结果与预期不符合")
                myassert.checkTestResult()
                testResult = 'Pass'
                log.info('===={}断言成功===='.format(id))

            if title == "医生端-我的问诊-进行中，能查询到问诊单且数据正确-未就医,未确诊":
                helpTip2 = getattr(EnvData, "helpTip2")
                helpContent2 = getattr(EnvData, "helpContent2")
                isAlreadyComeToHospital2 = getattr(EnvData, "isAlreadyComeToHospital1")
                isDiseaseDiagnosed2 = getattr(EnvData, "isDiseaseDiagnosed1")
                myassert = CheckPoint()
                myassert.checkAssertIn(expected, response_text, msg=id + "响应结果与预期不符合")
                myassert.checkAssertEqual(helpTip2, "病情咨询,挂号咨询,检查报告解读",
                                          msg=id + "响应结果与预期不符合")
                myassert.checkAssertEqual(helpContent2,
                                          "病情描述,自动化测试专用数据。病情描述,自动化测试专用数据。从3月12日开始，出现有打喷嚏鼻塞的情况，朋友说这是属于流感的症状，头痛发烧。123456ABVDE，腹泻难受。",
                                          msg=id + "响应结果与预期不符合")
                myassert.checkAssertEqual(isAlreadyComeToHospital2, False, msg=id + "响应结果与预期不符合")
                myassert.checkAssertEqual(isDiseaseDiagnosed2, False, msg=id + "响应结果与预期不符合")
                myassert.checkTestResult()
                testResult = 'Pass'
                log.info('===={}断言成功===='.format(id))

            if title == "提交订单后，订单详情查询问诊订单状态和数据正确":
                orderStatus = getattr(EnvData, "orderStatus1")
                payStatus= getattr(EnvData, "payStatus1")
                myassert = CheckPoint()
                myassert.checkAssertIn(expected, response_text, msg=id + "响应结果与预期不符合")
                myassert.checkAssertEqual(orderStatus, "WAITING_FOR_ADMISSION", msg=id + "响应结果与预期不符合")
                myassert.checkAssertEqual(payStatus, "SUCCESS", msg=id + "响应结果与预期不符合")
                myassert.checkTestResult()
                testResult = 'Pass'
                log.info('===={}断言成功===='.format(id))

            if title == "接诊后，订单详情查询问诊订单状态和数据正确":
                orderStatus = getattr(EnvData, "orderStatus2")
                payStatus= getattr(EnvData, "payStatus2")
                myassert = CheckPoint()
                myassert.checkAssertIn(expected, response_text, msg=id + "响应结果与预期不符合")
                myassert.checkAssertEqual(orderStatus, "RECEPTION", msg=id + "响应结果与预期不符合")
                myassert.checkAssertEqual(payStatus, "SUCCESS", msg=id + "响应结果与预期不符合")
                myassert.checkTestResult()
                testResult = 'Pass'
                log.info('===={}断言成功===='.format(id))

            if title == "填写咨询建议后，订单详情查询问诊订单状态和数据正确":
                orderStatus = getattr(EnvData, "orderStatus3")
                payStatus= getattr(EnvData, "payStatus3")
                myassert = CheckPoint()
                myassert.checkAssertIn(expected, response_text, msg=id + "响应结果与预期不符合")
                myassert.checkAssertEqual(orderStatus, "RECEPTION", msg=id + "响应结果与预期不符合")
                myassert.checkAssertEqual(payStatus, "SUCCESS", msg=id + "响应结果与预期不符合")
                myassert.checkTestResult()
                testResult = 'Pass'
                log.info('===={}断言成功===='.format(id))

            if title == "结束后，订单详情查询问诊订单状态和数据正确":
                orderStatus = getattr(EnvData, "orderStatus4")
                payStatus= getattr(EnvData, "payStatus4")
                myassert = CheckPoint()
                myassert.checkAssertIn(expected, response_text, msg=id + "响应结果与预期不符合")
                myassert.checkAssertEqual(orderStatus, "FINISH", msg=id + "响应结果与预期不符合")
                myassert.checkAssertEqual(payStatus, "SUCCESS", msg=id + "响应结果与预期不符合")
                myassert.checkTestResult()
                testResult = 'Pass'
                log.info('===={}断言成功===='.format(id))

            if title == "患者评价后，订单详情查询问诊订单状态和数据正确":
                orderStatus = getattr(EnvData, "orderStatus5")
                payStatus= getattr(EnvData, "payStatus5")
                myassert = CheckPoint()
                myassert.checkAssertIn(expected, response_text, msg=id + "响应结果与预期不符合")
                myassert.checkAssertEqual(orderStatus, "ALREADY_COMMENTS", msg=id + "响应结果与预期不符合")
                myassert.checkAssertEqual(payStatus, "SUCCESS", msg=id + "响应结果与预期不符合")
                myassert.checkTestResult()
                testResult = 'Pass'
                log.info('===={}断言成功===='.format(id))

            else:
                myassert = CheckPoint()
                myassert.checkAssertIn(expected, response_text, msg=id + "响应结果与预期不符合")
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
                test_telext_common.row += 1
            except IOError as e:
                print(e)



if __name__=='__main__':
    unittest.main()