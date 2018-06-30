#====================== Basic =================================
'''
变量名大小写敏感，不可以数字或下划线开头。
常用三种数据类型：
1.	Logical: True, False
	逻辑运算：&, |, not	
2.	Numeric
	//取整，%取余
3.	Character
'''

a = 2.1
b = 3.2
print(a + b) #5.30000000..1
print((a + b) == 5.3)  #False\
print(type(a)) #class float

from decimal import Decimal
a = Decimal('2.1')
b = Decimal('3.2')
print(a + b)
print((a + b) == Decimal('5.3'))
print(type(a)) #class decimal.Decimal
print('=====================================')


#===================== String 编码 =============================
'''
Unicode常用的是用两个字节表示一个字符（如果要用到非常偏僻的字符，就需要4个字节）.
ASCII编码和Unicode编码的区别：ASCII编码是1个字节，而Unicode编码通常是2个字节。
字母A用ASCII编码是十进制的65，二进制的01000001；
字符0用ASCII编码是十进制的48，二进制的00110000；

汉字'中'已经超出了ASCII编码的范围，用Unicode编码是十进制的20013，二进制的01001110 00101101。
如果把ASCII编码的A用Unicode编码，只需要在前面补0就可以，因此，A的Unicode编码是00000000 01000001。

新的问题又出现了：如果统一成Unicode编码，乱码问题从此消失了。但是，如果文本基本上全部是英文的话，用Unicode编码比ASCII编码需要多一倍的存储空间，在存储和传输上就十分不划算。

所以，本着节约的精神，又出现了把Unicode编码转化为'可变长编码'的UTF-8编码。UTF-8编码把一个Unicode字符根据不同的数字大小编码成1-6个字节，常用的英文字母被编码成1个字节，汉字通常是3个字节，只有很生僻的字符才会被编码成4-6个字节。如果你要传输的文本包含大量英文字符，用UTF-8编码就能节省空间：

字符	ASCII		Unicode					UTF-8
A	01000001	00000000 01000001		01000001
中	x			01001110 00101101		11100100 10111000 10101101
可以发现，UTF-8编码有一个额外的好处，就是ASCII编码实际上可以被看成是UTF-8编码的一部分，所以，只支持ASCII编码的历史遗留软件可以在UTF-8编码下继续工作。

Python2字符串设计上的一些缺陷：
使用ASCII码作为默认编码方式，对中文处理很不友好。
字符串分为unicode和str两种类型。

Python2提供了ord()和chr()，unichr()函数，可以把字母和对应的数字相互转换。
chr()函数用一个范围在range（256）内的（就是0～255）整数作参数，返回一个对应的字符。unichr()跟它一样，只不过返回的是Unicode字符。
ord()函数是chr()函数（对于8位的ASCII字符串）或unichr()函数（对于Unicode对象）的配对函数，它以一个字符（长度为1的字符串）作为参数，返回对应的ASCII数值，或者Unicode数值，如果所给的Unicode字符超出了你的Python定义范围，则会引发一个TypeError的异常。

Python2在后来添加了对Unicode的支持，以Unicode表示的字符串用u'...'表示
把u'xxx'转换为UTF-8编码的'xxx'用encode('utf-8')方法
反过来，把UTF-8编码表示的字符串'xxx'转换为Unicode字符串u'xxx'用decode('utf-8')

Python3两个问题都很好的解决了。
1.Python3系统默认编码设置为UTF-8。
2.文本字符和二进制数据区分得更清晰，分别用str和bytes表示。
文本字符全部用str类型表示，str能表示Unicode字符集中所有字符，而二进制字节数据用一种全新的数据类型，用bytes来表示。

Python3不再提供unichr()函数，而ord()函数的参数范围也得到扩展。

python字符串immutable。
'''

import sys
print(sys.getdefaultencoding())
print(type('a'))
print(type('中'))

print(ord('A'))
print(ord('中'))
print(chr(20011))

#String操作
a = 'python'
print(a + a)
print(a * 3)

#索引：
print(a[0], a[5]) #p n 
print(a[-1], a[-6]) #n p 
print(a[1:5]) #ytho
print(a[:])  #python 
print(a[3:]) #hon

