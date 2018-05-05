import pandas
print(pandas.Series)


from pandas import Series, DataFrame

kakao =Series([92600, 92400, 92100, 94300, 92300])

print(kakao)
print(kakao[0])
print(kakao[1])
print(kakao[2])
print(kakao[3])

kakao2 = Series([92600, 92400, 92100, 94300, 92300], index=['2016-02-19',
                                                            '2016-02-18',
                                                            '2016-02-17',
                                                            '2016-02-16',
                                                            '2016-02-15'])

print(kakao2)

for date in  kakao2.index:
    print(date)

for closing_price in kakao2.values: # kakao2.data도 가능.
    print(closing_price)

mine = Series([10, 20, 30], index=['naver', 'sk', 'kt'])
friend = Series([10, 20, 30], index=['kt', 'naver', 'sk'])

merge = mine + friend # Series는 인덱싱이 다른 경우에도 알아서 인덱싱이 같은 값끼리 덧셈 연산을 수행한다.
print(merge)

 
