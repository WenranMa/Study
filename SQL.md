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