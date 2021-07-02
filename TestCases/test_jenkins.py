#-*-coding:utf-8 -*-
#@Time :2021/7/1 15:05
#@Author :daiqiuqin
#@File  :test_jenkins.py

import os
import unittest

from Common.EvnData import EnvData
from Common.RWexcel import Wexcel
from Common.conf import conf
from Common.handle_path import reports_dir
from Common.logger import log


class test_01(unittest.TestCase):
        @classmethod
        def setUp(self) -> None:
            log.info("开始执行")
        def tearDown(self) -> None:
            log.info("结束执行")
        def test_01(self):
            print("hhhhhhhh")
            setattr(EnvData, 'gl_IsFailFlag',"true")
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
                Wexcel(output_file, "readSheet", 1, "id", "title", "method", "request_url", "request_body", "expected",
                       "response_text",
                       "testResult")
            except IOError as e:
                print(e)

if __name__=="__main__":
    unittest.main()