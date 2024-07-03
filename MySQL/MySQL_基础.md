# SQL
好的SQL可以增加数据库处理效率，减少响应时间，减少数据库服务器负载，增加稳定性，减少服务器通讯的网络流量。

	DDL 数据定义语言: creat、alter
	TPL 事务处理语言：commit、rollback
	DCL 数据控制语言：grant、revoke
	DML 数据操作语言：insert、update、 select、delete

## JOIN
	内连接（INNER  Join）
	全外连接（FULL OUTER）
	左外连接（LEFT OUTER）
	右外连接（RIGHT OUTER）
	交叉连结（CROSS）

### INNER JOIN  
即等值连接： 只返回两个表中联结字段相等的行，也就是求公共交集。
```
SELECT 
	a.user_name, 
	a.over, 
	b.over 
FROM user1 a INNER JOIN user2 b ON a.user_name = b.user_name;
```

### LEFT OUTER JOIN
以左表为基础查询，返回包括左表中的所有记录和右表中联结字段相等的记录。左表全部显示，右表存在为值，不存在为空。
```
SELECT <select_list> 
FROM TableA A  LEFT Join TableB B ON A.Key = B.Key;

SELECT 
	a.user_name, 
	a.over, 
	b.over 
FROM user1 a LEFT JOIN user2 b ON a.user_name = b.user_name;
```

如果查询只在A表而不在B表的数据，一般会在where中用not in B过滤。
```
SELECT <select_list> FROM TableA A  LEFT Join TableB B ON A.Key = B.Key 
WHERE B.Key is NULL;
```
此时返回只在左表中的数据。

### RIGHT OUTER JOIN
与left join相反。
以右表为基础查询，返回包括右表中的所有记录和左表中联结字段相等的记录。右表全部显示，左表存在为值，不存在为空。
```
SELECT <select_list> FROM TableA A RIGHT JOIN TableB B ON A.Key = B.Key;
```

如果查询只在B表而不在A表的数据，一般会在where中用not in A过滤。
```
SELECT <select_list> FROM TableA A RIGHT JOIN TableB B ON A.Key = B.Key 
WHERE A.Key IS NULL;
```

### FULL JOIN
返回两个表的集合。

但MYSQL中并不支持全连接FULL JOIN。FULL JOIN其实是左外连接和右外连接的交集，所以可用UNION ALL来连接左右外连接来实现全连接的功能。
```
SELECT 
	a.user_name,
	a.over,
	b.over 
FROM user1 a LEFT JOIN user2 b ON a.user_name=b.user_name
UNION ALL
SELECT 
	b.user_name,
	b.over,
	a.over
FROM user1 a RIGHT JOIN user2 b ON a.user_name=b.user_name
```

如果查询只在A表和只在B表的数据的集合，可在where中用not in A，B过滤。
```
SELECT 
	a.user_name,
	a.over,
	b.over 
FROM user1 a LEFT JOIN user2 b ON a.user_name=b.user_name
WHERE b.user_name is null
UNION ALL
SELECT 
	b.user_name,
	b.over,
	a.over
FROM user1 a RIGHT JOIN user2 b ON a.user_name=b.user_name
WHERE a.user_name is null
```

### CROSS JOIN
交叉连接，笛卡尔连接(Cartesian join)，叉乘(product)，即为两张表的乘积。
如果A和B是两个集合，他们的交叉连接就记为A×B。

笛卡尔积运算：
A={a, b}，集合B={0, 1, 2}，则两个集合的笛卡尔积为{(a, 0), (a, 1), (a, 2), (b, 0), (b, 1), (b, 2)}。

cross  join没有on从句，也就是没有连接关键词
```
select a.name, b.sex from user1 a cross join user2 b;
```

### JOIN解决错误
```
update user1 set over=‘齐天大圣’ 
where user1.user_name in (
	select 
		b.user_name 
	from user1 a join user2 b on a.user_name = b.user_name);
```
ERROR 1093错误 不能更新from语句中出现的表字段。

解决办法:
通过使用join进行联合更新。
```
update user1 a inner join user2 b on a.user_name = b.user_name set a.over='齐天大圣';
```
把两个表join构成一个虚拟表，检索出所有字段，然后再对它做select、update之类的数据操作。

