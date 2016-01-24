
#coding:utf-8

# ========= 函数 =============================
'''
返回多个值
比如在游戏中经常需要从一个点移动到另一个点，给出坐标、位移和角度，就可以计算出新的新的坐标.
但其实这只是一种假象，Python函数返回的仍然是单一值,返回值是一个tuple！但是，在语法上，返回一个tuple可以省略括号，而多个变量可以同时接收一个tuple，按位置赋给对应的值，所以，Python的函数返回多值其实就是返回一个tuple，但写起来更方便。
默认参数 (angle = 0) 降低了函数调用的难度，而一旦需要更复杂的调用时，又可以传递更多的参数来实现。无论是简单调用还是复杂调用，函数只需要定义一个。
'''
import math
def move(x, y, step, angle = 0): #angle = 0 是默认参数
    nx = x + step * math.cos(angle)
    ny = y - step * math.sin(angle)
    return nx, ny
print move(100, 100, 2, math.pi/4)
print '====================================='

'''
可变参数
传入的参数个数是可变的，可以是1个、2个到任意个，还可以是0个。
要定义出这个函数，我们必须确定输入的参数。由于参数个数不确定，我们首先想到可以把a，b，c……作为一个list或tuple传进来，这样，函数可以定义如下：
def calc(numbers):
    sum = 0
    for n in numbers:
        sum = sum + n * n
    return sum
但是调用的时候，需要先组装出一个list或tuple.

>>> calc([1, 2, 3])
14

可变参数：
def calc(*numbers):
    sum = 0
    for n in numbers:
        sum = sum + n * n
    return sum
定义可变参数和定义list或tuple参数相比，仅仅在参数前面加了一个*号。在函数内部，参数numbers接收到的是一个tuple，因此，函数代码完全不变。但是，调用该函数时，可以传入任意个参数，包括0个参数：
'''
def calc(*numbers):
    sum = 0
    for n in numbers:
        sum = sum + n * n
    return sum

print calc(1, 2)
print calc()
nums = [1,2,3,4,5]
print calc(*nums)
print '====================================='


'''
关键字参数
允许传入0个或任意个含参数名的参数，这些关键字参数在函数内部自动组装为一个dict。请看示例：
def person(name, age, **kw):
    print 'name:', name, 'age:', age, 'other:', kw
函数person除了必选参数name和age外，还接受关键字参数kw。在调用该函数时，可以只传入必选参数,也可以传入任意个数的关键字参数;

关键字参数可以扩展函数的功能。比如，在person函数里，我们保证能接收到name和age这两个参数，但是，如果调用者愿意提供更多的参数，我们也能收到。如一个用户注册的功能，除了用户名和年龄是必填项外，其他都是可选项，利用关键字参数来定义这个函数就能满足注册的需求。
和可变参数类似，也可以先组装出一个dict，然后，把该dict转换为关键字参数传进去。
'''
def person(name, age, **kw):
    print 'name:', name, 'age:', age, 'other:', kw

person('Michael', 30)
person('Bob', 35, city='Beijing')
person('Adam', 45, gender='M', job='Engineer')
kw = {'city': 'Beijing', 'job': 'Engineer'}
person('Jack', 24, **kw)
print '====================================='

'''
参数组合
在Python中定义函数，可以用必选参数、默认参数、可变参数和关键字参数，这4种参数都可以一起使用，或者只用其中某些，但是请注意，参数定义的顺序必须是：必选参数、默认参数、可变参数和关键字参数。

比如定义一个函数，包含上述4种参数：
def func(a, b, c=0, *args, **kw):
    print 'a =', a, 'b =', b, 'c =', c, 'args =', args, 'kw =', kw
在函数调用的时候，Python解释器自动按照参数位置和参数名把对应的参数传进去。

最神奇的是通过一个tuple和dict，你也可以调用该函数; 对于任意函数，都可以通过类似func(*args, **kw)的形式调用它，无论它的参数是如何定义的。
'''

def func(a, b, c=0, *args, **kw):
    print 'a =', a, 'b =', b, 'c =', c, 'args =', args, 'kw =', kw
func(1, 2)
func(1, 2, c=3)
func(1, 2, 3, 'a', 'b')
func(1, 2, 3, 'a', 'b', x=99)
args = (1, 2, 3, 4)
kw = {'x': 99}
func(*args, **kw)
print '====================================='


