#-*-coding:utf-8 -*-
#@Time :2021/2/3 10:14
#@Author :daiqiuqin
#@File  :handle_path.py

import os

# 获取当前文件的上两级目录的绝对路径
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

#拼接测试用例路径
case_dir = os.path.join(base_dir,"TestCases")

#拼接测试数据的路径
datas_dir = os.path.join(base_dir,"TestDatas")

#拼接报告输出的路径
reports_dir = os.path.join(base_dir,r"Outputs\reports")

#拼接日志输出路径
logs_dir = os.path.join(base_dir,r"Outputs\logs")

#拼接配置文件的路径
conf_dir = os.path.join(base_dir,"Conf")

if __name__ == "__main__":
    print(base_dir)
    print(case_dir)
    print(datas_dir)
    print(reports_dir)
    print(logs_dir)
    print(conf_dir)
