# Kubernetes 的概述
Kubernetes，又称为 k8s（首字母为 k、首字母与尾字母之间有 8 个字符、尾字母为 s，所以简称 k8s）或者简称为 "kube" ，是一种可自动实施 Linux 容器操作的开源平台。它可以帮助用户省去应用容器化过程的许多手动部署和扩展操作。也就是说，您可以将运行 Linux 容器的多组主机聚集在一起，由 Kubernetes 帮助您轻松高效地管理这些集群。而且，这些集群可跨公共云、私有云或混合云部署主机。因此，对于要求快速扩展的云原生应用而言，Kubernetes 是理想的托管平台。

Kubernetes 最初由 Google 的工程师开发和设计。Google 是最早研发 Linux 容器技术的企业之一（组建了cgrous），曾公开分享介绍Google 如何将一切都运行于容器之中（这是 Google 云服务背后的技术）。Google 每周会启用超过 20 亿个容器——全都由内部平台 Borg 支撑。Borg 是 Kubernetes 的前身，多年来开发 Borg 的经验教训成了影响 Kubernetes 中许多技术的主要因素。

趣事：Kubernetes 徽标的七个轮辐代表着项目最初的名称"九之七项目"(Project Seven of Nine)。

Kubernetes 是一个可移植的、可扩展的开源平台，用于管理容器化的工作负载和服务，可促进声明式配置和自动化。 Kubernetes 拥有一个庞大且快速增长的生态系统。Kubernetes 的服务、支持和工具广泛可用。

Kubernetes 这个名字源于希腊语，意为“舵手”或“飞行员”。k8s 这个缩写是因为 k 和 s 之间有八个字符的关系。 Google 在 2014 年开源了 Kubernetes 项目。


