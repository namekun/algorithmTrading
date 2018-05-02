#-*- coding: utf-8 -*-


import stock
import sys

print(sys.path)
# 이 결과의 ''는 파이참이 시작되는 현재 디렉토리를 이야기 한다.

print(stock.cal_upper(1000000))

print(stock.author)

print(stock.__name__) # name은 module의 이름을 말한다.

stock.run()

import os

print(os.getcwd())

print(os.listdir())

print(os.listdir('D://anaconda'))