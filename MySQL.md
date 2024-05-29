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

### 技巧

#### JOIN解决错误
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

#### JOIN优化子查询技巧：
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




## MySQL 面试题

### 适合添加索引的情况
1. 字段的数值有唯一性的限制

索引本身可以起到约束的作用，比如唯一索引、主键索引都可以起到唯一性约束的，因此我们在创建数据表时，如果某个字段时唯一的，就可以直接创建唯一性索引或主键索引。不要以为唯一索引影响了 insert 的速度，这个速度损耗可以忽略不计，单体高查找速度是明显的。

2. 频繁作为 where 查询条件的字段

如果某个字段经常在(包括 insert、update、delete 的) where 条件中被使用到，那么就需要给这个字段创建索引。尤其是在数据量大的情况下，创建普通索引就可以大幅提高查询效率。

3. 经常 group by 和 order by 的列

索引就是让数据按照某种顺序进行存储或检索，因此我们使用 group by 对数据进行分组查询，或者使用 order by 对数据进行排序的时候，就需要对分组或者排序的字段添加索引。如果待排序的列有多个，那么就可以在这些列上建立组合索引。

4. distinct 字段需要创建索引

有时我们需要对某个字段进行去重，使用 distinct，那么对这个字段创建索引，就能大幅提高效率。

5. 多表 join 连接操作时

首先，连接表的数量尽量不要超过3张，因为每增加一张表就相当于增加了一次嵌套的循环，数量级增长的非常快，严重影响查询效率。
其次，需要对 where 条件中的字段创建索引，因为 where 才是对数据条件的过滤。如果在数据量非常大的情况下，没有 where 条件过滤时非常可怕的。
最后，对用于连接的字段进行创建索引，并且该字段在多张表中的类型必须一致。因为如果数据类型不一致会进行隐式转换，索引就会失效。

6. 存储长字符串时建议使用字符串前缀创建索引

假设我们的字符串很长，那存储字符串就需要占用很大的存储空间。在我们需要为这个字符串列创建索引时，那就意味着对于的 b+ 树种有这么两个问题：

b+ 树索引中的记录需要把列的完整字符串存储起来，很费时。并且字符串越长，在索引中占用的存储空间就越大。
如果 b+ 树索引中索引列存储的字符串很长，拿在做字符串比较时会占用更多的时间。
因此我们可以通过截取字符串前面一部分内容建立索引，这就叫前缀索引。这样在查找记录时虽然不能精确的定位到记录的位置，但是能定位到相应前缀所在的位置，然后根据前缀相同的记录的主键回表查询完整的字符串值。即节约空间又减少了字符串的比较时间，还可以答题解决排序的问题。
注意：如果使用了索引列前缀的方式可能会导致使用索引排序时结果出错，只能使用文件排序。

7. 区分度高(散列性高)的列适合创建索引

列的基数指的是某一列中重复的个数，也就是说，在记录行数一定的情况下，列的基数越大，该列中的数值越分散；列的基数约小，该列中的数值越集中。这个列的基数指标会直接影响我们是否能有效的利用索引，为基数太小的列创建索引的效果可能不好。
可以使用公式 select count(distinct a)/count(*) from table 计算区分度，越接近1越好，一般超过 0.33 就算是基数比较高的列了。因此，有大量重复数据的列上就不用建立索引了。

### 不适合添加索引的情况
1. 在条件判断中没有使用的字段不用创建索引

在 where、group by、order by 里用不到的字段不需要创建索引，索引的价值时快速定位，如果起不到定位的字段通常是不需要建立索引的。

2. 数据量小的表最好不要使用索引

如果表记录太少，那么时不需要创建索引的。表记录太少的话，有没有索引对查询效率的影响并不大。甚至说，查询花费的时间可能比遍历索引的时间还要短，索引可能不会产生优化效果。

3. 避免对经常更新的字段创建索引

