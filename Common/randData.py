#-*-coding:utf-8 -*-
#@Time :2021/6/1 11:00
#@Author :daiqiuqin
#@File  :randData.py

import random
import unittest

# CJK统一表意文字（4E00-9FFF）：常用汉字
# CJK统一表意文字扩展A（3400-4DBF）：罕用汉字
# CJK统一表意文字扩展B（20000-2A6DF）：罕用汉字
# CJK统一表意文字扩展C（2A700-2B73F）：罕用汉字
# CJK兼容表意文字（F900-FAFF）：重复字符，可统一的异形字
# CJK兼容表意文字补充（2F800-2FA1F）：可统一的异形字

class randChinese():
    def __init__(self,num):
        self.num=num

    def Unicode(self):
        rand_Chinese = ""
        c=self.num
        while c>=0:
            val = random.randint(0x4e00,0x9fff)
            rand_Chinese=rand_Chinese+chr(val)
            c = c - 1
        return rand_Chinese

    def GBK2312(self):
        rand_Chinese=""
        c = self.num
        while c>=0:
            head = random.randint(0xb0,0xf7)
            body = random.randint(0xa1,0xfe)
            val = f'{head:x} {body:x}'
            str = bytes.fromhex(val).decode('gb2312')
            rand_Chinese = rand_Chinese + str
            c = c - 1
        return rand_Chinese


def randword(num):
    word="¥$€￡₣¥₩:,.。，……-！（）()""“”+-*、\|?<>《》‘；;/@#%&~"
    aaa="0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def randchinese(num,encode="Unicode"):
    rc = randChinese(num)
    if encode=="GBK2312":
        rand_Chinese = rc.Unicode()
    if encode=="Unicode":
        rand_Chinese = rc.GBK2312()
    return rand_Chinese

hanzi=randchinese(30)
print(hanzi)



