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



