
## Kafka
是流处理平台，可以发布和订阅，类似消息队列。
模式：生产者 - 数据流 - 消费者
存储：数据和日志

Kafka是分布式发布-订阅消息系统，在Kafka集群中，没有“中心主节点”的概念，集群中所有的服务器都是对等的，因此，可以在不做任何配置的更改的情况下实现服务器的的添加与删除，同样的消息的生产者和消费者也能够做到随意重启和机器的上下线。


慕课：

物理概念：

逻辑概念：


#### Kafka术语介绍
1. 消息生产者Producer，是消息的产生的源头，负责生成消息并发送到Kafka服务器上。
2. 消息消费者Consumer，是消息的使用方，负责消费Kafka服务器上的消息。
3. 主题Topic，逻辑概念，由用户定义并配置在Kafka服务器，用于建立生产者和消息者之间的订阅关系：生产者发送消息到指定的Topic下，消息者从这个Topic下消费消息。
4. 消息分区Partition，一个Topic下面会分为很多分区，物理概念，例如：“kafka-test”这个Topic下可以分为6个分区，分别由两台服务器提供，那么通常可以配置为让每台服务器提供3个分区，假如服务器ID分别为0、1，则所有的分区为0-0、0-1、0-2和1-0、1-1、1-2。partition是Topic物理上的分组，一个topic可以分为多个partition，每个partition是一个有序的队列。partition中的每条消息都会被分配一个有序的id（offset）。
5. Broker：即Kafka的服务器（节点），物理概念，用户存储消息，Kafa集群中的一台或多台服务器统称为broker。
6. 消费者分组Group，用于归组同类消费者，在Kafka中，多个消费者可以共同消息一个Topic下的消息，每个消费者消费其中的部分消息，这些消费者就组成了一个分组，拥有同一个分组名称，通常也被称为消费者集群。
7. Offset：消息存储在Kafka的Broker上，消费者拉取消息数据的过程中需要知道消息在文件中的偏移量，这个偏移量就是所谓的Offset。

8. Replication: partition的副本，可以有多个，之间的数据是一样的。
9. Replication Leader: 多个副本需要一个Leader与producer和consumer交互。
10. ReplicaManager: 


#### Broker
1. Message在Broker中通Log追加的方式进行持久化存储。并进行分区（patitions)。
2. 为了减少磁盘写入的次数,broker会将消息暂时buffer起来,当消息的个数(或尺寸)达到一定阀值时,再flush到磁盘,这样减少了磁盘IO调用的次数。
3. Broker没有副本机制，一旦broker宕机，该broker的消息将都不可用。Message消息是有多份的。
4. Broker不保存订阅者的状态，由订阅者自己保存。
5. 无状态导致消息的删除成为难题（可能删除的消息正在被订阅），kafka采用基于时间的SLA(服务水平保证)，消息保存一定时间（通常为7天）后会被删除。
6. 消息订阅者可以rewind back到任意位置重新进行消费，当订阅者故障时，可以选择最小的offset(id)进行重新读取消费消息。

#### Message组成
1. Message消息：是通信的基本单位，每个producer可以向一个topic（主题）发布一些消息。
2. Kafka中的Message是以topic为基本单位组织的，不同的topic之间是相互独立的。每个topic又可以分成几个不同的partition(每个topic有几个partition是在创建topic时指定的)，每个partition存储一部分Message。
3. partition中的每条Message包含了以下三个属性：
    - offset消息唯一标识，对应类型：long
    - MessageSize 对应类型：int32
    - data是message的具体内容。

#### Partitions分区
1. 通过分区，可以将日志内容分散到多个server上，来避免文件尺寸达到单机磁盘的上限，每个partiton都会被当前server(kafka实例)保存。
2. 可以将一个topic切分多任意多个partitions，来消息保存/消费的效率。
3. 越多的partitions意味着可以容纳更多的consumer，有效提升并发消费的能力。

#### Consumers
1. 消息和数据消费者，订阅topics并处理其发布的消息的过程叫做consumers。
2. 在kafka中，我们可以认为一个group是一个“订阅者”，一个Topic中的每个partions，只会被一个“订阅者”中的一个consumer消费，不过一个consumer可以消费多个partitions中的消息（消费者数据小于Partions的数量时）。注意：kafka的设计原理决定，对于一个topic，同一个group中不能有多于partitions个数的consumer同时消费，否则将意味着某些consumer将无法得到消息。
3. 一个partition中的消息只会被group中的一个consumer消费。每个group中consumer消息消费互相独立。


