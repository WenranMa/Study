# 事务

## 1. 什么是数据库事务？

事务是一个不可分割的数据库操作序列，也是数据库并发控制的基本单位，其执行的结果必须使数据库从一种一致性状态变到另一种一致性状态。

事务处理的原则：保证所有事务都作为 一个工作单元 来执行，即使出现了故障，都不能改变这种执行方式。当在一个事务中执行多个操作时，要么所有的事务都被提交( commit )，那么这些修改就永久地保存下来；要么数据库管理系统将 放弃 所作的所有 修改 ，整个事务回滚( rollback )到最初状态。

事务最经典也经常被拿出来说例子就是转账了。

假如小明要给小红转账1000元，这个转账会涉及到两个关键操作就是：将小明的余额减少1000元，将小红的余额增加1000元。万一在这两个操作之间突然出现错误比如银行系统崩溃，导致小明余额减少而小红的余额没有增加，这样就不对了。事务就是保证这两个关键操作要么都成功，要么都要失败。

对于一个事务, 要么事务内的SQL全部执行, 要么都不执行
```sql
START TRANSACTION;
SELECT balance FROM checking WHERE customer_id = 10233276;
UPDATE checking SET balance = balance - 200.00 WHERE customer_id = 10233276;
UPDATE savings SET balance = balance + 200.00 WHERE customer_id = 10233276;
COMMIT;
```

## 2. 开启事务

1. 显式事务

使用关键字start transction或begin开启事务，使用commit提交事务，使用rollback回滚事务。例如：
```sql
-- 开启事务
begin;
-- 插入数据 1
insert into demo_table values(1);
-- 提交事务，事务结束
commit;
-- 开启另一个事务
start transtion;
-- 插入数据 2
insert into demo_table values(2);
-- 回滚事务(回滚到上次提交事务的状态)，此时数据 2 并不会写入数据库，事务结束
rollback;
-- 开启事务
begin;
-- 插入数据 3
insert into demo_table values(3);
-- 设置保存点 s1
savepoint s1;
-- 插入数据 4
insert into demo_table values(4);
-- 回滚到保存点 s1，此时数据 3 会被保存(内存)，而数据 4 并不会保存(内存)，事务并没有结束
rollback to s1;
-- 提交事务，此时数据 3 才真正写入磁盘，事务结束
commit;
```
start transction 可以跟 read only / read write / with consistent snapshot

read only：表示当前事务是一个只读事务，也就是属于该事务的数据库操作只能读取数据，而不能修改数据。(只读事务只是不允许修改那些其他事务也能访问到的表中的数据，对于临时[使用 create tmeporary table 创建的表]表来说，由于它们只能在当前会话中可见，所以只读事务也是可以对临时表进行增、删、改操作的)
read write：表示当前事务是一个读写事务，也就是属于该事务的数据库操作既可以读取数据，也可以修改数据。
with consistent snapshop：启动一致性读。

2. 隐式事务

mysql 中有一个系统变量autocommit(默认值 ON)，默认请情况下，如果我们不显式使用 start transaction 或 begin 语句开启一个事务，那么每一条 DML(数据库操作语言) 语句都算是一个独立的事务，这种特性称之为事务的自动提交。如果我们想关闭这种自动提交的功能可以使用显式事务或把 autocommit 的值改为 OFF。这样的话，我们写入多条语句就算是属于同一个事务了，直到我们显式写出 commit 语句提交事务或写出 rollback 回滚事务才可以真正修改数据。

## 3. 事务的特性 ACID

- 原子性(atomicity)：原子性是指事务是一个不可分割的工作单位，要么全部提交，要么全部失败回滚。
- 一致性(consistency)：一致性是指事务执行前后，从一个合法性状态(满足预定的约束的状态)变换到另一个合法性状态。这种状态是语义上的而不是语法上的，跟具体的业务有关。如果数据库系统 运行中发生故障，有些事务尚未完成就被迫中断，这些未完成事务对数据库所做的修改有一部分已写入物理数据库，这时数据库就处于一种不正确的状态，或者说是 不一致的状态。

那什么是合法的数据状态呢？满足 预定的约束 的状态就叫做合法的状态。通俗一点，这状态是由你自己来定义的（比如满足现实世界中的约束）。满足这个状态，数据就是一致的，不满足这个状态，数据就是不一致的！如果事务中的某个操作失败了，系统就会自动撤销当前正在执行的事务，返回到事务操作之前的状态。

- 隔离性(isolation)：隔离性是指事务的执行不能被其他事务干扰，即一个事务内部的操作及使用的数据对并发的其他事务是隔离的，并发执行的各个事务之间不能互相干扰。
- 持久性(durability)：持久性是指一个事务一旦被提交，他对数据库的改变就是永久性的，接下来的其他操作和数据库故障不应对其有任何影响。持久性是通过事务日志来保证的，包括了重做日志和回滚日志。

持久性是通过 事务日志 来保证的。日志包括了 重做日志 和 回滚日志 。当我们通过事务对数据进行修改的时候，首先会将数据库的变化信息记录到重做日志中，然后再对数据库中对应的行进行修改。这样做的好处是，即使数据库系统崩溃，数据库重启后也能找到没有更新到数据库系统中的重做日志，重新执行，从而使事务具有持久性。

## 4. 事务的状态
- 活动的(active)：事务对应的数据库操作正在执行过程中，我们就说该事物处在活动的状态。
- 部分提交的(partially committed)：当事务中的最后一个操作执行完成，但由于操作都在内存中执行，所造成的影响并没有刷新到磁盘时，我们就说该事务处在部分提交的状态。
- 失败的(failed)：当事务处在活动的或部分提交的状态时，可能遇到了某些错误(数据库自身错误、操作系统错误或直接断电等)而无法继续执行，或者人为的停止当前事务的执行，我们就说该事务处在失败的状态。
- 中止的(aborted)：如果事务执行了一部分操作后变为了失败的状态，那么就需要把已经修改的事务中的操作还原到事务执行前的状态。我们把这个撤销的过程称之为回滚。当回滚操作完毕时，也就是数据库恢复到了执行事务之前的状态，我们就说该事务处在了中止的状态。
- 提交的(committed)：当一个处在部分提交的状态的事务将修改过的数据都同步到磁盘上之后，我们就可以说该事务处在了提交的状态。

