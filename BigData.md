# Big Data

2010年，国内第三次信息浪潮，大数据，物联网，云计算。
技术原因又三个：计算速度，存储，网络带宽。

大数据4V:
 - Volume
 - Velocity
 - Varity
 - Value 密度低
 
结构化数据（MySQL关系型数据），非结构化数据，大部分都是非结构化。

Jim Gray

大数据特征：全量而非抽样，效率和非精确（因为抽样，所以要精确），相关而非因果。

核心技术：分布式存储，分布式处理。

计算模式：
 - 批处理就算：MapReduce，Spark（时效性更高，内存中计算）
 - 流式计算：Storm，Flume
 - 图计算：
 - 查询分析计算，交互式查询：Hive


## Hadoop
开源大数据框架和分布式计算系统。

![Hadoop](./img/hadoop.JPG)

两大核心：
- HDFS
- MapReduce

### HDFS
HDFS分布式文件系统，存储。（Hadoop Distributed File System）

问题：
- 不适合大量小文件存储。
- 不适合并发写入。
- 不支持随机修改，只追加。
- 不支持随机读等低延时访问。

概念：
- 块，每个块都是128MB，很大，方便寻址。支持大规模数据存储，如果不分块，则一个大文件最多一个机器的容量，适合备份。
- 数据块太小内存压力大，太大加载慢。
- NameNode: 主，管理命名空间，存放文件元数据，维护所有文件与数据块的映射，也就是数据目录。同时记录各个块所在数据节点信息。
- DataNode：从，存储数据块，向namenode更新数据块列表。
- FsImage：保存系统文件树。
- EditLog：记录对数据的创建，删除等操作。
- 启动时，系统会读取FsImage以及EditLog，两者合并成最新的FsImage，并且再创建一个空的EditLog。
- SecondaryNameNode，解决EditLog不断增大的问题。会定期拉FsImage和Editlog到本地，合并后再推给NameNode。



存储原理：
- 冗余数据保存，默认数据存三份。
- 可以加快数据传输速度（并行）。
- 容易检查数据错误（副本对比）。
- 保证数据可靠，自动保证副本数量。

HDFS写流程：
- 客户端向NameNode发请求。
- 分块写入DataNode，DataNode自动备份。备份会被写到不同的机架上。
- DataNode通知NameNode，NameNode通知客户端。

HDFS读流程：
- 客户端向NameNode发请求。
- NameNode找到最近DataNode，客户端的机架ID和DataNode机架ID有API可以查询，如果在同一机架内，则最近，如果没有就随机。
- 客户端从该DataNode下载文件。

错误处理：
- 主节点NameNode挂了，2.0支持HA，有第二NameNode可以提供恢复。
- DataNode挂了，DataNode定期发送心跳数据给NameNode。NameNode有DataNode的列表，一旦DataNode无心跳，则把该机器的数据（其他机器上面有）复制一份到另一台机器上。
- 数据本身问题，生成数据块的时候会有校验码，对比校验码可以确定数据是否出错。



支持流式写入，一次写入，多次读取。



### MapReduce

一种编程模型，分而治之。输入一个大文件，分片，每片文件交给单独的机器去处理，这就是Map方法。各个结果再汇总得到最终结果，这就是Reduce方法。
	
理念：计算向数据靠拢（数据不进行或者只有很少的迁移，计算就发生在数据所在节点或者很近的节点），而不是数据向计算靠拢（机器拉取数据）。

Master/Slave结构：
- 一个Master服务器，提供JobTracker，处理整个作业的调度，失败处理，恢复等。
- 多个slave服务器，提供TaskTracker，负责JobTracker分发的作业处理指令，完成具体任务。

MapReduce方法：
- Map函数的输入是一个`<K,V>`，例如`<"row":"a,b,c">`，输出是一批，也就是`List(<K,V>)`，例如`(<"a":1>,<"b":(1,1)>,<"c":1>)`。他们是计算的中间结果。
- Reduce函数的输入`<K, List(V)>`，例如`<"a":(1,1,1)>`，输出是一个`<K,V>`，例如`<"a":3>`。

#### 结构
- client：用户通过client提交编写的程序到JobTracker端，同事可以查看状态等。
- JobTracker：资源监控，作业调度，监控TaskTracker的健康情况。
- TaskScheduler：通过JobTracker发过来的监控的信息，执行具体的资源调度。
- TaskTracker：执行具体任务，也会发送心跳信息发送给JobTracker。

TaskTracker会将本机资源（cpu，memory）分成多个slot，每个slot是一部分CPU和memory，slot还分为map类型和reduce类型。只有本机有空闲的slot，相关的task才可以被分配到本机。

Task分为map task和reduce task，一个机器可以同时运行map task和reduce task的。

#### 工作流程
- InputFormat从HDFS中加载数据。
- 把大的数据集切分成split，这里是逻辑切分并不是物理切分。
- RecordReader（RR）根据分片信息从HDFS中各个块中读取Split。
- 以KeyValue形式输入map函数，map函数包含了用户处理逻辑，map任务的数量是有分片split决定的。
- map函数输出的多组键值，进行Shuffle。
- 之后输入给reduce函数，输出键值对。
- OutputFormat对结果进行检查。

Shuffle过程：

Shuffle操作在map端和reduce端都有。
- map函数的结果并不是直接给reduce函数，而是先写入缓存。
- 缓存写入数据达到溢写比（通常0.8，100MB缓存写入80MB后，不能写满缓存再溢写，不然后续的结果没地方可写），启动溢写操作。
- 溢写会有分区，排序，合并（比如相同键的合并），合并不是必须的，是用户定义的。
- 每次溢写生成一个磁盘文件，多个磁盘文件会归并成一个或多个大文件。
- reduce任务会从多个map结果中把属于自己分区的任务拉到本地，并执行归并操作。

MapReduce实现自然连接操作，把两个表公共的column，比如ID当成key，其他列和表名当做value。key相同的会被连接。

MapReduce依赖磁盘读写，Map存在衔接开销，Reduce方法必须等所有的Map方法完成之后才能开始。



## Hadoop2.0 & YARNHadoop 2.0

HDFS1.0版本局限性：
- NameNode文件目录存在内存中，所以可以容纳对象有限。
- 整个系统的吞吐量，都受限于单个NameNode。
- 隔离问题。一个单点，APP无法隔离。
- 单点故障。

Hadoop2.0 HDFS的改进：

HDFS支持HA（High Availability）。
- 两个NameNode，一个active，一个standby。通过zookeeper保证只有一个活跃NameNode。
- 两个NameNode通过共享存储系统同步editlog。
- 映射表的信息则是通过DataNode同时向两个NameNode汇报。

HDFS Federation，管理多个命名空间。
- 包含多个NameNode，相互独立，每个NameNode有自己的namespace。
- 共享底层的DataNode。
- 解决集群扩展性问题。
- 性能高（吞吐率高）。
- 隔离性好。

