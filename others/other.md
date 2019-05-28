
## Kafka
是流处理平台，可以发布和订阅，类似消息队列。
模式：生产者 - 数据流 - 消费者
存储：数据和日志

Kafka是分布式发布-订阅消息系统，在Kafka集群中，没有“中心主节点”的概念，集群中所有的服务器都是对等的，因此，可以在不做任何配置的更改的情况下实现服务器的的添加与删除，同样的消息的生产者和消费者也能够做到随意重启和机器的上下线。

#### Kafka术语介绍
1. 消息生产者Producer，是消息的产生的源头，负责生成消息并发送到Kafka服务器上。
2. 消息消费者Consumer，是消息的使用方，负责消费Kafka服务器上的消息。
3. 主题Topic，由用户定义并配置在Kafka服务器，用于建立生产者和消息者之间的订阅关系：生产者发送消息到指定的Topic下，消息者从这个Topic下消费消息。
4. 消息分区Partition，一个Topic下面会分为很多分区，例如：“kafka-test”这个Topic下可以分为6个分区，分别由两台服务器提供，那么通常可以配置为让每台服务器提供3个分区，假如服务器ID分别为0、1，则所有的分区为0-0、0-1、0-2和1-0、1-1、1-2。partition是Topic物理上的分组，一个topic可以分为多个partition，每个partition是一个有序的队列。partition中的每条消息都会被分配一个有序的id（offset）。
5. Broker：即Kafka的服务器，用户存储消息，Kafa集群中的一台或多台服务器统称为broker。
6. 消费者分组Group，用于归组同类消费者，在Kafka中，多个消费者可以共同消息一个Topic下的消息，每个消费者消费其中的部分消息，这些消费者就组成了一个分组，拥有同一个分组名称，通常也被称为消费者集群。
7. Offset：消息存储在Kafka的Broker上，消费者拉取消息数据的过程中需要知道消息在文件中的偏移量，这个偏移量就是所谓的Offset。

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

---

## Druid

---

## Docker

Docker不是虚拟机。但可以理解为轻量的虚拟机，把一个应用程序放在一个独立的环境里运行。

![Docker Architecture](../img/architecture_docker.svg)

- 例子：

`docker run ubuntu echo hello docker` 是用一个Ubuntu镜像运行ehco hello docker命令。

`docker run nginx` 启动一个nginx容器。

- docker命令：
`docker pull` 获取image。

`docker build` 创建image。

`docker images` 可以看本地所有镜像。

`docker run` 启动container。

`docker ps` 可以查看运行中的container。

`docker stop [container id]` 来停止容器。

`docker rmi` 删除image。

`docker rm` 删除container。

`docker cp` 在host和container之间拷贝文件。

`docker commit` 保存改动为新的image。

---

## K8s

---

## Elastic Stack
#### Elasticsearch 

- 依赖JDK. 
- 配置文件位于config/elasticsearch.yml
- jvm.options 用于修改jvm相关参数如内存大小等。
- log4j2.properties 日志先关配置

本地启动集群方式：

- `bin/elasticsearch`
- `bin/elasticsearch -Ehttp.prot=8200 -Epath.data=node2`
- `bin/elasticsearch -Ehttp.prot=7200 -Epath.data=node3`

常用术语：

- Document 文档数据（一条数据）
- Index 索引(类似数据库)
- Type 索引中的数据类型（类似Table）
- Field 字段，文档属性
- Query DSL 查询语言

#### Kibana
配置config/kibana.yml
bin/kibana运行

#### Beats 
Light Weight Data Shipper

- FileBeat 日志文件
- Metricbeat 收集度量数据
- Packetbeat 网络数据
- Heartbeat 健康检查

beat属于数据起始端，用于收集数据，存储于elasticsearch，最后用kibana展示。

#### Logstash
Data Shipper

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

## AWS

S3

EC2

RDS