### JOIN优化子查询技巧：
一般子查询写法：(如果数据量大时，则要消耗大量时间)
```
select 
	a.user_name , 
	a.voer , 
	(select 
		over 
	from user2 
	where a.user_name = b,user_name) as over2
from user1 a;
```
如果这两张表的记录相当多 那么这个子查询相当于对A标的每一条记录都要进行一次子查询。

可以直接只用left join
```
select 
	a.user_name,
	a.over,
	b.over as over2 
from user1 a left join user2 b on a.user_name=b.user_name;
```

查询打怪最多的日期
```
select 
	a.user_name,
	b.timestr,
	b.kills 
from user1 a join user_kills b ON a.id=b.user_id 
where b.kills=(
	select 
		MAX(c.kills) 
	from user_kills c 
	where c.user_id=b.user_id);
```
使用join + having优化聚合子查询:
```
select 
	a.user_name,
	b.timestr,
	b.kills 
from user1 a
	join user_kills b on a.id = b.user_id 
	join user_kills c on c.user_id = b.user_id
group by a.user_name,btimestr,b.kills
having b.kills = max(c.kills);
```

分类聚合方式查询每一个用户某一个字段数据最大的两条数据：
```
select 
	d.user_name ,
	c.ctimestr,
	kills 
from (
	select 
		user_id,
		timestr,
		kills,
		(select 
			count(*) 
		from user_kills b 
		where b.user_id = a.user_id 
			and a.kills <= b.kills)as cnt 
    from 
		user_kills a
	group by user_id,timestr,kills) c 
	join user1 d on c.user_id = d.id 
where 
	cnt <= 2
```
刚仔细思考了一下最后一课的SQL，与大家分享一下，希望大家帮忙找出错误。
    select d.user_name ,c.ctimestr,kills from
    (select user_id ,timestr ,kills ,(
     select count(*) from user_kills b where b.user_id = a.user_id and a.kills <= b.kills) as cnt 
     from user_kills a group by user_id,timestr,kills) c 
     join user1 d on c.user_id = d.id where cnt <= 2
首先将第一个From后面的子查询看成一个普通表，这样就是一个普通的多表连接查询了。
where cnt < 2便是筛选条件，选择出顺序是1，2前两条记录。然后在看括号里面里层括号这里所做的就是查询出这条记录在分组中根据kills排序的顺序，但是为啥是count（*）呢？ 
假设孙悟空打怪 3，5，12 我用3，5,12分别与3，5,12比较
3   3,5,12  小于3的有3条记录
5  3,5,12   小于5的有2条记录  
12 3,5，12  小于12的有1条记录
如此count（*）代表的就是顺序了，如果需要正序，只要将<= 改成>=就好了


### Prerequisite
```
CREATE TABLE `user1` (
  `id` int(11) NOT NULL COMMENT '主键',
  `user_name` varchar(255) DEFAULT NULL COMMENT '姓名',
  `over` varchar(255) DEFAULT NULL COMMENT '结局',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO `blog`.`user1`(`id`, `user_name`, `over`) VALUES (1, '唐僧', '旃檀功德佛');
INSERT INTO `blog`.`user1`(`id`, `user_name`, `over`) VALUES (2, '猪八戒', '净坛使者');
INSERT INTO `blog`.`user1`(`id`, `user_name`, `over`) VALUES (3, '孙悟空', '斗战胜佛');
INSERT INTO `blog`.`user1`(`id`, `user_name`, `over`) VALUES (4, '沙僧', '金身罗汉');

CREATE TABLE `user2` (
  `id` int(11) NOT NULL COMMENT '主键',
  `user_name` varchar(255) DEFAULT NULL COMMENT '姓名',
  `over` varchar(255) DEFAULT NULL COMMENT '结局',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO `blog`.`user2`(`id`, `user_name`, `over`) VALUES (1, '孙悟空', '成佛');
INSERT INTO `blog`.`user2`(`id`, `user_name`, `over`) VALUES (2, '牛魔王', '被降服');
INSERT INTO `blog`.`user2`(`id`, `user_name`, `over`) VALUES (3, '蛟魔王', '被降服');
INSERT INTO `blog`.`user2`(`id`, `user_name`, `over`) VALUES (4, '鹏魔王', '被降服');
INSERT INTO `blog`.`user2`(`id`, `user_name`, `over`) VALUES (5, '狮驼王', '被降服');
```


## 列转行