HDFS Federation + HA共同解决单点故障和性能，隔离及扩展问题。

MapReduce1.0版本局限性：
- 单点故障。
- 一个JobTracker任务过重。
- 容易出现内存溢出，只看任务数，不看具体任务消耗资源。
- 资源划分不合理，map slot和reduce slot不通用。
- 既要做计算，又要做资源管理。

Hadoop2.0 MapReduce的改进：

在Apache Hadoop 2.x中，MapReduce(MRv1)分解为YARN，一种通用的分布式应用程序管理框架，而Apache Hadoop MapReduce（又称MRv2）仍然是一个纯粹的分布式计算框架。MRv2是在运行于资源管理框架YARN之上的计算框架MapReduce。

YARN的全称是Yet Another Resource Negotiator，另一种资源调度者。从Apache Hadoop 2.0开始，Hadoop包含YARN。可为各类应用程序进行资源管理和调度。YARN不仅限于MapReduce一种框架使用，也可以供其他框架使用，比如Hive、Spark、Storm等。由于YARN的通用性，下一代MapReduce的核心已经从简单的支持单一应用的计算框架MapReduce转移到通用的资源管理系统YARN。

### YARN架构
YARN的架构还是经典的主从（master/slave）结构，YARN服务由一个ResourceManager（RM）和多个NodeManager（NM）构成，ResourceManager为主节点（master），NodeManager为从节点（slave）。

![YARN](./img/yarn_architecture.gif)

YARN主要由ResourceManager、NodeManager、ApplicationMaster和Container等几个组件构成。

（1）ResourceManager（RM）是一个全局的资源管理器，负责整个系统的资源管理和分配。RM有两个主要组件：调度器(Scheduler)和应用程序管理器(Applications Manager)。
- Scheduler接收来自ApplicationMaster的资源请求，把系统中的资源以Container的形式向各种运行的应用程序分配。YARN提供了多种直接可用的调度器，比如FairScheduler和Capacity Scheduler等，并允许用户重新设计调度器。
- ApplicationsManager负责接受作业提交，启动应用程序特定的ApplicationMaster。监控ApplicationMaster的运行，在失败时重新启动ApplicationMaster。监控NodeManager。

（2）ApplicationMaster（AM）
ApplicationMaster负责一个应用程序生命周期内的所有工作。每一个应用程序都有一个ApplicationMaster，它可以运行在ResourceManager 以外的机器上。AM主要功能包括:
- 与RM调度器协商以获取资源（用Container表示）。
- 分配给内部的任务（map任务，reduce任务）。二次分配。
- 与NM通信以启动/停止任务。
- 监控所有任务运行状态，并在任务运行失败时重新为任务申请资源以重启任务。
- 向RM发送应用程序心跳。
- 程序完成后，向RM注销Container。

（3）NodeManager (NM)
是每个节点上的资源和任务管理器，Container的生命周期管理。它会定时地向RM汇报本节点上的资源使用情况和各个Container的运行状态，同时它接收并处理来自AM的Container启动/停止等各种请求。

（4）Container
Container是YARN中的资源抽象，它封装了某个节点上的资源，如内存、CPU等。YARN会为每个任务分配一个 Container，且该任务只能使用该Container中描述的资源。Container不同于MRv1中的slot，它是一个动态资源划分单位，是根据应用程序的需求动态生成的。目前YARN仅支持CPU和内存两种资源，且使用了轻量级资源隔离机制Cgroups进行资源隔离。

1.0时代的JobTracker负责资源管理，任务调度，任务监控。现在资源管理由ResourceManager负责，任务调度和监控由ApplicationMaster负责。每个程序都有自己的ApplicationMaster，这就实现了监控的分布化，减轻了NameNode节点的压力。

### YARN工作流程
当用户向YARN中提交一个应用程序后，YARN将分两个阶段运行该应用程序：第一个阶段是启动ApplicationMaster，第二个阶段是由ApplicationMaster创建应用程序，为它申请资源并监控它的整个运行过程直到运行完成。

1. 客户端程序向ResourceManager提交应用并请求一个ApplicationMaster实例。
2. ResourceManager进程和NodeManager进程通信，根据集群资源，为用户程序分配第一个容器，ResourceManager找到可以运行一个Container的NodeManager，并在这个Container中启动ApplicationMaster实例。
3. ApplicationMaster向ResourceManager进行注册，注册之后客户端就可以查询ResourceManager获得ApplicationMaster的详细信息，以后就可以和ApplicationMaster直接交互了。
4. ApplicationMaster根据resource-request协议向ResourceManager发送resource-request请求，为自己的应用程序申请容器资源。
5. 当Container被成功分配之后，ApplicationMaster通过向NodeManager发送container-launch-specification信息来启动Container，container-launch-specification信息包含了能够让Container和ApplicationMaster交流所需要的资料。
6. 应用程序的代码在启动的Container中运行，并把运行的进度、状态等信息通过application-specific协议发送给ApplicationMaster。
7. 在应用程序运行期间，提交应用的客户端主动和ApplicationMaster交流获得应用的运行状态、进度更新等信息，交流的协议也是application-specific协议。
8. 一但应用程序执行完成并且所有相关工作也已经完成，ApplicationMaster向ResourceManager取消注册然后关闭，用到所有的Container也归还给系统

### YARN的资源管理
资源调度和隔离是YARN最重要且最基础的两个功能。资源调度由resourcemanager完成，而资源隔离由各个nodemanager实现。

内存资源多少决定任务的生死，如果内存不够，任务可能运行失败；相比之下，cpu资源则不同，它只会决定任务的快慢，不会对任务的生死产生影响。

Yarn的内存管理：
yarn允许用户配置每个节点上可用的物理内存资源，比如一部分给了yarn，一部分给了hdfs，一部分给了hbase等，yarn配置的只是自己可用的，配置参数如下：

yarn.nodemanager.resource.memory-mb

表示该节点上yarn可以使用的物理内存总量，默认是8192m，注意，如果你的节点内存资源不够8g，则需要调减这个值，yarn不会智能的探测节点物理内存总量。

yarn.nodemanager.vmem-pmem-ratio

任务使用1m物理内存最多可以使用虚拟内存量，默认是2.1

yarn.nodemanager.pmem-check-enabled

是否启用一个线程检查每个任务证使用的物理内存量，如果任务超出了分配值，则直接将其kill，默认是true。

yarn.nodemanager.vmem-check-enabled

是否启用一个线程检查每个任务证使用的虚拟内存量，如果任务超出了分配值，则直接将其kill，默认是true。

yarn.scheduler.minimum-allocation-mb

单个任务可以使用最小物理内存量，默认1024m，如果一个任务申请物理内存量少于该值，则该对应值改为这个数。

yarn.scheduler.maximum-allocation-mb

单个任务可以申请的最多的内存量，默认8192m

