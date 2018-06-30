#========================= ML Basic ====================================
'''
数据整体DataSet，每一行是一个sample；
Dataset分为X,y：
X通常是个矩阵，多少行就是多少样本，多少列就是多少特征，每一行是一个特征向量。
y是向量，是Label（分类等）。

每个样本就是特征空间中的一个点。分类任务就是在特征空间切分，两个特征就是二维空间。

MNIST数据集，每个像素是一个特征，28*28=784个特征。

机器学习的任务：
分类：
	二分类；
	多分类：手写识别，图像识别等。
	多标签分类：例如一个图标可以分类到多个标签下。	
回归：
	结果是一个连续数字的值，而不是一个类。比如预测房价等。
		
监督学习，非监督学习，半监督学习，增强学习：
	监督学习：训练数据都有标记或者答案。分类和回归都是监督学习。	非监督学习：训练数据没有标记和答案。聚类分析，电商网站为客户分类等。意义：数据降维，特征提取（扔掉无关信息），特征压缩PCA。
	半监督：部分有答案，部分没有。可以用非监督学习做数据处理，在用处理好的数据通过监督学习训练模型。
	增强学习：
	
批量学习，在线学习，参数学习，非参数学习：
	批量学习：简单，训练后模型不再改变（或者定期再训练），适应环境变化能力差。
	在线学习：输入样例输入模型后的结果不浪费（前提是结果正确），而进到训练样本，再次对模型进行训练。
	参数学习：建立模型，通过训练集得到参数。
	非参数学习：	
'''

#====================================================================
#========================= Numpy ====================================
import numpy
print(numpy.__version__)

#python 自带array, 不像list, array限定类型。但在机器学习中仍然不方便，因为不带有向量或矩阵运算。
import array
arr = array.array('i', [i for i in range(10)])
print(arr[5])
arr[5] = 100
print(arr[5])

#numpy array, 同样也限定类型。
nparr = numpy.array([i for i in range(10)])
print(nparr[5])
nparr[5] = 100
print(nparr[5])
print(nparr.dtype) #int 32，如果赋值浮点数，会转为int.

nparr = numpy.array([1, 2, 3.0])
print(nparr)
print(nparr.dtype) #float 64.

#其他方式创建数组
z = numpy.zeros(10) #创建一位数组（向量，矩阵）
print(z, z.dtype) #float 64.
z = numpy.zeros(shape = (3, 5), dtype = int) #传入一个tuple. 3x5矩阵
print(z)

o = numpy.ones((4, 6), dtype = int)
print(o)

s = numpy.full(shape = (5, 7), fill_value = 12)
print(s)

#arange. 与python中range的意义一样。
r = numpy.arange(0, 20, 2)
print(r)
r = numpy.arange(0, 2, 0.2) #可以是浮点，python range不可以
print(r)

#linspace. linear space简写。
l = numpy.linspace(0, 20, 10) # 0与20之间取等差10个数，包括0与20.
print(l)
l = numpy.linspace(0, 20, 11)
print(l)

#random.
r = numpy.random.randint(0, 10) #0到10之间的随机数，不包括10
print(r)
r = numpy.random.randint(0, 10, size = 10)
print(r)
r = numpy.random.randint(0, 10, size = (3, 8)) #随机3x8矩阵
print(r)
numpy.random.seed(12) #可以指定随机数生成种子，保证随机矩阵的一致。

r = numpy.random.random(10) #10个0 1之间的随机数（均匀分布）
print(r)
r = numpy.random.random((3, 4))
print(r)

r = numpy.random.normal() #均值为0，方差为1的正太分布随机数
print(r)
r = numpy.random.normal(3, 4, (4, 5)) #均值为loc = 3，方差为scale = 4的3x5矩阵
print(r)

#=========================== Numpy 数组操作 =====================================
X = numpy.arange(15).reshape((3, 5))
print(X, X.ndim, X.shape, X.size) #ndim = 2, shape = (3,5), size = 15
print(X[2, 1]) #第三行，第二列的元素访问
print(X[:2, :3]) #前两行，前三列
print(X[::-1, ::-1])
print(X[0, :]) #取第一行
print(X[:, 0]) #取第一列

#numpy中矩阵的切片不会创建新矩阵，而是通过引用方式。
X = numpy.arange(16).reshape((4, 4))
subX = X[:2, :3]
subX[0, 0] = 100
print(X) #X中的元素也会变。

#如果要单独创建，可以用copy().
subX = X[:2, :3].copy()
subX[0, 0] = 200
print(subX, X) #X中的元素不变。

#reshape. 
x = numpy.arange(10)
x2 = x.reshape((2, 5))
x3 = x.reshape((1, 10))
print(x, x2, x3) #x 本身并不变。x是一维和x3是二维。
x4 = x.reshape((2, -1)) #表示两行，列自动算

#合并 concatenate
v1 = numpy.array([1, 2, 3])
v2 = numpy.array([4, 5, 6])
v3 = numpy.concatenate([v1, v2])
print(v3)

A = numpy.arange(15).reshape((3, 5))
B = numpy.concatenate([A, A, A]) #默认沿着行方向拼接，9x5 矩阵
print(B)
B = numpy.concatenate([A, A, A], axis = 1) #沿着列方向拼接，3x15矩阵
print(B)

#vstack, hstack.
A = numpy.arange(15).reshape((3, 5))
B = numpy.arange(5)
C = numpy.vstack([A, B]) #不同维度可以拼接
print(C)