## Kafka 结构

上游producer，下游consumer，中间是kafka集群。
横向有connector连接DB，stream processors与其他app做流式交互。
所以Kafka会有 producer API, consumer API, connectors API, Streams API

### zookeeper
Kafka强依赖与zookeeper, borker的信息，topic，partition的分布信息都存在zookeeper上。


### Kafka消息结构
Offset
Length
CRC32
Magic
attributes
Timestamp
Key Length
Key
Value Length
Value

### Kafka 特点





#### Kafka的持久化
1. 一个Topic可以认为是一类消息，每个topic将被分成多partition(区)，每个partition在存储层面是append log文件。任何发布到此partition的消息都会被直接追加到log文件的尾部，每条消息在文件中的位置称为offset（偏移量），partition是以文件的形式存储在文件系统中。
2. Logs文件根据broker中的配置要求,保留一定时间后删除来释放磁盘空间。

#### Kafka的通讯协议：
1. Kafka的Producer、Broker和Consumer之间采用的是一套自行设计基于TCP层的协议，根据业务需求定制，而非实现一套类似ProtocolBuffer的通用协议。
2. 基本数据类型：（Kafka是基于Scala语言实现的，类型也是Scala中的数据类型）
    - 定长数据类型：int8,int16,int32和int64，对应到Java中就是byte, short, int和long。
    - 变长数据类型：bytes和string。变长的数据类型由两部分组成，分别是一个有符号整数N(表示内容的长度)和N个字节的内容。其中，N为-1表示内容为null。bytes的长度由int32表示，string的长度由int16表示。
    - 数组：数组由两部分组成，分别是一个由int32类型的数字表示的数组长度N和N个元素。
3. Kafka通讯的基本单位是Request/Response。

#### 数据传输的事务定义：
1. at most once:最多一次,这个和JMS中"非持久化"消息类似，发送一次，无论成败，将不会重发。
消费者fetch消息，然后保存offset，然后处理消息；当client保存offset之后，但是在消息处理过程中出现了异常，导致部分消息未能继续处理.那么此后"未处理"的消息将不能被fetch到。
2. at least once:消息至少发送一次，如果消息未能接受成功，可能会重发，直到接收成功。
消费者fetch消息，然后处理消息，然后保存offset.如果消息处理成功之后，但是在保存offset阶段zookeeper异常导致保存操作未能执行成功，这就导致接下来再次fetch时可能获得上次已经处理过的消息。offset没有及时的提交给zookeeper，zookeeper恢复正常还是之前offset状态。
3. exactly once:消息只会发送一次。kafka中并没有严格的去实现，我们认为这种策略在kafka中是没有必要的。

注：通常情况下"at-least-once"是我们首选。(相比at most once而言，重复接收数据总比丢失数据要好)。


## 零拷贝提高性能





---

## Druid

随着互联网快速发展，数据量增长快，达到TB、PB。数据量如此大，如何满足后期分析，传统面向OLTP型数据库（ORACLE、MYSQL等）无法要求，渐渐开始转向OLAP，虽然很多OLAP数据库吸收分布式计算思想，数据达到20亿以上后，进行Count、聚合等操作性能仍然达不到客户实时分析要求。虽然相关大数据框架及组件已经很流行：Hadoop（离线分析）、Spark、storm、Hive、Impala、Hbase等，Hadoop生态系统大庞大，Spark一站式安装部署，但是满足实时分析还需借助其它组件、开发要求很高。

Druid是一个用于大数据实时查询和分析的高容错、高性能开源分布式时序数据库系统，旨在快速处理大规模的数据，并能够实现快速查询和分析。尤其是当发生代码部署、机器故障以及其他产品系统遇到宕机等情况时，Druid仍能够保持正常运行。创建Druid的最初意图主要是为了解决查询延迟问题，当时试图使用Hadoop来实现交互式查询分析，但是很难满足实时分析的需要。而Druid提供了以交互方式访问数据的能力，并权衡了查询的灵活性和性能而采取了特殊的存储格式。

#### Druid适用场景
Druid应用最多的是类似于广告分析创业公司Metamarkets中的应用场景，如广告分析、互联网广告系统监控以及网络监控等。当业务中出现以下情况时，Druid是一个很好的技术方案选择：

