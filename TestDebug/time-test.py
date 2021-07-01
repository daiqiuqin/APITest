#-*-coding:utf-8 -*-
#@Time :2021/6/16 14:26
#@Author :daiqiuqin
#@File  :time-test.py

# import time
#
# import re
# # orderDatetime="2021-05-10 08:04:00"
# spell="10:16-10:20"
# pattern = re.compile(r'(.*?)-')
# res = pattern.findall(spell)
# print(res)
# yy=time.localtime().tm_year
# mm=time.localtime().tm_mon
# dd=time.localtime().tm_mday
# dd=dd+2
# c=str(yy)+"-"+str(mm)+"-"+str(dd)+" "+res[0]
# print(c)

# import datetime
# # 判断 2018年4月30号 是不是节假日
from chinese_calendar import is_workday, is_holiday
# april_last = datetime.date(2021, 6, 19)
# print(is_workday(april_last))
# print(is_holiday(april_last))

import datetime

# now_time=datetime.datetime.now()
#
# print((now_time+datetime.timedelta(days=+14)).strftime("%Y-%m-%d")) #获取后一天
#
# print ((now_time+datetime.timedelta(hours=-1)).strftime("%Y-%m-%d")) #获取前一小时

now_time = datetime.datetime.now()
date_time = now_time + datetime.timedelta(days=+2)
while is_holiday(date_time):
    date_time = date_time + datetime.timedelta(days=+1)
orderDatetime = date_time.strftime("%Y-%m-%d") + " " + "08:00" + ":00"
print(type(orderDatetime))
# df['is_holiday'] = df['统计日期'].apply(lambda x:is_workday(x))

# # 或者在判断的同时，获取节日名
# import chinese_calendar as calendar  # 也可以这样 import
# on_holiday, holiday_name = calendar.get_holiday_detail(april_last)
# self.assertTrue(on_holiday)
# self.assertEqual(calendar.Holiday.labour_day.value, holiday_name)
#
# # 还能判断法定节假日是不是调休
# import chinese_calendar
# self.assertFalse(chinese_calendar.is_in_lieu(datetime.date(2006, 1, 1)))
# self.assertTrue(chinese_calendar.is_in_lieu(datetime.date(2006, 1, 2)))