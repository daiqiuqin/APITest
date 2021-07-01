#-*-coding:utf-8 -*-
#@Time :2021/1/29 14:45
#@Author :daiqiuqin
#@File  :requestLib.py
import requests
import json
from requests_toolbelt import MultipartEncoder
# 保留下面两个导入，上传附件需要
import os
from Common.handle_path import datas_dir,reports_dir,case_dir

def res(method,url,request_data=None,headers=None,files=None,type='json'):
    if method.upper()=='GET':
        response= requests.get(url=url, params=request_data,headers=headers, verify=False)

    if method.upper()=='POST' and type=='json':
        if files is None:
            # 用eval去除引号
            # new_data = eval(request_data)
            # 也可以转换成json格式
            # 当request_data不为空时，转换成json格式
            if isinstance(request_data,str):
                new_data = json.loads(request_data)
            else:
                new_data=request_data
            response = requests.post(url=url, json=new_data, headers=headers, verify=False)
        elif files is not None:
            files=eval(files)
            data = MultipartEncoder(fields=files,boundary="---uANPHGlpCQbTQxD4M-P3mn7ND85s4c0jHQIxhvo--")
            headers["content-type"]=data.content_type
            response = requests.post(url=url, data=data, headers=headers, verify=False)
            print(response.encoding)

    if method.upper()=='PUT' and type=='json':
        # 用eval去除引号
        # new_data = eval(request_data)
        # 也可以转换成json格式
        if request_data:
            new_data = json.loads(request_data)
        else:
            new_data = request_data
        response = requests.put(url=url, json=new_data, headers=headers, verify=False)

    return response

