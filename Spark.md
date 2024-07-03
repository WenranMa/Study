# Spark

## 基础
基于内存计算的大数据并行计算框架。计算的中间值存在于内存中。是MapReduce的替代方案。兼容HDFS，Hive等。本身是Scala开发，运行与JVM上。

Hadoop的中间计算结果会落盘（磁盘开销，序列化（结构体到可存储数据，json，string的过程）与反序列化（可存储数据到结构体的过程）开销），导致计算时效差，不适用与交互处理，更适合离线处理。Spark基于内存，计算时间是秒级和分钟级。

Spark没有存储部分，所以只是对等于Hadoop中的MapReduce。所有Spark取代Hadoop的说法不准确。

Spark拥有多种语言的函数式编程API，提供了除map和reduce之外更多的运算符，这些操作是通过一个称作弹性分布式数据集(resilient distributed datasets, RDD)的分布式数据框架进行的。

Spark vs Flink：流式计算方面Flink更优秀，实时性更好，Spark是模拟流式计算，本质还是批处理。

### RDD
弹性分布式数据集RDD（Resillient Distributed Dataset）。数据加载到内存生成RDD，多个RDD的依赖关系行程DAG。RDD是种编程抽象，高度受限（只读），代表可以跨机器进行分割的只读对象集合。RDD可以从一个继承结构（lineage）重建（因此可以容错），通过并行操作访问，可以读写HDFS或S3这样的分布式存储，可以缓存到worker节点的内存中进行立即重用。由于RDD可以被缓存在内存中，Spark对迭代应用特别有效，因为这些应用中，数据是在整个算法运算过程中都可以被重用。大多数机器学习和最优化算法都是迭代的，使得Spark对数据科学来说是个非常有效的工具。另外，可以通过类似Python REPL的命令行提示符交互式访问。

### 核心组件：
![Spark](./img/spark.JPG?raw=true)

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


### Spark架构与执行

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

### RDD编程
spark shell会自动创建SparkContext，变量名sc，可以通过sc访问。

#### 生成RDD

- textFile()，按行读入文件，生成RDD，每一行就是一个RDD元素，是个String类型。
- parallelize()方法，传入一个集合，也能生成RDD。

#### RDD操作
常见Transformation：

- filter(fucn) 筛选。
- map(func) 将RDD每个元素map到一个func中，得到新的RDD，例如map(x => x + 10)。
- flatMap(func) 与map类似，但每个元素又映射出多个结果。
- groupByKey() 分组，并得到key - value list。
- reduceByKey 分组，并对value list加和。

常见Action：

- count() 返回元素个数。
- collect() 以数组形式返回数据集所有元素。
- first() 返回第一个。
- take(n) 返回前n个。
- reduce(func) 通过func聚合。
- foreach(func) 遍历。

#### 持久化
如果遇到连续两次的动作类型操作，每次都会是从头到尾的计算，因为每次遇到action，spark就会生成一个job，所以一个程序可能会有生成多个job。为了节省资源，需要缓存：

- persist()方法，可以传入MEMORY_ONLY，MEMORY_AND_DISK。只是标记，只有遇到动作类型操作时才生效。
- cache() 等同于persist(MEMORY_ONLY)

rdd.cache()之后，遇到第一个动作，会从头到尾计算，遇到第二个，会调用缓存中的RDD，并不会从头到尾再计算。

#### RDD分区
分区可以增加并行度，减少网络开销？

分区原则：分区数和CPU核数（集群中所有的）尽量一致。

设置分区方法：
- textFile(path, partitionNum)
- parallelize() 方法进行分区。
- repartition() 重新分区。

自定义分区：定义类，继承org.apache.spark.Partitioner。
- 实现numPartitions:Int
- getPartition(key: Any): Int 返回该key的分区编号。
- equals()

只支持键值对。

- map((_,1)) 	//组成map操作。
- map(_._1)	//还原操作。


