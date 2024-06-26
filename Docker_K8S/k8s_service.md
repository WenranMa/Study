# Service

在 kubernetes 中，当创建带有多个副本的 deployment 时，kubernetes 会创建出多个 pod，此时即一个服务后端有多个容器，那么在 kubernetes 中负载均衡怎么做，容器漂移后 ip 也会发生变化，如何做服务发现以及会话保持？这就是 service 的作用，service 是一组具有相同 label pod 集合的抽象，集群内外的各个服务可以通过 service 进行互相通信，当创建一个 service 对象时也会对应创建一个 endpoint 对象，endpoint 是用来做容器发现的，service 只是将多个 pod 进行关联，实际的路由转发都是由 kubernetes 中的 kube-proxy 组件来实现，因此，service 必须结合 kube-proxy 使用，kube-proxy 组件可以运行在 kubernetes 集群中的每一个节点上也可以只运行在单独的几个节点上，其会根据 service 和 endpoints 的变动来改变节点上 iptables 或者 ipvs 中保存的路由规则。

## service 原理

endpoints controller 是负责生成和维护所有 endpoints 对象的控制器，监听 service 和对应 pod 的变化，更新对应 service 的 endpoints 对象。当用户创建 service 后 endpoints controller 会监听 pod 的状态，当 pod 处于 running 且准备就绪时，endpoints controller 会将 pod ip 记录到 endpoints 对象中，因此，service 的容器发现是通过 endpoints 来实现的。而 kube-proxy 会监听 service 和 endpoints 的更新并调用其代理模块在主机上刷新路由转发规则。

## service 的负载均衡
上文已经提到 service 实际的路由转发都是由 kube-proxy 组件来实现的，kube-proxy 的代理模块目前有四种实现方案，userspace、iptables、ipvs、kernelspace，其发展历程如下所示：

### iptables 模式
iptables 模式是目前默认的代理方式。当客户端请求 service 的 ClusterIP 时，根据 iptables 规则路由到各 pod 上，iptables 使用 DNAT 来完成转发，其采用了随机数实现负载均衡。

iptables 模式最主要的问题是在 service 数量大的时候会产生太多的 iptables 规则，使用非增量式更新会引入一定的时延，大规模情况下有明显的性能问题。

### ipvs 模式
当集群规模比较大时，iptables 规则刷新会非常慢，难以支持大规模集群，因其底层路由表的实现是链表，对路由规则的增删改查都要涉及遍历一次链表，ipvs 的问世正是解决此问题的，ipvs 是 LVS 的负载均衡模块，与 iptables 比较像的是，ipvs 的实现虽然也基于 netfilter 的钩子函数，但是它却使用哈希表作为底层的数据结构并且工作在内核态，也就是说 ipvs 在重定向流量和同步代理规则有着更好的性能，几乎允许无限的规模扩张。

ipvs 支持三种负载均衡模式：DR模式（Direct Routing）、NAT 模式（Network Address Translation）、Tunneling（也称 ipip 模式）。三种模式中只有 NAT 支持端口映射，所以 ipvs 使用 NAT 模式。linux 内核原生的 ipvs 只支持 DNAT，当在数据包过滤，SNAT 和支持 NodePort 类型的服务这几个场景中ipvs 还是会使用 iptables。

此外，ipvs 也支持更多的负载均衡算法，例如：

rr：round-robin/轮询
lc：least connection/最少连接
dh：destination hashing/目标哈希
sh：source hashing/源哈希
sed：shortest expected delay/预计延迟时间最短
nq：never queue/从不排队

userspace、iptables、ipvs 三种模式中默认的负载均衡策略都是通过 round-robin 算法来选择后端 pod 的，在 service 中可以通过设置 service.spec.sessionAffinity 的值实现基于客户端 ip 的会话亲和性，service.spec.sessionAffinity 的值默认为”None”，可以设置为 “ClientIP”，此外也可以使用 service.spec.sessionAffinityConfig.clientIP.timeoutSeconds 设置会话保持时间。

## service 的类型
service 支持的类型也就是 kubernetes 中服务暴露的方式，默认有四种 ClusterIP、NodePort、LoadBalancer、ExternelName，此外还有 Ingress，下面会详细介绍每种类型 service 的具体使用场景。

### ClusterIP
ClusterIP 类型的 service 是 kubernetes 集群默认的服务暴露方式，它只能用于集群内部通信，可以被各 pod 访问，其访问方式为：

pod ---> ClusterIP:ServicePort --> (iptables)DNAT --> PodIP:containePort
ClusterIP Service 类型的结构如下图所示:

