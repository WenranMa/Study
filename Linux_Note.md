
## Linux 软件安装
### RPM 安装
    有两种安装包：
    1. 最初的Linux是通过源码包安装的。编译时间长，容易报错。
    （LAMP Linux, Apache, MySQL, PHP网站开发套件。）

    2. 后来出现了二进制包，也就是RPM包，不能看到源码，但安装比源码安装简单。
    再后来出现了yum工具安装以解决RPM包安装的依赖问题。

    RPM安装命令：
    rpm -ivh 软件包全名。
    -i install 安装。
    -v verbose 显示详细信息。
    -h hash 显示进度。

    升级命令：
    rpm -Uvh 包全名。-U update。

    卸载命令：
    rpm -e 包名。-e erase。这里不需要包全名，只要包名（包全名的英文部分）就可以。

    查询命令：
    rpm -q 包名。查询某个包。
    rpm -qa 查询全部安装的包。rpm -qa | grep httpd
    rpm -ql 包名。查询包中各种文件的安装位置。也可以查询未安装的包准备装在哪。
    rpm -qf 系统文件名。查询该文件属于哪个包。

    校验命令：
    rpm -V 包名。查看包中文件是否会更改。

### yum 在线安装
    /etc/yum.repos.d/目录中存在.repo文件。
    repo文件的内容：
    [name]:     容器名称，如[base],[update]。
    name:       容器说明。
    mirrorlist: 镜像站点。
    baseurl:    yum源服务器地址。
    enabled:    容器是否生效，默认生效。
    gpgcheck:   如果是1，RPM数字证书生效。
    gpgkey:     数字证书的公钥保存位置。

    查询命令：
    yum list
    yum search 关键字

    安装命令：
    yum -y install 包名，-y 自动回答yes，而且不需要包全名，包名就可以。

    升级命令：
    yum -y update 包名。如果不写包名，则会升级所有。

    卸载：
    yum -y remove 包名。不建议使用，服务器使用最小化安装，用什么装什么，尽量不卸载。

    yum还支持组安装：
    yum grouplist, yum groupinstall, yum groupremove。

### 源码安装
    make 编译。
    make clear 如果错误，可以清楚已经编译的输出文件。
    make install，安装命令。

    如果删除，则直接删除安装目录。

---

## Linux 权限管理
    服务器应当合理分配权限，一般只有一个管理员，其他人为普通用户。

### 1. 基本权限
    权限位：-rw-r--r-- ,一共10位，第一位为文件类型（- 文件，d 目录，l 软链接）。
    后面每三位为一组，第一组代表所有者u，第二组为所属组g，第三组为其他人o。
    r读，w写，x执行。

#### 基本权限修改 chmod 命令：
    chmod [选项] 模式 文件名

    例如：
    chmod u+x readme.md 给readme.md的所有者u加可执行权限。
    chmod g+w,o+w readme.md 给readme.md的所属组g和其他人o加写权限。
    chmod u-w,g-w,o-w readme.md 去掉readme.md的写权限。
    chmod u=rwx,g=rw readme.md 另一种方式，直接复制。
    chomd a=rwx readme.md a代表所有人。

    用数字代表权限（二进制位）：r -- 4, w -- 2, x -- 1. rwxr-xr-x即755。
    chmod 755 readme.md, 777为最高权限，644读写权限，755可执行权限，这几个比较常用。

#### 权限的作用

    r: 读取文件内容（cat, more, head, tail），可以查看目录下文件名（ls）。
    w: 对文件编辑，新增，修改文件内容（vi, echo），但不包括删除文件。写权限是指对下一级的操作，例如要有对目录的写权限，才可以删除目录下的文件。对目录可新曾，删除，剪切文件和子目录等（touch, rm, mv, cp）。
    x: 对文件的执行权限。对目录可以进入（cd）。

    对文件的最高权限是执行x，对目录的最高权限是写w。对目录可以赋的权限只有0，5，7，其他（1，4，6）没有意义。

#### chown 命令
    修改文件所有者 chown user 文件名。
    chown user:group 文件名可以一次修改所有者和所属组。

