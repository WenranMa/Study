# Linux

### Linux 介绍

Linux有内核版本和发行版本。
内核版本：www.kernel.org
发行版本：redhat, centOS, Ubuntu..

CentOS与Redhat完全一样，但CentOS完全免费。

- Linux应用
    - 企业服务器
    - 嵌入式

- Linux vs Windows
    - Linux严格区分大小写。  
    - Linux所有内容以文件形式保存，包括硬件。一切内容皆文件。  
    - Linux不靠扩展名区分文件类型。是靠权限区分的。压缩包：.gz, .bz2, .tar.bz2, .tgz，二进制软件包：.rpm，网页：.html, .php，脚本：.sh，配置文件：.conf，以上扩展名都是约定俗成，都不是必须的。

### Linux命令
##### 基本格式
用户@主机名： [root@localhost ~]#  
~表示初始登录位置(home目录)，/root或者/home/user1/  
`#`表示当前用户是super user
`$`表示当前用户是普通用户

格式：  
命令 [选项] [参数]
 
多个选项时，可以写在一起，选项有简化选项和完整选项，`-a`等于`--all`。
`ls -a`, `ls -l`, `ls -ld`显示目录属性详情, `ls -i`显示id号。 `ls -l` = `ll` 
`ls`也可以加文件或目录做参数 `ll /tmp/`

`-rw-r--r--. 1 root root 1207 Jan 14 xxx`  一共十位，后面每三位为一组
-文件类型（-文件 d目录 l软连接文件）   
rw- 所有者 u  
r-- 所属组 g   
r-- 其他人 o  
r读，w写，x可执行  
数字1是引用计数  
后面root, root匹配所有者，所属组。  
1207是文件大小，单位字节。  
最后修改时间。    
文件名。  

/dev/保存硬件设备文件

##### 文件处理命令
`mkdir [-p] [目录名]` -p表示递归创建:
例：`mkdir a`, `mkdir -p b/c`

`cd [目录]`:
`cd ~`或者`cd` 都是回到home。
`cd -` 回到上次的目录

相对路径：参照当前目录。绝对路径：从根目录开始。

`pwd` pirnt working directory

`rmdir [目录名]` 删除空目录。基本不会用到。

`rm [-rf] [文件或目录]`  
`-r` 删除目录，`-f` force 强制。

`cp [选项] [文件或目录] [目标目录]`：
`-r` 复制目录，`-p` 连带文件属性（时间等）复制，`-d` 若原文件是链接文件，则复制链接属性，`-a` 相当于 `-pdr` 前三个的和。 

`mv [原文件或目录] [目标目录]` 如果原文件和目标在同一个目录下，则是改名。

`>` 重定向，将命令的结果写入。
`touch` 新建文件。    
比如 `touch cat`, `ls > cat` 将显示结果写入cat。   

##### 常用目录
- / 根目录
- /bin 命令保存目录（普通用户就可以读取的命令）(还包括/usr/bin /sbin /usr/sbin，其中sbin usr/sbin 只有root用户可用)
- /boot 启动目录
- /dev 设备文件保存目录
- /etc 配置文件
- /home 普通用户家目录
- /lib 系统库目录
- /mnt 系统挂载目录
- /media 挂载目录
- /root 超级用户家目录
- /tmp 临时目录
- /proc 直接写入内存
- /sys 直接写入内存
- /usr 系统资源保存目录 （/usr/bin /usr/sbin)
- /var 系统可变文档

##### 链接命令
`ln -s [原文件] [目标文件]`  
-s 软链接  
硬链接：原文件和目标文件有相同的i节点(id号，ls -i)，存储block块，可以看做是同一个文件，删掉一个也没问题，可以从另一个访问。不能跨分区，不能针对目录使用。（不推荐使用）  
软链接：类似windows快捷方式，软链接有自己的i节点（id号）和block块，但数据文件中只保存原文件的文件名和i节点号，没有实际数据。软链接权限都是：lrwxrwxrwx. 修改任意一个，另一个都改变，删除原文件，软链接不能使用。  
软链接要写绝对路径，否在原文件和目标文件只能在同一目录，否在报错。

##### 文件搜索
`locate 文件名` locate并不是直接搜索，而是搜索后台数据库/var/lib/mlocate（数据库名字可能不同）。所以搜索数据快，但是数据库不是实时更新。所以新建文件可能找不到。
`updatedb` 命令可以更新数据库。

`whereis 命令名` 只能搜索系统命令，-b 只看可执行文件 -m 只看帮助文档。

`which 命令名` 也用于搜索命令，可以看到别名。

`find [搜索范围] [搜索条件]`   
例如：  
`find /home/wrma/working/git/ -name install.log` 避免在过大范围进行搜索。

