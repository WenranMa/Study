# AWS

AWS Identity and Access Management (IAM) is a web service that helps you securely control access to AWS resources. You use IAM to control who is authenticated (signed in) and authorized (has permissions) to use resources.

## VPC
    虚拟局域网，一个路由下面的一个局域网。
    VPC包含公有子网和私有子网，公有子网可以直接访问公网，但私有子网不能，需要通过NAT，NAT可以理解为路由器(网关)。
    NAT可以用EC2实例来制作。
    AWS也提供了NAT服务（推荐）。

## EC2
    可以理解为虚拟机。
    上线代码方式：推荐Docker

Amazon EC2 is hosted in multiple locations world-wide. These locations are composed of Regions, Availability Zones, and Local Zones. Each Region is a separate geographic area. Each Region has multiple, isolated locations known as Availability Zones. Local Zones provide you the ability to place resources, such as compute and storage, in multiple locations closer to your end users. Resources aren't replicated across Regions unless you specifically choose to do so.

### Region, Availability Zone, and Local Zone Concepts
Each Region is completely independent. Each Availability Zone is isolated, but the Availability Zones in a Region are connected through low-latency links. A Local Zone is an AWS infrastructure deployment that places select services closer to your end users. A Local Zone is an extension of a Region that is in a different location from your Region. It provides a high-bandwidth backbone to the AWS infrastructure and is ideal for latency-sensitive applications, for example machine learning. The following diagram illustrates the relationship between Regions, Availability Zones, and Local Zones.

![Region](./img/aws_regions.png)

An Availability Zone is represented by a Region code followed by a letter identifier; for example, us-east-1a.

| Code |   Name  |  Opt-in Status | Local Zone |
| ---- | ------- | -------------- | ---------- |
| us-east-2 | US East (Ohio) | Not required | No |
| us-east-1 | US East (N. Virginia) | Not required | No |

## RDS
    关系型数据库的管理平台。
    可以选择不同数据库，比如mysql。可以创建主从库，并且有多个从库。
    kingshard中间件，可以管理数据库的主从分离，负载均衡。

## ElastiCache
    缓存系统管理平台。（Memcache）

## ELB
    Elastic Load Balance，可伸缩负载均衡。私有子网中的服务要通过ELB暴露到公网。

## AutoScaling
    自动缩小或扩容的工具。通过管理EC2的启动配置来管理EC2数量。

S3

ROUTE 53

## AWS CLI

