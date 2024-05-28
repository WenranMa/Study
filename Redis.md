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
127.0.0.1:6379> HMSET user:1 username redis.net.cn password redis.net.cn points 200
OK
127.0.0.1:6379> HGETALL user:1
1) "username"
2) "redis.net.cn"
3) "password"
4) "redis.net.cn"
5) "points"
6) "200"
127.0.0.1:6379> 
```
以上实例中 hash 数据类型存储了包含用户脚本信息的用户对象。 实例中我们使用了 Redis HMSET, HEGTALL 命令，user:1 为键值。

每个 hash 可以存储 2^32 - 1 键值对（40多亿）。

### List（列表）
Redis 列表是简单的字符串列表，按照插入顺序排序。你可以添加一个元素导列表的头部（左边）或者尾部（右边）。

```bash 
127.0.0.1:6379> lpush redis.net.cn redis
(integer) 1
127.0.0.1:6379> lpush redis.net.cn mongodb
(integer) 2
127.0.0.1:6379> lpush redis.net.cn nginx
(integer) 3
127.0.0.1:6379> lrange redis.net.cn 0 -1
1) "nginx"
2) "mongodb"
3) "redis"
```
列表最多可存储 2^32 - 1 元素 (4294967295, 每个列表可存储40多亿)。

### Set（集合）
Redis的Set是string类型的无序集合。集合是通过哈希表实现的，所以添加，删除，查找的复杂度都是O(1)。

`sadd` 命令添加一个string元素到,key对应的set集合中，成功返回1,如果元素以及在集合中返回0,key对应的set不存在返回错误。

```bash
127.0.0.1:6379> sadd course nginx redis golang
(integer) 3
127.0.0.1:6379> sadd crouse nginx
(integer) 1
127.0.0.1:6379> smembers course
1) "nginx"
2) "redis"
3) "golang"
```
注意：以上实例中 nginx 添加了两次，但根据集合内元素的唯一性，第二次插入的元素将被忽略。

集合中最大的成员数为 2^32 - 1 (4294967295, 每个集合可存储40多亿个成员)。

### zset(sorted set：有序集合)
Redis zset 和 set 一样也是string类型元素的集合,且不允许重复的成员。不同的是每个元素都会关联一个double类型的分数。redis正是通过分数来为集合中的成员进行从小到大的排序。

zset的成员是唯一的,但分数(score)却可以重复。

`zadd` 命令添加元素到集合，元素在集合中存在则更新对应score

```bash
127.0.0.1:6379> zadd team 100 data
(integer) 1
127.0.0.1:6379> zadd team 200 vi
(integer) 1
127.0.0.1:6379> zadd team 50 ads
(integer) 1
127.0.0.1:6379> zadd team 12 ads
(integer) 0
127.0.0.1:6379> zrangebyscore team 0 500
1) "ads"
2) "data"
3) "vi"
```

### HyperLogLog
Redis HyperLogLog 是用来做基数统计的算法，优点是在输入元素的数量或者体积非常非常大时，计算基数所需的空间总是固定的、并且很小。

在 Redis 里面，每个 HyperLogLog 键只需要花费 12KB 内存，就可以计算接近 2^64 个不同元素的基数。这和计算基数时，元素越多耗费内存就越多的集合形成鲜明对比。

但是，因为 HyperLogLog 只会根据输入元素来计算基数，而不会储存输入元素本身，所以 HyperLogLog 不能像集合那样，返回输入的各个元素。

什么是基数？

比如数据集 `{1, 3, 5, 7, 5, 7, 8}`， 那么这个数据集的基数集为 `{1, 3, 5 ,7, 8}`, 基数(不重复元素)为5。 基数估计就是在误差可接受的范围内，快速计算基数。

实例
```bash
127.0.0.1:6379> PFADD course git redis nginx
(integer) 1
127.0.0.1:6379> PFCOUNT course
(integer) 3
127.0.0.1:6379> PFADD course docker
(integer) 1
127.0.0.1:6379> PFCOUNT course
(integer) 4
127.0.0.1:6379> PFADD course2 git k8s
(integer) 1
127.0.0.1:6379> PFCOUNT course2
(integer) 2
127.0.0.1:6379> PFMERGE c course course2
OK
127.0.0.1:6379> PFCOUNT c
(integer) 5
```
Redis HyperLogLog 命令:
- PFADD key element [element ...] 添加指定元素到 HyperLogLog 中。
- PFCOUNT key [key ...] 返回给定 HyperLogLog 的基数估算值。
- PFMERGE destkey sourcekey [sourcekey ...] 将多个 HyperLogLog 合并为一个 HyperLogLog


## Redis Bitmap
bitmap就是通过最小的单位bit来进行0或者1的设置，表示某个元素对应的值或者状态。一个bit的值只有0或1；也就是说一个bit能存储的最多信息是2。

位图是字符串类型的扩展，offset就是数组的下标。

命令：
- SETBIT 对 key 所储存的字符串值，设置或清除指定偏移量上的位(bit)。O(1)
- GETBIT 对 key 所储存的字符串值，获取指定偏移量上的位(bit)。O(1)
- BITCOUNT 计算给定字符串中，被设置为 1 的比特位的数量。O(N)
- BITPOS 返回位图中第一个值为 bit 的二进制位的位置。O(N)

实例：
```bash
127.0.0.1:6379> setbit gitcommit 0 1
(integer) 0
127.0.0.1:6379> setbit gitcommit 1 1
(integer) 0
127.0.0.1:6379> setbit gitcommit 2 0
(integer) 0
127.0.0.1:6379> getbit gitcommit 1
(integer) 1
127.0.0.1:6379> bitcount gitcommit
(integer) 2
127.0.0.1:6379> bitpos gitcommit 0
(integer) 2
```

因为是字符串的扩展，所以可以直接使用set命令。
```bash
127.0.0.1:6379> set gitcommit "\xF0"
OK
127.0.0.1:6379> getbit gitcommit 1
(integer) 1
127.0.0.1:6379> getbit gitcommit 0
(integer) 1
127.0.0.1:6379> bitcount gitcommit
(integer) 4
127.0.0.1:6379> bitpos gitcommit 0
(integer) 4
```

优势
- 基于最小的单位bit进行存储，所以非常省空间。
- 设置时候时间复杂度O(1)、读取时候时间复杂度O(n)，操作是非常快的。
- 二进制数据的存储，进行相关计算的时候非常快。
- 方便扩容

限制
- redis中bit映射被限制在512MB之内，所以最大是2^32位。
- 因为读取时候时间复杂度O(n)，越大的串读的时间花销越多。

大概的空间占用计算公式是：($offset/8/1024/1024)MB

## Redis BitField
BITFIELD 命令可以将一个 Redis 字符串看作是一个由二进制位组成的数组， 并对这个数组中储存的长度不同的整数进行访问 （被储存的整数无需进行对齐）。也是字符串的延申。

```bash
127.0.0.1:6379> bitfield name set u8 #0 77
1) (integer) 0
127.0.0.1:6379> bitfield name set u8 #1 65
1) (integer) 0
127.0.0.1:6379> bitfield name set u8 #2 78
1) (integer) 0
127.0.0.1:6379> get name
"MAN"
127.0.0.1:6379> bitfield name get u24 #0
1) (integer) 5062990
127.0.0.1:6379> bitfield name get u8 #0
1) (integer) 77
127.0.0.1:6379> bitfield name incrby u8 #2 1
1) (integer) 79
127.0.0.1:6379> get name
"MAO"
```


## 发布订阅
Redis 发布订阅(pub/sub)是一种消息通信模式：发送者(pub)发送消息，订阅者(sub)接收消息。

Redis 客户端可以订阅任意数量的频道。

下图展示了频道 channel1，以及订阅这个频道的三个客户端 —— client2、client5和client1之间的关系：
![p1](/img/redis_pubsub1.png)

当有新消息通过`PUBLISH`命令发送给频道 channel1 时， 这个消息就会被发送给订阅它的三个客户端：
![p2](/img/redis_pubsub2.png)

以下实例演示了发布订阅是如何工作的。在我们实例中我们创建了订阅频道名为 chat:

```bash
redis 127.0.0.1:6379> SUBSCRIBE chat
1) "subscribe"
2) "chat"
3) (integer) 1
Reading messages... (press Ctrl-C to quit ... )
```

现在，我们先重新开启个 redis 客户端，然后在同一个频道 chat 发布两次消息，订阅者就能接收到消息。

```bash 
127.0.0.1:6379> PUBLISH chat gogogo
(integer) 1
127.0.0.1:6379> PUBLISH chat fly
(integer) 1
```

订阅者的客户端会显示如下消息

```bash
1) "message"
2) "chat"
3) "gogogo"
1) "message"
2) "chat"
3) "fly"
```

redis 发布订阅常用命令：
- PSUBSCRIBE pattern [pattern ...] 订阅一个或多个符合给定模式的频道。
- PUBSUB subcommand [argument [argument ...]] 查看订阅与发布系统状态。
- PUBLISH channel message 将信息发送到指定的频道。
- PUNSUBSCRIBE [pattern [pattern ...]] 退订所有给定模式的频道。
- SUBSCRIBE channel [channel ...] 订阅给定的一个或多个频道的信息。
- UNSUBSCRIBE [channel [channel ...]] 指退订给定的频道。


## Redis 事务
Redis 事务可以一次执行多个命令， 并且带有以下两个重要的保证：

- 事务是一个单独的隔离操作：事务中的所有命令都会序列化、按顺序地执行。事务在执行的过程中，不会被其他客户端发送来的命令请求所打断。
- 事务是一个原子操作：事务中的命令要么全部被执行，要么全部都不执行。

一个事务从开始到执行会经历以下三个阶段：
- 开始事务。
- 命令入队。
- 执行事务。

以下是一个事务的例子， 它先以 MULTI 开始一个事务， 然后将多个命令入队到事务中， 最后由 EXEC 命令触发事务， 一并执行事务中的所有命令：

```bash
# redis-cli
127.0.0.1:6379> multi
OK
127.0.0.1:6379(TX)> set book "the go programming language"
QUEUED
127.0.0.1:6379(TX)> get book
QUEUED
127.0.0.1:6379(TX)> sadd tag "go" "docker" "programming"
QUEUED
127.0.0.1:6379(TX)> smembers tag
QUEUED
127.0.0.1:6379(TX)> exec
1) OK
2) "the go programming language"
3) (integer) 3
4) 1) "go"
   2) "docker"
   3) "programming"
