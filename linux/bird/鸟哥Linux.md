# 鸟哥Linux

### 数据流重导向
standard output 与 standard error output

标准输出指的是“指令执行所回传的正确的讯息”，而标准错误输出为“ 指令执行失败后，所回传的错误讯息”。不管正确或错误的数据都是默认输出到屏幕上。

数据流重导向可以将 standard output （简称 stdout）与 standard error output （简称 stderr）分别传送到其他的文件或设备去：

- 标准输入　　（stdin） ：代码为 0 ，使用 < 或 << ；
- 标准输出　　（stdout）：代码为 1 ，使用 > 或 >> ；
- 标准错误输出（stderr）：代码为 2 ，使用 2> 或 2>> ；

为了理解 stdout 与 stderr ，我们先来进行一个范例的练习：

范例一：观察你的系统根目录 （/） 下各目录的文件名、权限与属性，并记录下来
[wrma@study ~]$ ll /  &lt;==此时屏幕会显示出文件名信息

[wrma@study ~]$ ll / &gt; ~/rootfile &lt;==屏幕并无任何信息
[wrma@study ~]$ ll  ~/rootfile &lt;==有个新文件被创建了！
-rw-rw-r--. 1 wrma wrma 1078 Jul  9 18:51 /home/wrma/rootfile
怪了！屏幕怎么会完全没有数据呢？这是因为原本“ ll / ”所显示的数据已经被重新导向到 ~/rootfile 文件中了！ 那个 ~/rootfile 的文件名可以随便你取。如果你下达“ cat ~/rootfile ”那就可以看到原本应该在屏幕上面的数据啰。 如果我再次下达：“ ll /home > ~/rootfile ”后，那个 ~/rootfile 文件的内容变成什么？ 他将变成“仅有 ll /home 的数据”而已！咦！原本的“ ll / ”数据就不见了吗？是的！因为该文件的创建方式是：

该文件 （本例中是 ~/rootfile） 若不存在，系统会自动的将他创建起来，但是
当这个文件存在的时候，那么系统就会先将这个文件内容清空，然后再将数据写入！
也就是若以 > 输出到一个已存在的文件中，那个文件就会被覆盖掉啰！
那如果我想要将数据累加而不想要将旧的数据删除，那该如何是好？利用两个大于的符号 （>>） 就好啦！以上面的范例来说，你应该要改成“ ll / >> ~/rootfile ”即可。 如此一来，当 （1） ~/rootfile 不存在时系统会主动创建这个文件；（2）若该文件已存在， 则数据会在该文件的最下方累加进去！



上面谈到的是 standard output 的正确数据，那如果是 standard error output 的错误数据呢？那就通过 2> 及 2>> 啰！同样是覆盖 （2>） 与累加 （2>>） 的特性！我们在刚刚才谈到 stdout 代码是 1 而 stderr 代码是 2 ， 所以这个 2> 是很容易理解的，而如果仅存在 > 时，则代表默认的代码 1 啰！也就是说：

1> ：以覆盖的方法将“正确的数据”输出到指定的文件或设备上；
1>>：以累加的方法将“正确的数据”输出到指定的文件或设备上；
2> ：以覆盖的方法将“错误的数据”输出到指定的文件或设备上；
2>>：以累加的方法将“错误的数据”输出到指定的文件或设备上；

要注意喔，“ 1>> ”以及“ 2>> ”中间是没有空格的！OK！有些概念之后让我们继续聊一聊这家伙怎么应用吧！ 当你以一般身份执行 find 这个指令的时候，由于权限的问题可能会产生一些错误信息。例如执行“ find / -name testing ”时，可能会产生类似“ find: /root: Permission denied ”之类的讯息。 例如下面这个范例：

范例二：利用一般身份帐号搜寻 /home 下面是否有名为 .bashrc 的文件存在
[wrma@study ~]$ find /home -name .bashrc &lt;==身份是 wrma 喔！
find: '/home/arod': Permission denied    &lt;== Standard error output
find: '/home/alex': Permission denied    &lt;== Standard error output
/home/wrma/.bashrc                     &lt;== Standard output
由于 /home 下面还有我们之前创建的帐号存在，那些帐号的主文件夹你当然不能进入啊！所以就会有错误及正确数据了。 好了，那么假如我想要将数据输出到 list 这个文件中呢？执行“ find /home -name .bashrc > list ” 会有什么结果？呵呵，你会发现 list 里面存了刚刚那个“正确”的输出数据， 至于屏幕上还是会有错误的讯息出现呢！伤脑筋！如果想要将正确的与错误的数据分别存入不同的文件中需要怎么做？

范例三：承范例二，将 stdout 与 stderr 分存到不同的文件去
[wrma@study ~]$ find /home -name .bashrc &gt; list_right 2&gt; list_error
注意喔，此时“屏幕上不会出现任何讯息”！因为刚刚执行的结果中，有 Permission 的那几行错误信息都会跑到 list_error 这个文件中，至于正确的输出数据则会存到 list_right 这个文件中啰！这样可以了解了吗？ 如果有点混乱的话，去休息一下再回来看看吧！

