# Scala

函数式编程，变量不可变更，可以更好的利用多核CPU的并发性能。

Martin Odersky，Scala之父，javac开发者。

Scala是纯粹的面向对象语言，但是既有面向对象特性，也有函数式特性。运行在Java虚拟机，与java完全兼容。

支持lambda表达式（匿名函数），高阶函数（函数名作为函数传入），


## 基础
### 变量，数据类型：
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
var i = if(x > 0) 1 else -1 //if可以又返回值。

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
	println(i) // 1 2 3 2 4 6
}

val r = for(i <- Array(1,2,3,4,5) if i%2 == 0) yield {
	println(i)
	i
} //r = [2,4]，是个Array
```

