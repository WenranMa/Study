
# Docker
    Docker不是虚拟机，但可以理解为轻量的虚拟机。Docker可以让开发者打包他们的应用以及依赖包到一个轻量级、可移植的容器中，然后发布到任何流行的Linux机器上。
    容器是完全使用沙箱机制，相互之间不会有任何接口（类似iPhone的app)，更重要的是容器性能开销极低。

![Docker Architecture](./img/architecture_docker.svg)

    Docker 包括三个基本概念:
    镜像（Image）
    容器（Container）
    仓库（Repository）

#### 镜像（Image）
    An image is an executable package that includes everything needed to run an application.
    the code, a runtime, libraries, environment variables, and configuration files.

    一个特殊的文件系统，操作系统分为内核和用户空间。
    对于Linux而言，内核启动后，会挂载root文件系统为其提供用户空间支持。
    而Docker镜像（Image），就相当于是一个root文件系统。
    Docker镜像是一个特殊的文件系统，除了提供容器运行时所需的程序、库、资源、配置等文件外，还包含了一些为运行时准备的一些配置参数（如环境变量、用户等）。 
    镜像不包含任何动态数据，其内容在构建之后也不会被改变。

    Docker设计时，就充分利用Union FS的技术(联合文件)，将其设计为分层存储的架构。
    镜像实际是由多层文件系统联合组成。镜像构建时，会一层层构建，前一层是后一层的基础。
    每一层构建完就不会再发生改变，后一层上的任何改变只发生在自己这一层。
    比如，删除前一层文件的操作，实际不是真的删除前一层的文件，而是仅在当前层标记为该文件已删除。
    在最终容器运行的时候，虽然不会看到这个文件，但是实际上该文件会一直跟随镜像。
    分层存储的特征还使得镜像的复用、定制变的更为容易。甚至可以用之前构建好的镜像作为基础层，然后进一步添加新的层，以定制自己所需的内容，构建新的镜像。

#### 容器（Container)
     A container is launched by running an image, an instance of an image.
     What the image becomes in memory when executed (that is, an image with state, or a user process).

    镜像运行时的实体。镜像（Image）和容器（Container）的关系，就像是面向对象程序设计中的类和实例一样，镜像是静态的定义，容器是镜像运行时的实体。
    容器可以被创建、启动、停止、删除、暂停等 。
    容器的实质是进程，但与直接在宿主执行的进程不同，容器进程运行于属于自己的独立的命名空间。
    前面讲过镜像使用的是分层存储，容器也是如此。
    容器存储层的生存周期和容器一样，容器消亡时，容器存储层也随之消亡。因此，任何保存于容器存储层的信息都会随容器删除而丢失。
    按照Docker最佳实践的要求，容器不应该向其存储层内写入任何数据，容器存储层要保持无状态化。
    所有的文件写入操作，都应该使用数据卷（Volume）来提供独立于容器之外的持久化存储。
    或者绑定宿主目录，在这些位置的读写会跳过容器存储层，直接对宿主(或网络存储)发生读写，其性能和稳定性更高。
    数据卷的生存周期独立于容器，容器消亡，数据卷不会消亡。因此，使用数据卷后，容器可以随意删除、重新run，数据却不会丢失。

#### 仓库（Repository）
    集中存放镜像文件的地方。
    镜像构建完成后，可以很容易的在当前宿主上运行，但是如果需要在其它服务器上使用这个镜像，我们就需要一个集中的存储、分发镜像的服务，Docker Registry就是这样的服务。
    一个Docker Registry中可以包含多个仓库（Repository），每个仓库可以包含多个标签（Tag），每个标签对应一个镜像(版本)。
    镜像仓库是Docker用来集中存放镜像文件的地方类似于我们之前常用的代码仓库。
    通常，一个仓库会包含同一个软件不同版本的镜像，而标签就常用于对应该软件的各个版本。我们可以通过<仓库名>:<标签>的格式来指定具体是这个软件哪个版本的镜像。
    如果不给出标签，将以latest作为默认标签。

    最常使用的Registry公开服务是官方的Docker Hub，这也是默认的Registry，并拥有大量的高质量的官方镜像，网址为：hub.docker.com/。
    国内也有一些云服务商提供类似于 Docker Hub 的公开服务。比如时速云镜像库、网易云镜像服务、DaoCloud 镜像市场、阿里云镜像库等。

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

## Dockerfile 
    可以用dockerfile来创建镜像。

    FROM alpine:latest
    MAINTAINER wrma
    CMD echo "Hello docker!"

    docker build -t hello_docker .
    docker images hello_docker
    docker run hello_docker


    第二个例子：
    mkdir docker_file
    cd docker_file
    touch Dockerfile
    vi Dockerfile

    FROM ubuntu
    MAINTAINER wrma
    RUN sed -i 's/archive.ubuntu.com/mirrors.ustc.edu.cn/g' /etc/apt/sources.list
    RUN apt-get update
    RUN apt-get install -y nginx
    COPY index.html /var/www/html
    ENTRYPOINT ["/usr/sbin/nginx", "-g", "daemon off;"]
    EXPOSE 80

    touch index.html
    vi index.html  随便填点什么
    docker build -t wrma/hello_nginx .
    docker run -d -p 80:80 wrma/hello_nginx

    语法：
    FROM base image
    RUN 执行命令
    ADD 添加文件
    COPY 拷贝文件
    CMD 执行命令
    EXPOSE 暴露端口

    镜像分层，dockerfile中每一行都是一个新层