/dev/null 垃圾桶黑洞设备与特殊写法
想像一下，如果我知道错误讯息会发生，所以要将错误讯息忽略掉而不显示或储存呢？ 这个时候黑洞设备 /dev/null 就很重要了！这个 /dev/null 可以吃掉任何导向这个设备的信息喔！将上述的范例修订一下：

范例四：承范例三，将错误的数据丢弃，屏幕上显示正确的数据
[wrma@study ~]$ find /home -name .bashrc 2&gt; /dev/null
/home/wrma/.bashrc  &lt;==只有 stdout 会显示到屏幕上， stderr 被丢弃了
再想像一下，如果我要将正确与错误数据通通写入同一个文件去呢？这个时候就得要使用特殊的写法了！ 我们同样用下面的案例来说明：

范例五：将指令的数据全部写入名为 list 的文件中
[wrma@study ~]$ find /home -name .bashrc &gt; list 2&gt; list  &lt;==错误
[wrma@study ~]$ find /home -name .bashrc &gt; list 2&gt;&1     &lt;==正确
[wrma@study ~]$ find /home -name .bashrc &&gt; list         &lt;==正确
上述表格第一行错误的原因是，由于两股数据同时写入一个文件，又没有使用特殊的语法， 此时两股数据可能会交叉写入该文件内，造成次序的错乱。所以虽然最终 list 文件还是会产生，但是里面的数据排列就会怪怪的，而不是原本屏幕上的输出排序。 至于写入同一个文件的特殊语法如上表所示，你可以使用 2>&1 也可以使用 &> ！ 一般来说，鸟哥比较习惯使用 2>&1 的语法啦！



standard input ： < 与 <<
了解了 stderr 与 stdout 后，那么那个 < 又是什么呀？呵呵！以最简单的说法来说， 那就是“将原本需要由键盘输入的数据，改由文件内容来取代”的意思。 我们先由下面的 cat 指令操作来了解一下什么叫做“键盘输入”吧！

范例六：利用 cat 指令来创建一个文件的简单流程
[wrma@study ~]$ cat &gt; catfile
testing
cat file test
&lt;==这里按下 [ctrl]+d 来离开

[wrma@study ~]$ cat catfile
testing
cat file test
由于加入 > 在 cat 后，所以那个 catfile 会被主动的创建，而内容就是刚刚键盘上面输入的那两行数据了。 唔！那我能不能用纯文本文件取代键盘的输入，也就是说，用某个文件的内容来取代键盘的敲击呢？ 可以的！如下所示：

范例七：用 stdin 取代键盘的输入以创建新文件的简单流程
[wrma@study ~]$ cat &gt; catfile &lt; ~/.bashrc
[wrma@study ~]$ ll catfile ~/.bashrc
-rw-r--r--. 1 wrma wrma 231 Mar  6 06:06 /home/wrma/.bashrc
-rw-rw-r--. 1 wrma wrma 231 Jul  9 18:58 catfile
# 注意看，这两个文件的大小会一模一样！几乎像是使用 cp 来复制一般！
这东西非常的有帮助！尤其是用在类似 mail 这种指令的使用上。 理解 < 之后，再来则是怪可怕一把的 << 这个连续两个小于的符号了。 他代表的是“结束的输入字符”的意思！举例来讲：“我要用 cat 直接将输入的讯息输出到 catfile 中， 且当由键盘输入 eof 时，该次输入就结束”，那我可以这样做：

[wrma@study ~]$ cat &gt; catfile &lt;&lt; "eof"
&gt; This is a test.
&gt; OK now stop
&gt; eof  &lt;==输入这关键字，立刻就结束而不需要输入 [ctrl]+d

[wrma@study ~]$ cat catfile
This is a test.
OK now stop     &lt;==只有这两行，不会存在关键字那一行！
看到了吗？利用 << 右侧的控制字符，我们可以终止一次输入， 而不必输入 [crtl]+d 来结束哩！这对程序写作很有帮助喔！好了，那么为何要使用命令输出重导向呢？我们来说一说吧！

屏幕输出的信息很重要，而且我们需要将他存下来的时候；
背景执行中的程序，不希望他干扰屏幕正常的输出结果时；
一些系统的例行命令 （例如写在 /etc/crontab 中的文件） 的执行结果，希望他可以存下来时；
一些执行命令的可能已知错误讯息时，想以“ 2> /dev/null ”将他丢掉时；
错误讯息与正确讯息需要分别输出时。
当然还有很多的功能的，最简单的就是网友们常常问到的：“为何我的 root 都会收到系统 crontab 寄来的错误讯息呢”这个咚咚是常见的错误， 而如果我们已经知道这个错误讯息是可以忽略的时候，嗯！“ 2> errorfile ”这个功能就很重要了吧！ 了解了吗？

