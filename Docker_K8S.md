# Docker

虚拟机技术：将物理服务器虚拟成多个逻辑服务器。
![hypervisor](/img/hypervisor.JPG)

每个虚拟机都右完整的操作系统，之间彼此隔离。因为运行完整的操作系统，所以速度慢。
![hypervisor1](/img/hypervisor_1.JPG)

Docker不是虚拟机，但可以理解为轻量的虚拟机。Docker可以让开发者打包他们的应用以及依赖包到一个轻量级、可移植的容器中，然后发布到任何流行的Linux机器上。
![docker](/img/docker.JPG)

## Docker 包括三个基本概念:
- 镜像（Image）
- 容器（Container）
- 仓库（Repository）

### 镜像（Image）
An image is an executable package that includes everything needed to run an application, the code, a runtime, libraries, environment variables, and configuration files.

操作系统分为内核和用户空间，对于Linux而言，内核启动后，会挂载root文件系统为其提供用户空间支持。

而Docker image就相当于是一个root文件系统，是一个特殊的文件系统，除了提供容器运行时所需的程序、库、资源、配置等文件外，还包含了一些为运行时准备的一些配置参数（如环境变量、用户等）。镜像不包含任何动态数据，其内容在构建之后也不会被改变。

利用Union FS的技术(联合文件)，将其设计为分层存储的架构。镜像构建时，会一层层构建，前一层是后一层的基础。
每一层构建完就不会再发生改变，后一层上的任何改变只发生在自己这一层。分层存储的特征还使得镜像的复用、定制变的更为容易。甚至可以用之前构建好的镜像作为基础层，然后进一步添加新的层，以定制自己所需的内容，构建新的镜像。

### 容器（Container)
A container is launched by running an image, an instance of an image. What the image becomes in memory when executed (that is, an image with state, or a user process).

镜像运行时的实体。镜像（Image）和容器（Container）的关系，就像是面向对象程序设计中的类和实例一样，镜像是静态的定义，容器是镜像运行时的实体。容器可以被创建、启动、停止、删除、暂停等 。容器的实质是进程，但与直接在宿主执行的进程不同，容器进程运行于属于自己的独立的命名空间。

容器也是分层存储。容器存储层的生存周期和容器一样，容器消亡时，容器存储层也随之消亡。因此，任何保存于容器存储层的信息都会随容器删除而丢失。按照Docker最佳实践的要求，容器不应该向其存储层内写入任何数据，容器存储层要保持无状态化。所有的文件写入操作，都应该使用数据卷（Volume）来提供独立于容器之外的持久化存储。或者绑定宿主目录，在这些位置的读写会跳过容器存储层，直接对宿主(或网络存储)发生读写，其性能和稳定性更高。

容器是完全使用沙箱机制，相互之间不会有任何接口（类似iPhone的app)，更重要的是容器性能开销极低。？？？

### 仓库（Repository）
集中存放镜像文件的地方。镜像构建完成后，可以很容易的在当前宿主上运行，但是如果需要在其它服务器上使用这个镜像，我们就需要一个集中的存储、分发镜像的服务，Docker Registry就是这样的服务。一个Docker Registry中可以包含多个仓库（Repository），每个仓库可以包含多个标签（Tag），每个标签对应一个镜像(版本)。我们可以通过<仓库名>:<标签>的格式来指定具体是这个软件哪个版本的镜像。如果不给出标签，将以latest作为默认标签。

最常使用的Registry公开服务是官方的Docker Hub(hub.docker.com)。

## Client-Server
Docker是client server模式。Docker Daemon是服务端的守护进程，负责管理Docker的各种资源。各种docker命令都是通过docker客户端发送给docker daemon，处理后再返回给docker client。
![Docker Architecture](./img/architecture_docker.svg)

## 命令
    docker run ubuntu echo hello docker 是用一个Ubuntu镜像运行ehco hello docker命令。
    docker run nginx 启动一个nginx容器。
    docker pull 获取image。
    docker build 创建image。
    docker images 可以看本地所有镜像。
    docker run 启动container。
    docker ps 可以查看运行中的container。
    docker stop [container id] 来停止容器。
    docker rmi 删除image。
    docker rm 删除container。
    docker cp 在host和container之间拷贝文件。
    docker commit 保存改动为新的image。

    docker search 搜索镜像。
    docker tag [imagename] [username] 给镜像打tag
    docker push [imagename] 提交打registry

    docker run -d 后台运行
    docker exec 在运行的容器中运行命令 （-i，-t）

    docker rm $(docker ps -aq) 删除所有container
    docker rmi $(docker images -q) 删除所有image