利用自身连接来实现：
```
SELECT *
FROM (
	SELECT SUM(KILLS) AS 'A'
	FROM A INNER JOIN B ON A.NAME=B.USER_NAME
	WHERE A.NAME='A') AS A CROSS JOIN(
	SELECT SUM(KILLS) AS 'B'
	FROM A INNER JOIN B ON A.NAME=B.USER_NAME
	WHERE A.NAME='B') AS B CROSS JOIN(
	SELECT SUM(KILLS) AS 'C'
	FROM A INNER JOIN B ON A.NAME=B.USER_NAME
	WHERE A.NAME='C')AS C;
```
比如成绩
1、分别查询出不同同学的成绩，并将字段名改为同学的名字
2、通过交叉连接，将不同的语句连接起来

缺点：是将原来查询的结果每一行单独查询出来，再进行拼接。因此每增加一个同学就增加一个SELECT语句。并且是通过交叉连接，要保证每个查询的结果只能是一个，不然没办法通过交叉连接实现转换。


使用case 语句来实现行列转换
```
SELECT SUM(CASE WHEN u.`user_name` = '八戒' THEN k.`kills` END) AS '八戒',
 SUM(CASE WHEN u.`user_name` = '悟空' THEN k.`kills` END) AS '悟空' ,
 SUM(CASE WHEN u.`user_name` = '沙僧' THEN k.`kills` END) AS '沙僧' 
 FROM user_kills k  JOIN user1 u ON k.`user_id` = u.`id`;
```

## 行转列
```
SELECT username,REPLACE(substring(SUBSTRING_INDEX(mobile,',',a.id), CHAR_LENGTH(SUBSTRING_INDEX(mobile,',',a.id-1))+1),',','') AS mobile 
FROM tb_sequence AS a
CROSS JOIN 
(SELECT username, CONCAT(mobile,',') AS mobile, (LENGTH(mobile)-LENGTH(REPLACE(mobile,',',''))+1) AS size 
FROM user1) AS b 
ON a.id <= b.size;
```


## 唯一序列号：
需要使用唯一序列号的场景：
1. 作为数据库主键。
2. 业务序列号。

生成序列号的方法：
- MySQL：AUTO_INCREMENT
- SQLServer：IDENTITY/SEQUENCE
- Oracle：SEQUENCE
- PgSQL：SEQUENCE

如何选择生成序列号的方式：

原则：优先选择系统提供的序列号生成方式。

优点：
1. 控制并发；
2. 不重复，保证序列号的唯一性。

缺点：序列号不连续（数据空洞），例如 1、2、4。

原因：对已有的数据的删除，以及事务回滚等方式不会影响自增长的序号，例如已有数据 1、2、3，删除 3 号数据。之后再插入一条数据，此时数据表的数据为 1、2、4。


存储过程，订单号：

```
DECLARE v_cnt INT;
DECLARE v_timestr INT;
DECLARE rowcount BIGINT;
SET v_timestr = DATE_FORMAT(NOW(),'%Y%m%d');
SELECT ROUND(RAND()*100,0)+1 INTO v_cnt;
START TRANSACTION;
UPDATE order_seq SET order_sn = order_sn + v_cnt WHERE timestr = v_timestr;
IF ROW_COUNT() = 0 THEN
INSERT INTO order_seq(timestr,order_sn) VALUES(v_timestr,v_cnt);
END IF;
SELECT CONCAT(v_timestr,LPAD(order_sn,7,0))AS order_sn
FROM order_seq WHERE timestr = v_timestr;
COMMIT;
```

知识点：
1、在sql语句中添加变量。
declare @local_variable data_type
声明时需要指定变量的类型，可以使用SET、SELECT、SELECT...INTO对变量进行赋值，在sql语句中就可以使用@local_variable来调用变量。
2、RAND()返回一个介于 0 到 1（不包括 0 和 1）之间的伪随机 float 值。
3、事务
4、ROW_COUNT()函数返回查询语句执行后，被影响的列数目
5、IF...THEN...END IF;

### 删除重复数据

1.查询数据是否重复
```
SELECT 
	user_name,
	COUNT(*)
FROM user1_test
GROUP BY 
	user_name
HAVING COUNT(*)>1;
```
2.删除重复数据，对于相同数据保留ID最大的
```
DELETE a 
FROM user1_test a JOIN(
	SELECT 
		user_name,
		COUNT(*),
		MAX(id) AS id
	FROM user1_test
	GROUP BY user_name HAVING COUNT(*)>1) b 
ON a.user_name=b.user_name
WHERE a.id<b.id;
```

