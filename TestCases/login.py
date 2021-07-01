#-*-coding:utf-8 -*-
#@Time :2021/1/12 14:01
#@Author :daiqiuqin
#@File  :login.py


import requests
import json
import jsonpath
from Common.conf import conf

def hospital_shulan_login():
    url="https://test-cloud-hospital.shulan.com/ms-doctor/v1/users/check/login"
    username=conf.getOption("shulan-doctor","doctorUser","str")
    password=conf.getOption("shulan-doctor","doctorPwd","str")
    data={
        "username":username,
        "password":password
    }
    response=json.loads(requests.get(url=url,params=data).text)
    hospital_shulan_access_token=jsonpath.jsonpath(response,'$..results.access_token')[0]
    return hospital_shulan_access_token

def hospital_tr_login():
    url="https://test-cloud-hospital-tr.rubikstack.com/ms-doctor/v1/users/check/login"
    username=conf.getOption("tr-doctor","doctorUser","str")
    password=conf.getOption("tr-doctor","doctorPwd","str")
    data={
        "username":username,
        "password":password
    }
    response=json.loads(requests.get(url=url,params=data).text)
    hospital_shulan_access_token=jsonpath.jsonpath(response,'$..results.access_token')[0]
    return hospital_shulan_access_token


def userApp_tr_login():
    url="https://test-cloud-hospital-tr.rubikstack.com/ms-pocket-hospital/v1/common/back/token"
    phone=conf.getOption("tr-patient","patientPhone","str")
    data={
        "phone":phone
    }
    response=json.loads(requests.get(url=url,params=data).text)
    userApp_tr_access_token=jsonpath.jsonpath(response,'$..results.access_token')[0]
    return userApp_tr_access_token

access_token=userApp_tr_login()
print(access_token)