The docker build command builds an image from a Dockerfile and a context. The build’s context is the set of files at a specified location PATH or URL. The PATH is a directory on your local filesystem. The URL is a Git repository location.

A context is processed recursively. So, a PATH includes any subdirectories and the URL includes the repository and its submodules.

The build is run by the Docker daemon, not by the CLI. The first thing a build process does is send the entire context (recursively) to the daemon. In most cases, it’s best to start with an empty directory as context and keep your Dockerfile in that directory. Add only the files needed for building the Dockerfile.

Here is the format of the Dockerfile:

    # Comment
    INSTRUCTION arguments

The instruction is not case-sensitive. However, convention is for them to be UPPERCASE to distinguish them from arguments more easily.

Docker runs instructions in a Dockerfile in order. A Dockerfile must start with a `FROM` instruction. The FROM instruction specifies the Base Image from which you are building.

Docker treats lines that begin with # as a comment, unless the line is a valid parser directive. A # marker anywhere else in a line is treated as an argument.

#### Paser Directives
syntax
escape

#### Environment Replacement
变量替换。declared with the `ENV` statement.

    FROM busybox
    ENV foo /bar
    WORKDIR ${foo}   # WORKDIR /bar
    ADD . $foo       # ADD . /bar
    COPY \$foo /quux # COPY $foo /quux


#### .dockerignore
忽略的目录和文件。


##### FROM
The `FROM` instruction initializes a new build stage and sets the Base Image for subsequent instructions. As such, a valid Dockerfile must start with a FROM instruction.

##### RUN
The `RUN` instruction will execute any commands in a new layer on top of the current image and commit the results. The resulting committed image will be used for the next step in the Dockerfile.

##### CMD
There can only be one CMD instruction in a Dockerfile. If you list more than one CMD then only the last CMD will take effect.

The main purpose of a CMD is to provide defaults for an executing container. These defaults can include an executable, or they can omit the executable, in which case you must specify an ENTRYPOINT instruction as well.

##### ADD
ADD has two forms:

    ADD [--chown=<user>:<group>] <src>... <dest>
    ADD [--chown=<user>:<group>] ["<src>",... "<dest>"] (this form is required for paths containing whitespace)

The ADD instruction copies new files, directories or remote file URLs from `<src>` and adds them to the filesystem of the image at the path `<dest>`.

##### COPY
COPY has two forms:

    COPY [--chown=<user>:<group>] <src>... <dest>
    COPY [--chown=<user>:<group>] ["<src>",... "<dest>"] (this form is required for paths containing whitespace)

The COPY instruction copies new files or directories from `<src>` and adds them to the filesystem of the container at the path `<dest>`.


docker网络
1. Bridge  端口映射
2. Host
3. None

docker run -p 主机端口:容器端口
docker run -P 所有端口随机映射


This port remapping of 4000:80 demonstrates the difference between EXPOSE within the Dockerfile and what the publish value is set to when running docker run -p.
In later steps, map port 4000 on the host to port 80 in the container and use http://localhost.

### Multi stage build

docker rm $(docker ps -aq) 删除所有container
docker rmi $(docker images -q) 删除所有image

exmaple:
```bash
# Stage 1:

# Start from the golang alpine as base image
FROM golang:1.11-alpine as builder

# Set the Working Directory inside the container
WORKDIR /go/src/app

# Copy the source from the current directory to the Working Directory inside the container
COPY . .

# Build the app spec-pusher
RUN go build

# enter point to the program
# ENTRYPOINT ["/go/src/spec-pusher/spec-pusher"]
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
# RUN chmod +x /root/spec-pusher/spec-pusher

# Entry point
ENTRYPOINT ["/root/app"]

# For pass arguments, only for test.
CMD []
```



---

## K8s
### 部署变迁
    1. 单机模式，IBM, SUN
    2. 虚拟化，VMware等，将单机划分为多个虚拟机，充分利用单机。
    基于虚拟机技术的Amazon Web Service。
    3. 虚拟化成熟。
    服务模式：IaaS, PaaS, SaaS?
    4. 容器化，Docker。
    5. 云原生，容器+微服务。K8S

### K8S
    容器的编排管理平台，微服务支撑平台，可移植云平台。

    kubectl get nodes命令
    kubectl create -f hello-service.yml --record 服务部署
    kubectl describe [service]
    kubectl run 命令 创建容器
    kubectl create -f hello-deployment.yml --record 
    kubectl logs 

### K8S架构
    有一组节点（node）组成，node可以是物理服务器，也可以是虚拟机。
    每个node上都有node组件，包括kubelet，kube-proxy。
    安装了master组件的节点是master节点。
    etcd是整个集群的主数据库。
    kutectl是超级命令行工具。

#### master组件
    所有的控制命令到传递给maste组件并在上面执行。
    K8S集群至少有一套master组件。
    Scheduler, Controller Manager, API Server, ETCD.
    API Server是核心。