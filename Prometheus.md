# Prometheus
Prometheus是一个开源监控系统，它前身是SoundCloud的警告工具包。以HTTP方式，通过pull模型拉去时间序列数据。

就Prometheus而言，pull拉取采样点的端点服务称之为instance。多个这样pull拉取采样点的instance, 则构成了一个job。

例如, 一个被称作api-server的任务有四个相同的实例。
```
job: api-server
   instance 1: 1.2.3.4:5670
   instance 2: 1.2.3.4:5671
   instance 3: 5.6.7.8:5670
   instance 4: 5.6.7.8:5671
```

自动化生成的标签和时间序列，当Prometheus拉取一个目标，会自动地把两个标签添加到度量名称的标签列表中，分别是：job目标所属的配置任务名称api-server。instance采样点所在服务host:port。

Prometheus fundamentally stores all data as time series: streams of timestamped values belonging to the same metric and the same set of labeled dimensions. Every time series is uniquely identified by its metric name and a set of key-value pairs, also known as labels.

The metric name must match the regex `[a-zA-Z_:][a-zA-Z0-9_:]*.`. The colons are reserved for user defined recording rules. They should not be used by exporters or direct instrumentation.

Label names may contain ASCII letters, numbers, as well as underscores. They must match the regex `[a-zA-Z_][a-zA-Z0-9_]*.`. Label names beginning with `__` are reserved for internal use.

Given a metric name and a set of labels, time series are frequently identified using this notation: `<metric name>{<label name>=<label value>, ...}`.

```
global:
  scrape_interval: 10s
  scrape_timeout: 6s
  evaluation_interval: 10s

scrape_configs:
  - job_name: schema-registry
    scrape_interval: 10s
    scrape_timeout: 6s
    metrics_path: /metrics
    scheme: http
    static_configs:
    - targets: ['localhost:5556']
    metric_relabel_configs:
    - source_labels: [__name__]
      regex: ^xxx_.*
      action: keep

remote_write:
- url: "http://xxx.xxx.xxx.xxx:8086/api/v1/prom/write?db=xxx&rp=autogen"
  write_relabel_configs:
  - source_labels: [job]
    regex: schema-registry
    action: keep
  queue_config:
    max_samples_per_send: 2000
    capacity: 100000
    batch_send_deadline: 1s

remote_read:
  - url: "xxx.xxx.xxx.xxx::8086/api/v1/prom/read?db=xxx&rp=autogen"
```

### metric type
Prometheus客户端库提供四种核心度量标准类型。这些目前仅在客户端库中区分。Prometheus服务器尚未使用类型信息，并将所有数据展平为无类型时间序列。

##### Counter
计数器是表示单个单调递增计数器的累积量，其值只能增加或在重启时重置为零。例如，使用计数器来表示服务的总请求数，已完成的任务或错误总数。不要使用计数器来监控可能减少的值。

counter主要有两个方法：
```go
//将counter值加1.
Inc()
// 将指定值加到counter值上，如果指定值< 0会panic.
Add(float64)
```
- Counter

一般metric容器使用的步骤都是：

1. 初始化一个metric容器
2. 2.Register注册容器
3. 向容器中添加值

使用举例：
```go
//step1:初始一个counter
pushCounter = prometheus.NewCounter(prometheus.CounterOpts{
    Name: "repository_pushes",
    Help: "Number of pushes to external repository.",
})

//setp2:注册容器
err = prometheus.Register(pushCounter)
if err != nil {
    fmt.Println("Push counter couldn't be registered AGAIN, no counting will happen:", err)
    return
}

pushComplete := make(chan struct{})
// TODO: Start a goroutine that performs repository pushes and reports
// each completion via the channel.
for range pushComplete {
    //step3:向容器中写入值
    pushCounter.Inc()
}
```

- CounterVec

