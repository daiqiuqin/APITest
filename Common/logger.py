#-*-coding:utf-8 -*-
#@Time :2021/1/12 18:01
#@Author :daiqiuqin
#@File  :logger.py

import logging
from Common.conf import Conf
import time
from Common.handle_path import logs_dir
import os
from Common.EvnData import EnvData

def log():
    """日志处理模块.
     :param : 无
     :return: 日志器对象
     """
    conf = Conf()
    level = conf.getOption('log', 'level').upper()
    # 日志器-处理器-格式器
    # 创建日志对象
    Logger = logging.getLogger('dqq_apiLog')
    # 设置日志器级别
    Logger.setLevel(level)

    # 创建格式器
    fmt = logging.Formatter("%(asctime)s %(name)s %(levelname)s %(filename)s-%(lineno)d line：%(message)s")

    # 创建屏幕处理器
    sh = logging.StreamHandler()
    sh.setLevel(level)
    # 给处理器设置格式器
    sh.setFormatter(fmt)
    # 将处理器加入日志器
    Logger.addHandler(sh)
    IsFile = conf.getOption('log', 'IsFile')

    if IsFile:
        # 创建文件处理器
        filename='ApiTest_'+time.strftime('%Y%m%d%H%M%S')+'.log'
        setattr(EnvData, 'gl_logname', filename)
        filepath=os.path.join(logs_dir,filename)
        fh = logging.FileHandler(filepath)
        fh.setLevel(level)
        # 给处理器设置格式器
        fh.setFormatter(fmt)
        # 将处理器加入日志器
        Logger.addHandler(fh)

    # 将处理器加入日志器
    Logger.addHandler(sh)
    return Logger

log=log()

if __name__=="__main__":
    log.info('测试一下能否进行日志记录')
