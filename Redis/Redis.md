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




--- 

## 高级应用

### 分布式锁

在 JVM 内部会有一个锁监视器来控制线程间的互斥，但在分布式的环境下会有多台机器部署同样的服务，也就是说每台机器都会有自己的锁监视器。而 JVM 的锁监视器只能保证自己内部线程的安全执行，并不能保证不同机器间的线程安全执行，因此也很难避免高并发带来的线程安全问题。

因此就需要分布式锁来保证整个集群的线程的安全，而分布式锁需要满足 5 点要求：
- 多进程可见
- 互斥性
- 高可用
- 高性能
- 安全性

其中核心要求就是多进程之间互斥，而满足这一点的方式有很多，最常见的有三种：mysql、Redis、Zookeeper。


不可重入：同一个线程无法多次获取同一把锁
不可重试：获取锁只能尝试一次，失败就返回 false，没有重试机制
超时释放：锁超时释放虽然可以避免死锁，但如果业务执行耗时较长，也会导致锁释放，存在安全隐患
主从一致性：如果 Redis 提供了主从集群，主从同步存在延迟，当主机宕机时，如果从机还没来得及同步主机的锁数据，则会出现锁失效。
要解决以上问题也非常简单，只需要利用 Redis 的 hash 结构记录线程标识和重入次数就可以解决不可重入的问题。利用信号量和 PubSub 功能实现等待、唤醒，获取锁失败的重试机制即可解决不可重试的问题。而超时释放的问题则可以通过获取锁时为锁添加一个定时任务(俗称看门狗)，定期刷新锁的超时时间即可。至于主从一致性问题，我们只需要利用多个独立的 Redis 节点(非主从)，必须在所有节点都获取重入锁，才算获取锁成功。


go-redis, redlock

![lock](/img/redis_lock.png)


Redis 分布式锁是一种在分布式系统中实现锁的机制，它利用 Redis 的原子性操作来保证在多个客户端之间的互斥访问。以下是 Redis 分布式锁的基本原理和关键特性：

- 原子性命令：

    - Redis 提供了一些原子性的命令，如 SET、GET、DEL 等，这些命令在执行过程中不会被其他命令中断，从而保证了操作的完整性。
    - 通常使用 SET key value EX expire-time NX 命令来实现分布式锁。SETNX（Set if Not eXists）只有在键不存在时才设置值，而 EX 参数用来设置键的过期时间，防止死锁。

- 互斥性：

    由于 SETNX 的特性，同一时间只有一个客户端能够设置成功，从而实现了锁的互斥性。

- 可重入性：

为了实现可重入性，即同一线程或进程可以多次获取同一把锁，通常会在锁的值中包含一些附加信息，如获取锁的客户端ID和获取锁的次数，这样客户端在尝试获取锁时可以检查自己是否已经持有锁。

- 锁超时：

设置锁的过期时间是为了防止客户端在持有锁时意外崩溃导致的死锁。过期时间需要根据业务逻辑设置一个合适的值，但这种方法不能完全防止死锁，因为如果客户端在锁到期前没有完成操作，可能会导致锁自动释放，而此时业务操作还在进行。

- 高可用性：

为了提高系统的高可用性，可以使用多个 Redis 节点并实现某种形式的复制，例如主从复制或哨兵模式。这样即使某个节点失败，其他节点仍然可以提供服务。

- 公平性和非公平性：

Redis 默认的 SETNX 命令是非公平的，即客户端获取锁的顺序与它们请求锁的顺序无关。
若要实现公平锁，需要额外的设计和算法，例如使用有序的请求队列。

- RedLock 算法：

为了提高可靠性，有些实现会使用多个 Redis 实例来创建一个分布式锁，称为 RedLock 算法。客户端需要在大多数实例上成功获取锁才能认为锁已被获取，这种方式增加了锁的可用性和容错性。

在实际应用中，还需要考虑锁的续期、锁的释放（确保在客户端崩溃后仍能释放锁）、锁的公平性等问题，以确保分布式锁的安全性和效率。


