#-*-coding:utf-8 -*-
#@Time :2021/6/17 15:39
#@Author :daiqiuqin
#@File  :handel_time.py

import datetime
from chinese_calendar import is_workday, is_holiday,Holiday,is_in_lieu,get_holiday_detail
# 判断是不是节假日
april_last = datetime.date(2021,9,21)
www=datetime.datetime(2021,9,30,1,1,0)
print(www)
print(is_workday(april_last))
print(is_holiday(april_last))

# 或者在判断的同时，获取节日名
on_holiday, holiday_name =get_holiday_detail(april_last)
print(on_holiday)
print(Holiday.labour_day.value, holiday_name)

# 还能判断法定节假日是不是调休
print(is_in_lieu(april_last))