问：假设我要将 echo "error message" 以 standard error output 的格式来输出，该如何处置？答：既然有 2>&1 来将 2> 转到 1> 去，那么应该也会有 1>&2 吧？没错！就是这个概念！因此你可以这样作：

[wrma@study ~]$ echo "error message" 1&gt;&2
[wrma@study ~]$ echo "error message" 2&gt; /dev/null 1&gt;&2
你会发现第一条有讯息输出到屏幕上，第二条则没有讯息！这表示该讯息已经是通过 2> /dev/null 丢到垃圾桶去了！ 可以肯定是错误讯息啰！ ^_^


### 命令执行的判断依据： ; , &&, ||
在某些情况下，很多指令我想要一次输入去执行，而不想要分次执行时，该如何是好？基本上你有两个选择， 一个是通过第十二章要介绍的 shell script 撰写脚本去执行，一种则是通过下面的介绍来一次输入多重指令喔！

cmd ; cmd （不考虑指令相关性的连续指令下达）
在某些时候，我们希望可以一次执行多个指令，例如在关机的时候我希望可以先执行两次 sync 同步化写入磁盘后才 shutdown 计算机，那么可以怎么作呢？这样做呀：

[root@study ~]# sync; sync; shutdown -h now
在指令与指令中间利用分号 （;） 来隔开，这样一来，分号前的指令执行完后就会立刻接着执行后面的指令了。 这真是方便啊～再来，换个角度来想，万一我想要在某个目录下面创建一个文件，也就是说，如果该目录存在的话， 那我才创建这个文件，如果不存在，那就算了。也就是说这两个指令彼此之间是有相关性的， 前一个指令是否成功的执行与后一个指令是否要执行有关！那就得动用到 && 或 || 啰！

$? （指令回传值） 与 && 或 ||
如同上面谈到的，两个指令之间有相依性，而这个相依性主要判断的地方就在于前一个指令执行的结果是否正确。 还记得本章之前我们曾介绍过指令回传值吧！嘿嘿！没错，您真聪明！就是通过这个回传值啦！ 再复习一次“若前一个指令执行的结果为正确，在 Linux 下面会回传一个 $? = 0 的值”。 那么我们怎么通过这个回传值来判断后续的指令是否要执行呢？这就得要借由“ && ”及“ || ”的帮忙了！ 注意喔，两个 & 之间是没有空格的！那个 | 则是 [Shift]+[] 的按键结果。

指令下达情况	说明
cmd1 && cmd2	1. 若 cmd1 执行完毕且正确执行（$?=0），则开始执行 cmd2。 2. 若 cmd1 执行完毕且为错误 （$?≠0），则 cmd2 不执行。
cmd1 || cmd2	1. 若 cmd1 执行完毕且正确执行（$?=0），则 cmd2 不执行。 2. 若 cmd1 执行完毕且为错误 （$?≠0），则开始执行 cmd2。
上述的 cmd1 及 cmd2 都是指令。好了，回到我们刚刚假想的情况，就是想要： （1）先判断一个目录是否存在； （2）若存在才在该目录下面创建一个文件。由于我们尚未介绍如何判断式 （test） 的使用，在这里我们使用 ls 以及回传值来判断目录是否存在啦！ 让我们进行下面这个练习看看：

范例一：使用 ls 查阅目录 /tmp/abc 是否存在，若存在则用 touch 创建 /tmp/abc/hehe
[wrma@study ~]$ ls /tmp/abc && touch /tmp/abc/hehe
ls: cannot access /tmp/abc: No such file or directory
# ls 很干脆的说明找不到该目录，但并没有 touch 的错误，表示 touch 并没有执行

[wrma@study ~]$ mkdir /tmp/abc
[wrma@study ~]$ ls /tmp/abc && touch /tmp/abc/hehe
[wrma@study ~]$ ll /tmp/abc
-rw-rw-r--. 1 wrma wrma 0 Jul  9 19:16 hehe
看到了吧？如果 /tmp/abc 不存在时，touch 就不会被执行，若 /tmp/abc 存在的话，那么 touch 就会开始执行啰！ 很不错用吧！不过，我们还得手动自行创建目录，伤脑筋～能不能自动判断，如果没有该目录就给予创建呢？ 参考一下下面的例子先：

范例二：测试 /tmp/abc 是否存在，若不存在则予以创建，若存在就不作任何事情
[wrma@study ~]$ rm -r /tmp/abc                &lt;==先删除此目录以方便测试
[wrma@study ~]$ ls /tmp/abc || mkdir /tmp/abc
ls: cannot access /tmp/abc: No such file or directory  &lt;==真的不存在喔！
[wrma@study ~]$ ll -d /tmp/abc
drwxrwxr-x. 2 wrma wrma 6 Jul  9 19:17 /tmp/abca   &lt;==结果出现了！有进行 mkdir
如果你一再重复“ ls /tmp/abc || mkdir /tmp/abc ”画面也不会出现重复 mkdir 的错误！这是因为 /tmp/abc 已经存在， 所以后续的 mkdir 就不会进行！这样理解否？好了，让我们再次的讨论一下，如果我想要创建 /tmp/abc/hehe 这个文件， 但我并不知道 /tmp/abc 是否存在，那该如何是好？试看看：

