from pandas import Series, DataFrame

daeshin = {'open': [11650, 11100, 11200, 11100, 11000],
           'high': [12100, 11800, 11200, 11100, 11150],
           'low': [11600, 11505, 10900, 10950, 10900],
           'close': [11900, 11600, 11000, 11100, 11050]}

dashin_day = DataFrame(daeshin)

print(dashin_day)

dashin_day2 = DataFrame(daeshin, columns=['open', 'high', 'low', 'close'])
# column도 지정해 줄 수 있다.

print(dashin_day2)


date = ['16,02,29', '16.02.26', '16.02.25', '16.02.24', '16.02.23']
dashin_day3 = DataFrame(daeshin, columns=['open', 'high', 'low', 'close'], index=date)
# index를 지정

print(dashin_day3)

# 데이터 프레임 칼럼, 로우 선택
close = dashin_day['close']
print(close)

# print(dashin_day3['16.02.24'])
# 에러 발생! pandas가 data frame 객체에 '16.02.04'라는 키값을 갖는 칼럼을 못찾기에!

day_data = dashin_day3.ix['16.02.24']
print(day_data)
print(type(day_data))
print(dashin_day3.columns)
print(dashin_day3.index) 
