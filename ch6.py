#-*- coding: utf-8 -*-


'''
def print_business_card(name, email, addr):
    print('----------------------')
    print('Name : %s' % name)
    print('E-mail : %s' % email)
    print('Address : %s' % addr)
    print('----------------------')


name = ['namekun', 'DusanBaek']
email = ['namkun@dfdf.com', 'dusan.back@naver,com']
addr = ['Incheon', 'Seoul']

print_business_card(name[0], email[0], addr[0])

print_business_card(name[1], email[1], addr[1])
'''

# 명함 클래스 정의
'''
class BusinessCard:
    pass

card1 = BusinessCard()

print(type(BusinessCard))

print(card1)
'''

# 명함 클래스에 메소드 추가
# 함수는 인자 맨 처음에 무조건 self를 줘야함. 객체 자체가 메소드의 첫번째 인자로 넘어오기에.
# python은 약타입 언어이기에, 변수를 선언하면서 동시에 실행한다.
# self.name 만 딸랑 써줄 수 없기에, self.name = name 이런 식으로 초기화를 해줘야한다.
# 반대로 강타입의 언어는?  int x; x = 10; 이런식으로만 해주면 됨.

'''
class BusinessCard():

    def set_info(self, name, email, addr):
        self.name = name # name을 사용하기전에 초기화 시켜주는 것.
        self.email = email
        self.addr = addr

    def print_business_card(self): # self는 class안에 함수를 쓸때 필요
        print('----------------------')
        print('Name : %s' % self.name)
        print('E-mail : %s' % self.email)
        print('Address : %s' % self.addr)
        print('----------------------')


member1 = BusinessCard()

print(member1)
print(member1.__init__())
print(member1.set_info('namkun', 'namkun@dfdf.com', 'Incheon'))

# 실행될 때, 데이터 타입이 만들어진다. 즉, 내부 변수가 선언되게 됨
print(member1.__dict__) # member1의 공간에 info 를 set 해주었기에 결과가 저렇게 보이는 것.
print(member1.email)

member2 = BusinessCard()
member2.set_info('sarang lee', 'saranglee@naver.com', 'Kyunggi')
print(member2.__dict__)

member1.print_business_card() # member1이 print_business_card의 self로 들어간다!
member2.print_business_card()

member1.set_info('iceGirl', 'namkun@dfdf.com', 'Incheon')
print(member1.name)
'''


# class 생성자 __init__

class BusinessCard():

    def __init__(self, name, email, addr):  # __init__
        self.name = name  # name을 사용하기전에 초기화 시켜주는 것.
        self.email = email
        self.addr = addr

    def print_business_card(self):  # self는 class안에 함수를 쓸때 필요
        print('----------------------')
        print('Name : %s' % self.name)
        print('E-mail : %s' % self.email)
        print('Address : %s' % self.addr)
        print('----------------------')


# member1 = BusinessCard() # 에러 나는 이유는 인자(argument)를 주지 않았기에

member1 = BusinessCard('namkun', 'hallo@dfdf.com', 'GaemaKowon')

member1.print_business_card()


# self 이해하기! (p.135)

class foo:
    def func1():
        print("Function1")

    def func2(self):
        print("Function2")


# f = foo()

# f.func1() -- self가 없으니까 안됩니다. argument를 아예 할당받지 못하니까.
# f.func2()


class foo:

    def func1():  # 호출시 className.func1()
        print()
        print("Function1")
        print()

    def func2(self):  # 호출시 , 1) Instance.func2() 2) className.func2(Instance)
        print()
        print(id(self))
        print("Function2")
        print()


f = foo()
f2 = foo()

f.func2()
foo.func1()  # static function의 느낌. 인스턴스를 만들지 않고 바로 호출할 수 있는 함수로 쓸 수 있다.

foo.func2(f)
foo.func2(f2)


# 04 class NameSpace

class stock:
    market = "kospi"  # market앞에 self. 이 없음에 유의/ class 에서 self 없이 변수를 만들면 이 변수는 class 변수가 된다.
    # 이 인스턴스의 공통 변수가 된다는 의미.


# 클래스 네임 스페이스

print(stock.__dict__)
print(stock.market)  # JAVA의 static 변수 같은 느낌

s1 = stock()
s2 = stock()

print(id(s1))
print(id(s2))  # s1 != s2 이기에 별도의 stock 객체

print(dir())

# 인스턴스의 네임 스페이스

print(s1.__dict__)
print(s2.__dict__)

print(s1.market)  # 이때 market은 class의 네임스페이스

# s1 인스턴스에 market 인스턴스 변수를 추가

s1.market = "kosdaq"  # python은 동적으로 얼마든지 변수를 할당해 줄 수 있다.

print(s1.__dict__)
print(s1.market)

print(s2.market)


# print(s2.volume)  # stock에 없으니 안나옴


# 05 클래스 변수와 인스턴스 변수

class Account:
    num_accounts = 0

    def __init__(self, name):
        self.name = name
        Account.num_accounts += 1

    def __del__(self):  # 소멸자
        Account.num_accounts -= 1


kim = Account("kim")
lee = Account("lee")

print(kim.name)
print(lee.name)

print(kim.num_accounts)
print(lee.num_accounts)

Account.num_accounts


# 06 클래스 상속

class Animal:

    def __init__(self, name):
        self.name = name

    def eat(self, food):
        print(str(self.name) + "(이)가 " + str(food) + "을(를) 먹는다.")


dog = Animal("개")

dog.eat("개밥")


class Dog(Animal):

    #    def __init__(self):
    #        super.__init__("개")

    def bark(self):
        print("왈왈")


dog2 = Dog("개")
dog2.eat("생선")
dog2.bark()


# 연습문제 6-1, 6-2

class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def setx(self, x):
        self.x = x

    def sety(self, y):
        self.y = y

    def get(self):
        return self.x, self.y

    def move(self, dx, dy):
        self.x = self.x + dx
        self.y = self.y + dy


p1 = Point(3, 5)
(x, y) = p1.get()
print(x, y)

p1.setx(x + 2)
p1.sety(y - 2)
(x, y) = p1.get()
print(x, y)

p1.move(-1, 1)
print(p1.get())