范例三：我不清楚 /tmp/abc 是否存在，但就是要创建 /tmp/abc/hehe 文件
[wrma@study ~]$ ls /tmp/abc || mkdir /tmp/abc && touch /tmp/abc/hehe
上面这个范例三总是会尝试创建 /tmp/abc/hehe 的喔！不论 /tmp/abc 是否存在。那么范例三应该如何解释呢？ 由于Linux 下面的指令都是由左往右执行的，所以范例三有几种结果我们来分析一下：

（1）若 /tmp/abc 不存在故回传 $?≠0，则 （2）因为 || 遇到非为 0 的 $? 故开始 mkdir /tmp/abc，由于 mkdir /tmp/abc 会成功进行，所以回传 $?=0 （3）因为 && 遇到 $?=0 故会执行 touch /tmp/abc/hehe，最终 hehe 就被创建了；

（1）若 /tmp/abc 存在故回传 $?=0，则 （2）因为 || 遇到 0 的 $? 不会进行，此时 $?=0 继续向后传，故 （3）因为 && 遇到 $?=0 就开始创建 /tmp/abc/hehe 了！最终 /tmp/abc/hehe 被创建起来。

整个流程图示如下：

指令依序执行的关系示意图图10.5.2、指令依序执行的关系示意图

上面这张图显示的两股数据中，上方的线段为不存在 /tmp/abc 时所进行的指令行为，下方的线段则是存在 /tmp/abc 所在的指令行为。如上所述，下方线段由于存在 /tmp/abc 所以导致 $?=0 ，让中间的 mkdir 就不执行了！ 并将 $?=0 继续往后传给后续的 touch 去利用啦！瞭乎？在任何时刻你都可以拿上面这张图作为示意！ 让我们来想想下面这个例题吧！

例题：以 ls 测试 /tmp/vbirding 是否存在，若存在则显示 "exist" ，若不存在，则显示 "not exist"！答：这又牵涉到逻辑判断的问题，如果存在就显示某个数据，若不存在就显示其他数据，那我可以这样做：

> ls /tmp/vbirding && echo "exist" || echo "not exist"

意思是说，当 ls /tmp/vbirding 执行后，若正确，就执行 echo "exist" ，若有问题，就执行 echo "not exist" ！那如果写成如下的状况会出现什么？

> ls /tmp/vbirding || echo "not exist" && echo "exist"

这其实是有问题的，为什么呢？由图 10.5.2 的流程介绍我们知道指令是一个一个往后执行， 因此在上面的例子当中，如果 /tmp/vbirding 不存在时，他会进行如下动作：

若 ls /tmp/vbirding 不存在，因此回传一个非为 0 的数值；
接下来经过 || 的判断，发现前一个指令回传非为 0 的数值，因此，程序开始执行 echo "not exist" ，而 echo "not exist" 程序肯定可以执行成功，因此会回传一个 0 值给后面的指令；
经过 && 的判断，咦！是 0 啊！所以就开始执行 echo "exist" 。
所以啊，嘿嘿！第二个例子里面竟然会同时出现 not exist 与 exist 呢！真神奇～

经过这个例题的练习，你应该会了解，由于指令是一个接着一个去执行的，因此，如果真要使用判断， 那么这个 && 与 || 的顺序就不能搞错。一般来说，假设判断式有三个，也就是：

command1 && command2 || command3

而且顺序通常不会变，因为一般来说， command2 与 command3 会放置肯定可以执行成功的指令， 因此，依据上面例题的逻辑分析，您就会晓得为何要如此放置啰～这很有用的啦！而且.....考试也很常考～


### 管线命令 （pipe）
管线命令使用的是“ | ”这个界定符号！ 管线命令与“连续下达命令”是不一样！ 

假设我们想要知道 /etc/ 下面有多少文件，那么可以利用 ls /etc 来查阅，不过， 因为 /etc 下面的文件太多，导致屏幕塞满，可以通过 less 指令的协助，利用：

```bash
$ ls -al /etc | less
```
使用 ls 指令输出后的内容，就能够被 less 读取，管线命令“ | ”仅能处理前面一个指令传来的正确信息，也就是 standard output 的信息，对于 stdandard error 并没有直接处理的能力。

管线后面接指令！而且必须要能够接受 standard input 的数据才行，例如 less, more, head, tail。例如 ls, cp, mv 等就不是管线命令，并不会接受来自 stdin 的数据。 也就是说，管线命令主要有两个比较需要注意的地方：

