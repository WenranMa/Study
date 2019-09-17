
# Elastic Stack

### Elasticsearch 

- 依赖JDK. 
- 配置文件位于config/elasticsearch.yml
- jvm.options 用于修改jvm相关参数如内存大小等。
- log4j2.properties 日志先关配置

本地快速启动集群方式：

    `bin/elasticsearch`
    `bin/elasticsearch -Ehttp.port=8200 -Epath.data=node2`
    `bin/elasticsearch -Ehttp.port=7200 -Epath.data=node3` 与通过配置文件修改一样。

可以通过API：

    localhost:9200/_cat/nodes
    localhost:9200/_cat/nodes?v

    localhost:9200/_cluster/stats
查看节点信息。

##### 配置文件：
```yaml
# Master node
cluster.name: wenran

node.name: master
node.master: true

network.host: 127.0.0.1

# Slave node
cluster.name: wenran
node.name: slave1

network.host: 127.0.0.1
http.port: 8200

discovery.zen.ping.unicast.hosts: ["127.0.0.1"]
```

##### 常用术语：

集群由多个节点构成，其中包括主节点master和从节点slave.

- Document 文档，可以被索引的基本数据单位（一条数据）
- Index 索引(类似数据库)
- Type 索引中的数据类型（类似Table）
- Field 字段，文档属性
- Query DSL 查询语言

mapping 类似schema.

Script ？？？？


---

### Kibana
bin/kibana运行

##### 配置文件：
config/kibana.yml
```yaml
server.host: http://localhost
server.port: 5601

elasticsearch.url: localhost:9200
```

##### 功能：

Dev tools可以执行CRUD的语句。
```javascript
//增加：
POST account/employee/1
{
  "name":"WenranMa",
  "age":32,
  "title":"software engineer"
}
//POST API类型，
//account 是Index
//employee 是Type
//1 是ID
//后面的{}是Document. 一条数据。

//返回结果
// Deprecation: [types removal] Specifying types in document index requests is deprecated, use the typeless endpoints instead (/{index}/_doc/{id}, /{index}/_doc, or /{index}/_create/{id}).
{
  "_index" : "account",
  "_type" : "employee",
  "_id" : "1",
  "_version" : 1,
  "result" : "created",
  "_shards" : {
    "total" : 2,
    "successful" : 1,
    "failed" : 0
  },
  "_seq_no" : 0,
  "_primary_term" : 1
}

//查：
GET account/employee/1

//改：
POST account/employee/1/_update
{
  "doc":{
    "age":30
  }
}

//删：
DELETE account/employee/1

//搜索：
GET account/employee/_search?q=Wenran

GET account/employee/_search
{
  "query":{
    "match": {
      "name": "Wenran"
    }
  }
}
```

---

### Beats
Light Weight Data Shipper

- FileBeat 日志文件
- Metricbeat 收集度量数据
- Packetbeat 网络数据
- Heartbeat 健康检查

beat属于数据起始端，用于收集数据，存储于elasticsearch，最后用kibana展示。
beat也可以先通过logstash将数据进行转换再进入elasticsearch。

![Beats](./img/beats-platform.png)

##### FileBeat
处理日志文件，包括Input, Filter, Output.

配置文件：
```yaml
#-------------------------- Iutput ------------------------------
filebeat.inputs:
- type: log
  # log, stdin  
  enabled: true

  # Paths that should be crawled and fetched. Glob based paths.
  # paths:
    #- /var/log/*.log

#-------------------------- Elasticsearch output ------------------------------
output.elasticsearch:
  # Array of hosts to connect to.
  hosts: ["localhost:9200"]

# output.console
output.console:
    pretty: true
```

Filebeat Module 将常用的集成配置封装好。

##### PacketBeat
实时抓取网络包。自动解析网络层协议。

就像一个轻量级的wireshark。

配置文件：test.yml
```yaml
#============================== Network device ================================
packetbeat.interfaces.device: lo0

#========================== Transaction protocols =============================
packetbeat.protocols:
- type: http
  # Configure the ports where to listen for HTTP traffic. You can disable
  # the HTTP protocol by commenting out the list of ports.
  ports: [9200]
  send_request: true

#========================== output ============================================
output.console:
  pretty: true
```

运行：`sudo ./packetbeat -e -c test.yml`