- 需要交互式聚合和快速探究大量数据时；
- 需要实时查询分析时；
- 具有大量数据时，如每天数亿事件的新增、每天数10T数据的增加；
- 对数据尤其是大数据进行实时分析时；
- 需要一个高可用、高容错、高性能数据库时

#### Druid数据
Druid是一个开源的数据存储设计的事件数据的OLAP查询，提供一个高层次的概述如何存储数据和Druid集群的体系结构。

数据样例:

| timestamp | publisher | advertiser | gender | country | click | price |
| --------- | --------- | ---------- | ------ | ------- | ----- | ----- |
| 2011-01-01T01:01:35Z | ever.com | google.com | Male | USA | 0 | 0.65 |
| 2011-01-01T01:03:63Z | ever.com | google.com | Male | USA | 0 | 0.62 |
| 2011-01-01T01:04:51Z | ever.com | google.com | Male | USA | 1 | 0.45 |
| 2011-01-01T01:00:00Z | fast.com | google.com | Female | UK | 0 | 0.87 |
| 2011-01-01T02:00:00Z | fast.com | google.com | Female | UK | 0 | 0.99 |
| 2011-01-01T02:00:00Z | fast.com | google.com | Female | UK | 1 | 1.53 |

数据集由三个不同的组件组成：

- 时间序列化列：以时间序列进行数据分片，所有查询以时间为中心轴。
- 维度列：Druid基于列式存储，查询结果展示列，常用于数据过滤，如示例数据集有四个维度:出版商，广告商，性别和国家。
- 聚合列：通常用于计算值，操作方法如：COUNT、SUM等。

#### Druid 聚合
上述例子数据集中的单条信息作用不大，因为这样的数据万亿。然而这种类型的数据研究概述可以产生经济效益。Druid使用我们称之为“聚合”的过程对这些原始数据聚合操作，类似（伪代码）如下：
```
GROUP BY timestamp, publisher, advertiser, gender, country
impressions = COUNT(1),  clicks = SUM(click),  revenue = SUM(price)
```

在实践中我们看到聚合数据可以大大减少需要被存储的数据的大小（高达100倍）。减少存储确实是以成本为代价的，聚合数据后无法查询单个数据的能力；另一种解决方式减少聚合粒度，尽量满足查询数据的最小粒度。因此Druid通过queryGranularity方法(或属性granularity)定义这个粒度查询数据，最低支持为毫秒。

通过上述伪代码聚合后的数据：

| timestamp | publisher | advertiser | gender | country | impressions | clicks | revenue |
| --------- | --------- | ---------- | ------ | ------- | ----------- | ----- | ------- |
| 2011-01-01T01:00:00Z | fast.com | google.com | Male | USA | 1800 | 25 | 15.70 |
| 2011-01-01T01:00:00Z | ever.com | google.com | Male | USA | 2912 | 42 | 29.18 |
| 2011-01-01T02:00:00Z | fast.com | google.com | Female | UK | 1953 | 17 | 17.31 |
| 2011-01-01T02:00:00Z | ever.com | google.com | Female | UK | 3194 | 170 | 34.01 |

#### Druid 分片数据
Druid的分片称之为Segment（即段），通常按时间对数据进行分片。如对示例数据进行压缩，我们可以创建两个段，按每小时分片。段是保存时间间隔内数据，段包含按列存储的数据以及这些列的索引，Druid查询索引扫描段。段由数据源、间隔、版本的唯一标识，和一个可选的分区号。段命名规范如：
datasource_interval_version_partitionnumber

例如：

Segment sampleData_2011-01-01T01:00:00:00Z_2011-01-01T02:00:00:00Z_v1_0 contains
```
2011-01-01T01:00:00Z  fast.com  google.com  Male  USA  1800  25  15.70
2011-01-01T01:00:00Z  ever.com  google.com  Male  USA  2912  42  29.18
```
Segment sampleData_2011-01-01T02:00:00:00Z_2011-01-01T03:00:00:00Z_v1_0 contains
```
2011-01-01T02:00:00Z  fast.com  google.com  Male  UK  1953  17  17.31
2011-01-01T02:00:00Z  fever.com  google.com  Male  UK  3194  170  34.01
```