## 部署变迁
![部署演进](https://d33wubrfki0l68.cloudfront.net/26a177ede4d7b032362289c6fccd448fc4a91174/eb693/images/docs/container_evolution.svg)

1. 单机模式

早期，各个组织机构在物理服务器上运行应用程序。无法为物理服务器中的应用程序定义资源边界，这会导致资源分配问题，无法扩展，并且维护许多物理服务器的成本很高，安全性较低，可迁移性差。

2. 虚拟化

VMware等，将单机划分为多个虚拟机，充分利用单机。基于虚拟机技术的Amazon Web Service。

虚拟化允许应用程序在 VM 之间隔离，并提供一定程度的安全，因为一个应用程序的信息 不能被另一应用程序随意访问。

虚拟化技术能够更好地利用物理服务器上的资源，并且因为可轻松地添加或更新应用程序 而可以实现更好的可伸缩性，降低硬件成本等等。

每个 VM 是一台完整的计算机，在虚拟化硬件之上运行所有组件，包括其自己的操作系统。

性能较差，资源利用率较低，扩展性较差，维护成本较高。

3. 虚拟化成熟。服务模式：IaaS, PaaS, SaaS
- iaas（基础设施即服务），用户租用（购买|分配权限）云主机，用户不需要考虑网络，DNS，硬件环境方面的问题。
- paas（平台即服务）
  - mysql/es/mq/...
- saas（软件即服务）

4. 容器化，Docker。

容器类似于 VM，但是它们具有被放宽的隔离属性，可以在应用程序之间共享操作系统（OS）。 因此，容器被认为是轻量级的。容器与 VM 类似，具有自己的文件系统、CPU、内存、进程空间等。 由于它们与基础架构分离，因此可以跨云和 OS 发行版本进行移植。

容器因具有许多优势而变得流行起来。下面列出的是容器的一些好处：

- 敏捷应用程序的创建和部署：与使用 VM 镜像相比，提高了容器镜像创建的简便性和效率。
- 持续开发、集成和部署：通过快速简单的回滚（由于镜像不可变性），支持可靠且频繁的 容器镜像构建和部署。
- 关注开发与运维的分离：在构建/发布时而不是在部署时创建应用程序容器镜像， 从而将应用程序与基础架构分离。
- 可观察性：不仅可以显示操作系统级别的信息和指标，还可以显示应用程序的运行状况和其他指标信号。
- 跨开发、测试和生产的环境一致性：在便携式计算机上与在云中相同地运行。
- 跨云和操作系统发行版本的可移植性：可在 Ubuntu、RHEL、CoreOS、本地、 Google Kubernetes Engine 和其他任何地方运行。
- 以应用程序为中心的管理：提高抽象级别，从在虚拟硬件上运行 OS 到使用逻辑资源在 OS 上运行应用程序。
- 松散耦合、分布式、弹性、解放的微服务：应用程序被分解成较小的独立部分， 并且可以动态部署和管理 - 而不是在一台大型单机上整体运行。
- 资源隔离：可预测的应用程序性能。
- 资源利用：高效率和高密度。

5. 云原生，容器+微服务。K8S

如果想要将 Docker 应用于庞大的业务实现，是存在困难的编排、管理和调度问题。于是，我们迫切需要一套管理系统，对 Docker 及容器进行更高级更灵活的管理。

为了让应用程序（项目，服务软件）都运行在云上的解决方案，这样的方案叫做`云原生`。

云原生有如下特点：

- 容器化，所有服务都必须部署在容器中
- 微服务，Web 服务架构式服务架构
- CI/CD
- DevOps

## Kubernetes 特点

K8s 是一个可移植的、可扩展的开源平台，用于编排，管理容器化的工作负载和服务。Kubernetes 包含了对容器化技术的使用，通过容器化镜像解决应用打包与分发问题，通过容器化运行时解决应用运行环境的问题。Kubernetes 提供了一系列资源对象抽象，用户通过对这些对象进行声明从而告诉 Kubernetes 期望的资源状态及行为是什么，之后 Kubernetes 强大的自动化系统会尽可能使得集群中的工作负载、服务、网络、配置项等资源尽可能与用户期望的保持一致。

1. 快速部署应用
2. 快速扩展应用
3. 无缝对接新的应用功能
4. 节省资源，优化硬件资源的使用
5. 可移植的
6. 容器化
7. 声明式
8. 自动化

- 服务发现和负载均衡
  Kubernetes 可以使用 DNS 名称或自己的 IP 地址公开容器，如果进入容器的流量很大， Kubernetes 可以负载均衡并分配网络流量，从而使部署稳定。
- 存储编排
  Kubernetes 允许你自动挂载你选择的存储系统，例如本地存储、公共云提供商等。
- 自动部署和回滚
  你可以使用 Kubernetes 描述已部署容器的所需状态，它可以以受控的速率将实际状态 更改为期望状态。例如，你可以自动化 Kubernetes 来为你的部署创建新容器， 删除现有容器并将它们的所有资源用于新容器。
- 自动二进制打包
  Kubernetes 允许你指定每个容器所需 CPU 和内存（RAM）。 当容器指定了资源请求时，Kubernetes 可以做出更好的决策来管理容器的资源。
- 自我修复
  Kubernetes 重新启动失败的容器、替换容器、杀死不响应用户定义的 运行状况检查的容器，并且在准备好服务之前不将其通告给客户端。
- 密钥与配置管理
  Kubernetes 允许你存储和管理敏感信息，例如密码、OAuth 令牌和 ssh 密钥。 你可以在不重建容器镜像的情况下部署和更新密钥和应用程序配置，也无需在堆栈配置中暴露密钥。

### Kubernetes 不是什么

Kubernetes 不是传统的、包罗万象的 PaaS（平台即服务）系统。 由于 Kubernetes 在容器级别而不是在硬件级别运行，它提供了 PaaS 产品共有的一些普遍适用的功能， 例如部署、扩展、负载均衡、日志记录和监视。 但是，Kubernetes 不是单体系统，默认解决方案都是可选和可插拔的。 Kubernetes 提供了构建开发人员平台的基础，但是在重要的地方保留了用户的选择和灵活性。

- 不限制支持的应用程序类型。 Kubernetes 旨在支持极其多种多样的工作负载，包括无状态、有状态和数据处理工作负载。 如果应用程序可以在容器中运行，那么它应该可以在 Kubernetes 上很好地运行。
- 不部署源代码，也不构建你的应用程序。 持续集成(CI)、交付和部署（CI/CD）工作流取决于组织的文化和偏好以及技术要求。
- 不提供应用程序级别的服务作为内置服务，例如中间件（例如，消息中间件）、 数据处理框架（例如，Spark）、数据库（例如，mysql）、缓存、集群存储系统 （例如，Ceph）。这样的组件可以在 Kubernetes 上运行。
- 不要求日志记录、监视或警报解决方案。 它提供了一些集成作为概念证明，并提供了收集和导出指标的机制。
- 不提供或不要求配置语言/系统（例如 jsonnet），它提供了声明性 API， 该声明性 API 可以由任意形式的声明性规范所构成。
- 不提供也不采用任何全面的机器配置、维护、管理或自我修复系统。
- 此外，Kubernetes 不仅仅是一个编排系统，实际上它消除了编排的需要。 编排的技术定义是执行已定义的工作流程：首先执行 A，然后执行 B，再执行 C。 相比之下，Kubernetes 包含一组独立的、可组合的控制过程， 这些过程连续地将当前状态驱动到所提供的所需状态。 如何从 A 到 C 的方式无关紧要，也不需要集中控制，这使得系统更易于使用 且功能更强大、系统更健壮、更为弹性和可扩展。


## Kubernetes 架构
概括来说 K8s 架构就是一个 Master 对应一群 Node 节点。

下面我们来逐一介绍 K8s 架构图中的 Master 和 Node。

1. Master 节点，用于控制 Kubernetes 节点的计算机。所有任务分配都来自于此。

- apiserver 即 K8s 网关，所有的指令请求都必须要经过 apiserver；
- scheduler 调度器，使用调度算法，把请求资源调度到某一个 node 节点；
- controller 控制器，维护 K8s 资源对象；
- etcd 存储资源对象；

2. Node节点，负责执行请求和所分配任务的计算机。由 Kubernetes 主机负责对节点进行控制。

- kubelet 在每一个 node 节点都存在一份，在 node 节点上的资源操作指令由 kubelet 来执行；
- kube-proxy 代理服务，处理服务间负载均衡；
- pod 是 k8s 管理的基本单元（最小单元），pod 内部是容器，k8s 不直接管理容器，而是管理pod；
- docker 运行容器的基础环境，容器引擎；
- fluentd 日志收集服务；


![系统组件](https://help-assets.codehub.cn/enterprise/2%E3%80%81components-of-kubernetes-01.png)

### Control Plane 中的组件
Control Plane 的组件对集群做出全局决策（比如调度），以及检测和响应集群事件（例如，当不满足部署的 Replicas 字段时，启动新的 Pod）。

Control Plane 组件可以在集群中的任何节点上运行。然而，为了简单起见，设置脚本通常会在同一个计算机上启动所有 Control Plane 组件，并且不会在此计算机上运行用户容器。

### API Server
是集群控制的唯一入口，是Rest API的核心组件。API Server 组件公开了 Kubernetes API。API Server 是 Kubernetes Control Plane 的前端。Kubernetes API 服务器的主要实现是 kube-apiserver。Kube-apiserver 设计上考虑了水平伸缩，也就是说，它可通过部署多个实例进行伸缩。你可以运行 kube-apiserver 的多个实例，并在这些实例之间平衡流量。

### Etcd
Etcd 是兼具一致性和高可用性的键值数据库，可以作为保存 Kubernetes 所有集群数据的后台数据库。

### Scheduler
Scheduler 组件负责监视新创建的、未指定运行节点（Node）的 Pods，选择节点让 Pod 在上面运行。

调度决策考虑的因素包括单个 Pod 和 Pod 集合的资源需求、硬件/软件/策略约束、亲和性和反亲和性规范、数据位置、工作负载间的干扰和最后时限。

### Controller Manager
从逻辑上讲，每个 Controller 都是一个单独的进程， 但是为了降低复杂性，它们都被编译到同一个可执行文件，并在一个进程中运行。

这些控制器包括:

- 节点控制器（Node Controller）: 负责在节点出现故障时进行通知和响应
- 副本控制器（Replication Controller）: 负责为系统中的每个副本控制器对象维护正确数量的 Pod
- 端点控制器（Endpoints Controller）: 填充端点(Endpoints)对象(即加入 Service 与 Pod)
- 服务帐户和令牌控制器（Service Account & Token Controllers）: 为新的命名空间创建默认帐户和 API 访问令牌

### Cloud Controller Manager (Optional)
Cloud Controller Manager 是指嵌入特定云的控制逻辑的 控制平面组件。Cloud Controller Manager 允许您链接聚合到云提供商的应用编程接口中，并分离出相互作用的组件与您的集群交互的组件。

Cloud-controller-manager 仅运行特定于云平台的控制回路。如果你在自己的环境中运行 Kubernetes，或者在本地计算机中运行学习环境，所部署的环境中不需要 Cloud Controller Manager。

与 kube-controller-manager 类似，cloud-controller-manager 将若干逻辑上独立的控制回路组合到同一个可执行文件中，供你以同一进程的方式运行。你可以对其执行水平扩容（运行不止一个副本）以提升性能或者增强容错能力。

下面的控制器都包含对云平台驱动的依赖：

- 节点控制器（Node Controller）: 用于在节点终止响应后检查云提供商以确定节点是否已被删除
- 路由控制器（Route Controller）: 用于在底层云基础架构中设置路由
- 服务控制器（Service Controller）: 用于创建、更新和删除云提供商负载均衡器

### Kubelet
一个在集群中每个节点（Node）上运行的代理。 它保证容器（Containers）都运行在 Pod 中。

Kubelet 接收一组通过各类机制提供给它的 PodSpecs，确保这些 PodSpecs 中描述的容器处于运行状态且健康。Kubelet 不会管理不是由 Kubernetes 创建的容器。

### Kube-proxy
Kube-proxy 是集群中每个节点上运行的网络代理， 实现 Kubernetes 服务（Service） 概念的一部分。
Kube-proxy 维护节点上的网络规则。这些网络规则允许从集群内部或外部的网络会话与 Pod 进行网络通信。
如果操作系统提供了数据包过滤层并可用的话，kube-proxy 会通过它来实现网络规则。否则， kube-proxy 仅转发流量本身。

### 容器运行时（Container Runtime）
容器运行环境是负责运行容器的软件。
Kubernetes 支持多个容器运行环境: Docker、 containerd、CRI-O 以及任何实现 Kubernetes CRI (容器运行环境接口)。

### 插件（Addons）
插件使用 Kubernetes 资源（DaemonSet、 Deployment等）实现集群功能。 因为这些插件提供集群级别的功能，插件中命名空间域的资源属于 kube-system 命名空间。下面描述众多插件中的几种

1.  DNS

尽管其他插件都并非严格意义上的必需组件，但几乎所有 Kubernetes 集群都应该 有集群 DNS， 因为很多示例都需要 DNS 服务。

集群 DNS 是一个 DNS 服务器，和环境中的其他 DNS 服务器一起工作，它为 Kubernetes 服务提供 DNS 记录。Kubernetes 启动的容器自动将此 DNS 服务器包含在其 DNS 搜索列表中。

2. Web 界面（Dashboard）

Dashboard 是 Kubernetes 集群的通用的、基于 Web 的用户界面。 它使用户可以管理集群中运行的应用程序以及集群本身并进行故障排除。

3. 容器资源监控

容器资源监控，将关于容器的一些常见的时间序列度量值保存到一个集中的数据库中，并提供用于浏览这些数据的界面。

4. 集群层面日志

集群层面日志，机制负责将容器的日志数据保存到一个集中的日志存储中，该存储能够提供搜索和浏览接口。

### 逻辑架构（用户资源对象）
[![用户资源对象](https://help-assets.codehub.cn/enterprise/3%E3%80%81objects-of-users.png)](https://help-assets.codehub.cn/enterprise/3、objects-of-users.png)用户资源对象

上图是一个简单且常见的，通过 Kubernetes 承载和调度的系统。下面让我们来简单分析一下应用是如何运行，以及网络流量是如何到达应用的。

### 工作负载相关
Controller 和 Pod 对象属于 Kubernetes 工作负载类对象，Pod 用于运行实际的应用程序容器，Controller 通过 Selector 选取特定 Labels 的 Pods 从而确定和它们之间的关系，Controller 会持续检查 Pods 是否按预期的状态和数量运行，当满足 Selector 的 Pod 数量小于 Controller 所预期的副本数量，Controller 会自动创建并运行新的 Pod，并为它添加对应的 Lables。

### 网络负衡相关
Ingress 和 Service 对象属于 Kubernetes 网络负载对象，Service 和 Controller 类似，都是通过 Selector 选取特定 Labels 的 Pods 从而确定和它们之间的关系。

Ingress 根据客户端所发出的 URL 特征对流量进行分发，反向代理至目标 Service 上，Service 会根据其自身配置结合算法将流量转发至特定 Pod 中处理。

### Docker运行状态
Docker技术仍然执行它原本的工作。当 kubernetes 将容器集调度到一个节点上时，该节点上的 kubelet 会发送指令让 docker 启动指定的容器。kubelet 随后会不断从 docker 收集这些容器的状态，并将这些信息汇集至主机。Docker 将容器拉至该节点，并按照常规启动和停止这些容器。不同在于，自动化系统要求 docker 在所有节点上对所有容器执行这些操作，而非要求管理员手动操作。

### Pod

- pod 是看s最小操作单元，Pod 用来封装容器的一个容器，Pod 是一个虚拟化分组；
- Pod 相当于独立主机，可以封装一个或者多个容器；

Pod 有自己的 IP 地址、主机名，相当于一台独立沙箱环境。

通常情况下，在服务部署时候，使用 Pod 来管理一组相关的服务。一个 Pod 中要么部署一个服务，要么部署一组有关系的服务。一组相关的服务是指：在链式调用的调用连路上的服务。

实现服务集群：只需要复制多方 Pod 的副本即可，这也是 K8s 管理的先进之处，K8s 如果继续扩容，只需要控制 Pod 的数量即可，缩容道理类似。

Pod 底层网络，数据存储
- Pod 内部容器创建之前，必须先创建 `Pause 容器`；
- 服务容器之间访问 localhost ，相当于访问本地服务一样，性能非常高；

那么为什么一个容器编排系统调度的单位是 Pod 而不是 container 呢，这就要容器的本质了。

稍微复杂的任务，真实世界的程序都比较喜欢用多个进程组合在一起的方式来解决问题。而 Pod 其实就是代表着一个进程组。进程组之间往往有共享磁盘，管道等通讯，如果 Kubernetes 不是把进程组一起调度而是把他们拆开，死板地按进程调度，将会让这些程序的进程可能分布在不同的主机上，导致程序不可用。你也可以把 Pod 类比成虚拟机。想象一下你在虚拟机下有一个 Java 应用，虚拟机里面装了 tomcat，Java war 包，日志搜集程序，如果没有 Pod，如果这些都是用一个个容器去替换，是很难把这个应用搬到 K8s 上的。

另外要注意的是，我们说容器本质是一个进程，并不是说容器不能运行两个进程，只不过能运行不等于能管理，如果你在 dockerfile 里面一次启动两个进程，当容器被杀掉后，第二个进程就不会被系统管到，直接就泄漏了。

使用命令 `kubectl get Pods`，

运行 `kubectl get Pods nginx-deployment-66b6c48dd5-qw9lp -o yaml`，终端中将会输出一堆 yaml:

```yaml
apiVersion: v1
kind: Pod
metadata:
    annotations:
        ....
    labels:
        app: nginx
    name: nginx-deployment-66b6c48dd5-qw9lp
    namespace: jimmy
spec:
    containers:
    - image: nginx:1.14.2
        imagePullPolicy: IfNotPresent
            name: nginx
            ports:
            - containerPort: 80
                protocol: TCP
```

上面代码中，我省略了一些信息，你现在还不用关注这些细节。这个 yaml 的内容，就是一个 Pod 对象，里面包含这个 Pod 在 Kubernetes 集群里运行的绝大部分信息。

#### Metadata
Metadata 是一个对象的元数据，里面包含的基本是这个 Pod 的标识，例如 name 也就是这个 Pod 的名字, namespace 也就是这个 Pod 所在的命名空间，uid 是这个 Pod 在集群里的唯一 id，creationTimestamp 表示这个 Pod 的创建时间。这些字段大多数都是 immutable 的，也就是一旦这个 Pod 创建，就不能再修改这些字段了。

#### Spec
Spec 是这个 Pod 里面具体的规格，包括容器的配置，volume 的配置等。

#### Annotations
Annotations 与 metadata 都属于一个对象的额外信息，但是 metadata 通常是非常重要的信息, 而 arhaenotation 通常来说都是相对没那么重要的信息，很多持续部署系统，云管平台之类的会利用 annotation 属性去做信息的维护。

#### 镜像，端口
Kubernetes 中，Pod 最重要的属性肯定是镜像和端口了，而他们的作用也很明显了，就不展开了

#### ImagePullPolicy
在这个属性决定你对 Kubernetes 发起一个 apply 操作时，镜像拉取的策略，ImagePullPolicy 的值默认是 Always，即每次创建 Pod 都重新拉取一次镜像。另外，当容器的镜像是类似于 nginx 或者 nginx:latest 这样的名字时，ImagePullPolicy 也会被认为 Always，而如果它的值被定义为 Never 或者 IfNotPresent，则意味着 Pod 永远不会主动拉取这个镜像，或者只在宿主机上不存在这个镜像时才拉取。

#### Volume
这个和 docker 的 volume 很相似，只不过他能挂的类型非常多的，从 git 到空目录，到 S3 储存，都不满足的话还可以自己扩展。volume 的定义类似这样：

```yaml
apiVersion: v1
kind: Pod
metadata:
    name: configmap-pod
spec:
    containers:
      - name: test
        image: busybox
        volumeMounts:
          - name: config-vol
            mountPath: /etc/config
    volumes:
      - name: config-vol
        configMap:
            name: log-config
            items:
              - key: log_level
                path: log_level
```

上面例子中，我们声明了一个 volume， 名字叫 config-vol，他的内容引用了一个 Kubernetes 中专门用于保存配置的 configmap 对象。然后在名字叫 test 的容器的 volumeMounts 属性里面，把这个 volume 挂载到了 /etc/config 目录下。

#### Pod 的生命周期

Pod 一共有 5 种状态，这个状态反映在 Pod 的 status 属性中，这是 Pod 除了 Metadata 和 Spec 之外的第三个重要字段。这 5 种状态分别是：

1. Pending。这个状态意味着，Pod 的 YAML 文件已经提交给了 Kubernetes，API 对象已经被创建并保存在 Etcd 当中。但是这个 Pod 还没有被调度成功，最常见的原因比如 Pod 中某个容器启动不成功
2. Running。这个状态下，Pod 已经调度成功。也就是它包含的容器都已经创建成功，并且至少有一个正在运行中
3. Succeeded。这个状态意味着，Pod 里的所有容器都正常运行成功并退出了。这种情况在运行一次性任务时最为常见
4. Failed。这个状态下，Pod 里至少有一个容器以不正常的状态退出。这个状态出现时，你得想办法 Debug 这个容器，比如查看 Pod 的事件和日志。
5. Unknown。这是一个异常状态，意味着 Pod 的状态不能集群检测到，这很有可能是主从节点（Master 和 Kubelet）间的通信出现了问题。

#### Pod 容器间如何共享东西

Pod 里的所有容器，共享的是同一个 Network Namespace，并且可以声明共享同一个 Volume。实际上，Pod 是共享了 linux namespace 的东西。

我们不妨来做个实验，在下面这个 Pod 的 YAML 文件中，我定义了 shareProcessNamespace=true：

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx
spec:
  shareProcessNamespace: true
  containers:
  - name: nginx
    image: nginx
  - name: shell
    image: busybox
    stdin: true
    tty: true
```

我们通过 `kubectl -n jimmy attach -it nginx -c shell` 能够进入到这个 Pod 的第二个容器，也就是 shell 容器里面。通过 ps -ef 命令，在这个容器里居然能看到 nginx 容器的进程。

![img](https://help-assets.codehub.cn/enterprise/20210604151919.png)

显然，Pod 把 linux namespace 共享了。

那么 Pod 是怎么做到这一点的呢？实际上，Pod 在启动的时候会先启动一个 Infra Container 去设置网络、Volume 等 namespace（如果 Volume 要共享的话），其他容器通过加入的方式共享这些 Namespace。实际上我们在上面的 ps -ef 里面也能看到这个 infra container 的进程 /pause。

![img](https://help-assets.codehub.cn/enterprise/20210604151931.png)

#### 使用 Pod 的容器设计模式

Pod 在 Kubernetes 的意义是实现容器设计模式。容器的设计思想，实际上就是希望，当用户想在一个容器里跑多个功能并不相关的应用时，应该优先考虑它们是不是更应该被描述成一个 Pod 里的多个容器。

例如说一个 web 服务的服务本身，和日志收集，他们的业务并不相关，最合理的方式就是使用两个容器去实现。又例如你如果想做一些服务流量的治理，也应该使用一个别的容器而不是耦合在业务代码里。

### ReplicaSet 副本控制器

控制 Pod 副本「服务集群」的数量，永远与预期设定的数量保持一致即可。当有 Pod 服务宕机时候，副本控制器将会立马重新创建一个新的 Pod，永远保证副本为设置数量。

副本控制器：标签选择器-选择维护一组相关的服务（它自己的服务）

```yaml
selector：     
    app = web    
    Release = stable 
```

### Deployment 部署对象

- 服务部署结构模型
- 滚动更新

ReplicaSet 副本控制器控制 Pod 副本的数量。但是，项目的需求在不断迭代、不断的更新，项目版本将会不停的的发版。版本的变化，如何做到服务更新？

- ReplicaSet 不支持滚动更新，Deployment 对象支持滚动更新，通常和 ReplicaSet 一起使用；
- Deployment 管理 ReplicaSet，RS 重新建立新的 RS，创建新的 Pod；

### MySQL 使用容器化部署，存在什么样的问题？

- 容器是生命周期的，一旦宕机，数据丢失
- Pod 部署，Pod 有生命周期，数据丢失

对于 K8s 来说，不能使用 Deployment 部署`有状态`服务。

通常情况下，Deployment 被用来部署无状态服务，那么对于有状态服务的部署，使用 StatefulSet 进行有状态服务的部署。

什么是`有状态服务`？

- 有实时的数据需要存储
- 有状态服务集群中，把某一个服务抽离出去，一段时间后再加入机器网络，如果集群网络无法使用

什么是`无状态服务`？

- 没有实时的数据需要存储
- 无状态服务集群中，把某一个服务抽离出去，一段时间后再加入机器网络，对集群服务没有任何影响

### StatefulSet

为了解决有状态服务使用容器化部署的一个问题。

- 部署模型
- 有状态服务

StatefulSet 保证 Pod 重新建立后，Hostname 不会发生变化，Pod 就可以通过 Hostname 来关联数据。


### Annotation
Kubernetes（k8s）中的annotation是一种元数据机制，用于存储与对象相关的非识别信息。它们扩展了Kubernetes对象的功能，提供了灵活性和额外的上下文信息。以下是Kubernetes annotations的一些关键作用：

- 元数据存储：Annotations允许用户或系统添加任意的键值对数据到API对象中，这些数据不直接影响对象的管理和运行逻辑，但可以被用来记录额外信息或传递给其他工具和系统。

- 信息传递：开发者或运维人员可以通过annotations向部署的组件传达配置信息或说明，比如指示自动缩放策略、服务发现细节、部署版本等。

- 工具集成：许多Kubernetes周边工具和服务会读取或设置annotations来实现特定功能，如CI/CD管道中的标签、日志收集器的配置、监控系统的自定义指标等。

- 文档和注释：它们可以用来为资源添加人类可读的注释，帮助理解资源的目的或维护历史记录，比如记录上次手动更新的时间、修改者等。



----

### K8S组成
容器的编排管理平台，微服务支撑平台，可移植云平台。

    kubectl get nodes命令
    kubectl create -f hello-service.yml --record 服务部署
    kubectl describe [service]
    kubectl run 命令 创建容器
    kubectl create -f hello-deployment.yml --record 
    kubectl logs 

Kubernetes中部署的最小单位是pod，而不是Docker容器，pod是非持久化的实体。K8s由一组节点（node）组成，node可以是物理服务器，也可以是虚拟机。每个node上都有node组件，包括kubelet，kube-proxy。安装了master组件的节点是master节点。etcd是整个集群的主数据库。kutectl是超级命令行工具。


#### Kubernetes对象模型：
静态属性：一般用YML文件描述。

    Kind: Pod/Service/Deployment/....
    Metedata: Name, Namespace, Labels...
    Spec: Replicas, selector, ...

操作方法：API kubectl

    Create/Get/Update/Delete

动态信息：ETCD

    Status

例子：

_Pod部署文件_
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-app
spec:
  containers:
    - name: my-app
      image: my-app:1.0
      command: ["/opt/my-app/my-app"]
      args: ["-config", "/etc/config/config_local"]
      volumeMounts:
        - name: config-volume
          mountPath: /etc/config/
  volumes:
    - name: config-volume
      configMap:
        name: my-app-config
```

_Deployment部署文件_
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app-deployment
  labels:
    app: my-app
spec:
  replicas: 1
  selector:
    matchLabels:
      app: my-app
  template:
    metadata:
      labels:
        app: my-app
    spec:
      containers:
        - name: my-app
          image: arti.fwmrm.net/pqm/my-app:1.0
          command: ["/opt/my-app/my-app"]
          args: ["-config", "/etc/config/config_local"]
          volumeMounts:
            - name: config-volume
              mountPath: /etc/config/
      volumes:
        - name: config-volume
          configMap:
            name: my-app-config
```


### Ingress Controller
Nginx Ingress Controller

Daemonset or Deployment + Serivce

### Ingress

#### 安装
virtualbox：

    brew cask install virtualbox

minikube:

    curl -Lo minikube https://storage.googleapis.com/minikube/releases/v1.3.0/minikube-darwin-amd64 && chmod +x minikube && sudo cp minikube /usr/local/bin/ && rm minikube

Minikube自带了Docker引擎，所以我们需要重新配置客户端，让docker命令行与Minikube中的Docker进程通讯：
`eval $(minikube docker-env)`

复制代码在运行上面的命令后，再运行 docker image ls 时只能看到一些Minikube自带的镜像，就看不到我们刚才构建的 docker-demo:0.1 镜像了。所以在继续之前，要重新构建一遍我们的镜像。

The command minikube docker-env returns a set of Bash environment variable exports to configure your local environment to re-use the Docker daemon inside the Minikube instance.

Passing this output through eval causes bash to evaluate these exports and put them into effect.

You can review the specific commands which will be executed in your shell by omitting the evaluation step and running minikube docker-env directly. However, this will not perform the configuration – the output needs to be evaluated for that.

eval "$(docker-machine env -u)"  undo!

---

#### volumes
When a Container crashes, kubelet will restart it, but the files will be lost - the Container starts with a clean state.

When running Containers together in a Pod it is often necessary to share files between those Containers.

The Kubernetes Volume abstraction solves both of these problems.

A Kubernetes volume has an explicit lifetime - the same as the Pod that encloses it. Consequently, a volume outlives any Containers that run within the Pod, and data is preserved across Container restarts. Of course, when a Pod ceases to exist, the volume will cease to exist, too.

Kubernetes supports many types of volumes, and a Pod can use any number of them simultaneously.

At its core, a volume is just a directory, possibly with some data in it, which is accessible to the Containers in a Pod. To use a volume, a Pod specifies what volumes to provide for the Pod (the `.spec.volumes` field) and where to mount those into Containers (the `.spec.containers.volumeMounts` field).

any volumes are mounted at the specified paths within the image. Volumes can not mount onto other volumes or have hard links to other volumes. Each Container in the Pod must independently specify where to mount each volume.

#### type of volumes
##### awsElasticBlockStore
An awsElasticBlockStore volume mounts an Amazon Web Services (AWS) EBS Volume into your Pod. Unlike emptyDir, which is erased when a Pod is removed, the contents of an EBS volume are preserved and the volume is merely unmounted. This means that an EBS volume can be pre-populated with data, and that data can be “handed off” between Pods.

Caution: You must create an EBS volume using aws ec2 create-volume or the AWS API before you can use it.

There are some restrictions when using an awsElasticBlockStore volume:

- the nodes on which Pods are running must be AWS EC2 instances
- those instances need to be in the same region and availability-zone as the EBS volume
- EBS only supports a single EC2 instance mounting a volume


#### Persistent Volumes
two new API resources: `PersistentVolume` and `PersistentVolumeClaim`.

A PersistentVolume (PV) is a piece of storage in the cluster that has been provisioned by an administrator or dynamically provisioned using Storage Classes. It is a resource in the cluster just like a node is a cluster resource. PVs are volume plugins like Volumes, but have a lifecycle independent of any individual pod that uses the PV.

A PersistentVolumeClaim (PVC) is a request for storage by a user. It is similar to a pod. Pods consume node resources and PVCs consume PV resources. Pods can request specific levels of resources (CPU and Memory). Claims can request specific size and access modes (e.g., can be mounted once read/write or many times read-only).

While PersistentVolumeClaims allow a user to consume abstract storage resources, it is common that users need PersistentVolumes with varying properties, such as performance, for different problems. Cluster administrators need to be able to offer a variety of PersistentVolumes that differ in more ways than just size and access modes, without exposing users to the details of how those volumes are implemented. For these needs there is the StorageClass resource.


#### annotations

You can use either labels or annotations to attach metadata to Kubernetes objects. Labels can be used to select objects and to find collections of objects that satisfy certain conditions. In contrast, annotations are not used to identify and select objects. The metadata in an annotation can be small or large, structured or unstructured, and can include characters not permitted by labels.

Annotations, like labels, are key/value maps

---

# Helm Charts

Tiller, the server portion of Helm, typically runs inside of your Kubernetes cluster. But for development, it can also be run locally, and configured to talk to a remote Kubernetes cluster.

kubectl -n kube-system get pods|grep tiller

helm create test
helm会自动建立test目录，生成tree
├── Chart.yaml #Chart本身的版本和配置信息
├── charts #依赖的chart
├── templates #配置模板目录
│   ├── NOTES.txt #helm提示信息
│   ├── _helpers.tpl #用于修改kubernetes objcet配置的模板
│   ├── deployment.yaml #kubernetes Deployment object
│   └── service.yaml #kubernetes Serivce
└── values.yaml #kubernetes object configuration

Templates目录下是yaml文件的模板，遵循Go template语法。
其中的Values是在values.yaml文件中定义.


`helm install --dry-run --debug <chart_dir>`
查看验证chart配置。该输出中包含了模板的变量配置与最终渲染的yaml文件

`helm install .`最终部署。


我们可以修改Chart.yaml中的helm chart配置信息，然后使用下列命令将chart打包成一个压缩文件。

`helm package .`

`helm delete xxx`


Statefulset????

命令：
```bash
helm status druid-test

kubectl describe pod --namespace druid-dev-test spec-pusher-deployment-5cbb7

kubectl exec --namespace druid-dev-test spec-pusher-deployment-5cbb7849b7-nxbql ls /sbin

kubectl describe ingress --namespace druid-dev-test druid-test-router

helm upgrade --namespace "druid-dev-test" "druid-test" --debug ./druid-chart -f ./druid-chart/values.dev.yaml

kubectl logs -f --namespace druid-dev-test spec-pusher-deployment-5cbb7849b7-nxbql

# https://kubernetes.io/docs/reference/kubectl/cheatsheet/

kubectl get statefulset --namespace druid-dev-test druid-test-historical

kubectl exec -it dip-dev-dmoaqs-ui-deploy-7b89759784-79cx9 --namespace aqs-dev ./bin/bash

helm rollback aqs-dev 20

helm history linear-post-action --max 10
```
helm 2.9 statefulset delete.....




Kubeconfig????

token?

---

# RBAC

Role-based access control (RBAC)

An RBAC Role or ClusterRole contains rules that represent a set of permissions. Role有namespace, ClusterRole没有。里面都是定义一些权限规则。

A role binding grants the permissions defined in a role to a user or set of users. It holds a list of subjects (users, groups, or service accounts). 就是把规则和用户绑在一起。ClusterRoleBinding类似。


# 常见问题

---
```
"" is invalid: spec.selector: Invalid value: v1.LabelSelector{MatchLabels:map[string]string{"app":"my-app"}, MatchExpressions:[]v1.LabelSelectorRequirement(nil)}: field is immutable
```
这个问题的原因是，两个相同的Deployment（一个已部署，一个将要部署），但它们选择器不同。

--- 
mountPath结合subPath(也可解决多个configmap挂载同一目录，导致覆盖)作用 
```
volumeMounts:
  - mountPath: /etc/conf/  #conf下会只有volume中的config文件，其他的都会被覆盖。
    name: test

volumeMounts:
  - mountPath: /etc/conf/config  
    subPath: config        #conf原有文件还在，只有config会新增或者被覆盖。
    name: test
```



源码阅读
https://www.bookstack.cn/read/source-code-reading-notes/README.md



---

# 拓展内容：Kubernetes 相关工具，插件
## Kubeadm
Kubeadm 是 Google 开源的一个用于安装和初始化 Kubernetes 集群实例的工具，通过使用 Kubeadm 可以快速搭建满足最佳实践的 Kubernetes 集群。

相关链接：[Kubeadm](https://github.com/kubernetes/kubeadm)

## Kubespray
Kubespray 是 Google 开源的一个部署生产级别的 Kubernetes 服务器集群的开源项目，它整合了 Ansible 作为部署的工具。

相关链接：[Kubespray](https://github.com/kubernetes-sigs/kubespray)

## Minikube
Minikube 在 macOS、Linux 和 Windows 上实现了本地 Kubernetes 集群。Minikube 的主要目标是成为本地 Kubernetes 应用程序开发的最佳工具，并支持所有合适的 Kubernetes 功能。

相关链接：[minikube](https://github.com/kubernetes/minikube)

## Microk8s
Microk8s 是一款适用 42 种 Linux 发行版的完全符合标准的、轻量级的单机 Kubernetes，适用于：

- 开发人员工作站
- 物联网
- 边缘计算
- CI/CD

相关链接：[microk8s](https://github.com/ubuntu/microk8s)

## K3s
K3s 是轻量级的 Kubernetes，可用于生产，易于安装，只需要标准 Kubernetes 一半的内存，所有二进制文件不到 100MB 的 Kubernetes，适用于：

- 边缘计算
- 物联网
- CI
- 开发环境
- ARM
- 嵌入式系统

相关链接：[k3s](https://github.com/k3s-io/k3s)

## Kubectl
Kubectl 是 Kubernetes 官方开源的 Kubernetes 命令行客户端工具，使用 kubectl 可以连接并管理目标 Kubernetes 集群

相关链接：[kubectl](https://github.com/kubernetes/kubectl)

## Lens
Lens 是一款开源、免费、功能强大、易用的 Kubernetes 图形化客户端工具，支持 macOS、Windows 和 Liunx 操作系统

相关链接：[lens](https://github.com/lensapp/lens)

## Ingress-nginx
Ingress-nginx 是使用 Nginx 作为反向代理和负载均衡器的 Kubernetes Ingress 控制器。

相关链接：[ingress-nginx](https://github.com/kubernetes/ingress-nginx)

## Traefik
Traefik 是一个为了让部署微服务更加便捷而诞生的现代 HTTP 反向代理、负载均衡工具，它可以作为 Kubernetes Ingress 控制器使用。

相关链接：[traefik](https://github.com/traefik/traefik)

## MetalLB
MetalLB 是符合标准路由协议的，用于裸机 Kubernetes 集群使用的软件负载均衡器，它可以弥补自建 Kubernetes 因为没有硬件负载均衡器导致无法使用 LoadBalancer 类型 Service 的功能缺陷

相关链接：[MetalLB](https://github.com/metallb/metallb)

## Longhorn
Longhorn 是 Kubernetes 的分布式块存储系统，它轻巧，可靠且功能强大。

相关链接：[Longhorn](https://github.com/longhorn/longhorn)