# ========== 高级特性 ===============
'''
切片
L = ['Michael', 'Sarah', 'Tracy', 'Bob', 'Jack']
取前3个元素，L[0:3]
L[0:3]表示，从索引0开始取，直到索引3为止，但不包括索引3。即索引0，1，2.
如果第一个索引是0，还可以省略：L[:3]

类似的，既然Python支持L[-1]取倒数第一个元素，那么它同样支持倒数切片：
>>> L[-2:]
['Bob', 'Jack']
>>> L[-2:-1]
['Bob']
记住倒数第一个元素的索引是-1。

>>> L = range(100)
前10个数，每两个取一个：
>>> L[:10:2]
[0, 2, 4, 6, 8]
所有数，每5个取一个：
>>> L[::5]
[0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95]
甚至什么都不写，只写[:]就可以原样复制一个list：
>>> L[:]
[0, 1, 2, 3, ..., 99]

tuple也是一种list，唯一区别是tuple不可变。因此，tuple也可以用切片操作，只是操作的结果仍是tuple;

字符串'xxx'或Unicode字符串u'xxx'也可以看成是一种list，每个元素就是一个字符。因此，字符串也可以用切片操作，只是操作结果仍是字符串;
>>> 'ABCDEFG'[:3]
'ABC'
>>> 'ABCDEFG'[::2]
'ACEG'
'''

print 'ABCDEF'[:3]
print 'ABCDEFG'[::2]
print (0, 1, 2, 3, 4, 5)[:3]
print '====================================='


'''
迭代
如果给定一个list或tuple，我们可以通过for循环来遍历这个list或tuple，这种遍历我们称为迭代（Iteration）。

在Python中，迭代是通过for ... in来完成的，Python的for循环不仅可以用在list或tuple上，还可以作用在其他可迭代对象上。比如dict就可以迭代;
默认情况下，dict迭代的是key。如果要迭代value，可以用for value in d.itervalues()，如果要同时迭代key和value，可以用for k, v in d.iteritems()。

由于字符串也是可迭代对象，因此，也可以作用于for循环；
如何判断一个对象是可迭代对象呢？方法是通过collections模块的Iterable类型判断;
Python内置的enumerate函数可以把一个list变成索引-元素对;同时引用了两个变量，在Python里是很常见的;
'''
d = {'a': 1, 'b': 2, 'c': 3}
for key in d:
    print key

for value in d.itervalues():
    print value

for k, v in d.iteritems():
    print k,':',v

for ch in 'ABC':
    print ch

from collections import Iterable
print isinstance('abc', Iterable) # str是否可迭代
print isinstance([1,2,3], Iterable) # list是否可迭代
print isinstance(123, Iterable) # 整数是否可迭代

for i, value in enumerate(['A', 'B', 'C']):
    print i, value

for x, y in [(1, 1), (2, 4), (3, 9)]:
    print x, y

print '====================================='


'''
列表生成式
列表生成式则可以用一行语句代替循环生成上面的list;
写列表生成式时，把要生成的元素放到前面，后面跟for循环，就可以把list创建出来;
for循环后面还可以加上if判断，这样我们就可以筛选出仅偶数的平方;
还可以使用两层循环，可以生成全排列;
'''
print [x * x for x in range(1, 11)]
print [x * x for x in range(1, 11) if x % 2 == 0]
print [m + n for m in 'ABC' for n in 'XYZ']

d = {'x': 'A', 'y': 'B', 'z': 'C' }
print [k + '=' + v for k, v in d.iteritems()]

L = ['Hello', 'World', 'IBM', 'Apple']
print [s.lower() for s in L]


'''
生成器
在循环的过程中不断推算出后续的元素,这样就不必创建完整的list，从而节省大量的空间。
在Python中，这种一边循环一边计算的机制，称为生成器（Generator）。
如果要一个一个打印出来，可以通过generator的next()方法;也可以通过for循环来迭代它。

定义generator的另一种方法。如果一个函数定义中包含yield关键字，那么这个函数就不再是一个普通函数，而是一个generator;这里，最难理解的就是generator和函数的执行流程不一样。函数是顺序执行，遇到return语句或者最后一行函数语句就返回。而变成generator的函数，在每次调用next()的时候执行，遇到yield语句返回，再次执行时从上次返回的yield语句处继续执行。
'''

g = (x * x for x in range(10))
print g.next()
for n in g:
    print n

def fib(max):
    n, a, b = 0, 0, 1
    while n < max:
        yield b
        a, b = b, a + b
        n = n + 1

