# Linux 命令行速查表

 [bash](https://www.cheat-sheet.cn/tags/bash) [linux](https://www.cheat-sheet.cn/tags/linux)

Linux是一套免费使用和自由传播的类Unix操作系统，是一个基于POSIX和Unix的多用户、多任务、支持多线程和多CPU的操作系统。它能运行主要的Unix工具软件、应用程序和网络协议。它支持32位和64位硬件。Linux继承了Unix以网络为核心的设计思想，是一个性能稳定的多用户网络操作系统。

## 系统

|                 |                                    |
| :-------------- | :--------------------------------- |
| uname           | 显示linux系统信息                  |
| uname -r        | 显示内核版本信息                   |
| uptime          | 显示系统运行的时间（包括平均负载） |
| hostname        | 显示系统主机名                     |
| hostname -i     | 显示系统的IP地址                   |
| last reboot     | 显示系统重新启动历史记录           |
| date            | 显示当前系统日期和时间             |
| timedatectl     | 查询和更改系统时钟                 |
| cal             | 显示当前日历的月份和日期           |
| w               | 显示系统中当前登录的用户           |
| whoami          | 显示您的登录身份                   |
| finger username | 显示有关用户的信息                 |

## 硬件

|                             |                                                           |
| :-------------------------- | :-------------------------------------------------------- |
| dmesg                       | 显示启动消息                                              |
| cat /proc/cpuinfo           | 显示有关CPU的更多信息，例如型号、型号名称、核心、厂商标识 |
| cat /proc/meminfo           | 显示有关硬件内存的更多信息，例如总内存和可用内存          |
| lshw                        | 显示有关系统硬件配置的信息                                |
| lsblk                       | 显示块设备相关信息                                        |
| free -m                     | 显示系统中空闲和使用的内存(-m标志表示内存(MB))            |
| lspci -tv                   | 在树状图中显示PCI设备                                     |
| lsusb -tv                   | 以树状图的形式显示USB设备                                 |
| dmidecode                   | 显示BIOS中的硬件信息                                      |
| hdparm -i /dev/xda          | 显示有关磁盘数据的信息                                    |
| hdparm -tT /dev/xda <:code> | 在设备xda上进行读速度测试                                 |
| badblocks -s /dev/xda       | 测试磁盘上不可读的块                                      |

## 用户

|                  |                                        |
| :--------------- | :------------------------------------- |
| id               | 显示活动用户的详细信息，如uid、gid和组 |
| last             | 显示系统中的最后一次登录               |
| who              | 显示谁已登录到系统                     |
| groupadd “admin” | 添加组“admin”                          |
| adduser “Sam”    | 添加用户 Sam                           |
| userdel “Sam”    | 删除用户 Sam                           |
| usermod          | 用于更改/修改用户信息                  |

## 文件

|                                    |                                                  |
| :--------------------------------- | :----------------------------------------------- |
| ls -al                             | 列出文件-包括常规文件和隐藏文件以及它们的权限    |
| pwd                                | 显示当前目录文件路径                             |
| mkdir ‘directory_name’             | 创建一个新目录                                   |
| rm file_name                       | 删除一个文件                                     |
| rm -f filename                     | 强制删除文件                                     |
| rm -r directory_name               | 递归地删除一个目录                               |
| rm -rf directory_name              | 强制并递归地删除一个目录                         |
| cp file1 file2                     | 将file1的内容复制到file2                         |
| cp -r dir1 dir2                    | 递归地将dir1复制到dir2。如果dir2不存在，则创建它 |
| mv file1 file2                     | 将file1重命名为file2                             |
| ln -s /path/to/file_name link_name | 创建到file_name的软链接                          |
| touch file_name                    | 创建一个新文件                                   |
| cat > file_name                    | 从键盘创建一个文件                               |
| more file_name                     | 输出文件的内容                                   |
| head file_name                     | 显示文件的前10行                                 |
| tail file_name                     | 显示文件的最后10行                               |
| gpg -c file_name                   | 加密一个文件                                     |
| gpg file_name.gpg                  | 解密文件                                         |
| wc                                 | 打印文件中的字节、单词和行数                     |
| xargs                              | 从标准输入执行命令                               |

## 进程

|                         |                                      |
| :---------------------- | :----------------------------------- |
| ps                      | 显示当前活动的进程                   |
| ps aux \| grep ‘telnet’ | 搜索进程’telnet’的id                 |
| pmap                    | 显示进程的内存映射                   |
| top                     | 显示所有正在运行的进程               |
| kill pid                | 使用给定的pid终止进程                |
| killall proc            | 杀死/终止所有名为proc的进程          |
| pkill process-name      | 向具有其名称的进程发送信号           |
| bg                      | 将一个在后台暂停的命令，变成继续执行 |
| fg                      | 将后台中的命令调至前台继续运行       |
| fg n                    | job n to the foreground              |
| lsof                    | 列出进程打开的文件                   |
| renice 19 PID           | 使进程以非常低的优先级运行           |
| pgrep firefox           | 查找Firefox进程ID                    |
| pstree                  | 在树模型中可视化过程                 |

## 文件权限

|                                        |                                                              |
| :------------------------------------- | :----------------------------------------------------------- |
| chmod octal filename                   | 将文件权限更改为八进制                                       |
| chmod 777 /data/test.c                 | 将rwx权限设置为owner、group和everyone(其他可以访问服务器的人) |
| chmod 755 /data/test.c                 | 将rwx设置为所有者，将r_x设置为组和所有人                     |
| chmod 766 /data/test.c                 | 为所有者设置rwx，为组和每个人设置rw                          |
| chown owner user-file                  | 更改文件的所有权                                             |
| chown owner-user:owner-group file_name | 更改文件的所有者和组所有者                                   |
| chown owner-user:owner-group directory | 更改目录的所有者和组所有者                                   |

## 网络

|                                        |                                                 |
| :------------------------------------- | :---------------------------------------------- |
| ip addr show                           | 显示IP地址和所有网络接口                        |
| ip address add 192.168.0.1/24 dev eth0 | 将IP地址192.168.0.1分配给接口eth0               |
| ifconfig                               | 显示所有网络接口的IP地址                        |
| ping host                              | ping命令发送ICMP回送请求以建立到服务器/PC的连接 |
| whois domain                           | 检索有关域名的更多信息                          |
| dig domain                             | 检索关于域的DNS信息                             |
| dig -x host                            | 对域执行反向查找                                |
| host google.com                        | 执行域名的IP查找                                |
| hostname -i                            | 显示本地IP地址                                  |
| wget file_name                         | 从在线资源下载文件                              |
| netstat -pnltu                         | 显示所有活动监听端口                            |

## 压缩/打包

|                                     |                                         |
| :---------------------------------- | :-------------------------------------- |
| tar -cf home.tar home<:code>        | 创建名为“home”的存档文件。tar文件’home' |
| tar -xf files.tar                   | 解压档案文件“files.tar”                 |
| tar -zcvf home.tar.gz source-folder | 从源文件夹创建压缩的tar存档文件         |
| gzip file                           | 压缩扩展名为.gz的文件                   |

## 安装包

|                      |                       |
| :------------------- | :-------------------- |
| rpm -i pkg_name.rpm  | 安装rpm包             |
| rpm -e pkg_name      | 删除rpm包             |
| dnf install pkg_name | 使用dnf工具安装软件包 |

## 安装源(编译)

|              |                                                              |
| :----------- | :----------------------------------------------------------- |
| ./configure  | 检查系统，以获得构建程序所需的软件。它将构建包含有效构建项目所需的指令的Makefile |
| make         |                                                              |
| make install | 编译后，该命令将二进制文件安装在默认/修改的路径中            |

## 搜索

|                           |                                                       |
| :------------------------ | :---------------------------------------------------- |
| grep ‘pattern’ files      | 在文件中搜索给定的模式                                |
| grep -r pattern dir       | Search recursively for a pattern in a given directory |
| locate file               | 查找文件的所有实例                                    |
| find /home/ -name “index” | 在/home文件夹中查找以’index’开头的文件名              |
| find /home -size +10000k  | 在主文件夹中查找大于10000k的文件                      |

## 登陆

|                              |                                 |
| :--------------------------- | :------------------------------ |
| ssh user@host                | 使用指定用户安全连接到主机      |
| ssh -p port_number user@host | 使用指定端口安全地连接到主机    |
| ssh host                     | 通过SSH默认端口22安全连接到系统 |
| telnet host                  | 通过telnet默认端口23连接到主机  |

## 文件传输

|                              |                                               |
| :--------------------------- | :-------------------------------------------- |
| scp file1.txt server2/tmp    | 安全地将file1.txt复制到/tmp目录中的server2    |
| rsync -a /home/apps /backup/ | 将/home/apps目录中的内容与/backup目录进行同步 |

## 磁盘使用情况

|                               |                                              |
| :---------------------------- | :------------------------------------------- |
| df -h                         | 显示安装系统上的空闲空间                     |
| df -i                         | 显示文件系统上的空闲inode                    |
| fdisk -l                      | 显示磁盘分区、大小和类型                     |
| du -sh                        | 以人类可读的格式显示当前目录中的磁盘使用情况 |
| findmnt                       | 显示所有文件系统的目标挂载点                 |
| mount device-path mount-point | 挂载设备                                     |

## 目录遍历

|          |                            |
| :------- | :------------------------- |
| cd ..    | 在目录树结构中向上移动一层 |
| cd       | 将目录更改为$HOME目录      |
| cd /test | 将目录更改为/test目录      |



# Linux 命令大全

| Linux 命令大全                                               |                                                              |                                                              |                                                              |
| :----------------------------------------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| **1、文件管理**                                              |                                                              |                                                              |                                                              |
| [cat](https://www.runoob.com/linux/linux-comm-cat.html)      | [chattr](https://www.runoob.com/linux/linux-comm-chattr.html) | [chgrp](https://www.runoob.com/linux/linux-comm-chgrp.html)  | [chmod](https://www.runoob.com/linux/linux-comm-chmod.html)  |
| [chown](https://www.runoob.com/linux/linux-comm-chown.html)  | [cksum](https://www.runoob.com/linux/linux-comm-cksum.html)  | [cmp](https://www.runoob.com/linux/linux-comm-cmp.html)      | [diff](https://www.runoob.com/linux/linux-comm-diff.html)    |
| [diffstat](https://www.runoob.com/linux/linux-comm-diffstat.html) | [file](https://www.runoob.com/linux/linux-comm-file.html)    | [find](https://www.runoob.com/linux/linux-comm-find.html)    | [git](https://www.runoob.com/linux/linux-comm-git.html)      |
| [gitview](https://www.runoob.com/linux/linux-comm-gitview.html) | [indent](https://www.runoob.com/linux/linux-comm-indent.html) | [cut](https://www.runoob.com/linux/linux-comm-cut.html)      | [ln](https://www.runoob.com/linux/linux-comm-ln.html)        |
| [less](https://www.runoob.com/linux/linux-comm-less.html)    | [locate](https://www.runoob.com/linux/linux-comm-locate.html) | [lsattr](https://www.runoob.com/linux/linux-comm-lsattr.html) | [mattrib](https://www.runoob.com/linux/linux-comm-mattrib.html) |
| [mc](https://www.runoob.com/linux/linux-comm-mc.html)        | [mdel](https://www.runoob.com/linux/linux-comm-mdel.html)    | [mdir](https://www.runoob.com/linux/linux-comm-mdir.html)    | [mktemp](https://www.runoob.com/linux/linux-comm-mktemp.html) |
| [more](https://www.runoob.com/linux/linux-comm-more.html)    | [mmove](https://www.runoob.com/linux/linux-comm-mmove.html)  | [mread](https://www.runoob.com/linux/linux-comm-mread.html)  | [mren](https://www.runoob.com/linux/linux-comm-mren.html)    |
| [mtools](https://www.runoob.com/linux/linux-comm-mtools.html) | [mtoolstest](https://www.runoob.com/linux/linux-comm-mtoolstest.html) | [mv](https://www.runoob.com/linux/linux-comm-mv.html)        | [od](https://www.runoob.com/linux/linux-comm-od.html)        |
| [paste](https://www.runoob.com/linux/linux-comm-paste.html)  | [patch](https://www.runoob.com/linux/linux-comm-patch.html)  | [rcp](https://www.runoob.com/linux/linux-comm-rcp.html)      | [rm](https://www.runoob.com/linux/linux-comm-rm.html)        |
| [slocate](https://www.runoob.com/linux/linux-comm-slocate.html) | [split](https://www.runoob.com/linux/linux-comm-split.html)  | [tee](https://www.runoob.com/linux/linux-comm-tee.html)      | [tmpwatch](https://www.runoob.com/linux/linux-comm-tmpwatch.html) |
| [touch](https://www.runoob.com/linux/linux-comm-touch.html)  | [umask](https://www.runoob.com/linux/linux-comm-umask.html)  | [which](https://www.runoob.com/linux/linux-comm-which.html)  | [cp](https://www.runoob.com/linux/linux-comm-cp.html)        |
| [whereis](https://www.runoob.com/linux/linux-comm-whereis.html) | [mcopy](https://www.runoob.com/linux/linux-comm-mcopy.html)  | [mshowfat](https://www.runoob.com/linux/linux-comm-mshowfat.html) | [rhmask](https://www.runoob.com/linux/linux-comm-rhmask.html) |
| [scp](https://www.runoob.com/linux/linux-comm-scp.html)      | [awk](https://www.runoob.com/linux/linux-comm-awk.html)      | [read](https://www.runoob.com/linux/linux-comm-read.html)    | [updatedb](https://www.runoob.com/linux/linux-comm-updatedb.html) |
| **2、文档编辑**                                              |                                                              |                                                              |                                                              |
| [col](https://www.runoob.com/linux/linux-comm-col.html)      | [colrm](https://www.runoob.com/linux/linux-comm-colrm.html)  | [comm](https://www.runoob.com/linux/linux-comm-comm.html)    | [csplit](https://www.runoob.com/linux/linux-comm-csplit.html) |
| [ed](https://www.runoob.com/linux/linux-comm-ed.html)        | [egrep](https://www.runoob.com/linux/linux-comm-egrep.html)  | [ex](https://www.runoob.com/linux/linux-comm-ex.html)        | [fgrep](https://www.runoob.com/linux/linux-comm-fgrep.html)  |
| [fmt](https://www.runoob.com/linux/linux-comm-fmt.html)      | [fold](https://www.runoob.com/linux/linux-comm-fold.html)    | [grep](https://www.runoob.com/linux/linux-comm-grep.html)    | [ispell](https://www.runoob.com/linux/linux-comm-ispell.html) |
| [jed](https://www.runoob.com/linux/linux-comm-jed.html)      | [joe](https://www.runoob.com/linux/linux-comm-joe.html)      | [join](https://www.runoob.com/linux/linux-comm-join.html)    | [look](https://www.runoob.com/linux/linux-comm-look.html)    |
| [mtype](https://www.runoob.com/linux/linux-comm-mtype.html)  | [pico](https://www.runoob.com/linux/linux-comm-pico.html)    | [rgrep](https://www.runoob.com/linux/linux-comm-rgrep.html)  | [sed](https://www.runoob.com/linux/linux-comm-sed.html)      |
| [sort](https://www.runoob.com/linux/linux-comm-sort.html)    | [spell](https://www.runoob.com/linux/linux-comm-spell.html)  | [tr](https://www.runoob.com/linux/linux-comm-tr.html)        | [expr](https://www.runoob.com/linux/linux-comm-expr.html)    |
| [uniq](https://www.runoob.com/linux/linux-comm-uniq.html)    | [wc](https://www.runoob.com/linux/linux-comm-wc.html)        | [let](https://www.runoob.com/linux/linux-comm-let.html)      |                                                              |
| **3、文件传输**                                              |                                                              |                                                              |                                                              |
| [lprm](https://www.runoob.com/linux/linux-comm-lprm.html)    | [lpr](https://www.runoob.com/linux/linux-comm-lpr.html)      | [lpq](https://www.runoob.com/linux/linux-comm-lpq.html)      | [lpd](https://www.runoob.com/linux/linux-comm-lpd.html)      |
| [bye](https://www.runoob.com/linux/linux-comm-bye.html)      | [ftp](https://www.runoob.com/linux/linux-comm-ftp.html)      | [uuto](https://www.runoob.com/linux/linux-comm-uuto.html)    | [uupick](https://www.runoob.com/linux/linux-comm-uupick.html) |
| [uucp](https://www.runoob.com/linux/linux-comm-uucp.html)    | [uucico](https://www.runoob.com/linux/linux-comm-uucico.html) | [tftp](https://www.runoob.com/linux/linux-comm-tftp.html)    | [ncftp](https://www.runoob.com/linux/linux-comm-ncftp.html)  |
| [ftpshut](https://www.runoob.com/linux/linux-comm-ftpshut.html) | [ftpwho](https://www.runoob.com/linux/linux-comm-ftpwho.html) | [ftpcount](https://www.runoob.com/linux/linux-comm-ftpcount.html) |                                                              |
| **4、磁盘管理**                                              |                                                              |                                                              |                                                              |
| [cd](https://www.runoob.com/linux/linux-comm-cd.html)        | [df](https://www.runoob.com/linux/linux-comm-df.html)        | [dirs](https://www.runoob.com/linux/linux-comm-dirs.html)    | [du](https://www.runoob.com/linux/linux-comm-du.html)        |
| [edquota](https://www.runoob.com/linux/linux-comm-edquota.html) | [eject](https://www.runoob.com/linux/linux-comm-eject.html)  | [mcd](https://www.runoob.com/linux/linux-comm-mcd.html)      | [mdeltree](https://www.runoob.com/linux/linux-comm-mdeltree.html) |
| [mdu](https://www.runoob.com/linux/linux-comm-mdu.html)      | [mkdir](https://www.runoob.com/linux/linux-comm-mkdir.html)  | [mlabel](https://www.runoob.com/linux/linux-comm-mlabel.html) | [mmd](https://www.runoob.com/linux/linux-comm-mmd.html)      |
| [mrd](https://www.runoob.com/linux/linux-comm-mrd.html)      | [mzip](https://www.runoob.com/linux/linux-comm-mzip.html)    | [pwd](https://www.runoob.com/linux/linux-comm-pwd.html)      | [quota](https://www.runoob.com/linux/linux-comm-quota.html)  |
| [mount](https://www.runoob.com/linux/linux-comm-mount.html)  | [mmount](https://www.runoob.com/linux/linux-comm-mmount.html) | [rmdir](https://www.runoob.com/linux/linux-comm-rmdir.html)  | [rmt](https://www.runoob.com/linux/linux-comm-rmt.html)      |
| [stat](https://www.runoob.com/linux/linux-comm-stat.html)    | [tree](https://www.runoob.com/linux/linux-comm-tree.html)    | [umount](https://www.runoob.com/linux/linux-comm-umount.html) | [ls](https://www.runoob.com/linux/linux-comm-ls.html)        |
| [quotacheck](https://www.runoob.com/linux/linux-comm-quotacheck.html) | [quotaoff](https://www.runoob.com/linux/linux-comm-quotaoff.html) | [lndir](https://www.runoob.com/linux/linux-comm-lndir.html)  | [repquota](https://www.runoob.com/linux/linux-comm-repquota.html) |
| [quotaon](https://www.runoob.com/linux/linux-comm-quotaon.html) |                                                              |                                                              |                                                              |
| **5、磁盘维护**                                              |                                                              |                                                              |                                                              |
| [badblocks](https://www.runoob.com/linux/linux-comm-badblocks.html) | [cfdisk](https://www.runoob.com/linux/linux-comm-cfdisk.html) | [dd](https://www.runoob.com/linux/linux-comm-dd.html)        | [e2fsck](https://www.runoob.com/linux/linux-comm-e2fsck.html) |
| [ext2ed](https://www.runoob.com/linux/linux-comm-ext2ed.html) | [fsck](https://www.runoob.com/linux/linux-comm-fsck.html)    | [fsck.minix](https://www.runoob.com/linux/linux-comm-fsck-minix.html) | [fsconf](https://www.runoob.com/linux/linux-comm-fsconf.html) |
| [fdformat](https://www.runoob.com/linux/linux-comm-fdformat.html) | [hdparm](https://www.runoob.com/linux/linux-comm-hdparm.html) | [mformat](https://www.runoob.com/linux/linux-comm-mformat.html) | [mkbootdisk](https://www.runoob.com/linux/linux-comm-mkbootdisk.html) |
| [mkdosfs](https://www.runoob.com/linux/linux-comm-mkdosfs.html) | [mke2fs](https://www.runoob.com/linux/linux-comm-mke2fs.html) | [mkfs.ext2](https://www.runoob.com/linux/linux-comm-mkfs-ext2.html) | [mkfs.msdos](https://www.runoob.com/linux/linux-comm-mkfs-msdos.html) |
| [mkinitrd](https://www.runoob.com/linux/linux-comm-mkinitrd.html) | [mkisofs](https://www.runoob.com/linux/linux-comm-mkisofs.html) | [mkswap](https://www.runoob.com/linux/linux-comm-mkswap.html) | [mpartition](https://www.runoob.com/linux/linux-comm-mpartition.html) |
| [swapon](https://www.runoob.com/linux/linux-comm-swapon.html) | [symlinks](https://www.runoob.com/linux/linux-comm-symlinks.html) | [sync](https://www.runoob.com/linux/linux-comm-sync.html)    | [mbadblocks](https://www.runoob.com/linux/linux-comm-mbadblocks.html) |
| [mkfs.minix](https://www.runoob.com/linux/linux-comm-mkfs-minix.html) | [fsck.ext2](https://www.runoob.com/linux/linux-comm-fsck-ext2.html) | [fdisk](https://www.runoob.com/linux/linux-comm-fdisk.html)  | [losetup](https://www.runoob.com/linux/linux-comm-losetup.html) |
| [mkfs](https://www.runoob.com/linux/linux-comm-mkfs.html)    | [sfdisk](https://www.runoob.com/linux/linux-comm-sfdisk.html) | [swapoff](https://www.runoob.com/linux/linux-comm-swapoff.html) |                                                              |
| **6、网络通讯**                                              |                                                              |                                                              |                                                              |
| [apachectl](https://www.runoob.com/linux/linux-comm-apachectl.html) | [arpwatch](https://www.runoob.com/linux/linux-comm-arpwatch.html) | [dip](https://www.runoob.com/linux/linux-comm-dip.html)      | [getty](https://www.runoob.com/linux/linux-comm-getty.html)  |
| [mingetty](https://www.runoob.com/linux/linux-comm-mingetty.html) | [uux](https://www.runoob.com/linux/linux-comm-uux.html)      | [telnet](https://www.runoob.com/linux/linux-comm-telnet.html) | [uulog](https://www.runoob.com/linux/linux-comm-uulog.html)  |
| [uustat](https://www.runoob.com/linux/linux-comm-uustat.html) | [ppp-off](https://www.runoob.com/linux/linux-comm-ppp-off.html) | [netconfig](https://www.runoob.com/linux/linux-comm-netconfig.html) | [nc](https://www.runoob.com/linux/linux-comm-nc.html)        |
| [httpd](https://www.runoob.com/linux/linux-comm-httpd.html)  | [ifconfig](https://www.runoob.com/linux/linux-comm-ifconfig.html) | [minicom](https://www.runoob.com/linux/linux-comm-minicom.html) | [mesg](https://www.runoob.com/linux/linux-comm-mesg.html)    |
| [dnsconf](https://www.runoob.com/linux/linux-comm-dnsconf.html) | [wall](https://www.runoob.com/linux/linux-comm-wall.html)    | [netstat](https://www.runoob.com/linux/linux-comm-netstat.html) | [ping](https://www.runoob.com/linux/linux-comm-ping.html)    |
| [pppstats](https://www.runoob.com/linux/linux-comm-pppstats.html) | [samba](https://www.runoob.com/linux/linux-comm-samba.html)  | [setserial](https://www.runoob.com/linux/linux-comm-setserial.html) | [talk](https://www.runoob.com/linux/linux-comm-talk.html)    |
| [traceroute](https://www.runoob.com/linux/linux-comm-traceroute.html) | [tty](https://www.runoob.com/linux/linux-comm-tty.html)      | [newaliases](https://www.runoob.com/linux/linux-comm-newaliases.html) | [uuname](https://www.runoob.com/linux/linux-comm-uuname.html) |
| [netconf](https://www.runoob.com/linux/linux-comm-netconf.html) | [write](https://www.runoob.com/linux/linux-comm-write.html)  | [statserial](https://www.runoob.com/linux/linux-comm-statserial.html) | [efax](https://www.runoob.com/linux/linux-comm-efax.html)    |
| [pppsetup](https://www.runoob.com/linux/linux-comm-pppsetup.html) | [tcpdump](https://www.runoob.com/linux/linux-comm-tcpdump.html) | [ytalk](https://www.runoob.com/linux/linux-comm-ytalk.html)  | [cu](https://www.runoob.com/linux/linux-comm-cu.html)        |
| [smbd](https://www.runoob.com/linux/linux-comm-smbd.html)    | [testparm](https://www.runoob.com/linux/linux-comm-testparm.html) | [smbclient](https://www.runoob.com/linux/linux-comm-smbclient.html) | [shapecfg](https://www.runoob.com/linux/linux-comm-shapecfg.html) |
| **7、系统管理**                                              |                                                              |                                                              |                                                              |
| [adduser](https://www.runoob.com/linux/linux-comm-adduser.html) | [chfn](https://www.runoob.com/linux/linux-comm-chfn.html)    | [useradd](https://www.runoob.com/linux/linux-comm-useradd.html) | [date](https://www.runoob.com/linux/linux-comm-date.html)    |
| [exit](https://www.runoob.com/linux/linux-comm-exit.html)    | [finger](https://www.runoob.com/linux/linux-comm-finger.html) | [fwhios](https://www.runoob.com/linux/linux-comm-fwhios.html) | [sleep](https://www.runoob.com/linux/linux-comm-sleep.html)  |
| [suspend](https://www.runoob.com/linux/linux-comm-suspend.html) | [groupdel](https://www.runoob.com/linux/linux-comm-groupdel.html) | [groupmod](https://www.runoob.com/linux/linux-comm-groupmod.html) | [halt](https://www.runoob.com/linux/linux-comm-halt.html)    |
| [kill](https://www.runoob.com/linux/linux-comm-kill.html)    | [last](https://www.runoob.com/linux/linux-comm-last.html)    | [lastb](https://www.runoob.com/linux/linux-comm-lastb.html)  | [login](https://www.runoob.com/linux/linux-comm-login.html)  |
| [logname](https://www.runoob.com/linux/linux-comm-logname.html) | [logout](https://www.runoob.com/linux/linux-comm-logout.html) | [ps](https://www.runoob.com/linux/linux-comm-ps.html)        | [nice](https://www.runoob.com/linux/linux-comm-nice.html)    |
| [procinfo](https://www.runoob.com/linux/linux-comm-procinfo.html) | [top](https://www.runoob.com/linux/linux-comm-top.html)      | [pstree](https://www.runoob.com/linux/linux-comm-pstree.html) | [reboot](https://www.runoob.com/linux/linux-comm-reboot.html) |
| [rlogin](https://www.runoob.com/linux/linux-comm-rlogin.html) | [rsh](https://www.runoob.com/linux/linux-comm-rsh.html)      | [sliplogin](https://www.runoob.com/linux/linux-comm-sliplogin.html) | [screen](https://www.runoob.com/linux/linux-comm-screen.html) |
| [shutdown](https://www.runoob.com/linux/linux-comm-shutdown.html) | [rwho](https://www.runoob.com/linux/linux-comm-rwho.html)    | [sudo](https://www.runoob.com/linux/linux-comm-sudo.html)    | [gitps](https://www.runoob.com/linux/linux-comm-gitps.html)  |
| [swatch](https://www.runoob.com/linux/linux-comm-swatch.html) | [tload](https://www.runoob.com/linux/linux-comm-tload.html)  | [logrotate](https://www.runoob.com/linux/linux-comm-logrotate.html) | [uname](https://www.runoob.com/linux/linux-comm-uname.html)  |
| [chsh](https://www.runoob.com/linux/linux-comm-chsh.html)    | [userconf](https://www.runoob.com/linux/linux-comm-userconf.html) | [userdel](https://www.runoob.com/linux/linux-comm-userdel.html) | [usermod](https://www.runoob.com/linux/linux-comm-usermod.html) |
| [vlock](https://www.runoob.com/linux/linux-comm-vlock.html)  | [who](https://www.runoob.com/linux/linux-comm-who.html)      | [whoami](https://www.runoob.com/linux/linux-comm-whoami.html) | [whois](https://www.runoob.com/linux/linux-comm-whois.html)  |
| [newgrp](https://www.runoob.com/linux/linux-comm-newgrp.html) | [renice](https://www.runoob.com/linux/linux-comm-renice.html) | [su](https://www.runoob.com/linux/linux-comm-su.html)        | [skill](https://www.runoob.com/linux/linux-comm-skill.html)  |
| [w](https://www.runoob.com/linux/linux-comm-w.html)          | [id](https://www.runoob.com/linux/linux-comm-id.html)        | [groupadd](https://www.runoob.com/linux/linux-comm-groupadd.html) | [free](https://www.runoob.com/linux/linux-comm-free.html)    |
| **8、系统设置**                                              |                                                              |                                                              |                                                              |
| [reset](https://www.runoob.com/linux/linux-comm-reset.html)  | [clear](https://www.runoob.com/linux/linux-comm-clear.html)  | [alias](https://www.runoob.com/linux/linux-comm-alias.html)  | [dircolors](https://www.runoob.com/linux/linux-comm-dircolors.html) |
| [aumix](https://www.runoob.com/linux/linux-comm-aumix.html)  | [bind](https://www.runoob.com/linux/linux-comm-bind.html)    | [chroot](https://www.runoob.com/linux/linux-comm-chroot.html) | [clock](https://www.runoob.com/linux/linux-comm-clock.html)  |
| [crontab](https://www.runoob.com/linux/linux-comm-crontab.html) | [declare](https://www.runoob.com/linux/linux-comm-declare.html) | [depmod](https://www.runoob.com/linux/linux-comm-depmod.html) | [dmesg](https://www.runoob.com/linux/linux-comm-dmesg.html)  |
| [enable](https://www.runoob.com/linux/linux-comm-enable.html) | [eval](https://www.runoob.com/linux/linux-comm-eval.html)    | [export](https://www.runoob.com/linux/linux-comm-export.html) | [pwunconv](https://www.runoob.com/linux/linux-comm-pwunconv.html) |
| [grpconv](https://www.runoob.com/linux/linux-comm-grpconv.html) | [rpm](https://www.runoob.com/linux/linux-comm-rpm.html)      | [insmod](https://www.runoob.com/linux/linux-comm-insmod.html) | [kbdconfig](https://www.runoob.com/linux/linux-comm-kbdconfig.html) |
| [lilo](https://www.runoob.com/linux/linux-comm-lilo.html)    | [liloconfig](https://www.runoob.com/linux/linux-comm-liloconfig.html) | [lsmod](https://www.runoob.com/linux/linux-comm-lsmod.html)  | [minfo](https://www.runoob.com/linux/linux-comm-minfo.html)  |
| [set](https://www.runoob.com/linux/linux-comm-set.html)      | [modprobe](https://www.runoob.com/linux/linux-comm-modprobe.html) | [ntsysv](https://www.runoob.com/linux/linux-comm-ntsysv.html) | [mouseconfig](https://www.runoob.com/linux/linux-comm-mouseconfig.html) |
| [passwd](https://www.runoob.com/linux/linux-comm-passwd.html) | [pwconv](https://www.runoob.com/linux/linux-comm-pwconv.html) | [rdate](https://www.runoob.com/linux/linux-comm-rdate.html)  | [resize](https://www.runoob.com/linux/linux-comm-resize.html) |
| [rmmod](https://www.runoob.com/linux/linux-comm-rmmod.html)  | [grpunconv](https://www.runoob.com/linux/linux-comm-grpunconv.html) | [modinfo](https://www.runoob.com/linux/linux-comm-modinfo.html) | [time](https://www.runoob.com/linux/linux-comm-time.html)    |
| [setup](https://www.runoob.com/linux/linux-comm-setup.html)  | [sndconfig](https://www.runoob.com/linux/linux-comm-sndconfig.html) | [setenv](https://www.runoob.com/linux/linux-comm-setenv.html) | [setconsole](https://www.runoob.com/linux/linux-comm-setconsole.html) |
| [timeconfig](https://www.runoob.com/linux/linux-comm-timeconfig.html) | [ulimit](https://www.runoob.com/linux/linux-comm-ulimit.html) | [unset](https://www.runoob.com/linux/linux-comm-unset.html)  | [chkconfig](https://www.runoob.com/linux/linux-comm-chkconfig.html) |
| [apmd](https://www.runoob.com/linux/linux-comm-apmd.html)    | [hwclock](https://www.runoob.com/linux/linux-comm-hwclock.html) | [mkkickstart](https://www.runoob.com/linux/linux-comm-mkkickstart.html) | [fbset](https://www.runoob.com/linux/linux-comm-fbset.html)  |
| [unalias](https://www.runoob.com/linux/linux-comm-unalias.html) | [SVGATextMode](https://www.runoob.com/linux/linux-comm-svgatextmode.html) | [gpasswd](https://www.runoob.com/linux/linux-comm-gpasswd.html) |                                                              |
| **9、备份压缩**                                              |                                                              |                                                              |                                                              |
| [ar](https://www.runoob.com/linux/linux-comm-ar.html)        | [bunzip2](https://www.runoob.com/linux/linux-comm-bunzip2.html) | [bzip2](https://www.runoob.com/linux/linux-comm-bzip2.html)  | [bzip2recover](https://www.runoob.com/linux/linux-comm-bzip2recover.html) |
| [gunzip](https://www.runoob.com/linux/linux-comm-gunzip.html) | [unarj](https://www.runoob.com/linux/linux-comm-unarj.html)  | [compress](https://www.runoob.com/linux/linux-comm-compress.html) | [cpio](https://www.runoob.com/linux/linux-comm-cpio.html)    |
| [dump](https://www.runoob.com/linux/linux-comm-dump.html)    | [uuencode](https://www.runoob.com/linux/linux-comm-uuencode.html) | [gzexe](https://www.runoob.com/linux/linux-comm-gzexe.html)  | [gzip](https://www.runoob.com/linux/linux-comm-gzip.html)    |
| [lha](https://www.runoob.com/linux/linux-comm-lha.html)      | [restore](https://www.runoob.com/linux/linux-comm-restore.html) | [tar](https://www.runoob.com/linux/linux-comm-tar.html)      | [uudecode](https://www.runoob.com/linux/linux-comm-uudecode.html) |
| [unzip](https://www.runoob.com/linux/linux-comm-unzip.html)  | [zip](https://www.runoob.com/linux/linux-comm-zip.html)      | [zipinfo](https://www.runoob.com/linux/linux-comm-zipinfo.html) |                                                              |
| **10、设备管理**                                             |                                                              |                                                              |                                                              |
| [setleds](https://www.runoob.com/linux/linux-comm-setleds.html) | [loadkeys](https://www.runoob.com/linux/linux-comm-loadkeys.html) | [rdev](https://www.runoob.com/linux/linux-comm-rdev.html)    | [dumpkeys](https://www.runoob.com/linux/linux-comm-dumpkeys.html) |
| [MAKEDEV](https://www.runoob.com/linux/linux-comm-makedev.html) | [poweroff](https://www.runoob.com/linux/linux-comm-poweroff.html) |                                                              |                                                              |

------

## 其他命令

- [Linux bc 命令](https://www.runoob.com/linux/linux-comm-bc.html)
- [Linux tail 命令](https://www.runoob.com/linux/linux-comm-tail.html)
- [Linux head 命令](https://www.runoob.com/linux/linux-comm-head.html)
- [Linux xargs 命令](https://www.runoob.com/linux/linux-comm-xargs.html)
- [Linux ip 命令](https://www.runoob.com/linux/linux-comm-ip.html)
- [Linux nohup 命令](https://www.runoob.com/linux/linux-comm-nohup.html)
- [Linux killall 命令](https://www.runoob.com/linux/linux-comm-killall.html)
- [Linux pkill 命令](https://www.runoob.com/linux/linux-comm-pkill.html)

### 扩展文章

- [Linux 常用命令全拼](https://www.runoob.com/w3cnote/linux-command-full-fight.html)