Yarn cpu管理：
目前cpu被划分为虚拟cpu，这里的虚拟cpu是yarn自己引入的概念，初衷是考虑到不同节点cpu性能可能不同，每个cpu具有计算能力也是不一样的，比如，某个物理cpu计算能力可能是另外一个物理cpu的2倍，这时可以通过为第一个物理cpu多配置几个虚拟cpu弥补这种差异。用户提交作业时，可以指定每个任务需要的虚拟cpu个数。在yarn中，cpu相关配置参数如下：

yarn.nodemanager.resource.cpu-vcores

表示该节点上yarn可使用的虚拟cpu个数，默认是8个，注意，目前推荐将该值为与物理cpu核数相同。如果你的节点cpu合数不够8个，则需要调减小这个值，而yarn不会智能的探测节点物理cpu总数。

yarn.scheduler.minimum-allocation-vcores

单个任务可申请最小cpu个数，默认1，如果一个任务申请的cpu个数少于该数，则该对应值被修改为这个数

yarn.scheduler.maximum-allocation-vcores

单个任务可以申请最多虚拟cpu个数，默认是32.


### Hadoop生态
#### Pig
- 简单的Pig Latin语句就能实现复杂的数据分析任务。
- Pig Latin语句自动转换成MapReduce任务。
- 减少编码量。

Pig做数据加工 -> Hive做数据仓库

#### Tez
支持DAG作业的计算框架。把map和reduce操作拆分成更细粒度的操作，然后生成有向无环图。并且可以去掉图中多余步骤，优化性能。

- Hive，Pig，MapReduce运行于Tez之上，优化性能。
- Tez在Yarn之上。
- Yarn在HDFS之上。

---


## Hbase
Google Big Table的开源实现，Big Table是架构在GFS（Google File System）之上的。

分布式数据库，利用HDFS作为文件存储系统，支持MapReduce程序读取数据。

支持存储非结构化和半结构化数据。

为什么出现HBase：
- MapReduce + HDFS 有延时，无法满足实时处理需求。
- 关系型数据库扩展性差，不能应对数据结构变化。

特点：
- 海量数据存储（单表百亿行x百万列），准实时查询。	
- 面向列，不同于关系型数据块，Hbase列可以动态增加。对列进行单独操作。
- 多版本，TimeStamp。
- 稀疏性，因为列是动态的，所以为空的列不占用空间。
- 扩展性，高可靠，依赖HDFS。

与传统关系型数据库区别：
- 区别于关系型数据库，hbase列是动态增加的，关系型数据库是需要提前定好列。
- 数据会自动切分，关系型数据库需要人工干预。
- 数据类型，传统数据库多，HBase就是未经解读的字符串。
- 数据操作，比传统的少，没有连接操作，因为不需要，都在一张表里。
- 存储模式，传统基于行，HBase基于列存储。
- 索引，传统支持多级索引，HBase行键索引。
- 数据维护，更新，传统覆盖，HBase版本控制。
- 可伸缩性，更好。
- 自带高并发读写，关系型数据库需要引入缓存一类的插件实现。
- 缺点：不支持条件查询，不能进行复杂查询

访问接口：
- Java API
- Shell
- Rest Gateway
- Thrift Gateway ?
- SQL类型接口
- Hive，HiveSQL

#### Data Model
有四个概念：
- 行键，RowKey数据唯一标识。
- 列族，Column Family多个列的集合。
- 列限定符
- 时间戳，TimeStamp，支持多版本数据。

每条数据有一个rowkey，一个timestamp，多个列簇，列簇包括多行数据。HBase不需要指定具体的列，而是要指定列簇，就是列的分类。列簇中每一条数据的列可以不同。

列簇的概念：
- 一张表的类簇尽可能不超过5个，否则容易导致性能下降。
- 每个列簇的列数没有限制。
- 列只有插入数据后才存在，是动态增加的。
- 列在列簇中是有序的。

举例：
![hbase](./img/hbase.jpg)

HBASE可以支持数十亿行，百万列，一个列族可以有多个列，列又叫列限定符。有单元格的概念，可以通过行键，时间戳，列族，列限定符确定一个单元格，即四维定位，HBASE的读写都是按单元格来的。

如果吧四个维度当成一个Key，HBase也可以理解为键值数据库。

列族可以动态扩展，增加或减少。

时间戳是因为HDFS只允许一次写入，多次读取，所以单元格不能被改写，只能生成新的版本，为了获取新版本，需要时间戳。

时间戳是自动生成的，取数据也是取最新版本。


概念视图，稀疏表，表示并不是每个单元格都有值。

物理视图，但在底层存储上，是以列族为单位进行存储。

分区是先按照行切，再按照列族切。

数据分析大多是基于某个或某些维度，即列来做分析。所以列式存储比行式存储做分析更快。另外列式存储，每个列类型都是一样的，所以方便压缩，压缩率高。

#### Region寻址

HBase架构；
- 有两个进程，Master和RegionServer。
- 依赖两个服务，Zookeeper和HDFS。Zookeeper在分布式构架中常用。

客户端可以直接和region服务器通信。

一个HBase表会被划分成多个region，一个region也可以被分裂成多个region。region实际大小取决于单台服务器的有效处理能力。每个region服务器可以存10到1000个region。同一个region不会被拆分到不同的region服务器。

三层结构实现region寻址。

- META表，有两列：region id， region server ID。是一个映射关系，但随着region的分裂，META表也需要分region去存。
- 所以又有ROOT表去存放META表与Region服务器的映射。Root表不能分裂，只能存在一个Region服务器。
- ROOT表地址写死在Zookeeper中。


#### 数据读写

- 客户端。
- Zookeeper，保证只有一个master在运行。
- Master，负责表和RegionServer的管理，负载均衡，Region分裂合并。
- RegionServer。

一个RegionServer会有存有多个Region，每个Region会存储一个表的若干列族，一个列族叫一个Store，Store的数据写入Storefile，Storefile对应的就是HDFS中的HFile中。

- 写入数据：先写缓存MemStore，同时写日志HLog。
- 读数据：也是先读MemStore，读不到再去RegionServer。
- 缓存刷新：系统周期性的把MemStore内容刷写到StoreFile，并在HLog中标记。
- 每个Store可以有多个StoreFile。
- 一个RegionServer会维护一个公共的HLog。

StoreFile合并，磁盘刷写的StoreFile过多达到阈值，会发生合并，合并会消耗资源。系统最初只有一个Region，多个StoreFile，多个StoreFile合并后超过一个RegionServer的处理能力，又会分裂成多个StoreFile到多个Region。

HLog，用于数据恢复，如果RegionServer故障，Master会拉取这个RegionServer的HLog，对其中的每个Region的操作记录拆分，再恢复。

- HColumnDescriptor.setInMemory：列放入缓存，提高读写性能。
- HColumnDescriptor.setMaxVersions：最大版本数，如果是1，则只存最新版本。
- TimeToLive：过期自动删除。

现在也可以通过SQL访问HBase，方便使用，减少编码。比如用Hive。