### 键值对RDD
```java
//spark-shell
//way no.1
val lines = sc.textFile("file:///Users/wrma/Working/Scala/car.scala")
val pairRDD = lines.flatMap(line => line.split(" ")).map(word => (word, 1)) //键值对RDD
pairRDD.foreach(println)

//way no.2
scala> val l = List("wrma", "xyhu")
//l: List[String] = List(wrma, xyhu)

scala> val rdd = sc.parallelize(l)
//rdd: org.apache.spark.rdd.RDD[String] = ParallelCollectionRDD[4] at parallelize at <console>:26

scala> val pairRDD = rdd.map(word => (word,1))
//pairRDD: org.apache.spark.rdd.RDD[(String, Int)] = MapPartitionsRDD[5] at map at <console>:25

scala> pairRDD foreach println
//(wrma,1)
//(xyhu,1)
```

常见操作：reduceByKey(func)，groupByKey()，keys，values，sortByKey()，sortBy()，mapValues()
```java
scala> val w = Array("one","two","two","three","three","three")
//w: Array[String] = Array(one, two, two, three, three, three)

scala> val wRDD = sc.parallelize(w).map(word => (word, 1))
//wRDD: org.apache.spark.rdd.RDD[(String, Int)] = MapPartitionsRDD[7] at map at <console>:26

scala> wRDD.foreach(println)
// (three,1)
// (three,1)
// (two,1)
// (three,1)
// (two,1)
// (one,1)

scala> val r = wRDD.reduceByKey(_ + _)
//r: org.apache.spark.rdd.RDD[(String, Int)] = ShuffledRDD[8] at reduceByKey at <console>:25

scala> r.foreach(println)
// (one,1)
// (two,2)
// (three,3)

scala> val r1 = wRDD.reduceByKey((a,b)=> a + b)
//r1: org.apache.spark.rdd.RDD[(String, Int)] = ShuffledRDD[9] at reduceByKey at <console>:25

scala> r1.foreach(println)
// (one,1)
// (two,2)
// (three,3)

scala> val g = wRDD.groupByKey()
//g: org.apache.spark.rdd.RDD[(String, Iterable[Int])] = ShuffledRDD[10] at groupByKey at <console>:25

scala> g.foreach(println)
// (one,CompactBuffer(1))
// (three,CompactBuffer(1, 1, 1))
// (two,CompactBuffer(1, 1))

scala> val g1 = wRDD.groupByKey().map(t => (t._1,t._2.sum))
//g1: org.apache.spark.rdd.RDD[(String, Int)] = MapPartitionsRDD[12] at map at <console>:25

scala> g1.foreach(println)
// (one,1)
// (two,2)
// (three,3)

scala> g1.keys.foreach(println)	//不能加括号keys()
// two
// one
// three

scala> g1.values.foreach(println)
// 1
// 2
// 3

scala> g1.sortByKey().foreach(println) //not sure about this ???
// (two,2)
// (three,3)
// (one,1)

scala> g1.sortByKey(false).foreach(println)
// (one,1)
// (two,2)
// (three,3)

scala> g1.sortBy(_._2).foreach(println)
// (one,1)
// (two,2)
// (three,3)

scala> g1.mapValues(x=>x+1).foreach(println)	//只改变value.
// (one,2)
// (two,3)
// (three,4)
```

join()操作：
```java
scala> val r1 = sc.parallelize(Array(("spark",1),("spark",2)))
scala> val r2 = sc.parallelize(Array(("spark","good"),("spark","perfect")))
scala> r1.join(r2).foreach(println)
// (spark,(1,good))
// (spark,(1,perfect))
// (spark,(2,good))
// (spark,(2,perfect))
```

例子：求书的日平均销量。key是书名，value是销量，每一条是一天。
```java
scala> val books = sc.parallelize(Array(("spark",2), ("hadoop", 3), ("spark", 6), ("hadoop",11)))
scala> books.mapValues(x=>(x,1)).reduceByKey((x,y) => (x._1 + y._1, x._2 + y._2)).mapValues(x => (x._1 / x._2)).collect()
//res5: Array[(String, Int)] = Array((hadoop,7), (spark,4))
scala> res5.foreach(println)
//(hadoop,7)
//(spark,4)
```