### 轻量化消息队列
虽然市面上有很多优秀的消息中间件如 RocketMQ、Kafka 等，但对于应用场景较为简单，只需要简单的消息传递，比如任务调度、简单的通知系统等，不需要复杂的消息路由、事务支持的业务来说，用那些专门的消息中间件成本就显得过高。因此我们就可以使用 Redis 来做消息队列。
Redis 提供了三种不同的方式来实现消息队列：

- list 结构：可以使用 list 来模拟消息队列，可以使用 BRPOP 或 BLPOP 命令来实现类似 JVM 阻塞队列的消息队列。
- PubSub：基于发布/订阅的消息模型，但不支持数据持久化，且消息堆积有上限，超出时数据丢失。
- Stream：Redis 5.0 新增的数据类型，可以实现一个功能非常完善的消息队列，也是我们实现消息队列的首选。

![message](/img/redis_message_queue.jpg)


### 缓存

- 缓存穿透

缓存穿透是指客户端的请求数据在缓存和数据库中都不存在，这样缓存永远不会生效，这些请求都会到达数据库，从而导致数据库负载过高。
常见解决方案有两种：

    缓存空对象：实现简单、方便维护，是解决缓存穿透的首选方法，但会造成额外内存消耗，或短期的数据不一致? 
    布隆过滤：内存占用少，没有多余key，但实现复杂且有可能误判?

- 缓存雪崩

缓存雪崩是指在同一时间段大量缓存 key 同时失效或 Redis 服务宕机，导致大量请求到达数据库，导致数据库负载过高。
常见解决方案如下：

    给不同的 key 的过期时间添加随机值 
    利用 Redis 集群提高服务的可用性
    给缓存业务添加限流降级策略
    给业务添加多级缓存

- 缓存击穿 

缓存击穿也叫热点 key 问题，就是一个被高并发访问并且缓存重建业务比较复杂的 key 突然失效了，无数的请求访问会在瞬间给数据库带来巨大的冲击。
常见解决方案有以下两种：

    互斥锁

    给重建缓存的逻辑加上一个互斥锁，避免多个线程同时访问数据库，这种方法通常应用在一致性要求较高的场景。

![lock](/img/redis_mutux.png)

    逻辑过期

    在缓存对象中维护一个过期时间的字段，当查询缓存时发现已过期则获取互斥锁(例如 Redis 中的 setnx)并开启一个新线程重建缓存数据并将释放互斥锁的逻辑放在新线程中，原线程返回过期数据。当在缓存重建时有其他线程访问缓存并发现数据过期时获取互斥锁失败则直接返回过期数据。这种方法通常应用在对可用性较高的场景。

![ex](/img/redis_expire.png)

![com](/img/redis_mutux_expire_com.png)




### redis一致性

Redis 作为一个内存数据存储系统，为了保证数据一致性，提供了多种策略和特性。以下是一些关键点：

主从同步：

Redis 支持主从复制，主节点接收写操作，从节点定期或实时地从主节点同步数据。这样可以保证在主节点上的写操作最终会被复制到所有从节点，实现最终一致性。

同步策略：

全量同步（Full resynchronization）：当从节点启动或者主从断开后重新连接时，主节点会进行全量同步，发送RDB（Redis Database）文件给从节点。

增量同步（Partial resynchronization）：如果主从心跳保持，主节点只需要发送自上次复制以来的命令日志（AOF，Append-Only File 或 PSYNC 命令）给从节点，实现快速同步。

异步复制：

默认情况下，Redis 使用异步复制，这意味着主节点接收到写请求后立即响应，不需要等待从节点确认，这牺牲了一定的一致性来换取更高的性能。

SYNC 命令：

旧版本的 Redis 使用 SYNC 命令进行全量同步，但在新版本中被 PSYNC 替代，以支持部分同步和更好的容错性。

一致性模型：

Redis 提供了两种一致性模型：
强一致性（sync）：写操作仅在复制到所有从节点后才返回成功，但这会影响性能。
最终一致性（async）：写操作在主节点上完成即可，不保证立即同步到从节点，适合对强一致性要求不高的场景。

原子操作：

Redis 的命令是原子的，这意味着在同一时刻，只有一个命令在执行，这有助于避免数据冲突，但不直接解决一致性问题。

Redis Sentinel：