## 子查询

子查询：这个查询是另外一个查询的条件，称作子查询。

	select user_name from user1 where id in (select user_id from user_kills);
	-- 使用子查询可以避免由于子查询中的数据产生的重复(子查询中的重复会被上面的语句忽略)。

	select a.user_name from user1 a join user_kills b on a.id =b.user_id;
	-- 会产生重复记录

	select distinct a.user_name from user1 a join user_kills b on a.id =b.user_id;
	-- 使用distinct去除重复记录

子查询转成join链接之后查询，注意数据重复的问题；子查询会自动过滤子查询中重复的记录的，但是join链接，会出现重复数据。

另一个子查询的例子：
```
select
	a.user_name,
	b.timestr,
	kills
from user1 a join user_kills b on a.id = b.user_id join (
	select
		user_id,
		max(kills) as cnt
	from user_kills
	group by user_id) c on b.user_id = c.user_id and b.kills = c.cnt;
```
上面的例子可以改成用MySQL中独有的多列过滤：
```
select
	a.user_name,
	b.timestr,
	kills
from user1 a join user_kills b on a.id = b.user_id
where (b.user_id, b.kills) in (
	select
		user_id,
		max(kills)
	from user_kills
	group by user_id);
```
可以不止两列。

## 同一属性多值过滤

前置条件
```
create table skills(
id mediumint primary key auto_increment,
username varchar(64),
skill varchar(64),
skill_level mediumint
);
insert into skills(username,skill,skill_level) values('唐僧','紧箍咒',5)
,('唐僧','打坐',4)
,('唐僧','念经',5)
,('唐僧','变化',0)
,('猪八戒','变化',4)
,('猪八戒','腾云',3)
,('猪八戒','浮水',5)
,('猪八戒','念经',0)
,('猪八戒','紧箍咒',0)
,('孙悟空','变化',5)
,('孙悟空','腾云',5)
,('孙悟空','浮水',3)
,('孙悟空','念经',2)
,('孙悟空','请神',5)
,('孙悟空','紧箍咒',0)
,('沙僧','变化',2)
,('沙僧','腾云',2)
,('沙僧','浮水',4)
,('沙僧','念经',1)
,('沙僧','紧箍咒',0);
```

```
select 
	s1.username,
	s1.skill,
	s2.skill
from skills s1 join skills s2 on s1.username=s2.username 
where
	s1.skill='变化'
	and s2.skill='念经'
	and s1.skill_level>0 and s2.skill_level>0;
``` 

```
Select a.user_name,b.skill,c.skill,e.skill From user1 a
From user1 a 
Left join user1_skill b on a.id =b.user_id and b.skill='念经' and
b.skill level>0
Left join user1_skill c on a.id = c.user_id and c.skill='变化' and
c.skill_level>0
Left join user1_skill d on a.id = d.user_id and d.skill = '腾云' and
c.skill_level>0
Left join user1_skill e on a.id = e.user_id and e.skill = '浮水' and
e.skill_level>0
Where (case when b.skill is not null then 1 else 0 end)
+(case when c.skill is not null then 1 else 0 end)
+(case when d.skill is not null then 1 else 0 end)
+(case when e.skill is not null then 1 else 0 end)>=2;
```

上面sql的问题是，如果再多选一个技能，join和where条件都会增加，不灵活。

```
select a.user_name 
from user1 a join user1_skills b on a.id=b.user_id 
where b.skill in ('念经','变化','腾云','浮水') and b.skill_level>0 
group by a.user_name having count(*)>=2;
```

## 累进税
```
select
	a.user_name,
	money,
	low,
	high,
	rate
from
	user1 a join taxRate b on a.money > b.low
order by user_name
```

```
select
	user_name,
	money,
	low,
	high,
	least(money-low, high-low) as curmoney,
	rate
from
	user1 a join taxRate b on a.money > b.low
order by user_name,low
```

应付税额

```
select 
	user_name,
	sum(curmoney*rate)
from (
	select
		user_name,
		money,
		low,
		high,
		least(money-low, high-low) as curmoney,
		rate
	from
		user1 a join taxRate b on a.money > b.low
) tax
group by user_name
```

###  类型转换
在MySQL中，类型转换通常用于在不同数据类型之间改变数据的表示形式。以下是一些主要的类型转换方法：