### 数据读写
文件：
```java
val t = sc.textFile("file:///Users/wrma/Working/Scala/car.scala")
t.saveAsTextFile("file:///Users/wrma/Working/Scala/writeBack")	//指定目录，而且只能是目录。目录下会有 _SUCCESS文件和具体的part文件（分区文件）。

//再次读的时候只要指定目录即可。
val t1 = sc.textFile("file:///Users/wrma/Working/Scala/writeBack")
```

HDFS文件：
```java
val t = sc.textFile("hdfs://")
t.saveAsTextFile("hdfs:// ... /writeBack")	//指定目录，而且只能是目录。目录下会有 _SUCCESS文件和具体的part文件（分区文件）。

//再次读的时候只要指定目录即可。
val t1 = sc.textFile("hdfs:// ... /writeBack")
```

JSON文件：
???


读写HBASE：

HBASE是以HDFS做基础的。

稀疏 多维度 排序 映射表

有四个概念：行键，列族，列限定符，时间戳。

HBASE可以支持数十亿行，百万列，一个列族可以有多个列，列又叫列限定符。有单元格的概念，可以通过行键，时间戳，列族，列限定符确定一个单元格，即四维定位，HBASE的读写都是按单元格来的。

时间戳是因为HDFS只允许一次写入，多次读取，所以单元格不能被改写，只能生成新的版本，为了获取新版本，需要时间戳。

时间戳是自动生成的，取数据也是取最新版本。

分区是先按照行切，再按照列族切。



## Spark SQL

Hive：SQL on Hadoop，就是把sql转成MapReduce程序。

Spark也需要一个类似的工具，早期就是Hive on Spark -- Shark，把sql转成Spark程序，照搬Hive而存在问题。后来就有了Spark SQL。

### DataFrame
可以理解为带有Schema信息的RDD。

Spark SQL融合了结构化和非结构化数据的查询和计算。
不是所有的数据都是结构化的，非结构化和半结构化的数据可以转换成DataFrame，从而通过Spark SQL进行查询。

DataFrame 可以通过SparkSession创建。

```java
import org.apach.spark.sql.SparkSession
val s = SparkSession.builder().getOrCreate()
```

spark-shell启动后会自动创建spark，sc两个对象，分别是SparkSession和SparkContext的sc。

编程中必须手动建立。

json，parquet，csv都可以加载生成DataFrame。

- spark.read.json(...) //...表示路径
- spark.read.parquet(...)
- spark.read.csv(...)

#### DataFrame操作

```java
scala> val df = spark.read.json("file:///Users/wrma/Working/Java/spark/examples/src/main/resources/people.json")
//df: org.apache.spark.sql.DataFrame = [age: bigint, name: string]

scala> df.show()
// +----+-------+
// | age|   name|
// +----+-------+
// |null|Michael|
// |  30|   Andy|
// |  19| Justin|
// +----+-------+

scala> df.select("name").show()
// +-------+
// |   name|
// +-------+
// |Michael|
// |   Andy|
// | Justin|
// +-------+

scala> df.select("name").write.format("csv").save("file:///Users/wrma/Working/Scala/name")
// 写文件，只要给出路径地址，不要写文件名，路径下会存储_SUCCESS和文件本身。

scala> df.printSchema
// root
//  |-- age: long (nullable = true)
//  |-- name: string (nullable = true)

scala> df.filter(df("age")> 20).show
// +---+----+
// |age|name|
// +---+----+
// | 30|Andy|
// +---+----+

scala> df.groupBy("age").count.show
// +----+-----+
// | age|count|
// +----+-----+
// |  19|    1|
// |null|    1|
// |  30|    1|
// +----+-----+

scala> df.sort(df("age").desc).show
// +----+-------+
// | age|   name|
// +----+-------+
// |  30|   Andy|
// |  19| Justin|
// |null|Michael|
// +----+-------+

scala> df.select(df("name").as("username"), df("age")+ 1).show
// +--------+---------+
// |username|(age + 1)|
// +--------+---------+
// | Michael|     null|
// |    Andy|       31|
// |  Justin|       20|
// +--------+---------+

```