通配符匹配，通配符是完全匹配。  
* 任意内容, `find ./Mine/Github/ -name "*.md"` 注意加引号。  
? 匹配任意一个字符  
[] 匹配任意一个括号内的字符 `find ./Mine/Github/Go_study/ -name "*[ab]"` 显示所有a或b结尾的内容。

`find /root -iname install.log` 不区分大小写。  
`find /root -user root` 按所有者搜索，`find /root -nouser` 没有所有者的垃圾文件。  

`find /var/log/ -mtime +10` 查找10天修改的文件。  
-10：10天内，10：10天当天，+10：10天前。  
atime 文件访问时间，ctime 改变文件属性，mtime 修改文件内容。

`find /var/log/ -size 15k` 按文件大小搜索。  
-15k 小于15k, +15k 大于15k。  小写的k，大写的M。。。。

`find /var/log/ -inum 123` 按ID号（i节点）搜索。

`find /var/log/ -size +20k -a -size -50k` 搜索大于20k且小于50k的文件。  
-a表示and，与。  
-o or，或。

`find /var/log/ -size +20k -a -size -50k -exec ls -lh {} \;` 搜索大于20k且小于50k的文件并显示。  
`-exec 命令 {} \;` 表示执行下一条命令。（一定是可以处理第一条搜索结果的命令）

`grep [选项] 字符串 文件名` 在指定的文件中搜索字符串。-i 忽略大小写，-v 排除指定字符串。

`whoami` ???

`whatis` ???

##### 帮助命令
`man 命令名称` 


##### 压缩命令
常见压缩格式：.zip, .gz, .bz2, .tar.gz, .tar.bz2

zip在Linux和Windows通用:  
`zip 压缩文件名 源文件`。`zip -r 压缩文件名 源目录`。  
`unzip 压缩文件`  

`gzip 源文件` 压缩成.gz文件，源文件会消失。  
`gzip -c 源文件 > 压缩文件` 压缩成.gz文件，源文件保留。  
`gzip -r 目录` 压缩目录下的所有子文件，但不能压缩目录，不打包。
`gzip -d 压缩文件` 用于解压缩，或者`gunzip 压缩文件`，同样-r解压目录。

`bzip2 源文件` 压缩成.bz2文件，源文件不保留。
`bzip2 -k 源文件` 保存源文件。bzip2不支持压缩目录。  
`bzip -d 压缩文件` 解压缩，不保留压缩文件，`bunzip2 压缩文件` 同样解压，-k保留压缩文件。

`tar -cvf 打包文件名 源文件（目录）` tar用于打包文件，来解决gzip,bz2对目录压缩的限制。
-c: 打包， -v: 显示过程， -f: 指定打包后文件名。
`tar -xvt 打包文件名` -x: 解打包。  
然后就可以用gzip或者bzip2压缩。

tar命令支持直接打包压缩，`tar -zcvf 压缩包.tar.gz 源文件` -z: 压缩为.tar.gz格式。  
`tar -zxvf 压缩包.tar.gz` 解压缩.tar.gz格式。  
`tar -jcvf 压缩包.tar.bz2 源文件` -z: 压缩为.tar.bz2格式。  
`tar -jxvf 压缩包.tar.bz2` 解压缩.tar.bz2格式。

`tar -zcvf 压缩包.tar.bz2 源文件1 源文件2` 压缩打包多个
`tar -zxvf 压缩包.tar.bz2 -C 目标位置` -C 目标目录

`tar -ztvf 压缩包` 只显示，-t表示test。


##### 关机 重启
`shutdown [选项] 时间`  时间表示定时关机。  
-c: 取消前一个关机命令。  
-h: 关机  
-r: 重启  
`shutdown -r now` 立刻重启。

其他关机命令：`halt`, `poweroff` `init 0` 没有shutdown安全。
其他重启命令：`reboot` `init 6` reboot相对安全。

系统运行级别：0 - 6 一共七个，0关机，1单用户（类似windows安全模式），2不完全多用户，不含NFS服务，3完全多用户，4未分配，5图形界面，6重启。

`logout`退出登录


##### 挂载


##### 其他命令
`echo xxx1 >> xxx2`

`cat xxx2`






---

### Shell
shell 命令行解释器，它为用户提供一个向linux内核发送请求界面系统程序。同时是一个编程语言，解释型脚本语言，可以直接调用linux命令。

分类：两种语法家族

- Bourne Shell: 最早的shell, 文件名为sh。主要有sh, ksh, Bash(linux标准shell), psh, zsh.
- C Shell: 与C语言类似。有csh, tcsh. 

`echo $SHELL` 查看当前shell. `/etc/shells`保存了系统支持的shell.

系统登录后进入默认shell. 但可以调用子shell。例如zsh中可以启动sh, exit退出。

`echo [选项] [输出内容]` -e 支持字符转义如：\a, \t, \n等，\x16进制输入。
`echo -e "\e[1;31mwhat is this?\e[0m"` 显示颜色: 30m=黑色，31m=红色，32m=绿色，33m=黄色，34m=蓝色，35m=洋红，36m=青色，37m=白色。

