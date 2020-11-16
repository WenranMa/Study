# Big Data

## Hadoop
开源大数据框架和分布式计算系统。

两大核心：

1.HDFS分布式文件系统，存储。（Hadoop Distributed File System）

	1. 数据块: 128MB 备份x3
	2. NameNode: 主，管理命名空间，存放文件元数据，维护所有文件与数据块的映射，记录各个块所在数据节点信息。
	3. DataNode：从，存储数据块，向namenode更新数据块列表。

	有容错，恢复，支持流式写入，一次写入，多次读取。
	不适合大量小文件存储，不适合并发写入，不支持随机修改，不支持随机读等低延时访问。

	数据块大小？太小内存压力大，太大加载慢？？

	主节点挂了？Hadoop2.0支持HA，有备用节点。

HDFS写流程：

	客户端向NameNode发请求。
	分块写入DataNode，DataNode自动备份。
	DataNode通知NameNode，NameNode通知客户端。

HDFS读流程：

	客户端向NameNode发请求。
	NameNode找到最近DataNode。
	客户端从该DataNode下载文件。

2.MapReduce分布式计算
一种编程模型，分而治之。

YARN概念

	ResourceManager：

		分配调度资源
		启动和监控ApplicationMaster
		监控NodeManager

	ApplicationMaster

		为MR类型程序申请资源
		数据切分
		监控任务执行和容错

	NodeManager

		管理单个节点资源
		处理ResourceManager和ApplicationMaster的命令

	输入一个大文件，分片，每片文件交给单独的机器去处理，这就是Map方法。
	各个结果再汇总得到最终结果，这就是Reduce方法。


## Spark
	基于内存计算的大数据并行计算框架。计算的中间值存在于内存中。
	MapReduce的替代方案。
	兼容HDFS，Hive等。
	本身是Scala开发，运行与JVM上。
	Hadoop的中间计算结果会落盘，导致计算时效差，不适用与交互处理，更适合离线处理。Spark基于内存，计算时间是秒级和分钟级。

	弹性分布式数据集RDD ???
	基于事件驱动？？？

	spark shell


## Hbase
	分布式数据库，利用HDFS作为文件存储系统，支持MapReduce程序读取数据。
	支持存储非结构化和半结构化数据？？

	特点：
		海量数据存储（单表百亿行x百万列），准实时查询。	面向列，不同于关系型数据块，Hbase列可以动态增加。对列进行单独操作。
		多版本，TimeStamp。
		稀疏性，因为列是动态的，所以为空的列不占用空间。
		扩展性，高可靠，依赖HDFS。

	几个概念：
		RowKey：数据唯一标识。
		Column Family：多个列的集合。
		TimeStamp：支持多版本数据。

	每条数据有一个rowkey，一个timestamp，多个列簇，列簇包括多行数据

	列簇的概念：
		一张表的类簇尽可能不超过5个，否则容易导致性能下降。
		每个列簇的列数没有限制。
		列只有插入数据后才存在，是动态增加的。
		列在列簇中是有序的。

举例：
![hbase](./img/hbase.jpg)

	HBase架构；
	有两个进程，Master和RegionServer。
	依赖两个服务，Zookeeper和HDFS。Zookeeper在分布式构架中常用。

	HBase不需要指定具体的列，而是要指定列簇，就是列的分类。列簇中每一条数据的列可以不同。

	与关系型数据库对比：
		区别于关系型数据库，hbase列是动态增加的，关系型数据库是需要提前定好列。
		数据会自动切分，关系型数据库需要人工干预。
		自带高并发读写，关系型数据库需要引入缓存一类的插件实现。
		缺点：不支持条件查询，不能进行复杂查询


## Hive


## Presto

presto cli
```bash
presto --server kpr-s0000230f-presto-master.amazonaws.com:9106 --catalog fw --schema ax_fact --http-proxy x.x.x.x:portn
```