# Spark VS Flink

## Spark简介

Spark的历史比较悠久，已经发展了很长时间，目前在大数据领域也有了一定的地位。Spark是Apache的一个顶级项目。它是一种快速的、轻量级、基于内存、分布式迭代计算的大数据处理框架。Spark最初由美国加州伯克利大学（UCBerkeley）的AMP（Algorithms，Machines and People）实验室与2009年开发，是基于内存计算的大数据并行计算框架，可用于构建大型的、低延迟的数据分析应用程序。2003年加入Apache孵化器项目后的到迅猛的发展，如今已成为Apache的顶级项目。

## Flink简介

Flink出来的时间比较晚，可以说是大数据流计算的新贵，但是发展速度很快，劲头不容小觑，到2016年的时候才崭露头角，Stratosphere 项目最早在 2010 年 12 月由德国柏林理工大学教授 Volker Markl 发起，主要开发人员包括 Stephan Ewen、Fabian Hueske。Stratosphere 是以 MapReduce 为超越目标的系统，同时期有加州大学伯克利 AMP 实验室的 Spark。相对于 Spark，Stratosphere 是个彻底失败的项目。其实刚开始的时候Flink也是做批处理的，但是当时，spark已经在批处理领域有所建树，所以Flink决定放弃批处理，直接在流处理方面发力。所以 Volker Markl 教授参考了谷歌的流计算最新论文 MillWheel，决定以流计算为基础，开发一个流批结合的分布式流计算引擎 Flink。Flink 于 2014 年 3 月进入 Apache 孵化器并于 2014 年 11 月毕业成为 Apache 顶级项目。

### 1、两者最重要的区别(流和微批)

(1)Micro Batching 模式(spark)

Micro-Batching 计算模式认为 `流是批的特例`， 流计算就是将连续不断的批进行持续计算，如果批足够小那么就有足够小的延时，在一定程度上满足了99%的实时计算场景。那么那1%为啥做不到呢？这就是架构的魅力，在Micro-Batching模式的架构实现上就有一个自然流数据流入系统进行攒批的过程，这在一定程度上就增加了延时。

把输入的数据，分成微小的批次，然后一个批次一个批次的处理，然后也是一片批次的输出。很显然Micro-Batching模式有其天生的低延时瓶颈，但任何事物的存在都有两面性，在大数据计算的发展历史上，最初Hadoop上的MapReduce就是优秀的批模式计算框架，Micro-Batching在设计和实现上可以借鉴很多成熟实践。

(2)Native Streaming 模式(flink)

Native Streaming 计算模式认为 `批是流的特例`，这个认知更贴切流的概念，比如一些监控类的消息流，数据库操作的binlog，实时的支付交易信息等等自然流数据都是一条，一条的流入。Native Streaming 计算模式每条数据的到来都进行计算，这种计算模式显得更自然，并且延时性能达到更低。

输入的数据过来一条处理一条，然后输出，几乎不存在延迟，很明显Native Streaming模式占据了流计算领域 "低延时" 的核心竞争力，当然Native Streaming模式的实现框架是一个历史先河，第一个实现Native Streaming模式的流计算框架是第一个吃螃蟹的人，需要面临更多的挑战，后续章节我们会慢慢介绍。当然Native Streaming模式的框架实现上面很容易实现Micro-Batching和Batching模式的计算，Apache Flink就是Native Streaming计算模式的流批统一的计算引擎。

### 2、数据模型

