#-*-coding:utf-8 -*-
#@Time :2021/4/7 15:23
#@Author :daiqiuqin
#@File  :test_doctorVisit_common.py

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


# 读取测试用例
readExcelName=conf.getOption("excel","readExcelName")
readExcel = os.path.join(datas_dir,readExcelName)
readSheet = '医护上门正常流程'
excel = ReadExcel(readExcel, readSheet)
titles = excel.read_titles()
alldatas = excel.read_all_datas()
maxRow = excel.get_max_row() - 1

@ddt
class test_doctorVisit_common(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.row=1
        #执行testCase前先清除环境变量
        clear_EnvData_attrs()
        log.info("doctorVisit_common测试套件开始执行,共有{}条用例".format(maxRow))

    @classmethod
    def tearDownClass(cls) -> None:
        log.info("doctorVisit_common测试套件执行完毕")

    def setUp(self) -> None:
        log.info("用例开始执行".format(id))

    def tearDown(self) -> None:
        log.info("用例结束执行")

    @data(*alldatas)
    def test_doctorVisit_common(self,data):
        # 判断是否跳过用例
        isexcute = pre_data(data['isexcute'])
        if isexcute=="n":
            self.skipTest("跳过这个用例")

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

        # 接口请求
        headers = {
            "accept": "application/json,text/plain,*/*",
            "accept-encoding": "gzip,deflate,br",
            # "authorization": token,
            "content-type": "application/json;charset=UTF-8"
        }

        if not files:
            files=None

        url=protocal+"://"+host+path
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
            for item in extract_data_list:
                extract_data_list = item.split("=")
                extract_name = extract_data_list[0]
                extract_formula = extract_data_list[1]
                extract_value = jsonpath.jsonpath(response_json, extract_formula)[0]
                print("提取{}：{}".format(extract_name, extract_value))
                setattr(EnvData, extract_name, extract_value)


        # 断言
        try:
            self.assertIn(expected, response_text, msg=id + "：断言结果与预期不符合")

            if data['title']=="项目详情-校验项目内容是否正确":
                serviceType=getattr(EnvData,"serviceType")
                projectName =getattr(EnvData, "projectName")
                projectDesc = getattr(EnvData, "projectDesc")
                serviceFee=getattr(EnvData,"serviceFee")
                serviceDesc =getattr(EnvData, "serviceDesc")
                image = getattr(EnvData, "image")
                staffId1=getattr(EnvData,"staffId1")
                # staffId2 =getattr(EnvData, "staffId2")
                myassert1 = CheckPoint()
                myassert1.checkAssertEqual(serviceType,"HealthPromotion", msg=id + ":校验值serviceType与预期不符合")
                myassert1.checkAssertEqual(projectName,"api-test服务项目-主流程", msg=id + ":校验值projectName与预期不符合")
                myassert1.checkAssertEqual(projectDesc,"根据患者的病情，对易发生压力性损伤的患者采取定时翻身、气垫减压等方法预防压力性损伤的发生。为患者及照顾者提供压力性损伤护理的健康指导。", msg=id + "校验值:projectDesc与预期不符合")
                myassert1.checkAssertEqual(serviceFee,10.0, msg=id + ":校验值serviceFee与预期不符合")
                myassert1.checkAssertEqual(serviceDesc,"<p>服务描述：为患者及照顾者提供压力性损伤护理的健康指导。</p>", msg=id + ":校验值serviceDesc与预期不符合")
                myassert1.checkAssertEqual(image,"df239afb134f4f2c8850a3415dcff616.jpg", msg=id + "：校验值:image与预期不符合")
                myassert1.checkAssertEqual(staffId1,"ef2588ccbfd44404a6bb39decc0a65f3", msg=id + ":校验值staffId1与预期不符合")
                # myassert1.checkAssertEqual(staffId2,"4556acbc7ed3408f901064947cd5d491", msg=id + ":校验值staffId2与预期不符合")
                myassert1.checkTestResult()

            if data['title']=="耗材详情-校验耗材内容是否正确":
                consumableName=getattr(EnvData,"consumableName")
                consumableFee = str(getattr(EnvData, "consumableFee"))
                unit = getattr(EnvData, "unit")
                myassert = CheckPoint()
                myassert.checkAssertEqual(unit,"个", msg=id + ":校验值unit与预期不符合")
                myassert.checkAssertEqual(consumableName,"apitest添加的服务耗材", msg=id + ":校验值consumableName与预期不符合")
                myassert.checkAssertEqual(consumableFee,"10000.0", msg=id + "校验值:consumableFee与预期不符合")
                myassert.checkTestResult()

            if data['title']=="耗材详情-校验耗材下线是否生效":
                onlineStatus=getattr(EnvData,"onlineStatus")
                myassert=CheckPoint()
                myassert.checkAssertEqual(onlineStatus,False,msg=id + ":校验值onlineStatus与预期不符合")
                myassert.checkTestResult()

            if data['title']=="耗材详情-校验耗材上线是否生效":
                onlineStatus=getattr(EnvData,"onlineStatus")
                myassert=CheckPoint()
                myassert.checkAssertEqual(onlineStatus,True,msg=id + ":校验值onlineStatus与预期不符合")
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

            try:
                Wexcel(output_file, readSheet, self.row, id, title, method, request_url, request_body, expected,
                       response_text,
                       testResult)
                # 写入的行数加1
                test_doctorVisit_common.row += 1
            except IOError as e:
                print(e)


if __name__ == '__main__':
    unittest.main()