### NodePort
如果你想要在集群外访问集群内部的服务，可以使用这种类型的 service，NodePort 类型的 service 会在集群内部署了 kube-proxy 的节点打开一个指定的端口，之后所有的流量直接发送到这个端口，然后会被转发到 service 后端真实的服务进行访问。Nodeport 构建在 ClusterIP 上，其访问链路如下所示：

client ---> NodeIP:NodePort ---> ClusterIP:ServicePort ---> (iptables)DNAT ---> PodIP:containePort
其对应具体的 iptables 规则会在后文进行讲解。

### LoadBalancer
LoadBalancer 类型的 service 通常和云厂商的 LB 结合一起使用，用于将集群内部的服务暴露到外网，云厂商的 LoadBalancer 会给用户分配一个 IP，之后通过该 IP 的流量会转发到你的 service 上。

### ExternelName
通过 CNAME 将 service 与 externalName 的值(比如：foo.bar.example.com)映射起来，这种方式用的比较少。

### Ingress
Ingress 其实不是 service 的一个类型，但是它可以作用于多个 service，被称为 service 的 service，作为集群内部服务的入口，Ingress 作用在七层，可以根据不同的 url，将请求转发到不同的 service 上。


## iptables
iptables 的功能：

- 流量转发：DNAT 实现 IP 地址和端口的映射；
- 负载均衡：statistic 模块为每个后端设置权重；
- 会话保持：recent 模块设置会话保持时间；

iptables 有五张表和五条链，五条链分别对应为：

- PREROUTING 链：数据包进入路由之前，可以在此处进行 DNAT；
- INPUT 链：一般处理本地进程的数据包，目的地址为本机；
- FORWARD 链：一般处理转发到其他机器或者 network namespace 的数据包；
- OUTPUT 链：原地址为本机，向外发送，一般处理本地进程的输出数据包；
- POSTROUTING 链：发送到网卡之前，可以在此处进行 SNAT；

五张表分别为：

- filter 表：用于控制到达某条链上的数据包是继续放行、直接丢弃(drop)还是拒绝(reject)；
- nat 表：network address translation 网络地址转换，用于修改数据包的源地址和目的地址；
- mangle 表：用于修改数据包的 IP 头信息；
- raw 表：iptables 是有状态的，其对数据包有链接追踪机制，连接追踪信息在 /proc/net/nf_conntrack 中可以看到记录，而 raw 是用来去除链接追踪机制的；
- security 表：最不常用的表，用在 SELinux 上；

这五张表是对 iptables 所有规则的逻辑集群且是有顺序的，当数据包到达某一条链时会按表的顺序进行处理，表的优先级为：raw、mangle、nat、filter、security


## 练习

简述kube-proxy iptables的原理

    Kubernetes从1.2版本开始，将iptables作为kube-proxy的默认模式。iptables模式下的kube-proxy不再起到Proxy的作用，其核心功能：通过API Server的Watch接口实时跟踪Service与Endpoint的变更信息，并更新对应的iptables规则，Client的请求流量则通过iptables的NAT机制“直接路由”到目标Pod。


简述kube-proxy ipvs的原理

    IPVS在Kubernetes1.11中升级为GA稳定版。IPVS则专门用于高性能负载均衡，并使用更高效的数据结构（Hash表），允许几乎无限的规模扩张，因此被kube-proxy采纳为最新模式。

    在IPVS模式下，使用iptables的扩展ipset，而不是直接调用iptables来生成规则链。iptables规则链是一个线性的数据结构，ipset则引入了带索引的数据结构，因此当规则很多时，也可以很高效地查找和匹配。

    可以将ipset简单理解为一个IP（段）的集合，这个集合的内容可以是IP地址、IP网段、端口等，iptables可以直接添加规则对这个“可变的集合”进行操作，这样做的好处在于可以大大减少iptables规则的数量，从而减少性能损耗。


简述kube-proxy ipvs和iptables的异同

    iptables与IPVS都是基于Netfilter实现的，但因为定位不同，二者有着本质的差别：iptables是为防火墙而设计的；IPVS则专门用于高性能负载均衡，并使用更高效的数据结构（Hash表），允许几乎无限的规模扩张。

    与iptables相比，IPVS拥有以下明显优势：

    - 为大型集群提供了更好的可扩展性和性能；
    - 支持比iptables更复杂的复制均衡算法（最小负载、最少连接、加权等）；
    - 支持服务器健康检查和连接重试等功能；
    - 可以动态修改ipset的集合，即使iptables的规则正在使用这个集合。

    底层数据结构：iptables 使用链表，ipvs 使用哈希表
    负载均衡算法：iptables 只支持随机、轮询两种负载均衡算法而 ipvs 支持的多达 8 种；
    操作工具：iptables 需要使用 iptables 命令行工作来定义规则，ipvs 需要使用 ipvsadm 来定义规则。
    此外 ipvs 还支持 realserver 运行状况检查、连接重试、端口映射、会话保持等功能。


