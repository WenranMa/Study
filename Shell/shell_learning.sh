cat主要有三大功能：
1.一次显示整个文件。$ cat filename
2.从键盘创建一个文件。$ cat > filename  
   只能创建新文件,不能编辑已有文件.
3.将几个文件合并为一个文件： $cat file1 file2 > file
参数：
-n 或 --number 由 1 开始对所有输出的行数编号
-b 或 --number-nonblank 和 -n 相似，只不过对于空白行不编号
-s 或 --squeeze-blank 当遇到有连续两行以上的空白行，就代换为一行的空白行
-v 或 --show-nonprinting
例：
把 textfile1 的档案内容加上行号后输入 textfile2 这个档案里
cat -n textfile1 > textfile2

把 textfile1 和 textfile2 的档案内容加上行号（空白行不加）之后将内容附加到 textfile3 里。
cat -b textfile1 textfile2 >> textfile3

cat /dev/null > /etc/test.txt  把test.txt文件扔进垃圾箱



管道符号，是unix一个很强大的功能,符号为一条竖线:"|"。
用法: command 1 | command 2 他的功能是把第一个命令command 1执行的结果作为command 2的输入传给command 2，例如:

$ls -s|sort -nr (请注意不要复制$符号进去哦)

-s 是file size，-n是numeric-sort，-r是reverse，反转
该命令列出当前目录中的文档(含size)，并把输出送给sort命令作为输入，sort命令按数字递减的顺序把ls的输出排序。

$ls -s|sort -n

按从小到大的顺序输出。
当然还可进行多次操作，如下面的功能为先去除纯数字，再由sed 将竖线(这里不是管道符号)替换为空格，再将结果取出来排序，再进行结果的选择显示，不明白可查看 排序和分页 。

cat filename |grep -v '^[0-9]*$' | sed 's/|/ /g' |sort -nrk 8 -nrk 9 |tail -n +1 |head -n 10

Linux术语-管道符号
英文原义：Piping Symbol

中文释义：键盘字符|（典型101键键盘的Enter键上面反斜杠的上档字符）

注解：经常用来将某个命令或程序的输出提供给另一个命令或程序。例如，history | grep mcopy

（用history命令）将.bash_history文件的内容发送到grep程序，以搜索字符串“mcopy”。