`#` 在shell脚本中表示注释。`#!/bin/zsh`第一句话不是注释。
```shell
#!/bin/zsh
#this is my first shell script.
echo -e "\e[1;36mHello World\e[0m"
```
`chmod 755 fisrt.sh` 更改执行权限，可以直接通过./first.sh调用。

##### 查看与设定别名：
`alias`命令，可以查看已有别名。
alias 别名='原命令'来设定命令别名。`alias ls='ls --color=never'`

命令行使用alias只能临时生效，如果永久生效要写入环境变量，如./zshrc文件，然后通过source .zshrc使其生效。

删除别名：unalias

重名命令生效顺序：绝对路径或相对路径>别名>Bash内部命令>$PATH定义路径中查找的第一个命令。

##### 常用快捷键
ctrl + c 终止当前命令
ctrl + l 清屏
ctrl + a 光标移动到命令行首
ctrl + e 光标移动到命令行尾
ctrl + u 从光标的位置删除到行首
ctrl + z 命令放入后台
ctrl + r 在历史命令中搜索

##### 历史命令
`history [选项] [历史命令保存文件]`   
-c 清空历史命令  
-w 把缓存中的历史命令写入历史保存文件 ~/.bash_history

历史命令默认保存1000条。可以用上下箭头查找。`!n` 可以执行第N条命令。`!!`重复上一条命令。

##### 重定向
设备：键盘 /dev/stdin 标准输入，显示器 /dev/stdout 或者/dev/stderr 标准（错误）输出。

输出重定向：`命令>文件` 以覆盖方式输出到文件。 `命令>>文件` 以追加方式输出。文件不存在会新建文件后再输出。

`错误命令 2>文件` 把命令的错误信息输出到文件。（覆盖或追加），注意不能有空格。这条作用有限，因为事前不确定命令的正确与错误。

`命令>文件 2>&1` 覆盖方式把正确和错误输出保存到同一文件。  
`命令>>文件 2>&1` 追加。  
`命令 &>文件` 覆盖方式把正确和错误写入同一文件。  
`命令 &>>文件` 追加。  
`命令>>文件1 2>>文件2` 正确写入1，错误的写入2。

`ls &>/dev/null` 把信息扔进黑洞，类似垃圾桶不可查看。

输入重定向：  
`wc [选项] [文件名]` 统计命令。-c统计字节，-w统计单词数，-l统计行数。
命令<文件作为命令输入: 例如`wc < a.test` 统计a.test字节单词和行数。
命令<<标记，表示输入结束。

##### 管道
多命令顺序执行：

- 通过;链接，`命令1;命令2`，两个命令顺序执行，之间没有关系。不管中间命令是否报错，都会顺序执行。
- && 逻辑与，`命令1&&命令2`，命令1执行正确，才会执行命令2，命令1不正确，不执行命令2.
- || 逻辑或，`命令1||命令2`，命令1执行正确，不会执行命令2，命令1不正确，执行命令2.

`ls && echo yes || echo no`: 如果ls正确执行，打印yes，否在打印no. 

管道符号，是unix一个很强大的功能,符号为一条竖线:"|"。`命令1 | 命令2`   

命令1的正确输出作为命令2的操作对象。命令2要严格选择，一定要可以操作命令1的输出。

例如：`netstat -an | grep ESTABLISHED | wc -l` 统计服务器连接数量。 

`ls -s|sort -nr` -s 是file size，-n是numeric-sort，-r是reverse，反转
该命令列出当前目录中的文档，并把输出送给sort命令作为输入，sort命令按数字递减的顺序把ls的输出排序。

`ls -s|sort -n`按从小到大的顺序输出。

##### 通配符
可以匹配其他内容的符号：  
* 任意内容, `find ./Mine/Github/ -name "*.md"` 注意加引号。  
? 匹配任意一个字符  
[] 匹配任意一个括号内的字符 `find ./Mine/Github/Go_study/ -name "*[ab]"` 显示所有a或b结尾的内容。
[-]代表范围，比如[0-9]，表示匹配一个数字。
[^]逻辑非，如[^0-9]，表示匹配非数字。

特殊符号：  
'' 单引号，单引号中所有的特殊符号都没有意义，比如`echo '$PATH'` 显示$PATH, 而不是变量内容。