Spark 最早采用 RDD 模型，达到比 MapReduce 计算快 100 倍的显著优势，对 Hadoop 生态大幅升级换代。RDD 弹性数据集是分割为固定大小的批数据，RDD 提供了丰富的底层 API 对数据集做操作。为持续降低使用门槛，Spark 社区开始开发高阶 API：DataFrame/DataSet，Spark SQL 作为统一的 API，掩盖了底层，同时针对性地做 SQL 逻辑优化和物理优化，非堆存储优化也大幅提升了性能。

Spark Streaming 里的 DStream 和 RDD 模型类似，把一个实时进来的无限数据分割为一个个小批数据集合 DStream，定时器定时通知处理系统去处理这些微批数据。劣势非常明显，API 少、难胜任复杂的流计算业务，调大吞吐量而不触发背压是个体力活。不支持乱序处理，或者说很难处理乱序的问题。Spark Streaming 仅适合简单的流处理，这里稍微解释一下，因为spark的创始人在当时认为延迟不是那么的重要，他认为现实生活中没有那么多低延迟的应用场景，所以就没太注重延迟的问题，但是随着生活多样化场景的不断增加，对实时性的要求越来越高，所以spark也注意到了这个问题，开始在延迟方面发力，进而推出了Structured Streaming，相信很快spark streaming就会被Structured Streaming替代掉。

Spark Structured Streaming 提供了微批和流式两个处理引擎。微批的 API 虽不如 Flink 丰富，窗口、消息时间、trigger、watermarker、流表 join、流流 join 这些常用的能力都具备了。时延仍然保持最小 100 毫秒。当前处在试验阶段的流式引擎，提供了 1 毫秒的时延，但不能保证 exactly-once 语义，支持 at-least-once 语义。同时，微批作业打了快照，作业改为流式模式重启作业是不兼容的。这一点不如 Flink 做的完美。当然了现在还在优化阶段。

综上，Spark Streaming 和 Structured Streaming 是用批计算的思路做流计算。其实，用流计算的思路开发批计算才是最合理的。对 Spark 来讲，大换血不大可能，只有局部优化。其实，Spark 里 core、streaming、structured streaming、graphx 四个模块，是四种实现思路，通过上层 SQL 统一显得不纯粹和谐。

Flink 的基本数据模型是数据流，及事件(Event)的序列。数据流作为数据的基本模型可能没有表或者数据块直观熟悉，但是可以证明是完全等效的。流可以是无边界的无限流，即一般意义上的流处理。也可以是有边界的有限流，这样就是批处理。

Flink 采用 Dataflow 模型，和 Lambda 模式不同。Dataflow 是纯粹的节点组成的一个图，图中的节点可以执行批计算，也可以是流计算，也可以是机器学习算法，流数据在节点之间流动，被节点上的处理函数实时 apply 处理，节点之间是用 netty 连接起来，两个 netty 之间 keepalive，网络 buffer 是自然反压的关键。经过逻辑优化和物理优化，Dataflow 的逻辑关系和运行时的物理拓扑相差不大。这是纯粹的流式设计，时延和吞吐理论上是最优的。

### 3、运行时架构

Spark 运行时架构

批计算是把 DAG 划分为不同 stage，DAG 节点之间有血缘关系，在运行期间一个 stage 的 task 任务列表执行完毕，销毁再去执行下一个 stage；Spark Streaming 则是对持续流入的数据划分一个批次，定时去执行批次的数据运算。Structured Streaming 将无限输入流保存在状态存储中，对流数据做微批或实时的计算，跟 Dataflow 模型比较像。

Flink 运行时架构

Flink 有统一的 runtime，在此之上可以是 Batch API、Stream API、ML、Graph、CEP 等，DAG 中的节点上执行上述模块的功能函数，DAG 会一步步转化成 ExecutionGraph，即物理可执行的图，最终交给调度系统。节点中的逻辑在资源池中的 task 上被 apply 执行，task 和 Spark 中的 task 类似，都对应线程池中的一个线程。

