# Spark

基于内存计算的大数据并行计算框架。计算的中间值存在于内存中。是MapReduce的替代方案。兼容HDFS，Hive等。本身是Scala开发，运行与JVM上。

Hadoop的中间计算结果会落盘（磁盘开销，序列化（结构体到可存储数据，json，string的过程）与反序列化（可存储数据到结构体的过程）开销），导致计算时效差，不适用与交互处理，更适合离线处理。Spark基于内存，计算时间是秒级和分钟级。

Spark没有存储部分，所以只是对等于Hadoop中的MapReduce。所有Spark取代Hadoop的说法不准确。

Spark拥有多种语言的函数式编程API，提供了除map和reduce之外更多的运算符，这些操作是通过一个称作弹性分布式数据集(resilient distributed datasets, RDD)的分布式数据框架进行的。

Spark vs Flink：流式计算方面Flink更优秀，实时性更好，Spark是模拟流式计算，本质还是批处理。


## RDD

弹性分布式数据集RDD（Resillient Distributed Dataset）。数据加载到内存生成RDD，多个RDD的依赖关系行程DAG。RDD是种编程抽象，高度受限（只读），代表可以跨机器进行分割的只读对象集合。RDD可以从一个继承结构（lineage）重建（因此可以容错），通过并行操作访问，可以读写HDFS或S3这样的分布式存储，可以缓存到worker节点的内存中进行立即重用。由于RDD可以被缓存在内存中，Spark对迭代应用特别有效，因为这些应用中，数据是在整个算法运算过程中都可以被重用。大多数机器学习和最优化算法都是迭代的，使得Spark对数据科学来说是个非常有效的工具。另外，可以通过类似Python REPL的命令行提示符交互式访问。


## 核心组件：

![Spark](./img/spark.jpg)

- Spark Core：包含Spark的基本功能；尤其是定义RDD的API、操作以及这两者上的动作。其他Spark的库都是构建在RDD和Spark Core之上的。
- Spark SQL：提供通过Apache Hive的SQL变体Hive查询语言（HiveQL）与Spark进行交互的API。每个数据库表被当做一个RDD，Spark SQL查询被转换为Spark操作。对熟悉Hive和HiveQL的人，Spark可以拿来就用。
- Spark Streaming：允许对实时数据流进行处理和控制。很多实时数据库（如Apache Store）可以处理实时数据。Spark Streaming允许程序能够像普通RDD一样处理实时数据。
- MLlib：一个常用机器学习算法库，算法被实现为对RDD的Spark操作。这个库包含可扩展的学习算法，比如分类、回归等需要对大量数据集进行迭代的操作。之前可选的大数据机器学习库Mahout，将会转到Spark，并在未来实现。
- GraphX：控制图、并行图操作和计算的一组算法和工具的集合。GraphX扩展了RDD API，包含控制图、创建子图、访问路径上所有顶点的操作。

Spark提供了使用Scala、Java和Python编写的API。


## Spark编程

编写Spark应用与在Hadoop上的其他数据流语言类似。代码写入一个惰性求值的驱动程序（driver program）中，通过一个动作（action），驱动代码被分发到集群上，由各个RDD分区上的worker来执行。然后结果会被发送回驱动程序进行聚合或编译。本质上，驱动程序创建一个或多个RDD，调用操作来转换RDD，然后调用动作处理被转换后的RDD。

这些步骤大体如下：

1. 定义一个或多个RDD，可以通过获取存储在磁盘上的数据（HDFS，Cassandra，HBase，Local Disk），并行化内存中的某些集合，转换（transform）一个已存在的RDD，或者，缓存或保存。
2. 通过传递一个闭包（函数）给RDD上的每个元素来调用RDD上的操作。Spark提供了除了Map和Reduce的80多种高级操作。
3. 使用结果RDD的动作（action）（如count、collect、save等）。动作将会启动集群上的计算。

当Spark在一个worker上运行闭包时，闭包中用到的所有变量都会被拷贝到节点上，但是由闭包的局部作用域来维护。Spark提供了两种类型的共享变量，这些变量可以按照限定的方式被所有worker访问。广播变量会被分发给所有worker，但是是只读的。累加器这种变量，worker可以使用关联操作来“加”，通常用作计数器。

Spark应用本质上通过转换和动作来控制RDD。