CAST 函数:
sql
   CAST(expression AS type)
这个函数将expression转换为指定的type。例如，将字符串转换为整数：

sql
   SELECT CAST('123' AS UNSIGNED INTEGER);
CONVERT 函数:
sql
   CONVERT(expression, type)
同样，CONVERT函数也用于将一个表达式转换为另一种类型。用法和CAST类似，例如：

sql
   SELECT CONVERT('2024-05-29', DATE);
直接赋值: MySQL允许在某些情况下通过赋值操作隐式转换类型，但这可能会导致数据丢失或错误，因此在生产环境中谨慎使用。

函数转换:

STR_TO_DATE() 和 DATE_FORMAT() 函数用于日期和时间的字符串转换。
TO_CHAR() 和 TO_DATE()（在某些数据库系统中，如Oracle，而不是MySQL）用于日期和数字的转换。
特定类型的函数: 有些函数可以用来在特定情况下转换数据类型，比如 UNIX_TIMESTAMP() 和 FROM_UNIXTIME() 用于和Unix时间戳之间的转换。

存储过程/触发器: 在存储过程或触发器中，可以根据需要进行复杂的类型转换逻辑。

例如，如果你想将一个字符串转换为日期，你可以这样做：

sql
SELECT STR_TO_DATE('2024-05-29', '%Y-%m-%d');
这将会返回一个日期类型的值，对应于2024年5月29日。

请记住，类型转换时要考虑数据可能的丢失和潜在的错误，特别是从大范围类型到小范围类型时，例如从整数到字符，或者从大精度数值到小精度数值。在进行类型转换时，应确保转换后的数据仍然有效并且符合预期。

## key

如果只是key的话，就是普通索引。

mysql的key和index多少有点令人迷惑，单独的key和其它关键词结合的key(primary key)实际表示的意义是不同，这实际上考察对数据库体系结构的了解的。

1 ：key 是数据库的物理结构，它包含两层意义和作用，

一是约束（偏重于约束和规范数据库的结构完整性），

二是索引（辅助查询用的）。

包括primary key, unique key, foreign key 等。

primary key 有两个作用，一是约束作用（constraint），用来规范一个存储主键和唯一性，但同时也在此key上建立了一个主键索引；    

PRIMARY KEY 约束：唯一标识数据库表中的每条记录；

主键必须包含唯一的值；

主键列不能包含 NULL 值；

每个表都应该有一个主键，并且每个表只能有一个主键。（PRIMARY KEY 拥有自动定义的 UNIQUE 约束）

unique key 也有两个作用，一是约束作用（constraint），规范数据的唯一性，但同时也在这个key上建立了一个唯一索引；

UNIQUE 约束：唯一标识数据库表中的每条记录。
                
UNIQUE 和 PRIMARY KEY 约束均为列或列集合提供了唯一性的保证。（每个表可以有多个 UNIQUE 约束，但是每个表只能有一个 PRIMARY KEY 约束

三、mysql中UNIQUE KEY和PRIMARY KEY有什么区别 

1，Primary key的1个或多个列必须为NOT NULL，如果列为NULL，在增加PRIMARY KEY时，列自动更改为NOT NULL。

而UNIQUE KEY 对列没有此要求 

2，一个表只能有一个PRIMARY KEY，但可以有多个UNIQUE KEY 


# 基础

## 1. 数据库的三范式是什么？

- 第一范式：强调的是列的原子性，即数据库表的每一列都是不可分割的原子数据项。
- 第二范式：要求实体的属性完全依赖于主关键字。所谓完全 依赖是指不能存在仅依赖主关键字一部分的属性。
- 第三范式：任何非主属性不依赖于其它非主属性。


数据库的三范式是数据库设计中用于规范数据表结构、减少数据冗余和提升数据一致性的基本原则。这三范式分别为：

1. 第一范式（1NF）
定义：要求表中的每一列（字段）都是不可分割的基本数据项，即原子性。每个字段都包含单一的数据值，不能是列表、集合或数组。
目的：确保数据的原子性，避免数据管理的复杂性。
2. 第二范式（2NF）
前提：在满足第一范式的基础上。
定义：要求表中的所有非主键字段完全依赖于任何候选键，而非部分依赖。即表中的每一个非主属性都必须完全依赖于主键，而不能只依赖于主键的一部分。
目的：消除部分依赖，减少数据冗余，使得更新操作更有效率且不会引起数据不一致。
3. 第三范式（3NF）
前提：在满足第二范式的基础上。
定义：要求一个表中的所有非主键字段直接依赖于主键，而不是依赖于其他非主键字段，即消除传递依赖。
目的：进一步减少数据冗余，增强数据独立性，使得数据变更更加灵活且不易出错。
遵循这三范式可以构建出结构合理、易于维护的数据库，但实际应用中，为了性能或其他考虑，有时会适当违反这些范式原则。