#方法：
fileName = 'videos.txt'
print(fileName.startswith('v')) #True
print(fileName.endswith('.txt')) #True

url = 'http://m.org'
protocols = ('http', 'https')
print(url.startswith(protocols)) #must be a tuple of strings
print(url.find('.org')) #返回索引，没找到返回-1
print(url.replace('m', 'python'))

parts = ['apple', 'orange', 'banana']
print(','.join(parts)) #用,拼接
print('=====================================')


# ===================== Format =========================
'''
在Python中，采用的格式化方式和C语言是一致的，用%实现，举例如下：
%d	整数
%f	浮点数
%s	字符串
%x	十六进制整数
有些时候，字符串里面的%是一个普通字符怎么办？这个时候就需要转义，用%%来表示一个%：
'''
print('Hello, %s' % 'world')
print('Hi, %s, you have $%d.' % ('Michael', 1000000))
print('growth rate: %d%%' % 7)
print('=====================================')


#============================ Bytes ===============================   ？？？？？？？？
'''
Python3中，在字符引号前加'b'，明确表示这是一个bytes类型的对象，实际上它就是一组二进制字节序列组成的数据，bytes类型可以是ASCII范围内的字符和其它十六进制形式的字符数据，但不能用中文等非ASCII字符表示。

>>> c = b'a'
>>> c
b'a'
>>> type(c)
<class 'bytes'>

>>> d = b'\xe7\xa6\x85'
>>> d
b'\xe7\xa6\x85'
>>> type(d)
<class 'bytes'>
>>>

>>> e = b'禅'
  File "<stdin>", line 1
SyntaxError: bytes can only contain ASCII literal characters.
bytes 类型提供的操作和 str 一样，支持分片、索引、基本数值运算等操作。但是 str 与 bytes 类型的数据不能执行 + 操作，尽管在py2中是可行的。

>>> b"a"+b"c"
b'ac'
>>> b"a"*2
b'aa'
>>> b"abcdef\xd6"[1:]
b'bcdef\xd6'
>>> b"abcdef\xd6"[-1]
214

>>> b"a" + "b"
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: can't concat bytes to str
python2 与 python3 字节与字符的对应关系

python2	python3	表现	转换	作用
str	bytes	字节	encode	存储
unicode	str	字符	decode	显示
encode 与 decode
str 与 bytes 之间的转换可以用 encode 和从decode 方法。 py3-str

encode 负责字符到字节的编码转换。默认使用 UTF-8 编码准换。

>>> s = "Python之禅"
>>> s.encode()
b'Python\xe4\xb9\x8b\xe7\xa6\x85'
>>> s.encode("gbk")
b'Python\xd6\xae\xec\xf8'
decode 负责字节到字符的解码转换，通用使用 UTF-8 编码格式进行转换。

>>> b'Python\xe4\xb9\x8b\xe7\xa6\x85'.decode()
'Python之禅'
>>> b'Python\xd6\xae\xec\xf8'.decode("gbk")
'Python之禅'

'''


#===================== re module ===========================  ？？？？？？？？？？？


#===================== 数据结构 ============================
#list操作, list is mutable
l = [3, 5, 7, 9]
print(l + l) 
print(l * 2) #同上
print(l[1:3])
print(3 in l)
l[2] = 10000
print(l) #[3, 5, 10000, 9]

#tuple，类似list，但不可修改
t = (1)
print(t) #定义的不是tuple，是1这个数！这是因为括号()既可以表示tuple，又可以表示数学公式中的小括号，这就产生了歧义，因此，Python规定，这种情况下，按小括号进行计算，计算结果自然是1。
t = (1,)
print(t) #只有1个元素的tuple定义时必须加一个逗号,，来消除歧义，Python在显示只有1个元素的tuple时，也会加一个逗号,，以免你误解成数学计算意义上的括号。
t0 = ()
t1 = (2, 3)
t2 = (3, 4)
print(t0 + t1 + t2) #(2,3,3,4)

#Set,无序无重复！可以使用{}或者set()函数创建，但不可以用{}创建空的set,空的{}是Dic。
s1 = set('abcdefabcdef')
s2 = set('abchigabchig')
print(s1, s2)
print(s1 - s2)
print(s1 | s2) #set没有+操作
print(s1 ^ s2) #不同时存在的
print(s1 & s2)