HBase二级索引?

---

## NoSQL
反SQL运动的演变到Not Only SQL。

现在的关系型数据库如MySQL常常采用主从结构，master和slave，master用于写负载，slave用于读负载。数据写入master后同步到slave。实现读写分离。数据量进一步扩大后，则采用分库，分表的方式，不同的库放在不同的物理机，实现负载分流。

- 复杂，集群管理复杂。
- 主库压力大时，会有延时。
- 扩容重新重新分库分表太难。
- 单一数据模型也有局限性。

所以无法解决数据扩张的问题。

关系型数据库的事务性和高效查询，反而成了web2.0时代的累赘。

- web2.0不都是严格事务。
- 没有实时要求。
- 不包含复杂SQL。

所以就出现了NoSQL，可以支持对大规模数据的存储，灵活的数据模型。

#### NoSQL数据库类型

- 键值数据库：Redis，DynamoDB。键是字符串，值可以是任意类型，数组，列表，结合等。应用于涉及频繁读写，简单数据模型的应用。大量写操作时性能好。但无法存储结构型数据，条件查询效率低。无法通过值查询。是理想的缓冲层解决方案，把经常访问的数据放入缓冲层，提高访问性能。DDB Sinker
- 列族数据库：如HBase，数据模型就是列族。用于分布式数据存储，适用于拥有动态字段的应用。查找速度快。
- 文档数据库：可看做键值数据库，不过形式是文档。例如：MongoDB。可以对数据内容和类型做自我描述。Json数据格式是典型的文档数据库，文档数据库可以完整的包含在一个文档里，并发性好，数据更新只要锁定一个文档。灵活性高，支持嵌套。但缺乏统一查询语法，并且文档间不支持事务。
- 图形数据库：Neo4j，用图的节点和边来存储信息，适用于高度相关联的数据，比如社交网络，推荐，依赖分析。

#### NoSQL理论

CAP：

- Consistency，一致性，任何一次读操作，总能读到之前一次写的结果。
- Availability，可用性，快速获取数据，确定时间内返回结果。
- Partition tolerance，一部分节点无法通信，系统也可以正常运行。

分布式系统不可能同时满足以上三点，只能三取二：

- CA：MySQL。
- AP：DynamoDB。
- CP：HBase，MongoDB。

BASE：（中文翻译碱，对应事务性ACID的酸）

- Basically Available：基本可以用，即满足P。
- Soft state：硬状态，一直保持数据一致。软状态，可以有一段时间不一致，滞后性。
- Eventual consistency：强一致性，弱一致性，区别是高并发时，能否获取最新数据。最终一致性是弱一致性的一个特例，可以有时间不一致，但最终一致。

最终一致性：

- 因果一致性：进程A通知进程B已更新数据，则B可以获取A写入的结果。
- “读己之所写”一致性：进程A写入一个数据，它自己总是可以获取新的值。
- 单调读一致性：如果进程看到过对象的某个值，那个该进程不会得到这个值之前的旧值。
- 会话一致性：进程在会话的上下文中，会话存在就能保证一致性。
- 单调写一致性：同一进程的写操作要保证顺序执行。

一致性理论：

- N：数据冗余份数。
- W：更新数据所需节点数。
- R：读取数据所需节点数。
- W+R>N：强一致性，如W=2，N=2，R=1。
- W+R<=N：弱一致性。

HBase采用底层HDFS实现数据冗余。HDFS采用强一致性，在数据没有同步到N个节点之前，写操作W不会成功返回，所以W=N，而读只要读到一个节点即可，R=1。

NewSQL：同时具有OldSQL和NoSQL的特点，事务性，强一致性，可扩展，SQL查询。比如RDS。

#### MongoDB
文档数据库，数据存储为一个文档，数据由键值对组成，类似Json，是二进制格式的，叫BSon。

与传统数据库对比：

| 传统数据库 | MongoDB    |
|----------|------------|
| database | database   |
| table    | collection |
| row      | document   |
| column   | field      |

每一行都是一个单独的文档。一个文档记录所有内容，所以不需要跨表连接操作。

比如下面的例子：
```json
{
	"id":1,
	"author": "wrma",
	"blogs": {
		"title": "First",
		"comment": {
			"by": "xyhu",
			"text": "good post!"
		}
	}
}
```
普通数据库，需要author，blogs，comment三张表，而MongoDB只要一个文档。

一个collection可以有多个文档，而且文档的数据格式可以完全不同。



## Cloud DB
UMP，阿里Unified MySQL Platform。


AWS云服务：

- 全球分为12个Region，每个Region又分多个Available Zone，AZ。
- 网络：Route 53，云域名解析系统。
- 计算：EC2，ELB。
- 存储：S3。EBS，针对EC2设计，给EC2挂一个EBS。Glacier，存储较少使用的数据。
- DB：NoSQL，KV型SimpleDB，DynamoDB。关系型RDS。ElastiCache。
- App Service。
- 部署。

EBS的服务对象是系统管理员，不对用户开放。S3服务员管理员和最终用户。

RDS关系型数据库：支持MySQL，Oracle，SQLServer，PostgreSQL，MariaDB，AWS的关系型数据库Aurora。


---

## Hive
	
数据仓库，将多个数据源的数据经过ETL之后，按照一定主题集成起来提供决策支持和联机分析应用的数据环境。

ETL = Extract, Transform, Load.

Hive就是基于Hadoop的数仓工具，提供类SQL支持。它以MapReduce作计算引擎，HDFS作为存储系统。

Hive不负责存储，数据实体不在Hive，Hive的库和表是对HDFS上数据的映射。这些映射叫Hive的元数据（metadata），存在外部关系型数据块上，即Hive metastore

Hive语句的执行：将HQL转换成MapReduce任务。MR要频繁进行IO读写，所以Hive的查询速度不快，所以与Presto查询引擎结合。



hive server2?  类似presto

HMS api? atomic 代替 hive server2 (jdbc)

metadata 结构
 database
  tables
   partitions
   	buckets

fileformat and serdes??


OLTP and OLAP ？？


#### Hive存储格式
	
	TextFile
	Sequence File
	OrcFile
	
	列式存储


---

## Presto
	
	分布式SQL查询引擎，支持标准SQL，高速实时，低延时，高并发，属于内存计算引擎。解决Hive MapReduce模型太慢的问题。是一个计算引擎，并不存储数据，通过丰富的connector获取第三方服务的数据，比如连接Hive metastore service，Hbase，Kafka，MongoDB。

#### 概念：	
```sql
select *
from 
	hive.testdb.table_a a 
	join mysql.testdb.table_b b on a.id = b.id
where
	a.name = "xxx"
```
	Catalog：数据源，上面的hive，mysql都是数据源。Presto支持多个数据源和跨数据源查询。
	Schema：类比于Database，一个Catalog可以有多个Schema。
	Table：数据表，与常规数据库的表一个概念，一个上Schema可以有多个table。