## 2. MySQL 支持哪些存储引擎?

MySQL 支持多种存储引擎,比如 InnoDB,MyISAM,Memory,Archive 等等.在大多数的情况下,直接选择使用 InnoDB 引擎都是最合适的,InnoDB 也是 MySQL 的默认存储引擎。

|  | InnoDB | MyISAM |
| --- | --- | --- |
| 事务 | 支持 | 不支持 |
| 外键 | 支持 | 不支持 |
| 行锁 | 支持 | 不支持 |
| 行表锁 | 行锁，操作时只锁某一行，不对其它行有影响，适合高并发的操作 | 表锁，即使操作一条记录也会锁住整个表，不适合高并发的操作 |
| 缓存 | 不仅缓存索引还要缓存真实数据，对内存要求较高，而且内存大小对性能有决定性的影响 | 只缓存索引，不缓存真实数据 |
| crash-safe能力 | 支持 | 不支持 |
| MVCC | 支持 | 不支持 |
| 索引存储类型 | 聚簇索引，数据文件是和索引绑在一起的，必须要有主键，通过主键索引效率很高 | 非聚簇索引，数据文件是分离的，索引保存的是数据文件的指针，主键索引和辅助索引是独立的。|
|全文索引| 不支持| 支持|
| 是否保存表行数 | 不保存 | 保存 |
| 关注点 | 事务：并发写、事务、更大资源 | 性能：节省资源、消耗少、简单业务 |

- InnoDB支持事物，而MyISAM不支持事物
- InnoDB支持行级锁，而MyISAM支持表级锁
- InnoDB支持MVCC, 而MyISAM不支持
- InnoDB支持外键，而MyISAM不支持
- InnoDB不支持全文索引，而MyISAM支持。

MVCC，全称Multi-Version Concurrency Control，即多版本并发控制。MVCC是一种并发控制的方法，一般在数据库管理系统中，实现对数据库的并发访问，在编程语言中实现事务内存。

## 3. 超键、候选键、主键、外键分别是什么？

- 超键：在关系中能唯一标识元组的属性集称为关系模式的超键。一个属性可以为作为一个超键，多个属性组合在一起也可以作为一个超键。超键包含候选键和主键。
- 候选键：是最小超键，即没有冗余元素的超键。
- 主键：数据库表中对储存数据对象予以唯一和完整标识的数据列或属性的组合。一个数据列只能有一个主键，且主键的取值不能缺失，即不能为空值（Null）。
- 外键：在一个表中存在的另一个表的主键称此表的外键。

## 4. SQL 约束有哪几种？

- NOT NULL: 用于控制字段的内容一定不能为空（NULL）。
- UNIQUE: 控件字段内容不能重复，一个表允许有多个 Unique 约束。
- PRIMARY KEY: 也是用于控件字段内容不能重复，但它在一个表只允许出现一个。
- FOREIGN KEY: 用于预防破坏表之间连接的动作，也能防止非法数据插入外键列，因为它必须是它指向的那个表中的值之一。
- CHECK: 用于控制字段的值范围。

## 5. MySQL 中的 varchar 和 char 有什么区别？

char 是一个定长字段,假如申请了char(10)的空间,那么无论实际存储多少内容.该字段都占用 10 个字符,而 varchar 是变长的,也就是说申请的只是最大长度,占用的空间为实际字符长度+1,最后一个字符存储使用了多长的空间.

在检索效率上来讲,char > varchar,因此在使用中,如果确定某个字段的值的长度,可以使用 char,否则应该尽量使用 varchar.例如存储用户 MD5 加密后的密码,则应该使用 char。

## 6. MySQL中 in 和 exists 区别

MySQL中的in语句是把外表和内表作hash 连接，而exists语句是对外表作loop循环，每次loop循环再对内表进行查询。一直大家都认为exists比in语句的效率要高，这种说法其实是不准确的。这个是要区分环境的。