#### Druid 索引数据
Druid查询速度取决于如何存储数据。从搜索基础架构借用想法，Druid创建只读数据快照，查询分析存储在高度优化的数据结构。Druid是一个列存储，每列被单独存储。Druid查询相当好，是因为只查询所需的列。不同的列还可以采用不同的压缩方式，不同的列也可以有与它们相关的不同的索引。Druid索引数据在数据分片级别上。

#### Druid 数据加载
Druid有两方式获取数据，实时和批量，Druid实时获取很费劲，确切的说Druid不能保证实时获取。批量获取可以保证批量创建段及相应数据。Druid通常采用实时管道获取实时数据（最近数据），采用批管道获取副本数据。

#### Druid 数据查询
Druid的本地查询语言是JSON通过HTTP，虽然社区在众多的语言中提供了查询库，包括SQL查询贡献库；Druid设计用于单表操作，目前不支持联接(JOIN)。

#### Druid 集群
Druid是由不同角色的系统构建而成的一个整体系统，它的名字来自在许多角色扮演游戏中的Druid类：它是一个shape-shifter，可以在一个群组中采取许多不同的形式来满足各种不同的角色。Druid的整体架构中目前包括以下节点类型：

- Historical

对“historical”数据（非实时）进行处理存储和查询的地方。historical节点响应从broker节点发来的查询，并将结果返回给broker节点。它们在Zookeeper的管理下提供服务，并使用Zookeeper监视信号加载或删除新数据段。

- Middlemanager

Middlemanager进程负责将新的数据摄入到集群中，将外部数据源数据转换成Druid所识别的segment。

- Coordinator

监控historical节点组，以确保数据可用、可复制，并且在一般的“最佳”配置。它们通过从MySQL读取数据段的元数据信息，来决定哪些数据段应该在集群中被加载，使用Zookeeper来确定哪个historical节点存在，并且创建Zookeeper条目告诉historical节点加载和删除新数据段。

Coordinator进程负责监控Historical进程，它负责将segment分配到指定的Historical服务上，确保所有Historical节点间的段均衡。

- Overload

Overload进程负责监控Middlemanager进程，它负责将摄取任务分配给Middlemanager并协调segment的发布。它就是数据摄入到Druid的控制器

- Broker

接收来自外部客户端的查询，并将这些查询转发到Realtime和Historical节点。当Broker节点收到结果，它们将合并这些结果并将它们返回给调用者。由于了解拓扑，Broker节点使用Zookeeper来确定哪些Realtime和Historical节点的存在。

Broker进程负责接受Client的查询请求，并将查询转发到Historical和Middlemanager中。Broker会接受所有子查询的结果，并且将数据进行合并返回给Client

- Router

Router进程是一个可选的进程，他为Broker、Overload和Coordinator提供了统一API网管服务。如果不启动该进程，也可以直接连接Broker、Overload和Coordinator服务

- Realtime ???

实时摄取数据，它们负责监听输入数据流并让其在内部的Druid系统立即获取，Realtime节点同样只响应broker节点的查询请求，返回查询结果到broker节点。旧数据会被从Realtime节点转存至Historical节点。

- Indexer ???

节点会形成一个加载批处理和实时数据到系统中的集群，同时会对存储在系统中的数据变更（也称为索引服务）做出响应。这种分离让每个节点只关心自身的最优操作。通过将Historical和Realtime分离，将对进入系统的实时流数据监控和处理的内存分离。通过将Coordinator和Broker分离，把查询操作和维持集群上的“好的”数据分布的操作分离。

- Zookeeper

负责存储集群的状态以及作为服务发现组件，例如集群的拓扑信息，overlord leader 的选举，indexing task 的管理等等。

Coordinator 负责 segments 的管理，如 segments 下载、删除以及如何在 historical 之间做均衡等等。

Metadata storage 负责存储 segments 的元信息，以及管理集群各种各样的持久化或临时性数据，比如配置信息、审计信息等等。
产品优势
E-MapReduce Druid 基于开源 Druid 做了大量的改进，包括与E-MapReduce、阿里云周边生态的集成、方便的监控与运维支持、易用的产品接口等等，真正做到了即买即用和 7*24 免运维。


Druid 使用建议
本小节主要想结合实际问题，给大家提供一些 Druid 的使用建议，供大家参考。
①什么样的业务适合用 Druid?
建议如下：