返回结果：
```json
{
  "@timestamp": "2019-09-14T13:35:24.266Z",
  "@metadata": {
    "beat": "packetbeat",
    "type": "_doc",
    "version": "7.3.2"
  },
  "url": {
    "path": "/",
    "full": "http://[localhost:9200]:9200/",
    "scheme": "http",
    "domain": "localhost:9200",
    "port": 9200
  },
  "user_agent": {
    "original": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36"
  },
  "http": {
    "request": {
      "method": "get",
      "bytes": 494,
      "headers": {
        "content-length": 0
      }
    },
    "response": {
      "bytes": 391,
      "body": {
        "bytes": 280
      },
      "headers": {
        "content-type": "application/json; charset=UTF-8",
        "content-length": 280
      },
      "status_phrase": "ok",
      "status_code": 200
    },
    "version": "1.1"
  },
  "event": {
    "category": "network_traffic",
    "dataset": "http",
    "duration": 5208000,
    "start": "2019-09-14T13:35:24.266Z",
    "end": "2019-09-14T13:35:24.272Z",
    "kind": "event"
  },
  "agent": {
    "hostname": "wrma-mac",
    "id": "e994a6be-3051-441f-8ede-1ec059f2a620",
    "version": "7.3.2",
    "type": "packetbeat",
    "ephemeral_id": "4c510f9b-6d4a-4b7e-816d-b91c8845a35a"
  },
  "client": {
    "ip": "::1",
    "port": 53786,
    "bytes": 494
  },
  "method": "get",
  "destination": {
    "bytes": 391,
    "ip": "::1",
    "port": 9200,
    "domain": "localhost:9200"
  },
  "query": "GET /",
  "network": {
    "community_id": "1:f69TrMVE2osxDstLcrs4J3+a2rA=",
    "bytes": 885,
    "type": "ipv6",
    "transport": "tcp",
    "protocol": "http"
  },
  "status": "OK",
  "source": {
    "ip": "::1",
    "port": 53786,
    "bytes": 494
  },
  "server": {
    "port": 9200,
    "domain": "localhost:9200",
    "bytes": 391,
    "ip": "::1"
  },
  "request": "GET / HTTP/1.1\r\nHost: localhost:9200\r\nConnection: keep-alive\r\nUpgrade-Insecure-Requests: 1\r\nUser-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36\r\nSec-Fetch-Mode: navigate\r\nSec-Fetch-User: ?1\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3\r\nSec-Fetch-Site: none\r\nAccept-Encoding: gzip, deflate, br\r\nAccept-Language: zh-CN,zh;q=0.9\r\n\r\n",
  "ecs": {
    "version": "1.0.1"
  },
  "host": {
    "name": "wrma-mac"
  },
  "type": "http"
}
```

---

### Logstash
Data Shipper（对比beats是light weight data shipper）

ETL:

    Extract
    Transform
    Load

所以与Beats的Input, Filter, Output一样，但功能更强。

##### Filter
Logstash 主要强在Filter.

1. Grok: 基于正则。将非结构化的数据做结构化处理。
2. Date: 字符串类型转换成时间戳类型。
3. Mutate: CRUD.

---

### 案例
PacketBeat + LogStash 负责数据的抓取。
Kibana + ElasticSearch 负责数据分析。

两个ElasticSearch 集群，prd和monitor，prd是被监控对象。（如果是一个集群演示会出现抓包死循环）

1.启动Production ElasticSearch 集群。使用默认配置。

    bin/elasticsearch
    bin/elasticsearch -Ehttp.port=9201 -Epath.data=node2
    elasticsearch至少启动两个节点。否则Kibana启动会失败。??

2.启动Production Kibana。

    bin/kibana

3.启动Monitor ElasticSearch 集群。

    bin/elasticsearch -Ecluster.name=monitor -Ehttp.port=8200 —Epath.data=monitor

4.启动Monitor Kibana。

    bin/kibana -e http://127.0.0.1:8200 -p 8601

5.LogStash配置及启动。

```json
input {
  beats {
    port => 5044
  }
}

filter {
    if "search" in [request]{
        grok {
            match => { "request" => ".*\n\{(?<query_body>.*)"}
        }
        grok {
            match => { "path" => "\/(?<index>.*)\/_search"}
        }
    }
    if [index] {
    } else {
        mutate {
            add_field  => { "index" => "All" }
        }
    }

    mutate {
        update  => { "query_body" => "{%{query_body}"}}
    }

output {
  if "search" in [request]{
        elasticsearch {
        hosts => "127.0.0.1:8200"
        }
   }
}
```

6.PacketBeat配置及启动。

```yaml
packetbeat.interfaces.device: lo0
packetbeat.protocols:
- type: http
  ports: [9200]
  send_request: true

output.logstash:
  hosts: ["127.0.0.1:5044"]
```

在Monitor Kibana中:

    GET _cat/indices 就可以看到logstash的索引。

可以创建Index pattern，然后通过命名找到已有index. Pattern创建完成后，可以在discover中看到数据展示。