#分割
A = numpy.arange(15)
x1, x2, x3 = numpy.split(A, [3, 7])  #分成三段，分成两段也要传入数组
print(x1, x2, x3) #[0,1,2] [3,4,...] [7,8, ...]

A = numpy.arange(16).reshape((4, 4))
A1, A2 = numpy.split(A, [2])
print(A1, A2) #A1是前两行， A2是后两行
A1, A2 = numpy.split(A, [2], axis = 1)
print(A1, A2) #A1是前两列， A2是后两列

#vsplit, hsplit
A = numpy.arange(16).reshape((4, 4))
A1, A2 = numpy.vsplit(A, [3])
print(A1, A2) #A1是前三行， A2是后一行
A1, A2 = numpy.hsplit(A, [3])
print(A1, A2) #A1是前三列， A2是后一列

#=========================== Numpy 矩阵运算 =====================================
L = [i for i in range(10)]
print(2 * L) #两个array拼接，python不支持原生矩阵计算。
L = numpy.array([i for i in range(10)])
print(2 * L) #向量元素x2

#Universal Functions
A = numpy.arange(16).reshape((4, 4))
print(A + 1)
print(A - 1)
print(A * 2)
print(A / 2)
print(A // 2)
print(A % 2)
print(A ** 2) #乘方
print(1 / (A + 1))
print(numpy.abs(A))
print(numpy.sin(A))
print(numpy.cos(A))
print(numpy.tan(A))
print(numpy.exp(A)) # e ^ A
print(numpy.power(3, A))  #3 ^ A
print(numpy.log2(A))
print(numpy.log10(A))

#矩阵之间的运算
A = numpy.arange(9).reshape((3, 3))
B = numpy.arange(9).reshape((3, 3))
print(A + B)
print(A - B)
print(A * B) #元素间运算
print(A / B) #元素间运算
print(A.dot(B)) #矩阵点乘
print(A.T) #矩阵转置，行变列，列变行

#矩阵和向量运算
A = numpy.arange(9).reshape((3, 3))
B = numpy.arange(3)
print(A * B) #元素间运算
print(A.dot(B)) #numpy 会自动判断取行向量或者列向量 B当作列向量

#逆矩阵 AB = BA = I I是单位矩阵，则AB互逆。
A = numpy.arange(4).reshape((2, 2))
invA = numpy.linalg.inv(A)
print(invA)
print(invA.dot(A))
print(A.dot(invA))

#必须是方阵才有逆矩阵，但不是方阵在numpy中可以求伪逆矩阵。
#numpy.linalg.pinv()

#=========================== Numpy 聚合运算 =====================================
A = numpy.arange(20)
print(numpy.sum(A)) #求和，多为数组也可以
print(numpy.min(A)) #最小值
print(numpy.max(A)) #最大值

A = numpy.arange(25).reshape((5, 5))
print(numpy.sum(A, axis = 1)) #求和，每一行
print(numpy.prod(A + 1)) #求积
A[2, 4] = 1000
print(numpy.mean(A)) #求平均
print(numpy.median(A)) #求中位数 ??
print(numpy.percentile(A, q = 25)) # 25%的数小于
print(numpy.var(A)) #方差 ？？
print(numpy.std(A)) #标准差  ？？

#=========================== Numpy 索引 =====================================
A = numpy.arange(20) * 12
print(numpy.argmin(A)) #最小值索引
print(numpy.argmax(A)) #最大值索引

#排序
A = numpy.arange(20)
numpy.random.shuffle(A)
print(A)
A = numpy.sort(A)
print(A)

numpy.random.shuffle(A)
print(A)
A = numpy.argsort(A) #输出索引排序数组
print(A)

#partition
numpy.random.shuffle(A)
print(A)
A = numpy.partition(A, 9) #分成两部分，分别比9小和大
print(A)
 
#=========================== Numpy Fancy Indexing =====================================
A = numpy.arange(20) * 2 
index = [3, 5, 9]
print(A[index])
index = numpy.array([[2, 3], [0, 1]])
print(A[index]) #得到2x2矩阵

A = numpy.arange(20).reshape((5, 4)) * 2 
row = numpy.array([2, 3, 4])
col = numpy.array([2, 3, 1])
print(A[row, col]) # A22 A33 A41
print(A[:, col]) 
print(A[3, col])
col = [True, False, True, False]
print(A[:, col]) # 第一列，第三列

#比较
r = A < 12
print(r) #返回True False 矩阵
r = numpy.all(A < 100)
print(r) # True
r = numpy.sum(A % 2 == 0)
print(r) # 偶数个数


#====================================================================
#=========================== matplotlib =============================
import matplotlib.pyplot as plt
x = numpy.linspace(0, 10, 100)
siny = numpy.sin(x)
cosy = numpy.cos(x)
plt.plot(x, siny)
plt.plot(x, cosy, color = 'red', linestyle = '-.')
plt.xlim(-5, 12)
plt.ylim(-1, 1.5)

plt.scatter(x, siny) #散点图
plt.show()



#====================================================================
#=========================== ML part1 KNN ===========================
'''
K Nearest Neighbors K近邻。监督学习中的分类。

基础的思想是两个样本如果足够相似，那就很大概率是一个类。
取距离目标最近的K个样本，那个类别最多，则目标就是那个类别。、

可以认为是没有模型的算法，或者说训练集本身就是模型。

'''





#====================================================================
#=========================== ML part2 线性回归 Linear Regression ====
'''


'''