#Dic, 无序键值对，key必须为不可变类型，并且不重复。
tel = {'J':123, 'M':345}
print(tel)
tel['K'] = 556
print(tel)
del tel['J']
print(tel)
print(list(tel.keys()))
tel1 = dict([('A', 123), ('B', 234), ('C', 223)]) #构造函数
tel2 = dict(A = 123, B = 234, C = 223) #构造函数
print(tel1, tel2)
print('=====================================')


#========================== 函数 function =====================
#返回多个值
'''
比如在游戏中经常需要从一个点移动到另一个点，给出坐标、位移和角度，就可以计算出新的新的坐标。
但其实这只是一种假象，Python函数返回的仍然是单一值,返回值是一个tuple！但是，在语法上，返回一个tuple可以省略括号，而多个变量可以同时接收一个tuple，按位置赋给对应的值，所以，Python的函数返回多值其实就是返回一个tuple，但写起来更方便。
默认参数 (angle = 0) 降低了函数调用的难度，而一旦需要更复杂的调用时，又可以传递更多的参数来实现。无论是简单调用还是复杂调用，函数只需要定义一个。
'''
import math
def move(x, y, step, angle = 0): #angle = 0 是默认参数，放在最后
    nx = x + step * math.cos(angle)
    ny = y - step * math.sin(angle)
    return nx, ny
ballx, bally = move(100, 100, 2, math.pi/4)
print(ballx, bally)
print(move(100, 100, 2))
print('=====================================')

#可变参数
'''
定义可变参数和定义list或tuple参数相比，仅仅在参数前面加了一个*号。在函数内部，参数numbers接收到的是一个tuple，可以传入任意个参数，包括0个参数。
'''
def calc(*numbers):
	sum = 0
	for n in numbers:
		sum = sum + n * n
	return sum
print(calc(1, 2))
print(calc())
nums = (1,2,3,4,5)
print(calc(*nums))
print('=====================================')

#关键字参数 Key value
'''
允许传入0个或任意个含参数名的参数，这些关键字参数在函数内部自动组装为一个dict。
关键字参数可以扩展函数的功能。如一个用户注册的功能，除了用户名和年龄是必填项外，其他都是可选项，利用关键字参数来定义这个函数就能满足注册的需求。和可变参数类似，也可以先组装出一个dict，然后，把该dict转换为关键字参数传进去。
'''
def person(name, age, **kw):
	print('name:', name, 'age:', age, 'other:', kw)
person('Michael', 30)
person('Bob', 35, city='Beijing')
person('Adam', 45, gender='M', job='Engineer')
kw = {'city': 'Beijing', 'job': 'Engineer'}
person('Jack', 24, **kw)
print('=====================================')

#参数组合
'''
在Python中定义函数，可以用必选参数、默认参数、可变参数和关键字参数，这4种参数都可以一起使用，或者只用其中某些，但是请注意，参数定义的顺序必须是：必选参数、默认参数、可变参数和关键字参数。
在函数调用的时候，Python解释器自动按照参数位置和参数名把对应的参数传进去。

最神奇的是通过一个tuple和dict，也可以调用该函数; 对于任意函数，都可以通过类似func(*args, **kw)的形式调用它，无论它的参数是如何定义的。
'''

def func(a, b, c=0, *args, **kw):
	print('a =', a, 'b =', b, 'c =', c, 'args =', args, 'kw =', kw)
func(1, 2)
func(1, 2, c=3)
func(1, 2, 3, 'a', 'b')
func(1, 2, 3, 'a', 'b', x = 99)
args = (1, 2, 3, 4)
kw = {'x': 99}
func(*args, **kw) # a = 1 b = 2 c = 3 args = (4,) kw = {'x': 99}
print('=====================================')







# ================== global ================== ???????????????????

name = 'Ma'
def what():
	''' This is a test about the global variable. If there is no global name, it gonna print Ma'''
	global name
	name = 'wenran'
	print(name)

what()
print(name)
print(what.__doc__)

'''
there is a  __doc__ for every function..
'''


#==================



L = [i for i in range(10)]
print(L)














