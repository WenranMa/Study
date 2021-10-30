# Scala

函数式编程，变量不可变更，可以更好的利用多核CPU的并发性能。

Martin Odersky，Scala之父，javac开发者。

Scala是纯粹的面向对象语言，但是既有面向对象特性，也有函数式特性。运行在Java虚拟机，与java完全兼容。

支持lambda表达式（匿名函数），高阶函数（函数名作为函数传入），


## 基础

### 变量，数据类型
Byte, Short, Int, Long, Float, Double, Boolean, Char这些都是类，String类型直接复用了Java中的String。

字面量（Literal），val i=123  //123就是整型的字面量

操作符实际是对象的方法。val sum=5+3 //等价于5.+(3)

富包装类，例如Int对应RichInt，里面定义了更多的不常用的方法。

变量分为可变不可变两种：
- val，不可变，必须初始化。val a：Int = 123
- var，可变，可以初始化。var b: Int = 12

类型推断（type inference）可以不声明类型，系统会自动推断。

### 输入输出
```scala
import io.StdIn._ //._表示全部导入
var i = readInt()

print(i)
```
print()被定义在scala.Predef里面，自动加载，不需要import，所以可以直接调用。

插值字符串，字符串中可以类似jenkins groovy脚本中的$name做变量替换。

### 控制结构

```scala
var i = if(x > 0) 1 else -1 //if可以有返回值。

for(i <- 1 to 5){
	println(i)
}

for(i <- 1 to 5 by 2){
	println(i)
}

for(i <- 1 to 5 if i%2 == 0 ){
	println(i)
}

for(i <- 1 to 2; j <- 1 to 3){
	println(i*j) // 1 2 3 2 4 6
}

val r = for(i <- Array(1,2,3,4,5) if i%2 == 0) yield {
	println(i)
	i
} //r = [2,4]，是个Array
```

### 数组Array
```scala
val arr = new Array[Int](3) //初始化为0，下标从0开始。
arr(0) = 12  //用圆括号，给元素赋值。

val arr = Array(1,2,3)
val arrs = Array("WRM", "XYH")
```

Array.ofDim()方法，可以定义多维数组
```scala
val arr2D = new Array.ofDim[Int](3,5) // 3x5的二维数组。
arr2D(0)(1) //返回二维数组某个元素。
```

### 元组Tuple
对不同类型元素的一个简单封装。用小括号括起来，就是元组。同下划线访问。
```scala
val t = ("wrma", 34, 169.5)
print(t._1)  //从1开始
print(t._2)
print(t._3)
```

### 容器

scala.collection库，定义了可变容器和不可变容器的一些通用操作。
是scala.collection.mutable和scala.collection.immutable两个库的超类（特质Trait）。

Traversable（Trait）在最高层，Iterable继承Traversable，下面Seq，Set，Map继承Iterable。

#### List
具体的容器类，它继承了LinearSeq特质，定义在scala.collection.immutable中。
```scala
val l = List("wrma", "xyhu")
print(l.head) //wrma
print(l.tail) //xyhu

val l2 = "xxx"::l  //在l的头部加一个元素，生成一个新的List。
val li = 1::2::3::Nil // 从右往左执行。
```

#### Vector
```scala
val v1 = Vector(1,2)
val v2 = 3+:4+:v1 //(3, 4, 1, 2)
val v3 = v2:+5 // (3, 4, 1, 2, 5)
```

#### Range
带索引的不可变数字等差序列。
```scala
val r = new Range(1,5,1) 	// 与 1 to 5是一个意思。
							// 1.to(5) 同意。

1 until 5 // (1,2,3,4)
1 to 10 by 2 //(1,3,5,7,9)
```

#### Set
Set有可变和不可变两种。

#### Map
也是可变和不可变两种。
```scala
val m = Map(1->"wrma", 2->"xyhu")
```