频繁更新的字段不一定要创建索引。因为数据更新的时候，也需要更新索引，如果索引太多，在更新索引的时候也会造成负担，从而影响效率。
避免对经常更新的表创建过多索引，并且索引中的列尽可能少。否则，虽然提高了查询速度，但却降低更新表的速度。

4. 不建议用无序的值作为索引

例如：身份证、UUID、MD5、HASH、无序长字符串等。

5. 很少使用或不使用的列无需建立索引

表中的数据被大量更新，或者数据的使用方式被改变后，原有的一些索引可能不再需要。DBA 应当定期找出这些索引，将他们删除，从而减少索引对更新操作的影响。

6. 已经有索引的列尽量避免定义冗余或重复索引

比如某些字段已经存在于联合索引中了，就不在需要单独创建索引。又或者某个字段已经创建了唯一索引，则无需在定义一个普通索引。

补充说明
- 在多个字段都要创建索引的情况下，联合索引优于单值索引。
创建联合索引时，使用最频繁的列需要放到联合索引的左侧。在进行查询时，也应该把使用最频繁的列放在最左侧。
- 索引是一般双刃剑，可以提高查询效率，但也会降低插入和更新的速度，并占用更多的磁盘空间。
在实际工作中，我们也需要注意平衡，索引的数目不是越多越好。我们需要限制每张表上的索引数量尽量不超过 6 个。原因：
	- 每个索引都需要占用磁盘空间，索引越多，需要的磁盘空间就越大。
	- 索引会影响 insert、delete、update 等语句的性能，因为表中的数据更改的同时，索引也会进行调整和更新，会造成负担。
	- 优化器在选择如何优化查询时，会根据统一信息对每一个可以用到的索引来进行评估，以生成一个最好的执行计划，如果同时有很多个索引可以用于查询，会增加 mysql 优化器生成执行计划时间，降低查询性能


## 事务

事务是数据库区别于文件系统的重要特性之一，当我们有了事务就会让数据库始终保持`一致性`，同时我们还能通过事务的机制`恢复到某个时间点`，这样我们就可以保证已提交到数据库的修改不会因为系统崩溃而丢失。mysql 数据库目前只有 `InnoDB` 存储引擎是支持事务的。

事务：一组逻辑操作单元，使数据库从一种状态变换到另一种状态。

事务处理的原则：保证所有操作都作为一个工作单元来执行，即使出现了故障，都不能改变这种执行方式。当在一个事务中执行多个操作时，要么所有的操作都被提交(commit)，那么这些修改就永久保存下来；要么数据库管理系统将放弃所有修改，整个事务回滚(rollback)到最初状态。

事务的 ACID 特性
- 原子性(atomicity)：原子性是指事务是一个不可分割的工作单位，要么全部提交，要么全部失败回滚。
- 一致性(consistency)：一致性是指事务执行前后，从一个合法性状态(满足预定的约束的状态)变换到另一个合法性状态。这种状态是语义上的而不是语法上的，跟具体的业务有关。
- 隔离性(isolation)：隔离性是指事务的执行不能被其他事务干扰，即一个事务内部的操作及使用的数据对并发的其他事务是隔离的，并发执行的各个事务之间不能互相干扰。
- 持久性(durability)：持久性是指一个事务一旦被提交，他对数据库的改变就是永久性的，接下来的其他操作和数据库故障不应对其有任何影响。持久性是通过事务日志来保证的，包括了重做日志和回滚日志。

事务的状态
- 活动的(active)：事务对应的数据库操作正在执行过程中，我们就说该事物处在活动的状态。
- 部分提交的(partially committed)：当事务中的最后一个操作执行完成，但由于操作都在内存中执行，所造成的影响并没有刷新到磁盘时，我们就说该事务处在部分提交的状态。
- 失败的(failed)：当事务处在活动的或部分提交的状态时，可能遇到了某些错误(数据库自身错误、操作系统错误或直接断电等)而无法继续执行，或者人为的停止当前事务的执行，我们就说该事务处在失败的状态。
- 中止的(aborted)：如果事务执行了一部分操作后变为了失败的状态，那么就需要把已经修改的事务中的操作还原到事务执行前的状态。我们把这个撤销的过程称之为回滚。当回滚操作完毕时，也就是数据库恢复到了执行事务之前的状态，我们就说该事务处在了中止的状态。
- 提交的(committed)：当一个处在部分提交的状态的事务将修改过的数据都同步到磁盘上之后，我们就可以说该事务处在了提交的状态。

