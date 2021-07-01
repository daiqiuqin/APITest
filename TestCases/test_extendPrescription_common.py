#-*-coding:utf-8 -*-
#@Time :2021/6/1 17:10
#@Author :daiqiuqin
#@File  :test_extendPrescription_common.py

import jsonpath
import unittest
from Common.myddt import ddt,data
from Common.RWexcel  import ReadExcel,Wexcel
from TestCases.login import userApp_tr_login
from Common.requestLib import res
from Common.handle_data import pre_data,replace_mark_with_data
from Common.EvnData import EnvData,clear_EnvData_attrs
from Common.logger import log
import os
from Common.handle_path import datas_dir,reports_dir
from Common.conf import conf
from Common.CheckPoint import CheckPoint
from random import randint
import json

# 读取测试用例
readExcel = os.path.join(datas_dir,'智慧服务接口测试.xlsx')
print(readExcel)
readSheet = '在线续方流程（接受）'
excel = ReadExcel(readExcel, readSheet)
titles = excel.read_titles()
alldatas = excel.read_all_datas()
maxRow = excel.get_max_row() - 1

@ddt
class test_extendPrescription_common(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.token=userApp_tr_login()
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
    def test_extendPrescription_common(self,data):
        # 判断是否跳过用例
        isexcute = pre_data(data['isexcute'])
        if isexcute=="n":
            self.skipTest("跳过这个用例")

        #####前置处理#####
        # 读取token
        token = self.token

        #数据准备
        hospitalId=conf.getOption("tr-hospital", "hospitalId", "str")
        hospitalName = conf.getOption("tr-hospital", "hospitalName", "str")
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
        setattr(EnvData, "hospitalName", hospitalName)
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

        # 接口请求
        headers = {
            "content-type": "application/json;charset=UTF-8",
            "Authorization":"Bearer "+token
            }

        if not files:
            files=None

        url=protocal+"://"+host+path
        print("======request_data=={}====".format(request_data))
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
                try:
                    if title == "搜索诊断-随机取诊断":
                        preliminaryDiagnosis=[]
                        ex = jsonpath.jsonpath(response_json, extract_formula)[0]
                        if isinstance(ex, list):
                            # 随机取的诊断个数，最多三个诊断，最少一个诊断
                            num = randint(1, 3)
                            print(num)
                            # 随机提取一个号源及其它后置数据
                            while num>0:
                                max = len(ex)- 1
                                r = randint(0, max)
                                resp = ex[r]
                                preliminaryDiagnosis.append(resp)
                                num=num-1
                        extract_name="preliminaryDiagnosis"
                        extract_value=preliminaryDiagnosis
                        # 将jsonpath提取出的单引号转换成双引号
                        jbdmid=json.dumps(jsonpath.jsonpath(preliminaryDiagnosis,"$[*].jbdmid"))
                        print("提取{}：{}".format("jbdmid", jbdmid))
                        setattr(EnvData, "jbdmid", jbdmid)


                    elif title=="查询医院下已启用药房-随机取一个药房":
                        resp1 = jsonpath.jsonpath(response_json, extract_formula)
                        if isinstance(resp1, list):
                            max = len(resp1) - 1
                            r = randint(0, max)
                            extract_value = resp1[r]
                            pharmacyId = jsonpath.jsonpath(extract_value, "$.pharmacyId")[0]
                            pharmacyName = jsonpath.jsonpath(extract_value, "$.pharmacyName")[0]
                            setattr(EnvData, "pharmacyId", pharmacyId)
                            print("提取{}：{}".format("pharmacyId", pharmacyId))
                            setattr(EnvData, "pharmacyName", pharmacyName)
                            print("提取{}：{}".format("pharmacyName", pharmacyName))

                    elif title=="查询字典-取随机值":
                        resp1 = jsonpath.jsonpath(response_json, extract_formula)
                        if isinstance(resp1, list):
                            max = len(resp1) - 1
                            r = randint(0, max)
                            extract_value = resp1[r]
                            frequency = jsonpath.jsonpath(extract_value, "$.value")[0]
                            frequencyCode = jsonpath.jsonpath(extract_value, "$.code")[0]
                            setattr(EnvData, "frequency", frequency)
                            print("提取{}：{}".format("frequency", frequency))
                            setattr(EnvData, "frequencyCode", frequencyCode)
                            print("提取{}：{}".format("frequencyCode", frequencyCode))

                    elif title=="查询his给药频率-取随机值":
                        resp1 = jsonpath.jsonpath(response_json, extract_formula)
                        if isinstance(resp1, list):
                            max = len(resp1) - 1
                            r = randint(0, max)
                            extract_value = resp1[r]

                    elif title=="查询his给药方式-取随机值":
                        resp1 = jsonpath.jsonpath(response_json, extract_formula)
                        if isinstance(resp1, list):
                            max = len(resp1) - 1
                            r = randint(0, max)
                            extract_value = resp1[r]

                    else:
                        extract_value = jsonpath.jsonpath(response_json, extract_formula)[0]

                    print("提取{}：{}".format(extract_name, extract_value))
                    setattr(EnvData, extract_name, extract_value)
                except TypeError as e:
                    print("{}未提取到数据，错误原因:{}".format(extract_name,e))

            if title == "患者端-获取就诊人信息成功并提取数据":
                try:
                    resSex = getattr(EnvData, "resSex")
                    if resSex == "男":
                        sexCode = "1"
                    elif resSex == "女":
                        sexCode = "2"
                    else:
                        sexCode = "3"
                    setattr(EnvData, "sexCode", sexCode)
                except:
                    print("性别未提取到数据")

        # 断言
        try:
            if title=="患者端-检查申请中续方单的数量增加1":
                total = getattr(EnvData, "extendPrescriptionCount1")
                extendPrescriptionCount2=getattr(EnvData, "extendPrescriptionCount2")
                total_AfterAdd=total+1
                myassert = CheckPoint()
                myassert.checkAssertIn(expected, response_text, msg=id + "响应结果与预期不符合")
                myassert.checkAssertIn(extendPrescriptionCount2,total_AfterAdd, msg=id + "响应结果与预期不符合")

            if title=="患者端-查询申请中续方列表，有新增续方单且数据正确":
                extendPrescriptionId=getattr(EnvData,"extendPrescriptionId")
                resultList=getattr(EnvData,"resultList")
                resSex=getattr(EnvData,"resSex")
                sexCode = getattr(EnvData, "sexCode")
                resContactId = getattr(EnvData, "resContactId")
                resContactName = getattr(EnvData, "resContactName")
                resBirthday = getattr(EnvData, "resBirthday")
                resIdCard = getattr(EnvData, "resIdCard")
                resPhone = getattr(EnvData, "resPhone")

                for item in resultList:
                    if item["extendPrescriptionId"]==extendPrescriptionId:
                        print("======extendPrescriptionId========{}".format(extendPrescriptionId))
                        myassert = CheckPoint()
                        myassert.checkAssertIn(expected, response_text, msg=id + "响应结果与预期不符合")
                        myassert.checkAssertIn(item["remake"], "续方备注，吧啦吧啦", msg=id + "响应结果与预期不符合")
                        myassert.checkAssertIn(item["sex"],resSex, msg=id + "响应结果与预期不符合")
                        myassert.checkAssertIn(str(item["sexCode"]),sexCode, msg=id + "响应结果与预期不符合")
                        myassert.checkAssertIn(item["contactId"], resContactId, msg=id + "响应结果与预期不符合")
                        myassert.checkAssertIn(item["contactName"], resContactName, msg=id + "响应结果与预期不符合")
                        myassert.checkAssertIn(item["birthday"],resBirthday, msg=id + "响应结果与预期不符合")
                        myassert.checkAssertIn(item["idCard"],resIdCard, msg=id + "响应结果与预期不符合")
                        myassert.checkAssertIn(item["phone"],resPhone, msg=id + "响应结果与预期不符合")

                myassert.checkTestResult()
                testResult = 'Pass'
                log.info('===={}断言成功===='.format(id))

            if title=="患者端-检查续方详情数据与新增一致":
                resSex=getattr(EnvData, "resSex")
                sexCode=getattr(EnvData, "sexCode")
                resContactName=getattr(EnvData, "resContactName")
                resContactId=getattr(EnvData, "resContactId")
                resBirthday=getattr(EnvData, "resBirthday")
                resIdCard=getattr(EnvData, "resIdCard")
                resPhone=getattr(EnvData, "resPhone")

                resRemake2=getattr(EnvData,"resRemake2")
                resSex2=getattr(EnvData, "resSex2")
                resSexCode2=getattr(EnvData, "resSexCode2")
                resContactName2=getattr(EnvData, "resContactName2")
                resContactId2=getattr(EnvData, "resContactId2")
                resBirthday2=getattr(EnvData, "resBirthday2")
                resIdCard2=getattr(EnvData, "resIdCard2")
                resPhone2=getattr(EnvData, "resPhone2")

                myassert = CheckPoint()
                myassert.checkAssertIn(expected, response_text, msg=id + "响应结果与预期不符合")
                myassert.checkAssertIn(resRemake2, "续方备注,吧啦吧啦", msg=id + "响应结果与预期不符合")
                myassert.checkAssertIn(resSex2,resSex, msg=id + "响应结果与预期不符合")
                myassert.checkAssertIn(str(resSexCode2), sexCode, msg=id + "响应结果与预期不符合")
                myassert.checkAssertIn(resContactName2,resContactName, msg=id + "响应结果与预期不符合")
                myassert.checkAssertIn(resContactId2,resContactId, msg=id + "响应结果与预期不符合")
                myassert.checkAssertIn(resBirthday2,resBirthday, msg=id + "响应结果与预期不符合")
                myassert.checkAssertIn(resIdCard2,resIdCard, msg=id + "响应结果与预期不符合")
                myassert.checkAssertIn(resPhone2,resPhone, msg=id + "响应结果与预期不符合")

                myassert.checkTestResult()
                testResult = 'Pass'
                log.info('===={}断言成功===='.format(id))

            if title == "医生端-检查续方详情数据与新增一致":
                resSex = getattr(EnvData, "resSex")
                sexCode = getattr(EnvData, "sexCode")
                resContactName = getattr(EnvData, "resContactName")
                resContactId = getattr(EnvData, "resContactId")
                resBirthday = getattr(EnvData, "resBirthday")
                resIdCard = getattr(EnvData, "resIdCard")
                resPhone = getattr(EnvData, "resPhone")

                resRemake2 = getattr(EnvData, "resRemake2")
                resSex2 = getattr(EnvData, "resSex2")
                resSexCode2 = getattr(EnvData, "resSexCode2")
                resContactName2 = getattr(EnvData, "resContactName2")
                resContactId2 = getattr(EnvData, "resContactId2")
                resBirthday2 = getattr(EnvData, "resBirthday2")
                resIdCard2 = getattr(EnvData, "resIdCard2")
                resPhone2 = getattr(EnvData, "resPhone2")

                myassert = CheckPoint()
                myassert.checkAssertIn(expected, response_text, msg=id + "响应结果与预期不符合")
                myassert.checkAssertIn(resRemake2, "续方备注，吧啦吧啦", msg=id + "响应结果与预期不符合")
                myassert.checkAssertIn(resSex2, resSex, msg=id + "响应结果与预期不符合")
                myassert.checkAssertIn(str(resSexCode2), sexCode, msg=id + "响应结果与预期不符合")
                myassert.checkAssertIn(resContactName2, resContactName, msg=id + "响应结果与预期不符合")
                myassert.checkAssertIn(resContactId2, resContactId, msg=id + "响应结果与预期不符合")
                myassert.checkAssertIn(resBirthday2, resBirthday, msg=id + "响应结果与预期不符合")
                myassert.checkAssertIn(resIdCard2, resIdCard, msg=id + "响应结果与预期不符合")
                myassert.checkAssertIn(resPhone2, resPhone, msg=id + "响应结果与预期不符合")

                myassert.checkTestResult()
                testResult = 'Pass'
                log.info('===={}断言成功===='.format(id))

            if title=="医生工作站-检查处方详情数据正确":
                resname = getattr(EnvData, "resname")
                ressex = getattr(EnvData, "ressex")
                resage = getattr(EnvData, "resage")
                residCard = getattr(EnvData, "residCard")
                resphone = getattr(EnvData, "resphone")
                resprescriptionId = getattr(EnvData, "resprescriptionId")
                resdoctorName = getattr(EnvData, "resdoctorName")
                resdepartmentName = getattr(EnvData, "resdepartmentName")
                resdiagnosisList = getattr(EnvData, "resdiagnosisList")
                resmedicinalName = getattr(EnvData, "resmedicinalName")
                resmedicineSpecific = getattr(EnvData, "resmedicineSpecific")
                ressingleDose = getattr(EnvData, "ressingleDose")
                ressingleUnit = getattr(EnvData, "ressingleUnit")
                resfrequency = getattr(EnvData, "resfrequency")
                resusageName = getattr(EnvData, "resusageName")
                resdays = getattr(EnvData, "resdays")
                resquantity = getattr(EnvData, "resquantity")
                resunitPrice = getattr(EnvData, "resunitPrice")
                resremark = getattr(EnvData, "resremark")

                resContactName3 = getattr(EnvData, "resContactName3")
                resSex3 = getattr(EnvData, "resSex3")
                resAge3 = getattr(EnvData, "resAge3")
                resIdCard3 = getattr(EnvData, "resIdCard3")
                resPhone3 = getattr(EnvData, "resPhone3")
                prescriptionId = getattr(EnvData, "prescriptionId")
                doctorName = getattr(EnvData, "doctorName")
                preliminaryDiagnosis = getattr(EnvData, "preliminaryDiagnosis")
                medicineName = getattr(EnvData, "medicineName")
                medicineSpecific = getattr(EnvData, "medicineSpecific")
                frequency = getattr(EnvData, "frequency")
                gyzwmc = getattr(EnvData, "gyzwmc")
                unitPrice = getattr(EnvData, "unitPrice")

                myassert = CheckPoint()
                # 校验处方信息:患者姓名、性别、年龄、证件号、电话、处方编号、开方时间、开单医生、开单科室、诊断
                # 校验处方详情：药品名称、规格、单次剂量、单位、用药频次、用法、天数、数量、单价、备注
                myassert.checkAssertIn(expected, response_text, msg=id + "响应结果与预期不符合")
                myassert.checkAssertIn(resname, resContactName3, msg=id + "患者姓名与预期不符合")
                myassert.checkAssertIn(ressex, resSex3, msg=id + "患者性别与预期不符合")
                myassert.checkAssertIn(str(resage), str(resAge3), msg=id + "患者年龄与预期不符合")
                myassert.checkAssertIn(residCard, resIdCard3, msg=id + "患者证件号与预期不符合")
                myassert.checkAssertIn(resphone, resPhone3, msg=id + "患者电话与预期不符合")
                myassert.checkAssertIn(resprescriptionId, prescriptionId, msg=id + "处方编号与预期不符合")
                myassert.checkAssertIn(resdoctorName, doctorName, msg=id + "开单医生与预期不符合")
                myassert.checkAssertIn(resdepartmentName, "胃肠外科门诊", msg=id + "开单科室与预期不符合")
                myassert.checkAssertIn(str(resdiagnosisList), str(preliminaryDiagnosis), msg=id + "诊断与预期不符合")
                myassert.checkAssertIn(resmedicinalName, medicineName, msg=id + "药品名称与预期不符合")
                myassert.checkAssertIn(resmedicineSpecific, medicineSpecific, msg=id + "规格与预期不符合")
                myassert.checkAssertIn(str(ressingleDose), "1.0", msg=id + "单次剂量与预期不符合")
                myassert.checkAssertIn(ressingleUnit, "SLICE", msg=id + "单位与预期不符合")
                myassert.checkAssertIn(resfrequency, frequency, msg=id + "用药频次与预期不符合")
                myassert.checkAssertIn(resusageName, gyzwmc, msg=id + "用法与预期不符合")
                myassert.checkAssertIn(str(resdays), "1", msg=id + "天数与预期不符合")
                myassert.checkAssertIn(str(resquantity), "1", msg=id + "数量与预期不符合")
                myassert.checkAssertIn(str(resunitPrice), str(unitPrice), msg=id + "单价与预期不符合")
                myassert.checkAssertIn(resremark, "儿童减半", msg=id + "备注与预期不符合")

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
                test_extendPrescription_common.row += 1
            except IOError as e:
                print(e)

if __name__=='__main__':
    unittest.main()