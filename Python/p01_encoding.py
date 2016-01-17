#coding:utf-8

# ==================== 编码 =========================
'''
Unicode标准在不断发展，但最常用的是用两个字节表示一个字符（如果要用到非常偏僻的字符，就需要4个字节）.
ASCII编码和Unicode编码的区别：ASCII编码是1个字节，而Unicode编码通常是2个字节。
字母A用ASCII编码是十进制的65，二进制的01000001；
字符0用ASCII编码是十进制的48，二进制的00110000；

汉字 '中' 已经超出了ASCII编码的范围，用Unicode编码是十进制的20013，二进制的01001110 00101101。
如果把ASCII编码的A用Unicode编码，只需要在前面补0就可以，因此，A的Unicode编码是00000000 01000001。

新的问题又出现了：如果统一成Unicode编码，乱码问题从此消失了。但是，如果文本基本上全部是英文的话，用Unicode编码比ASCII编码需要多一倍的存储空间，在存储和传输上就十分不划算。

所以，本着节约的精神，又出现了把Unicode编码转化为“可变长编码”的UTF-8编码。UTF-8编码把一个Unicode字符根据不同的数字大小编码成1-6个字节，常用的英文字母被编码成1个字节，汉字通常是3个字节，只有很生僻的字符才会被编码成4-6个字节。如果你要传输的文本包含大量英文字符，用UTF-8编码就能节省空间：

字符	ASCII		Unicode					UTF-8
A	01000001	00000000 01000001		01000001
中	x			01001110 00101101		11100100 10111000 10101101
可以发现，UTF-8编码有一个额外的好处，就是ASCII编码实际上可以被看成是UTF-8编码的一部分，所以，只支持ASCII编码的历史遗留软件可以在UTF-8编码下继续工作。

Python提供了ord()和chr()，unichr()函数，可以把字母和对应的数字相互转换。
chr()函数用一个范围在range（256）内的（就是0～255）整数作参数，返回一个对应的字符。unichr()跟它一样，只不过返回的是Unicode字符.
ord()函数是chr()函数（对于8位的ASCII字符串）或unichr()函数（对于Unicode对象）的配对函数，它以一个字符（长度为1的字符串）作为参数，返回对应的ASCII数值，或者Unicode数值，如果所给的Unicode字符超出了你的Python定义范围，则会引发一个TypeError的异常。

Python在后来添加了对Unicode的支持，以Unicode表示的字符串用u'...'表示
把u'xxx'转换为UTF-8编码的'xxx'用encode('utf-8')方法
反过来，把UTF-8编码表示的字符串'xxx'转换为Unicode字符串u'xxx'用decode('utf-8')
'''

print ord('A')
print ord(u'中')
print chr(65)
print unichr(324)

a = u'''xxxxxxx
sss \' 
\\
\"
ssdf\n
dfss'''

print a

print u'xxx\
xxxx'
# \表示换行


# ===================== Format =========================
'''
在Python中，采用的格式化方式和C语言是一致的，用%实现，举例如下：

%d	整数
%f	浮点数
%s	字符串
%x	十六进制整数

有些时候，字符串里面的%是一个普通字符怎么办？这个时候就需要转义，用%%来表示一个%：
'''

print 'Hello, %s' % 'world'
print 'Hi, %s, you have $%d.' % ('Michael', 1000000)
print 'growth rate: %d %%' % 7


# =========================================

# to show the Library under usr
# $ chflags nohidden ~/Library/
# $ chflags hidden ~/Library/


# ================== global ==================

name = 'Ma'
def what():
	''' This is a test about the glabal variable. If there is no global name, it gonna print Ma'''
	global name
	name = 'wenran'
	print name

what()
print name
print what.__doc__

'''
there is a  __doc__ for every function..
'''


# ================= list and tuple ==================

'''
>>> t = (1)
>>> t
1
定义的不是tuple，是1这个数！这是因为括号()既可以表示tuple，又可以表示数学公式中的小括号，这就产生了歧义，因此，Python规定，这种情况下，按小括号进行计算，计算结果自然是1。

所以，只有1个元素的tuple定义时必须加一个逗号,，来消除歧义：

>>> t = (1,)
>>> t
(1,)
Python在显示只有1个元素的tuple时，也会加一个逗号,，以免你误解成数学计算意义上的括号。
'''
t = (1)
print t
t = (1,)
print t

