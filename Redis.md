# Redis
Remote Dictionary Server, 基于内存的数据存储系统（key-value数据库，属于NoSQL范畴）。

- Redis支持数据的持久化，可以将内存中的数据保持在磁盘中，重启的时候可以再次加载进行使用。
- Redis支持数据的备份，即master-slave模式的数据备份。
- Redis的key-value，value可以多种类型。

支持5种基本类型和5种高级类型：
![data_type](/img/redis_data_type.JPG)

## 数据类型

### String（字符串）
string是redis最基本的类型，一个key对应一个value。string类型是二进制安全的。意思是redis的string可以包含任何数据。比如jpg图片或者序列化的对象 。

string类型是Redis最基本的数据类型，一个键最大能存储512MB。

```bash
redis 127.0.0.1:6379> SET name "redis.net.cn"
OK
redis 127.0.0.1:6379> GET name
"redis.net.cn"
```

### Hash（哈希）
Redis hash 是一个键值对集合，是一个string类型的field和value的映射表，hash特别适合用于存储对象。

```bash
redis 127.0.0.1:6379> HMSET user:1 username redis.net.cn password redis.net.cn points 200
OK
redis 127.0.0.1:6379> HGETALL user:1
1) "username"
2) "redis.net.cn"
3) "password"
4) "redis.net.cn"
5) "points"
6) "200"
redis 127.0.0.1:6379>
```
以上实例中 hash 数据类型存储了包含用户脚本信息的用户对象。 实例中我们使用了 Redis HMSET, HEGTALL 命令，user:1 为键值。

每个 hash 可以存储 2^32 - 1 键值对（40多亿）。

### List（列表）
Redis 列表是简单的字符串列表，按照插入顺序排序。你可以添加一个元素导列表的头部（左边）或者尾部（右边）。

实例
redis 127.0.0.1:6379> lpush redis.net.cn redis
(integer) 1
redis 127.0.0.1:6379> lpush redis.net.cn mongodb
(integer) 2
redis 127.0.0.1:6379> lpush redis.net.cn rabitmq
(integer) 3
redis 127.0.0.1:6379> lrange redis.net.cn 0 10
1) "rabitmq"
2) "mongodb"
3) "redis"
redis 127.0.0.1:6379>
列表最多可存储 232 - 1 元素 (4294967295, 每个列表可存储40多亿)。

### Set（集合）

Redis的Set是string类型的无序集合。

集合是通过哈希表实现的，所以添加，删除，查找的复杂度都是O(1)。

sadd 命令
添加一个string元素到,key对应的set集合中，成功返回1,如果元素以及在集合中返回0,key对应的set不存在返回错误。

sadd key member
实例
redis 127.0.0.1:6379> sadd redis.net.cn redis
(integer) 1
redis 127.0.0.1:6379> sadd redis.net.cn mongodb
(integer) 1
redis 127.0.0.1:6379> sadd redis.net.cn rabitmq
(integer) 1
redis 127.0.0.1:6379> sadd redis.net.cn rabitmq
(integer) 0
redis 127.0.0.1:6379> smembers redis.net.cn

1) "rabitmq"
2) "mongodb"
3) "redis"
注意：以上实例中 rabitmq 添加了两次，但根据集合内元素的唯一性，第二次插入的元素将被忽略。


集合中最大的成员数为 232 - 1 (4294967295, 每个集合可存储40多亿个成员)。

### zset(sorted set：有序集合)
Redis zset 和 set 一样也是string类型元素的集合,且不允许重复的成员。
不同的是每个元素都会关联一个double类型的分数。redis正是通过分数来为集合中的成员进行从小到大的排序。

zset的成员是唯一的,但分数(score)却可以重复。

zadd 命令
添加元素到集合，元素在集合中存在则更新对应score

zadd key score member 
实例
redis 127.0.0.1:6379> zadd redis.net.cn 0 redis
(integer) 1
redis 127.0.0.1:6379> zadd redis.net.cn 0 mongodb
(integer) 1
redis 127.0.0.1:6379> zadd redis.net.cn 0 rabitmq
(integer) 1
redis 127.0.0.1:6379> zadd redis.net.cn 0 rabitmq
(integer) 0
redis 127.0.0.1:6379> ZRANGEBYSCORE redis.net.cn 0 1000

1) "redis"
2) "mongodb"
3) "rabitmq"


