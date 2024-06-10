# kube-scheduler

Kube-scheduler 是 kubernetes 的核心组件之一，也是所有核心组件之间功能比较单一的。kube-scheduler 的目的就是为每一个 pod 选择一个合适的 node，整体流程可以概括为三步，获取未调度的 podList，通过执行一系列调度算法为 pod 选择一个合适的 node，提交数据到 apiserver，其核心则是一系列调度算法的设计与执行。

kube-scheduler 目前包含两部分调度算法 predicates 和 priorities。

- 预选（Predicates）：输入是所有节点，输出是满足预选条件的节点。kube-scheduler根据预选策略过滤掉不满足策略的Nodes。如果某节点的资源不足或者不满足预选策略的条件则无法通过预选。如“Node的label必须与Pod的Selector一致”。
- 优选（Priorities）：输入是预选阶段筛选出的节点，优选会根据优先策略为通过预选的Nodes进行打分排名，选择得分最高的Node。例如，资源越富裕、负载越小的Node可能具有越高的排名。

抢占策略，在 pod 调度发生失败的时候尝试抢占低优先级的 pod，函数返回发生抢占的 node，被 抢占的 pods 列表，nominated node name 需要被移除的 pods 列表以及 error

## Predicates
默认的 predicates 调度算法主要分为五种类型：

1. 第一种类型叫作 GeneralPredicates，包含 PodFitsResources、PodFitsHost、PodFitsHostPorts、PodMatchNodeSelector 四种策略，其具体含义如下所示：

- PodFitsHost：检查宿主机的名字是否跟 Pod 的 spec.nodeName 一致
- PodFitsHostPorts：检查 Pod 申请的宿主机端口（spec.nodePort）是不是跟已经被使用的端口有冲突
- PodMatchNodeSelector：检查 Pod 的 nodeSelector 或者 nodeAffinity 指定的节点是否与节点匹配等
- PodFitsResources：检查主机的资源是否满足 Pod 的需求，根据实际已经分配（Request）的资源量做调度

kubelet 在启动 Pod 前，会执行一个 Admit 操作来进行二次确认，这里二次确认的规则就是执行一遍 GeneralPredicates。

2. 第二种类型是与 Volume 相关的过滤规则，主要有NoDiskConflictPred、MaxGCEPDVolumeCountPred、MaxAzureDiskVolumeCountPred、MaxCSIVolumeCountPred、MaxEBSVolumeCountPred、NoVolumeZoneConflictPred、CheckVolumeBindingPred。

3. 第三种类型是宿主机相关的过滤规则，主要是 PodToleratesNodeTaintsPred。

4. 第四种类型是 Pod 相关的过滤规则，主要是 MatchInterPodAffinityPred。

5. 第五种类型是新增的过滤规则，与宿主机的运行状况有关，主要有 CheckNodeCondition、 CheckNodeMemoryPressure、CheckNodePIDPressure、CheckNodeDiskPressure 四种。若启用了 TaintNodesByCondition FeatureGates 则在 predicates 算法中会将该四种算法移除，TaintNodesByCondition 基于 node conditions 当 node 出现 pressure 时自动为 node 打上 taints 标签，该功能在 v1.8 引入，v1.12 成为 beta 版本，目前 v1.16 中也是 beta 版本，但在 v1.13 中该功能已默认启用。

## priorities
定义了多个优先级函数，调度算法的逻辑是在 PrioritizeNodes()函数中，其目的是执行每个 priority 函数为 node 打分，分数为 0-10，其功能主要有：

- PrioritizeNodes() 通过并行运行各个优先级函数来对节点进行打分
- 每个优先级函数会给节点打分，打分范围为 0-10 分，0 表示优先级最低的节点，10表示优先级最高的节点
- 每个优先级函数有各自的权重
- 优先级函数返回的节点分数乘以权重以获得加权分数
- 最后计算所有节点的总加权分数