```

Redis 事务命令:
- DISCARD 取消事务，放弃执行事务块内的所有命令。
- EXEC 执行所有事务块内的命令。
- MULTI 标记一个事务块的开始。
- UNWATCH 取消 WATCH 命令对所有 key 的监视。
- WATCH key [key ...] 监视一个(或多个) key ，如果在事务执行之前这个(或这些) key 被其他命令所改动，那么事务将被打断。


## Redis Stream
Redis Stream 是 Redis 5.0 版本新增加的数据结构。

Redis Stream 主要用于消息队列（MQ，Message Queue），Redis 本身是有一个 Redis 发布订阅 (pub/sub) 来实现消息队列的功能，但它有个缺点就是消息无法持久化，如果出现网络断开、Redis 宕机等，消息就会被丢弃。

简单来说发布订阅 (pub/sub) 可以分发消息，但无法记录历史消息。

而 Redis Stream 提供了消息的持久化和主备复制功能，可以让任何客户端访问任何时刻的数据，并且能记住每一个客户端的访问位置，还能保证消息不丢失。

Redis Stream 的结构如下所示，它有一个消息链表，将所有加入的消息都串起来，每个消息都有一个唯一的 ID 和对应的内容：

![stream](/img/redis_stream.png)

每个 Stream 都有唯一的名称，它就是 Redis 的 key，在我们首次使用 xadd 指令追加消息时自动创建。

上图解析：

- Consumer Group ：消费组，使用 XGROUP CREATE 命令创建，一个消费组有多个消费者(Consumer)。
- last_delivered_id ：游标，每个消费组会有个游标 last_delivered_id，任意一个消费者读取了消息都会使游标 last_delivered_id 往前移动。
- pending_ids ：消费者(Consumer)的状态变量，作用是维护消费者的未确认的 id。 pending_ids 记录了当前已经被客户端读取的消息，但是还没有 ack (Acknowledge character：确认字符）。

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

使用 XADD 向队列添加消息，如果指定的队列不存在，则创建一个队列，XADD 语法格式：

`XADD key ID field value [field value ...]`
- key ：队列名称，如果不存在就创建
- ID ：消息 id，我们使用 * 表示由 redis 生成，可以自定义，但是要自己保证递增性。
- field value ： 记录。

使用 XTRIM 对流进行修剪，限制长度， 语法格式：

`XTRIM key MAXLEN [~] count`
- key ：队列名称
- MAXLEN ：长度
- count ：数量

使用 XDEL 删除消息，语法格式：

`XDEL key ID [ID ...]`
- key：队列名称
- ID ：消息 ID

```bash
127.0.0.1:6379> XADD mystream * name Sara surname OConnor
"1716910387942-0"
127.0.0.1:6379> XADD mystream * book golang price 30
"1716910415691-0"
127.0.0.1:6379> 
127.0.0.1:6379> XADD mystream * test "this is a test message"
"1716910458117-0"
127.0.0.1:6379> xrange mystream - +
1) 1) "1716910387942-0"
   2) 1) "name"
      2) "Sara"
      3) "surname"
      4) "OConnor"