## 发布订阅
Redis 发布订阅(pub/sub)是一种消息通信模式：发送者(pub)发送消息，订阅者(sub)接收消息。

Redis 客户端可以订阅任意数量的频道。

下图展示了频道 channel1，以及订阅这个频道的三个客户端 —— client2、client5和client1之间的关系：
![p1](/img/redis_pubsub1.png)

当有新消息通过`PUBLISH`命令发送给频道 channel1 时， 这个消息就会被发送给订阅它的三个客户端：
![p2](/img/redis_pubsub2.png)

以下实例演示了发布订阅是如何工作的。在我们实例中我们创建了订阅频道名为 redisChat:

redis 127.0.0.1:6379> SUBSCRIBE redisChat

Reading messages... (press Ctrl-C to quit)
1) "subscribe"
2) "redisChat"
3) (integer) 1

现在，我们先重新开启个 redis 客户端，然后在同一个频道 redisChat 发布两次消息，订阅者就能接收到消息。

redis 127.0.0.1:6379> PUBLISH redisChat "Redis is a great caching technique"

(integer) 1

redis 127.0.0.1:6379> PUBLISH redisChat "Learn redis by w3cschool.cc"

(integer) 1

订阅者的客户端会显示如下消息
1) "message"
2) "redisChat"
3) "Redis is a great caching technique"
1) "message"
2) "redisChat"
3) "Learn redis by w3cschool.cc"
Redis 发布订阅命令
下表列出了 redis 发布订阅常用命令：

序号	命令及描述
1	PSUBSCRIBE pattern [pattern ...] 订阅一个或多个符合给定模式的频道。
2	PUBSUB subcommand [argument [argument ...]] 查看订阅与发布系统状态。
3	PUBLISH channel message 将信息发送到指定的频道。
4	PUNSUBSCRIBE [pattern [pattern ...]] 退订所有给定模式的频道。
5	SUBSCRIBE channel [channel ...] 订阅给定的一个或多个频道的信息。
6	UNSUBSCRIBE [channel [channel ...]] 指退订给定的频道。


## Redis 事务

Redis 事务可以一次执行多个命令， 并且带有以下两个重要的保证：

事务是一个单独的隔离操作：事务中的所有命令都会序列化、按顺序地执行。事务在执行的过程中，不会被其他客户端发送来的命令请求所打断。
事务是一个原子操作：事务中的命令要么全部被执行，要么全部都不执行。
一个事务从开始到执行会经历以下三个阶段：

开始事务。
命令入队。
执行事务。
实例
以下是一个事务的例子， 它先以 MULTI 开始一个事务， 然后将多个命令入队到事务中， 最后由 EXEC 命令触发事务， 一并执行事务中的所有命令：

redis 127.0.0.1:6379> MULTI
OK
 
redis 127.0.0.1:6379> SET book-name "Mastering C++ in 21 days"
QUEUED
 
redis 127.0.0.1:6379> GET book-name
QUEUED
 
redis 127.0.0.1:6379> SADD tag "C++" "Programming" "Mastering Series"
QUEUED
 
redis 127.0.0.1:6379> SMEMBERS tag
QUEUED
 
redis 127.0.0.1:6379> EXEC
1) OK
2) "Mastering C++ in 21 days"
3) (integer) 3
4) 1) "Mastering Series"
   2) "C++"
   3) "Programming"
Redis 事务命令
下表列出了 redis 事务的相关命令：

序号	命令及描述
1	DISCARD 取消事务，放弃执行事务块内的所有命令。
2	EXEC 执行所有事务块内的命令。
3	MULTI 标记一个事务块的开始。
4	UNWATCH 取消 WATCH 命令对所有 key 的监视。
5	WATCH key [key ...] 监视一个(或多个) key ，如果在事务执行之前这个(或这些) key 被其他命令所改动，那么事务将被打断。

## Redis Stream
Redis Stream 是 Redis 5.0 版本新增加的数据结构。

Redis Stream 主要用于消息队列（MQ，Message Queue），Redis 本身是有一个 Redis 发布订阅 (pub/sub) 来实现消息队列的功能，但它有个缺点就是消息无法持久化，如果出现网络断开、Redis 宕机等，消息就会被丢弃。

简单来说发布订阅 (pub/sub) 可以分发消息，但无法记录历史消息。

而 Redis Stream 提供了消息的持久化和主备复制功能，可以让任何客户端访问任何时刻的数据，并且能记住每一个客户端的访问位置，还能保证消息不丢失。