Tips 想一想，如果你硬要让 standard error 可以被管线命令所使用，那该如何处理？其实就是通过上一小节的数据流重导向即可！ 让 2>&1 加入指令中～就可以让 2> 变成 1> 啰！了解了吗？

#### 撷取命令： cut, grep
将一段数据经过分析后，取出我们所想要的。撷取讯息通常是针对“一行一行”来分析的。

cut 这个指令可以将一段讯息的某一段给他“切”出来，处理的讯息是以“行”为单位。

```bash
cut -d '分隔字符' -f fields
cut -c 字符区间 
# -d  ：后面接分隔字符。与 -f 一起使用；
# -f  ：依据 -d 的分隔字符将一段讯息分区成为数段，用 -f 取出第几段的意思；
# -c  ：以字符 （characters） 的单位取出固定字符区间；

# 一：将 PATH 变量取出，我要找出第五个路径。
echo ${PATH}
# /usr/local/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/home/wrma/.local/bin:/home/wrma/bin

echo ${PATH} | cut -d ':' -f 5
# 如同上面的数字显示，我们是以“ : ”作为分隔，因此会出现 /home/wrma/.local/bin
# 那么如果想要列出第 3 与第 5 呢？，就是这样：
echo ${PATH} | cut -d ':' -f 3,5

#二：将 export 输出的讯息，取得第 12 字符以后的所有字串
export
# declare -x HISTCONTROL="ignoredups"
# 不想要“ declare -x ”时，就得这么做：

export | cut -c 12-
# HISTCONTROL="ignoredups"
# 用 -c 可以处理比较具有格式的输出数据！
# 我们还可以指定某个范围的值，例如第 12-20 的字符，就是 cut -c 12-20 等等！

#三：用 last 将显示的登陆者的信息中，仅留下使用者大名
last
# root   pts/1    192.168.201.101  Sat Feb  7 12:35   still logged in
# last 可以输出“帐号/终端机/来源/日期时间”的数据，并且是排列整齐的

last | cut -d ' ' -f 1
```

grep 分析一行讯息，若当中有我们所需要的信息，就将该行拿出来：
```bash
grep [-acinv] [--color=auto] '搜寻字串' filename
# -a ：将 binary 文件以 text 文件的方式搜寻数据
# -c ：计算找到 '搜寻字串' 的次数
# -i ：忽略大小写的不同，所以大小写视为相同
# -n ：顺便输出行号
# -v ：反向选择，亦即显示出没有 '搜寻字串' 内容的那一行！
# --color=auto ：可以将找到的关键字部分加上颜色的显示喔！

# 一：将 last 当中，有出现 root 的那一行就取出来；
last | grep 'root'

# 二：与范例一相反，只要没有 root 的就取出！
last | grep -v 'root'

# 三：在 last 的输出讯息中，只要有 root 就取出，并且仅取第一栏
last | grep 'root' | cut -d ' ' -f 1

# 四：取出 /etc/man_db.conf 内含 MANPATH 的那几行
grep --color=auto 'MANPATH' /etc/man_db.conf
# MANPATH_MAP     /usr/games              /usr/share/man
# MANPATH_MAP     /opt/bin                /opt/man
# MANPATH_MAP     /opt/sbin               /opt/man
# 加上 --color=auto，关键字部分会用特殊颜色显示！
```
CentOS 7 当中，默认的 grep 已经主动加上 --color=auto 在 alias 内了。

#### 排序命令： sort, wc, uniq
sort 可以依据不同的数据型态来排序！例如数字与文字的排序就不一样。排序的字符与语系的编码有关，如果您需要排序时，建议使用 LANG=C 来让语系统一，数据排序比较好一些。
```bash
sort [-fbMnrtuk] [file or stdin]
# -f  ：忽略大小写的差异，例如 A 与 a 视为编码相同；
# -b  ：忽略最前面的空白字符部分；
# -M  ：以月份的名字来排序，例如 JAN, DEC 等等的排序方法；
# -n  ：使用“纯数字”进行排序（默认是以文字体态来排序的）；
# -r  ：反向排序；
# -u  ：就是 uniq ，相同的数据中，仅出现一行代表；
# -t  ：分隔符号，默认是用 [tab] 键来分隔；
# -k  ：以那个区间 （field） 来进行排序的意思

# 一：个人帐号都记录在 /etc/passwd 下，请将帐号进行排序。
cat /etc/passwd | sort
# sort 是默认“以第一个”数据来排序，而且默认是以“文字”型态来排序的！所以由 a 开始排到最后！

# 二：/etc/passwd 内容是以 : 来分隔的，以第三栏来排序
cat /etc/passwd | sort -t ':' -k 3
# root:x:0:0:root:/root:/bin/bash
# wrma:x:1000:1000:wrma:/home/wrma:/bin/bash
# alex:x:1001:1002::/home/alex:/bin/bash
# arod:x:1002:1003::/home/arod:/bin/bash
cat /etc/passwd | sort -t ':' -k 3 -n
# 告知 sort 以数字来排序啊！

# 三：利用 last ，将输出的数据仅取帐号，并加以排序
last | cut -d ' ' -f1 | sort
```

