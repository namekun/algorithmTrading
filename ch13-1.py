from pandas import Series, DataFrame

# dictionary 를 이용한 DataFrame 객체 생성
raw_Data = {'col0': [1, 2, 3, 4],
            'col1': [10, 20, 30, 40],
            'col2': [100, 200, 300, 400]}

data = DataFrame(raw_Data)
print(data)

print(data['col0'])
print(data['col1'])
print(data['col2']) 