如果查询的两个表大小相当，那么用in和exists差别不大。如果两个表中一个较小，一个是大表，则子查询表大的用exists，子查询表小的用in。not in 和not exists：如果查询语句使用了not in，那么内外表都进行全表扫描，没有用到索引；而not extsts的子查询依然能用到表上的索引。所以无论那个表大，用not exists都比not in要快。

## 7. drop、delete与truncate的区别

三者都表示删除，但是三者有一些差别：

![img](https://cdn.nlark.com/yuque/0/2022/png/22219483/1647160345752-99ea4690-4262-4a15-aafc-e56aea6ae8ee.png)

## 8. 什么是存储过程？有哪些优缺点？

存储过程是一些预编译的 SQL 语句。

1、更加直白的理解：存储过程可以说是一个记录集，它是由一些 T-SQL 语句组成的代码块，这些 T-SQL 语句代码像一个方法一样实现一些功能（对单表或多表的增删改查），然后再给这个代码块取一个名字，在用到这个功能的时候调用他就行了。 

2、存储过程是一个预编译的代码块，执行效率比较高,一个存储过程替代大量 T_SQL 语句 ，可以降低网络通信量，提高通信速率,可以一定程度上确保数据安全

但是,在互联网项目中,其实是不太推荐存储过程的,比较出名的就是阿里的《Java 开发手册》中禁止使用存储过程,我个人的理解是,在互联网项目中,迭代太快,项目的生命周期也比较短,人员流动相比于传统的项目也更加频繁,在这样的情况下,存储过程的管理确实是没有那么方便,同时,复用性也没有写在服务层那么好。

## 9. MySQL 执行查询的过程
1. 客户端通过TCP连接发生连接请求到 MySQL 连接器, 连接器会对该请求进行权限验证以及连接资源分配
2. 查询缓存(8.0之后没了, 原因是一般失效会非常频繁)。
   1. 当判断缓存是否命中时，MySQL不会进行解析查询语句，而是直接使用SQL语句和客户端发送过来的其他原始信息。所以，任何字符上的不同，例如空格、注解等都会导致缓存的不命中。）
3. 分析器(词法分析 ->语法分析)
   1. （SQL语法是否写错了）。 如何把语句给到预处理器，检查数据表和数据列是否存在，解析别名看是否存在歧义。
4. 优化器(决定索引的最佳使用方案)。是否使用索引，生成执行计划。
5. 执行器(检查权限 -> 执行语句 -> 返回结果集)
   1. 交给执行器，将数据保存到结果集中，同时会逐步将数据缓存到查询缓存中，最终将结果集返回给客户端。

![img](https://cdn.nlark.com/yuque/0/2022/png/22219483/1647160345866-2e93225c-5e99-4aa5-a2b9-764c1cbef23b.png)

更新语句执行会复杂一点。需要检查表是否有排它锁，写 binlog，刷盘，是否执行 commit。

## MySQL字符集
字符集规定了字符在数据库中的存储格式，比如占多少空间，支持哪些字符等等。不同的字符集有不同的编码规则，在有些情况下，甚至还有校对规则的存在。在运维和使用MySQL数据库中，选取合适的字符集非常重要，如果选择不恰当，轻则影响数据库性能，严重的可能导致数据存储乱码。
常见的MySQl字符集主要有以下四种：

| **字符集** | **长度** | **说明** |
| --- | --- | --- |
| GBK | 2 | 支持中文，但是不是国际通用字符集 |
| UTF-8 | 3 | 支持中英文混合场景，是国际通用字符集 |
| latin1 | 1 | MySQL默认字符集 |
| utf8mb4 | 4 | 完全兼容UTF-8，用四个字节存储更多的字符 |

MySQL数据库在开发运维中，字符集选用规则如下：
1、如果系统开发面向国外业务，需要处理不同国家、不同语言，则应该选择utf-8或者utf8mb4。
2、如果只需要支持中文，没有国外业务，则为了性能考虑，可以采用GBK。

## 设置数据库的字符集和设置表字段字符集的区别是什么？
mysql提供4种不同的颗粒度

1. server,全局级
2. 数据库级
3. 表级
4. 列级

4个级别作用域依次递减，优先级依次递增。就是设置的列字符集>表>库>server
如果修改库的字符集不会对原有的数据字符集进行改变，只会影响新增字符集。
如果修改表和列字符集，会对历史数据进行修改
