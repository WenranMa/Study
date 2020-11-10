# Big Data

## Hadoop
开源大数据框架和分布式计算系统。

两大核心：

1. HDFS分布式文件系统，存储。
	
	1. 数据块: 128MB 备份x3
	2. NameNode: 主，管理命名空间，存放文件元数据，维护所有文件与数据块的映射，记录各个块所在数据节点信息。
	3. DataNode：从，存储数据块，向namenode更新数据块列表。

有容错，恢复，支持流式写入，一次写入，多次读取。
不适合大量小文件存储，不适合并发写入，不支持随机修改，不支持随机读等低延时访问。

数据块大小？
太小内存压力大，太大加载慢？？

主节点挂了？
Hadoop2.0支持HA，有备用节点。
	
HDFS写流程：
	客户端向NameNode发请求。
	分块写入DataNode，DataNode自动备份。
	DataNode通知NameNode，NameNode通知客户端。
	
HDFS读流程：
	客户端向NameNode发请求。
	NameNode找到最近DataNode。
	客户端从该DataNode下载文件。

2. MapReduce分布式计算
一种编程模型

YARN





## Spark


Hive数据仓库

Presto

presto cli
```bash
presto --server kpr-s0000230f-presto-master.amazonaws.com:9106 --catalog fw --schema ax_fact --http-proxy x.x.x.x:portn
```