"" 双引号，单引号中所有的特殊符号都没有意义，但$ ` \除外。  

\`\` 反引号，引用系统命令，比如：a=\`ls\`, 把ls命令的结果赋给变量a

$() 作用与``一样，建议使用。

$ 调用变量

\# 表示注释

\ 转义符号

---

### 命令及工具

#### cat
cat主要有三大功能:

- 一次显示整个文件。`cat filename`
- 从键盘创建一个文件。`cat > filename`，只能创建新文件,不能编辑已有文件。
- 将几个文件合并为一个文件： `cat file1 file2 > file`

参数：

1. -n 或 --number 由 1 开始对所有输出的行数编号。
2. -b 或 --number-nonblank 和 -n 相似，只不过对于空白行不编号。
3. -s 或 --squeeze-blank 当遇到有连续两行以上的空白行，就代换为一行的空白行。

例：把 textfile1 的档案内容加上行号后输入 textfile2 这个档案里：
`cat -n textfile1 > textfile2`

把 textfile1 和 textfile2 的档案内容加上行号（空白行不加）之后将内容附加到 textfile3 里：
`cat -b textfile1 textfile2 >> textfile3`

把test.txt文件扔进垃圾箱：`cat /dev/null > /etc/test.txt`  

当然还可进行多次操作，如下面的功能为先去除纯数字，再由sed 将竖线(这里不是管道符号)替换为空格，再将结果取出来排序，再进行结果的选择显示，不明白可查看 排序和分页 。
`cat filename |grep -v '^[0-9]*$' | sed 's/|/ /g' |sort -nrk 8 -nrk 9 |tail -n +1 |head -n 10`


#### Screen

Screen可以看作是窗口管理器的命令行界面版本。它提供了统一的管理多个会话的界面和相应的功能。

常用screen参数：

- screen -S yourname -> 新建一个叫yourname的session
- screen -ls -> 列出当前所有的session
- screen -r yourname -> 回到yourname这个session
- screen -d yourname -> 远程detach某个session
- screen -d -r yourname -> 结束当前session并回到yourname这个session
- screen -help 查看帮助

当使用`screen -S xxx` 启动后，会创建第一个窗口，也就是窗口No. 0，并在其中打开一个系统默认的shell，一般都会是bash。所以你敲入命令screen之后，会立刻又返回到命令提示符，仿佛什么也没有发生似的，其实你已经进入Screen的世界了。当然，也可以在screen命令之后加入你喜欢的参数，使之直接打开你指定的程序，例如：`screen vi david.txt`
screen创建一个执行vi david.txt的单窗口会话，退出vi 将退出该窗口/会话。

在每个screen session下，所有命令都以 ctrl+a(C-a) 开始。
```
常用：
C-a c -> 创建一个新的运行shell的窗口并切换到该窗口
C-a n -> Next，切换到下一个 window 
C-a p -> Previous，切换到前一个 window 
C-a d -> detach，暂时离开当前session，将目前的screen session(可能含有多个 windows) 丢到后台执行，并会回到还没进screen时的状态，此时在screen session里，每个window内运行的 process (无论是前台/后台)都在继续执行，即使logout也不影响。 