时序化数据：Druid 可以理解为时序数据库，所有的数据必须有时间字段。
实时数据接入可容忍丢数据(tranquility)：目前 tranquility 有丢数据的风险，所以建议实时和离线一起用，实时接当天数据，离线第二天把今天的数据全部覆盖，保证数据完备性。
OLAP 查询而不是 OLTP 查询：Druid 查询并发有限，不适合 OLTP 查询。
非精确的去重计算：目前 Druid 的去重都是非精确的。
无 Join 操作：Druid 适合处理星型模型的数据，不支持关联操作。
数据没有 update 更新操作，只对 segment 粒度进行覆盖：由于时序化数据的特点，Druid 不支持数据的更新。

②如何设置合理的 Granularity?

Granularity 设置

首先解释下 segmentGranularity 和 queryGranularity，前者是 segment 的组成粒度，后者是 segment 的聚合粒度。
要求 queryGranularity 小于等于 segmentGranularity，然后在数据导入时，按照下面的规则进行设置。
segmentGranularity(离线数据导入的设置)：

导入的数据是天级别以内的：“hour”或者“day”。
导入的数据是天级别以上的：“day”。
导入的数据是年级别以上的：“month”。

需要说明的是，这里我们仅仅是简单的通过 intervals 进行 segmentGranularity 的设置，更加合理的做法应该是结合每个 segment 的大小以及查询的复杂度进行综合衡量。
考虑到 tranquility 实时任务的特殊性和数据的安全性，我们建议实时数据导入时，segmentGranularity 设置成“hour”。
queryGranularity：根据业务查询最小粒度和查询复杂度来定，假设查询只需要到小时粒度，则该参数设置为“hour”。
③需要去重的维度到底需不需要定义到维度列中?

如果去重的维度只需要去重计算，没有其他的作用，譬如进行过滤或者作为分组字段，我们建议不要添加到维度列中，因为不添加的话，这样数据的预聚合效果更好。

④如何选择查询方式?
常用的三种查询：

select sum(A) from DS where time>? [timeseries]
select sum(A) from DS where time>? group by B order by C limit 2 [topN]
select sum(A) from DS where time>? group by B，C order by C limit 2[groupby]

没有维度分组的场景使用 timeseries，单维度分组查询的场景使用 topN，多维度分组查询场景使用 groupby。
由于 groupby 并不会将 limit 下推(Druid 新版本进行了优化，虽然可以下推，但是对于指标的排序是不准确的)，所以单维度的分组查询，尽量用 topN 查询。




Druid.

Slice and dice

Segment
列存储columnar storage. ??
Dictionary Encoding
Inverted Indexes

Rollup 预聚合
segment granularity  !!
Query granularity  !!

Ingestion    middle manager负责
streaming ingestion
    kafka indexing service.
    kinesis…
    tranquility
Batch ingestion
    Native ?
    Hadoop

Append only ??
exactly once??

外部依赖：
Deep storage
    s3  HDFS
Metadata storage
    mysql   postgresql
Zookeeper
存储 计算分离

Middle manager 数据摄入
Historical Node
Brocker Node 响应client query, return result
Coordinator 管理 historical 节点
Overlord 管理 Middle manager 节点







---

## Prometheus
Prometheus是一个开源监控系统，它前身是SoundCloud的警告工具包。以HTTP方式，通过pull模型拉去时间序列数据。

就Prometheus而言，pull拉取采样点的端点服务称之为instance。多个这样pull拉取采样点的instance, 则构成了一个job。

例如, 一个被称作api-server的任务有四个相同的实例。
```
job: api-server
   instance 1: 1.2.3.4:5670
   instance 2: 1.2.3.4:5671
   instance 3: 5.6.7.8:5670
   instance 4: 5.6.7.8:5671
```

自动化生成的标签和时间序列，当Prometheus拉取一个目标，会自动地把两个标签添加到度量名称的标签列表中，分别是：job目标所属的配置任务名称api-server。instance采样点所在服务host:port。

Prometheus fundamentally stores all data as time series: streams of timestamped values belonging to the same metric and the same set of labeled dimensions. Every time series is uniquely identified by its metric name and a set of key-value pairs, also known as labels.

The metric name must match the regex `[a-zA-Z_:][a-zA-Z0-9_:]*.`. The colons are reserved for user defined recording rules. They should not be used by exporters or direct instrumentation.

Label names may contain ASCII letters, numbers, as well as underscores. They must match the regex `[a-zA-Z_][a-zA-Z0-9_]*.`. Label names beginning with `__` are reserved for internal use.

