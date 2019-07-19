/*
JS中区分大小写

String：
Number + String = String.
parseInt() 字符串到Int
parseFloat() 字符串到Float

length属性
charAt()方法
indexOf()方法
lastIndexOf()方法,一个字符串中有多个相同的字符
subString()方法
replace()方法
split()方法，根据某个字符分割字符串，返回数组

Array: typeOf(Array) is Ojbect.
length属性
push()方法，添加在最后
pop()方法，弹出最后一个元素并返回
shift()方法，删除第一个并返回

delete Array[3], 删除值，并不给便数组长度
splice()方法，删除某个元素，并给便数组长度

concat()方法，合并数组并返回
*/

/*
function:
function setName() {}
let setName = function() {}
*/

/*
Object:
let person = {
	name: 'Wenran',
	age: 31
};
person.color = 'Yellow';
person['hobby'] = 'xxx';
person.show = function(){}

delete person.age, 返回true，表示删除成功。
*/

//=========================================================

/*
JS中有三种对象：
1. user-defined object
2. native object: like Array, Math, Date.
3. host object: 浏览器提供的对象。window, Form, Element, Image.

Node.
元素节点 element node: like <body> <div>
文本节点 text node: like the text inside <div></div>
属性节点 attribute node: 元素节点的属性。

关系：
element node:
  /         \
text node(child)   attribute node(not child)

---
CSS继承
CSS也把文档视为节点树，元素继承父节点样式属性。

Selector:
.表示class
#表示id

---
获取节点
getElementById
getElementsByTagName
getElementsByClassName

querySelector
querySelectorAll

childNodes 返回数组
nodeType 返回数字，body.nodeType == 1.
nodeType 一共12个值。
元素节点：1
属性节点：2
文本节点：3

node.childNodes[0] == node.firstNode;
node.childNodes[node.childNodes.length - 1] == node.lastNode

nodeValue:
text node is just text.
element node is null?

childElementCount
firstElementChild
lastElementChild


let a = document.createElement('li');
let b = document.createTextNode('xxx');
a.appendChild(b);

removeChild()
insertBefore()
*/


//global variable. 
//onclick = "xxx; return false;" 可以起到不跳转作用


xxx = 60;

function s(num) {
	total = num * num;
	return total;
}

var total = 50;
var number = s(230);
console.log(total);
console.log(xxx);


/*
innerHTML 一个节点内的所有内容。
createElement
appendChild

//===== 动画 =====
element.style.position
element.style.top
element.style.left
element.style.bottom
element.style.right

position有四个属性 static(默认) fixed relative absolute.
如果是absolute 位置有 上下左右 决定，并且parent要是document，fixed或者absolute.

*/


/*
事件处理
a.onclick = function () {};
a.addEventListener('click', function(){}, false/true);

事件传播
false: 由内向外（冒泡）。
true: 由外向内（捕获）。

event.stopPropagation(); 停止事件传播。
*/



//yarn?????