## Spark架构与执行

- Driver Node.
- Manager（资源调度，可以用自带的，Yarn，Mesos）
- Worker Node，有Executor进程，又分多个线程，每个线程负责一个任务。

Spark应用作为独立的进程运行，由驱动程序中的**SparkContext**协调。这个context将会连接到一些集群管理者（如YARN），这些管理者分配系统资源。集群上的每个worker由执行者（executor）管理，执行者反过来由SparkContext管理。执行者管理计算、存储，还有每台机器上的缓存。

过程：

RDD -> SparkContext -> DAG图 -> DAG Scheduler -> Task Scheduler -> WorkerNode -> Executor进程

特性：

- 基于事件驱动，代码中对RDD的操作，会转换成DAG。
- Spark RDD操作分为两大类，transformation和action。
- 惰性调用机制，也就是转换只会被记录，只有到了action，才开始一整套执行。
- RDD是粗粒度转换，不能对RDD中一部分进行转换。

重点要记住的是应用代码由Driver发送给Executor，执行者指定context和要运行的任务。执行者与驱动程序通信进行数据分享或者交互。驱动程序是Spark作业的主要参与者，因此需要与集群处于相同的网络。这与Hadoop代码不同，Hadoop中你可以在任意位置提交作业给JobTracker，JobTracker处理集群上的执行。

### 作业切割

一个DAG就是一个作业。

宽依赖窄依赖。Shuffle操作，比如词频统计中不同机器处理不同的单词，涉及到大量的网络分发。
一个父RDD对应多个子RDD分区，就会有shuffle操作，shuffle操作会写磁盘，因为又等待的过程，此时就是宽依赖。遇到宽依赖会进行任务阶段划分，而遇到窄依赖不会。因为宽依赖无法进行流水线优化（得等），而窄依赖可以优化等待的过程。

优化过程就是反向解析DAG图，如果遇到窄依赖就加到前一个RDD的阶段，遇到宽依赖就断开成新的阶段。


## spark shell

spark-shell读取parquet文件。
```scala
val sqlContext = new org.apache.spark.sql.SQLContext(sc)
val parquetFile = sqlContext.parquetFile("/Users/wrma/Downloads/basic.parquet")
parquetFile.take(200).foreach(println)

// second way:
val p = spark.read.load("/Users/wrma/Downloads/basic.parquet")
// 查询 Schema 和数据
p.printSchema
p.show
p.show(10) //显示10行

p.select($"seller_network_id",$"postal_code",$"date").show
p.select($"seller_network_id",$"postal_code",$"date").write.save("/Users/wrma/Downloads/test.parquet")
```


## 与Spark交互

使用Spark最简单的方式就是使用交互式命令行提示符。

### PySpark
Python的交互命令，在命令行中打出pyspark。PySpark将会自动使用本地Spark配置创建一个SparkContext。你可以通过sc变量来访问它。我们来创建第一个RDD。
```bash
>>> text = sc.textFile("BigData.md")
>>> print(text)
BigData.md MapPartitionsRDD[1] at textFile at NativeMethodAccessorImpl.java:0
```
textFile方法将BigData.md加载到一个RDD命名文本。如果查看了RDD，你就可以看出它是个MappedRDD，文件路径是相对于当前工作目录的一个相对路径。我们转换下这个RDD，来进行分布式计算的“hello world”：“字数统计”。
```bash
>>> from operator import add
>>> def tokenize(text):
...     return text.split()
...
>>> words=text.flatMap(tokenize)
>>> print(words)
PythonRDD[2] at RDD at PythonRDD.scala:53
```
首先导入add操作符，它是个命名函数，可以作为加法的闭包来使用。我们稍后再使用这个函数。首先我们要做的是把文本拆分为单词。我们创建了一个tokenize函数，参数是文本片段，返回根据空格拆分的单词列表。然后我们通过给flatMap操作符传递tokenize闭包对textRDD进行变换创建了一个wordsRDD。你会发现，words是个PythonRDD，但是执行本应该立即进行。显然，我们还没有把整个莎士比亚数据集拆分为单词列表。

如果你曾使用MapReduce做过Hadoop版的“字数统计”，你应该知道下一步是将每个单词映射到一个键值对，其中键是单词，值是1，然后使用reducer计算每个键的1总数。

