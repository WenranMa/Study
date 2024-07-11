1、Ansible是什么？
Ansible是一个自动化运维工具，基于Python开发，集合了众多运维工具的优点，可以实现批量系统配置、批量程序部署、批量运行命令等功能。并且它是基于模块工作的，本身没有批量部署的能力，真正批量部署的是ansible所运行的模块，而ansible只是提供一种框架。

2、Ansible常用模块（至少6个）？
command ping yum copy service shell file replace user group

3、什么是 Ansible 模块？
模块被认为是 Ansible 的工作单元。每个模块大多是独立的，可以用标准的脚本语言编写，如 Python、Perl、Ruby、bash 等。模块的一个重要属性是幂等性，意味着一个操作执行多次不会产生副作用。

4、什么是 Ansible 的 playbooks ？
Playbooks 是 Ansible 的配置、部署和编排语言，它是基于YAML语言编写的。他们可以描述您希望远程系统实施的策略，或者描述一般 IT 流程中的一系列步骤。

5、描述Ansible是如何工作的？
Ansible由节点和控制机器组成。 控制机器是安装Ansibles的地方，节点由这些机器通过SSH管理。 借助SSH协议，控制机器可以部署临时存储在远程节点上的模块。
控制机器使用ansible或者ansible-playbooks在服务器终端输入的Ansible命令集或者playbook后，Ansible会遵循预先编排的规则将PLAYbook逐条拆解为Play，再将Play组织成Ansible可以识别的任务tasks，随后调用任务涉及到的所有MODULES及PLUGINS，根据主机清单INVENTORY中定义的主机列表通过SSH协议将任务集以临时文件或者命令的形式传输到远程节点并返回结果，如果是临时文件则执行完毕后自动删除。

练习题：

1、ansible使用copy模块来将/opt/aa.txt复制到/home/jack中
ansible node1 -m copy -a 'src=/opt/aa.txt dest=/home/jack/'

[root@manager ~]# ansible node1 -m copy -a 'src=/opt/aa.txt dest=/home/jack/'
node1 | CHANGED => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python"
    }, 
    "changed": true, 
    "checksum": "da39a3ee5e6b4b0d3255bfef95601890afd80709", 
    "dest": "/home/jack/aa.txt", 
    "gid": 0, 
    "group": "root", 
    "md5sum": "d41d8cd98f00b204e9800998ecf8427e", 
    "mode": "0644", 
    "owner": "root", 
    "size": 0, 
    "src": "/root/.ansible/tmp/ansible-tmp-1592384605.11-1992-33979510717979/source", 
    "state": "file", 
    "uid": 0
}
[root@manager ~]# ansible node1 -a 'ls -l /home/jack'
node1 | CHANGED | rc=0 >>
总用量 0
-rw-r--r-- 1 root root 0 6月  17 17:03 aa.txt
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
2、使用file模块，来定义/home/jack/aa.txt的权限为777，归属为所有者是jack，所属组为jack
ansible node1 -m file -a 'path=/home/jack/aa.txt owner=jack group=jack mode=0777’

[root@manager ~]# ansible node1 -m file -a 'path=/home/jack/aa.txt owner=jack group=jack mode=0777'
node1 | CHANGED => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python"
    }, 
    "changed": true, 
    "gid": 1001, 
    "group": "jack", 
    "mode": "0777", 
    "owner": "jack", 
    "path": "/home/jack/aa.txt", 
    "size": 0, 
    "state": "file", 
    "uid": 1001
}
[root@manager ~]# ansible node1 -a 'ls -l /home/jack'
node1 | CHANGED | rc=0 >>
总用量 0
-rwxrwxrwx 1 jack jack 0 6月  17 17:03 aa.txt
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
3、使用yum模块，安装httpd服务
ansible node1 -m yum -a 'name=httpd state=present’

[root@manager ~]# ansible node1 -m yum -a 'name=httpd state=present'

node1 | CHANGED => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python"
    }, 
    "changed": true, 
    "changes": {
        "installed": [
            "httpd"
        ]
    }, 
    "msg": "Repository base is listed more than once in the configuration\n", 
    "rc": 0, 
    "results": [
        "Loaded plugins: fastestmirror\nLoading mirror speeds from cached hostfile\n * base: mirrors.aliyun.com\n * epel: mirrors.yun-idc.com\n * extras: mirrors.aliyun.com\n * updates: mirrors.aliyun.com\nResolving Dependencies\n--> Running transaction check\n---> Package httpd.x86_64 0:2.4.6-93.el7.centos will be installed\n--> Finished Dependency Resolution\n\nDependencies Resolved\n\n================================================================================\n Package       Arch           Version                        Repository    Size\n================================================================================\nInstalling:\n httpd         x86_64         2.4.6-93.el7.centos            base         2.7 M\n\nTransaction Summary\n================================================================================\nInstall  1 Package\n\nTotal download size: 2.7 M\nInstalled size: 9.4 M\nDownloading packages:\nRunning transaction check\nRunning transaction test\nTransaction test succeeded\nRunning transaction\n  Installing : httpd-2.4.6-93.el7.centos.x86_64                             1/1 \n  Verifying  : httpd-2.4.6-93.el7.centos.x86_64                             1/1 \n\nInstalled:\n  httpd.x86_64 0:2.4.6-93.el7.centos                                            \n\nComplete!\n"
    ]
}
[root@manager ~]# 
[root@manager ~]# ansible node1 -a 'rpm -q httpd'
[WARNING]: Consider using the yum, dnf or zypper module rather than running 'rpm'.
If you need to use command because yum, dnf or zypper is insufficient you can add
'warn: false' to this command task or set 'command_warnings=False' in ansible.cfg
to get rid of this message.
node1 | CHANGED | rc=0 >>
httpd-2.4.6-93.el7.centos.x86_64
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
4、使用cron模块，定义一个任务，每周五的14点30分执行备份/var
ansible node1 -m cron -a 'name=“crontab test” weekday=5 hour=14 minute=30 job="/usr/bin/tar -czf /opt/var.tar.gz /var"'

[root@manager ~]# ansible node1 -m cron -a 'name="crontab test" weekday=5 hour=14 minute=30 job="/usr/bin/tar -czf /opt/var.tar.gz /var"'
node1 | CHANGED => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python"
    }, 
    "changed": true, 
    "envs": [], 
    "jobs": [
        "crontab test"
    ]
}
1
2
3
4
5
6
7
8
9
10
11
5、使用user模块，创建用户student，让其是系统用户，属组为root,uid为2000
ansible node1 -m user -a 'name=student system=yes group=root uid=2000’

[root@manager ~]# ansible node1 -m user -a 'name=student system=yes group=root uid=2000'
node1 | CHANGED => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python"
    }, 
    "changed": true, 
    "comment": "", 
    "create_home": true, 
    "group": 0, 
    "home": "/home/student", 
    "name": "student", 
    "shell": "/bin/bash", 
    "state": "present", 
    "system": true, 
    "uid": 2000
}
[root@manager ~]# ansible node1 -m shell -a 'id student'
node1 | CHANGED | rc=0 >>
uid=2000(student) gid=0(root) 组=0(root)
)
