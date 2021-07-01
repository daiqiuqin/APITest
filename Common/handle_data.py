#-*-coding:utf-8 -*-
#@Time :2021/1/29 14:48
#@Author :daiqiuqin
#@File  :handle_data.py

import re
from Common.EvnData import EnvData
def pre_data(data=None):
    if data:
        if data.find("\n") != -1:
            data = data.replace("\n", "")
        return data

def replace_mark_with_data(data):
    '''数据替换，替换的值需要为str类型
    :param data: 需要替换的数据
    :return:替换后的数据
    '''
    pattern = re.compile(r'#(.*?)#')
    print(data)
    ndata = data
    for key,value in data.items():
        if isinstance(value,str):
            res = pattern.findall(value)
            oldvalue=value
            if res:
                for item in res:
                    newdata = getattr(EnvData, item)
                    if newdata is not None and isinstance(newdata, str):
                        ndata[key] = oldvalue.replace('#{}#'.format(item), newdata)
                        oldvalue=ndata[key]
                    elif newdata is not None and not isinstance(newdata, str):
                        newdata=str(newdata)
                        ndata[key] = oldvalue.replace('#{}#'.format(item), newdata)
                        oldvalue = ndata[key]
    return ndata
