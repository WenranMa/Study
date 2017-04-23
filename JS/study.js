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