#### chgrp 命令
    修改文件所属组 chgrp 组名 文件名
    Linux会在添加用户时，会默认增加和用户名相同的组名。

#### 文件默认权限 umask
    umask 命令，结果022。可以修改mask值。

    文件默认不能建立可执行文件，必须手动赋予，所以文件默认权限最大为666，默认权限和umask换算成字母后相减得到最后权限。
    文件最大权限666（-rw-rw-rw-），umask为022（-----w--w-），再相减为 -rw-r--r--。

    目录的默认权限为777（drwxrwxrwx），umask为022（-----w--w-），换算后相减为755（drwxr-xr-x)。

### 2. 特殊权限
#### sudo 权限
    root把超级用户执行的命令赋予普通用户。sudo的操作对象是系统命令！

    visudo超级用户赋予权限的命令。visudo会打开/etc/sudoers文件，可以赋予普通用户命令。
    例如：visudo 然后键入 user1 ALL=/sbin/shutdown -r now。保存退出。
    
    su命令可以切换用户。
    然后用普通用户，sudo -l可以拆看可以执行的命令（被赋予的）。
    普通用户输入的命令前都要加sudo。

---

## Linux 系统管理
### 1. 进程管理
    进程是一个正在运行的程序或者命令，有自己的地址空间，占用系统资源。
    进程管理主要是：判断服务器健康状态，查看系统中所有进程，杀死进程。

#### 进程查看命令 ps
    ps aux 查看系统所有进程，BSD操作系统格式。
    ps -le 查看系统所有进程，Linux标准命令格式。(常用ps -ef|grep "xxx")

    ps命令输出：
    USER: 哪个用户产生。
    PID: 进程ID。
    CPU: CPU占比。
    MEM: 物理内存百分比。
    VSZ: 虚拟内存大小，KB。
    RSS: 物理内存大小，KB。
    TTY: 终端，tty1-tty6为本地字符终端，tty7为本地图形终端，pts/0 - xxx是远程终端。如果是？基本为系统进程。
    TIME: 占用CPU时间。
    CMD: 进程名字。

    pstree, 显示进程树。

#### top命令
    top [选项] 每三秒钟刷新一次，默认按CPU占用率排序，可以用上面的几行查看进程是否健康。

    选项：
    -d 秒数，指定每隔几秒更新，默认3秒。
    -b 使用批处理输出，一般和-n合用。
    -n 次数，指定执行top命令次数。
    top -b -n 1 > top.log

    交互命令：
    shift+P 以CPU占用率排序。
    shift+M 以内存占用率排序。
    shift+N 以PID排序。
    q 退出。

最上面的几行：
```
top - 11:05:32 up 462 days,  3:37, 68 users,  load average: 0.09, 0.10, 0.06
Tasks: 739 total,   1 running, 737 sleeping,   1 stopped,   0 zombie
%Cpu(s):  0.2 us,  0.1 sy,  0.0 ni, 98.7 id,  1.0 wa,  0.0 hi,  0.0 si,  0.0 st
KiB Mem : 16267988 total, 11000276 free,  1124160 used,  4143552 buff/cache
KiB Swap:  8388604 total,  5282652 free,  3105952 used. 14630928 avail Mem 

# top - 系统时间 up 运行时间, 当前登录用户, 1分钟，5分钟，15分钟的平均负载。
# Tasks: 总进程，在运行，休眠，正在停止， 僵尸进程。
# CPU: us用户占用，sy系统占用， ni修改过优先级的用户进程占比， id空闲， wa等待输入输出进程占比，
  hi硬中断请求服务占比, si软终端服务请求占比, st（steal time）虚拟时间占比。
# 内存占用情况。
# 交换分区占比。

Buffer缓冲，加快数据写入。
Cache缓存，加快数据读取。
```

#### 杀死进程
    kill命令, 杀死单一进程
    kill -信号 进程号PID
    kill -l 显示信号，一共64个。

    kill -1 xxx 重启。
    kill -9 xxx 强制杀死。
    kill -15 xxx 默认。

    killall, 批量杀进程
    killall [选项][信号] 进程名。
    例如：killall -i -9 httpd，-i表示交互模式，系统会询问，-I表示忽略进程名字大小写。

    pkill, 也是批量
    pkill [选项][信号] 终端，例如：pkill -9 -t pts/xxx -t表示按终端杀死。

    w命令，可以查看登录用户。

