# Deployment

kube-controller-manager 中有数十个 controller， deployment controller是其中之一，用的最多。

deployment 是 kubernetes 中用来部署无状态应用的一个对象，也是最常用的一种对象。

deployment 的本质是控制 replicaSet，replicaSet 会控制 pod，然后由 controller 驱动各个对象达到期望状态。

## 删除

当删除 deployment 对象时，仅仅是判断该对象中是否存在 metadata.DeletionTimestamp 字段，然后进行一次状态同步，并没有看到删除 deployment、rs、pod 对象的操作，其实删除对象并不是在此处进行而是在 kube-controller-manager 的垃圾回收器(garbagecollector controller)中完成的，此外在删除对象时还需要指定一个删除选项(orphan、background 或者 foreground)来说明该对象如何删除。

## 回滚

kubernetes 中的每一个 Deployment 资源都包含有 revision 这个概念，并且其 .spec.revisionHistoryLimit 字段指定了需要保留的历史版本数，默认为10，每个版本都会对应一个 rs，若发现集群中有大量 0/0 rs 时请不要删除它，这些 rs 对应的都是 deployment 的历史版本，否则会导致无法回滚。当一个 deployment 的历史 rs 数超过指定数时，deployment controller 会自动清理。

## 更新
1. 滚动更新

2. deployment 的另一种更新策略recreate 就比较简单粗暴了，当更新策略为 Recreate 时，deployment 先将所有旧的 rs 缩容到 0，并等待所有 pod 都删除后，再创建新的 rs。

rolloutRecreate 方法主要逻辑为：

    1、获取 newRS 和 oldRSs；
    2、缩容 oldRS replicas 至 0；
    3、创建 newRS；
    4、扩容 newRS；
    5、同步 deployment 状态；


## replicaset

在平时的操作中其实我们并不会直接操作 replicaset，replicaset 也仅有几个简单的操作，创建、删除、更新等，但其地位是非常重要的，replicaset 的主要功能就是通过 add/del pod 来达到期望的状态。

### manageReplicas
manageReplicas 是最核心的方法，它会计算 replicaSet 需要创建或者删除多少个 pod 并调用 apiserver 的接口进行操作，在此阶段仅仅是调用 apiserver 的接口进行创建，并不保证 pod 成功运行，如果在某一轮，未能成功创建的所有 Pod 对象，则不再创建剩余的 pod。一个周期内最多只能创建或删除 500 个 pod，若超过上限值未创建完成的 pod 数会在下一个 syncLoop 继续进行处理。

该方法主要逻辑如下所示：

1. 计算已存在 pod 数与期望数的差异；
2. 如果 diff < 0 说明 rs 实际的 pod 数未达到期望值需要继续创建 pod，首先会将需要创建的 pod 数在 expectations 中进行记录，然后调用 slowStartBatch 创建所需要的 pod，slowStartBatch 以指数级增长的方式批量创建 pod，创建 pod 过程中若出现 timeout err 则忽略，若为其他 err 则终止创建操作并更新 expectations；
3. 如果 diff > 0 说明可能是一次缩容操作需要删除多余的 pod，如果需要删除全部的 pod 则直接进行删除，否则会通过 getPodsToDelete 方法筛选出需要删除的 pod，具体的筛选策略在下文会将到，然后并发删除这些 pod，对于删除失败操作也会记录在 expectations 中；

在 slowStartBatch 中会调用 rsc.podControl.CreatePodsWithControllerRef 方法创建 pod，若创建 pod 失败会判断是否为创建超时错误，或者可能是超时后失败，但此时认为超时并不影响后续的批量创建动作，大家知道，创建 pod 操作提交到 apiserver 后会经过`认证、鉴权、以及动态访问控制`三个步骤，此过程有可能会超时，即使真的创建失败了，等到 expectations 过期后在下一个 syncLoop 时会重新创建。

若 diff > 0 时再删除 pod 阶段会调用getPodsToDelete 对 pod 进行筛选操作，此阶段会选出最劣质的 pod，下面是用到的 6 种筛选方法：

1. 判断是否绑定了 node：Unassigned < assigned；
2. 判断 pod phase：PodPending < PodUnknown < PodRunning；
3. 判断 pod 状态：Not ready < ready；
4. 若 pod 都为 ready，则按运行时间排序，运行时间最短会被删除：empty time < less time < more time；
5. 根据 pod 重启次数排序：higher restart counts < lower restart counts；
6. 按 pod 创建时间进行排序：Empty creation time pods < newer pods < older pods；

## 练习

简述Kubernetes deployment升级策略

    在Deployment的定义中，可以通过spec.strategy指定Pod更新的策略，目前支持两种策略：Recreate（重建）和RollingUpdate（滚动更新），默认值为RollingUpdate。

    - Recreate：设置spec.strategy.type=Recreate，表示Deployment在更新Pod时，会先杀掉所有正在运行的Pod，然后创建新的Pod。
    - RollingUpdate：设置spec.strategy.type=RollingUpdate，表示Deployment会以滚动更新的方式来逐个更新Pod。同时，可以通过设置spec.strategy.rollingUpdate下的两个参数（maxUnavailable和maxSurge）来控制滚动更新的过程。

    maxSurge
    指定升级期间存在的总Pod对象数量最多可超出期望值的个数，可以是百分比，也可以是具体的值。默认为1。

    例如: 期望的值是5，maxSurge的属性是2，则表示Pod对象总数不能超过6个。计算公式: 5+(5×20%)=6

    maxUnavailable

    升级期间不可用的Pod副本数(包括新版本)最多不能低于期望值的个数，默认值为1；
    例如: 期望的值为5个，maxunavailable属性为2，则Pod处于正常的状态至少有4个，计算公式: 5-(5×20%)=4。


无状态服务一般使用什么方式进行部署？

    Deployment 为 Pod 和 ReplicaSet 提供了一个 声明式定义方法，通常被用来部署无状态服务。

    Deployment 的主要作用：

    定义 Deployment 来创建 Pod 和 ReplicaSet 滚动升级和回滚应用扩容和索容暂停和继续。Deployment不仅仅可以滚动更新，而且可以进行回滚，如果发现升级到 V2 版本后，服务不可用，可以迅速回滚到 V1 版本。



简述Kubernetes deployment升级过程 ？？？？？？？？？？ 不确定

- 初始创建Deployment时，系统创建了一个ReplicaSet，并按用户的需求创建了对应数量的Pod副本。
- 当更新Deployment时，系统创建了一个新的ReplicaSet，并将其副本数量扩展到1，然后将旧ReplicaSet缩减为2。
- 之后，系统继续按照相同的更新策略对新旧两个ReplicaSet进行逐个调整。
- 最后，新的ReplicaSet运行了对应个新版本Pod副本，旧的ReplicaSet副本数量则缩减为0。