uniq 将重复的数据仅列出一个显示
```bash
uniq [-ic]
# -i  ：忽略大小写字符的不同；
# -c  ：进行计数

# 一：使用 last 将帐号列出，仅取出帐号栏，进行排序后仅取出一位；
last | cut -d ' ' -f1 | sort | uniq

# 二：承上题，如果我还想要知道每个人的登陆总次数呢？
last | cut -d ' ' -f1 | sort | uniq -c
```

wc 计算输出的讯息的整体数据。
```bash
wc [-lwm]
# -l  ：仅列出行；
# -w  ：仅列出多少字（英文单字）；
# -m  ：多少字符；

# 一：/etc/man_db.conf 里面到底有多少相关字、行、字符数？
cat /etc/man_db.conf | wc 
# 131     723    5171
# 输出的三个数字中，分别代表： “行、字数、字符数”

# 二：last 取得登陆系统的总人次？
last | grep [a-zA-Z] | grep -v 'wtmp' | grep -v 'reboot' | grep -v 'unknown' |wc -l 
# 由于 last 会输出空白行, wtmp, unknown, reboot 等无关帐号登陆的信息，因此，我利用
# grep 取出非空白行，以及去除上述关键字那几行，再计算行数，就能够了解啰！

# 目前帐号文件中有多少个帐号时
cat /etc/passwd | wc -l
#因为 /etc/passwd 里头一行代表一个使用者
```

#### 双向重导向： tee
tee 会同时将数据流分送到文件去与屏幕(screen)；输出到屏幕的就是 stdout。
```bash
tee [-a] file
# -a  ：以累加 （append） 的方式，将数据加入 file 当中

last | tee last.list | cut -d " " -f1
# 将 last 的输出存一份到 last.list 文件中；

ls -l /home | tee ~/homefile | more
# 将 ls 的数据存一份到 ~/homefile ，同时屏幕也有输出讯息！

ls -l / | tee -a ~/homefile | more
# 加上 -a 这个选项则能将讯息追加。
```

#### 字符转换命令： tr, col, join, paste, expand
tr 可以用来删除一段讯息当中的文字，或者是进行文字讯息的替换！
```bash
tr [-ds] SET1 ...
# -d  ：删除讯息当中的 SET1 这个字串；
# -s  ：取代掉重复的字符！

# 一：将 last 输出的讯息中，所有的小写变成大写字符：
last | tr '[a-z]' '[A-Z]' # 没有加上单引号也是可以执行的，如：“ last | tr [a-z] [A-Z] ”

# 二：将 /etc/passwd 输出的讯息中，将冒号 （:） 删除
cat /etc/passwd | tr -d ':'

# 三：将 /etc/passwd 转存成 dos 断行到 /root/passwd 中，再将 ^M 符号删除
cp /etc/passwd ~/passwd && unix2dos ~/passwd
file /etc/passwd ~/passwd
# /etc/passwd:       ASCII text
# /home/wrma/passwd: ASCII text, with CRLF line terminators  #就是 DOS 断行

cat ~/passwd | tr -d '\r' > ~/passwd.linux # \r 指的是 DOS 的断行字符
ll /etc/passwd ~/passwd*
# -rw-r--r--. 1 root   root   2092 Jun 17 00:20 /etc/passwd
# -rw-r--r--. 1 wrma wrma 2133 Jul  9 22:13 /home/wrma/passwd
# -rw-rw-r--. 1 wrma wrma 2092 Jul  9 22:13 /home/wrma/passwd.linux
# 处理过后，发现文件大小与原本的 /etc/passwd 就一致了！
# DOS 下面会自动的在每行行尾加入 ^M 这个断行符号！除了以前讲过的 dos2unix 之外，也可以使用这个 tr 来将 ^M (\r)去除。
```

col 将 [tab] 按键取代成为空白键
```bash
col [-xb]
# -x  ：将 tab 键转换成对等的空白键

# 一：利用 cat -A 显示出所有特殊按键，最后以 col 将 [tab] 转成空白
cat -A /etc/man_db.conf  #此时会看到很多 ^I 的符号，那就是 tab
cat /etc/man_db.conf | col -x | cat -A | more
```