#### 修改进程优先级
    cpu在同一个时钟周期只能运算一个指令。进程优先级决定每个进程的处理顺序。
    ps -le可以显示进程优先级，PRI(priority)和NI(nice)两位都代表优先级。
    用户只能修改NI，但系统最终生效的是PRI。PRI = PRI + NI。
    NI的范围是-20到19，普通用户只能修改0到19，root用户可以修改NI为负值。一般不需要用户去手动调整优先级。

    nice命令用于修改NI值，只能用户新启动的进程优先级，已经存在的不能改。
    nice [选项] 命令。
    举例：nice -n -5 service httpd start，-n表示NI值，后面跟一个进程的启动命令。

    renice [选项] PID用于修改已经存在进程的优先级。

### 2. 工作管理（后台管理）
    工作（jobs）是和终端绑定的，当前终端只能管理当前终端的工作，不能管理其他终端。

    有两种方法将工作放入后台。
    1. 命令 &，可以放入后台的，必须是不用和用户交互的，比如tar命令。如果是top命令，则+&后会是暂停状态。
    2. 命令执行过程中按ctrl+z, 这表示将程序在后台暂停。

    jobs命令可以查看后台进程。jobs -l 可以显示PID号。方括号[xx]中是工作号，还有+表示最后一个放入后台的命令，-表示倒数第二个。
    fg命令把进程恢复到前台，fg %工作号。bg命令把进程再放入后台，bg %工作号。
    如果不加工作号，则按顺序执行(+,-在这里会变化，工作号不会)。

    如果终端关掉，所有该终端的后台进程也会关闭。使进程与终端不绑定的方法：
    1. 放入/etc/rc.local文件。系统启动时调用，不与终端绑定。
    2. 使用系统定时任务。
    3. 使用nohup命令。nohup 命令 &。终端关闭，进程仍然存在。

### 3. 查看系统资源
#### vmstat 命令
    显示系统内存，磁盘和CPU信息
    vmstat [刷新延时 刷新次数]，例如`vmstat 1 3`

```
procs -----------memory---------- ---swap-- -----io---- -system-- ------cpu-----
 r  b   swpd   free   buff  cache   si   so    bi    bo   in   cs us sy id wa st
 1  0 2896312 12693512 404924 2339520    0    0     0     5    0    0  0  0 99  1  0
 0  0 2896312 12694116 404924 2339560    0    0     0     0  226  414  0  0 100  0  0
 0  0 2896312 12693744 404924 2339560    0    0     0     8  208  369  0  0 100  0  0

procs 进程信息字段：
r: 等待运行的进程数，数字越大，系统越繁忙。
b: 不能被唤醒的进程数，数字越大，系统越繁忙。

memory 内存信息字段：
swpd: 虚拟内存使用情况，单位KB。
free: 空闲的内存。
buff: 缓冲的内存。加速数据写入硬盘。
cache: 缓存的内存。加速数据从硬盘的读取。

swap 交换分区：
si: 从磁盘交换到内存的数据量，单位KB。
so: 从内存到磁盘的量。两个数越大，系统性能越差。

io 磁盘读写信息字段：
bi: 从块设备读入数据的总量，单位是块。
bo: 写到块设备的数据量。两个数越大，系统IO越繁忙。

system 系统信息字段：
in: 每秒被中断的进程次数。
cs: 每秒进行的事件切换次数。两个数越大，系统越繁忙。

cpu 处理器信息段：
us: 非内核进程消耗CPU运行时间百分比。
sy: 内核进程。
id: 空闲CPU百分比。越大系统越闲。
wa: 等待IO。
st: 被虚拟机盗用。
```

#### dmesg 命令
    显示内核自检信息
    demesg | grep CPU

#### free 命令
    查看内存使用状态
    free [-b -k -m -g] 选项表示不同的单位，字节，KB，MB，GB。