Given a metric name and a set of labels, time series are frequently identified using this notation: `<metric name>{<label name>=<label value>, ...}`.

### metric type
Prometheus客户端库提供四种核心度量标准类型。这些目前仅在客户端库中区分。Prometheus服务器尚未使用类型信息，并将所有数据展平为无类型时间序列。

##### Counter
计数器是表示单个单调递增计数器的累积量，其值只能增加或在重启时重置为零。例如，使用计数器来表示服务的总请求数，已完成的任务或错误总数。不要使用计数器来监控可能减少的值。

counter主要有两个方法：
```go
//将counter值加1.
Inc()
// 将指定值加到counter值上，如果指定值< 0会panic.
Add(float64)
```
- Counter

一般metric容器使用的步骤都是：

1. 初始化一个metric容器
2. 2.Register注册容器
3. 向容器中添加值

使用举例：
```go
//step1:初始一个counter
pushCounter = prometheus.NewCounter(prometheus.CounterOpts{
    Name: "repository_pushes",
    Help: "Number of pushes to external repository.",
})

//setp2:注册容器
err = prometheus.Register(pushCounter)
if err != nil {
    fmt.Println("Push counter couldn't be registered AGAIN, no counting will happen:", err)
    return
}

pushComplete := make(chan struct{})
// TODO: Start a goroutine that performs repository pushes and reports
// each completion via the channel.
for range pushComplete {
    //step3:向容器中写入值
    pushCounter.Inc()
}
```

- CounterVec

CounterVec是一组counter，这些计数器具有相同的描述，但它们的变量标签具有不同的值。如果要计算按各种维度划分的相同内容（例如，响应代码和方法分区的HTTP请求数，则使用此方法。使用NewCounterVec创建实例。
```go
//step1:初始化一个容器
httpReqs := prometheus.NewCounterVec(
    prometheus.CounterOpts{
        Name: "http_requests_total",
        Help: "How many HTTP requests processed, partitioned by status code and HTTP method.",
    },
    []string{"code", "method"}, //Labels.
)
//step2:注册容器
prometheus.MustRegister(httpReqs)

httpReqs.WithLabelValues("404", "POST").Add(42)

// If you have to access the same set of labels very frequently, it
// might be good to retrieve the metric only once and keep a handle to
// it. But beware of deletion of that metric, see below!
//step3:向容器中写入值，主要调用容器的方法如Inc()或者Add()方法
m := httpReqs.WithLabelValues("200", "GET")
for i := 0; i < 1000000; i++ {
    m.Inc()
}
// Delete a metric from the vector. If you have previously kept a handle
// to that metric (as above), future updates via that handle will go
// unseen (even if you re-create a metric with the same label set
// later).
httpReqs.DeleteLabelValues("200", "GET")
// Same thing with the more verbose Labels syntax.
httpReqs.Delete(prometheus.Labels{"method": "GET", "code": "200"})
```

##### Gauge
- Gauge

Gauge可以用来存放一个可以任意变大变小的数值，通常用于测量值，例如温度或当前内存使用情况，或者运行的goroutine数量。主要有以下四个方法：
```go
// 将Gauge中的值设为指定值.
Set(float64)
// 将Gauge中的值加1.
Inc()
// 将Gauge中的值减1.
Dec()
// 将指定值加到Gauge中的值上。(指定值可以为负数)
Add(float64)
// 将指定值从Gauge中的值减掉。(指定值可以为负数)
Sub(float64)
```

示例代码（实时统计CPU的温度）：
```go
//step1:初始化容器
cpuTemprature := prometheus.NewGauge(prometheus.GaugeOpts{
    Name:      "CPU_Temperature",
    Help:      "the temperature of CPU",
})
//step2:注册容器
prometheus.MustRegister(cpuTemprature)
//定时获取cpu温度并且写入到容器
func(){
    tem = getCpuTemprature()
    //step3:向容器中写入值。调用容器的方法
    cpuTemprature.Set(tem)  
}
```

- GaugeVec

假设你要一次性统计四个cpu的温度，这个时候就适合使用GaugeVec了。
```go
cpusTemprature := prometheus.NewGaugeVec(
    prometheus.GaugeOpts{
        Name:      "CPUs_Temperature",
        Help:      "the temperature of CPUs.",
    },
    []string{
        // Which cpu temperature?
        "cpuName",
    },
)
prometheus.MustRegister(cpusTemprature)

cpusTemprature.WithLabelValues("cpu1").Set(temperature1)
cpusTemprature.WithLabelValues("cpu2").Set(temperature2)
cpusTemprature.WithLabelValues("cpu3").Set(temperature3)
```