其他：
C-a ? -> 显示所有键绑定信息
C-a 0..9 -> 切换到第 0..9 个 window
Ctrl+a [Space] -> 由视窗0循序切换到视窗9
C-a C-a -> 在两个最近使用的 window 间切换 
C-a x -> 锁住当前的 window，需用用户密码解锁
C-a z -> 把当前session放到后台执行，用 shell 的 fg 命令则可回去。
C-a w -> 显示所有窗口列表
C-a t -> Time，显示当前时间，和系统的 load 
C-a k -> kill window，强行关闭当前的 window
C-a [ -> 进入 copy mode，在 copy mode 下可以回滚、搜索、复制就像用使用 vi 一样
    C-b Backward，PageUp 
    C-f Forward，PageDown 
    H(大写) High，将光标移至左上角 
    L Low，将光标移至左下角 
    0 移到行首 
    $ 行末 
    w forward one word，以字为单位往前移 
    b backward one word，以字为单位往后移 
    Space 第一次按为标记区起点，第二次按为终点 
    Esc 结束 copy mode 
C-a ] -> Paste，把刚刚在 copy mode 选定的内容贴上
```

5.3 查看窗口和窗口名称

打开多个窗口后，可以使用快捷键C-a w列出当前所有窗口。如果使用文本终端，这个列表会列在屏幕左下角，如果使用X环境下的终端模拟器，这个列表会列在标题栏里。窗口列表的样子一般是这样：

0$ bash  1-$ bash  2*$ bash  
这个例子中我开启了三个窗口，其中*号表示当前位于窗口2，-号表示上一次切换窗口时位于窗口1。

Screen默认会为窗口命名为编号和窗口中运行程序名的组合，上面的例子中窗口都是默认名字。练习了上面查看窗口的方法，你可能就希望各个窗口可以有不同的名字以方便区分了。可以使用快捷键C-a A来为当前窗口重命名，按下快捷键后，Screen会允许你为当前窗口输入新的名字，回车确认。

5.4 会话分离与恢复

你可以不中断screen窗口中程序的运行而暂时断开（detach）screen会话，并在随后时间重新连接（attach）该会话，重新控制各窗口中运行的程序。例如，我们打开一个screen窗口编辑/tmp/david.txt文件：

[root@TS-DEV ~]# screen vi /tmp/david.txt
之后我们想暂时退出做点别的事情，比如出去散散步，那么在screen窗口键入C-a d，Screen会给出detached提示：

暂时中断会话


半个小时之后回来了，找到该screen会话：

[root@TS-DEV ~]# screen -ls


重新连接会话：

[root@TS-DEV ~]# screen -r 12865
一切都在。

当然，如果你在另一台机器上没有分离一个Screen会话，就无从恢复会话了。

这时可以使用下面命令强制将这个会话从它所在的终端分离，转移到新的终端上来：


5.5 清除dead 会话

如果由于某种原因其中一个会话死掉了（例如人为杀掉该会话），这时screen -list会显示该会话为dead状态。使用screen -wipe命令清除该会话：


5.6 关闭或杀死窗口

正常情况下，当你退出一个窗口中最后一个程序（通常是bash）后，这个窗口就关闭了。另一个关闭窗口的方法是使用C-a k，这个快捷键杀死当前的窗口，同时也将杀死这个窗口中正在运行的进程。

如果一个Screen会话中最后一个窗口被关闭了，那么整个Screen会话也就退出了，screen进程会被终止。

除了依次退出/杀死当前Screen会话中所有窗口这种方法之外，还可以使用快捷键C-a :，然后输入quit命令退出Screen会话。需要注意的是，这样退出会杀死所有窗口并退出其中运行的所有程序。其实C-a :这个快捷键允许用户直接输入的命令有很多，包括分屏可以输入split等，这也是实现Screen功能的一个途径，不过个人认为还是快捷键比较方便些。



如何杀死一个已经detached的screen会话？

如果想杀死一个已经detached的screen会话，可以使用以下命令：

screen -X -S [session # you want to kill] quit

举例如下：

[root@localhost ~]# screen -ls
There are screens on:
        9975.pts-0.localhost    (Detached)
        4588.pts-3.localhost    (Detached)
2 Sockets in /var/run/screen/S-root.

[root@localhost ~]# screen -X -S 4588 quit
[root@localhost ~]# screen -ls
There is a screen on:
        9975.pts-0.localhost    (Detached)
1 Socket in /var/run/screen/S-root.
可以看到，4588会话已经没有了。


#### curl
在Linux中curl是一个利用URL规则在命令行下工作的文件传输工具，可以说是一款很强大的http命令行工具。它支持文件的上传和下载，是综合传输工具，但按传统，习惯称url为下载工具。

语法：# curl [option] [url]
常见参数：

复制代码
-A/--user-agent <string>              设置用户代理发送给服务器
-b/--cookie <name=string/file>    cookie字符串或文件读取位置
-c/--cookie-jar <file>                    操作结束后把cookie写入到这个文件中
-C/--continue-at <offset>            断点续转
-D/--dump-header <file>              把header信息写入到该文件中
-e/--referer                                  来源网址
-f/--fail                                          连接失败时不显示http错误
-o/--output                                  把输出写到该文件中
-O/--remote-name                      把输出写到该文件中，保留远程文件的文件名
-r/--range <range>                      检索来自HTTP/1.1或FTP服务器字节范围
-s/--silent                                    静音模式。不输出任何东西
-T/--upload-file <file>                  上传文件
-u/--user <user[:password]>      设置服务器的用户和密码
-w/--write-out [format]                什么输出完成后
-x/--proxy <host[:port]>              在给定的端口上使用HTTP代理
-#/--progress-bar                        进度条显示当前的传送状态
复制代码
例子：
1、基本用法
`curl http://www.linux.com`

执行后，www.linux.com 的html就会显示在屏幕上了。Ps：由于安装linux的时候很多时候是没有安装桌面的，也意味着没有浏览器，因此这个方法也经常用于测试一台服务器是否可以到达一个网站。

2、保存访问的网页
2.1:使用linux的重定向功能保存

# curl http://www.linux.com >> linux.html
2.2:可以使用curl的内置option:-o(小写)保存网页

$ curl -o linux.html http://www.linux.com
执行完成后会显示如下界面，显示100%则表示保存成功

% Total    % Received % Xferd  Average Speed  Time    Time    Time  Current
                                Dload  Upload  Total  Spent    Left  Speed
100 79684    0 79684    0    0  3437k      0 --:--:-- --:--:-- --:--:-- 7781k
2.3:可以使用curl的内置option:-O(大写)保存网页中的文件
要注意这里后面的url要具体到某个文件，不然抓不下来

# curl -O http://www.linux.com/hello.sh
3、测试网页返回值

# curl -o /dev/null -s -w %{http_code} www.linux.com
Ps:在脚本中，这是很常见的测试网站是否正常的用法

4、指定proxy服务器以及其端口
很多时候上网需要用到代理服务器(比如是使用代理服务器上网或者因为使用curl别人网站而被别人屏蔽IP地址的时候)，幸运的是curl通过使用内置option：-x来支持设置代理

