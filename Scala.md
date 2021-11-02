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


## 面向对象

### Class
```scala
class Counter{
	var value = 0	//也可以用val定义不可变量。
	def increase(step:Int):Unit = {value += step}
	def current():Int = {value}
}

// def定义方法
// Unit表示不返回结果
// 不用return，方法的最后一个值就是返回值。

val c = new Counter //可以没有小括号
c.value = 5
c.increase(3) // 等价于 c increase 5，中缀调用。
println(c.current) //8，可以省略方法后面小括号。
```

可见性：成员也有可见范围，默认为public，private，protected。

通过一个成对的方法来实现getter和setter：
- value 
- value_=  //也不是赋值操作

方法特点：
- 方法的参数列表中不能有var，val。
- 没有参数时，可以省略小括号。
- 如果小括号在定义时省略，则调用时也不能有小括号。
- 定义时不省略，调用时省不省略均可。
- 如果只有一个参数，可以中缀调用。
- 如果方法体只有一条语句，也可以省略方法体大括号。
- 如果返回值可以被系统推断，则可以省略`：类型`。
- 如果返回值是Unit，则可以省略`:Unit=`，但不能省略大括号，这个好像deprecated了。

#### Constructor
类的定义主体就是一个构造器，叫主构造器。

在类的参数列表中加var或者val修饰的参数，会自动成为类的成员。

```scala
class Counter(var name:String) //不用大括号就可以定义一个类。
var c = new Counter("BJO") //构造Counter对象c。
println(c.name) // getter调用。
c.name_=("NYO") // setter调用。
println(c.name) 
c.name="NYO" // setter中缀调用。
```

如果参数列表里面没有var，val字段，则只是简单的传参。

辅助构造器：每个辅助构造器的第一条必须是调用前面已经定义的辅助构造器或者主构造器。

```scala
class Counter {
	private var value = 0
	private var name = ""
	private var step = 1
	println("Main constructor")
	
	def this(name: String){
		this() // 调用主构造器
		this.name = name
		println("First auxiliary constructor")
	}
	
	def this(name: String, step: Int){
		this(name) //调用第一个辅助构造器
		this.step = step
		println("Second auxiliary constructor")
	}
	
	def increase(step: Int):Unit = {value += step}
}
```

### Object
#### singleton 单例对象
```scala
object Person { // ojbect关键字，定义单例。
	private var lastId = 0 //内部字段是静态的。
	def newId()={
		lastId += 1
		lastId
	}
}

println(Person.newId()) // 可以直接调用，返回1.
println(Person.newId()) // 2.
```

伴生类，伴生对象：在一个scala文件中定义了class A和object A，他们就互为伴生类和伴生对象。可以互相访问内部资源？

没有重名的object就是孤立对象。

```scala
class P(var name: String){
	private val id = P.newId()
	def info():Unit = {
		printf("name:%s, ID:%d\n", name, id)
	}
}

object P{
	private var lastId = 0
	def newId()={
		lastId += 1
		lastId
	}
	
	def main(args: Array[String]):Unit = {
		val p1 = new P("wrma")
		val p2 = new P("xyhu")
		p1.info()
		p2.info()
	}
}

//scalac ./p.scala
//scala -classpath . P
```

#### apply方法
例如有的语句：`val arrs = Array("WRM", "XYH")`

可以不用new关键字才创建对象。

scala会自动调用Array这个类的伴生对象Array中的apply方法去创建一个Array对象。

apply方法约定：
- 用括号传递给类实例或者单例对象名一个或多个参数时。
- Scala会在类或者对象中查找apply方法。
- 且判断参数列表与传入的参数一致。
- 用传入的参数调用apply方法。

```scala
class P(var name:String){
	def apply(name:String):Unit={
		printf("Hi %s, apply method called.\n", name)
	}
}

var p = new P("z")
p("x") //will print 'Hi x, apply method called.'
```

Array的例子就是：
- 一个class Array
- 同时有一个伴生对象
- 类的构造方法以apply方法的形式写在伴生对象里面
- 写Array("xxx","yyy")时，伴生对象apply会被调用
- 生成类对象

apply方法的目的就是很好融合了面向对象和函数式编程。例如：
```scala
def add=(x:Int, y:Int)=>x+y
add(4,5) // 9，函数式调用。
add.apply(4,5) // 9，add也是对象，采用.method方法调用。

//def add(x:Int, y:Int):Int={x+y} 就不行？？？？

```

#### update方法