2) 1) "1716910415691-0"
   2) 1) "book"
      2) "golang"
      3) "price"
      4) "30"
3) 1) "1716910458117-0"
   2) 1) "test"
      2) "this is a test message"

127.0.0.1:6379> xtrim mystream MAXLEN 2
(integer) 1
127.0.0.1:6379> xrange mystream - +
1) 1) "1716910415691-0"
   2) 1) "book"
      2) "golang"
      3) "price"
      4) "30"
2) 1) "1716910458117-0"
   2) 1) "test"
      2) "this is a test message"

127.0.0.1:6379> xdel mystream "1716910458117-0"
(integer) 1
127.0.0.1:6379> xrange mystream - +
1) 1) "1716910415691-0"
   2) 1) "book"
      2) "golang"
      3) "price"
      4) "30"
```

使用 XLEN 获取流包含的元素数量，即消息长度，语法格式：

`XLEN key`
- key：队列名称

使用 XRANGE 获取消息列表，会自动过滤已经删除的消息 ，语法格式：

`XRANGE key start end [COUNT count]`
- key ：队列名
- start ：开始值， - 表示最小值
- end ：结束值， + 表示最大值
- count ：数量

使用 XREAD 以阻塞或非阻塞方式获取消息列表 ，语法格式：

`XREAD [COUNT count] [BLOCK milliseconds] STREAMS key [key ...] id [id ...]`
- count ：数量
- milliseconds ：可选，阻塞毫秒数，没有设置就是非阻塞模式
- key ：队列名
- id ：消息 ID

从 Stream 头部读取两条消息
```bash
127.0.0.1:6379> xread count 2 streams mystream 0-0
1) 1) "mystream"
   2) 1) 1) "1716910415691-0"
         2) 1) "book"
            2) "golang"
            3) "price"
            4) "30"
      2) 1) "1716911520023-0"
         2) 1) "test"
            2) "this is a test message"