CounterVec是一组counter，这些计数器具有相同的描述，但它们的变量标签具有不同的值。如果要计算按各种维度划分的相同内容（例如，响应代码和方法分区的HTTP请求数，则使用此方法。使用NewCounterVec创建实例。
```go
//step1:初始化一个容器
httpReqs := prometheus.NewCounterVec(
    prometheus.CounterOpts{
        Name: "http_requests_total",
        Help: "How many HTTP requests processed, partitioned by status code and HTTP method.",
    },
    []string{"code", "method"}, //Labels.
)
//step2:注册容器
prometheus.MustRegister(httpReqs)

httpReqs.WithLabelValues("404", "POST").Add(42)

// If you have to access the same set of labels very frequently, it
// might be good to retrieve the metric only once and keep a handle to
// it. But beware of deletion of that metric, see below!
//step3:向容器中写入值，主要调用容器的方法如Inc()或者Add()方法
m := httpReqs.WithLabelValues("200", "GET")
for i := 0; i < 1000000; i++ {
    m.Inc()
}
// Delete a metric from the vector. If you have previously kept a handle
// to that metric (as above), future updates via that handle will go
// unseen (even if you re-create a metric with the same label set
// later).
httpReqs.DeleteLabelValues("200", "GET")
// Same thing with the more verbose Labels syntax.
httpReqs.Delete(prometheus.Labels{"method": "GET", "code": "200"})
```

##### Gauge
- Gauge

Gauge可以用来存放一个可以任意变大变小的数值，通常用于测量值，例如温度或当前内存使用情况，或者运行的goroutine数量。主要有以下四个方法：
```go
// 将Gauge中的值设为指定值.
Set(float64)
// 将Gauge中的值加1.
Inc()
// 将Gauge中的值减1.
Dec()
// 将指定值加到Gauge中的值上。(指定值可以为负数)
Add(float64)
// 将指定值从Gauge中的值减掉。(指定值可以为负数)
Sub(float64)
```

示例代码（实时统计CPU的温度）：
```go
//step1:初始化容器
cpuTemprature := prometheus.NewGauge(prometheus.GaugeOpts{
    Name:      "CPU_Temperature",
    Help:      "the temperature of CPU",
})
//step2:注册容器
prometheus.MustRegister(cpuTemprature)
//定时获取cpu温度并且写入到容器
func(){
    tem = getCpuTemprature()
    //step3:向容器中写入值。调用容器的方法
    cpuTemprature.Set(tem)  
}
```

- GaugeVec

假设你要一次性统计四个cpu的温度，这个时候就适合使用GaugeVec了。
```go
cpusTemprature := prometheus.NewGaugeVec(
    prometheus.GaugeOpts{
        Name:      "CPUs_Temperature",
        Help:      "the temperature of CPUs.",
    },
    []string{
        // Which cpu temperature?
        "cpuName",
    },
)
prometheus.MustRegister(cpusTemprature)

cpusTemprature.WithLabelValues("cpu1").Set(temperature1)
cpusTemprature.WithLabelValues("cpu2").Set(temperature2)
cpusTemprature.WithLabelValues("cpu3").Set(temperature3)
```

##### Histogram

主要用于表示一段时间范围内对数据进行采样，（通常是请求持续时间或响应大小），并能够对其指定区间以及总数进行统计，通常我们用它计算分位数的直方图。
```go
temps := prometheus.NewHistogram(prometheus.HistogramOpts{
    Name:    "pond_temperature_celsius",
    Help:    "The temperature of the frog pond.", // Sorry, we can't measure how badly it smells.
    Buckets: prometheus.LinearBuckets(20, 5, 5),  // 5 buckets, each 5 centigrade wide. Start with 20.
})

// Simulate some observations.
for i := 0; i < 1000; i++ {
    temps.Observe(30 + math.Floor(120*math.Sin(float64(i)*0.1))/10)
}

// Just for demonstration, let's check the state of the histogram by
// (ab)using its Write method (which is usually only used by Prometheus
// internally).
metric := &dto.Metric{}
temps.Write(metric)
fmt.Println(proto.MarshalTextString(metric))
```

##### Summary
Summary从事件或样本流中捕获单个观察，并以类似于传统汇总统计的方式对其进行汇总：

1. 观察总和。
2. 观察计数。
3. 排名估计。

典型的用例是观察请求延迟，默认情况下Summary提供延迟的中位数。
```go
temps := prometheus.NewSummary(prometheus.SummaryOpts{
    Name:       "pond_temperature_celsius",
    Help:       "The temperature of the frog pond.",
    Objectives: map[float64]float64{0.5: 0.05, 0.9: 0.01, 0.99: 0.001},
})

// Simulate some observations.
for i := 0; i < 1000; i++ {
    temps.Observe(30 + math.Floor(120*math.Sin(float64(i)*0.1))/10)
}

// Just for demonstration, let's check the state of the summary by
// (ab)using its Write method (which is usually only used by Prometheus
// internally).
metric := &dto.Metric{}
temps.Write(metric)
fmt.Println(proto.MarshalTextString(metric))
```



prometheus client.
metrics name 拼接？


### SQL Exporter