#### presto cli
```bash
presto --server kpr-s0000230f-presto-master.amazonaws.com:9106 --catalog fw --schema ax_fact --http-proxy x.x.x.x:portn
```
	可以用`show tables`命令查看所有schema下的table。
	
#### 架构
	Master-Slave架构：
	一个Coordinator节点，负责解析SQL语句，生成查询计划，分发执行任务。
	一个Discovery Server节点，负责维护Coordinator和Worker的关系，通常内嵌于Coordinator节点。
	多个Worker节点，负责查询任务，与HDFS进行交互读取数据。每个worker可以有多个connector对应不同的数据源来支持跨数据源查询，结果在内存中汇总。

![presto](./img/presto.PNG)
![presto](./img/presto_1.PNG)

#### MPP
	数据块架构：
	Shared Everything：完全透明，共享CPU，Memory，IO，并行处理能力差，比如SQL Server。
	Shared Storage：各个处理单元有私有的CPU和内存，共享磁盘。
	Shared Nothing：有私有的CPU，内存和磁盘，典型代表Hadoop。
	
	Shared　Nothing就是属于MPP架构（Massive Parallel Processing）。容易扩展，并行能力强。无IO冲突，无资源竞争。
	短板效应，单个节点会影像整个查询。所以一般每个worker都是一样的配置。







大数据本身是个很宽泛的概念，Hadoop生态圈(或者泛生态圈)基本上都是为了处理超过单机尺度的数据处理而诞生的。你可以把它比作一个厨房所以需要的各种工具。锅碗瓢盆，各有各的用处，互相之间又有重合。你可以用汤锅直接当碗吃饭喝汤，你可以用小刀或者刨子去皮。但是每个工具有自己的特性，虽然奇怪的组合也能工作，但是未必是最佳选择。

大数据，首先你要能存的下大数据

传统的文件系统是单机的，不能横跨不同的机器。HDFS(Hadoop Distributed FileSystem)的设计本质上是为了大量的数据能横跨成百上千台机器，但是你看到的是一个文件系统而不是很多文件系统。比如你说我要获取/hdfs/tmp/file1的数据，你引用的是一个文件路径，但是实际的数据存放在很多不同的机器上。你作为用户，不需要知道这些，就好比在单机上你不关心文件分散在什么磁道什么扇区一样。HDFS为你管理这些数据。

存的下数据之后，你就开始考虑怎么处理数据。虽然HDFS可以为你整体管理不同机器上的数据，但是这些数据太大了。一台机器读取成T上P的数据(很大的数据哦，比如整个东京热有史以来所有高清电影的大小甚至更大)，一台机器慢慢跑也许需要好几天甚至好几周。对于很多公司来说，单机处理是不可忍受的，比如微博要更新24小时热博，它必须在24小时之内跑完这些处理。那么我如果要用很多台机器处理，我就面临了如何分配工作，如果一台机器挂了如何重新启动相应的任务，机器之间如何互相通信交换数据以完成复杂的计算等等。这就是MapReduce / Tez / Spark的功能。MapReduce是第一代计算引擎，Tez和Spark是第二代。MapReduce的设计，采用了很简化的计算模型，只有Map和Reduce两个计算过程(中间用Shuffle串联)，用这个模型，已经可以处理大数据领域很大一部分问题了。

那什么是Map，什么是Reduce?

考虑如果你要统计一个巨大的文本文件存储在类似HDFS上，你想要知道这个文本里各个词的出现频率。你启动了一个MapReduce程序。Map阶段，几百台机器同时读取这个文件的各个部分，分别把各自读到的部分分别统计出词频，产生类似(hello, 12100次)，(world，15214次)等等这样的Pair(我这里把Map和Combine放在一起说以便简化);这几百台机器各自都产生了如上的集合，然后又有几百台机器启动Reduce处理。Reducer机器A将从Mapper机器收到所有以A开头的统计结果，机器B将收到B开头的词汇统计结果(当然实际上不会真的以字母开头做依据，而是用函数产生Hash值以避免数据串化。因为类似X开头的词肯定比其他要少得多，而你不希望数据处理各个机器的工作量相差悬殊)。然后这些Reducer将再次汇总，(hello，12100)+(hello，12311)+(hello，345881)= (hello，370292)。每个Reducer都如上处理，你就得到了整个文件的词频结果。

这看似是个很简单的模型，但很多算法都可以用这个模型描述了。

Map+Reduce的简单模型很黄很暴力，虽然好用，但是很笨重。第二代的Tez和Spark除了内存Cache之类的新feature，本质上来说，是让Map/Reduce模型更通用，让Map和Reduce之间的界限更模糊，数据交换更灵活，更少的磁盘读写，以便更方便地描述复杂算法，取得更高的吞吐量。

有了MapReduce，Tez和Spark之后，程序员发现，MapReduce的程序写起来真麻烦。他们希望简化这个过程。这就好比你有了汇编语言，虽然你几乎什么都能干了，但是你还是觉得繁琐。你希望有个更高层更抽象的语言层来描述算法和数据处理流程。于是就有了Pig和Hive。Pig是接近脚本方式去描述MapReduce，Hive则用的是SQL。它们把脚本和SQL语言翻译成MapReduce程序，丢给计算引擎去计算，而你就从繁琐的MapReduce程序中解脱出来，用更简单更直观的语言去写程序了。

有了Hive之后，人们发现SQL对比Java有巨大的优势。一个是它太容易写了。刚才词频的东西，用SQL描述就只有一两行，MapReduce写起来大约要几十上百行。而更重要的是，非计算机背景的用户终于感受到了爱：我也会写SQL!于是数据分析人员终于从乞求工程师帮忙的窘境解脱出来，工程师也从写奇怪的一次性的处理程序中解脱出来。大家都开心了。Hive逐渐成长成了大数据仓库的核心组件。甚至很多公司的流水线作业集完全是用SQL描述，因为易写易改，一看就懂，容易维护。

自从数据分析人员开始用Hive分析数据之后，它们发现，Hive在MapReduce上跑，真鸡巴慢!流水线作业集也许没啥关系，比如24小时更新的推荐，反正24小时内跑完就算了。但是数据分析，人们总是希望能跑更快一些。比如我希望看过去一个小时内多少人在充气娃娃页面驻足，分别停留了多久，对于一个巨型网站海量数据下，这个处理过程也许要花几十分钟甚至很多小时。而这个分析也许只是你万里长征的第一步，你还要看多少人浏览了跳蛋多少人看了拉赫曼尼诺夫的CD，以便跟老板汇报，我们的用户是猥琐男闷骚女更多还是文艺青年/少女更多。你无法忍受等待的折磨，只能跟帅帅的工程师蝈蝈说，快，快，再快一点!