join 处理“两个文件当中，有 "相同数据" 的那一行，将他加在一起”
```bash
join [-ti12] file1 file2
# -t  ：join 默认以空白字符分隔数据，并且比对“第一个字段”的数据，如果两个文件相同，则将两笔数据联成一行，且第一个字段放在第一个！
# -i  ：忽略大小写的差异；
# -1  ：数字1 ，代表“第一个文件要用那个字段来分析”的意思；
# -2  ：代表“第二个文件要用那个字段来分析”的意思。

# 一：用 root 的身份，将 /etc/passwd 与 /etc/shadow 相关数据整合成一栏
head -n 3 /etc/passwd /etc/shadow
# /etc/passwd
# root:x:0:0:root:/root:/bin/bash
# bin:x:1:1:bin:/bin:/sbin/nologin
# daemon:x:2:2:daemon:/sbin:/sbin/nologin

# /etc/shadow 
# root:$6$wtbCCce/PxMeE5wm$KE2IfSJr...:16559:0:99999:7:::
# bin:*:16372:0:99999:7:::
# daemon:*:16372:0:99999:7:::
# 这两个文件的最左边字段都是相同帐号，且以 : 分隔

join -t ':' /etc/passwd /etc/shadow | head -n 3
# root:x:0:0:root:/root:/bin/bash:$6$wtbCCce/PxMeE5wm$KE2IfSJr...:16559:0:99999:7:::
# bin:x:1:1:bin:/bin:/sbin/nologin:*:16372:0:99999:7:::
# daemon:x:2:2:daemon:/sbin:/sbin/nologin:*:16372:0:99999:7:::
# 通过上面这个动作，我们可以将两个文件第一字段相同者整合成一列！

# 二：/etc/passwd 第四个字段是 GID ，GID 又记录在 /etc/group 当中的第三个字段，将两个文件整合
head -n 3 /etc/passwd /etc/group
# /etc/passwd 
# root:x:0:0:root:/root:/bin/bash
# bin:x:1:1:bin:/bin:/sbin/nologin
# daemon:x:2:2:daemon:/sbin:/sbin/nologin
# 
# /etc/group 
# root:x:0:
# bin:x:1:
# daemon:x:2:
join -t ':' -1 4 /etc/passwd -2 3 /etc/group | head -n 3
# 0:root:x:0:root:/root:/bin/bash:root:x:
# 1:bin:x:1:bin:/bin:/sbin/nologin:bin:x:
# 2:daemon:x:2:daemon:/sbin:/sbin/nologin:daemon:x:
# 同样的，相同的字段部分被移动到最前面了！所以第二个文件的内容就没再显示。

#在使用 join 之前，需要处理的文件应该要事先经过排序 （sort） 处理！ 否则有些比对的项目会被略过。
```

paste 就直接“将两行贴在一起，且中间以 [tab] 键隔开”。
```bash
paste [-d] file1 file2
# -d  ：后面可以接分隔字符。默认是以 [tab] 来分隔的！
# -   ：如果 file 部分写成 - ，表示来自 standard input 的数据的意思。

# 一：用 root 身份，将 /etc/passwd 与 /etc/shadow 同一行贴在一起
paste /etc/passwd /etc/shadow
# root:x:0:0:root:/root:/bin/bash root:$6$wtbCCce/PxMeE5wm$KE2IfSJr...:16559:0:99999:7:::
# bin:x:1:1:bin:/bin:/sbin/nologin        bin:*:16372:0:99999:7:::
# daemon:x:2:2:daemon:/sbin:/sbin/nologin daemon:*:16372:0:99999:7:::
# 同一行中间是以 [tab] 按键隔开的！

# 二：先将 /etc/group 读出（用 cat），然后与范例一贴上一起！且仅取出前三行
cat /etc/group | paste /etc/passwd /etc/shadow - | head -n 3 # 重点在 - 的使用！代表 stdin
```

expand 将 [tab] 按键转成空白键：
```bash
expand [-t] file
# -t  ：后面可以接数字。定义一个 [tab] 按键代表多少个字符。默认8个

# 一：将 /etc/man_db.conf 内行首为 MANPATH 的字样就取出；仅取前三行；将所有的符号都列出来；
grep '^MANPATH' /etc/man_db.conf | head -n 3 |cat -A
# MANPATH_MAP^I/bin^I^I^I/usr/share/man$
# MANPATH_MAP^I/usr/bin^I^I/usr/share/man$
# MANPATH_MAP^I/sbin^I^I^I/usr/share/man$
# [tab] 按键可以被 cat -A 显示成为 ^I 

# 二：将 [tab] 按键设置成 6 个字符
grep '^MANPATH' /etc/man_db.conf | head -n 3 | expand -t 6 - | cat -A
# MANPATH_MAP /bin              /usr/share/man$
# MANPATH_MAP /usr/bin          /usr/share/man$
# MANPATH_MAP /sbin             /usr/share/man$
```

