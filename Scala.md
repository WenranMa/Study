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
update方法约定：
- 当对带有括号并包括一到若干参数的对象进行赋值时。
- 编译器将调用对象的update方法。

```scala
val s = new Array[String](3)
s(0) = "wrma" // 与s.update(0, "wrma")等价的。
```

#### unapply方法
反向解构的过程。apply是通过参数传递构建对象，unapply是已经有了对象，提取出参数。

```scala
class Car(var brand: String, var price: Int) {
	def info():Unit = {
		printf("Car brand is %s, price is %d.\n", brand, price)
	}
}

object Car{
	def apply(brand: String, price: Int) = {
		println("apply method called ...")
		new Car(brand, price)
	}
	def unapply(c: Car): Option[(String, Int)] = {
		println("unapply method called ...")
		Some((c.brand, c.price))
	}
}

object Main{
	def main(args: Array[String]): Unit = {
		var Car(b,p) = Car("BMW", 50000)  //这句同时调用了apply和unapply方法。
		println("Car brand is " + b + ", and price is " + p + ".")
	}
}
//Option和Some暂时未知。
```

### 继承
抽象类，一个类中包含没有被实现的成员，就是抽象类，必须用abstract做修饰。

- 需要使用abstract关键字定义抽象类。
- 抽象方法不需要abstract，不定义即可。
- 字段没有初始化，就是抽象字段，必须给类型声明。
- extends关键字继承，override关键字重载。
- override可选，父类本身抽象的字段，子类重载可以不加override。
- 如果父类中成员本身被实现或赋值，子类重载必须加override。
- 只能重载val类型，因为var类型本身是变量，不存在重载。

```scala
abstract class Car {
	val carBrand: String //字段没有初始化，就是抽象字段。
	def info(): Unit //抽象方法
	def greeting(): Unit = {
		println("Welcome ~ ~ ~ ~")
	}
}

class BMWCar extends Car {
	override val carBrand = "BMW"
	def info(): Unit = {
		println("BMW Car ...")
	}
	override def greeting(): Unit = {
		println("Welcome BMW ~ ~ ~ ~")
	}
}

class BYDCar extends Car {
	override val carBrand = "BYD"
	def info(): Unit = {
		println("BYD Car ...")
	}
	override def greeting(): Unit = {
		println("Welcome BYD ~ ~ ~ ~")
	}
}

object Main {
	def main(args: Array[String]): Unit = {
		val c1 = new BMWCar()
		var c2 = new BYDCar()
		c1.greeting()
		c2.greeting()
	}
}
```

类层次：
- 最高层是Any类
- 下面两个AnyVal，AnyRef
- AnyVal是对应的基础类型，Int，Double等，但不包括String（java过来的）。
- AnyVal类型存在寄存器中，不能用new实例化。
- AnyRef引用类型，对应其他所有类，在堆内存中。
- Null是AnyRef的子类，为了兼容java。
- Nothing是所有类的子类。
- Option类，用于取代Null，有个Some子类，只要返回是Option类型，都会封装成Some对象。
- Option中还有个None对象，没有返回值就返回None，有就是Some。
- Some对象的get方法，返回被包装的对象。
- getOrElse方法，有就返回，没有就返回else中封装的对象。

case class会自动封装apply方法。

```scala
case class Book(val name: String, val price: Int)
val books = Map("spark" -> Book("Spark", 20))
books.get("spark") //返回 Option[Book] = Some(Book(Spark, 20))
books.get("hive") //返回 Option[Book] = None
books.get("spark").get //返回Book = Book(Spark, 20)
books.get("hive").get //抛出异常
books.get("hive").getOrElse(Book("Unknown", 0)) //返回Book(Unknown, 0)
```

### 特质Trait
类似java中的接口但有区别。Trait可以定义抽象方法，也可以提供具体方法实现。

一个类只能继承一个父类，但却可以混入（mixin）多个Trait。简介实现多重继承。

定义特质用trait关键字，继承特质可以用with关键字或extends关键字。

```scala

```

### 匹配模式
match case语句，类似其他语言的swith语句。
```scala
for(elem <- List(6, 9, 3.14, "spark", "hive")){
	val str = elem match{
		case i: Int => i + " is an int value."
		case d: Double => d + " is an double value."
		case s: String => s + " is an string value."
		case "spark" => "spark in this list."
		case _ => "unexpected " + elem
	}
	println(str)
}
//可以匹配值，也可以匹配类型。
//case _ 表示进来什么值都可以。

for(elem <- List(1, 2, 3, 4)){
	elem match{
		case _ if(elem % 2 == 0) => println(elem + " is even.")
		case _ => println(elem + " is odd.")
	}
}
```

case class，在类定义前加case，会自动重载很多method，比如toString，equals等。同时会自动生成类的伴生对象，也就有apply的工厂方法和unapply方法。

### 包











