#-*-coding:utf-8 -*-
#@Time :2021/7/1 15:05
#@Author :daiqiuqin
#@File  :test_jenkins.py

import unittest
from Common.logger import log
class test_01(unittest.TestCase):
        @classmethod
        def setUp(self) -> None:
            log.info("开始执行")
        def tearDown(self) -> None:
            log.info("结束执行")
        def test_01(self):
            print("hhhhhhhh")

if __name__=="__main__":
    unittest.main()