## Dockerfile 
可以用Dockerfile来创建镜像。例如：
```bash
FROM ubuntu
RUN sed -i 's/archive.ubuntu.com/mirrors.ustc.edu.cn/g' /etc/apt/sources.list
RUN apt-get update
RUN apt-get install -y nginx
COPY index.html /var/www/html
ENTRYPOINT ["/usr/sbin/nginx", "-g", "daemon off;"]
EXPOSE 80
```
then build and run the image:
```bash
touch index.html
vi index.html  随便填点什么
docker build -t wrma/hello_nginx .
docker run -d -p 80:80 wrma/hello_nginx
```

The docker build command builds an image from a Dockerfile and a context. The build’s context is the set of files at a specified location PATH or URL. The PATH is a directory on your local filesystem. The URL is a Git repository location.

A context is processed recursively. So, a PATH includes any subdirectories and the URL includes the repository and its submodules.

The build is run by the Docker daemon, not by the CLI. The first thing a build process does is send the entire context (recursively) to the daemon. In most cases, it’s best to start with an empty directory as context and keep your Dockerfile in that directory. Add only the files needed for building the Dockerfile.

Here is the format of the Dockerfile:

    # Comment
    INSTRUCTION arguments

The instruction is not case-sensitive. However, convention is for them to be UPPERCASE to distinguish them from arguments more easily.

Docker runs instructions in a Dockerfile in order. A Dockerfile must start with a `FROM` instruction. The FROM instruction specifies the Base Image from which you are building.

Docker treats lines that begin with # as a comment, unless the line is a valid parser directive. A # marker anywhere else in a line is treated as an argument.

镜像分层，Dockerfile中每一行都是一个新层。

### FROM
The `FROM` instruction initializes a new build stage and sets the Base Image for subsequent instructions. As such, a valid Dockerfile must start with a FROM instruction.

### RUN 执行命令
The `RUN` instruction will execute any commands in a new layer on top of the current image and commit the results. The resulting committed image will be used for the next step in the Dockerfile.

### CMD
There can only be one CMD instruction in a Dockerfile. If you list more than one CMD then only the last CMD will take effect. 常用于传递命令参数。

The main purpose of a CMD is to provide defaults for an executing container. These defaults can include an executable, or they can omit the executable, in which case you must specify an ENTRYPOINT instruction as well.

### ADD 添加文件
ADD has two forms:

    ADD [--chown=<user>:<group>] <src>... <dest>
    ADD [--chown=<user>:<group>] ["<src>",... "<dest>"] (this form is required for paths containing whitespace)

The ADD instruction copies new files, directories or remote file URLs from `<src>` and adds them to the filesystem of the image at the path `<dest>`.

### COPY
COPY has two forms:

    COPY [--chown=<user>:<group>] <src>... <dest>
    COPY [--chown=<user>:<group>] ["<src>",... "<dest>"] (this form is required for paths containing whitespace)

The COPY instruction copies new files or directories from `<src>` and adds them to the filesystem of the container at the path `<dest>`.

这里的source是相对于Dockerfile的路径，dest目标路径是相对于镜像的路径。

### EXPOSE 暴露端口
    docker run -p 主机端口:容器端口
    docker run -P 所有端口随机映射

This port remapping of 4000:80 demonstrates the difference between EXPOSE within the Dockerfile and what the publish value is set to when running docker run -p.
In later steps, map port 4000 on the host to port 80 in the container and use http://localhost.

### Paser Directives
syntax
escape

### Environment Replacement
变量替换。declared with the `ENV` statement.

    FROM busybox
    ENV foo /bar
    WORKDIR ${foo}   # WORKDIR /bar
    ADD . $foo       # ADD . /bar
    COPY \$foo /quux # COPY $foo /quux

### .dockerignore
忽略的目录和文件，类似.gitignore文件。

## Multi stage build
例如：
```bash
# Stage 1:

# Start from the golang alpine as base image
FROM golang:1.11-alpine as builder

# Set the Working Directory inside the container
WORKDIR /go/src/app

# Copy the source from the current directory to the Working Directory inside the container
COPY . .

# Build the app my-app
RUN go build

# enter point to the program
# ENTRYPOINT ["/go/src/my-app/my-app"]
# CMD []

# Stage 2:

# Start from alpine system as base image:
FROM alpine:latest

# Add Maintainer Info
LABEL maintainer="Wenran Ma <mawenran@gmail.com>"

# Set the Working Directory inside the container
WORKDIR /root

# Copy binary from previous stage to working dir
COPY --from=builder /go/src/app ./

# Set permission, no need actually
# RUN chmod +x /root/my-app/my-app

# Entry point
ENTRYPOINT ["/root/app"]

# For pass arguments, only for test.
CMD []
```