Redis Sentinel 是一个高可用性解决方案，它监视主从节点的状态，当主节点失败时，可以自动进行故障转移，将一个从节点提升为主节点，保证服务的连续性。

Redis Cluster：

Redis Cluster 自带的分片和故障转移机制，通过数据分区和槽的迁移，可以在多个节点间保持数据的一致性。
事务（Transactions）：

Redis 的事务保证了单个客户端的多条命令执行的隔离性，但不提供跨客户端的事务一致性。
lua 脚本：

使用 Lua 脚本可以在服务器端执行原子的操作序列，确保在执行期间的隔离性。

要实现更严格的一致性，通常需要结合使用上述特性，并根据具体的应用需求和性能要求进行适当的设计和配置。例如，可以考虑在更新数据库后立即删除 Redis 缓存，或者使用发布/订阅（Pub/Sub）模式来通知其他组件数据已更新。



### rdb持久化的时候，主进程键值发生更改，写入的是新值还是旧值

在Redis的RDB（Redis Database）持久化过程中，如果主进程在执行bgsave命令（后台保存）时发生了键值更改，RDB文件会包含这些更改后的键值。这是因为RDB持久化是通过以下步骤进行的：

主进程fork出一个子进程。
子进程开始创建RDB文件，它基于fork时刻主进程的内存数据快照。
在子进程创建RDB文件期间，如果主进程接收到了新的写操作，它会使用写时复制（Copy-On-Write, COW）机制。
当主进程需要修改内存中的数据时，由于COW机制，操作系统会在需要时为主进程分配新的内存页来保存修改，而子进程继续使用未修改的旧页面来创建RDB文件。
子进程完成RDB文件的创建后，会替换旧的RDB文件。
因此，RDB文件最终会包含fork时刻之后主进程的写操作导致的新值，而不是旧值。这意味着RDB文件反映了持久化操作完成时Redis数据库的状态。




### redis基本数据类型以及底层结构
Redis 提供了五种基本数据类型，它们的底层数据结构如下：

字符串（String）：

底层数据结构通常是简单动态字符串（Simple Dynamic String, SDS）。
SDS 是一种二进制安全的字符串表示，它预分配了一定的额外空间以减少动态扩展的开销。
如果字符串存储的是整数值，且可以用 long 类型表示，Redis 可能会使用整数集合（IntSet）来优化存储，节省空间。

哈希（Hash）：

底层数据结构通常是哈希表（Hash Table）。
哈希表允许存储键值对，且支持高效的查找、插入和删除操作。

列表（List）：

底层数据结构通常是双向链表（Doubly Linked List）。
列表可以存储有序的元素，支持在两端添加和移除元素。

集合（Set）：

底层数据结构可能是整数集合（IntSet）如果所有元素都是整数，或者是普通的哈希表。
集合存储不重复的元素，支持成员的添加、删除和查询。

有序集合（Sorted Set）：

底层数据结构是跳跃表（Skip List）加上哈希表。
跳跃表允许高效地按分数排序元素，而哈希表用于快速查找元素。
这些数据结构的选择和实现优化了Redis在内存中的存储效率和操作性能，使其成为高速缓存和数据结构服务器的理想选择。



### 4.4先update再delete不一致性场景举例

Redis 事务（Transactions）通过以下方式来保证数据一致性：

原子性（Atomicity）：在事务开始（MULTI）和结束（EXEC）之间的所有命令作为一个整体执行，要么全部成功，要么全部失败。这意味着在事务内部的多个操作被视为一个单一的操作，不会被其他客户端的命令中断。

隔离性（Isolation）：在事务执行期间，其他客户端的命令不会影响事务中的命令执行。事务内部的操作是顺序执行的，看起来就像是独占了数据库。

举例：

text
   WATCH key1 key2
   // 监视key1和key2，如果它们在接下来的命令执行前被修改，则事务将不会执行
   MULTI
   INCR key1
   DECR key2
   // 开始事务
   EXEC
在这个例子中，WATCH 命令用于监视 key1 和 key2。如果在 EXEC 之前，这两个键的值被其他客户端修改，那么整个事务将会被取消，以防止脏读。然后，MULTI 开启事务，INCR 增加 key1 的值，DECR 减少 key2 的值。最后，EXEC 命令提交事务，执行所有命令。如果在 EXEC 之前没有其他客户端修改了监视的键，那么这些操作会原子性地执行。