开启事务

1. 显式事务

使用关键字start transction或begin开启事务，使用commit提交事务，使用rollback回滚事务。例如：

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
start transction 可以跟 read only / read write / with consistent snapshot

read only：表示当前事务是一个只读事务，也就是属于该事务的数据库操作只能读取数据，而不能修改数据。(只读事务只是不允许修改那些其他事务也能访问到的表中的数据，对于临时[使用 create tmeporary table 创建的表]表来说，由于它们只能在当前会话中可见，所以只读事务也是可以对临时表进行增、删、改操作的)
read write：表示当前事务是一个读写事务，也就是属于该事务的数据库操作既可以读取数据，也可以修改数据。
with consistent snapshop：启动一致性读。

2. 隐式事务

mysql 中有一个系统变量autocommit(默认值 ON)，默认请情况下，如果我们不显式使用 start transaction 或 begin 语句开启一个事务，那么每一条 DML(数据库操作语言) 语句都算是一个独立的事务，这种特性称之为事务的自动提交。如果我们想关闭这种自动提交的功能可以使用显式事务或把 autocommit 的值改为 OFF。这样的话，我们写入多条语句就算是属于同一个事务了，直到我们显式写出 commit 语句提交事务或写出 rollback 回滚事务才可以真正修改数据。

事务的隔离级别

mysql 是客户端/服务器架构的软件，对于一个服务器来说，可以有若干个客户端与之连接，每个客户端与服务器连接之后，就可以称之为一个会话(session)。每个客户端都可以在自己的会话中向服务器发出请求语句，一个请求语句可能是某个事务的一部分，可就是对于服务器来说可能同时处理多个事务。事务有隔离性的特性，理论上在某个事务对某个数据进行访问时，其他事物应该进行排队，当事务提交之后，其他事务才可以继续访问这个数据。但是这样对性能的影响太大，我们既想保持事务的隔离性，又想让服务器在处理访问同一数据的多个事务时性能尽量高些，因此就需要采用适当的隔离级别。

数据并发问题(严重级别从高到低)
- 脏写(Dirty Write)：对于两个事务 SessionA、SessionB，如果事务 SessionA 修改了另一个未提交事务 SessionB 修改过的数据，那就意味着发生了脏写。
- 脏读(Dirty Read)：对于两个事务 SessionA、SessionB，SessionA 读取了已经被 SessionB 更新但还没与被提交的数据。若之后 SessionB 回滚，SessionA 读取的内容就是临时且无效的，称为脏读。
- 不可重复读(Non-Repeatable Read)：对于两个事务 SessionA、SessionB，SessionA 读取了一个字段，然后 SessionB 更新了该字段。之后 SessionA 再次读取同一个字段，值读到的值就不同了。就意味着发生了不可重复读。
- 幻读(Phantom)：对于两个事务 SessionA、SessionB，SessionA 从一个表中读取了一个字段，然后 SessionB 在该表中插入了一些新的行。之后如果 SessionA 再次读取同一个表，就会多出几行，我们把多出来的行称之为幻影记录，该现象称为幻读。

SQL 的隔离级别(从低到高)
- READ UNCOMMITTED：读未提交，在该隔离级别，所有事务都可以看到其他未提交事务的执行结果。仅能避免脏写，不能避免脏读、不可重复读、幻读。
- READ COMMITTED：读已提交，它满足了隔离级别的简单定义(一个事务只能看见已提交事务所做的改变)。可以避免脏写、脏读，但不能避免不可重复读、幻读。
- REPEATABLE READ：可重复读，事务 A 在读到一条数据之后，此时事务 B 对该数据进行了修改并提交，那么事务 A 再读改数据，读到的还是原来的内容。可以避免脏写、脏读、不可重复读，但幻读问题仍然存在。mysql 默认的隔离级别
- SERIALIZABLE：可串行化，确保事务可以从一个表中读取相同的行。在这个事务持续期间，禁止其他事务对该表执行插入、更新和删除操作。该级别所有并发问题都可以避免，但性能十分低下。

