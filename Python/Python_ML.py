#=======================================================================
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

#=========================== Numpy 数组操作 =========================
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

#=========================== Numpy 矩阵运算 =========================
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

#=========================== Numpy 聚合运算 =========================
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

#=========================== Numpy 索引 =============================
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

#=========================== Numpy Fancy Indexing ===================
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
#=========================== ML KNN =================================
'''
K Nearest Neighbors K近邻。监督学习中的分类。

基础的思想是两个样本如果足够相似，那就很大概率是一个类。
取距离目标最近的K个样本，那个类别最多，则目标就是那个类别。、

可以认为是没有模型的算法，或者说训练集本身就是模型。
'''

import numpy as np
from math import sqrt
from collections import Counter

#测试数据：
from sklearn import datasets
iris = datasets.load_iris() #鸢尾花数据集
X_train = iris.data
Y_train = iris.target

#自己定义的KNN
def KNN_classify(k, X_train, Y_train, x):
	assert 1 <= k <= X_train.shape[0], 'k must be valid, less or equal to sample count.'
	assert X_train.shape[0] == Y_train.shape[0], 'sample and result must equal.'
	assert X_train.shape[1] == x.shape[0], 'feature number should be the same.'
	
	distances = [sqrt(np.sum((x_train - x)**2)) for x_train in X_train]
	nearest = np.argsort(distances)
	topK_y = [Y_train[i] for i in nearest[:k]]
	votes = Counter(topK_y)
	
	return votes.most_common(1)[0][0]

result = KNN_classify(6, X_train, Y_train, np.array([0, 0.4, 4, 2]))
print(result)	
	
#scikit-learn中的KNN
from sklearn.neighbors import KNeighborsClassifier
KNN_classifier = KNeighborsClassifier(n_neighbors = 6)
KNN_classifier.fit(X_train, Y_train) #x_train, y_train
result = KNN_classifier.predict([[1, 0.4, 4, 2]])  #
print(result)

'''
超参数：算法运行前决定的参数。
数据归一化：防止结果被某个feature所主导，将所有数据映射到统一尺度。
最值归一化(normalization)：把所有数据映射到0-1之间。x_scale = (x - x_min)/(x_max - x_min)。适用于有明显边界的情况。
均值方差归一化(standardization)：归一到均值为0方差为1的分布中。没有明显边界的情况。x_scale = (x - x_mean)/ S, x_mean为均值，S为方差。
'''


#====================================================================
#=========================== ML 线性回归 Linear Regression ==========
'''
寻找最佳拟合的线性方程。

假设最佳的拟合直线方程是y = a * x + b.
则对于每个样本点x_i, 带入方程，都有预测值：y_ip = a * x_i + b. 每个样本点又有一个真值y_i.  
我们希望预测值y_ip和真值y_i的差最小。

目标：使 sum((y_i - y_ip)^2),i = 1 ~ m 最小。带入y_ip = a * x_i + b. 
就有：sum((y_i - a * x_i + b)^2),i = 1 ~ m, 找到a和b的值，是前面的式子最小，x_i, y_i是训练样本，已知值。

上面的函数叫损失函数（lost function）。于是目标就是损失函数尽可能小。
（或者效用函数尽可能大）

确定损失函数或者效用函数，获得机器学习的模型。参数学习的套路。

最小二乘法问题：最小化误差的平方。
a = sum((x_i - x_mean) * (y_i - y_mean))/sum((x_i - x_mean)^2).
b = y_mean - a * x_mean.
'''
def linearRegression(x_train, y_train, x):
	assert x_train.ndim == 1, 'Simple Linear Regressor can only solve single feature training data.'
	assert len(x_train) == len(y_train), 'the size of x_train must be equal to the size of y_train.'
	x_mean = np.mean(x_train)
	y_mean = np.mean(y_train)

	a = (x_train - x_mean).dot(y_train - y_mean) / (x_train - x_mean).dot(x_train - x_mean)
	b = y_mean - a * x_mean
	
	y = a * x + b
	return y

