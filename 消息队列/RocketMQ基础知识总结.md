# RocketMQ

RocketMQ 是一个 **队列模型** 的消息中间件，具有**高性能、高可靠、高实时、分布式** 的特点。它是一个采用 Java 语言开发的分布式的消息系统，由阿里巴巴团队开发，在 2016 年底贡献给 Apache，成为了 Apache 的一个顶级项目。 在阿里内部，RocketMQ 很好地服务了集团大大小小上千个应用，在每年的双十一当天，更有不可思议的万亿级消息通过 RocketMQ 流转。

## 队列模型和主题模型

### 队列模型

就像我们理解队列一样，消息中间件的队列模型就真的只是一个队列。

![](https://oss.javaguide.cn/github/javaguide/high-performance/message-queue/16ef3834ae653469.jpg)

在一开始我跟你提到了一个 **“广播”** 的概念，也就是说如果我们此时我们需要将一个消息发送给多个消费者(比如此时我需要将信息发送给短信系统和邮件系统)，这个时候单个队列即不能满足需求了。

当然你可以让 `Producer` 生产消息放入多个队列中，然后每个队列去对应每一个消费者。问题是可以解决，创建多个队列并且复制多份消息是会很影响资源和性能的。而且，这样子就会导致生产者需要知道具体消费者个数然后去复制对应数量的消息队列，这就违背我们消息中间件的 **解耦** 这一原则。

### 主题模型

那么有没有好的方法去解决这一个问题呢？有，那就是 **主题模型** 或者可以称为 **发布订阅模型** 。（设计模式里面的观察者模式）

在主题模型中，消息的生产者称为 **发布者(Publisher)** ，消息的消费者称为 **订阅者(Subscriber)** ，存放消息的容器称为 **主题(Topic)** 。其中，发布者将消息发送到指定主题中，订阅者需要 **提前订阅主题** 才能接受特定主题的消息。

![](https://oss.javaguide.cn/github/javaguide/high-performance/message-queue/16ef3837887d9a54sds.jpg)

### RocketMQ 中的消息模型
RocketMQ 中的消息模型就是按照 **主题模型** 所实现的。你可能会好奇这个 **主题** 到底是怎么实现的呢？你上面也没有讲到呀！

其实对于主题模型的实现来说每个消息中间件的底层设计都是不一样的，就比如 `Kafka` 中的 **分区** ，`RocketMQ` 中的 **队列** ，`RabbitMQ` 中的 `Exchange` 。我们可以理解为 **主题模型/发布订阅模型** 就是一个标准，那些中间件只不过照着这个标准去实现而已。

所以，`RocketMQ` 中的 **主题模型** 到底是如何实现的呢？

![](https://oss.javaguide.cn/github/javaguide/high-performance/message-queue/16ef383d3e8c9788.jpg)

我们可以看到在整个图中有 `Producer Group`、`Topic`、`Consumer Group` 三个角色。

- `Producer Group` 生产者组：代表某一类的生产者，比如我们有多个秒杀系统作为生产者，这多个合在一起就是一个 `Producer Group` 生产者组，它们一般生产相同的消息。
- `Consumer Group` 消费者组：代表某一类的消费者，比如我们有多个短信系统作为消费者，这多个合在一起就是一个 `Consumer Group` 消费者组，它们一般消费相同的消息。
- `Topic` 主题：代表一类消息，比如订单消息，物流消息等等。

你可以看到图中生产者组中的生产者会向主题发送消息，而 **主题中存在多个队列**，生产者每次生产消息之后是指定主题中的某个队列发送消息的。

每个主题中都有多个队列(分布在不同的 `Broker`中，如果是集群的话，`Broker`又分布在不同的服务器中)，集群消费模式下，一个消费者集群多台机器共同消费一个 `topic` 的多个队列，**一个队列只会被一个消费者消费**。如果某个消费者挂掉，分组内其它消费者会接替挂掉的消费者继续消费。就像上图中 `Consumer1` 和 `Consumer2` 分别对应着两个队列，而 `Consumer3` 是没有队列对应的，所以一般来讲要控制 **消费者组中的消费者个数和主题中队列个数相同** 。

当然也可以消费者个数小于队列个数，只不过不太建议。如下图。

![](https://oss.javaguide.cn/github/javaguide/high-performance/message-queue/16ef3850c808d707.jpg)

**每个消费组在每个队列上维护一个消费位置** ，为什么呢？

因为我们刚刚画的仅仅是一个消费者组，我们知道在发布订阅模式中一般会涉及到多个消费者组，而每个消费者组在每个队列中的消费位置都是不同的。如果此时有多个消费者组，那么消息被一个消费者组消费完之后是不会删除的(因为其它消费者组也需要呀)，它仅仅是为每个消费者组维护一个 **消费位移(offset)** ，每次消费者组消费完会返回一个成功的响应，然后队列再把维护的消费位移加一，这样就不会出现刚刚消费过的消息再一次被消费了。

![](https://oss.javaguide.cn/github/javaguide/high-performance/message-queue/16ef3857fefaa079.jpg)

可能你还有一个问题，**为什么一个主题中需要维护多个队列** ？

答案是 **提高并发能力** 。的确，每个主题中只存在一个队列也是可行的。你想一下，如果每个主题中只存在一个队列，这个队列中也维护着每个消费者组的消费位置，这样也可以做到 **发布订阅模式** 。如下图。

![](https://oss.javaguide.cn/github/javaguide/high-performance/message-queue/16ef38600cdb6d4b.jpg)

但是，这样我生产者是不是只能向一个队列发送消息？又因为需要维护消费位置所以一个队列只能对应一个消费者组中的消费者，这样是不是其他的 `Consumer` 就没有用武之地了？从这两个角度来讲，并发度一下子就小了很多。

所以总结来说，RocketMQ 通过**使用在一个 `Topic` 中配置多个队列并且每个队列维护每个消费者组的消费位置** 实现了 **主题模式/发布订阅模式** 。

## RocketMQ 的架构图
讲完了消息模型，我们理解起 RocketMQ 的技术架构起来就容易多了。

RocketMQ 技术架构中有四大角色 `NameServer`、`Broker`、`Producer`、`Consumer` 。

- `Broker`：主要负责消息的存储、投递和查询以及服务高可用保证。说白了就是消息队列服务器嘛，生产者生产消息到 `Broker` ，消费者从 `Broker` 拉取消息并消费。

`Broker`、`Topic` 和 队列的关系。一个 `Topic` 中存在多个队列，那么这个 `Topic` 和队列存放在哪呢？ **一个 `Topic` 分布在多个 `Broker`上，一个 `Broker` 可以配置多个 `Topic` ，它们是多对多的关系**。如果某个 `Topic` 消息量很大，应该给它多配置几个队列(上文中提到了提高并发能力)，并且 **尽量多分布在不同 `Broker` 上，以减轻某个 `Broker` 的压力** 。`Topic` 消息量都比较均匀的情况下，如果某个 `broker` 上的队列越多，则该 `broker` 压力越大。

![](https://oss.javaguide.cn/github/javaguide/high-performance/message-queue/16ef38687488a5a4.jpg)

所以说我们需要配置多个 Broker。

- `NameServer`：不知道你们有没有接触过 `ZooKeeper` 和 `Spring Cloud` 中的 `Eureka` ，它其实也是一个 **注册中心** ，主要提供两个功能：**Broker 管理** 和 **路由信息管理** 。说白了就是 `Broker` 会将自己的信息注册到 `NameServer` 中，此时 `NameServer` 就存放了很多 `Broker` 的信息(Broker 的路由表)，消费者和生产者就从 `NameServer` 中获取路由表然后照着路由表的信息和对应的 `Broker` 进行通信(生产者和消费者定期会向 `NameServer` 去查询相关的 `Broker` 的信息)。

- `Producer`：消息发布的角色，支持分布式集群方式部署。说白了就是生产者。

- `Consumer`：消息消费的角色，支持分布式集群方式部署。支持以 push 推，pull 拉两种模式对消息进行消费。同时也支持集群方式和广播方式的消费，它提供实时消息订阅机制。说白了就是消费者。

![](https://oss.javaguide.cn/github/javaguide/high-performance/message-queue/16ef386c6d1e8bdb.jpg)

`Broker` 是需要保证高可用的，如果整个系统仅仅靠着一个 `Broker` 来维持的话，那么这个 `Broker` 的压力会不会很大？所以我们需要使用多个 `Broker` 来保证 **负载均衡** 。消费者和生产者直接和多个 `Broker` 相连，那么当 `Broker` 修改的时候必定会牵连着每个生产者和消费者，这样就会产生耦合问题，而 `NameServer` 注册中心就是用来解决这个问题的。

当然，`RocketMQ` 中的技术架构肯定不止前面那么简单，因为上面图中的四个角色都是需要做集群的。我给出一张官网的架构图，大家尝试理解一下。

![](https://oss.javaguide.cn/github/javaguide/high-performance/message-queue/16ef386fa3be1e53.jpg)

其实和我们最开始画的那张乞丐版的架构图也没什么区别，主要是一些细节上的差别。听我细细道来 🤨。

第一、我们的 `Broker` **做了集群并且还进行了主从部署** ，由于消息分布在各个 `Broker` 上，一旦某个 `Broker` 宕机，则该`Broker` 上的消息读写都会受到影响。所以 `Rocketmq` 提供了 `master/slave` 的结构，`salve` 定时从 `master` 同步数据(同步刷盘或者异步刷盘)，如果 `master` 宕机，**则 `slave` 提供消费服务，但是不能写入消息** (后面我还会提到哦)。

第二、为了保证 `HA` ，我们的 `NameServer` 也做了集群部署，但是请注意它是 **去中心化** 的。也就意味着它没有主节点，你可以很明显地看出 `NameServer` 的所有节点是没有进行 `Info Replicate` 的，在 `RocketMQ` 中是通过 **单个 Broker 和所有 NameServer 保持长连接** ，并且在每隔 30 秒 `Broker` 会向所有 `Nameserver` 发送心跳，心跳包含了自身的 `Topic` 配置信息，这个步骤就对应这上面的 `Routing Info` 。

第三、在生产者需要向 `Broker` 发送消息的时候，**需要先从 `NameServer` 获取关于 `Broker` 的路由信息**，然后通过 **轮询** 的方法去向每个队列中生产数据以达到 **负载均衡** 的效果。

第四、消费者通过 `NameServer` 获取所有 `Broker` 的路由信息后，向 `Broker` 发送 `Pull` 请求来获取消息数据。`Consumer` 可以以两种模式启动—— **广播（Broadcast）和集群（Cluster）**。广播模式下，一条消息会发送给 **同一个消费组中的所有消费者** ，集群模式下消息只会发送给一个消费者。

## RocketMQ 功能特性

### 消息

#### 普通消息

普通消息一般应用于微服务解耦、事件驱动、数据集成等场景，这些场景大多数要求数据传输通道具有可靠传输的能力，且对消息的处理时机、处理顺序没有特别要求。以在线的电商交易场景为例，上游订单系统将用户下单支付这一业务事件封装成独立的普通消息并发送至 RocketMQ 服务端，下游按需从服务端订阅消息并按照本地消费逻辑处理下游任务。每个消息之间都是相互独立的，且不需要产生关联。另外还有日志系统，以离线的日志收集场景为例，通过埋点组件收集前端应用的相关操作日志，并转发到 RocketMQ 。

![](https://rocketmq.apache.org/zh/assets/images/lifecyclefornormal-e8a2a7e42a0722f681eb129b51e1bd66.png)

**普通消息生命周期**

- 初始化：消息被生产者构建并完成初始化，待发送到服务端的状态。
- 待消费：消息被发送到服务端，对消费者可见，等待消费者消费的状态。
- 消费中：消息被消费者获取，并按照消费者本地的业务逻辑进行处理的过程。 此时服务端会等待消费者完成消费并提交消费结果，如果一定时间后没有收到消费者的响应，RocketMQ 会对消息进行重试处理。
- 消费提交：消费者完成消费处理，并向服务端提交消费结果，服务端标记当前消息已经被处理（包括消费成功和失败）。RocketMQ 默认支持保留所有消息，此时消息数据并不会立即被删除，只是逻辑标记已消费。消息在保存时间到期或存储空间不足被删除前，消费者仍然可以回溯消息重新消费。
- 消息删除：RocketMQ 按照消息保存机制滚动清理最早的消息数据，将消息从物理文件中删除。

#### 定时消息

在分布式定时调度触发、任务超时处理等场景，需要实现精准、可靠的定时事件触发。使用 RocketMQ 的定时消息可以简化定时调度任务的开发逻辑，实现高性能、可扩展、高可靠的定时触发能力。定时消息仅支持在 MessageType 为 Delay 的主题内使用，即定时消息只能发送至类型为定时消息的主题中，发送的消息的类型必须和主题的类型一致。在 4.x 版本中，只支持延时消息，默认分为 18 个等级分别为：1s 5s 10s 30s 1m 2m 3m 4m 5m 6m 7m 8m 9m 10m 20m 30m 1h 2h，也可以在配置文件中增加自定义的延时等级和时长。在 5.x 版本中，开始支持定时消息，在构造消息时提供了 3 个 API 来指定延迟时间或定时时间。

基于定时消息的超时任务处理具备如下优势：

- **精度高、开发门槛低**：基于消息通知方式不存在定时阶梯间隔。可以轻松实现任意精度事件触发，无需业务去重。
- **高性能可扩展**：传统的数据库扫描方式较为复杂，需要频繁调用接口扫描，容易产生性能瓶颈。RocketMQ 的定时消息具有高并发和水平扩展的能力。

![](https://rocketmq.apache.org/zh/assets/images/lifecyclefordelay-2ce8278df69cd026dd11ffd27ab09a17.png)

**定时消息生命周期**

- 初始化：消息被生产者构建并完成初始化，待发送到服务端的状态。
- 定时中：消息被发送到服务端，和普通消息不同的是，服务端不会直接构建消息索引，而是会将定时消息**单独存储在定时存储系统中**，等待定时时刻到达。
- 待消费：定时时刻到达后，服务端将消息重新写入普通存储引擎，对下游消费者可见，等待消费者消费的状态。
- 消费中：消息被消费者获取，并按照消费者本地的业务逻辑进行处理的过程。 此时服务端会等待消费者完成消费并提交消费结果，如果一定时间后没有收到消费者的响应，RocketMQ 会对消息进行重试处理。
- 消费提交：消费者完成消费处理，并向服务端提交消费结果，服务端标记当前消息已经被处理（包括消费成功和失败）。RocketMQ 默认支持保留所有消息，此时消息数据并不会立即被删除，只是逻辑标记已消费。消息在保存时间到期或存储空间不足被删除前，消费者仍然可以回溯消息重新消费。
- 消息删除：Apache RocketMQ 按照消息保存机制滚动清理最早的消息数据，将消息从物理文件中删除。

定时消息的实现逻辑需要先经过定时存储等待触发，定时时间到达后才会被投递给消费者。因此，如果将大量定时消息的定时时间设置为同一时刻，则到达该时刻后会有大量消息同时需要被处理，会造成系统压力过大，导致消息分发延迟，影响定时精度。

#### 顺序消息

顺序消息仅支持使用 MessageType 为 FIFO 的主题，即顺序消息只能发送至类型为顺序消息的主题中，发送的消息的类型必须和主题的类型一致。和普通消息发送相比，顺序消息发送必须要设置消息组。（推荐实现 MessageQueueSelector 的方式，见下文）。要保证消息的顺序性需要单一生产者串行发送。

单线程使用 MessageListenerConcurrently 可以顺序消费，多线程环境下使用 MessageListenerOrderly 才能顺序消费。

#### 事务消息

事务消息是 Apache RocketMQ 提供的一种高级消息类型，支持在分布式场景下保障消息生产和本地事务的最终一致性。简单来讲，就是将本地事务（数据库的 DML 操作）与发送消息合并在同一个事务中。例如，新增一个订单。在事务未提交之前，不发送订阅的消息。发送消息的动作随着事务的成功提交而发送，随着事务的回滚而取消。当然真正地处理过程不止这么简单，包含了半消息、事务监听和事务回查等概念，下面有更详细的说明。

## 关于发送消息

### **不建议单一进程创建大量生产者**

Apache RocketMQ 的生产者和主题是多对多的关系，支持同一个生产者向多个主题发送消息。对于生产者的创建和初始化，建议遵循够用即可、最大化复用原则，如果有需要发送消息到多个主题的场景，无需为每个主题都创建一个生产者。

### **不建议频繁创建和销毁生产者**

Apache RocketMQ 的生产者是可以重复利用的底层资源，类似数据库的连接池。因此不需要在每次发送消息时动态创建生产者，且在发送结束后销毁生产者。这样频繁的创建销毁会在服务端产生大量短连接请求，严重影响系统性能。

正确示例：

```java
Producer p = ProducerBuilder.build();
for (int i =0;i<n;i++){
    Message m= MessageBuilder.build();
    p.send(m);
 }
p.shutdown();
```

## 消费者分类

### PushConsumer

高度封装的消费者类型，消费消息仅仅通过消费监听器监听并返回结果。消息的获取、消费状态提交以及消费重试都通过 RocketMQ 的客户端 SDK 完成。

PushConsumer 的消费监听器执行结果分为以下三种情况：

- 返回消费成功：以 Java SDK 为例，返回`ConsumeResult.SUCCESS`，表示该消息处理成功，服务端按照消费结果更新消费进度。
- 返回消费失败：以 Java SDK 为例，返回`ConsumeResult.FAILURE`，表示该消息处理失败，需要根据消费重试逻辑判断是否进行重试消费。
- 出现非预期失败：例如抛异常等行为，该结果按照消费失败处理，需要根据消费重试逻辑判断是否进行重试消费。

具体实现可以参见这篇文章[RocketMQ 对 pull 和 push 的实现](http://devedmc.com/archives/1691854198138)。

使用 PushConsumer 消费者消费时，不允许使用以下方式处理消息，否则 RocketMQ 无法保证消息的可靠性。

- 错误方式一：消息还未处理完成，就提前返回消费成功结果。此时如果消息消费失败，RocketMQ 服务端是无法感知的，因此不会进行消费重试。
- 错误方式二：在消费监听器内将消息再次分发到自定义的其他线程，消费监听器提前返回消费结果。此时如果消息消费失败，RocketMQ 服务端同样无法感知，因此也不会进行消费重试。
- PushConsumer 严格限制了消息同步处理及每条消息的处理超时时间，适用于以下场景：
  - 消息处理时间可预估：如果不确定消息处理耗时，经常有预期之外的长时间耗时的消息，PushConsumer 的可靠性保证会频繁触发消息重试机制造成大量重复消息。
  - 无异步化、高级定制场景：PushConsumer 限制了消费逻辑的线程模型，由客户端 SDK 内部按最大吞吐量触发消息处理。该模型开发逻辑简单，但是不允许使用异步化和自定义处理流程。

### SimpleConsumer

SimpleConsumer 是一种接口原子型的消费者类型，消息的获取、消费状态提交以及消费重试都是通过消费者业务逻辑主动发起调用完成。

一个来自官网的例子：

```java
// 消费示例：使用 SimpleConsumer 消费普通消息，主动获取消息处理并提交。
ClientServiceProvider provider = ClientServiceProvider.loadService();
String topic = "YourTopic";
FilterExpression filterExpression = new FilterExpression("YourFilterTag", FilterExpressionType.TAG);
SimpleConsumer simpleConsumer = provider.newSimpleConsumerBuilder()
        // 设置消费者分组。
        .setConsumerGroup("YourConsumerGroup")
        // 设置接入点。
        .setClientConfiguration(ClientConfiguration.newBuilder().setEndpoints("YourEndpoint").build())
        // 设置预绑定的订阅关系。
        .setSubscriptionExpressions(Collections.singletonMap(topic, filterExpression))
        // 设置从服务端接受消息的最大等待时间
        .setAwaitDuration(Duration.ofSeconds(1))
        .build();
try {
    // SimpleConsumer 需要主动获取消息，并处理。
    List<MessageView> messageViewList = simpleConsumer.receive(10, Duration.ofSeconds(30));
    messageViewList.forEach(messageView -> {
        System.out.println(messageView);
        // 消费处理完成后，需要主动调用 ACK 提交消费结果。
        try {
            simpleConsumer.ack(messageView);
        } catch (ClientException e) {
            logger.error("Failed to ack message, messageId={}", messageView.getMessageId(), e);
        }
    });
} catch (ClientException e) {
    // 如果遇到系统流控等原因造成拉取失败，需要重新发起获取消息请求。
    logger.error("Failed to receive message", e);
}
```

SimpleConsumer 适用于以下场景：

- 消息处理时长不可控：如果消息处理时长无法预估，经常有长时间耗时的消息处理情况。建议使用 SimpleConsumer 消费类型，可以在消费时自定义消息的预估处理时长，若实际业务中预估的消息处理时长不符合预期，也可以通过接口提前修改。
- 需要异步化、批量消费等高级定制场景：SimpleConsumer 在 SDK 内部没有复杂的线程封装，完全由业务逻辑自由定制，可以实现异步分发、批量消费等高级定制场景。
- 需要自定义消费速率：SimpleConsumer 是由业务逻辑主动调用接口获取消息，因此可以自由调整获取消息的频率，自定义控制消费速率。

### PullConsumer

TBD 。。。


## 消费者分组和生产者分组

### 生产者分组

RocketMQ 服务端 5.x 版本开始，**生产者是匿名的**，无需管理生产者分组（ProducerGroup）；对于历史版本服务端 3.x 和 4.x 版本，已经使用的生产者分组可以废弃无需再设置，且不会对当前业务产生影响。

### 消费者分组

消费者分组是多个消费行为一致的消费者的负载均衡分组。消费者分组不是具体实体而是一个逻辑资源。通过消费者分组实现消费性能的水平扩展以及高可用容灾。

消费者分组中的订阅关系、投递顺序性、消费重试策略是一致的。

- 订阅关系：Apache RocketMQ 以消费者分组的粒度管理订阅关系，实现订阅关系的管理和追溯。
- 投递顺序性：Apache RocketMQ 的服务端将消息投递给消费者消费时，支持顺序投递和并发投递，投递方式在消费者分组中统一配置。
- 消费重试策略： 消费者消费消息失败时的重试策略，包括重试次数、死信队列设置等。

RocketMQ 服务端 5.x 版本：上述消费者的消费行为从关联的消费者分组中统一获取，因此，同一分组内所有消费者的消费行为必然是一致的，客户端无需关注。

RocketMQ 服务端 3.x/4.x 历史版本：上述消费逻辑由消费者客户端接口定义，因此，您需要自己在消费者客户端设置时保证同一分组下的消费者的消费行为一致。(来自官方网站)

## 如何解决顺序消费和重复消费？

### 顺序消费

在上面的技术架构介绍中，我们已经知道了 **`RocketMQ` 在主题上是无序的、它只有在队列层面才是保证有序** 的。

这又扯到两个概念——**普通顺序** 和 **严格顺序** 。

所谓普通顺序是指 消费者通过 **同一个消费队列收到的消息是有顺序的** ，不同消息队列收到的消息则可能是无顺序的。普通顺序消息在 `Broker` **重启情况下不会保证消息顺序性** (短暂时间) 。

所谓严格顺序是指 消费者收到的 **所有消息** 均是有顺序的。严格顺序消息 **即使在异常情况下也会保证消息的顺序性** 。

但是，严格顺序看起来虽好，实现它可会付出巨大的代价。如果你使用严格顺序模式，`Broker` 集群中只要有一台机器不可用，则整个集群都不可用。你还用啥？现在主要场景也就在 `binlog` 同步。

一般而言，我们的 `MQ` 都是能容忍短暂的乱序，所以推荐使用普通顺序模式。

那么，我们现在使用了 **普通顺序模式** ，我们从上面学习知道了在 `Producer` 生产消息的时候会进行轮询(取决你的负载均衡策略)来向同一主题的不同消息队列发送消息。那么如果此时我有几个消息分别是同一个订单的创建、支付、发货，在轮询的策略下这 **三个消息会被发送到不同队列** ，因为在不同的队列此时就无法使用 `RocketMQ` 带来的队列有序特性来保证消息有序性了。

![](https://oss.javaguide.cn/github/javaguide/high-performance/message-queue/16ef3874585e096e.jpg)

那么，怎么解决呢？

其实很简单，我们需要处理的仅仅是将同一语义下的消息放入同一个队列(比如这里是同一个订单)，那我们就可以使用 **Hash 取模法** 来保证同一个订单在同一个队列中就行了。

RocketMQ 实现了两种队列选择算法，也可以自己实现

- 轮询算法

  - 轮询算法就是向消息指定的 topic 所在队列中依次发送消息，保证消息均匀分布
  - 是 RocketMQ 默认队列选择算法

- 最小投递延迟算法

  - 每次消息投递的时候统计消息投递的延迟，选择队列时优先选择消息延时小的队列。


### 特殊情况处理

#### 发送异常

选择队列后会与 Broker 建立连接，通过网络请求将消息发送到 Broker 上，如果 Broker 挂了或者网络波动发送消息超时此时 RocketMQ 会进行重试。

重新选择其他 Broker 中的消息队列进行发送，默认重试两次，可以手动设置。

```java
producer.setRetryTimesWhenSendFailed(5);
```

#### 消息过大

消息超过 4k 时 RocketMQ 会将消息压缩后在发送到 Broker 上，减少网络资源的占用。

### 重复消费

 **幂等** 。在编程中一个幂等 操作的特点是其任意多次执行所产生的影响均与一次执行的影响相同。比如说，这个时候我们有一个订单的处理积分的系统，每当来一个消息的时候它就负责为创建这个订单的用户的积分加上相应的数值。可是有一次，消息队列发送给订单系统 FrancisQ 的订单信息，其要求是给 FrancisQ 的积分加上 500。但是积分系统在收到 FrancisQ 的订单信息处理完成之后返回给消息队列处理成功的信息的时候出现了网络波动(当然还有很多种情况，比如 Broker 意外重启等等)，这条回应没有发送成功。

那么，消息队列没收到积分系统的回应会不会尝试重发这个消息？问题就来了，我再发这个消息，万一它又给 FrancisQ 的账户加上 500 积分怎么办呢？

所以我们需要给我们的消费者实现 **幂等** ，也就是对同一个消息的处理结果，执行多少次都不变。

那么如何给业务实现幂等呢？这个还是需要结合具体的业务的。你可以使用 **写入 `Redis`** 来保证，因为 `Redis` 的 `key` 和 `value` 就是天然支持幂等的。当然还有使用 **数据库插入法** ，基于数据库的唯一键来保证重复数据不会被插入多条。

不过最主要的还是需要 **根据特定场景使用特定的解决方案** ，你要知道你的消息消费是否是完全不可重复消费还是可以忍受重复消费的，然后再选择强校验和弱校验的方式。毕竟在 CS 领域还是很少有技术银弹的说法。

而在整个互联网领域，幂等不仅仅适用于消息队列的重复消费问题，这些实现幂等的方法，也同样适用于，**在其他场景中来解决重复请求或者重复调用的问题** 。比如将 HTTP 服务设计成幂等的，**解决前端或者 APP 重复提交表单数据的问题** ，也可以将一个微服务设计成幂等的，解决 `RPC` 框架自动重试导致的 **重复调用问题** 。

## RocketMQ 如何实现分布式事务？

如何解释分布式事务呢？事务大家都知道吧？**要么都执行要么都不执行** 。在同一个系统中我们可以轻松地实现事务，但是在分布式架构中，我们有很多服务是部署在不同系统之间的，而不同服务之间又需要进行调用。比如此时我下订单然后增加积分，如果保证不了分布式事务的话，就会出现 A 系统下了订单，但是 B 系统增加积分失败或者 A 系统没有下订单，B 系统却增加了积分。前者对用户不友好，后者对运营商不利，这是我们都不愿意见到的。

那么，如何去解决这个问题呢？

如今比较常见的分布式事务实现有 2PC、TCC 和事务消息(half 半消息机制)。每一种实现都有其特定的使用场景，但是也有各自的问题，**都不是完美的解决方案**。

在 `RocketMQ` 中使用的是 **事务消息加上事务反查机制** 来解决分布式事务问题的。我画了张图，大家可以对照着图进行理解。

![](https://oss.javaguide.cn/github/javaguide/high-performance/message-queue/16ef38798d7a987f.png)

在第一步发送的 half 消息 ，它的意思是 **在事务提交之前，对于消费者来说，这个消息是不可见的** 。

> 那么，如何做到写入消息但是对用户不可见呢？RocketMQ 事务消息的做法是：如果消息是 half 消息，将备份原消息的主题与消息消费队列，然后 **改变主题** 为 RMQ_SYS_TRANS_HALF_TOPIC。由于消费组未订阅该主题，故消费端无法消费 half 类型的消息，**然后 RocketMQ 会开启一个定时任务，从 Topic 为 RMQ_SYS_TRANS_HALF_TOPIC 中拉取消息进行消费**，根据生产者组获取一个服务提供者发送回查事务状态请求，根据事务状态来决定是提交或回滚消息。

你可以试想一下，如果没有从第 5 步开始的 **事务反查机制** ，如果出现网路波动第 4 步没有发送成功，这样就会产生 MQ 不知道是不是需要给消费者消费的问题，他就像一个无头苍蝇一样。在 `RocketMQ` 中就是使用的上述的事务反查来解决的，而在 `Kafka` 中通常是直接抛出一个异常让用户来自行解决。

你还需要注意的是，在 `MQ Server` 指向系统 B 的操作已经和系统 A 不相关了，也就是说在消息队列中的分布式事务是——**本地事务和存储消息到消息队列才是同一个事务**。这样也就产生了事务的**最终一致性**，因为整个过程是异步的，**每个系统只要保证它自己那一部分的事务就行了**。

实践中会遇到的问题：事务消息需要一个事务监听器来监听本地事务是否成功，并且事务监听器接口只允许被实现一次。那就意味着需要把各种事务消息的本地事务都写在一个接口方法里面，必将会产生大量的耦合和类型判断。采用函数 Function 接口来包装整个业务过程，作为一个参数传递到监听器的接口方法中。再调用 Function 的 apply() 方法来执行业务，事务也会在 apply() 方法中执行。让监听器与业务之间实现解耦，使之具备了真实生产环境中的可行性。

1.模拟一个添加用户浏览记录的需求

```java
@PostMapping("/add")
@ApiOperation("添加用户浏览记录")
public Result<TransactionSendResult> add(Long userId, Long forecastLogId) {

        // 函数式编程:浏览记录入库
        Function<String, Boolean> function = transactionId -> viewHistoryHandler.addViewHistory(transactionId, userId, forecastLogId);

        Map<String, Long> hashMap = new HashMap<>();
        hashMap.put("userId", userId);
        hashMap.put("forecastLogId", forecastLogId);
        String jsonString = JSON.toJSONString(hashMap);

        // 发送事务消息;将本地的事务操作,用函数Function接口接收,作为一个参数传入到方法中
        TransactionSendResult transactionSendResult = mqProducerService.sendTransactionMessage(jsonString, MQDestination.TAG_ADD_VIEW_HISTORY, function);
        return Result.success(transactionSendResult);
}
```

2.发送事务消息的方法

```java
/**
 * 发送事务消息
 *
 * @param msgBody
 * @param tag
 * @param function
 * @return
 */
public TransactionSendResult sendTransactionMessage(String msgBody, String tag, Function<String, Boolean> function) {
    // 构建消息体
    Message<String> message = buildMessage(msgBody);

    // 构建消息投递信息
    String destination = buildDestination(tag);

    TransactionSendResult result = rocketMQTemplate.sendMessageInTransaction(destination, message, function);
    return result;
}
```

3.生产者消息监听器,只允许一个类去实现该监听器

```java
@Slf4j
@RocketMQTransactionListener
public class TransactionMsgListener implements RocketMQLocalTransactionListener {

    @Autowired
    private RedisService redisService;

    /**
     * 执行本地事务（在发送消息成功时执行）
     *
     * @param message
     * @param o
     * @return commit or rollback or unknown
     */
    @Override
    public RocketMQLocalTransactionState executeLocalTransaction(Message message, Object o) {

        // 1、获取事务ID
        String transactionId = null;
        try {
            transactionId = message.getHeaders().get("rocketmq_TRANSACTION_ID").toString();
            // 2、判断传入函数对象是否为空，如果为空代表没有要执行的业务直接抛弃消息
            if (o == null) {
                //返回ROLLBACK状态的消息会被丢弃
                log.info("事务消息回滚，没有需要处理的业务 transactionId={}", transactionId);
                return RocketMQLocalTransactionState.ROLLBACK;
            }
            // 将Object o转换成Function对象
            Function<String, Boolean> function = (Function<String, Boolean>) o;
            // 执行业务 事务也会在function.apply中执行
            Boolean apply = function.apply(transactionId);
            if (apply) {
                log.info("事务提交，消息正常处理 transactionId={}", transactionId);
                //返回COMMIT状态的消息会立即被消费者消费到
                return RocketMQLocalTransactionState.COMMIT;
            }
        } catch (Exception e) {
            log.info("出现异常 返回ROLLBACK transactionId={}", transactionId);
            return RocketMQLocalTransactionState.ROLLBACK;
        }
        return RocketMQLocalTransactionState.ROLLBACK;
    }

    /**
     * 事务回查机制，检查本地事务的状态
     *
     * @param message
     * @return
     */
    @Override
    public RocketMQLocalTransactionState checkLocalTransaction(Message message) {

        String transactionId = message.getHeaders().get("rocketmq_TRANSACTION_ID").toString();

        // 查redis
        MqTransaction mqTransaction = redisService.getCacheObject("mqTransaction:" + transactionId);
        if (Objects.isNull(mqTransaction)) {
            return RocketMQLocalTransactionState.ROLLBACK;
        }
        return RocketMQLocalTransactionState.COMMIT;
    }
}
```

4.模拟的业务场景,这里的方法必须提取出来,放在别的类里面.如果调用方与被调用方在同一个类中,会发生事务失效的问题.

```java
@Component
public class ViewHistoryHandler {

    @Autowired
    private IViewHistoryService viewHistoryService;

    @Autowired
    private IMqTransactionService mqTransactionService;

    @Autowired
    private RedisService redisService;

    /**
     * 浏览记录入库
     *
     * @param transactionId
     * @param userId
     * @param forecastLogId
     * @return
     */
    @Transactional
    public Boolean addViewHistory(String transactionId, Long userId, Long forecastLogId) {
        // 构建浏览记录
        ViewHistory viewHistory = new ViewHistory();
        viewHistory.setUserId(userId);
        viewHistory.setForecastLogId(forecastLogId);
        viewHistory.setCreateTime(LocalDateTime.now());
        boolean save = viewHistoryService.save(viewHistory);

        // 本地事务信息
        MqTransaction mqTransaction = new MqTransaction();
        mqTransaction.setTransactionId(transactionId);
        mqTransaction.setCreateTime(new Date());
        mqTransaction.setStatus(MqTransaction.StatusEnum.VALID.getStatus());

        // 1.可以把事务信息存数据库
        mqTransactionService.save(mqTransaction);

        // 2.也可以选择存redis,4个小时有效期,'4个小时'是RocketMQ内置的最大回查超时时长,过期未确认将强制回滚
        redisService.setCacheObject("mqTransaction:" + transactionId, mqTransaction, 4L, TimeUnit.HOURS);

        // 放开注释,模拟异常,事务回滚
        // int i = 10 / 0;

        return save;
    }
}
```

5.消费消息,以及幂等处理

```java
@Service
@RocketMQMessageListener(topic = MQDestination.TOPIC, selectorExpression = MQDestination.TAG_ADD_VIEW_HISTORY, consumerGroup = MQDestination.TAG_ADD_VIEW_HISTORY)
public class ConsumerAddViewHistory implements RocketMQListener<Message> {
    // 监听到消息就会执行此方法
    @Override
    public void onMessage(Message message) {
        // 幂等校验
        String transactionId = message.getTransactionId();

        // 查redis
        MqTransaction mqTransaction = redisService.getCacheObject("mqTransaction:" + transactionId);

        // 不存在事务记录
        if (Objects.isNull(mqTransaction)) {
            return;
        }

        // 已消费
        if (Objects.equals(mqTransaction.getStatus(), MqTransaction.StatusEnum.CONSUMED.getStatus())) {
            return;
        }

        String msg = new String(message.getBody());
        Map<String, Long> map = JSON.parseObject(msg, new TypeReference<HashMap<String, Long>>() {
        });
        Long userId = map.get("userId");
        Long forecastLogId = map.get("forecastLogId");

        // 下游的业务处理
        // TODO 记录用户喜好,更新用户画像

        // TODO 更新'证券预测文章'的浏览量,重新计算文章的曝光排序

        // 更新状态为已消费
        mqTransaction.setUpdateTime(new Date());
        mqTransaction.setStatus(MqTransaction.StatusEnum.CONSUMED.getStatus());
        redisService.setCacheObject("mqTransaction:" + transactionId, mqTransaction, 4L, TimeUnit.HOURS);
        log.info("监听到消息：msg={}", JSON.toJSONString(map));
    }
}
```

## 如何解决消息堆积问题？

在上面我们提到了消息队列一个很重要的功能——**削峰** 。那么如果这个峰值太大了导致消息堆积在队列中怎么办呢？

其实这个问题可以将它广义化，因为产生消息堆积的根源其实就只有两个——生产者生产太快或者消费者消费太慢。

我们可以从多个角度去思考解决这个问题，当流量到峰值的时候是因为生产者生产太快，我们可以使用一些 **限流降级** 的方法，当然你也可以增加多个消费者实例去水平扩展增加消费能力来匹配生产的激增。如果消费者消费过慢的话，我们可以先检查 **是否是消费者出现了大量的消费错误** ，或者打印一下日志查看是否是哪一个线程卡死，出现了锁资源不释放等等的问题。

当然，最快速解决消息堆积问题的方法还是增加消费者实例，不过 **同时你还需要增加每个主题的队列数量** 。在 `RocketMQ` 中，**一个队列只会被一个消费者消费** 

## 什么是回溯消费？

回溯消费是指 `Consumer` 已经消费成功的消息，由于业务上需求需要重新消费，在`RocketMQ` 中， `Broker` 在向`Consumer` 投递成功消息后，**消息仍然需要保留** 。并且重新消费一般是按照时间维度，例如由于 `Consumer` 系统故障，恢复后需要重新消费 1 小时前的数据，那么 `Broker` 要提供一种机制，可以按照时间维度来回退消费进度。`RocketMQ` 支持按照时间回溯消费，时间维度精确到毫秒。

这是官方文档的解释，我直接照搬过来就当科普了 😁😁😁。

## RocketMQ 如何保证高性能读写

### 传统 IO 方式

![](https://oss.javaguide.cn/github/javaguide/high-performance/message-queue/31699457085_.pic.jpg)

传统的 IO 读写其实就是 read + write 的操作，整个过程会分为如下几步

- 用户调用 read()方法，开始读取数据，此时发生一次上下文从用户态到内核态的切换，也就是图示的切换 1
- 将磁盘数据通过 DMA 拷贝到内核缓存区
- 将内核缓存区的数据拷贝到用户缓冲区，这样用户，也就是我们写的代码就能拿到文件的数据
- read()方法返回，此时就会从内核态切换到用户态，也就是图示的切换 2
- 当我们拿到数据之后，就可以调用 write()方法，此时上下文会从用户态切换到内核态，即图示切换 3
- CPU 将用户缓冲区的数据拷贝到 Socket 缓冲区
- 将 Socket 缓冲区数据拷贝至网卡
- write()方法返回，上下文重新从内核态切换到用户态，即图示切换 4

整个过程发生了 4 次上下文切换和 4 次数据的拷贝，这在高并发场景下肯定会严重影响读写性能故引入了零拷贝技术

### 零拷贝技术

#### mmap

mmap（memory map）是一种内存映射文件的方法，即将一个文件或者其它对象映射到进程的地址空间，实现文件磁盘地址和进程虚拟地址空间中一段虚拟地址的一一对映关系。

简单地说就是内核缓冲区和应用缓冲区共享，从而减少了从读缓冲区到用户缓冲区的一次 CPU 拷贝。基于此上述架构图可变为：

![](https://oss.javaguide.cn/github/javaguide/high-performance/message-queue/41699457086_.pic.jpg)

基于 mmap IO 读写其实就变成 mmap + write 的操作，也就是用 mmap 替代传统 IO 中的 read 操作。

当用户发起 mmap 调用的时候会发生上下文切换 1，进行内存映射，然后数据被拷贝到内核缓冲区，mmap 返回，发生上下文切换 2；随后用户调用 write，发生上下文切换 3，将内核缓冲区的数据拷贝到 Socket 缓冲区，write 返回，发生上下文切换 4。

发生 4 次上下文切换和 3 次 IO 拷贝操作，在 Java 中的实现：

```java
FileChannel fileChannel = new RandomAccessFile("test.txt", "rw").getChannel();
MappedByteBuffer mappedByteBuffer = fileChannel.map(FileChannel.MapMode.READ_WRITE, 0, fileChannel.size());
```

#### sendfile

sendfile()跟 mmap()一样，也会减少一次 CPU 拷贝，但是它同时也会减少两次上下文切换。

![](https://oss.javaguide.cn/github/javaguide/high-performance/message-queue/51699457087_.pic.jpg)

如图，用户在发起 sendfile()调用时会发生切换 1，之后数据通过 DMA 拷贝到内核缓冲区，之后再将内核缓冲区的数据 CPU 拷贝到 Socket 缓冲区，最后拷贝到网卡，sendfile()返回，发生切换 2。发生了 3 次拷贝和两次切换。Java 也提供了相应 api：

```java
FileChannel channel = FileChannel.open(Paths.get("./test.txt"), StandardOpenOption.WRITE, StandardOpenOption.CREATE);
//调用transferTo方法向目标数据传输
channel.transferTo(position, len, target);
```

在如上代码中，并没有文件的读写操作，而是直接将文件的数据传输到 target 目标缓冲区，也就是说，sendfile 是无法知道文件的具体的数据的；但是 mmap 不一样，他是可以修改内核缓冲区的数据的。假设如果需要对文件的内容进行修改之后再传输，只有 mmap 可以满足。

通过上面的一些介绍，结论是基于零拷贝技术，可以减少 CPU 的拷贝次数和上下文切换次数，从而可以实现文件高效的读写操作。

RocketMQ 内部主要是使用基于 mmap 实现的零拷贝(其实就是调用上述提到的 api)，用来读写文件，这也是 RocketMQ 为什么快的一个很重要原因。

## RocketMQ 的刷盘机制

上面我讲了那么多的 `RocketMQ` 的架构和设计原理，你有没有好奇

在 `Topic` 中的 **队列是以什么样的形式存在的？**

**队列中的消息又是如何进行存储持久化的呢？**

我在上文中提到的 **同步刷盘** 和 **异步刷盘** 又是什么呢？它们会给持久化带来什么样的影响呢？

下面我将给你们一一解释。

### 同步刷盘和异步刷盘

![](https://oss.javaguide.cn/github/javaguide/high-performance/message-queue/16ef387fba311cda-20230814005009889.jpg)

如上图所示，在同步刷盘中需要等待一个刷盘成功的 `ACK` ，同步刷盘对 `MQ` 消息可靠性来说是一种不错的保障，但是 **性能上会有较大影响** ，一般地适用于金融等特定业务场景。

而异步刷盘往往是开启一个线程去异步地执行刷盘操作。消息刷盘采用后台异步线程提交的方式进行， **降低了读写延迟** ，提高了 `MQ` 的性能和吞吐量，一般适用于如发验证码等对于消息保证要求不太高的业务场景。

一般地，**异步刷盘只有在 `Broker` 意外宕机的时候会丢失部分数据**，你可以设置 `Broker` 的参数 `FlushDiskType` 来调整你的刷盘策略(ASYNC_FLUSH 或者 SYNC_FLUSH)。

### 同步复制和异步复制

上面的同步刷盘和异步刷盘是在单个结点层面的，而同步复制和异步复制主要是指的 `Borker` 主从模式下，主节点返回消息给客户端的时候是否需要同步从节点。

- 同步复制：也叫 “同步双写”，也就是说，**只有消息同步双写到主从节点上时才返回写入成功** 。
- 异步复制：**消息写入主节点之后就直接返回写入成功** 。

然而，很多事情是没有完美的方案的，就比如我们进行消息写入的节点越多就更能保证消息的可靠性，但是随之的性能也会下降，所以需要程序员根据特定业务场景去选择适应的主从复制方案。

那么，**异步复制会不会也像异步刷盘那样影响消息的可靠性呢？**

答案是不会的，因为两者就是不同的概念，对于消息可靠性是通过不同的刷盘策略保证的，而像异步同步复制策略仅仅是影响到了 **可用性** 。为什么呢？其主要原因**是 `RocketMQ` 是不支持自动主从切换的，当主节点挂掉之后，生产者就不能再给这个主节点生产消息了**。

比如这个时候采用异步复制的方式，在主节点还未发送完需要同步的消息的时候主节点挂掉了，这个时候从节点就少了一部分消息。但是此时生产者无法再给主节点生产消息了，**消费者可以自动切换到从节点进行消费**(仅仅是消费)，所以在主节点挂掉的时间只会产生主从结点短暂的消息不一致的情况，降低了可用性，而当主节点重启之后，从节点那部分未来得及复制的消息还会继续复制。

在单主从架构中，如果一个主节点挂掉了，那么也就意味着整个系统不能再生产了。那么这个可用性的问题能否解决呢？**一个主从不行那就多个主从的呗**，别忘了在我们最初的架构图中，每个 `Topic` 是分布在不同 `Broker` 中的。

![](https://oss.javaguide.cn/github/javaguide/high-performance/message-queue/16ef38687488a5asadasfg4.jpg)

但是这种复制方式同样也会带来一个问题，那就是无法保证 **严格顺序** 。在上文中我们提到了如何保证的消息顺序性是通过将一个语义的消息发送在同一个队列中，使用 `Topic` 下的队列来保证顺序性的。如果此时我们主节点 A 负责的是订单 A 的一系列语义消息，然后它挂了，这样其他节点是无法代替主节点 A 的，如果我们任意节点都可以存入任何消息，那就没有顺序性可言了。

而在 `RocketMQ` 中采用了 `Dledger` 解决这个问题。他要求在写入消息的时候，要求**至少消息复制到半数以上的节点之后**，才给客⼾端返回写⼊成功，并且它是⽀持通过选举来动态切换主节点的。这里我就不展开说明了，读者可以自己去了解。

> 也不是说 `Dledger` 是个完美的方案，至少在 `Dledger` 选举过程中是无法提供服务的，而且他必须要使用三个节点或以上，如果多数节点同时挂掉他也是无法保证可用性的，而且要求消息复制半数以上节点的效率和直接异步复制还是有一定的差距的。

### 存储机制

还记得上面我们一开始的三个问题吗？到这里第三个问题已经解决了。

但是，在 `Topic` 中的 **队列是以什么样的形式存在的？队列中的消息又是如何进行存储持久化的呢？** 还未解决，其实这里涉及到了 `RocketMQ` 是如何设计它的存储结构了。我首先想大家介绍 `RocketMQ` 消息存储架构中的三大角色——`CommitLog`、`ConsumeQueue` 和 `IndexFile` 。

- `CommitLog`：**消息主体以及元数据的存储主体**，存储 `Producer` 端写入的消息主体内容,消息内容不是定长的。单个文件大小默认 1G ，文件名长度为 20 位，左边补零，剩余为起始偏移量，比如 00000000000000000000 代表了第一个文件，起始偏移量为 0，文件大小为 1G=1073741824；当第一个文件写满了，第二个文件为 00000000001073741824，起始偏移量为 1073741824，以此类推。消息主要是**顺序写入日志文件**，当文件满了，写入下一个文件。
- `ConsumeQueue`：消息消费队列，**引入的目的主要是提高消息消费的性能**(我们再前面也讲了)，由于`RocketMQ` 是基于主题 `Topic` 的订阅模式，消息消费是针对主题进行的，如果要遍历 `commitlog` 文件中根据 `Topic` 检索消息是非常低效的。`Consumer` 即可根据 `ConsumeQueue` 来查找待消费的消息。其中，`ConsumeQueue`（逻辑消费队列）**作为消费消息的索引**，保存了指定 `Topic` 下的队列消息在 `CommitLog` 中的**起始物理偏移量 `offset` **，消息大小 `size` 和消息 `Tag` 的 `HashCode` 值。**`consumequeue` 文件可以看成是基于 `topic` 的 `commitlog` 索引文件**，故 `consumequeue` 文件夹的组织方式如下：topic/queue/file 三层组织结构，具体存储路径为：$HOME/store/consumequeue/{topic}/{queueId}/{fileName}。同样 `consumequeue` 文件采取定长设计，每一个条目共 20 个字节，分别为 8 字节的 `commitlog` 物理偏移量、4 字节的消息长度、8 字节 tag `hashcode`，单个文件由 30W 个条目组成，可以像数组一样随机访问每一个条目，每个 `ConsumeQueue`文件大小约 5.72M；
- `IndexFile`：`IndexFile`（索引文件）提供了一种可以通过 key 或时间区间来查询消息的方法。这里只做科普不做详细介绍。

总结来说，整个消息存储的结构，最主要的就是 `CommitLoq` 和 `ConsumeQueue` 。而 `ConsumeQueue` 你可以大概理解为 `Topic` 中的队列。

![](https://oss.javaguide.cn/github/javaguide/high-performance/message-queue/16ef3884c02acc72.png)

`RocketMQ` 采用的是 **混合型的存储结构** ，即为 `Broker` 单个实例下所有的队列共用一个日志数据文件来存储消息。有意思的是在同样高并发的 `Kafka` 中会为每个 `Topic` 分配一个存储文件。这就有点类似于我们有一大堆书需要装上书架，`RocketMQ` 是不分书的种类直接成批的塞上去的，而 `Kafka` 是将书本放入指定的分类区域的。

而 `RocketMQ` 为什么要这么做呢？原因是 **提高数据的写入效率** ，不分 `Topic` 意味着我们有更大的几率获取 **成批** 的消息进行数据写入，但也会带来一个麻烦就是读取消息的时候需要遍历整个大文件，这是非常耗时的。

所以，在 `RocketMQ` 中又使用了 `ConsumeQueue` 作为每个队列的索引文件来 **提升读取消息的效率**。我们可以直接根据队列的消息序号，计算出索引的全局位置（索引序号\*索引固定⻓度 20），然后直接读取这条索引，再根据索引中记录的消息的全局位置，找到消息。

讲到这里，你可能对 `RocketMQ` 的存储架构还有些模糊，没事，我们结合着图来理解一下。

![](https://oss.javaguide.cn/github/javaguide/high-performance/message-queue/16ef388763c25c62.jpg)

emmm，是不是有一点复杂 🤣，看英文图片和英文文档的时候就不要怂，硬着头皮往下看就行。

> 如果上面没看懂的读者一定要认真看下面的流程分析！

首先，在最上面的那一块就是我刚刚讲的你现在可以直接 **把 `ConsumerQueue` 理解为 `Queue`**。

在图中最左边说明了红色方块代表被写入的消息，虚线方块代表等待被写入的。左边的生产者发送消息会指定 `Topic`、`QueueId` 和具体消息内容，而在 `Broker` 中管你是哪门子消息，他直接 **全部顺序存储到了 CommitLog**。而根据生产者指定的 `Topic` 和 `QueueId` 将这条消息本身在 `CommitLog` 的偏移(offset)，消息本身大小，和 tag 的 hash 值存入对应的 `ConsumeQueue` 索引文件中。而在每个队列中都保存了 `ConsumeOffset` 即每个消费者组的消费位置(我在架构那里提到了，忘了的同学可以回去看一下)，而消费者拉取消息进行消费的时候只需要根据 `ConsumeOffset` 获取下一个未被消费的消息就行了。

上述就是我对于整个消息存储架构的大概理解(这里不涉及到一些细节讨论，比如稀疏索引等等问题)，希望对你有帮助。

因为有一个知识点因为写嗨了忘讲了，想想在哪里加也不好，所以我留给大家去思考 🤔🤔 一下吧。

为什么 `CommitLog` 文件要设计成固定大小的长度呢？提醒：**内存映射机制**。

## 总结

总算把这篇博客写完了。我讲的你们还记得吗 😅？

这篇文章中我主要想大家介绍了

1. 消息队列出现的原因
2. 消息队列的作用(异步，解耦，削峰)
3. 消息队列带来的一系列问题(消息堆积、重复消费、顺序消费、分布式事务等等)
4. 消息队列的两种消息模型——队列和主题模式
5. 分析了 `RocketMQ` 的技术架构(`NameServer`、`Broker`、`Producer`、`Consumer`)
6. 结合 `RocketMQ` 回答了消息队列副作用的解决方案
7. 介绍了 `RocketMQ` 的存储机制和刷盘策略。


## 面试题

**RocketMQ 特点**

- 是一个队列模型的消息中间件，具有高性能、高可靠、高实时、分布式等特点
- Producer、Consumer、队列都可以分布式
- Producer 向一些队列轮流发送消息，队列集合称为 Topic，Consumer 如果做广播消费，则一个 Consumer 实例消费这个 Topic 对应的所有队列，如果做集群消费，则多个 Consumer 实例平均消费这个 Topic 对应的队列集合
- 能够保证严格的消息顺序
- 支持拉（pull）和推（push）两种消息模式
- 高效的订阅者水平扩展能力
- 实时的消息订阅机制
- 亿级消息堆积能力
- 支持多种消息协议，如 JMS、OpenMessaging 等
- 较少的依赖

## 2. RocketMQ由哪些角色组成，每个角色作用和特点是什么？

| 角色       | 作用                                                         |
| ---------- | ------------------------------------------------------------ |
| Nameserver | 无状态，动态列表；这也是和zookeeper的重要区别之一。zookeeper是有状态的。 |
| Producer   | 消息生产者，负责发消息到Broker。                             |
| Broker     | 就是MQ本身，负责收发消息、持久化消息等。                     |
| Consumer   | 消息消费者，负责从Broker上拉取消息进行消费，消费完进行ack。  |

## 3. RocketMQ消费模式有几种？

消费模型由Consumer决定，消费维度为Topic。

1、集群消费

* 一条消息只会被同Group中的一个Consumer消费

* 多个Group同时消费一个Topic时，每个Group都会有一个Consumer消费到数据

2、广播消费

消息将对一 个Consumer Group 下的各个 Consumer 实例都消费一遍。即即使这些 Consumer 属于同一个Consumer Group ，消息也会被 Consumer Group 中的每个 Consumer 都消费一次。

## 4. RocketMQ消费消息是push还是pull？

RocketMQ没有真正意义的push，都是pull，虽然有push类，但实际底层实现采用的是**长轮询机制**，即拉取方式

> broker端属性 longPollingEnable 标记是否开启长轮询。默认开启

### 追问：为什么要主动拉取消息而不使用事件监听方式？

事件驱动方式是建立好长连接，由事件（发送数据）的方式来实时推送。

如果broker主动推送消息的话有可能push速度快，消费速度慢的情况，那么就会造成消息在consumer端堆积过多，同时又不能被其他consumer消费的情况。而pull的方式可以根据当前自身情况来pull，不会造成过多的压力而造成瓶颈。所以采取了pull的方式。

## 5. broker如何处理拉取请求的？

Consumer首次请求Broker

- Broker中是否有符合条件的消息

- 有 

- - 响应Consumer
  - 等待下次Consumer的请求

- 没有

- - DefaultMessageStore#ReputMessageService#run方法
  - PullRequestHoldService 来Hold连接，每个5s执行一次检查pullRequestTable有没有消息，有的话立即推送
  - 每隔1ms检查commitLog中是否有新消息，有的话写入到pullRequestTable
  - 当有新消息的时候返回请求
  - 挂起consumer的请求，即不断开连接，也不返回数据
  - 使用consumer的offset，

## 6. 如何让RocketMQ保证消息的顺序消费？

首先多个queue只能保证单个queue里的顺序，queue是典型的FIFO，天然顺序。多个queue同时消费是无法绝对保证消息的有序性的。所以总结如下：

同一topic，同一个QUEUE，发消息的时候一个线程去发送消息，消费的时候 一个线程去消费一个queue里的消息。

## 7. RocketMQ如何保证消息不丢失？

首先在如下三个部分都可能会出现丢失消息的情况：

- Producer端
- Broker端
- Consumer端

1 、Producer端如何保证消息不丢失

- 采取send()同步发消息，发送结果是同步感知的。
- 发送失败后可以重试，设置重试次数。默认3次。

- 集群部署，比如发送失败了的原因可能是当前Broker宕机了，重试的时候会发送到其他Broker上。

2、Broker端如何保证消息不丢失

- 修改刷盘策略为同步刷盘。默认情况下是异步刷盘的。

- 集群部署，主从模式，高可用。

3、Consumer端如何保证消息不丢失

- 完全消费正常后在进行手动ack确认。

## 7. rocketMQ的消息堆积如何处理？

首先要找到是什么原因导致的消息堆积，是Producer太多了，Consumer太少了导致的还是说其他情况，总之先定位问题。

然后看下消息消费速度是否正常，正常的话，可以通过上线更多consumer临时解决消息堆积问题

### 追问：如果Consumer和Queue不对等，上线了多台也在短时间内无法消费完堆积的消息怎么办？

- 准备一个临时的topic
- queue的数量是堆积的几倍
- queue分布到多Broker中
- 上线一台Consumer做消息的搬运工，把原来Topic中的消息挪到新的Topic里，不做业务逻辑处理，只是挪过去
- 上线N台Consumer同时消费临时Topic中的数据
- 改bug
- 恢复原来的Consumer，继续消费之前的Topic

### 追问：堆积时间过长消息超时了？

RocketMQ中的消息只会在commitLog被删除的时候才会消失，不会超时。也就是说未被消费的消息不会存在超时删除这情况。

### 追问：堆积的消息会不会进死信队列？

不会，消息在消费失败后会进入重试队列（%RETRY%+ConsumerGroup），18次（默认18次，网上所有文章都说是16次，无一例外。但是我没搞懂为啥是16次，这不是18个时间吗 ？）才会进入死信队列（%DLQ%+ConsumerGroup）。

## 8. RocketMQ为什么自研nameserver而不用zk？

1. RocketMQ只需要一个轻量级的维护元数据信息的组件，为此引入zk增加维护成本还强依赖另一个中间件了。
2. RocketMQ追求的是AP，而不是CP，也就是需要高可用。
   * zk是CP，因为zk节点间通过zap协议有数据共享，每个节点数据会一致，但是zk集群当挂了一半以上的节点就没法使用了。
   * nameserver是AP，节点间不通信，这样会导致节点间数据信息会发生短暂的不一致，但每个broker都会定时向所有nameserver上报路由信息和心跳。当某个broker下线了，nameserver也会延时30s才知道，而且不会通知客户端（生产和消费者），只能靠客户端自己来拉，rocketMQ是靠消息重试机制解决这个问题的，所以是最终一致性。但nameserver集群只要有一个节点就可用。https://juejin.cn/post/6844904068771479559




   ## 分布式消息中心

### [#](#_2-1-问题与解决) 2.1 问题与解决

#### [#](#_2-1-1-消息丢失的问题) 2.1.1 消息丢失的问题

1. 当你系统需要保证百分百消息不丢失，你可以使用生产者每发送一个消息，Broker 同步返回一个消息发送成功的反馈消息
2. 即每发送一个消息，同步落盘后才返回生产者消息发送成功，这样只要生产者得到了消息发送生成的返回，事后除了硬盘损坏，都可以保证不会消息丢失
3. 但是这同时引入了一个问题，同步落盘怎么才能快？

#### [#](#_2-1-2-同步落盘怎么才能快) 2.1.2 同步落盘怎么才能快

1. 使用 FileChannel + DirectBuffer 池，使用堆外内存，加快内存拷贝
2. 使用数据和索引分离，当消息需要写入时，使用 commitlog 文件顺序写，当需要定位某个消息时，查询index 文件来定位，从而减少文件IO随机读写的性能损耗

#### [#](#_2-1-3-消息堆积的问题) 2.1.3 消息堆积的问题

1. 后台定时任务每隔72小时，删除旧的没有使用过的消息信息
2. 根据不同的业务实现不同的丢弃任务，具体参考线程池的 AbortPolicy，例如FIFO/LRU等（RocketMQ没有此策略）
3. 消息定时转移，或者对某些重要的 TAG 型（支付型）消息真正落库

#### [#](#_2-1-4-定时消息的实现) 2.1.4 定时消息的实现

1. 实际 RocketMQ 没有实现任意精度的定时消息，它只支持某些特定的时间精度的定时消息
2. 实现定时消息的原理是：创建特定时间精度的 MessageQueue，例如生产者需要定时1s之后被消费者消费，你只需要将此消息发送到特定的 Topic，例如：MessageQueue-1 表示这个 MessageQueue 里面的消息都会延迟一秒被消费，然后 Broker 会在 1s 后发送到消费者消费此消息，使用 newSingleThreadScheduledExecutor 实现

#### [#](#_2-1-5-顺序消息的实现) 2.1.5 顺序消息的实现

1. 与定时消息同原理，生产者生产消息时指定特定的 MessageQueue ，消费者消费消息时，消费特定的 MessageQueue，其实单机版的消息中心在一个 MessageQueue 就天然支持了顺序消息
2. 注意：同一个 MessageQueue 保证里面的消息是顺序消费的前提是：消费者是串行的消费该 MessageQueue，因为就算 MessageQueue 是顺序的，但是当并行消费时，还是会有顺序问题，但是串行消费也同时引入了两个问题：

> 1. 引入锁来实现串行
> 2. 前一个消费阻塞时后面都会被阻塞

#### [#](#_2-1-6-分布式消息的实现) 2.1.6 分布式消息的实现

1. 需要前置知识：2PC
2. RocketMQ4.3 起支持，原理为2PC，即两阶段提交，prepared->commit/rollback
3. 生产者发送事务消息，假设该事务消息 Topic 为 Topic1-Trans，Broker 得到后首先更改该消息的 Topic 为 Topic1-Prepared，该 Topic1-Prepared 对消费者不可见。然后定时回调生产者的本地事务A执行状态，根据本地事务A执行状态，来是否将该消息修改为 Topic1-Commit 或 Topic1-Rollback，消费者就可以正常找到该事务消息或者不执行等

> 注意，就算是事务消息最后回滚了也不会物理删除，只会逻辑删除该消息

#### [#](#_2-1-7-消息的-push-实现) 2.1.7 消息的 push 实现

1. 注意，RocketMQ 已经说了自己会有低延迟问题，其中就包括这个消息的 push 延迟问题
2. 因为这并不是真正的将消息主动的推送到消费者，而是 Broker 定时任务每5s将消息推送到消费者
3. pull模式需要我们手动调用consumer拉消息，而push模式则只需要我们提供一个listener即可实现对消息的监听，而实际上，RocketMQ的push模式是基于pull模式实现的，它没有实现真正的push。
4. push方式里，consumer把轮询过程封装了，并注册MessageListener监听器，取到消息后，唤醒MessageListener的consumeMessage()来消费，对用户而言，感觉消息是被推送过来的。

#### [#](#_2-1-8-消息重复发送的避免) 2.1.8 消息重复发送的避免

1. RocketMQ 会出现消息重复发送的问题，因为在网络延迟的情况下，这种问题不可避免的发生，如果非要实现消息不可重复发送，那基本太难，因为网络环境无法预知，还会使程序复杂度加大，因此默认允许消息重复发送
2. RocketMQ 让使用者在消费者端去解决该问题，即需要消费者端在消费消息时支持幂等性的去消费消息
3. 最简单的解决方案是每条消费记录有个消费状态字段，根据这个消费状态字段来判断是否消费或者使用一个集中式的表，来存储所有消息的消费状态，从而避免重复消费
4. 具体实现可以查询关于消息幂等消费的解决方案

#### [#](#_2-1-9-广播消费与集群消费) 2.1.9 广播消费与集群消费

1. 消息消费区别：广播消费，订阅该 Topic 的消息者们都会消费**每个**消息。集群消费，订阅该 Topic 的消息者们只会有一个去消费**某个**消息
2. 消息落盘区别：具体表现在消息消费进度的保存上。广播消费，由于每个消费者都独立的去消费每个消息，因此每个消费者各自保存自己的消息消费进度。而集群消费下，订阅了某个 Topic，而旗下又有多个 MessageQueue，每个消费者都可能会去消费不同的 MessageQueue，因此总体的消费进度保存在 Broker 上集中的管理

#### [#](#_2-1-10-rocketmq-不使用-zookeeper-作为注册中心的原因-以及自制的-nameserver-优缺点) 2.1.10 RocketMQ 不使用 ZooKeeper 作为注册中心的原因，以及自制的 NameServer 优缺点？

1. ZooKeeper 作为支持顺序一致性的中间件，在某些情况下，它为了满足一致性，会丢失一定时间内的可用性，RocketMQ 需要注册中心只是为了发现组件地址，在某些情况下，RocketMQ 的注册中心可以出现数据不一致性，这同时也是 NameServer 的缺点，因为 NameServer 集群间互不通信，它们之间的注册信息可能会不一致
2. 另外，当有新的服务器加入时，NameServer 并不会立马通知到 Producer，而是由 Producer 定时去请求 NameServer 获取最新的 Broker/Consumer 信息（这种情况是通过 Producer 发送消息时，负载均衡解决）

#### [#](#_2-1-11-其它) 2.1.11 其它

![img](https://leran2deeplearnjavawebtech.oss-cn-beijing.aliyuncs.com/somephoto/RocketMQ流程.png)

加分项咯

1. 包括组件通信间使用 Netty 的自定义协议
2. 消息重试负载均衡策略（具体参考 Dubbo 负载均衡策略）
3. 消息过滤器（Producer 发送消息到 Broker，Broker 存储消息信息，Consumer 消费时请求 Broker 端从磁盘文件查询消息文件时,在 Broker 端就使用过滤服务器进行过滤）
4. Broker 同步双写和异步双写中 Master 和 Slave 的交互
5. Broker 在 4.5.0 版本更新中引入了基于 Raft 协议的多副本选举，之前这是商业版才有的特性 [ISSUE-1046open in new window](http://rocketmq.apache.org/release_notes/release-notes-4.5.0/)