## 优先级 抢占机制
正常情况下，当一个 pod 调度失败后，就会被暂时 “搁置” 处于 pending 状态，直到 pod 被更新或者集群状态发生变化，调度器才会对这个 pod 进行重新调度。但在实际的业务场景中会存在在线与离线业务之分，若在线业务的 pod 因资源不足而调度失败时，此时就需要离线业务下掉一部分为在线业务提供资源，即在线业务要抢占离线业务的资源，此时就需要 scheduler 的优先级和抢占机制了，该机制解决的是 pod 调度失败时该怎么办的问题，若该 pod 的优先级比较高此时并不会被”搁置”，而是会”挤走”某个 node 上的一些低优先级的 pod，这样就可以保证高优先级的 pod 调度成功。

抢占发生的原因，一定是一个高优先级的 pod 调度失败，我们称这个 pod 为“抢占者”，称被抢占的 pod 为“牺牲者”(victims)。而 kubernetes 调度器实现抢占算法的一个最重要的设计，就是在调度队列的实现里，使用了两个不同的队列。

第一个队列叫作 activeQ，凡是在 activeQ 里的 pod，都是下一个调度周期需要调度的对象。所以，当你在 kubernetes 集群里新创建一个 pod 的时候，调度器会将这个 pod 入队到 activeQ 里面，调度器不断从队列里出队(pop)一个 pod 进行调度，实际上都是从 activeQ 里出队的。

第二个队列叫作 unschedulableQ，专门用来存放调度失败的 pod，当一个 unschedulableQ 里的 pod 被更新之后，调度器会自动把这个 pod 移动到 activeQ 里，从而给这些调度失败的 pod “重新做人”的机会。

当 pod 拥有了优先级之后，高优先级的 pod 就可能会比低优先级的 pod 提前出队，从而尽早完成调度过程。

## 优先级与抢占机制的使用
1、创建 PriorityClass 对象：
```yml
apiVersion: scheduling.k8s.io/v1
kind: PriorityClass
metadata:
  name: high-priority
value: 1000000
globalDefault: false
description: "This priority class should be used for XYZ service pods only."
```

2、在 deployment、statefulset 或者 pod 中声明使用已有的 priorityClass 对象即可

在 pod 中使用：
```yml
apiVersion: v1
kind: Pod
metadata:
  labels:
    app: nginx-a
  name: nginx-a
spec:
  containers:
  - image: nginx:1.7.9
    imagePullPolicy: IfNotPresent
    name: nginx-a
    ports:
    - containerPort: 80
      protocol: TCP
    resources:
      requests:
        memory: "64Mi"
        cpu: 5
      limits:
        memory: "128Mi"
        cpu: 5
  priorityClassName: high-priority
```
在 deployment 中使用：
```yml
  template:
    spec:
      containers:
      - image: nginx
        name: nginx-deployment
        priorityClassName: high-priority
```


通过API servert的watch接口监听新建Pod副本信息，并通过调度算法为Pod选择一个合适的Node。
检索复合Pod要求的Node列表。之后会绑定Pod到Node，然后将状态写入ETCD

## 练习：

简述Kubernetes Scheduler作用及实现原理

Kubernetes Scheduler是负责Pod调度的重要功能模块，Kubernetes Scheduler在整个系统中承担了“承上启下”的重要功能，“承上”是指它负责接收Controller Manager创建的新Pod，为其调度至目标Node；“启下”是指调度完成后，目标Node上的kubelet服务进程接管后继工作，负责Pod接下来生命周期。

Kubernetes Scheduler的作用是将待调度的Pod（API新创建的Pod、Controller Manager为补足副本而创建的Pod等）按照特定的调度算法和调度策略绑定（Binding）到集群中某个合适的Node上，并将绑定信息写入etcd中。

在整个调度过程中涉及三个对象，分别是待调度Pod列表、可用Node列表，以及调度算法和策略。

Kubernetes Scheduler通过调度算法调度为待调度Pod列表中的每个Pod从Node列表中选择一个最适合的Node来实现Pod的调度。随后，目标节点上的kubelet通过API Server监听到Kubernetes Scheduler产生的Pod绑定事件，然后获取对应的Pod清单，下载Image镜像并启动容器。