## Docker compose
Compose is a tool for defining and running multi-container Docker applications. With Compose, you use a YAML file to configure your application’s services. Then, with a single command, you create and start all the services from your configuration.


---

# Kubernetes
### 部署变迁
1. 单机模式，IBM, SUN
2. 虚拟化，VMware等，将单机划分为多个虚拟机，充分利用单机。基于虚拟机技术的Amazon Web Service。
3. 虚拟化成熟。服务模式：IaaS, PaaS, SaaS?
4. 容器化，Docker。
5. 云原生，容器+微服务。K8S

### K8S组成
容器的编排管理平台，微服务支撑平台，可移植云平台。

    kubectl get nodes命令
    kubectl create -f hello-service.yml --record 服务部署
    kubectl describe [service]
    kubectl run 命令 创建容器
    kubectl create -f hello-deployment.yml --record 
    kubectl logs 

Kubernetes中部署的最小单位是pod，而不是Docker容器，pod是非持久化的实体。K8s由一组节点（node）组成，node可以是物理服务器，也可以是虚拟机。每个node上都有node组件，包括kubelet，kube-proxy。安装了master组件的节点是master节点。etcd是整个集群的主数据库。kutectl是超级命令行工具。

#### master组件
所有的控制命令到传递给maste组件并在上面执行。K8S集群至少有一套master组件。
master构成：Scheduler, Controller Manager, API Server, ETCD.

API Server是核心。是集群控制的唯一入口，是Rest API的核心组件。

Scheduler通过API servert的watch接口监听新建Pod副本信息，并通过调度算法为Pod选择一个合适的Node。
检索复合Pod要求的Node列表。之后会绑定Pod到Node，然后将状态写入ETCD。

ControllerManager，没中资源都会有相应controller, controller manager就是管理这些controller。

ETCD默认与Master在同一个Node上。

#### Node
K8s集群真正的工作负载节点。Pod被分配到某个Node上。K8s通过node controller对node资源进行管理，支持动态删除和添加node。每个node上有Kubelet和Kube proxy。

Kubelet，服务进程组件，本身是非容器的组件。Pod的创建，启停等管理服务。

Kube proxy，Service抽象概念的实现，将Service的请求分发到Pod上。

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

#### Service

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



### Ingress Controller
Nginx Ingress Controller


Daemonset or Deployment + Serivce






### Ingress




#### Docker entry and cmd overwritten.

When you override the default Entrypoint and Cmd, these rules apply:

1. If you do not supply command or args for a Container, the defaults defined in the Docker image are used.
2. If you supply a command but no args for a Container, only the supplied command is used. The default EntryPoint and the default Cmd defined in the Docker image are ignored.
3. If you supply only args for a Container, the default Entrypoint defined in the Docker image is run with the args that you supplied.
4. If you supply a command and args, the default Entrypoint and the default Cmd defined in the Docker image are ignored. Your command is run with your args.

Here are some examples:

|  Image Entrypoint | Image Cmd | Container command | Container args | Command run    |
| ----------------- | --------- | ----------------- | -------------- | -------------- |
|    [/ep-1]        | [foo bar] | not set           | not set        | [ep-1 foo bar] |
|    [/ep-1]        | [foo bar] | [/ep-2]           | not set        | [ep-2]         |
|    [/ep-1]        | [foo bar] | not set           | [zoo boo]      | [ep-1 zoo boo] |
|    [/ep-1]        | [foo bar] | [/ep-2]           | [zoo boo]      | [ep-2 zoo boo] |

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
```
helm status druid-test

kubectl describe pod --namespace druid-dev-test spec-pusher-deployment-5cbb7

kubectl exec --namespace druid-dev-test spec-pusher-deployment-5cbb7849b7-nxbql ls /sbin

kubectl describe ingress --namespace druid-dev-test druid-test-router

helm upgrade --namespace "druid-dev-test" "druid-test" --debug ./druid-chart -f ./druid-chart/values.dev.yaml

kubectl logs -f --namespace druid-dev-test spec-pusher-deployment-5cbb7849b7-nxbql

https://kubernetes.io/docs/reference/kubectl/cheatsheet/

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