注意：
Redis 事务不提供像关系型数据库那样的回滚（ROLLBACK）功能，如果事务中的某个命令失败，后续命令仍然会执行。
事务不提供死锁检测。
事务内部的命令顺序是确定的，但与其他客户端的命令并发执行时，执行顺序是不确定的，除非使用了WATCH命令。
因此，虽然Redis的事务提供了基本的数据一致性保证，但它们并不完全等同于传统数据库的ACID事务，而是更适合于那些对事务要求较低的场景。在需要更高级别的事务支持时，可能需要结合其他策略，如使用Lua脚本或分布式锁来增强一致性。



### 淘汰策略
Redis 缓存淘汰策略用于管理内存空间，当Redis实例达到其配置的最大内存限制(maxmemory)时，这些策略决定哪些键值对应该被移除来释放空间。以下是Redis支持的主要缓存淘汰策略：

- noeviction:
当内存达到上限时，拒绝写操作，返回错误。读操作仍然允许，除非是DEL或某些特殊命令。

- allkeys-LRU:
选择最近最少使用的键进行淘汰。LRU（Least Recently Used）算法试图保留最近最常使用的数据。

- allkeys-RAND:
随机淘汰一个键，不考虑使用频率或时间。

- volatile-LRU:
只在设置了过期时间的键中选择最近最少使用的键进行淘汰。

- volatile-TTL:
淘汰最早到期的键，即具有最短生存时间（TTL）的键。

- volatile-RAND:
在设置了过期时间的键中随机淘汰一个键。

- volatile-lfu:
Redis 4.0及更高版本引入，使用LFU（Least Frequently Used）算法，淘汰最近最少访问的键。LFU考虑了访问频率，相比LRU更倾向于保留经常但不总是访问的键。




### 注册中心 服务发现

edis 也可以用作服务注册中心和服务发现的组件，虽然它并不是专门为这个目的设计的，但其数据结构和功能可以适应这种用途。以下是使用 Redis 实现服务注册与发现的基本步骤：

服务注册：

服务提供者（Service Provider）启动时，它会将自身的信息（如服务ID、IP地址、端口、版本号等）作为一个键值对存储在 Redis 中。通常，服务ID作为键，服务元数据作为JSON或其他格式的值。
示例命令：

```bash
   SET service:<service-name>:<instance-id> '{"ip": "192.168.1.1", "port": 8080, "version": "1.0.0"}'
```
服务发现：

服务消费者（Service Consumer）通过查询 Redis 来获取服务提供者的列表。可以使用 SCAN 命令遍历服务相关的键，或者使用 GET 命令获取特定服务的实例信息。
示例查询：

```bash
   SCAN 0 MATCH "service:*" COUNT 100
```

发布/订阅模型：

为了实时通知服务的增减，服务提供者和消费者可以利用 Redis 的发布/订阅（Pub/Sub）机制。服务提供者在服务上线或下线时发布消息到特定频道，订阅这些频道的服务消费者会接收到这些通知。

示例：

提供者：
```bash
     PUBLISH service-updates "<service-name>:<instance-id>"
```

消费者：
```bash
     SUBSCRIBE service-updates
```

健康检查：

服务提供者可以定期向 Redis 发送心跳信号，表明其还在运行。服务消费者可以通过检查这些心跳来判断服务是否可用。

版本管理和负载均衡：

可以通过添加额外的键值对来跟踪服务的不同版本，然后在服务消费者端实现负载均衡策略，如轮询、权重分配等。

客户端库：

开发者通常会使用客户端库（如 redis-py for Python 或 Jedis for Java）来更方便地与 Redis 交互，这些库提供了高级接口来简化服务注册和发现的操作。
请注意，虽然 Redis 可以胜任服务注册与发现的角色，但它可能不如专门为此设计的工具（如 ZooKeeper、Consul 或 Eureka）那样成熟和完善。在实际生产环境中，应权衡性能、复杂性和稳定性等因素来选择最适合的解决方案。