#### uptime 命令
    其实就是top命令的第一行。

#### uname 命令
    查看内核相关信息。
    uname [-a -r -s] 分别为所有信息，内核版本，内核名称。

#### lsof 命令
    列出进程打开或使用的文件信息。
    lsof | more 显示所有进程调用的文件。
    lsof /sbin/init 查看某个文件被哪个进程调用。
    lsof -c 进程名，如lsof -c httpd 查看httpd进程调用了哪些文件。
    lsof -u 用户名，如lsof -u root 查看root用户的进程调用文件。

### 4. 系统定时任务
#### at 单次任务
    atd有访问控制，/etc/目录下有at.allow文件白名单中的用户可以使用at命令。
    或这at.deny黑名单中的用户不能使用at。
    或者都有但at.allow优先级高。
    如果都没有，则只有root用户可用。

    at [选项] 时间
    -c 工作号：显示at工作的实际内容。
    时间格式：
    HH:MM
    HH:MM YYYY-MM-DD   , 02:30 2019-07-01
    HH:MM [month][date], 02:30 July 25
    HH:MM + [minutes|hours|days|weeks], now + 2 minutes

    at+时间之后会进入at交互模式以输入具体要执行的任务。
    例如：
    at now + 2 minutes
    at> /home/wrma/hello.sh

    atq命令可以查看当前服务器at的工作。

#### crontab 循环定时任务
    与at一样有cron.allow白名单和cron.deny黑名单。

    crontab [选项]
    -e 编辑定时任务。
    -l 查询任务。
    -r 删除当前用户的crontab任务（删除所有任务）。

    crontab -e 后会打开vim。格式是 * * * * * 加上任务或脚本。这个命令会绑定当前用户身份。

    五个星号*代表时间，分别表示：
    1. 一个小时中的第几分钟，范围0-59
    2. 一天当中的第几个小时，范围0-23
    3. 一月当中的第几天，范围1-31
    4. 一年中的第几个月，范围1-12
    5. 一周当中的星期几，0-7（0，7都是星期日）
    最小单位是分钟，最大单位是月。

    特殊符号：
    *表示任意时间，比如第一个*代表一个小时中的每一个分钟都执行一次。
    ,代表不连续时间，比如0 8,12,15 * * * 表示每天8点0分，12点0分，15点0分执行一次命令。
    -代表连续时间，比如0 5 * * 1-6 表示周一到周六每天5点0分执行一次。
    */n 表示每隔多久执行，比如*/10 * * * *代表每隔10分钟执行一次。

    系统的定时任务：
    需要编辑/etc/crontab配置文件下。
    或者直接拷贝要执行的脚本到/etc/cron.{hourly,daily,weekly,monthly}目录中。

#### anacron
    保证系统关机时错过的定时任务，可以在开机后再执行。
    anacron会以一天，一周，一个月作为检测周期。
    系统的/var/spool/anacron/目录中存在cron.{daily,weekly,monthly}文件，记录上次cron的时间。
    和当前时间比较，如果两个值的差超过了anacron的指定时间，则证明cron被漏执行。

    anacron配置文件在/etc/anacrontab，上面的/etc/cron.{daily,weekly,monthly}会被调用。

---

## Linux 服务管理
#### 系统运行级别：

    0. 关机
    1. 单用户模式，主要用于系统修复
    2. 不完全命令模式，不含NFS服务
    3. 完全命令模式，就是标准字符界面
    4. 系统保留
    5. 图形模式
    6. 重启

    runlevel 显示运行级别。
    init 级别号 改变运行级别。

#### 服务分类







---

## Linux 网络管理
### 1.基础
#### ISO/OSI七层模型
    OSI,开放系统互联模型。