Redis Stream 的结构如下所示，它有一个消息链表，将所有加入的消息都串起来，每个消息都有一个唯一的 ID 和对应的内容：

![stream](/img/redis_stream.png)

每个 Stream 都有唯一的名称，它就是 Redis 的 key，在我们首次使用 xadd 指令追加消息时自动创建。

上图解析：

Consumer Group ：消费组，使用 XGROUP CREATE 命令创建，一个消费组有多个消费者(Consumer)。
last_delivered_id ：游标，每个消费组会有个游标 last_delivered_id，任意一个消费者读取了消息都会使游标 last_delivered_id 往前移动。
pending_ids ：消费者(Consumer)的状态变量，作用是维护消费者的未确认的 id。 pending_ids 记录了当前已经被客户端读取的消息，但是还没有 ack (Acknowledge character：确认字符）。
消息队列相关命令：

XADD - 添加消息到末尾
XTRIM - 对流进行修剪，限制长度
XDEL - 删除消息
XLEN - 获取流包含的元素数量，即消息长度
XRANGE - 获取消息列表，会自动过滤已经删除的消息
XREVRANGE - 反向获取消息列表，ID 从大到小
XREAD - 以阻塞或非阻塞方式获取消息列表
消费者组相关命令：

XGROUP CREATE - 创建消费者组
XREADGROUP GROUP - 读取消费者组中的消息
XACK - 将消息标记为"已处理"
XGROUP SETID - 为消费者组设置新的最后递送消息ID
XGROUP DELCONSUMER - 删除消费者
XGROUP DESTROY - 删除消费者组
XPENDING - 显示待处理消息的相关信息
XCLAIM - 转移消息的归属权
XINFO - 查看流和消费者组的相关信息；
XINFO GROUPS - 打印消费者组的信息；
XINFO STREAM - 打印流信息
XADD
使用 XADD 向队列添加消息，如果指定的队列不存在，则创建一个队列，XADD 语法格式：

XADD key ID field value [field value ...]
key ：队列名称，如果不存在就创建
ID ：消息 id，我们使用 * 表示由 redis 生成，可以自定义，但是要自己保证递增性。
field value ： 记录。
实例
redis> XADD mystream * name Sara surname OConnor
"1601372323627-0"
redis> XADD mystream * field1 value1 field2 value2 field3 value3
"1601372323627-1"
redis> XLEN mystream
(integer) 2
redis> XRANGE mystream - +
1) 1) "1601372323627-0"
   2) 1) "name"
      2) "Sara"
      3) "surname"
      4) "OConnor"
2) 1) "1601372323627-1"
   2) 1) "field1"
      2) "value1"
      3) "field2"
      4) "value2"
      5) "field3"
      6) "value3"
redis>
XTRIM
使用 XTRIM 对流进行修剪，限制长度， 语法格式：

XTRIM key MAXLEN [~] count
key ：队列名称
MAXLEN ：长度
count ：数量
实例
127.0.0.1:6379> XADD mystream * field1 A field2 B field3 C field4 D
"1601372434568-0"
127.0.0.1:6379> XTRIM mystream MAXLEN 2
(integer) 0
127.0.0.1:6379> XRANGE mystream - +
1) 1) "1601372434568-0"
   2) 1) "field1"
      2) "A"
      3) "field2"
      4) "B"
      5) "field3"
      6) "C"
      7) "field4"
      8) "D"
127.0.0.1:6379>

redis>
XDEL
使用 XDEL 删除消息，语法格式：

XDEL key ID [ID ...]
key：队列名称
ID ：消息 ID
实例
> XADD mystream * a 1
1538561698944-0
> XADD mystream * b 2
1538561700640-0
> XADD mystream * c 3
1538561701744-0
> XDEL mystream 1538561700640-0
(integer) 1
127.0.0.1:6379> XRANGE mystream - +
1) 1) 1538561698944-0
   2) 1) "a"
      2) "1"
2) 1) 1538561701744-0
   2) 1) "c"
      2) "3"
XLEN
使用 XLEN 获取流包含的元素数量，即消息长度，语法格式：

XLEN key
key：队列名称
实例
redis> XADD mystream * item 1
"1601372563177-0"
redis> XADD mystream * item 2
"1601372563178-0"
redis> XADD mystream * item 3
"1601372563178-1"
redis> XLEN mystream
(integer) 3
redis>
XRANGE
使用 XRANGE 获取消息列表，会自动过滤已经删除的消息 ，语法格式：