mysql 查看隔离级别
-- mysql 5.7.20 之前查看隔离级别
show variables like 'tx_isolation';
-- mysql 5.7.20 之后查看隔离级别
show variables like 'transaction_isolation';
-- 查看隔离级别(各版本都可以使用)
select @@transaction_isolation;

mysql 设置隔离级别
/*
隔离级别：READ UNCOMMITTED、READ COMMITTED、REPEATABLE READ、SERIALIZABLE
*/
set [global | session] transaction isolation level 隔离级别;
或者

/*
隔离级别：READ-UNCOMMITTED、READ-COMMITTED、REPEATABLE-READ、SERIALIZABLE
*/
set [global | session] transaction_isolation='隔离级别';



## Mysql 数据库性能分析工具简介

### explain
`explain [format=JSON | TREE] select * from demo_table where id=1;`

mysql 中有专门负责优化 select 语句的优化器模块，主要功能：通过计算分析系统中收集到的统计信息，为客户端请求的 Query 提供它认为最优的执行计划(它认为最优的数据检索方式不一定是 DBA 认为最优的，这部分最耗费时间)。

mysql 5.6.3 以前 explain 只能分析 select 语句，5.6.3 之后就可以分析 select、update、delete

explain 语句输出的各个列的含义如下：

- id：代表查询执行中的执行顺序标识号和执行优先级
- select_type：select 关键字对于的查询类型
- table：表名
- partitions：匹配的分区信息，代表分区表的命中情况，非分区表该项为 NULL。
- type：针对单表的访问方法，常见值如下(从好到坏)：
	- system：当表中只有一条记录并且该表使用的存储引擎的统计数据时精确的(如：MyISAM、Memory)，那么对该表的访问方法就是 system
	- const：当我们根据主键或唯一索引列与常数进行等值匹配时，对单表的访问方法就是 const
	- eq_ref：在连接查询时，如果被驱动表是通过主键或唯一二级索引等值匹配的方式进行访问的(如果该主键或唯一二级索引时联合索引的话，所有的索引列都必须进行等值比较)，则对该被驱动表的访问方法就是 eq_ref。
	- ref：当通过普通二级索引与常量进行等值匹配时来查询某个表，那么该表的访问方法就是 ref。
	- ref_or_null：当对普通二级索引进行等值匹配查询，该索引列的值也可以时 null 值时，那么对该表的访问方法就可能是 ref_or_null。
	- index_merge：单表访问方法时在某些场景下可以使用 Intersection、Union、Sort-Union 这三种索引合并的方式来执行，那么对该表的访问方法就是 index_merge。
	- unique_subquery：针对在一些包含 in 子查询的查询语句中，如果查询优化器决定将 in 子查询转换为 exists 子查询，且子查询可以使用到主键进行等值匹配的话，那么该子查询执行计划的类型就是 unique_subquery。
	- range：如果使用索引获取某些范围区间的记录，那么就可能使用到 range 访问方法。
	- index：当我们可以使用索引覆盖，但需要扫描圈闭的索引记录时，该表的访问方法就是 index。
	- ALL：全表扫描
		sql 性能优化的目标至少要达到 range 级别
- possible_keys：可能用到的索引
- key：实际用到的索引
- key_len：实际使用到的索引长度(即字节数)，主要针对于联合索引有一定参考意义。
- ref：当使用索引列等值查询时，与索引列进行等值匹配的对象信息。
- rows：预估的需要读取的记录条数，该数值越小越好
- filtered：某个经过搜索条件过滤后剩余记录数的百分比，该数值越大越好
extra：额外信息，包含不适合在其他列中显示但十分重要的信息。我们可以通过这些信息来更准确的理解 mysql 到底将如何执行给定的查询语句。
mysql 5.7 以前的版本总，要想显示 partitions 需要使用 explain partitions 命令，想要显示 filtered 需要使用 explain extended 命令。在 5.7 版本后，默认显示中就包含了 partitions 和 filtered 信息。