```

使用 XGROUP CREATE 创建消费者组，语法格式：

`XGROUP [CREATE key groupname id-or-$] [SETID key groupname id-or-$] [DESTROY key groupname] [DELCONSUMER key groupname consumername]`
- key ：队列名称，如果不存在就创建
- groupname ：组名。
- $ ： 表示从尾部开始消费，只接受新消息，当前 Stream 消息会全部忽略。

从头开始消费: `XGROUP CREATE mystream consumer-group-name 0-0`

从尾部开始消费:`XGROUP CREATE mystream consumer-group-name $`

使用 XREADGROUP GROUP 读取消费组中的消息，语法格式：

`XREADGROUP GROUP group consumer [COUNT count] [BLOCK milliseconds] [NOACK] STREAMS key [key ...] ID [ID ...]`
- group ：消费组名
- consumer ：消费者名。
- count ： 读取数量。
- milliseconds ： 阻塞毫秒数。
- key ： 队列名。
- ID ： 消息 ID。


## Redis 数据备份与恢复  -- BGSAVE tbd
`SAVE` 命令用于创建当前数据库的备份。

该命令将在 redis 安装目录中创建dump.rdb文件。

如果需要恢复数据，只需将备份文件 (dump.rdb) 移动到 redis 安装目录并启动服务即可。获取 redis 目录可以使用 CONFIG 命令，如下所示：

```bash
127.0.0.1:6379> config get dir
1) "dir"
2) "/data"
```

Bgsave
创建 redis 备份文件也可以使用命令 BGSAVE，该命令在后台执行。

```bash
127.0.0.1:6379> bgsave
Background saving started
127.0.0.1:6379> set age 37
OK
```


不好使啊？
时间是啥？？？？  


## Redis 安全
可以通过 redis 的配置文件设置密码参数，这样客户端连接到 redis 服务就需要密码验证。

通过以下命令查看是否设置了密码验证：
```bash
127.0.0.1:6379> CONFIG get requirepass
1) "requirepass"
2) ""
```

默认 requirepass 参数是空的，意味着无需通过密码验证就可以连接到 redis 服务。

可以通过以下命令来修改该参数：
```bash
127.0.0.1:6379> config set requirepass 870220
OK
127.0.0.1:6379> config get requirepass
1) "requirepass"
2) "870220"
```

设置密码后，客户端连接 redis 服务就需要密码验证，否则无法执行命令。使用 `AUTH` 命令输入密码：
```bash
# redis-cli
127.0.0.1:6379> set age 37
(error) NOAUTH Authentication required.
127.0.0.1:6379> auth 870220
OK
127.0.0.1:6379> set age 37
OK
127.0.0.1:6379> 
```

## Redis 性能测试
Redis 性能测试是通过同时执行多个命令实现的。

基本命令：
`redis-benchmark [option] [option value]`

注意：该命令是在 redis 的目录下执行的，而不是 redis 客户端的内部指令。

以下实例同时执行 1000 个请求来检测性能：
```bash
# redis-benchmark -n 1000 -q
PING_INLINE: 10638.30 requests per second, p50=0.367 msec          
PING_MBULK: 45454.55 requests per second, p50=0.407 msec
SET: 50000.00 requests per second, p50=0.391 msec
GET: 40000.00 requests per second, p50=0.415 msec
INCR: 38461.54 requests per second, p50=0.407 msec
LPUSH: 47619.05 requests per second, p50=0.415 msec
RPUSH: 40000.00 requests per second, p50=0.431 msec                  
LPOP: 52631.58 requests per second, p50=0.415 msec
RPOP: 37037.04 requests per second, p50=0.455 msec
SADD: 45454.55 requests per second, p50=0.415 msec
HSET: 47619.05 requests per second, p50=0.407 msec
SPOP: 45454.55 requests per second, p50=0.439 msec
ZADD: 37037.04 requests per second, p50=0.471 msec
ZPOPMIN: 52631.58 requests per second, p50=0.399 msec
LPUSH (needed to benchmark LRANGE): 47619.05 requests per second, p50=0.415 msec
LRANGE_100 (first 100 elements): 29411.76 requests per second, p50=0.703 msec
LRANGE_300 (first 300 elements): 15384.62 requests per second, p50=1.551 msec                 
LRANGE_500 (first 500 elements): 12048.19 requests per second, p50=1.927 msec
LRANGE_600 (first 600 elements): 10526.32 requests per second, p50=2.279 msec
MSET (10 keys): 38461.54 requests per second, p50=0.631 msec                  
XADD: 45454.55 requests per second, p50=0.375 msec
```

```bash
# redis-benchmark -n 100 -t set,lpush -q
SET: 50000.00 requests per second, p50=0.423 msec         
LPUSH: 99999.99 requests per second, p50=0.375 msec
```

- `-n`	指定请求数	10000
- `-q`	强制退出 redis。仅显示 query/sec 值	
- `-t`	仅运行以逗号分隔的测试命令列表。	


## Redis 客户端连接 -TBD

xxxxx

## Redis 管道技术

Redis是一种基于客户端-服务端模型以及请求/响应协议的TCP服务。这意味着通常情况下一个请求会遵循以下步骤：

- 客户端向服务端发送一个查询请求，并监听Socket返回，通常是以阻塞模式，等待服务端响应。
- 服务端处理命令，并将结果返回给客户端。

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
```

这些命令一次性向 redis 服务提交，并最终一次性读取所有服务端的响应。

管道技术最显著的优势是提高了 redis 服务的性能。

## Redis 主从复制

## Redis 哨兵模式

## Redis 分区  -- TBD

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