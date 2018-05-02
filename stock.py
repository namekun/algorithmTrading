#-*- coding: utf-8 -*-


def cal_upper(price):
    increment = price * 0.3
    upper_price = price + increment
    return upper_price

def cal_lower(price):
    decrement = price * 0.3
    lower_price = price - decrement
    return lower_price

def cal_upper_lower(price):
    offset = price * 0.3
    upper = price + offset
    lower = price - offset
    return (upper, lower)


def cal_macd(item):
    pass


def run():
    print(cal_upper(100000))
    print(cal_lower(100000))
    print(__name__)

# Module이 제대로 동작하는지 확인하기 위해서 testcode를 실행시킨다.
# python stock을 통해서 실행시키면 안뜬다. stock.run()을 해줘야 함.

if __name__ == '__main__':
    run()

mylist = ['samsung', 'sk']

author = 'pystock'

