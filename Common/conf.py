#-*-coding:utf-8 -*-
#@Time :2021/1/20 15:40
#@Author :daiqiuqin
#@File  :conf.py
import os
import configparser
from Common.handle_path import conf_dir
class Conf:
    def getOption(self,section, option,type='str'):
        """读取配置文件的value值.
         :param section:要读取的section
         :param option:要读取的option
         :return: 无
         :rtype: String
         """
        config = configparser.ConfigParser()
        filePath=os.path.join(conf_dir,'config.ini')
        config.read(filePath, encoding='utf-8')
        if not config.has_option(section, option):
            print('Error:section[' + section + ']不存在option:' + option)
        if config.has_option(section, option):
            if type=='str':
                getData = config.get(section, option)
            elif type=='bool':
                getData = config.getboolean(section, option)
            elif type=='float':
                getData = config.getfloat(section, option)
            elif type=='int':
                getData = config.getint(section, option)
            return getData

    def setOption(self,section, option, value):
        """给option进行赋值.
        :param section:要操作的section
        :param option:要操作的option
        :param value:要设置的value
        """
        config = configparser.ConfigParser()
        filePath = os.path.join(conf_dir, 'config.ini')
        config.read(filePath, encoding='utf-8')
        config.set(section, option, value=value)
        config.write(open(filePath, 'w', encoding='utf-8'))

    def removeOption(self,section, option):
        """删除option.
        :param section:要操作的section
        :param option:要删除的option
        """
        config = configparser.ConfigParser()
        filePath = os.path.join(conf_dir, 'config.ini')
        config.read(filePath, encoding='utf-8')
        config.remove_option(section, option)
        config.write(open(filePath, 'w', encoding='utf-8'))

conf=Conf()

if __name__ == '__main__':
    smtp_server=conf.getOption('excel','writeExcelName','str')
    print(smtp_server)