# Kafka
是流处理平台，可以发布和订阅，类似消息队列。
模式：生产者 - 数据流 - 消费者
存储：数据和日志

Kafka是分布式发布-订阅消息系统，在Kafka集群中，没有“中心主节点”的概念，集群中所有的服务器都是对等的，因此，可以在不做任何配置的更改的情况下实现服务器的的添加与删除，同样的消息的生产者和消费者也能够做到随意重启和机器的上下线。

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



### confluent schema registry