# curl -x 192.168.100.100:1080 http://www.linux.com
5、cookie
有些网站是使用cookie来记录session信息。对于chrome这样的浏览器，可以轻易处理cookie信息，但在curl中只要增加相关参数也是可以很容易的处理cookie
5.1:保存http的response里面的cookie信息。内置option:-c（小写）

# curl -c cookiec.txt  http://www.linux.com
执行后cookie信息就被存到了cookiec.txt里面了

5.2:保存http的response里面的header信息。内置option: -D

# curl -D cookied.txt http://www.linux.com
执行后cookie信息就被存到了cookied.txt里面了

注意：-c(小写)产生的cookie和-D里面的cookie是不一样的。


5.3:使用cookie
很多网站都是通过监视你的cookie信息来判断你是否按规矩访问他们的网站的，因此我们需要使用保存的cookie信息。内置option: -b

# curl -b cookiec.txt http://www.linux.com
6、模仿浏览器
有些网站需要使用特定的浏览器去访问他们，有些还需要使用某些特定的版本。curl内置option:-A可以让我们指定浏览器去访问网站

# curl -A "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.0)" http://www.linux.com
这样服务器端就会认为是使用IE8.0去访问的

7、伪造referer（盗链）
很多服务器会检查http访问的referer从而来控制访问。比如：你是先访问首页，然后再访问首页中的邮箱页面，这里访问邮箱的referer地址就是访问首页成功后的页面地址，如果服务器发现对邮箱页面访问的referer地址不是首页的地址，就断定那是个盗连了
curl中内置option：-e可以让我们设定referer

# curl -e "www.linux.com" http://mail.linux.com
这样就会让服务器其以为你是从www.linux.com点击某个链接过来的

8、下载文件
8.1：利用curl下载文件。
#使用内置option：-o(小写)

# curl -o dodo1.jpg http:www.linux.com/dodo1.JPG
#使用内置option：-O（大写)

# curl -O http://www.linux.com/dodo1.JPG
这样就会以服务器上的名称保存文件到本地

8.2：循环下载
有时候下载图片可以能是前面的部分名称是一样的，就最后的尾椎名不一样

# curl -O http://www.linux.com/dodo[1-5].JPG
这样就会把dodo1，dodo2，dodo3，dodo4，dodo5全部保存下来

8.3：下载重命名

# curl -O http://www.linux.com/{hello,bb}/dodo[1-5].JPG
由于下载的hello与bb中的文件名都是dodo1，dodo2，dodo3，dodo4，dodo5。因此第二次下载的会把第一次下载的覆盖，这样就需要对文件进行重命名。

# curl -o #1_#2.JPG http://www.linux.com/{hello,bb}/dodo[1-5].JPG
这样在hello/dodo1.JPG的文件下载下来就会变成hello_dodo1.JPG,其他文件依此类推，从而有效的避免了文件被覆盖

8.4：分块下载
有时候下载的东西会比较大，这个时候我们可以分段下载。使用内置option：-r

# curl -r 0-100 -o dodo1_part1.JPG http://www.linux.com/dodo1.JPG
# curl -r 100-200 -o dodo1_part2.JPG http://www.linux.com/dodo1.JPG
# curl -r 200- -o dodo1_part3.JPG http://www.linux.com/dodo1.JPG
# cat dodo1_part* > dodo1.JPG
这样就可以查看dodo1.JPG的内容了

8.5：通过ftp下载文件
curl可以通过ftp下载文件，curl提供两种从ftp中下载的语法

# curl -O -u 用户名:密码 ftp://www.linux.com/dodo1.JPG
# curl -O ftp://用户名:密码@www.linux.com/dodo1.JPG
8.6：显示下载进度条

# curl -# -O http://www.linux.com/dodo1.JPG
8.7：不会显示下载进度信息

# curl -s -O http://www.linux.com/dodo1.JPG
9、断点续传
在windows中，我们可以使用迅雷这样的软件进行断点续传。curl可以通过内置option:-C同样可以达到相同的效果
如果在下载dodo1.JPG的过程中突然掉线了，可以使用以下的方式续传

# curl -C -O http://www.linux.com/dodo1.JPG
10、上传文件
curl不仅仅可以下载文件，还可以上传文件。通过内置option:-T来实现

# curl -T dodo1.JPG -u 用户名:密码 ftp://www.linux.com/img/
这样就向ftp服务器上传了文件dodo1.JPG

11、显示抓取错误

# curl -f http://www.linux.com/error
其他参数(此处翻译为转载)：