XRANGE key start end [COUNT count]
key ：队列名
start ：开始值， - 表示最小值
end ：结束值， + 表示最大值
count ：数量
实例
redis> XADD writers * name Virginia surname Woolf
"1601372577811-0"
redis> XADD writers * name Jane surname Austen
"1601372577811-1"
redis> XADD writers * name Toni surname Morrison
"1601372577811-2"
redis> XADD writers * name Agatha surname Christie
"1601372577812-0"
redis> XADD writers * name Ngozi surname Adichie
"1601372577812-1"
redis> XLEN writers
(integer) 5
redis> XRANGE writers - + COUNT 2
1) 1) "1601372577811-0"
   2) 1) "name"
      2) "Virginia"
      3) "surname"
      4) "Woolf"
2) 1) "1601372577811-1"
   2) 1) "name"
      2) "Jane"
      3) "surname"
      4) "Austen"
redis>
XREVRANGE
使用 XREVRANGE 获取消息列表，会自动过滤已经删除的消息 ，语法格式：

XREVRANGE key end start [COUNT count]
key ：队列名
end ：结束值， + 表示最大值
start ：开始值， - 表示最小值
count ：数量
实例
redis> XADD writers * name Virginia surname Woolf
"1601372731458-0"
redis> XADD writers * name Jane surname Austen
"1601372731459-0"
redis> XADD writers * name Toni surname Morrison
"1601372731459-1"
redis> XADD writers * name Agatha surname Christie
"1601372731459-2"
redis> XADD writers * name Ngozi surname Adichie
"1601372731459-3"
redis> XLEN writers
(integer) 5
redis> XREVRANGE writers + - COUNT 1
1) 1) "1601372731459-3"
   2) 1) "name"
      2) "Ngozi"
      3) "surname"
      4) "Adichie"
redis>
XREAD
使用 XREAD 以阻塞或非阻塞方式获取消息列表 ，语法格式：

XREAD [COUNT count] [BLOCK milliseconds] STREAMS key [key ...] id [id ...]
count ：数量
milliseconds ：可选，阻塞毫秒数，没有设置就是非阻塞模式
key ：队列名
id ：消息 ID
实例
 从 Stream 头部读取两条消息
> XREAD COUNT 2 STREAMS mystream writers 0-0 0-0
1) 1) "mystream"
   2) 1) 1) 1526984818136-0
         2) 1) "duration"
            2) "1532"
            3) "event-id"
            4) "5"
            5) "user-id"
            6) "7782813"
      2) 1) 1526999352406-0
         2) 1) "duration"
            2) "812"
            3) "event-id"
            4) "9"
            5) "user-id"
            6) "388234"
2) 1) "writers"
   2) 1) 1) 1526985676425-0
         2) 1) "name"
            2) "Virginia"
            3) "surname"
            4) "Woolf"
      2) 1) 1526985685298-0
         2) 1) "name"
            2) "Jane"
            3) "surname"
            4) "Austen"

XGROUP CREATE
使用 XGROUP CREATE 创建消费者组，语法格式：

XGROUP [CREATE key groupname id-or-$] [SETID key groupname id-or-$] [DESTROY key groupname] [DELCONSUMER key groupname consumername]
key ：队列名称，如果不存在就创建
groupname ：组名。
$ ： 表示从尾部开始消费，只接受新消息，当前 Stream 消息会全部忽略。
从头开始消费:

XGROUP CREATE mystream consumer-group-name 0-0  
从尾部开始消费:

XGROUP CREATE mystream consumer-group-name $
XREADGROUP GROUP
使用 XREADGROUP GROUP 读取消费组中的消息，语法格式：

XREADGROUP GROUP group consumer [COUNT count] [BLOCK milliseconds] [NOACK] STREAMS key [key ...] ID [ID ...]
group ：消费组名
consumer ：消费者名。
count ： 读取数量。
milliseconds ： 阻塞毫秒数。
key ： 队列名。
ID ： 消息 ID。
XREADGROUP GROUP consumer-group-name consumer-name COUNT 1 STREAMS mystream >





## Redis 管道技术

Redis是一种基于客户端-服务端模型以及请求/响应协议的TCP服务。这意味着通常情况下一个请求会遵循以下步骤：

- 客户端向服务端发送一个查询请求，并监听Socket返回，通常是以阻塞模式，等待服务端响应。
- 服务端处理命令，并将结果返回给客户端。