result = linearRegression(np.array([1, 2, 3, 4]), np.array([2, 2.5, 3, 3.5]), 6)
print(result)

	
#====================================================================
#=========================== ML 梯度下降 Gradient Descent ===========
'''
梯度下降不是机器学习算法，是基于搜索的最优化方法。最小化损失函数。（梯度上升法，最大化效用函数）

-eta * dJ/dtheta.、
eta叫学习率，learning rate. yita是此算法的一个超参数。
不是所有的函数都有唯一的极值点，所以梯度下降的初始位置是另一个超参数。
'''

plot_x = np.linspace(-1, 6, 141) #lost function (plot_x - 2.5)**2 - 1

def dJ(theta):
	return 2 * (theta - 2.5) #导数。

def J(theta): #损失函数
	return (theta - 2.5)**2 - 1

eta = 0.1
epsilon = 1e-8
theta = 0.0
theta_history = [theta]
while True:
	gradient = dJ(theta)
	previous_theta = theta
	theta = theta - eta * gradient
	theta_history.append(theta)
	if(abs(J(theta) - J(previous_theta)) < epsilon):
		break

print(theta, J(theta))
plt.plot(plot_x, J(plot_x))
plt.plot(np.array(theta_history), J(np.array(theta_history)), color = 'r', marker = '+')
plt.show()
	

#====================================================================
#=========================== ML PCA主成分分析与梯度上升 =============
'''
主成分分析，非监督学习，用于数据降维，可视化，去噪。

例如一个二维样本空间，找到一个一维直线，使样本在直线上的间距最大。
方差就是表示间距的一种方式，所以问题就变成找到一个轴，使样本映射后，方差最大。
1. 样本均值归零(demean)，样本减去均值，相当于移动坐标轴。
2. 要找到一个轴w = (w_1, w_2) 使得
	Var(X_project) = 1/m * sum((X_i_project)^2)最大，i = 1 ~ m。
3. 映射的关系就是投影，点乘。X_i_project = X_i.dot(w), 点乘。
4. 于是问题就是求目标函数 Var(X_project) = 1/m * sum((X_i.doc(w))^2)的最大值。

上面的式子中w是未知量。
'''


#====================================================================
#=========================== ML SVM 支持向量机 ======================
'''
分类问题：
例如在二维特征平面，决策边界不唯一。（线性可分）

SVM想解决的问题是决策边界的泛化能力，也就是找到一条最优的决策边界，离两个类别最近的训练样本都最远。
最近的样本就是支持向量。支 持向量所组成的两条线的距离叫margin = 2 * d.
SVM就是最大化margin或者d。

点(x, y)到直线 Ax + By + C = 0距离:  abs(Ax + By + C)/sqrt(A^2 + B^2)
对于两个类中的任何点：距离应该都大于等于d, 或者小于等于-d

支持向量机要求的就是A B C，AB可以用一个向量w表示。
推导后的公式：
y_i * (inv(w) * x_i + b) >= 1，这是条件。在满足之前条件下，对于任意支持向量x, 最小化w的模。

Soft Margin SVM.加一个容错空间。
'''


#====================================================================
#=========================== ML 决策树 Decision Tree ================
'''
每一个节点都是一个判断信息，每个叶子都是最后的结果或者分类。

非参数学习算法，可以解决多分类问题。
首先找到一个维度，然后找到该维度的一个阈值作为依据判断。

信息熵：随机变量的不确定度，不确定度就越大，熵越大，反之。
H = -sum(Pi * log(Pi)), i = 0~k. k类信息，Pi是每个信息所占比例。
H最小值是0，说明数据约确定。

二分类，H = -x * log(x) - (1 - x) * log(1 - x)
'''

import matplotlib.pyplot as plt
import numpy as np
def entropy(p):
	return -p * np.log(p) - (1 - p) * np.log(1 - p)
x = np.linspace(0.01, 0.99, 200)
plt.plot(x, entropy(x))
plt.show() #0.5是峰值，表示二分类概率是0.5是，不确定度越大。

'''
决策树在划分后应该使子类的信息熵降低。
'''