K8s的Service是什么？

    Pod每次重启或者重新部署，其IP地址都会产生变化，这使得pod间通信和pod与外部通信变得困难，这时候，就需要Service为pod提供一个固定的入口。Service的Endpoint列表通常绑定了一组相同配置的pod，通过负载均衡的方式把外界请求分配到多个pod上

k8s是怎么进行服务注册的？ ???

    答：Pod启动后会加载当前环境所有Service信息，以便不同Pod根据Service名进行通信。

k8s集群外流量怎么访问Pod？

    答：可以通过Service的NodePort方式访问，会在所有节点监听同一个端口，比如：30000，访问节点的流量会被重定向到对应的Service上面。


简述Kubernetes Service分发后端的策略 

    Service负载分发的策略有：RoundRobin和SessionAffinity

    - RoundRobin：默认为轮询模式，即轮询将请求转发到后端的各个Pod上。
    - SessionAffinity：基于客户端IP地址进行会话保持的模式，即第1次将某个客户端发起的请求转发到后端的某个Pod上，之后从相同的客户端发起的请求都将被转发到后端相同的Pod上。


简述Kubernetes Headless Service

    在某些应用场景中，若需要人为指定负载均衡器，不使用Service提供的默认负载均衡的功能，或者应用程序希望知道属于同组服务的其他实例。Kubernetes提供了Headless Service来实现这种功能，即不为Service设置ClusterIP（入口IP地址），仅通过Label Selector将后端的Pod列表返回给调用的客户端。

    当不需要负载均衡以及单独的 ClusterIP 时，可以通过指定 spec.clusterIP 的值为 None 来创建 Headless service，它会给一个集群内部的每个成员提供一个唯一的 DNS 域名来作为每个成员的网络标识，集群内部成员之间使用域名通信。

```yml
apiVersion: v1
kind: Service
metadata:
name: my-nginx
spec:
clusterIP: None
ports:
- nodePort: 30090
    port: 80
    protocol: TCP
    targetPort: 8080
selector:
    app: my-nginx
```

简述Kubernetes ingress

    Kubernetes的Ingress资源对象，用于将不同URL的访问请求转发到后端不同的Service，以实现HTTP层的业务路由机制。

    Kubernetes使用了Ingress策略和Ingress Controller，两者结合并实现了一个完整的Ingress负载均衡器。使用Ingress进行负载分发时，Ingress Controller基于Ingress规则将客户端请求直接转发到Service对应的后端Endpoint（Pod）上，从而跳过kube-proxy的转发功能，kube-proxy不再起作用，全过程为：ingress controller + ingress 规则 ----> services。

    同时当Ingress Controller提供的是对外服务，则实际上实现的是边缘路由器的功能。


```yaml
apiVersion: v1
kind: Service
metadata:
  name: {{ .Values.name }}
  labels:
    app: {{ .Values.app }}
    chart: {{ include "project.chart" . }}
    component: {{ .Values.app }}
    release: {{ .Release.Name }}
    heritage: {{ .Release.Service }}
spec:
  type: NodePort #LoadBalancer works, but not Cluster IP if there is a ingress bond to Route53.
  ports:
    - name: {{ .Values.name }}
      port: {{ .Values.config.api_server.port }}
      targetPort: {{ .Values.config.api_server.port }}
      protocol: TCP
  selector:
    app: {{ .Values.app }}
```

For some parts of your application (for example, frontends) you may want to expose a Service onto an external IP address, that's outside of your cluster.

Kubernetes ServiceTypes allow you to specify what kind of Service you want. The default is ClusterIP.

Type values and their behaviors are:

- ClusterIP: Exposes the Service on a cluster-internal IP. Choosing this value makes the Service only reachable from within the cluster. This is the default ServiceType.
- NodePort: Exposes the Service on each Node's IP at a static port (the NodePort). A ClusterIP Service, to which the NodePort Service routes, is automatically created. You'll be able to contact the NodePort Service, from outside the cluster, by requesting <NodeIP>:<NodePort>.
- LoadBalancer: Exposes the Service externally using a cloud provider's load balancer. NodePort and ClusterIP Services, to which the external load balancer routes, are automatically created.
- ExternalName: Maps the Service to the contents of the externalName field (e.g. foo.bar.example.com), by returning a CNAME record with its value. No proxying of any kind is set up.