首先，我们map一下。
```bash
>>> wc = words.map(lambda x: (x,1))
>>> print wc.toDebugString()
b'(2) PythonRDD[3] at RDD at PythonRDD.scala:53 []\n |  BigData.md MapPartitionsRDD[1] at textFile at NativeMethodAccessorImpl.java:0 []\n |  BigData.md HadoopRDD[0] at textFile at NativeMethodAccessorImpl.java:0 []'
```
我使用了一个匿名函数（用了Python中的lambda关键字）而不是命名函数。这行代码将会把lambda映射到每个单词。因此，每个x都是一个单词，每个单词都会被匿名闭包转换为元组(word, 1)。为了查看转换关系，我们使用toDebugString方法来查看PipelinedRDD是怎么被转换的。可以使用reduceByKey动作进行字数统计，然后把统计结果写到磁盘。
```bash
>>> counts = wc.reduceByKey(add)
>>> counts.saveAsTextFile("wc")
```
一旦我们最终调用了saveAsTextFile动作，这个分布式作业就开始执行了，在作业“跨集群地”（或者你本机的很多进程）运行时，你应该可以看到很多INFO语句。如果退出解释器，你可以看到当前工作目录下有个“wc”目录。
```bash
$ ls wc/
_SUCCESS   part-00000 part-00001
```
每个part文件都代表你本机上的进程计算得到的被保持到磁盘上的最终RDD。

注意这些键没有像Hadoop一样被排序（因为Hadoop中Map和Reduce任务中有个必要的打乱和排序阶段）。但是，能保证每个单词在所有文件中只出现一次，因为你使用了reduceByKey操作符。你还可以使用sort操作符确保在写入到磁盘之前所有的键都被排过序。

### spark-shell




## 编写一个Spark应用
编写Spark应用与通过交互式控制台使用Spark类似。API是相同的。首先，你需要访问SparkContext，它已经由pyspark自动加载好了。

使用Spark编写Spark应用的一个基本模板如下：
```python
## Spark Application - execute with spark-submit
 
## Imports
from pyspark import SparkConf, SparkContext
 
## Module Constants
APP_NAME = "My Spark Application"
 
## Closure Functions
 
## Main functionality
 
def main(sc):
    pass
 
if __name__ == "__main__":
    # Configure Spark
    conf = SparkConf().setAppName(APP_NAME)
    conf = conf.setMaster("local[*]")
    sc   = SparkContext(conf=conf)
 
    # Execute Main functionality
    main(sc)
```
这个模板列出了一个Spark应用所需的东西：导入Python库，模块常量，用于调试和Spark UI的可识别的应用名称，还有作为驱动程序运行的一些主要分析方法学。在ifmain中，我们创建了SparkContext，使用了配置好的context执行main。我们可以简单地导入驱动代码到pyspark而不用执行。注意这里Spark配置通过setMaster方法被硬编码到SparkConf，一般你应该允许这个值通过命令行来设置，所以你能看到这行做了占位符注释。

使用sc.stop()或sys.exit(0)来关闭或退出程序。