在 DAG 的执行上，Spark 和 Flink 有一个比较显著的区别。在 Flink 的流执行模式中，一个事件在一个节点处理完后的输出就可以发到下一个节点立即处理。这样执行引擎并不会引入额外的延迟。与之相应的，所有节点是需要同时运行的。而 Spark 的 micro batch 和一般的 batch 执行一样，处理完上游的 stage 得到输出之后才开始下游的 stage。

在流计算的运行时架构方面，Flink 明显更为统一且优雅一些。

### 4、时延和吞吐

至于延迟和吞吐方面，spark streaming是秒级别的，Structured Streaming是毫秒级别的，Flink是亚秒级别的，其实这个没差多少，吞吐量的话，我测试的结果是Flink是Spark的1.X倍，也相差不是太大。

### 5、反压

Flink 中，下游的算子消费流入到网络 buffer 的数据，如果下游算子处理能力不够，则阻塞网络 buffer，这样也就写不进数据，那么上游算子发现无法写入，则逐级把压力向上传递，直到数据源，这种自然反压的方式非常合理。Spark Streaming 是设置反压的吞吐量，到达阈值就开始限流，从批计算上来看是合理的。从这点看Flink的反压机制是要比spark好的。

### 6、状态存储

Spark 的快照 API 是 RDD 基础能力，定时开启快照后，会对同一时刻整个内存数据持久化。Spark 一般面向大数据集计算，内存数据较大，快照不宜太频繁，会增加集群计算量。spark的状态管理目前做的比较简单，只有两个对应的算子，具体可以看这篇文章。保存在checkpoint中的。

Flink 提供文件、内存、RocksDB 三种状态存储，可以对运行中的状态数据异步持久化。打快照的机制是给 source 节点的下一个节点发一条特殊的 savepoint 或 checkpoint 消息，这条消息在每个算子之间流动，通过协调者机制对齐多个并行度的算子中的状态数据，把状态数据异步持久化。

Flink 打快照的方式，是我见过最为优雅的一个。Flink 支持局部恢复快照，作业快照数据保存后，修改作业，DAG 变化，启动作业恢复快照，新作业中未变化的算子的状态仍旧可以恢复。而且 Flink 也支持增量快照，面对内存超大状态数据，增量无疑能降低网络和磁盘开销。我们会发现Flink的状态存储也有较多的选择.

### 7、API方面
Spark 的初衷之一就是用统一的编程模型来解决用户的各种需求，在这方面一直很下功夫。最初基于 RDD 的 API 就可以做各种类型的数据处理。后来为了简化用户开发，逐渐推出了更高层的 DataFrame(在 RDD 中加了列变成结构化数据)和 Datasets(在 DataFrame 的列上加了类型)，并在 Spark 2.0 中做了整合(DataFrame = DataSet[Row])。Spark SQL 的支持也比较早就引入了。在加上各个处理类型 API 的不断改进，比如 Structured Streaming 以及和机器学习深度学习的交互，到了今天 Spark 的 API 可以说是非常好用的，也是 Spark 最强的方面之一。

Flink 的 API 也有类似的目标和发展路线。Flink 和 Spark 的核心 API 可以说是可以基本对应的。今天 Spark API 总体上更完备一下，比如说最近一两年大力投入的和机器学习深度学习的整合方面。Flink 在流处理相关的方面还是领先一些，比如对 watermark、window、trigger 的各种支持要比spark好很多。

总结
spark和flink最大的区别还是在对流计算的支持上面，现在两者也都在做批流统一的相关工作，从spark最新的发展来看，会发展成一个和 Flink 的流处理模式比较相似的执行引擎。不过主要的功能都还在开发中或者待开发。对将来能做到什么程度，和 Spark 原来的 batch 执行引擎怎么结合，我们拭目以待。Flink也在做大量的完善工作，也逐步在ML、图计算等领域发力，使得Flink的生态系统越来越完善。