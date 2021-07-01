#-*-coding:utf-8 -*-
#@Time :2021/1/29 17:43
#@Author :daiqiuqin
#@File  :EvnData.py
class EnvData:
    pass


def clear_EnvData_attrs():
    values = dict(EnvData.__dict__.items())
    for key,value in values.items():
        if key.startswith("__"):
            pass
        elif key.find("gl_") != -1:
            pass
        else:
            delattr(EnvData,key)
