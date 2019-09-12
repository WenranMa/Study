
# Elastic Stack

### Logstash
Data Shipper



### Elasticsearch 

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

### Kibana
配置config/kibana.yml
bin/kibana运行

#### Beats 
Light Weight Data Shipper

- FileBeat 日志文件
- Metricbeat 收集度量数据
- Packetbeat 网络数据
- Heartbeat 健康检查

beat属于数据起始端，用于收集数据，存储于elasticsearch，最后用kibana展示。