### Redis 管道技术
Redis 管道技术可以在服务端未响应时，客户端可以继续向服务端发送请求，并最终一次性读取所有服务端的响应。

查看 redis 管道，只需要启动 redis 实例并输入以下命令：
```shell
$ touch a.txt
$ echo "PING\r\n SET w3ckey redis\r\nGET w3ckey\r\nINCR visitor\r\nINCR visitor\r\nINCR visitor\r\n" > a.txt
$ cat a.txt | redis-cli --pipe 
All data transferred. Waiting for the last reply...
Last reply received from server.
errors: 0, replies: 6
$ redis-cli
127.0.0.1:6379> get w3ckey
"redis"

#############################################################

$(echo -en "PING\r\n SET w3ckey redis\r\nGET w3ckey\r\nINCR visitor\r\nINCR visitor\r\nINCR visitor\r\n"; sleep 10) | nc localhost 6379
 
+PONG
+OK
redis
:1
:2
:3
```
以上实例中我们通过使用 PING 命令查看redis服务是否可用， 之后我们们设置了 w3ckey 的值为 redis，然后我们获取 w3ckey 的值并使得 visitor 自增 3 次。

在返回的结果中我们可以看到这些命令一次性向 redis 服务提交，并最终一次性读取所有服务端的响应。

管道技术最显著的优势是提高了 redis 服务的性能。


## Redis 分区

分区是分割数据到多个Redis实例的处理过程，因此每个实例只保存key的一个子集。

### 分区的优势
通过利用多台计算机内存的和值，允许我们构造更大的数据库。
通过多核和多台计算机，允许我们扩展计算能力；通过多台计算机和网络适配器，允许我们扩展网络带宽。

### 分区的不足
redis的一些特性在分区方面表现的不是很好：

涉及多个key的操作通常是不被支持的。举例来说，当两个set映射到不同的redis实例上时，你就不能对这两个set执行交集操作。
涉及多个key的redis事务不能使用。
当使用分区时，数据处理较为复杂，比如你需要处理多个rdb/aof文件，并且从多个实例和主机备份持久化文件。
增加或删除容量也比较复杂。redis集群大多数支持在运行时增加、删除节点的透明数据平衡的能力，但是类似于客户端分区、代理等其他系统则不支持这项特性。然而，一种叫做presharding的技术对此是有帮助的。

### 分区类型
Redis 有两种类型分区。 假设有4个Redis实例 R0，R1，R2，R3，和类似user:1，user:2这样的表示用户的多个key，对既定的key有多种不同方式来选择这个key存放在哪个实例中。也就是说，有不同的系统来映射某个key到某个Redis服务。

#### 范围分区
最简单的分区方式是按范围分区，就是映射一定范围的对象到特定的Redis实例。

比如，ID从0到10000的用户会保存到实例R0，ID从10001到 20000的用户会保存到R1，以此类推。

这种方式是可行的，并且在实际中使用，不足就是要有一个区间范围到实例的映射表。这个表要被管理，同时还需要各 种对象的映射表，通常对Redis来说并非是好的方法。

#### 哈希分区
另外一种分区方法是hash分区。这对任何key都适用，也无需是object_name:这种形式，像下面描述的一样简单：

用一个hash函数将key转换为一个数字，比如使用crc32 hash函数。对key foobar执行crc32(foobar)会输出类似93024922的整数。
对这个整数取模，将其转化为0-3之间的数字，就可以将这个整数映射到4个Redis实例中的一个了。93024922 % 4 = 2，就是说key foobar应该被存到R2实例中。注意：取模操作是取除的余数，通常在多种编程语言中用%操作符实现。

---


## Docker启动
`redis/redis-stack-server`: To start Redis Stack server using the redis-stack-server image, run the following command in your terminal:
```bash
$ docker run -d --name redis-stack-server -p 6379:6379 redis/redis-stack-server:latest
```

`redis/redis-stack`: To start a Redis Stack container using the redis-stack image, run the following command in your terminal:
```bash
$ docker run -d --name redis-stack -p 6379:6379 -p 8001:8001 redis/redis-stack:latest
```
The docker run command above also exposes Redis Insight on port 8001. You can use Redis Insight by pointing your browser to `localhost:8001`.

`Connect with redis-cli`: If you don’t have redis-cli installed locally, you can run it from the Docker container:
```bash
$ docker exec -it redis-stack redis-cli
```