## Kafka
是流处理平台，可以发布和订阅，类似消息队列。
模式：生产者 - 数据流 - 消费者
存储：数据和日志

---

## Docker

Docker不是虚拟机。但可以理解为轻量的虚拟机，把一个应用程序放在一个独立的环境里运行。

![Docker Architecture](../img/architecture_docker.svg)

- 例子：

`docker run ubuntu echo hello docker` 是用一个Ubuntu镜像运行ehco hello docker命令。

`docker run nginx` 启动一个nginx容器。

- docker命令：
`docker pull` 获取image。

`docker build` 创建image。

`docker images` 可以看本地所有镜像。

`docker run` 启动container。

`docker ps` 可以查看运行中的container。

`docker stop [container id]` 来停止容器。

`docker rmi` 删除image。

`docker rm` 删除container。

`docker cp` 在host和container之间拷贝文件。

`docker commit` 保存改动为新的image。

---

## K8s

---

## Elastic Stack
#### Elasticsearch 

- 依赖JDK. 
- 配置文件位于config/elasticsearch.yml
- jvm.options 用于修改jvm相关参数如内存大小等。
- log4j2.properties 日志先关配置

本地启动集群方式：

- `bin/elasticsearch`
- `bin/elasticsearch -Ehttp.prot=8200 -Epath.data=node2`
- `bin/elasticsearch -Ehttp.prot=7200 -Epath.data=node3`

常用术语：

- Document 文档数据（一条数据）
- Index 索引(类似数据库)
- Type 索引中的数据类型（类似Table）
- Field 字段，文档属性
- Query DSL 查询语言

#### Kibana
配置config/kibana.yml
bin/kibana运行

#### Beats 
Light Weight Data Shipper

- FileBeat 日志文件
- Metricbeat 收集度量数据
- Packetbeat 网络数据
- Heartbeat 健康检查

beat属于数据起始端，用于收集数据，存储于elasticsearch，最后用kibana展示。

#### Logstash
Data Shipper