于是Impala，Presto，Drill诞生了(当然还有无数非著名的交互SQL引擎，就不一一列举了)。三个系统的核心理念是，MapReduce引擎太慢，因为它太通用，太强壮，太保守，我们SQL需要更轻量，更激进地获取资源，更专门地对SQL做优化，而且不需要那么多容错性保证(因为系统出错了大不了重新启动任务，如果整个处理时间更短的话，比如几分钟之内)。这些系统让用户更快速地处理SQL任务，牺牲了通用性稳定性等特性。如果说MapReduce是大砍刀，砍啥都不怕，那上面三个就是剔骨刀，灵巧锋利，但是不能搞太大太硬的东西。

这些系统，说实话，一直没有达到人们期望的流行度。因为这时候又两个异类被造出来了。他们是Hive on Tez / Spark和SparkSQL。它们的设计理念是，MapReduce慢，但是如果我用新一代通用计算引擎Tez或者Spark来跑SQL，那我就能跑的更快。而且用户不需要维护两套系统。

上面的介绍，基本就是一个数据仓库的构架了。底层HDFS，上面跑MapReduce/Tez/Spark，在上面跑Hive，Pig。或者HDFS上直接跑Impala，Drill，Presto。这解决了中低速数据处理的要求。

那如果我要更高速的处理呢？

如果我是一个类似微博的公司，我希望显示不是24小时热博，我想看一个不断变化的热播榜，更新延迟在一分钟之内，上面的手段都将无法胜任。于是又一种计算模型被开发出来，这就是Streaming(流)计算。Storm是最流行的流计算平台。流计算的思路是，如果要达到更实时的更新，我何不在数据流进来的时候就处理了?比如还是词频统计的例子，我的数据流是一个一个的词，我就让他们一边流过我就一边开始统计了。流计算很牛逼，基本无延迟，但是它的短处是，不灵活，你想要统计的东西必须预先知道，毕竟数据流过就没了，你没算的东西就无法补算了。因此它是个很好的东西，但是无法替代上面数据仓库和批处理系统。

还有一个有些独立的模块是KV Store，比如Cassandra，HBase，MongoDB以及很多很多很多很多其他的(多到无法想象)。所以KV Store就是说，我有一堆键值，我能很快速滴获取与这个Key绑定的数据。比如我用身份证号，能取到你的身份数据。这个动作用MapReduce也能完成，但是很可能要扫描整个数据集。而KV Store专用来处理这个操作，所有存和取都专门为此优化了。从几个P的数据中查找一个身份证号，也许只要零点几秒。这让大数据公司的一些专门操作被大大优化了。比如我网页上有个根据订单号查找订单内容的页面，而整个网站的订单数量无法单机数据库存储，我就会考虑用KV Store来存。KV Store的理念是，基本无法处理复杂的计算，大多没法JOIN，也许没法聚合，没有强一致性保证(不同数据分布在不同机器上，你每次读取也许会读到不同的结果，也无法处理类似银行转账那样的强一致性要求的操作)。但是丫就是快。极快。

每个不同的KV Store设计都有不同取舍，有些更快，有些容量更高，有些可以支持更复杂的操作。必有一款适合你。

除此之外，还有一些更特制的系统/组件，比如Mahout是分布式机器学习库，Protobuf是数据交换的编码和库，ZooKeeper是高一致性的分布存取协同系统，等等。

有了这么多乱七八糟的工具，都在同一个集群上运转，大家需要互相尊重有序工作。所以另外一个重要组件是，调度系统。现在最流行的是Yarn。



---

## Parquet
### 简介
Apache Parquet是Hadoop生态圈中一种新型列式存储格式，它可以兼容Hadoop生态圈中大多数计算框架(Hadoop、Spark等)，被多种查询引擎支持(Hive、Impala、Drill等)。Parquet是语言无关的，而且不与任何一种数据处理框架绑定在一起，适配多种语言和组件，能够与Parquet配合的组件有：

- 查询引擎: Hive, Impala, Pig, Presto, Drill, Tajo, HAWQ, IBM Big SQL
- 计算框架: MapReduce, Spark, Cascading, Crunch, Scalding, Kite
- 数据模型: Avro, Thrift, Protocol Buffers, POJOs

那么Parquet是如何与这些组件协作的呢？这个可以通过下图来说明。数据从内存到Parquet文件或者反过来的过程主要由以下三个部分组成：

- 存储格式(storage format)，parquet-format项目定义了Parquet内部的数据类型、存储格式等。
- 对象模型转换器(object model converters)，这部分功能由parquet-mr项目来实现，主要完成外部对象模型与Parquet内部数据类型的映射。
- 对象模型(object models)，对象模型可以简单理解为内存中的数据表示，Avro, Thrift, Protocol Buffers, Hive SerDe, Pig Tuple, Spark SQL InternalRow等这些都是对象模型。Parquet也提供了一个example object model 帮助大家理解。

例如parquet-mr项目里的parquet-pig项目就是负责把内存中的Pig Tuple序列化并按列存储成Parquet格式，以及反过来把Parquet文件的数据反序列化成Pig Tuple。

这里需要注意的是Avro, Thrift, Protocol Buffers都有他们自己的存储格式，但是Parquet并没有使用他们，而是使用了自己在parquet-format项目里定义的存储格式。所以如果你的应用使用了Avro等对象模型，这些数据序列化到磁盘还是使用的parquet-mr定义的转换器把他们转换成Parquet自己的存储格式。

### 列式存储
列式存储，顾名思义就是按照列进行存储数据，把某一列的数据连续的存储，每一行中的不同列的值离散分布。列式存储技术并不新鲜，在关系数据库中都已经在使用，尤其是在针对OLAP场景下的数据存储，由于OLAP场景下的数据大部分情况下都是批量导入，基本上不需要支持单条记录的增删改操作，而查询的时候大多数都是只使用部分列进行过滤、聚合，对少数列进行计算(基本不需要select * from xx之类的查询)。

以下这张表有A、B、C三个字段：

A | B | C
--|---|--
A1| B1| C1
A2| B2| C2
A3| B3| C3

行存储：
```
|A1|B1|C1|A2|B2|C2|A3|B3|C3| |-|-|-|-|-|-|-|-|-|
```
列存储
```
|A1|A2|A3|B1|B2|B3|C1|C2|C3| |-|-|-|-|-|-|-|-|-|
```
列式存储可以大大提升这类查询的性能，较之于行是存储，列式存储能够带来这些优化：

- 查询的时候不需要扫描全部的数据，而只需要读取每次查询涉及的列，这样可以将I/O消耗降低N倍，另外可以保存每一列的统计信息(min、max、sum等)，实现部分的谓词下推。
- 由于每一列的成员都是同构的，可以针对不同的数据类型使用更高效的数据压缩算法，进一步减小I/O。
- 由于每一列的成员的同构性，可以使用更加适合CPU pipeline的编码方式，减小CPU的缓存失效。