复制代码
-a/--append                        上传文件时，附加到目标文件
--anyauth                            可以使用“任何”身份验证方法
--basic                                使用HTTP基本验证
-B/--use-ascii                      使用ASCII文本传输
-d/--data <data>                  HTTP POST方式传送数据
--data-ascii <data>            以ascii的方式post数据
--data-binary <data>          以二进制的方式post数据
--negotiate                          使用HTTP身份验证
--digest                        使用数字身份验证
--disable-eprt                  禁止使用EPRT或LPRT
--disable-epsv                  禁止使用EPSV
--egd-file <file>              为随机数据(SSL)设置EGD socket路径
--tcp-nodelay                  使用TCP_NODELAY选项
-E/--cert <cert[:passwd]>      客户端证书文件和密码 (SSL)
--cert-type <type>              证书文件类型 (DER/PEM/ENG) (SSL)
--key <key>                    私钥文件名 (SSL)
--key-type <type>              私钥文件类型 (DER/PEM/ENG) (SSL)
--pass  <pass>                  私钥密码 (SSL)
--engine <eng>                  加密引擎使用 (SSL). "--engine list" for list
--cacert <file>                CA证书 (SSL)
--capath <directory>            CA目   (made using c_rehash) to verify peer against (SSL)
--ciphers <list>                SSL密码
--compressed                    要求返回是压缩的形势 (using deflate or gzip)
--connect-timeout <seconds>    设置最大请求时间
--create-dirs                  建立本地目录的目录层次结构
--crlf                          上传是把LF转变成CRLF
--ftp-create-dirs              如果远程目录不存在，创建远程目录
--ftp-method [multicwd/nocwd/singlecwd]    控制CWD的使用
--ftp-pasv                      使用 PASV/EPSV 代替端口
--ftp-skip-pasv-ip              使用PASV的时候,忽略该IP地址
--ftp-ssl                      尝试用 SSL/TLS 来进行ftp数据传输
--ftp-ssl-reqd                  要求用 SSL/TLS 来进行ftp数据传输
-F/--form <name=content>        模拟http表单提交数据
-form-string <name=string>      模拟http表单提交数据
-g/--globoff                    禁用网址序列和范围使用{}和[]
-G/--get                        以get的方式来发送数据
-h/--help                      帮助
-H/--header <line>              自定义头信息传递给服务器
--ignore-content-length        忽略的HTTP头信息的长度
-i/--include                    输出时包括protocol头信息
-I/--head                      只显示文档信息
-j/--junk-session-cookies      读取文件时忽略session cookie
--interface <interface>        使用指定网络接口/地址
--krb4 <level>                  使用指定安全级别的krb4
-k/--insecure                  允许不使用证书到SSL站点
-K/--config                    指定的配置文件读取
-l/--list-only                  列出ftp目录下的文件名称
--limit-rate <rate>            设置传输速度
--local-port<NUM>              强制使用本地端口号
-m/--max-time <seconds>        设置最大传输时间
--max-redirs <num>              设置最大读取的目录数
--max-filesize <bytes>          设置最大下载的文件总量
-M/--manual                    显示全手动
-n/--netrc                      从netrc文件中读取用户名和密码
--netrc-optional                使用 .netrc 或者 URL来覆盖-n
--ntlm                          使用 HTTP NTLM 身份验证
-N/--no-buffer                  禁用缓冲输出
-p/--proxytunnel                使用HTTP代理
--proxy-anyauth                选择任一代理身份验证方法
--proxy-basic                  在代理上使用基本身份验证
--proxy-digest                  在代理上使用数字身份验证
--proxy-ntlm                    在代理上使用ntlm身份验证
-P/--ftp-port <address>        使用端口地址，而不是使用PASV
-Q/--quote <cmd>                文件传输前，发送命令到服务器
--range-file                    读取（SSL）的随机文件
-R/--remote-time                在本地生成文件时，保留远程文件时间
--retry <num>                  传输出现问题时，重试的次数
--retry-delay <seconds>        传输出现问题时，设置重试间隔时间
--retry-max-time <seconds>      传输出现问题时，设置最大重试时间
-S/--show-error                显示错误
--socks4 <host[:port]>          用socks4代理给定主机和端口
--socks5 <host[:port]>          用socks5代理给定主机和端口
-t/--telnet-option <OPT=val>    Telnet选项设置
--trace <file>                  对指定文件进行debug
--trace-ascii <file>            Like --跟踪但没有hex输出
--trace-time                    跟踪/详细输出时，添加时间戳
--url <URL>                    Spet URL to work with
-U/--proxy-user <user[:password]>  设置代理用户名和密码
-V/--version                    显示版本信息
-X/--request <command>          指定什么命令
-y/--speed-time                放弃限速所要的时间。默认为30
-Y/--speed-limit                停止传输速度的限制，速度时间'秒
-z/--time-cond                  传送时间设置
-0/--http1.0                    使用HTTP 1.0
-1/--tlsv1                      使用TLSv1（SSL）
-2/--sslv2                      使用SSLv2的（SSL）
-3/--sslv3                      使用的SSLv3（SSL）
--3p-quote                      like -Q for the source URL for 3rd party transfer
--3p-url                        使用url，进行第三方传送
--3p-user                      使用用户名和密码，进行第三方传送
-4/--ipv4                      使用IP4
-6/--ipv6                      使用IP6