```python
## Spark Application - execute with spark-submit
 
## Imports
import csv
import matplotlib.pyplot as plt
 
from StringIO import StringIO
from datetime import datetime
from collections import namedtuple
from operator import add, itemgetter
from pyspark import SparkConf, SparkContext
 
## Module Constants
APP_NAME = "Flight Delay Analysis"
DATE_FMT = "%Y-%m-%d"
TIME_FMT = "%H%M"
 
fields   = ('date', 'airline', 'flightnum', 'origin', 'dest', 'dep',
            'dep_delay', 'arv', 'arv_delay', 'airtime', 'distance')
Flight   = namedtuple('Flight', fields)
 
## Closure Functions
def parse(row):
    """
    Parses a row and returns a named tuple.
    """
 
    row[0]  = datetime.strptime(row[0], DATE_FMT).date()
    row[5]  = datetime.strptime(row[5], TIME_FMT).time()
    row[6]  = float(row[6])
    row[7]  = datetime.strptime(row[7], TIME_FMT).time()
    row[8]  = float(row[8])
    row[9]  = float(row[9])
    row[10] = float(row[10])
    return Flight(*row[:11])
 
def split(line):
    """
    Operator function for splitting a line with csv module
    """
    reader = csv.reader(StringIO(line))
    return reader.next()
 
def plot(delays):
    """
    Show a bar chart of the total delay per airline
    """
    airlines = [d[0] for d in delays]
    minutes  = [d[1] for d in delays]
    index    = list(xrange(len(airlines)))
 
    fig, axe = plt.subplots()
    bars = axe.barh(index, minutes)
 
    # Add the total minutes to the right
    for idx, air, min in zip(index, airlines, minutes):
        if min > 0:
            bars[idx].set_color('#d9230f')
            axe.annotate(" %0.0f min" % min, xy=(min+1, idx+0.5), va='center')
        else:
            bars[idx].set_color('#469408')
            axe.annotate(" %0.0f min" % min, xy=(10, idx+0.5), va='center')
 
    # Set the ticks
    ticks = plt.yticks([idx+ 0.5 for idx in index], airlines)
    xt = plt.xticks()[0]
    plt.xticks(xt, [' '] * len(xt))
 
    # minimize chart junk
    plt.grid(axis = 'x', color ='white', linestyle='-')
 
    plt.title('Total Minutes Delayed per Airline')
    plt.show()
 
## Main functionality
def main(sc):
 
    # Load the airlines lookup dictionary
    airlines = dict(sc.textFile("ontime/airlines.csv").map(split).collect())
 
    # Broadcast the lookup dictionary to the cluster
    airline_lookup = sc.broadcast(airlines)
 
    # Read the CSV Data into an RDD
    flights = sc.textFile("ontime/flights.csv").map(split).map(parse)
 
    # Map the total delay to the airline (joined using the broadcast value)
    delays  = flights.map(lambda f: (airline_lookup.value[f.airline],
                                     add(f.dep_delay, f.arv_delay)))
 
    # Reduce the total delay for the month to the airline
    delays  = delays.reduceByKey(add).collect()
    delays  = sorted(delays, key=itemgetter(1))
 
    # Provide output from the driver
    for d in delays:
        print "%0.0f minutes delayed\t%s" % (d[1], d[0])
 
    # Show a bar chart of the delays
    plot(delays)
 
if __name__ == "__main__":
    # Configure Spark
    conf = SparkConf().setMaster("local[*]")
    conf = conf.setAppName(APP_NAME)
    sc   = SparkContext(conf=conf)
 
    # Execute Main functionality
    main(sc)
```
使用spark-submit命令来运行这段代码（假设你已有ontime目录，目录中有两个CSV文件）：
```bash
~$ spark-submit app.py
```
这个Spark作业使用本机作为master，并搜索app.py同目录下的ontime目录下的2个CSV文件。最终结果显示，4月的总延误时间（单位分钟），既有早点的（如果你从美国大陆飞往夏威夷或者阿拉斯加），但对大部分大型航空公司都是延误的。注意，我们在app.py中使用matplotlib直接将结果可视化出来了。

特别注意下与Spark最直接相关的main函数。首先，加载CSV文件到RDD，然后把split函数映射给它。split函数使用csv模块解析文本的每一行，并返回代表每行的元组。最后，我们将collect动作传给RDD，这个动作把数据以Python列表的形式从RDD传回驱动程序。本例中，airlines.csv是个小型的跳转表（jump table），可以将航空公司代码与全名对应起来。我们将转移表存储为Python字典，然后使用sc.broadcast广播给集群上的每个节点。

接着，main函数加载了数据量更大的flights.csv。拆分CSV行完成之后，我们将parse函数映射给CSV行，此函数会把日期和时间转成Python的日期和时间，并对浮点数进行合适的类型转换。每行作为一个NamedTuple保存，名为Flight，以便高效简便地使用。

有了Flight对象的RDD，我们映射一个匿名函数，这个函数将RDD转换为一些列的键值对，其中键是航空公司的名字，值是到达和出发的延误时间总和。使用reduceByKey动作和add操作符可以得到每个航空公司的延误时间总和，然后RDD被传递给驱动程序（数据中航空公司的数目相对较少）。最终延误时间按照升序排列，输出打印到了控制台，并且使用matplotlib进行了可视化。

这个例子能演示出集群和驱动程序之间的相互作用（发送数据进行分析，结果取回给驱动程序），以及Python代码在Spark应用中的角色。

### 打包
sbt或者maven可以编译和打包app代码，生成jar文件。
然后通过spark-submit提交。
