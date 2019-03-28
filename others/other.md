## Kafka

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

## K8s