一个基本的状态转换图如下所示：
![image.png](https://cdn.nlark.com/yuque/0/2022/png/22219483/1655343228326-9c236f52-d4e0-4fe7-84c9-9ce989e13e2e.png#averageHue=%23fbfbfb&clientId=u93f3805a-794b-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=404&id=ue26b1dc2&margin=%5Bobject%20Object%5D&name=image.png&originHeight=404&originWidth=555&originalType=binary&ratio=1&rotation=0&showTitle=false&size=57775&status=done&style=none&taskId=u7b06426a-2d47-4624-8efa-c347eff5066&title=&width=555)

## 5. 并发的问题

- **丢失修改 Lost to modify** (脏写？？？)
指在一个事务读取一个数据时，另外一个事务也访问了该数据，那么在第一个事务中修改了这个数据后，第二个事务也修改了这个数据。这样第一个事务内的修改结果就被丢失，因此称为丢失修改
- **脏读 Dirty Read**
当一个事务正在访问数据并且对数据进行了修改，而这种修改还没有提交到数据库中，这时另外一个事务也访问了这个数据，然后使用了这个数据。因为这个数据是还没有提交的数据，那么另外一个事务读到的这个数据是“脏数据”，依据“脏数据”所做的操作可能是不正确的
- **不可重复读 Unrepeatable Read**
指在一个事务内多次读同一数据。在这个事务还没有结束时，另一个事务也访问该数据。那么，在第一个事务中的两次读数据之间，由于第二个事务的修改导致第一个事务两次读取的数据可能不太一样。这就发生了在一个事务内两次读到的数据是不一样的情况，因此称为不可重复读. 侧重点为修改.
- **幻读 Phantom Read**
幻读与不可重复读类似。它发生在一个事务（T1）读取了几行数据，接着另一个并发事务（T2）插入了一些数据时。在随后的查询中，第一个事务（T1）就会发现多了一些原本不存在的记录，就好像发生了幻觉一样，所以称为幻读. 侧重点为新增或删除.

## 6. 隔离级别
mysql 是客户端/服务器架构的软件，对于一个服务器来说，可以有若干个客户端与之连接，每个客户端与服务器连接之后，就可以称之为一个会话(session)。每个客户端都可以在自己的会话中向服务器发出请求语句，一个请求语句可能是某个事务的一部分，可就是对于服务器来说可能同时处理多个事务。事务有隔离性的特性，理论上在某个事务对某个数据进行访问时，其他事物应该进行排队，当事务提交之后，其他事务才可以继续访问这个数据。但是这样对性能的影响太大，我们既想保持事务的隔离性，又想让服务器在处理访问同一数据的多个事务时性能尽量高些，因此就需要采用适当的隔离级别。

mysql 查看隔离级别
```sql
-- mysql 5.7.20 之前查看隔离级别
show variables like 'tx_isolation';
-- mysql 5.7.20 之后查看隔离级别
show variables like 'transaction_isolation';
-- 查看隔离级别(各版本都可以使用)
select @@transaction_isolation;

-- mysql 设置隔离级别
/*
隔离级别：READ UNCOMMITTED、READ COMMITTED、REPEATABLE READ、SERIALIZABLE
*/
set [global | session] transaction isolation level 隔离级别;
或者

/*
隔离级别：READ-UNCOMMITTED、READ-COMMITTED、REPEATABLE-READ、SERIALIZABLE
*/
set [global | session] transaction_isolation='隔离级别';
```

SQL 的隔离级别(从低到高)
- READ UNCOMMITTED：读未提交，在该隔离级别，所有事务都可以看到其他未提交事务的执行结果。本隔离级别很少用于实际应用，因为它的性能也不比其他级别好多少。仅能避免脏写，不能避免脏读、不可重复读、幻读。
- READ COMMITTED：读已提交，它满足了隔离级别的简单定义(一个事务只能看见已提交事务所做的改变)。可以避免脏写、脏读，但不能避免不可重复读、幻读。
- REPEATABLE READ：可重复读，事务 A 在读到一条数据之后，此时事务 B 对该数据进行了修改并提交，那么事务 A 再读改数据，读到的还是原来的内容。可以避免脏写、脏读、不可重复读，但幻读问题仍然存在。mysql 默认的隔离级别
- SERIALIZABLE：可串行化，强制事务排序，确保事务可以从一个表中读取相同的行。在这个事务持续期间，禁止其他事务对该表执行插入、更新和删除操作。该级别所有并发问题都可以避免，可能导致大量的超时现象和锁竞争，性能十分低下。

因为隔离级别越低，事务请求的锁越少，所以大部分数据库系统的隔离级别都是READ-COMMITTED(读取提交内容)，但InnoDB 存储引擎默认使用 `REPEATABLE-READ（可重读）` 并不会有任何性能损失。所以MySQL 默认采用的 REPEATABLE_READ隔离级别。

InnoDB 存储引擎在 分布式事务 的情况下一般会用到**SERIALIZABLE(可串行化)**隔离级别。

事务隔离机制的实现基于锁机制和并发调度。其中并发调度使用的是MVVC（多版本并发控制），通过保存修改的旧版本信息来支持并发一致性读和回滚等特性。

| 隔离级别 | 说明 |
| --- | --- |
| 读未提交 | 一个事务还没提交时，它做的变更就能被别的事务看到 |
| 读提交 | 一个事务提交之后，它做的变更才会被其他事务看到 |
| 可重复读 | 一个事务中，对同一份数据的读取结果总是相同的，无论是否有其他事务对这份数据进行操作，以及这个事务是否提交。InnoDB默认级别。 |
| 串行化 | 事务串行化执行，每次读都需要获得表级共享锁，读写相互都会阻塞，隔离级别最高，牺牲系统并发性。 |

不同的隔离级别是为了解决不同的问题。也就是脏读、幻读、不可重复读。

| 隔离级别 | 脏读 | 不可重复读 | 幻读 |
| --- | --- | --- | --- |
| 读未提交 | 可以出现 | 可以出现 | 可以出现 |
| 读提交 | 不允许出现 | 可以出现 | 可以出现 |
| 可重复读 | 不允许出现 | 不允许出现 | 可以出现 |
| 串行化 | 不允许出现 | 不允许出现 | 不允许出现 |

### 隔离级别演示：
```sql
 CREATE TABLE `student` (
   `id` bigint(20) NOT NULL COMMENT '学生编号',
   `name` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '' COMMENT '学生姓名',
   `birth` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '' COMMENT '出生年月',
   `sex` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '' COMMENT '学生性别',
   PRIMARY KEY (`id`)
 ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='学生表';
 
 insert  into `student`(`id`,`name`,`birth`,`sex`) values 
 (1,'赵雷','1990-01-01','男'),
 (2,'钱电','1990-12-21','男'),
 (3,'孙风','1990-05-20','男'),
 (4,'李云','1990-08-06','男');
```
 
1. 读未提交（Read Uncommitted）

在该隔离级别，所有事务都可以看到其他事务未提交的执行结果。读取未提交的数据，也被称之为脏读。本隔离级别很少用于实际应用，因为它的性能也不比其他级别好多少。

演示：将事务T1设置为read uncommitted
![iso1](/img/mysql_iso_01.png)

经过上面的实验可以得出结论，T1在T2修改和插入操作前后两次读取的数据不一致，当T2未提交时，T1读到了T2未提交的数据，即称之为脏读，该实验同时也出现了幻读和不可重复读。

2. 读已提交（Read Committed）

在一个事务中，可以读取到其他事务已经提交的数据，比如事务T1的两条相同的查询语句之间，被事务T2执行修改数据并提交，那么事务T1第二次读取到了T2已提交的数据，先后两次读取的数据不一致，这种读取也就叫做不可重复读，因为两次同样的查询可能会得到不一样的结果。

演示：将事务T1设置为Read Committed
![iso2](/img/mysql_iso_02.png)

经过上面的实验可以得出结论，读已提交解决了脏读现象，但是前后两次读取的数据不一致，所以依然存在不可重复读和幻读的现象。

3. 可重复读（Repeatable Read）

MySQL默认的隔离级别，在一个事务中，直到事务结束前，都可以反复读取到事务最开始时读取到的数据，并一直不会发生变化，避免了脏读、不可重复读现象，但是它还是无法解决幻读问题。

简单的说，幻读指当用户读取某一范围的数据行时，另一个事务又在该范围内插入了新行，当用户再读取该范围的数据行时，会读取到新的“幻影” 行。InnoDB和Falcon存储引擎通过多版本并发控制（MVCC，Multiversion Concurrency Control）机制解决了该问题。

演示：将事务T1设置为Repeatable Read
![iso3](/img/mysql_iso_03.png)

经过上面的实验可以得出结论，不论是在T2对数据更新和是否提交事务的前后，T1每次读取的数据都是一致的。但是仔细地同学会发现，在可重复读的级别下，事务T2插入了一条新的数据，但是T1却并未出现幻读地情况。按照上面地不同的隔离级别会引发的问题对照表中的描述，可重复读是会出现幻读的，这又是怎么回事呢。这里需要提到一点，多版本并发控制(Multi-Version Concurrency Control, MVCC)这样一种机制（知识点，要考！！本篇不做详解），它解决了插入情况下的幻读，但是下面的修改操作依旧存在幻读问题。

![iso4](/img/mysql_iso_04.png)

从上面的实验可以发现，T1在不知道还有其他事务干扰的情况下进行修改操作，不出意外的情况下应该更新第一次读取到的4条数据，但是最后却查出了5条被更新的记录，此时即发生了幻读，将新读取（幻读）出来的一条数据也同时更新了。

4. 可串行化（Serializable）

这是最高的隔离级别，它强制事务串行执行，使之不可能相互冲突，避免了前面说的幻读现象，简单来说，它会在读取的每一行数据上都加锁，所以可能会导致大量的超时和锁竞争，一般不推荐使用。

![iso5](/img/mysql_iso_05.png)

从上面的实验可以发现，当两个事务并发操作同一份数据时，必然会有一个事务进入等待状态，直到另外的事务结束才能继续执行。

## 7. 事务的实现原理
事务是基于重做日志文件(redo log)和回滚日志(undo log)实现的。
每提交一个事务必须先将该事务的所有日志写入到重做日志文件进行持久化，数据库就可以通过重做日志来保证事务的原子性和持久性。
每当有修改事务时，还会产生 undo log，如果需要回滚，则根据 undo log 的反向语句进行逻辑操作，比如 insert 一条记录就 delete 一条记录。undo log 主要实现数据库的一致性。

### 原子性
利用Innodb的undo log。
undo log名为回滚日志，是实现原子性的关键，当事务回滚时能够撤销所有已经成功执行的sql语句，他需要记录你要回滚的相应日志信息。
例如

- (1)当你delete一条数据的时候，就需要记录这条数据的信息，回滚的时候，insert这条旧数据
- (2)当你update一条数据的时候，就需要记录之前的旧值，回滚的时候，根据旧值执行update操作
- (3)当年insert一条数据的时候，就需要这条记录的主键，回滚的时候，根据主键执行delete操作

undo log记录了这些回滚需要的信息，当事务执行失败或调用了rollback，导致事务需要回滚，便可以利用undo log中的信息将数据回滚到修改之前的样子。

### 持久性
redo log 保证了持久性，事务提交了，redo log的内容就会flush到磁盘中。

Mysql是先把磁盘上的数据加载到内存中，在内存中对数据进行修改，再刷回磁盘上。如果此时突然宕机，内存中的数据就会丢失。怎么解决这个问题？简单，事务提交前直接把数据写入磁盘就行啊。但这么做有什么问题？

- 只修改一个页面里的一个字节，就要将整个页面刷入磁盘，太浪费资源了。毕竟一个页面16kb大小，你只改其中一点点东西，就要将16kb的内容刷入磁盘，听着也不合理。
- 毕竟一个事务里的SQL可能牵涉到多个数据页的修改，而这些数据页可能不是相邻的，也就是属于随机IO。显然操作随机IO，速度会比较慢。

于是，决定采用redo log解决上面的问题。当做数据修改的时候，不仅在内存中操作，还会在redo log中记录这次操作。当事务提交的时候，会将redo log日志进行刷盘(redo log一部分在内存中，一部分在磁盘上)。当数据库宕机重启的时候，会将redo log中的内容恢复到数据库中，再根据undo log和binlog内容决定回滚数据还是提交数据。

redo log进行刷盘比对数据页刷盘效率高，具体表现如下

- redo log体积小，毕竟只记录了哪一页修改了啥，因此体积小，刷盘快。
- redo log是一直往末尾进行追加，属于顺序IO。效率显然比随机IO来的快。

### 隔离性
mysql采用mvcc进行，通过版本链、read view以及隐藏的三个字段来实现

利用的是锁和MVCC机制。
至于MVCC,即多版本并发控制(Multi Version Concurrency Control),一个行记录数据有多个版本对快照数据，这些快照数据在undo log中。
如果一个事务读取的行正在做DELELE或者UPDATE操作，读取操作不会等行上的锁释放，而是读取该行的快照版本。

但是有一点说明一下，在事务隔离级别为读已提交(Read Commited)时，一个事务能够读到另一个事务已经提交的数据，是不满足隔离性的。但是当事务隔离级别为可重复读(Repeateable Read)中，是满足隔离性的。

### 一致性
这个问题分为两个层面来说。
从**数据库层面**，数据库通过原子性、隔离性、持久性来保证一致性。也就是说ACID四大特性之中，C(一致性)是目的，A(原子性)、I(隔离性)、D(持久性)是手段，是为了保证一致性，数据库提供的手段。数据库必须要实现AID三大特性，才有可能实现一致性。例如，原子性无法保证，显然一致性也无法保证。
但是，如果你在事务里故意写出违反约束的代码，一致性还是无法保证的。例如，你在转账的例子中，你的代码里故意不给B账户加钱，那一致性还是无法保证。因此，还必须从应用层角度考虑。
从**应用层面**，通过代码判断数据库数据是否有效，然后决定回滚还是提交数据！


## 8. redo log（重写日志）
redo log 是物理日志, 记录的是"在某个数据页做出了什么修改", 属于 `InnoDB存储引擎` 层面.

当有一条记录需要更新的时候, InnoDB引擎会先把记录写到 redo log 中, 并更新内存, 这时候更新就算完成. 同时, InnoDB引擎会在适当的时候, 将这个操作记录更新到磁盘里面, 往往是系统较为空闲时.

InnoDB的redo log是固定大小的, 如可以配置为一组4个文件, 每个文件1GB, 那么redo log总共就可以记录4GB的操作. 从头开始写, 写到末尾又回到开头循环写.
![image-20220304195247657.png](https://cdn.nlark.com/yuque/0/2022/png/21380271/1646468474598-8d818589-d1ec-4e9a-ae1b-bbb9540d96ea.png#averageHue=%23dfe6d4&clientId=ub63f7278-093b-4&crop=0&crop=0&crop=1&crop=1&from=ui&id=GuR8t&margin=%5Bobject%20Object%5D&name=image-20220304195247657.png&originHeight=214&originWidth=547&originalType=binary&ratio=1&rotation=0&showTitle=false&size=62322&status=done&style=none&taskId=ue7ee8264-f69f-4f72-9b9d-b2c439271c0&title=)

**write pos** 是当前记录的位置, 边写边后移, 写到第三号文件末尾后就回到0号文件开头.

**checkpoint** 是当前要擦除的位置, 也是往后推移并循环的, 擦除记录前要把记录更新到数据文件.

**write pos** 和 **checkpoint** 之间是空闲的部分, 可以用来记录新的操作, 如果 **write pos** 追上 **checkpoint** ,表示 redo log 满了, 这时不能再执行新的更新, 得停下先擦掉一些记录, 把 **checkpoint** 推进.

有了 redo log, InnoDB 可以保证即使数据库发生异常重启, 之前提交的记录都不会丢失, 这个能力被称为 **crash-safe**。

redo log 不是随着事务的提交才写入的，而是在事务的执行过程中，便开始写入 redo 中。具体的落盘策略可以进行配置。防止在发生故障的时间点，尚有脏页未写入磁盘，在重启 MySQL 服务的时候，根据 redo log 进行重做，从而达到事务的未入磁盘数据进行持久化这一特性。RedoLog 是为了实现事务的持久性而出现的产物

### redo log 与持久性
对于一个已经提交的事务，在事务提交后即使系统发生了崩溃，这个事务对数据库中所做的更改也不能丢失。

那么如何保证这个持久性呢？ 一个简单的做法 ：在事务提交完成之前把该事务所修改的所有页面都刷新到磁盘，但是这个简单粗暴的做法有些问题

另一个解决的思路 ：我们只是想让已经提交了的事务对数据库中数据所做的修改永久生效，即使后来系统崩溃，在重启后也能把这种修改恢复出来。所以我们其实没有必要在每次事务提交时就把该事务在内存中修改过的全部页面刷新到磁盘，只需要把 修改 了哪些东西 记录一下 就好。比如，某个事务将系统表空间中 第10号 页面中偏移量为 100 处的那个字节的值 1 改成 2 。我们只需要记录一下：将第0号表空间的10号页面的偏移量为100处的值更新为 2 。

### REDO日志的好处、特点
- redo日志降低了刷盘频率
- redo日志占用的空间非常小
- redo日志是顺序写入磁盘的
- 事务执行过程中，redo log不断记录

### redo的组成
Redo log可以简单分为以下两个部分：

- 重做日志的缓冲 (redo log buffer) ，保存在内存中，是易失的。

**参数设置：innodb_log_buffer_size：**
redo log buffer 大小，默认 16M ，最大值是4096M，最小值为1M。
```sql
mysql> show variables like '%innodb_log_buffer_size%';
+------------------------+----------+
| Variable_name          | Value
+------------------------+----------+
| innodb_log_buffer_size | 16777216 |
+------------------------+----------+
```

- 重做日志文件 (redo log file) ，保存在硬盘中，是持久的。

### redo的整体流程
以一个更新事务为例，redo log 流转过程，如下图所示：
![image.png](https://cdn.nlark.com/yuque/0/2022/png/22219483/1655385880949-8b99c805-e7fe-48f5-90b6-45b5575da558.png#averageHue=%23f8f9f6&clientId=u3fe4f8a9-affe-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=237&id=ub6795cbc&margin=%5Bobject%20Object%5D&name=image.png&originHeight=237&originWidth=776&originalType=binary&ratio=1&rotation=0&showTitle=false&size=85093&status=done&style=none&taskId=u4461b7e8-dc60-498d-964a-ed6fa9a0e09&title=&width=776)
1. 先将原始数据从磁盘中读入内存中来，修改数据的内存拷贝
2. 生成一条重做日志并写入redo log buffer，记录的是数据被修改后的值
3. 当事务commit时，将redo log buffer中的内容刷新到 redo log file，对 redo log file采用追加写的方式
4. 定期将内存中修改的数据刷新到磁盘中

#### 5 redo log的刷盘策略
redo log的写入并不是直接写入磁盘的，InnoDB引擎会在写redo log的时候先写redo log buffer，之后以一定的频率 刷入到真正的redo log file 中。这里的一定频率怎么看待呢？这就是我们要说的刷盘策略。

注意，redo log buffer刷盘到redo log file的过程并不是真正的刷到磁盘中去，只是刷入到 文件系统缓存（page cache）中去（这是现代操作系统为了提高文件写入效率做的一个优化），真正的写入会交给系统自己来决定（比如page cache足够大了）。那么对于InnoDB来说就存在一个问题，如果交给系统来同步，同样如果系统宕机，那么数据也丢失了（虽然整个系统宕机的概率还是比较小的）。针对这种情况，InnoDB给出 innodb_flush_log_at_trx_commit 参数，该参数控制 commit提交事务时，如何将 redo log buffer 中的日志刷新到 redo log file 中。它支持三种策略：

- 设置为0 ：表示每次事务提交时不进行刷盘操作。（系统默认master thread每隔1s进行一次重做日志的同步）
- 设置为1 ：表示每次事务提交时都将进行同步，刷盘操作（ 默认值 ）
- 设置为2 ：表示每次事务提交时都只把 redo log buffer 内容写入 page cache，不进行同步。由os自己决定什么时候同步到磁盘文件。

## 9. undo log
事务未提交之前，Undo 保存了未提交之前的版本数据，Undo 中的数据可作为数据旧版本快照供其他并发事务进行快照读。在 MySQL innodb 存储引擎中用来实现多版本并发控制(MVCC)。

每次开启一个事务，则mysql的innodb引擎就会生成一张**undo log**文件，该文件主要记录这个事务ID所产生的一些更新、删除、插入操作。

当事务1执行update的时候，就会将udpate记录到undo log文件，当事务进行commit的时候，就会将undo log文件删除，如果回滚时，则会根据undo log文件的内容进行执行插入回滚SQL脚本。

### Undo日志的作用
- 作用1：回滚数据
- 作用2：MVCC

### undo的存储结构

1. 回滚段与undo页
InnoDB对undo log的管理采用段的方式，也就是 回滚段（rollback segment） 。每个回滚段记录了1024 个 undo log segment ，而在每个undo log segment段中进行 undo页 的申请。
- 在 InnoDB1.1版本之前 （不包括1.1版本），只有一个rollback segment，因此支持同时在线的事务限制为 1024 。虽然对绝大多数的应用来说都已经够用。
- 从1.1版本开始InnoDB支持最大 128个rollback segment ，故其支持同时在线的事务限制提高到了 128*1024 。
```sql
mysql> show variables like 'innodb_undo_logs';
+------------------+-------+
| Variable_name | Value |
+------------------+-------+
| innodb_undo_logs | 128 |
+------------------+-------+
```

2. 回滚段与事务
   1. 每个事务只会使用一个回滚段，一个回滚段在同一时刻可能会服务于多个事务。
   2. 当一个事务开始的时候，会制定一个回滚段，在事务进行的过程中，当数据被修改时，原始的数
据会被复制到回滚段。
   3. 在回滚段中，事务会不断填充盘区，直到事务结束或所有的空间被用完。如果当前的盘区不够
用，事务会在段中请求扩展下一个盘区，如果所有已分配的盘区都被用完，事务会覆盖最初的盘
区或者在回滚段允许的情况下扩展新的盘区来使用。
   4. 回滚段存在于undo表空间中，在数据库中可以存在多个undo表空间，但同一时刻只能使用一个
undo表空间。
   5. 当事务提交时，InnoDB存储引擎会做以下两件事情：
将undo log放入列表中，以供之后的purge操作
判断undo log所在的页是否可以重用，若可以分配给下个事务使用
3. 回滚段中的数据分类	
   1. 未提交的回滚数据(uncommitted undo information)
   2. 已经提交但未过期的回滚数据(committed undo information)
   3. 事务已经提交并过期的数据(expired undo information)

### undo的类型
在InnoDB存储引擎中，undo log分为：

- insert undo log
- update undo log

### undo redo log总结
![image.png](https://cdn.nlark.com/yuque/0/2022/png/22219483/1655387070230-7902c807-f5c4-4cc3-b2b9-7de80264d326.png#averageHue=%2389ada8&clientId=u3fe4f8a9-affe-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=410&id=ue5129c3a&margin=%5Bobject%20Object%5D&name=image.png&originHeight=410&originWidth=829&originalType=binary&ratio=1&rotation=0&showTitle=false&size=163277&status=done&style=none&taskId=u7fe50653-4d50-45cb-8072-6333e03242a&title=&width=829)

undo log是逻辑日志，对事务回滚时，只是将数据库逻辑地恢复到原来的样子。
redo log是物理日志，记录的是数据页的物理变化，undo log不是redo log的逆过程。

## 10. 什么是MySQL的 binlog？

MySQL的 binlog 是记录所有数据库表结构变更（例如 CREATE、ALTER TABLE）以及表数据修改（INSERT、UPDATE、DELETE）的二进制日志。binlog 不会记录 SELECT 和 SHOW 这类操作，因为这类操作对数据本身并没有修改，但你可以通过查询通用日志来查看 MySQL 执行过的所有语句。

MySQL binlog 以事件形式记录，还包含语句所执行的消耗的时间，MySQL 的二进制日志是事务安全型的。binlog 的主要目的是复制和恢复。

binlog是逻辑日志, 记录的是SQL语句的原始逻辑, 属于 `MySQL Server` 层面.
binlog 主要用来保证数据的一致性, 在主从等环境下, 需要通过 binlog 来进行数据的同步.
![image-20220304200528837.png](https://cdn.nlark.com/yuque/0/2022/png/21380271/1646468485491-e2e4e686-f1b2-4bf0-ae12-05538a835fe8.png#averageHue=%23cafbc9&clientId=ub63f7278-093b-4&crop=0&crop=0&crop=1&crop=1&from=ui&id=woc8w&margin=%5Bobject%20Object%5D&name=image-20220304200528837.png&originHeight=434&originWidth=983&originalType=binary&ratio=1&rotation=0&showTitle=false&size=85666&status=done&style=none&taskId=ue9b2d913-ea22-4e58-9596-baa453fdd55&title=)
binlog 日志有三种记录格式

- **statement**
这个记录的内容是SQL语句的原文, 同步数据时, 会执行记录的SQL语句, 但如果存在 `update_time = now()` 这种实时性强的SQL语句, 那么两次操作的时间不一样就会导致数据不一致问题.
- **row**
指定为 row 时, 记录的内容包含了操作的具体数据, 解决了 statement 格式的问题, 但是有数据的存在说明需要空间占用, 恢复与同步时会更消耗 IO 资源, 影响执行速度.
- **mixed**
作为以上两种的折中方案, 通过判断SQL语句是否会带来数据不一致问题而采用 statement 或 row
### MySQL的binlog有几种录入格式?分别有什么区别?
有三种格式,statement,row和mixed.

- statement模式下,记录单元为语句.即每一个sql造成的影响会记录.由于sql的执行是有上下文的,因此在保存的时候需要保存相关的信息,同时还有一些使用了函数之类的语句无法被记录复制.
- row级别下,记录单元为每一行的改动,基本是可以全部记下来但是由于很多操作,会导致大量行的改动(比如alter table),因此这种模式的文件保存的信息太多,日志量太大。
- mixed. 一种折中的方案,普通操作使用statement记录,当无法使用statement的时候使用row. 此外,新版的MySQL中对row级别也做了一些优化,当表结构发生变化的时候,会记录语句而不是逐行记录.
### 两阶段提交
redo log 让 InnoDB 存储引擎拥有 crash-safe 能力; binlog 保证了 MySQL 集群下的数据一致性.
redo log 在事务执行过程中可以不断写入, 而 binlog 只有在提交事务时才写入, 两者写入时机不同.

假设有一个事务正在执行, 执行过程中已经写入了 redo log, 而提交完后 binlog写入时发生异常, 那么在 binlog 中可能就没有对应的更新记录, 之后从库使用 binlog 恢复时, 导致少一次更新操作. 而主库用 redo log 进行恢复, 操作则正常. 最终导致这两个库的数据不一致.

于是 InnoDB存储引擎 使用**两阶段提交**方案 : 将 redo log 的写入拆成了两个步骤 **prepare** 和 **commit**

1. 执行事务时写入redo log (这时处于prepare)
2. 提交事务之前, 先写入 binlog
3. 最后提交事务, 并将 redo log 进行 commit

若使用 redo log 恢复数据时, 发现处于 prepare 阶段, 且没有 binlog, 则会回滚该事务. 若 redo log commit 时异常, 但是存在对应 binlog, MySQL还是认为这一组操作是有效的, 并不会进行回滚.

![image-20220304202100774.png](https://cdn.nlark.com/yuque/0/2022/png/21380271/1646468496177-312faa13-aa9e-4568-bb48-ad3e960f7dd9.png#averageHue=%23e1e7d6&clientId=ub63f7278-093b-4&crop=0&crop=0&crop=1&crop=1&from=ui&id=Ux6md&margin=%5Bobject%20Object%5D&name=image-20220304202100774.png&originHeight=640&originWidth=433&originalType=binary&ratio=1&rotation=0&showTitle=false&size=141141&status=done&style=none&taskId=u4adb75c5-7cc8-47c7-a651-64c8aa2de9b&title=)


## 11. MySQL中的六种日志
#### （一）概述
MySQL中存在着以下几种日志：重写日志（redo log）、回滚日志（undo log）、二进制日志（bin log）、错误日志（error log）、慢查询日志（slow query log）、一般查询日志（general log）。
MySQL中的数据变化会体现在上面这些日志中，比如事务操作会体现在redo log、undo log以及bin log中，数据的增删改查会体现在 binlog 中。本章是对MySQL日志文件的概念及基本使用介绍，不涉及底层内容。针对开发人员而言，这几种日志中最有可能使用到的是慢查询日志。
#### （二）redo log
redo log是一种基于磁盘的数据结构，用来在MySQL宕机情况下将不完整的事务执行数据纠正，redo日志记录事务执行后的状态。
当事务开始后，redo log就开始产生，并且随着事务的执行不断写入redo log file中。redo log file中记录了xxx页做了xx修改的信息，我们都知道数据库的更新操作会在内存中先执行，最后刷入磁盘。
redo log就是为了恢复更新了内存但是由于宕机等原因没有刷入磁盘中的那部分数据。
#### （三）undo log

1. undo log主要用来回滚到某一个版本，是一种逻辑日志。undo log记录的是修改之前的数据，比如：当delete一条记录时，undolog中会记录一条对应的insert记录，从而保证能恢复到数据修改之前。在执行事务回滚的时候，就可以通过undo log中的记录内容并以此进行回滚。
2. undo log还可以提供多版本并发控制下的读取（MVCC）。
#### （四）bin log
MySQL的bin log日志是用来记录MySQL中增删改时的记录日志。简单来讲，就是当你的一条sql操作对数据库中的内容进行了更新，就会增加一条bin log日志。查询操作不会记录到bin log中。bin log最大的用处就是进行**主从复制**，以及数据库的恢复。
![image.png](https://cdn.nlark.com/yuque/0/2022/png/22219483/1663236050094-37f9663c-c825-4486-a07d-46a1ab73b3d4.png#averageHue=%23828098&clientId=uc9b92f8f-761c-4&crop=0&crop=0&crop=1&crop=1&from=paste&id=u606e8b9d&margin=%5Bobject%20Object%5D&name=image.png&originHeight=326&originWidth=640&originalType=url&ratio=1&rotation=0&showTitle=false&size=84791&status=done&style=none&taskId=u84bf4b2d-5dde-4c9c-8bfc-9b001527a2d&title=)
通过下面的命令可以查看是否开启binlog日志
```shell
show VARIABLES like '%log_bin%'
```
开启binlog的方式如下：
```shell
log-bin=mysql-bin
server-id=1
binlog_format=ROW
```
其中log-bin指定日志文件的名称，默认会放到数据库目录下，可通过以下命令查看
```shell
show VARIABLES like '%datadir%'
```
#### （五）error log
error log主要记录MySQL在启动、关闭或者运行过程中的错误信息，在MySQL的配置文件my.cnf中，可以通过log-error=/var/log/mysqld.log 执行mysql错误日志的位置。
通过MySQL的命令
```shell
show variables like "%log_error%";
```
也可以获取到错误日志的位置。
#### （六）slow query log
慢查询日志用来记录执行时间超过指定阈值的SQL语句，慢查询日志往往用于优化生产环境的SQL语句。可以通过以下语句查看慢查询日志是否开启以及日志的位置：
```shell
show variables like "%slow_query%";
```
慢查询日志的常用配置参数如下：
```shell
slow_query_log=1 #是否开启慢查询日志，0关闭，1开启
slow_query_log_file=/usr/local/mysql/mysql-8.0.20/data/slow-log.log #慢查询日志地址（5.6及以上版本）
long_query_time=1 #慢查询日志阈值，指超过阈值时间的SQL会被记录
log_queries_not_using_indexes #表示未走索引的SQL也会被记录
```
分析慢查询日志一般会用专门的日志分析工具。找出慢SQL后可以通过explain关键字进行SQL分析，找出慢的原因。
#### （七）general log
general log 记录了客户端连接信息以及执行的SQL语句信息，通过MySQL的命令
```shell
show variables like '%general_log%';
```
可以查看general log是否开启以及日志的位置。
![image.png](https://cdn.nlark.com/yuque/0/2022/png/22219483/1663236049994-8295d29e-98cb-4788-9751-0e7fba7e5ae5.png#averageHue=%230b0908&clientId=uc9b92f8f-761c-4&crop=0&crop=0&crop=1&crop=1&from=paste&id=u62c45274&margin=%5Bobject%20Object%5D&name=image.png&originHeight=152&originWidth=640&originalType=url&ratio=1&rotation=0&showTitle=false&size=62203&status=done&style=none&taskId=ufcd8b81a-05eb-41bf-bec0-49b1b989ed6&title=)
general log 可通过配置文件启动，配置参数如下：
general_log = on
general_log_file = /usr/local/mysql/mysql-8.0.20/data/hecs-78422.log
普通查询日志会记录增删改查的信息，因此一般是关闭的。

## 12. 在事务中可以混合使用存储引擎吗？

尽量不要在同一个事务中使用多种存储引擎，MySQL服务器层不管理事务，事务是由下层的存储引擎实现的。

如果在事务中混合使用了事务型和非事务型的表（例如InnoDB和MyISAM表）,在正常提交的情况下不会有什么问题。

但如果该事务需要回滚，非事务型的表上的变更就无法撤销，这会导致数据库处于不一致的状态，这种情况很难修复，事务的最终结果将无法确定。所以，为每张表选择合适的存储引擎非常重要。

## 13. MySQL中是如何实现事务隔离的?

读未提交和串行化基本上是不需要考虑的隔离级别，前者不加锁限制，后者相当于单线程执行，效率太差。

MySQL 在可重复读级别解决了幻读问题，是通过行锁和间隙锁的组合 Next-Key 锁实现的。

## 14. MVCC
有了锁，当前事务没有写锁就不能修改数据，但还是能读的，而且读的时候，即使该行数据其他事务已修改且提交，还是`可以重复读到同样的值`。这就是MVCC，`多版本的并发控制，Multi-Version Concurrency Control`。

### 一致性非锁定读
对于一致性非锁定读(MVCC)的实现, 通常时加一个版本号或时间戳. 查询时, 将当前可见的版本号和对应的版本号进行比对, 若记录的版本号小于可见版本号, 则表示该记录可见.

在 InnoDB 中, 多版本控制(Multi Versioning)就是对非锁定读的实现. 若读取的行正在执行 DELETE 或 UPDATE, 这时读操作不会去等待行锁的释放, 而是读取行的一个快照, 被称为**快照读**

### 锁定读
也被称为 **当前读**. 锁定读会对读取到的记录加锁.

- `select ... lock in share mode` : 对记录加 S 锁, 其它事务也可以加 S 锁, 但是加 X 锁会被阻塞
- `select ... for update`、`insert`、`update`、`delete` : 对记录加 X 锁

当前读每次读取的都是最新数据, 两次查询中间如果有其他事务插入数据, 就会产生幻读.

### MVCC 实现原理
MVCC是通过保存数据在某个时间点的快照来实现的. 根据事务开始的时间不同, 每个事务对同一张表, 同一时刻看到数据可能是不一样的.
![image-20220304210135517.png](https://cdn.nlark.com/yuque/0/2022/png/21380271/1646468515309-09d9dfe3-929e-46fb-91b7-3a169f96bd6e.png#averageHue=%23eaede1&clientId=ub63f7278-093b-4&crop=0&crop=0&crop=1&crop=1&from=ui&id=UWfiP&margin=%5Bobject%20Object%5D&name=image-20220304210135517.png&originHeight=299&originWidth=681&originalType=binary&ratio=1&rotation=0&showTitle=false&size=121327&status=done&style=none&taskId=u17740057-d3c4-4067-9dff-5b35436a6a3&title=)

MVCC实现依赖于: **隐藏字段**, **Read View**, **undo log**

隐藏字段主要包含:

- ROW ID : 隐藏的自增ID, 如果表没有主键, InnoDB 会自动按 ROW ID 产生一个聚簇索引树
- 事务 ID : 记录最后一次修改该记录的事务ID
- 回滚指针 : 指向这条记录的上一个版本

举例：

![img](https://cdn.nlark.com/yuque/0/2022/png/22219483/1647160347032-8a5cb969-2fb8-4d0e-b4ee-621544ac9253.png)

如图，首先 insert 语句向表 t1 中插入了一条数据，a 字段为 1，b 字段为 1， ROW ID 也为 1 ，事务 ID 假设为 1，回滚指针假设为 null。当执行 update t1 set b=666 where a=1 时，大致步骤如下：

- 数据库会先对满足 a=1 的行加排他锁；
- 然后将原记录复制到 undo 表空间中；
- 修改 b 字段的值为 666，修改事务 ID 为 2；
- 并通过隐藏的回滚指针指向 undo log 中的历史记录；
- 事务提交，释放前面对满足 a=1 的行所加的排他锁。

在前面实验的第 6 步中，session2 查询的结果是 session1 修改之前的记录，这个记录就是**来自 undolog** 中。

因此可以总结出 MVCC 实现的原理大致是：

InnoDB 每一行数据都有一个隐藏的回滚指针，用于指向该行修改前的最后一个历史版本，这个历史版本存放在 undo log 中。如果要执行更新操作，会将原记录放入 undo log 中，并通过隐藏的回滚指针指向 undo log 中的原记录。其它事务此时需要查询时，就是查询 undo log 中这行数据的最后一个历史版本。

但是 undo log 总不可能一直保留. 在不需要的时候它应该被删除, 这时就交由系统自动判断, 即当系统没有比这个 undo log 更早的 read-view 的时候. 所以尽量不要使用长事务, 长事务意味着系统里会存在非常古老的事务视图. 由于这些事务随时可能访问数据库中任何数据, 所以这个事务提交前, 数据库里它可能使用到的 undo log 都必须保存, 导致占用大量存储空间.

MVCC 最大的好处是读不加锁，读写不冲突，极大地增加了 MySQL 的并发性。通过 MVCC，保证了事务 ACID 中的 I（隔离性）特性。

--- 

# 锁

## 1. 为什么要加锁?
当多个用户**并发地存取数据**时，在数据库中就会**产生多个事务同时存取同一数据的情况**。若对并发操作不加控制就可能会读取和存储不正确的数据，破坏数据库的一致性。保证多用户环境下保证数据库完整性和一致性。

## 2. 按照锁的粒度分数据库锁有哪些？
在关系型数据库中，可以按照锁的粒度把数据库锁分为行级锁(INNODB引擎)、表级锁(MYISAM引擎 )和页级锁(BDB引擎 )。

行级锁

- 行级锁是MySQL中锁定粒度最细的一种锁，表示只针对当前操作的行进行加锁。行级锁能大大减少数据库操作的冲突。其加锁粒度最小，但加锁的开销也最大。行级锁分为共享锁 和 排他锁。
- 开销大，加锁慢；会出现死锁；锁定粒度最小，发生锁冲突的概率最低，并发度也最高。

在 InnoDB 事务中，行锁通过给索引上的索引项加锁来实现。这意味着只有通过索引条件检索数据，InnoDB才使用行级锁，否则将使用表锁。
行级锁定同样分为两种类型：共享锁和排他锁。

表级锁

- 表级锁是MySQL中锁定粒度最大的一种锁，表示对当前操作的整张表加锁，它实现简单，资源消耗较少，被大部分MySQL引擎支持。最常使用的MYISAM与INNODB都支持表级锁定。表级锁定分为表共享读锁（共享锁）与表独占写锁（排他锁）。
- 开销小，加锁快；不会出现死锁；锁定粒度大，发出锁冲突的概率最高，并发度最低。

页级锁

- 页级锁是MySQL中锁定粒度介于行级锁和表级锁中间的一种锁。表级锁速度快，但冲突多，行级冲突少，但速度慢。所以取了折衷的页级，一次锁定相邻的一组记录。BDB支持页级锁
- 开销和加锁时间界于表锁和行锁之间；会出现死锁；锁定粒度界于表锁和行锁之间，并发度一般

全局锁

全局锁就是对整个数据库实例加锁. MySQL提供了一个加全局读锁的方法, `Flush tables with read lock(FTWRL)` 使整个库都处于只读状态. 一般用于全局备份.

## 3. 从锁的类别上分MySQL都有哪些锁呢？
从锁的类别上来讲，有共享锁和排他锁。

- 共享锁: 又叫做读锁。 当用户要进行数据的读取时，对数据加上共享锁。共享锁可以同时加上多个。
- 排他锁: 又叫做写锁。 当用户要进行数据的写入时，对数据加上排他锁。排他锁只可以加一个，他和其他的排他锁，共享锁都相斥。

用例子来说就是用户的行为有两种，一种是来看房，多个用户一起看房是可以接受的。 一种是真正的入住一晚，在这期间，无论是想入住的还是想看房的都不可以。

锁的粒度取决于具体的存储引擎，InnoDB实现了行级锁，页级锁，表级锁。

他们的加锁开销从大到小，并发能力也是从大到小。

## 4. 数据库的乐观锁和悲观锁是什么？怎么实现的？
悲观锁 (Pessimistic Lock)
概念： 悲观锁假定会发生并发冲突，因此在数据处理前就进行加锁，阻止其他事务对数据的访问，直到当前事务结束。这种策略较为保守，适用于写操作频繁且并发冲突较多的场景。实现方式：使用数据库中的锁机制

实现方式：

SELECT ... FOR UPDATE： 在查询语句中加入FOR UPDATE子句，可以对查询结果集中的行加写锁，确保其他事务无法修改这些行，直到当前事务结束。
锁定级别： InnoDB存储引擎支持行级锁，因此悲观锁通常是行锁。
注意事项： 使用悲观锁时，需关闭MySQL的自动提交模式(SET autocommit = 0;)，并在事务结束后手动提交(COMMIT)或回滚(ROLLBACK)。

乐观锁 (Optimistic Lock)
概念： 乐观锁假设数据一般不会发生并发冲突，仅在数据更新提交时检查数据是否被其他事务修改过。如果数据未被修改，则提交成功；否则，根据策略重试或回滚事务。这种方式减少了锁的开销，提高了系统的并发性能。通过version的方式来进行锁定。实现方式：乐一般会使用版本号机制或CAS算法实现。

实现方式：

版本号/时间戳： 在表中增加一个额外的字段，如version或update_time，每次更新时自动递增版本号或更新时间戳。
检查逻辑： 更新数据时，同时检查该行记录的版本号或时间戳是否与之前读取时一致，如果不一致则抛出异常或重试操作。
示例：

sql
-- 假设有一个表table_with_version，包含id, data, version字段
START TRANSACTION;
SELECT * FROM table_with_version WHERE id = ? FOR UPDATE; -- 可选，根据需要使用
UPDATE table_with_version SET data = ?, version = version + 1 WHERE id = ? AND version = ?; -- 检查并更新
COMMIT;
适用场景：

乐观锁适合读多写少的应用场景，可以有效提升系统的并发处理能力。
悲观锁更适合写多读少，且并发冲突频繁的场景，保证数据的一致性。
选择哪种锁策略应基于具体业务场景的需求，平衡并发性能和数据一致性之间的关系。

## 5. InnoDB引擎的行锁是怎么实现的？
InnoDB是基于索引来完成行锁

例: select * from tab_with_index where id = 1 for update;

for update 可以根据条件来完成行锁锁定，并且 id 是有索引键的列，如果 id 不是索引键那么InnoDB将完成表锁，并发将无从谈起

## 6. 什么是死锁？怎么解决？ --- TBD
死锁是指两个或多个事务在同一资源上相互占用，并请求锁定对方的资源，从而导致恶性循环的现象。

常见的解决死锁的方法

1、如果不同程序会并发存取多个表，**尽量约定以相同的顺序访问表，可以大大降低死锁机会。**

2、在同一个事务中，尽可能做到**一次锁定所需要的所有资源**，减少死锁产生概率；

3、对于**非常容易产生死锁**的业务部分，可以尝试使用**升级锁定颗粒度，通过表级锁定来减少死锁产生的概率**；

如果业务处理不好可以用分布式事务锁或者使用乐观锁

## 7. 隔离级别与锁的关系
在Read Uncommitted级别下，读取数据不需要加共享锁，这样就不会跟被修改的数据上的排他锁冲突

在Read Committed级别下，读操作需要加共享锁，但是在语句执行完以后释放共享锁；

在Repeatable Read级别下，读操作需要加共享锁，但是在事务提交之前并不释放共享锁，也就是必须等待事务执行完毕以后才释放共享锁。

SERIALIZABLE 是限制性最强的隔离级别，因为该级别锁定整个范围的键，并一直持有锁，直到事务完成。

## 8. 优化锁方面的意见？-- TBD
- 使用较低的隔离级别
- 设计索引，尽量使用索引去访问数据，加锁更加精确，从而减少锁冲突
- 选择合理的事务大小，给记录显示加锁时，最好一次性请求足够级别的锁。列如，修改数据的话，最好申请排他锁，而不是先申请共享锁，修改时在申请排他锁，这样会导致死锁
- 不同的程序访问一组表的时候，应尽量约定一个相同的顺序访问各表，对于一个表而言，尽可能的固定顺序的获取表中的行。这样大大的减少死锁的机会。
- 尽量使用相等条件访问数据，这样可以避免间隙锁对并发插入的影响
- 不要申请超过实际需要的锁级别
- 数据查询的时候不是必要，不要使用加锁。MySQL的MVCC可以实现事务中的查询不用加锁，优化事务性能：MVCC只在committed read（读提交）和 repeatable read （可重复读）两种隔离级别
- 对于特定的事务，可以使用表锁来提高处理速度活着减少死锁的可能。

## 9. 行锁的实现算法
-  Record Lock（记录锁）

   - 功能：这是最基本的行锁类型，它锁定的是索引记录上的单一行。当一个事务请求对某一行进行锁定时，InnoDB会在相应的索引记录上放置一个记录锁。
   - 特点：只锁定特定的索引项，不会影响到索引范围内的其他记录。
   - 应用场景：适用于精确匹配的查询，如WHERE id = 10。

- Gap Lock（间隙锁）

   - 功能：锁定一个索引记录范围内的间隙，但不包括该范围内的任何实际记录。目的是防止其他事务插入新的记录到这个范围内，从而避免幻读现象。
   - 特点：锁定的是两个索引记录之间的空隙，确保新纪录不会插入到这个间隙中，但不阻止对已存在记录的访问。
   - 应用场景：通常在执行范围查询（如使用BETWEEN，<, >等操作符）并启用了隔离级别为可重复读（Repeatable Read）或更高时出现。

- Next-Key Lock（下一个键锁）

   - 功能：它是Record Lock和Gap Lock的结合体，不仅锁定一个索引记录，还锁定该记录前面的间隙。这实际上是一种防止幻读的有效机制。
   - 特点：既能防止其他事务修改或插入索引记录，也能防止在这个记录前的间隙内插入新的记录。
   - 应用场景：默认情况下，在可重复读（Repeatable Read）隔离级别下，InnoDB使用Next-Key Locks来处理范围查询，以防止幻读。

-  **Insert Intention Lock 插入意向锁**
若插入位置已被别的事务加了 Gap Lock, 则事务在等待时也需要在内存中生成一个锁结构, 被称为 插入意向锁. 当 Gap Lock 释放的时候,插入意向锁就会将等待事务中锁结构内的 is_waiting 的状态改为 false, 然后开始继续往下执行插入操作. 
-  **隐式锁**
隐式锁其实是一种延迟生成锁结构的方案, 通过判断事务id, 确定两个并发事务之间是否真的有必要加锁, 若需要, 则会生成锁结构, 然后进入等待; 不需要, 那么就没必要浪费内存去对事务生成锁结构, 降低维护成本. 类似于乐观锁实现. 

## 10. 两阶段锁协议
在InnoDB事务中, 行锁是需要的时候才加上的, 但并不是不需要了就立刻释放, 而是等到事务结束时才释放. 这就是 **两阶段锁协议**

如果事务中需要锁住多行, 要把最可能造成锁冲突、最可能影响并发度的锁尽量往后放. 这样就最大程度减少了事务间的锁等待, 提升了并发度.



---

以下 --- TBD
MVCC...
#### 版本链
Innodb 中行记录的存储格式，有一些额外的字段：**DATA_TRX_ID **和 **DATA_ROLL_PTR**。

- **DATA_TRX_ID**：数据行版本号。用来标识最近对本行记录做修改的事务 id。
- **DATA_ROLL_PTR**：指向该行回滚段的指针。该行记录上所有旧版本，在 undo log 中都通过链表的形式组织。
- undo log : 记录数据被修改之前的日志，后面会详细说。

![image.png](https://cdn.nlark.com/yuque/0/2022/png/22219483/1663236594178-8dd5c313-e422-41c0-9602-f5f68a2b6ce5.png#averageHue=%236eac44&clientId=ub06f29a5-b09f-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=37&id=u0a2c85e4&margin=%5Bobject%20Object%5D&name=image.png&originHeight=73&originWidth=600&originalType=binary&ratio=1&rotation=0&showTitle=false&size=7568&status=done&style=none&taskId=uaec341e2-f127-493f-b51f-e3c91ad4772&title=&width=300)

#### ReadView
在每一条 SQL 开始的时候被创建，有几个重要属性：

**trx_ids:** 当前系统活跃(未提交)事务版本号集合。
**low_limit_id:** 创建当前 read view 时“当前系统最大事务版本号+1”。
**up_limit_id:** 创建当前read view 时“系统正处于活跃事务最小版本号”
**creator_trx_id:** 创建当前read view的事务版本号；

**开始查询**
现在开始查询，一个 select 过来了，找到了一行数据。

- **DATA_TRX_ID <up_limit_id ：说明数据在当前事务之前就存在了，显示。**
- **DATA_TRX_ID >= low_limit_id：**说明该数据是在当前read view 创建后才产生的，数据不显示。
   - 不显示怎么办，根据 DATA_ROLL_PTR 从 undo log 中找到历史版本，找不到就空。
- ** up_limit_id <DATA_TRX_ID <low_limit_id ：**就要看隔离级别了。

### RC(**读提交**)和RR(可重复读)级别下MVCC的差异

- RC级别 : 每次SELECT查询前都生成一个Read View
- RR级别  : 事务开启后第一次SELECT数据前生成一个Read View

### MVCC + Next-key Lock 防止幻读
InnoDB在RR级别下通过 `MVCC` 和 `Next-key Lock` 解决幻读问题

- 在快照读（snapshot read）的情况下，MySQL通过MVCC（多版本并发控制）来避免幻读。
   - 快照读，读取的是记录的可见版本 (有可能是历史版本)，不用加锁。主要应用于无需加锁的普通查询（select）操作。

- 在当前读（current read）的情况下，MySQL通过next-key lock来避免幻读。
   - 当前读，读取的是记录的最新版本，并且会对当前记录加锁，防止其他事务发修改这条记录。
   - 加行共享锁（SELECT ... LOCK IN SHARE MODE ）、加行排他锁（SELECT ... FOR UPDATE / INSERT / UPDATE / DELETE）的操作都会用到当前度。


1. **执行普通 **`**SELECT**`**, 此时会以 **`**MVCC**`** 快照读方式读取数据.**
在快照读的情况下，RR 隔离级别只会在事务开启后的第一次查询生成 `Read View` ，并使用至事务提交。所以在生成 `Read View` 之后其它事务所做的更新、插入记录版本对当前事务并不可见，实现了可重复读和防止快照读下的 “幻读”
2. **执行 select...for update/lock in share mode、insert、update、delete 等当前读**
在当前读下，读取的都是最新的数据，如果其它事务有插入新的记录，并且刚好在当前事务查询范围内，就会产生幻读！

      `InnoDB` 使用 `Next-key Lock` 来防止这种情况。当执行当前读时，会锁定读取到的记录的同时，锁定它们的间隙，防止其它事务在查询范围内插入数据。只要我不让你插入，就不会发生幻读

### innoDB的间隙锁/Next-Key Lock
**明确前提条件**

- innoDB的间隙锁只存在于 RR 隔离级别

所以希望禁用间隙锁，提升系统性能的时候，可以考虑将隔离级别降为 RC。

**间隙锁/Next-Key Lock**
间隙锁在innoDB中的唯一作用就是在一定的“间隙”内防止其他事务的插入操作，以此防止幻读的发生：

- 防止间隙内有新数据被插入。
- 防止已存在的数据，更新成间隙内的数据。

### innoDB支持三种行锁定方式：
- 行锁（Record Lock）：锁直接加在索引记录上面（无索引项时演变成表锁）。
- 间隙锁（Gap Lock）：锁定索引记录间隙，确保索引记录的间隙不变。间隙锁是针对事务隔离级别为可重复读或以上级别的。
- Next-Key Lock ：行锁和间隙锁组合起来就是 Next-Key Lock。

1. innoDB默认的隔离级别是可重复读(Repeatable Read)，并且会以Next-Key Lock的方式对数据行进行加锁。
2. Next-Key Lock是行锁和间隙锁的组合，当InnoDB扫描索引记录的时候，会首先对索引记录加上行锁（Record Lock），
3. 再对索引记录两边的间隙加上间隙锁（Gap Lock）。
4. 加上间隙锁之后，其他事务就不能在这个间隙修改或者插入记录。
5. 当查询的索引含有唯一属性（唯一索引，主键索引）时，Innodb存储引擎会对next-key lock进行优化，将其降为record lock,即仅锁住索引本身，而不是范围。

### 何时使用行锁，何时产生间隙锁
对上一节的最后一句做个扩展说明。

1. 只使用唯一索引查询，并且只锁定一条记录时，innoDB会使用行锁。
2. 只使用唯一索引查询，但是检索条件是范围检索，或者是唯一检索然而检索结果不存在（试图锁住不存在的数据）时，会产生 Next-Key Lock。
3. 使用普通索引检索时，不管是何种查询，只要加锁，都会产生间隙锁。
4. 同时使用唯一索引和普通索引时，由于数据行是优先根据普通索引排序，再根据唯一索引排序，所以也会产生间隙锁。