| Level | 数据单位 | 解释 |
| ----- | ---- | ------- |
| 应用层 | APDU | 用户接口，比如浏览器界面 |
| 表示层 | PPDU | 数据表现形式，ASCII, mp3, jpg, 压缩，加密 |
| 会话层 | SPDU | 管理会话层，比如判断是否给传输层 |
| 传输层 | TPDU | TCP/UDP可靠或不可靠传输，端口号 |
| 网络层 | 报文 | 存着IP地址，用于外网通信 |
| 数据链路层 | 帧 | 帧中存储着MAC地址，也就是网卡的物理地址，负责局域网络 | 
| 物理层 | Bit | 比特流传输，物理接口，电气特性 |

    上层最接近用户。上三层给用户提供服务，没有网络也需要这三层，下四层用于数据传输。
    PDU: Protocol Data Unit。

#### TCP/IP四层模型

| Level | 解释 |
| ----- | ---- |
| 应用层 | 对应OSI上三层 FTP, Telnet, DNS, SMTP|
| 传输层 | OSI 传输层 TCP, UDP|
| 网际互联层 | OSI 网络层 IP协议，IGMP，ICMP互联网控制报文协议(ping)|
| 网络接口层 | OSI 下两层 ARP地址解析协议工作这层| 

#### IP地址与子网掩码

| 类别 | 最大网络数 | IP地址范围 | 最大主机数 | 私有IP地址 |
| --- | --------- | --------- | -------- | ---------- |
| A类 | 126（2^7-2）| 1.0.0.0 -- 126.255.255.255 | 2^24-2 | 10.0.0.0 -- 10.255.255.255 |
| B类 | 2^14 | 128.0.0.0 -- 191.255.255.255 | 2^16-2 | 172.16.0.0 -- 172.31.255.255 |
| C类 | 2^21 | 192.0.0.0 -- 223.255.255.255 | 2^8-2 | 192.168.0.0 -- 192.168.255.255 |

    A类最大网络数减2是因为0.0.0.0 不用，而127.0.0.0表示本地IP。
    公网IP需要付费。但私有IP地址表示免费使用，可以做内网IP，比如学校，办公室等大量使用，可以保护公网IP。
    但私有IP不可以直接访问公网。私有IP数都减2是因为第一个地址为网络地址，最后一个为广播地址。

    路由器是跨网络通信，同一个网络使用交换机通信。

    子网掩码（subnet mask）
    255.0.0.0, 255.255.0.0, 255.255.255.0分别是三类（A, B, C）标准子网掩码。
    IP和子网掩码要一起查看。子网掩码255对应IP的公网段，0对应的私有IP，同一个网段中的主机。

#### 端口号
    用于区分具体服务。
    FTP文件传输协议：20，21
    SSH安全shell协议：22
    telnet远程登录协议：23（不安全，基本已经禁止）
    DNS域名系统：53
    http超文本传输协议：80 （https: 443）
    SMTP简单邮件传输协议：25
    POP3邮局协议3代：110

#### DNS
    Domain Name System域名解析。早期用hosts文件进行ip和域名的对应，但是维护困难。

    域名空间：
    域名中的点（.）用于分级管理，域名服务器也是分层结构。
    主机名（www）.二级域（ibm, microsoft....）.顶级域（com/org/cn/jp）。域名都是全球唯一的。

#### 网关
    网关（Gateway）又称网间连接器，协议转换器。
    1. 内网计算机访问的不是本网段数据时，就要使用。
    2. 网关负责内网IP和公网IP的互转。

    网关是服务器或路由器。
    一个局域网可以用交换机传递数据，交换机属于数据链路层，所以不认识IP（网络层），交换机认识MAC地址。
    路由器是不同网段之间进行数据交换的。这个路由器就是网关。也可以用服务器搭建网关功能，所以网关也可以是服务器。

### 2.网络配置
#### IP地址配置
    ifconfig命令可以用于查看网络状态和配置IP地址，但只是一次生效，重启之后就会恢复。

    ifconfig结果：
    lo表示loopback网卡，本地地址127.0.0.1，这个网卡只是说明当前主机的网络协议正常。

    eth0表示第一块网卡：
    IP地址 inet 10.2.1.56
    子网掩码 netmask 255.255.255.0
    广播地址 broadcast 10.2.1.255
    还有接收包，发送包的信息等。

    ifconfig命令配置网络:
    ifconfig etho 192.168.0.200 netmask 255.255.255.0