### 数据模型
理解Parquet首先要理解这个列存储格式的数据模型。我们以一个下面这样的schema和数据为例来说明这个问题。
```
message AddressBook {
 required string owner;
 repeated string ownerPhoneNumbers;
 repeated group contacts {
   required string name;
   optional string phoneNumber;
 }
}
```
这个schema中每条记录表示一个人的AddressBook。有且只有一个owner，owner可以有0个或者多个ownerPhoneNumbers，owner可以有0个或者多个contacts。每个contact有且只有一个name，这个contact的phoneNumber可有可无。

每个schema的结构是这样的：根叫做message，message包含多个fields。每个field包含三个属性：repetition, type, name。repetition可以是以下三种：required（出现1次），optional（出现0次或者1次），repeated（出现0次或者多次）。type可以是一个group或者一个primitive类型。

Parquet格式的数据类型不需要复杂的Map, List, Set等，而是使用repeated fields 和 groups来表示。例如List和Set可以被表示成一个repeated field，Map可以表示成一个包含有key-value对的repeated group ，而且key是required的。

List(或Set)可以用repeated field来表示：

Schema: List of Strings
```
message ExampleList {
 repeated string list;
}
```
Data: ["a", "b", "c"]
```
{
    list: "a",
    list: "b",
    list: "c",
}
```

Map可以用包含key-value对且key是required的repeated group来表示：

Schema: Map of Strings to Strings
```
message ExampleMap {
 repeated group map {
   required string key;
   optional string value;
 }
}
```
Data: {"AL" -> "Alabama", "TX" -> "Texas", ...}
```
{
    map: {
        key: "AL",
        value: "Alabama"
    },
    map: {
        key: "TX",
        value: "Texas"
    },
    ...
}
```

### 列存储格式
列存储通过将相同基本类型（primitive type）的值存储在一起来提供高效的编码和解码。为了用列存储来存储如上嵌套的数据结构，我们需要将该schema用某种方式映射到一系列的列使我们能够将记录写到列中并且能读取成原来的嵌套的数据结构。
在Parquet格式的存储中，一个schema的树结构有几个叶子节点（叶子节点都是primitive type），实际的存储中就会有多少column。
上面的schema的树结构如图所示：

![parquet schema](./img/parquet_tree.jpeg)

上面这个schema的数据存储实际上有四个column：
```
| ------------------------------------------- |
|            AddressBook                      |
| ----- | ----------------- | --------------- |
| owner | ownerPhoneNumbers |     contacts    |
|       |                   | --------------- |
|       |                   | name | phoneNum |
| ----- | ----------------- | ---- | -------- |
| "a"   | "310-562-9582"    | ...  | ...      |
| ...   | ...               | ...  | ...      |
| ----- | ----------------- | ---- | -------- |
```

只有字段值不能清楚地表达记录的结构。给出一个repeated field的两个值，我们不知道此值是按什么‘深度’被重复的（比如，这些值是来自两个不同的记录，还是相同的记录中两个重复的值）。同样的，给出一个缺失的可选字段，我们不知道整个路径有多少字段被显示定义了。因此我们将介绍repetition level和definition level的概念。

### Definition levels
Definition level指明该列的路径上多少个可选field被定义了。嵌套数据类型的特点是有些field（optional field和repeated field）可以是空的，也就是没有定义。如果一个field是定义的，那么它的所有的父节点都是被定义的。从根节点开始遍历，当某一个field的路径上的节点开始是空的时候我们记录下当前的深度作为这个field的Definition level。如果一个field的definition level等于这个field的最大Definition level就说明这个field是有数据的。对于required类型的field必须是有定义的，所以这个Definition level是不需要的。在关系型数据中，optional类型的field被编码成0表示空和1表示非空（或者反之）。

注：definition level是该路径上有定义的repeated field和optional field的个数，不包括required field，因为required field是必须有定义的。

简单的例子：
```
message ExampleDefinitionLevel {
    optional group a {
        optional group b {
            optional string c;
        }
    }
}
```
![definition level](./img/parquet_definition_level_01.png)

![definition level](./img/parquet_definition_level_02.png)

再一个例子：
```
message ExampleDefinitionLevel {
    optional group a {
        required group b {
            optional string c;
        }
    }
}
```

![definition level](./img/parquet_definition_level_03.png)

因为b是required field，所以第3行c的definition level为1而不是2（因为b是required field，所有不需计算在内）；第4行c的definition level为2而不是3。

### Repetition levels
重复深度这个概念的作用，是能用一个数字告诉我们在路径中的什么重复字段，此值重复了，以此来确定此值的位置（注意，这里的重复，特指在某个repeated类型的字段下“重复”出现的“重复”）。我们用深度0表示一个纪录的开头（虚拟的根节点），深度的计算忽略非重复字段（标签不是repeated的字段都不算在深度里）。

比如：

![repetition level](./img/parquet_repetition_level_01.png)

The column will contain the following repetition levels and values:
![repetition level](./img/parquet_repetition_level_02.png)

a,b,c 是一个 level2 List， d,e,f,g 是一个level2 List，h 是一个level2List，i,j 是一个level2 List。a,b,c,d,e,f,g 所在的两个 level2 list是同一个 level1 List 里的，h,i,j 所在的两个 level2 List 是同一个 level1List里的。那么repetition level标示着新List出现的层级：

- 0 表示整条记录的开始，此时应该创建新的level1 List和level2 List
- 1 表示level1 List 的开始，此时应该创建一个level2 List
- 2 表示level2 List中新的值产生，此时不新建List，只在List里插入新值.

下图可以看出，换句话说就是repetition level告诉我们，在从列式表达，还原嵌套结构的时候，是在哪一级插入新值的.

![repetition level](./img/parquet_repetition_level_03.png)

repetiton = 0，标志着一整条新 record 的开始. 在扁平化结构里，没有repetition 所以 repetition level 总是 0. Only levels that arerepeated need a Repetitionlevel:optional 和 required 永远也不会重复，在计算 repetition level的时候，可将其跳过.

### Striping and assembly
下面用AddressBook的例子来说明Striping和assembly的过程。对于每个column的最大的Repetion Level和 Definition Level下图所示。

![Striping](./img/parquet_s_01.png)

下面这样两条record：
```
AddressBook {
 owner: "Julien Le Dem",
 ownerPhoneNumbers: "555 123 4567",
 ownerPhoneNumbers: "555 666 1337",
 contacts: {
   name: "Dmitriy Ryaboy",
   phoneNumber: "555 987 6543",
 },
 contacts: {
   name: "Chris Aniszczyk"
 }
}
AddressBook {
 owner: "A. Nonymous"
}
```

以contacts.phoneNumber这一列为例，"555 987 6543"这个contacts.phoneNumber的Definition Level是最大Definition Level=2。而如果一个contact没有phoneNumber，那么它的Definition Level就是1。如果连contact都没有，那么它的Definition Level就是0。下面我们拿掉其他三个column只看contacts.phoneNumber这个column，把上面的两条record简化成下面的样子：