----

### Tmux

快捷键
一般情况下 tmux 中所有的快捷键都需要和前缀快捷键 ⌃b 来组合使用（注：⌃ 为 Mac 的 control 键），以下是常用的窗格（pane）快捷键列表，大家可以依次尝试下：

窗格操作
% 左右平分出两个窗格

" 上下平分出两个窗格

x 关闭当前窗格

{ 当前窗格前移

} 当前窗格后移

; 选择上次使用的窗格

o 选择下一个窗格，也可以使用上下左右方向键来选择

space 切换窗格布局，tmux 内置了五种窗格布局，也可以通过 ⌥1 至 ⌥5来切换

z 最大化当前窗格，再次执行可恢复原来大小

q 显示所有窗格的序号，在序号出现期间按下对应的数字，即可跳转至对应的窗格

窗口操作
tmux 除了窗格以外，还有窗口（window） 的概念。依次使用以下快捷键来熟悉 tmux 的窗口操作：

c 新建窗口，此时当前窗口会切换至新窗口，不影响原有窗口的状态

p 切换至上一窗口

n 切换至下一窗口

w 窗口列表选择，注意 macOS 下使用 ⌃p 和 ⌃n 进行上下选择

& 关闭当前窗口

, 重命名窗口，可以使用中文，重命名后能在 tmux 状态栏更快速的识别窗口 id

0 切换至 0 号窗口，使用其他数字 id 切换至对应窗口

f 根据窗口名搜索选择窗口，可模糊匹配

 

会话操作
如果运行了多次 tmux 命令则会开启多个 tmux 会话（session）。在 tmux 会话中，使用前缀快捷键 ⌃b 配合以下快捷键可操作会话：

$ 重命名当前会话

s 选择会话列表

d detach 当前会话，运行后将会退出 tmux 进程，返回至 shell 主进程

在 shell 主进程下运行以下命令可以操作 tmux 会话：

 
tmux new -s foo # 新建名称为 foo 的会话
tmux ls # 列出所有 tmux 会话
tmux a # 恢复至上一次的会话
tmux a -t foo # 恢复名称为 foo 的会话，会话默认名称为数字
tmux kill-session -t foo # 删除名称为 foo 的会话
tmux kill-server # 删除所有的会话
 
 
除以上提到的快捷键以外，tmux 还有许多其他的快捷键和命令，使用前缀快捷键 ⌃b 加 ? 可以查看所有的快捷键列表，该列表视图为 tmux copy 模式，该模式下可使用以下快捷键（无需加 ⌃b 前缀）：

⌃v 下一页

Meta v 上一页 （tmux 快捷键为 Emacs 风格，这里的 Meta 键可用 Esc 模拟）

⌃s 向前搜索

q 退出 copy 模式

常见配置与问题
1、鼠标滚屏
tmux 默认配置中最糟糕的体验就是滚屏查看和文本复制（大家可以先试试看）。你需要先使用 ⌃b [ 快捷键进入 copy 模式，然后使用翻页、字符定位来选择需要的字符，效率远没有鼠标选择来的快。

因此 tmux 提供了一些个性化配置项来优化这些配置，首先在 shell 中运行 touch ~/.tmux.conf 新建用户配置文件。在文件中增加以下内容：

 
# 开启鼠标模式
set -g mode-mouse on
​
# 允许鼠标选择窗格
set -g mouse-select-pane on
​
# 如果喜欢给窗口自定义命名，那么需要关闭窗口的自动命名
set-option -g allow-rename off
​
# 如果对 vim 比较熟悉，可以将 copy mode 的快捷键换成 vi 模式
set-window-option -g mode-keys vi
 

  
配置文件修改完成后，可以 tmux kill-server 重启所有 tmux 进程，或者在 tmux 会话中使用 ⌃b : 进入控制台模式，输入 source-file ~/.tmux.conf 命令重新加载配置。

 

2、鼠标复制
tmux 下开启鼠标滚屏后，复制文本有两种方式：

方法 1：使用 ⌃b z 进入窗格全屏模式，鼠标选择文本的同时按住 option 键 ⌥，然后使用 ⌘c 进行复制；

方法 2：开启 iTerm2 「在选择时复制」选项，即可实现自动选择复制。如下图：

 

3、tips
screen 是另外一款终端复用命令行，但他没有 tmux 好看好用；

tmux 有个 bug ，导致从它启动的 vscode 的复制粘贴快捷键会失效；

iTerm2 可以通过 「Preferences -> Profiles -> Keyboard Behavior -> Left option key acts as +Esc」将键盘的左侧 option 键映射为 Meta 键




---


vim是vi的增强版本。


---


`time curl -v http://influxdb.pqm.dev.aws.fwmrm.net/ping`