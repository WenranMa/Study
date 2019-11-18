# AWS

AWS Identity and Access Management (IAM) is a web service that helps you securely control access to AWS resources. You use IAM to control who is authenticated (signed in) and authorized (has permissions) to use resources.

### VPC
    虚拟局域网，一个路由下面的一个局域网。
    VPC包含公有子网和私有子网，公有子网可以直接访问公网，但私有子网不能，需要通过NAT，NAT可以理解为路由器(网关)。
    NAT可以用EC2实例来制作。
    AWS也提供了NAT服务（推荐）。

### EC2
    可以理解为虚拟机。
    上线代码方式：推荐Docker

### RDS
    关系型数据库的管理平台。
    可以选择不同数据库，比如mysql。可以创建主从库，并且有多个从库。
    kingshard中间件，可以管理数据库的主从分离，负载均衡。

### ElastiCache
    缓存系统管理平台。（Memcache）

### ELB
    Elastic Load Balance，可伸缩负载均衡。私有子网中的服务要通过ELB暴露到公网。

### AutoScaling
    自动缩小或扩容的工具。通过管理EC2的启动配置来管理EC2数量。

S3

ROUTE 53