#### 分区命令： split
split 将一个大文件，依据文件大小或行数来分区成小文件～
```bash
split [-bl] file PREFIX
# -b  ：后面可接分区文件大小，可加单位，例如 b, k, m 等；
# -l  ：以行数来进行分区。
# PREFIX ：代表前置字符的意思，可作为分区文件的前导文字。

# 一：我的 /etc/services 有六百多K，若想要分成 300K 一个文件
cd /tmp; split -b 300k /etc/services services
ll -k services*
# -rw-rw-r--. 1 wrma wrma 307200 Jul  9 22:52 servicesaa
# -rw-rw-r--. 1 wrma wrma 307200 Jul  9 22:52 servicesab
# -rw-rw-r--. 1 wrma wrma  55893 Jul  9 22:52 servicesac
# 小文件会以xxxaa, xxxab, xxxac 等方式来创建！

# 二：如何将上面的三个小文件合成一个文件，文件名为 servicesback
cat services* >> servicesback
# 就用数据流重导向

# 三：使用 ls -al / 输出的信息中，每十行记录成一个文件
ls -al / | split -l 10 - lsroot
wc -l lsroot*
# 10 lsrootaa
# 10 lsrootab
#  4 lsrootac
# 24 total
# 重点在 - ，一般来说，如果需要 stdout/stdin 时，- 就会被当成 stdin 或 stdout ～
```

#### 参数代换： xargs
xargs 在产生某个指令的参数，xargs 可以读入 stdin 的数据，且以空白字符或断行字符将 stdin 的数据分隔成为 arguments 。如果有一些文件名或者是其他意义的名词内含有空白字符的时候，xargs 可能就会误判了。
```bash
xargs [-0epn] command
# -0  ：如果输入的 stdin 含有特殊字符，例如 `, \, 空白键等等字符时，这个 -0 可以将他还原成一般字符。
# -e  ：这个是 EOF （end of file） 的意思。后面可以接一个字串，当 xargs 分析到这个字串时，就会停止工作
# -p  ：在执行每个指令的 argument 时，都会询问使用者的意思；
# -n  ：后面接次数，每次 command 指令执行时，要使用几个参数的意思。
# 当 xargs 后面没有接任何的指令时，默认是以 echo 来进行输出！

# 一：将 /etc/passwd 内的第一栏取出，仅取三行，使用 id 这个指令将每个帐号内容秀出来
id root
# uid=0（root） gid=0（root） groups=0（root）   # 这个 id 指令可以查询使用者的 UID/GID 等信息

id $（cut -d ':' -f 1 /etc/passwd | head -n 3）
# 使用 $（cmd） 可以预先取得参数，但是， id 这个指令仅能接受一个参数！所以这个指令执行会出现错误！

cut -d ':' -f 1 /etc/passwd | head -n 3 | id
# uid=1000（wrma） gid=1000（wrma） groups=1000（wrma）,10（wheel）   # 查自己了~
# 因为 id 并不是管线命令，因此这个指令执行后，前面的东西通通不见！只会执行 id！

cut -d ':' -f 1 /etc/passwd | head -n 3 | xargs id
# 依旧会出现错误！这是因为 xargs 一口气将全部的数据通通丢给 id 处理～但 id 就接受 1 个！

cut -d ':' -f 1 /etc/passwd | head -n 3 | xargs -n 1 id
# uid=0（root） gid=0（root） groups=0（root）
# uid=1（bin） gid=1（bin） groups=1（bin）
# uid=2（daemon） gid=2（daemon） groups=2（daemon）
# 通过 -n 来处理，一次给予一个参数，因此上述的结果就 OK 正常的显示！

# 二：同上，但每次执行 id 时，都要询问使用者是否动作
cut -d ':' -f 1 /etc/passwd | head -n 3 | xargs -p -n 1 id
# id root ?...y
# uid=0（root） gid=0（root） groups=0（root）
# id bin ?...y
# .....

# 三：将所有的 /etc/passwd 内的帐号都以 id 查阅，但查到 sync 就结束指令串
cut -d ':' -f 1 /etc/passwd | xargs -e'sync' -n 1 id
#  -e'sync' 是连在一起的，中间没有空白键。
# 使用 xargs 的原因是很多指令不支持管线命令，可以通过 xargs 来提供该指令引用 standard input：

# 四：找出 /usr/sbin 下面具有特殊权限的文件名，并使用 ls -l 列出详细属性
find /usr/sbin -perm /7000 | xargs ls -l
# -rwx--s--x. 1 root lock      11208 Jun 10  2014 /usr/sbin/lockdev
# -rwsr-xr-x. 1 root root     113400 Mar  6 12:17 /usr/sbin/mount.nfs
# -rwxr-sr-x. 1 root root      11208 Mar  6 11:05 /usr/sbin/netreport
# .....（下面省略）.....
# 也可以使用“ ls -l $（find /usr/sbin -perm /7000） ”来处理
```

#### 减号 - 的用途
在管线命令当中，常常会使用到前一个指令的 stdout 作为这次的 stdin，减号 "-" 可以替代stdout stdin：
```bash
mkdir /tmp/homeback
tar -cvf - /home | tar -xvf - -C /tmp/homeback
# 将 /home 里面的文件打包，传送到 stdout（减号）； 后面的 tar -xvf - 中的减号是stdin，取用前一个指令的 stdout。
```