for n in fib(6):
    print n

print '========================'

# ========= list set==========
l = [1 ,23, 'wenran',]
for i in range(0, len(l)):
	print l[i]

for i in l:
	print i

s = set([1,1,2,2,3,3])
print s

print '========================'


# ==================== 返回函数 =================

'''
函数作为返回值
高阶函数除了可以接受函数作为参数外，还可以把函数作为结果值返回。
在函数lazy_sum中又定义了函数sum，并且，内部函数sum可以引用外部函数lazy_sum的参数和局部变量，当lazy_sum返回函数sum时，相关参数和变量都保存在返回的函数中，这种称为“闭包（Closure）”的程序结构拥有极大的威力。
调用lazy_sum()时，每次调用都会返回一个新的函数，即使传入相同的参数;

闭包
注意到返回的函数在其定义内部引用了局部变量args，所以，当一个函数返回了一个函数后，其内部的局部变量还被新函数引用，所以，闭包用起来简单，实现起来可不容易。另一个需要注意的问题是，返回的函数并没有立刻执行，而是直到调用了f()才执行。我们来看一个例子：

def count():
    fs = []
    for i in range(1, 4):
        def f():
             return i*i
        fs.append(f)
    return fs

f1, f2, f3 = count()
在上面的例子中，每次循环，都创建了一个新的函数，然后，把创建的3个函数都返回了。

你可能认为调用f1()，f2()和f3()结果应该是1，4，9，但实际结果是：

>>> f1()
9
>>> f2()
9
>>> f3()
9
全部都是9！原因就在于返回的函数引用了变量i，但它并非立刻执行。等到3个函数都返回时，它们所引用的变量i已经变成了3，因此最终结果为9。

返回闭包时牢记的一点就是：返回函数不要引用任何循环变量，或者后续会发生变化的变量。

如果一定要引用循环变量怎么办？方法是再创建一个函数，用该函数的参数绑定循环变量当前的值，无论该循环变量后续如何更改，已绑定到函数参数的值不变：

>>> def count():
...     fs = []
...     for i in range(1, 4):
...         def f(j):
...             def g():
...                 return j*j
...             return g
...         fs.append(f(i))
...     return fs
... 
>>> f1, f2, f3 = count()
>>> f1()
1
>>> f2()
4
>>> f3()
9
缺点是代码较长，可利用lambda函数缩短代码。

'''
def lazy_sum(*args):
    def sum():
        ax = 0
        for n in args:
            ax = ax + n
        return ax
    return sum

f = lazy_sum(1, 3, 5, 7, 9)
print f
print f()

f1 = lazy_sum(1, 3, 5, 7, 9)
print f1 == f # return false;


'''
匿名函数
有些时候，不需要显式地定义函数，直接传入匿名函数更方便。

在Python中，对匿名函数提供了有限支持。还是以map()函数为例，计算f(x)=x2时，除了定义一个f(x)的函数外，还可以直接传入匿名函数：

>>> map(lambda x: x * x, [1, 2, 3, 4, 5, 6, 7, 8, 9])
[1, 4, 9, 16, 25, 36, 49, 64, 81]
通过对比可以看出，匿名函数lambda x: x * x实际上就是：

def f(x):
    return x * x
关键字lambda表示匿名函数，冒号前面的x表示函数参数。

匿名函数有个限制，就是只能有一个表达式，不用写return，返回值就是该表达式的结果。

用匿名函数有个好处，因为函数没有名字，不必担心函数名冲突。此外，匿名函数也是一个函数对象，也可以把匿名函数赋值给一个变量，再利用变量来调用该函数：

>>> f = lambda x: x * x
>>> f
<function <lambda> at 0x10453d7d0>
>>> f(5)
25
同样，也可以把匿名函数作为返回值返回，比如：

def build(x, y):
    return lambda: x * x + y * y
小结

Python对匿名函数的支持有限，只有一些简单的情况下可以使用匿名函数。


'''

# === lambda ====
# lambda语句被用来创建新的函数对象,并且在运行时返回它们。

def make_repeater(n): 
    return lambda s, y: s * n + y

twice = make_repeater(2)

print twice('world', '3')
print twice(5,2)


# ==== exec 和 eval语句
# exec语句用来执行储存在字符串或文件中的Python语句.
# eval语句用来计算存储在字符串中的有效Python表达式。
exec 'print "hello world"'
print eval('2*3')