注意：

explain 不考虑各种 Cache
explain 不能显示 mysql 在执行查询时优化器所做的工作
explain 不会告诉你关于触发器、存储过程的信息或用户自定义函数时对查询的影响情况
部分统计信息时估算的，并非精确值



### mysql乐观锁悲观锁

在MySQL中，乐观锁和悲观锁是两种不同的并发控制策略，用于处理多用户同时访问同一数据时可能引发的并发问题。下面分别介绍这两种锁的特点、实现方式和适用场景。

悲观锁 (Pessimistic Lock)
概念： 悲观锁假定会发生并发冲突，因此在数据处理前就进行加锁，阻止其他事务对数据的访问，直到当前事务结束。这种策略较为保守，适用于写操作频繁且并发冲突较多的场景。

实现方式：

SELECT ... FOR UPDATE： 在查询语句中加入FOR UPDATE子句，可以对查询结果集中的行加写锁，确保其他事务无法修改这些行，直到当前事务结束。
锁定级别： InnoDB存储引擎支持行级锁，因此悲观锁通常是行锁。
注意事项： 使用悲观锁时，需关闭MySQL的自动提交模式(SET autocommit = 0;)，并在事务结束后手动提交(COMMIT)或回滚(ROLLBACK)。

乐观锁 (Optimistic Lock)
概念： 乐观锁假设数据一般不会发生并发冲突，仅在数据更新提交时检查数据是否被其他事务修改过。如果数据未被修改，则提交成功；否则，根据策略重试或回滚事务。这种方式减少了锁的开销，提高了系统的并发性能。

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


### 索引失效
MySQL索引失效是指在执行查询时，尽管相关字段上存在索引，但数据库管理系统没有利用这些索引来加速查询过程，而是选择了全表扫描等效率较低的策略。这可能导致查询性能下降。以下是一些可能导致索引失效的常见场景：

使用不等于(!= 或 <>)操作符： 当查询条件使用不等于操作符时，索引可能不会被使用，尤其是对于复合索引的第一个列。

使用LIKE操作符进行模糊查询： 如果LIKE模式以通配符开头（如'%value'），索引通常无法使用。但如果是固定前缀匹配（如'value%'），索引可能仍会被利用。

使用函数或表达式： 在查询条件中，如果对索引列进行了函数运算或表达式计算，如ABS(column) > 10，索引可能失效。

类型转换： 当索引列与比较值类型不匹配时，MySQL可能需要进行类型转换，这可能导致索引失效。特别是字符串与数字比较时，如果字符串需要被转换成数字，可能会导致索引不能使用。

- 复合索引未按顺序使用： 对于复合索引（多个列组成的索引），如果查询条件没有按照索引定义的顺序使用列，索引可能部分或完全失效。

索引列参与计算： 如果查询条件中包含了索引列的计算，如column + 1 = value，索引可能无法被优化器识别并使用。

OR连接条件： 使用OR连接多个条件时，如果每个条件单独都有索引，但优化器无法确定最佳索引时，可能会选择全表扫描。

索引列上使用NOT操作符： 类似于不等于操作符，使用NOT操作符也可能导致索引失效。

索引覆盖不全： 查询中需要的所有列没有被索引覆盖（即构成覆盖索引），导致即使使用了索引，也需要回表获取其他列数据，影响性能。

超出索引范围的比较： 对于某些数据类型（如无符号整数），如果比较值超出了索引列的范围，索引可能不会被使用。

使用IS NULL或IS NOT NULL： 在某些情况下，这些条件可能不会利用索引。

要诊断索引是否被正确使用，可以使用EXPLAIN命令查看查询执行计划，其中key列显示了实际使用的索引，如果显示为NULL，则表示没有使用索引