#### linux网络配置文件
    网卡配置文件位置：/etc/sysconfig/network-scripts/ifcfg-eth0

    内容：
    DEVICE=eth0 名字必须和文件匹配
    TYPE=Ethernet
    NAME="eth0"
    ONBOOT=yes
    BOOTPROTO=dhcp 也可以是none, static
    IPV6INIT=no
    PEERDNS=no

    hostname命令可以用于查看主机名。
    主机名文件：/etc/sysconfig/network

    DNS文件：/etc/resolv.conf
    nameserver:名称服务器。

### 3.网络命令
#### 环境查看命令
    ifconfig 只能查看ip和子网掩码和广播地址，不能看到网关和DNS。

    ifup ifdown命令用于开启和关闭网卡。例如ifdown lo, ifup lo.

    netstat命令：
    -t TCP端口号。
    -u UDP端口号。
    -l 仅列出在监听状态的网络服务。
    -a 查看所有连接和端口。
    -n 显示IP和端口号，不显示域名和服务器。

```
例如 netstat -tuln
Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State
tcp        0      0 0.0.0.0:3306            0.0.0.0:*               LISTEN
tcp        0      0 0.0.0.0:587             0.0.0.0:*               LISTEN
tcp        0      0 0.0.0.0:9100            0.0.0.0:*               LISTEN
tcp        0      0 0.0.0.0:111             0.0.0.0:*               LISTEN
tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN
tcp        0      0 0.0.0.0:20088           0.0.0.0:*               LISTEN
tcp        0      0 0.0.0.0:8089            0.0.0.0:*               LISTEN
tcp        0      0 127.0.0.1:199           0.0.0.0:*               LISTEN
udp        0      0 0.0.0.0:68              0.0.0.0:*
udp        0      0 0.0.0.0:111             0.0.0.0:*
udp        0      0 0.0.0.0:161             0.0.0.0:*
udp        0      0 127.0.0.1:323           0.0.0.0:*
udp        0      0 127.0.0.1:25375         0.0.0.0:*
udp        0      0 0.0.0.0:947             0.0.0.0:*
udp        0      0 0.0.0.0:58773           0.0.0.0:*
udp        0      0 0.0.0.0:10144           0.0.0.0:*
```

    再例如：
    netstat -an | grep ESTABLISHED 显示建立的远程连接。
    netstat -an | grep ESTABLISHED | wc -l 统计建立的远程连接。

    netstat -rn 列出所有路由，最后一个就是网关。
    route -n 与上面的命令一致。

    nslookup 进行域名与IP的解析。
    例如nslookup localhost, nslookup www.taobao.com。

#### 网络测试命令
    ping命令，ping ip或域名。-c 次数，可以限定ping的次数。
    例如：ping www.taobao.com -c 10

    telnet命令，telnet ip或域名 端口号，可以测试服务器端口是否开启。
    例如：telnet www.taobao.com 80 （ctrl+] quit退出）。

    traceroute命令，traceroute ip或域名，路由跟踪。
    例如：traceroute www.google.com。

    wget命令，下载命令。

    tcpdump命令，用于抓包。
    例如：tcpdump -i eth0 -nnX prot 21
    -i 指定网卡。
    -nn 将数据包中的域名和服务转为IP和端口。
    -X 16进制显示。
    port 端口号。

### 4.远程登录
#### SSH
    对称加密算法，一个秘钥可以同时用作信息加密和解密，也叫单秘钥加密。
    非对称加密算法，有两个秘钥，公开和私有（public key and private key）。
    想象一个房间有两扇门，一个是管理员的公钥和密码加密，另一个是用户的公钥和密码，这样两人都能开门，但彼此不知道密码，比对称加密更安全。

    SSH即Secure Shell，用的是非对称加密策略。

    ssh命令：
    ssh 用户名@ip(或主机名)。用户名可以省略，表示用当前用户登录。exit命令退出。
    第一ssh会提示下载主机的ssh公钥，存于.ssh目录下。

    scp命令：
    scp [-r] 用户名@ip:文件路径 本地路径 用于下载文件。
    scp [-r] 粉底文件 用户名@ip:文件路径 用于上传文件。-r表示目录。
