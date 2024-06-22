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

### 事务的隔离级别

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


### B+树的主要特点：

我们今天要介绍的是工作开发中最常接触到的 InnoDB 存储引擎中的 B+ 树索引。要介绍 B+ 树索引，就不得不提二叉查找树，平衡二叉树和 B 树这三种数据结构。B+ 树就是从他们仨演化来的。

1. 二叉查找树

二叉查找树的特点就是任何节点的左子节点的键值都小于当前节点的键值，右子节点的键值都大于当前节点的键值。顶端的节点我们称为根节点，没有子节点的节点我们称之为叶节点。

利用二叉查找树我们只需要 log(n) 次即可找到匹配的数据。

2. 平衡二叉树
上面我们讲解了利用二叉查找树可以快速的找到数据。但是，如果上面的二叉查找树是这样的构造：
5是root.

5 -> 6 -> 7 -> 9 -> 11 -> 13 -> 15

这个时候可以看到我们的二叉查找树变成了一个链表。如果我们需要查找 id=15 的用户信息，我们需要查找 7 次，也就相当于全表扫描了。 导致这个现象的原因其实是二叉查找树变得不平衡了，也就是高度太高了，从而导致查找效率的不稳定。为了解决这个问题，我们需要保证二叉查找树一直保持平衡，就需要用到平衡二叉树了。 平衡二叉树又称 AVL 树，在满足二叉查找树特性的基础上，要求每个节点的左右子树的高度差不能超过 1。 

平衡二叉树保证了树的构造是平衡的，当我们插入或删除数据导致不满足平衡二叉树不平衡时，平衡二叉树会进行调整树上的节点来保持平衡。

3. B 树
因为内存的易失性。一般情况下，我们都会选择将 user 表中的数据和索引存储在磁盘这种外围设备中。但是和内存相比，从磁盘中读取数据的速度会慢上百倍千倍甚至万倍，所以，我们应当尽量减少从磁盘中读取数据的次数。另外，从磁盘中读取数据时，都是按照磁盘块来读取的，并不是一条一条的读。如果我们能把尽量多的数据放进磁盘块中，那一次磁盘读取操作就会读取更多数据，那我们查找数据的时间也会大幅度降低。如果我们用树这种数据结构作为索引的数据结构，那我们每查找一次数据就需要从磁盘中读取一个节点，也就是我们说的一个磁盘块。我们都知道平衡二叉树可是每个节点只存储一个键值和数据的。那说明什么？说明每个磁盘块仅仅存储一个键值和数据！那如果我们要存储海量的数据呢？

可以想象到二叉树的节点将会非常多，高度也会极其高，我们查找数据时也会进行很多次磁盘 IO，我们查找数据的效率将会极低！


为了解决平衡二叉树的这个弊端，我们应该寻找一种单个节点可以存储多个键值和数据的平衡树。也就是我们接下来要说的 B 树。

B 树（Balance Tree）即为平衡树的意思，
图中的 p 节点为指向子节点的指针，二叉查找树和平衡二叉树其实也有，因为图的美观性，被省略了。

图中的每个节点称为页，页就是我们上面说的磁盘块，在 MySQL 中数据读取的基本单位都是页，所以我们这里叫做页更符合 MySQL 中索引的底层数据结构。

从上图可以看出，B 树相对于平衡二叉树，每个节点存储了更多的键值（key）和数据（data），并且每个节点拥有更多的子节点，子节点的个数一般称为阶，3 阶 B 树，高度也会很低。

基于这个特性，B 树查找数据读取磁盘的次数将会很少，数据的查找效率也会比平衡二叉树高很多。

假如我们要查找 id=28 的用户信息，那么我们在上图 B 树中查找的流程如下：

先找到根节点也就是页 1，判断 28 在键值 17 和 35 之间，那么我们根据页 1 中的指针 p2 找到页 3。
将 28 和页 3 中的键值相比较，28 在 26 和 30 之间，我们根据页 3 中的指针 p2 找到页 8。
将 28 和页 8 中的键值相比较，发现有匹配的键值 28，键值 28 对应的用户信息为（28，bv）。
 

4. B+ 树
B+ 树是对 B 树的进一步优化。 B+ 树和 B 树有什么不同：

1. B+ 树非叶子节点上是不存储数据的，仅存储键值，而 B 树节点中不仅存储键值，也会存储数据。

之所以这么做是因为在数据库中页的大小是固定的，InnoDB 中页的默认大小是 16KB。

如果不存储数据，那么就会存储更多的键值，相应的树的阶数（节点的子节点树）就会更大，树就会更矮更胖，如此一来我们查找数据进行磁盘的 IO 次数又会再次减少，数据查询的效率也会更快。

另外，B+ 树的阶数是等于键值的数量的，如果我们的 B+ 树一个节点可以存储 1000 个键值，那么 3 层 B+ 树可以存储 1000×1000×1000=10 亿个数据。

一般根节点是常驻内存的，所以一般我们查找 10 亿数据，只需要 2 次磁盘 IO。

2. 因为 B+ 树索引的所有数据均存储在叶子节点，而且数据是按照顺序排列的。

那么 B+ 树使得范围查找，排序查找，分组查找以及去重查找变得异常简单。而 B 树因为数据分散在各个节点，要实现这一点是很不容易的。

B+ 树中各个页之间是通过双向链表连接的，叶子节点中的数据是通过单向链表连接的。

其实上面的 B 树我们也可以对各个节点加上链表。这些不是它们之前的区别，是因为在 MySQL 的 InnoDB 存储引擎中，索引就是这样存储的。

也就是说上图中的 B+ 树索引就是 InnoDB 中 B+ 树索引真正的实现方式，准确的说应该是聚集索引（聚集索引和非聚集索引下面会讲到）。

通过上图可以看到，在 InnoDB 中，我们通过数据页之间通过双向链表连接以及叶子节点中数据之间通过单向链表连接的方式可以找到表中所有的数据。


节点结构：B+树的每个节点可以包含多个关键字和对应的指针。叶子节点存储实际的数据记录或指向数据记录的指针，而内部节点（非叶子节点）只存储关键字和指向子节点的指针。

有序性：B+树中的关键字保持有序，这使得范围查询（如查找某个值区间的所有记录）非常高效。

所有叶子节点相连：B+树的所有叶子节点通过指针连接成一个链表，这使得遍历所有数据记录变得简单快速。

分支因子：每个节点能容纳的最大子节点数量称为分支因子，较大的分支因子可以减少树的高度，从而减少磁盘I/O次数，提高查询效率。

在数据库中的应用：
索引结构：B+树是关系型数据库中最常用的索引结构之一，因为它能够高效地支持快速查找、顺序访问以及范围查询。

磁盘友好：由于数据库数据通常存储在外存中，B+树的设计考虑了磁盘I/O的效率。通过最大化节点内数据量，减少树的高度，进而减少磁盘访问次数。

范围查询优化：由于B+树的叶子节点包含了所有数据记录的指针，并且叶子节点间通过指针相连，这使得执行范围查询时可以直接从一个叶子节点遍历到另一个叶子节点，无需回溯到根节点。

插入与删除：B+树在插入和删除操作时会自动调整以保持平衡，确保查询性能稳定。虽然这些操作可能比在内存中的数据结构更复杂，但通过分裂和合并节点等机制，仍能维持较高的效率。

缓存友好：数据库系统通常会利用缓存（如缓冲池）来减少磁盘访问。B+树的结构使得经常访问的数据或其索引更有可能被缓存，进一步提升查询速度。



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





### 隔离级别演示：

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