```
AddressBook {
 contacts: {
   phoneNumber: "555 987 6543"
 }
 contacts: {
 }
}
AddressBook {
}
```

这两条记录的序列化过程如下图所示：

![Striping](./img/parquet_s_02.png)

如果我们要把这个column写到磁盘上，磁盘上会写入这样的数据：

- contacts.phoneNumber: “555 987 6543”
    - new record: R = 0
    - value is defined: D = maximum (2)

- contacts.phoneNumber: null
    - repeated contacts: R = 1
    - only defined up to contacts: D = 1

- contacts: null
    - new record: R = 0
    - only defined up to AddressBook: D = 0

注意：NULL实际上不会被存储，如果一个column value的Definition Level小于该column最大Definition Level的话，那么就表示这是一个空值。

![Striping](./img/parquet_s_03.png)

下面是从磁盘上读取数据并反序列化成AddressBook对象的过程：

- R=0, D=2, Value=”555 987 6543”
    - R=0 表示是一个新的record，要根据schema创建一个新的nested record直到Definition Level=2。
    - D=2 说明Definition Level=Max Definition Level，那么这个Value就是contacts.phoneNumber这一列的值，赋值操作contacts.phoneNumber=”555 987 6543”。

- R=1, D=1
    - R=1 表示不是一个新的record，是上一个record中一个新的contacts。
    - D=1 表示contacts定义了，但是contacts的下一个级别也就是phoneNumber没有被定义，所以创建一个空的contacts。

- R=0, D=0
    - R=0 表示一个新的record，根据schema创建一个新的nested record直到Definition Level=0，也就是创建一个AddressBook根节点。
    - D=0 都没有定义，所以是个空的Addressbook。

可以看出在Parquet列式存储中，对于一个schema的所有叶子节点会被当成column存储，而且叶子节点一定是primitive类型的数据。对于这样一个primitive类型的数据会衍生出三个sub columns (R, D, Value)，也就是从逻辑上看除了数据本身以外会存储大量的Definition Level和Repetition Level。那么这些Definition Level和Repetition Level是否会带来额外的存储开销呢？实际上这部分额外的存储开销是可以忽略的。因为对于一个schema来说level都是有上限的，而且非repeated类型的field不需要Repetition Level，required类型的field不需要Definition Level，也可以缩短这个上限。

### 文件格式
#### Row Group
按照行将数据物理上划分为多个单元，每一个行组包含一定的行数。一个行组包含这个行组对应的区间内的所有列的列块。

官方建议：

更大的行组意味着更大的列块，使得能够做更大的序列IO。建议设置更大的行组（512MB-1GB）。因为一次可能需要读取整个行组，所以想让一个行组刚好在一个HDFS块中。因此，HDFS块的大小也需要被设得更大。一个最优的读设置是：1GB的行组，1GB的HDFS块，1个HDFS块放一个HDFS文件。

#### Column Chunk
在一个行组中每一列保存在一个列块中，行组中的所有列连续的存储在这个行组文件中。不同的列块可能使用不同的算法进行压缩。一个列块由多个页组成。

#### Page
每一个列块划分为多个页，页是压缩和编码的单元，对数据模型来说页是透明的。在同一个列块的不同页可能使用不同的编码方式。官方建议一个页为8KB。

![parquet_format](./img/parquet_format_01.gif)

![parquet_format](./img/parquet_format_02.gif)

上图展示了一个Parquet文件的结构，一个文件中可以存储多个行组。

- 文件的首位都是该文件的Magic Number，用于校验它是否是一个Parquet文件。
- Footer中存储着FileMetaData，Footer length存储了文件元数据的大小，通过该值和文件长度可以计算出元数据（metadata）的偏移量（offset）。
    - FileMetaData中包括每一个行组的元数据信息和当前文件的Schema信息。
- 每一页的开始都会存储该页的元数据（PageHeader）。
    - 在Parquet中，有三种类型的页：数据页、字典页和索引页。数据页用于存储当前行组中该列的值，字典页存储该列值的编码字典，每一个列块中最多包含一个字典页，索引页用来存储当前行组下该列的索引。

### 映射下推(Project PushDown)
说到列式存储的优势，映射下推是最突出的，它意味着在获取表中原始数据时只需要扫描查询中需要的列，由于每一列的所有值都是连续存储的，所以分区取出每一列的所有值就可以实现TableScan算子，而避免扫描整个表文件内容。在Parquet中原生就支持映射下推，执行查询的时候可以通过Configuration传递需要读取的列的信息，这些列必须是Schema的子集，映射每次会扫描一个Row Group的数据，然后一次性得将该Row Group里所有需要的列的Cloumn Chunk都读取到内存中，每次读取一个Row Group的数据能够大大降低随机读的次数，除此之外，Parquet在读取的时候会考虑列是否连续，如果某些需要的列是存储位置是连续的，那么一次读操作就可以把多个列的数据读取到内存。

### 谓词下推(Predicate PushDown)
在数据库之类的查询系统中最常用的优化手段就是谓词下推了，通过将一些过滤条件尽可能的在最底层执行可以减少每一层交互的数据量，从而提升性能，例如 `select count(1) from A Join B on A.id = B.id where A.a > 10 and B.b < 100`SQL查询中，在处理Join操作之前需要首先对A和B执行TableScan操作，然后再进行Join，再执行过滤，最后计算聚合函数返回，但是如果把过滤条件A.a>10和B.b<100分别移到A表的TableScan和B表的TableScan的时候执行，可以大大降低Join操作的输入数据。无论是行式存储还是列式存储，都可以在将过滤条件在读取一条记录之后执行以判断该记录是否需要返回给调用者，在Parquet做了更进一步的优化，优化的方法时对每一个Row Group的每一个Column Chunk在存储的时候都计算对应的统计信息，包括该Column Chunk的最大值、最小值和空值个数。通过这些统计值和该列的过滤条件可以判断该Row Group是否需要扫描。另外Parquet未来还会增加诸如Bloom Filter和Index等优化数据，更加有效的完成谓词下推。

### 压缩
使用不同格式存储TPC-H和TPC-DS数据集中两个表数据的文件大小对比，Parquet较之于其他的二进制文件存储格式能够更有效的利用存储空间，而新版本的Parquet(2.0版本)使用了更加高效的页存储方式，进一步的提升存储空间。

### 查询
看出Parquet较之于其他的行式存储格式有较明显的性能提升。criteo公司在Hive中使用ORC和Parquet两种列式存储格式执行TPC-DS基准测试的结果，数据存储方面，两种存储格式在都是用snappy压缩的情况下量中存储格式占用的空间相差并不大，查询的结果显示Parquet格式稍好于ORC格式，两者在功能上也都有优缺点，Parquet原生支持嵌套式数据结构，而ORC对此支持的较差，这种复杂的Schema查询也相对较差；而Parquet不支持数据的修改和ACID，但是ORC对此提供支持，但是在OLAP环境下很少会对单条数据修改，更多的则是批量导入。