##### Histogram

主要用于表示一段时间范围内对数据进行采样，（通常是请求持续时间或响应大小），并能够对其指定区间以及总数进行统计，通常我们用它计算分位数的直方图。
```go
temps := prometheus.NewHistogram(prometheus.HistogramOpts{
    Name:    "pond_temperature_celsius",
    Help:    "The temperature of the frog pond.", // Sorry, we can't measure how badly it smells.
    Buckets: prometheus.LinearBuckets(20, 5, 5),  // 5 buckets, each 5 centigrade wide. Start with 20.
})

// Simulate some observations.
for i := 0; i < 1000; i++ {
    temps.Observe(30 + math.Floor(120*math.Sin(float64(i)*0.1))/10)
}

// Just for demonstration, let's check the state of the histogram by
// (ab)using its Write method (which is usually only used by Prometheus
// internally).
metric := &dto.Metric{}
temps.Write(metric)
fmt.Println(proto.MarshalTextString(metric))
```

##### Summary
Summary从事件或样本流中捕获单个观察，并以类似于传统汇总统计的方式对其进行汇总：

1. 观察总和。
2. 观察计数。
3. 排名估计。

典型的用例是观察请求延迟，默认情况下Summary提供延迟的中位数。
```go
temps := prometheus.NewSummary(prometheus.SummaryOpts{
    Name:       "pond_temperature_celsius",
    Help:       "The temperature of the frog pond.",
    Objectives: map[float64]float64{0.5: 0.05, 0.9: 0.01, 0.99: 0.001},
})

// Simulate some observations.
for i := 0; i < 1000; i++ {
    temps.Observe(30 + math.Floor(120*math.Sin(float64(i)*0.1))/10)
}

// Just for demonstration, let's check the state of the summary by
// (ab)using its Write method (which is usually only used by Prometheus
// internally).
metric := &dto.Metric{}
temps.Write(metric)
fmt.Println(proto.MarshalTextString(metric))
```

---

## Nginx

Nginx是一款轻量级的Web服务器、反向代理服务器，由于它的内存占用少，启动极快，高并发能力强，在互联网项目中广泛应用。

由于防火墙的原因，我们并不能直接访问谷歌，那么我们可以借助VPN来实现，这就是一个简单的正向代理的例子。这里你能够发现，正向代理“代理”的是客户端，而且客户端是知道目标的，而目标是不知道客户端是通过VPN访问的。

当我们在外网访问百度的时候，其实会进行一个转发，代理到内网去，这就是所谓的反向代理，即反向代理“代理”的是服务器端，而且这一个过程对于客户端而言是透明的。


很多时候，在开发、测试环境下，我们都得自己去配置Nginx，就是去配置nginx.conf。nginx.conf是典型的分段配置文件，下面我们来分析下。

所谓反向代理，很简单，其实就是在location这一段配置中的root替换成proxy_pass即可。root说明是静态资源，可以由Nginx进行返回；而proxy_pass说明是动态请求，需要进行转发，比如代理到Tomcat上。反向代理过程是透明的，比如说request -> Nginx -> Tomcat，那么对于Tomcat而言，请求的IP地址就是Nginx的地址，而非真实的request地址，

---

## AWS
### VPC
    虚拟局域网，一个路由下面的一个局域网。
    VPC包含公有子网和私有子网，公有子网可以直接访问公网，但私有子网不能，需要通过NAT，NAT可以理解为路由器(网关)。
    NAT可以用EC2实例来制作。
    AWS也提供了NAT服务（推荐）。

### EC2
    可以理解为虚拟机。
    上线代码方式：推荐Docker

### RDS
    关系型数据库的管理平台。
    可以选择不同数据库，比如mysql。可以创建主从库，并且有多个从库。
    kingshard中间件，可以管理数据库的主从分离，负载均衡。

### ElastiCache
    缓存系统管理平台。（Memcache）

### ELB
    Elastic Load Balance，可伸缩负载均衡。私有子网中的服务要通过ELB暴露到公网。

### AutoScaling
    自动缩小或扩容的工具。通过管理EC2的启动配置来管理EC2数量。

S3

ROUTE 53



---



## Presto

Hive

Presto