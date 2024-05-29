# gRPC

## 微服务

单体架构缺点：
- 一旦某个服务器挂了，整体不可用，隔离性差。
- 只能整体伸缩，浪费资源，可伸缩性差。（比如某个模块需要经常用，某个模块用的少）
- 代码都在一起。

微服务：
- 独立开发
- 独立部署
- 故障隔离
- 混合技术栈  – 可以使用不同的语言和技术来构建同一应用程序的不同服务
- 粒度缩放  – 单个组件可根据需要进行缩放，无需将所有组件缩放在一起

- 解决单体架构问题。
- 代码冗余，会有重复代码。
- 服务之前存在进程间的调用关系。



存在调用关系，自然想到http，但性能差？

引入RPC，gRPC是RPC框架的具体实现。

客户端，服务端通信过程：
- 客户端发送数据，以字节流方式传输。
- 接收字节流，解析，服务端执行方法，返回数据。

gRPC基于服务定义的思想，通过描述来定义一个服务，描述方法和语言无关。这个描述定义了服务名称，服务方法，客户端只需要调用定义好的方法，服务端用什么语言实现无所谓。

### 服务治理

比如某个微服务有上百个机器，那调用方该选择调用具体哪个服务呢？
这个逻辑不应该再调用方实现，所以有了服务治理。

这里一个重要的概念，服务发现，服务发现中一个重要概念叫注册中心。

每个服务启动时向注册中心注册自身ip等信息。调用方向注册中心请求地址。

服务容错，链路追踪？



## Protocal Buffers
数据结构序列化机制。

字节流就是二进制传输，客户端和服务端不认识。

序列化：将数据结构或对象转换成二进制字节流的过程。

反序列化：将字节流转换为程序认识的数据结构或对象的过程。

Protobuf是google开源的一种数据格式。

优势：
- 序列化后体积比Json或者xml小很多，适合网络传输。
- 跨平台多语言，兼容性好。
- 序列化和反序列化速度快。？


底层使用的HTTP2协议，

http2.0有headers frame, data frame, 对应http1.1的header和body。 

gRPC就是将数据序列化之后放入data frame中。

### Message

```
syntax = "proto3"; 

option go_package = .;service;

service SayHello {
  rpc SayHello(HelloRequest) returns (HelloResponse) {}
}

message HelloRequest {
  string query = 1;
  int32 page_number = 2;
  int32 result_per_page = 3;
}

message HelloResponse {
  string respnseMessage = 1;
}
```

必须以syntax为第一行。
每个field要有一个唯一的数字，最小是1，1到15用1byte编码，16到2047用2byte。

## 认证和安全传输

认证：多个server和client之间，如何识别对方，可以进行安全的数据传输。
- SSL/TLS（http2协议）
- token
- 没有措施，不安全（http1)
- 自定义

### Https相关知识

#### HTTPS、SSL、TLS
1. Http

首先，HTTP 是一个网络协议，是专门用来帮你传输 Web 内容滴。比如浏览器地址栏的如下的网址 https://wenranma.com 这就是指 HTTP 协议。大部分网站都是通过 HTTP 协议来传输 Web 页面、以及 Web 页面上包含的各种资源（图片、CSS 样式、JS 脚本）。

2. SSL/TLS

SSL 是“Secure Sockets Layer”的缩写，中文叫做“安全套接层”。它是在上世纪90年代中期，由网景公司设计的。（顺便插一句，网景公司不光发明了 SSL，还发明了很多 Web 的基础设施——比如“CSS 样式表”和“JS 脚本”）原先互联网上使用的 HTTP 协议是明文的，存在很多缺点——比如传输内容会被偷窥（嗅探）和篡改。发明 SSL 协议，就是为了解决这些问题。到了1999年，SSL 因为应用广泛，已经成为互联网上的事实标准。IETF 就在那年把 SSL 标准化。标准化之后的名称改为 TLS（是“Transport Layer Security”的缩写），中文叫做“传输层安全协议”。很多相关的文章都把这两者并列称呼（SSL/TLS），因为这两者可以视作同一个东西的不同阶段。

SSL 和 TLS 协议解决三个问题：可以为通信双方提供`识别和认证`通道，从而保证通信的`机密性`和`数据完整性`。

3. HTTPS

通常所说的 HTTPS 协议，说白了就是“HTTP 协议”和“SSL/TLS 协议”的组合。你可以把 HTTPS 大致理解为——“HTTP over SSL”或“HTTP over TLS”（反正 SSL 和 TLS 差不多）。

作为背景知识介绍，还需要再稍微谈一下 HTTP 协议本身的特点。HTTP 本身有很多特点，这里只说和 HTTPS 相关的特点。

1. HTTP 和 TCP 之间的关系

简单地说，TCP 协议是 HTTP 协议的基石——HTTP 协议需要依靠 TCP 协议来传输数据。

在网络分层模型中，TCP 被称为“传输层协议”，而 HTTP 被称为“应用层协议”

有很多常见的应用层协议是以 TCP 为基础的，比如“FTP、SMTP、POP、IMAP”等。
TCP 被称为“面向连接”的传输层协议。传输层主要有两个协议，分别是 TCP 和 UDP。TCP 比 UDP 更可靠（TCP三次握手）。并且 TCP 协议能够确保，先发送的数据先到达（与之相反，UDP 不保证这点）。

3. HTTP 协议如何使用 TCP 连接

HTTP 对 TCP 连接的使用，分为两种方式：俗称“短连接”和“长连接”（“长连接”又称“持久连接”，“Keep-Alive”或“Persistent Connection”）

假设有一个网页，里面包含好多图片，还包含好多【外部的】CSS 文件和 JS 文件。在“短连接”的模式下，浏览器会先发起一个 TCP 连接，拿到该网页的 HTML 源代码（拿到 HTML 之后，这个 TCP 连接就关闭了）。然后，浏览器开始分析这个网页的源码，知道这个页面包含很多外部资源（图片、CSS、JS）。然后针对【每一个】外部资源，再分别发起一个个 TCP 连接，把这些文件获取到本地（同样的，每抓取一个外部资源后，相应的 TCP 就断开）

相反，如果是“长连接”的方式，浏览器也会先发起一个 TCP 连接去抓取页面。但是抓取页面之后，该 TCP 连接并不会立即关闭，而是暂时先保持着（所谓的“Keep-Alive”）。然后浏览器分析 HTML 源码之后，发现有很多外部资源，就用刚才那个 TCP 连接去抓取此页面的外部资源。

在 HTTP 1.0 版本，【默认】使用的是“短连接”（那时候是 Web 诞生初期，网页相对简单，“短连接”的问题不大）；
到了1995年底开始制定 HTTP 1.1 草案的时候，网页已经开始变得复杂（网页内的图片、脚本越来越多了）。这时候再用短连接的方式，效率太低下了（因为建立 TCP 连接是有“时间成本”和“CPU 成本”滴）。所以，在 HTTP 1.1 中，【默认】采用的是“Keep-Alive”的方式。

#### 加密

1. 加密”和“解密

通俗而言，你可以把“加密”和“解密”理解为某种【互逆的】数学运算。就好比“加法和减法”互为逆运算、“乘法和除法”互为逆运算。
“加密”的过程，就是把“明文”变成“密文”的过程；反之，“解密”的过程，就是把“密文”变为“明文”。在这两个过程中，都需要一个“密钥”来参与数学运算。

2. 对称加密

所谓的“对称加密技术”，意思就是说：“加密”和“解密”使用【相同的】密钥。这个比较好理解。就好比你用 7zip 或 WinRAR 创建一个带密码（口令）的加密压缩包。当你下次要把这个压缩文件解开的时候，你需要输入【同样的】密码。在这个例子中，密码/口令就如同刚才说的“密钥”。

3. 非对称加密

所谓的“非对称加密技术”，意思就是说：“加密”和“解密”使用【不同的】密钥。比较难理解，也比较难想到。当年“非对称加密”的发明，还被誉为“密码学”历史上的一次革命。

4. 各自有啥优缺点

看完刚才的定义，很显然：（从功能角度而言）“非对称加密”能干的事情比“对称加密”要多。这是“非对称加密”的优点。但是“非对称加密”的实现，通常需要涉及到“复杂数学问题”。所以，“非对称加密”的性能通常要差很多（相对于“对称加密”而言）。
这两者的优缺点，也影响到了 SSL 协议的设计。

#### HTTPS 协议的需求
1. 兼容性

因为是先有 HTTP 再有 HTTPS。所以，HTTPS 的设计者肯定要考虑到对原有 HTTP 的兼容性。
这里所说的兼容性包括很多方面。比如已有的 Web 应用要尽可能无缝地迁移到 HTTPS；比如对浏览器厂商而言，改动要尽可能小；

基于“兼容性”方面的考虑，很容易得出如下几个结论：

- HTTPS 还是要基于 TCP 来传输
（如果改为 UDP 作传输层，无论是 Web 服务端还是浏览器客户端，都要大改，动静太大了）
- 单独使用一个新的协议，把 HTTP 协议包裹起来
（所谓的“HTTP over SSL”，实际上是在原有的 HTTP 数据外面加了一层 SSL 的封装。HTTP 协议原有的 GET、POST 之类的机制，基本上原封不动）

2. 可扩展性

前面说了，HTTPS 相当于是“HTTP over SSL”。
如果 SSL 这个协议在“可扩展性”方面的设计足够牛逼，那么它除了能跟 HTTP 搭配，还能够跟其它的应用层协议搭配。岂不美哉？
现在看来，当初设计 SSL 的人确实比较牛。如今的 SSL/TLS 可以跟很多常用的应用层协议（比如：FTP、SMTP、POP、Telnet）搭配，来强化这些应用层协议的安全性。

3. 保密性（防泄密）

HTTPS 需要做到足够好的保密性。
说到保密性，首先要能够对抗嗅探（行话叫 Sniffer）。所谓的“嗅探”，通俗而言就是监视你的网络传输流量。如果你使用明文的 HTTP 上网，那么监视者通过嗅探，就知道你在访问哪些网站的哪些页面。
嗅探是最低级的攻击手法。除了嗅探，HTTPS 还需要能对抗其它一些稍微高级的攻击手法——比如“重放攻击”。

4. 完整性（防篡改）

除了“保密性”，还有一个同样重要的目标是“确保完整性”。在发明 HTTPS 之前，由于 HTTP 是明文的，不但容易被嗅探，还容易被篡改。

举个例子：比如网络运营商（ISP）都比较流氓，经常有网友抱怨说访问某网站（本来是没有广告的），竟然会跳出很多中国电信的广告。为啥会这样捏？因为你的网络流量需要经过 ISP 的线路才能到达公网。如果你使用的是明文的 HTTP，ISP 很容易就可以在你访问的页面中植入广告。
所以，当初设计 HTTPS 的时候，还有一个需求是“确保 HTTP 协议的内容不被篡改”。

5. 真实性（防假冒）

在谈到 HTTPS 的需求时，“真实性”经常被忽略。其实“真实性”的重要程度不亚于前面的“保密性”和“完整性”。

举个例子：你因为使用网银，需要访问该网银的 Web 站点。那么，你如何确保你访问的网站确实是你想访问的网站？（这话有点绕口令）因为 DNS 系统本身是不可靠的（尤其是在设计 SSL 的那个年代，连 DNSSEC 都还没发明）。由于 DNS 的不可靠（存在“域名欺骗”和“域名劫持”），你看到的网址里面的域名【未必】是真实！

6. 性能

引入 HTTPS 之后，【不能】导致性能变得太差。为了确保性能，SSL 的设计者至少要考虑如下几点：

- 如何选择加密算法（“对称”or“非对称”）？
- 如何兼顾 HTTP 采用的“短连接”TCP 方式？
（SSL 是在1995年之前开始设计的，那时候的 HTTP 版本还是 1.0，默认使用的是“短连接”的 TCP 方式——默认不启用 Keep-Alive

#### 一些概念

- KEY

KEY文件通常用于存储私钥或公钥。用于加密和解密。与证书文件不同，KEY文件只包含密钥信息，不包含证书信息。KEY文件可以使用PEM或DER格式进行编码。使用PEM格式编码的KEY文件具有良好的可读性和可编辑性，而使用DER格式编码的KEY文件则更加紧凑和高效。

- CSR 

是Certificate Signing Request的缩写，即证书签名请求，这不是证书，可以简单理解成公钥，生成证书时要把这个提交给权威的证书颁发机构。

- CRT（Certificate）和 CER（Certificate）

CRT和CER都是证书文件的扩展名，它们通常用于存储X.509证书。感觉是用于确保网站真实性。
在Windows平台上，CRT文件通常用于存储公钥证书，而CER文件则用于存储包含公钥和私钥的证书。然而，在实际应用中，CRT和CER文件的区别并不严格，它们通常可以互换使用。CRT文件通常使用PEM或DER格式进行编码，而CER文件则通常使用DER格式进行编码。

- X.509 

是一种证书格式.对X.509证书来说，认证者总是CA或由CA指定的人，一份X.509证书是一些标准字段的集合，这些字段包含有关用户或设备及其相应公钥的信息。

X.509的证书文件，一般以.crt结尾，根据该文件的内容编码格式，可以分为以下二种格式：

- PEM（Privacy-Enhanced Mail）

PEM是一种基于ASCII编码的证书和密钥存储格式，广泛应用于安全领域，特别是在SSL/TLS协议中。PEM文件通常以“.pem”为后缀名，可以包含公钥、私钥、证书等敏感信息。PEM文件使用Base64编码，并且包含了起始标记和结束标记（以"-----BEGIN..."开头, "-----END..."结尾），以便于识别和区分不同类型的密钥和证书。由于PEM格式具有良好的可读性和可编辑性，它成为了一种广泛使用的证书和密钥文件格式。

- DER（Distinguished Encoding Rules）

DER是一种二进制编码格式，用于表示X.509证书、CRL（证书吊销列表）和PKCS#7等数据结构。DER文件通常以“.der”或“.cer”为后缀名。与PEM格式相比，DER格式更加紧凑和高效，因为它使用二进制编码而不是Base64编码。然而，DER格式的文件不易于阅读和编辑，通常需要专业的工具才能查看和解析。


#### openssl 步骤：

前提：先建一个cert目录，cd到该目录，以下所有命令的当前路径均为该目录

1. 生成私钥KEY

`openssl genrsa -des3 -out server.key 2048`
这一步执行完以后，cert目录下会生成server.key文件

2. 生成CA的证书

前面提过X.509证书的认证者总是CA或由CA指定的人，所以得先生成一个CA的证书

`openssl req -new -x509 -key server.key -out ca.crt -days 3650`

3. 生成证书请求文件CSR

`openssl req -new -key server.key -out server.csr`
该命令先进入交互模式，让你填一堆东西，要注意的是Common Name这里，要填写成使用SSL证书(即：https协议)的域名或主机名，否则浏览器会认为不安全。例如：如果以后打算用https://wenran-docker/xxx 这里就填写wenran-docker

openssl.cfg

4. 最后用第3步的CA证书给自己颁发一个证书玩玩

`openssl x509 -req -days 3650 -in server.csr \
  -CA ca.crt -CAkey server.key \
  -CAcreateserial -out server.crt`

执行完以后，cert目录下server.crt 就是我们需要的证书。当然，如果要在google等浏览器显示出安全的绿锁标志，自己颁发的证书肯定不好使，得花钱向第三方权威证书颁发机构申请。


#### go tls 代码

```go
// 服务端
  lis, err := net.Listen("tcp", ":8972")
	if err != nil {
		fmt.Printf("failed to listen: %v", err)
		return
	}

	// TLS认证
	creds, err := credentials.NewServerTLSFromFile("/Users/test/server.crt", "/Users/test/server.key")
	if err != nil {
		grpclog.Fatalf("Failed to generate credentials %v", err)
	}

	//开启TLS认证 注册拦截器
	s := grpc.NewServer(grpc.Creds(creds), grpc.UnaryInterceptor(LoggingInterceptor))

// -------------------------------------
// 客户端
	creds, err := credentials.NewClientTLSFromFile("/Users/rickiyang/ca.crt", "www.rickiyang.com")
	if err != nil {
		grpclog.Fatalf("Failed to create TLS credentials %v", err)
	}
	opts = append(opts, grpc.WithTransportCredentials(creds))

	//连接服务端
	conn, err := grpc.Dial(":8972", opts...)
	if err != nil {
		fmt.Printf("faild to connect: %v", err)
	}
	defer conn.Close()
```


### token/自定义metadata

token 即令牌的意思，令牌的生成规则是我们自定义的，用户第一次登录后服务端生成一个令牌返回给客户端，以后客户端在令牌过期内只需要带上这个令牌以及生成令牌必要的参数，服务端通过生成规则能生成一样的令牌即表示校验通过。

go代码：
提供接口，自己实现

```go

// client

// customCredential 自定义认证
type customCredential struct{}

func (c customCredential) GetRequestMetadata(ctx context.Context, uri ...string) (map[string]string, error) {
    return map[string]string{
        "appid":  "101010",
        "appkey": "i am key",
    }, nil
}

func (c customCredential) RequireTransportSecurity() bool {
    return false
}
// 上面是第1步，实例准备

func main() {
    var opts []grpc.DialOption
	opts = append(opts, grpc.WithInsecure())
	opts = append(opts, grpc.WithBlock())
  // 使用自定义认证
  opts = append(opts, grpc.WithPerRPCCredentials(new(customCredential)))
	// Set up a connection to the server.
	conn, err := grpc.Dial(address, opts...)
	if err != nil {
		log.Fatalf("did not connect: %v", err)
	}
	defer conn.Close()
	c := pb.NewGreeterClient(conn)

	// Contact the server and print out its response.
	name := defaultName
	if len(os.Args) > 1 {
		name = os.Args[1]
	}
	ctx, cancel := context.WithTimeout(context.Background(), time.Second)
	defer cancel()
	r, err := c.SayHello(ctx, &pb.HelloRequest{Name: name})
	if err != nil {
		log.Fatalf("could not greet: %v", err)
	}
	log.Printf("Greeting: %s", r.GetMessage())
}


// server端
// SayHello implements helloworld.GreeterServer
func (s *server) SayHello(ctx context.Context, in *pb.HelloRequest) (*pb.HelloReply, error) {
    // 解析metada中的信息并验证
    md, ok := metadata.FromIncomingContext(ctx)
    if !ok {
        return nil, grpc.Errorf(codes.Unauthenticated, "无Token认证信息")
	}
	
    var (
        appid  string
        appkey string
    )

    if val, ok := md["appid"]; ok {
        appid = val[0]
    }

    if val, ok := md["appkey"]; ok {
        appkey = val[0]
    }

    if appid != "101010" || appkey != "i am key" {
        return nil, grpc.Errorf(codes.Unauthenticated, "Token认证信息无效: appid=%s, appkey=%s", appid, appkey)
    }
	log.Printf("Received: %v.\nToken info: appid=%s,appkey=%s", in.GetName(), appid, appkey)
	return &pb.HelloReply{Message: "Hello " + in.GetName()}, nil
}
```

## 流 stream

客户端流

服务端流

双向流


## 面试问题

1. 什么是 RPC ？

	RPC (Remote Procedure Call)即远程过程调用，是分布式系统常见的一种通信方法。它允许程序调用另一个地址空间（通常是共享网络的另一台机器上）的过程或函数，而不用程序员显式编码这个远程调用的细节。

	RPC就是从一台机器（客户端）上通过参数传递的方式调用另一台机器（服务器）上的一个函数或方法（可以统称为服务）并得到返回的结果。

	RPC会隐藏底层的通讯细节（不需要直接处理Socket通讯或Http通讯）。客户端发起请求，服务器返回响应（类似于Http的工作方式）RPC在使用形式上像调用本地函数（或方法）一样去调用远程的函数（或方法）。

	除 RPC 之外，常见的多系统数据交互方案还有分布式消息队列、HTTP 请求调用、数据库和分布式缓存等。

	其中 RPC 和 HTTP 调用是没有经过中间件的，它们是端到端系统的直接数据交互。

	http更像是资源的获取。

2. 为什么我们要用RPC?

RPC 的主要目标是让构建分布式应用更容易，在提供强大的远程调用能力时不损失本地调用的语义简洁性。为实现该目标，RPC 框架需提供一种透明调用机制让使用者不必显式的区分本地调用和远程调用。

3. RPC需要解决的三个问题
RPC要达到的目标：远程调用时，要能够像本地调用一样方便，让调用者感知不到远程调用的逻辑。

Call ID映射。我们怎么告诉远程机器我们要调用哪个函数呢？在本地调用中，函数体是直接通过函数指针来指定的，我们调用具体函数，编译器就自动帮我们调用它相应的函数指针。但是在远程调用中，是无法调用函数指针的，因为两个进程的地址空间是完全不一样。所以，在RPC中，所有的函数都必须有自己的一个ID。这个ID在所有进程中都是唯一确定的。客户端在做远程过程调用时，必须附上这个ID。然后我们还需要在客户端和服务端分别维护一个 {函数 <--> Call ID} 的对应表。两者的表不一定需要完全相同，但相同的函数对应的Call ID必须相同。当客户端需要进行远程调用时，它就查一下这个表，找出相应的Call ID，然后把它传给服务端，服务端也通过查表，来确定客户端需要调用的函数，然后执行相应函数的代码。

序列化和反序列化。客户端怎么把参数值传给远程的函数呢？在本地调用中，我们只需要把参数压到栈里，然后让函数自己去栈里读就行。但是在远程过程调用时，客户端跟服务端是不同的进程，不能通过内存来传递参数。甚至有时候客户端和服务端使用的都不是同一种语言（比如服务端用C++，客户端用Java或者Python）。这时候就需要客户端把参数先转成一个字节流，传给服务端后，再把字节流转成自己能读取的格式。这个过程叫序列化和反序列化。同理，从服务端返回的值也需要序列化反序列化的过程。

网络传输。远程调用往往是基于网络的，客户端和服务端是通过网络连接的。所有的数据都需要通过网络传输，因此就需要有一个网络传输层。网络传输层需要把Call ID和序列化后的参数字节流传给服务端，然后再把序列化后的调用结果传回客户端。只要能完成这两者的，都可以作为传输层使用。因此，它所使用的协议其实是不限的，能完成传输就行。尽管大部分RPC框架都使用TCP协议，但其实UDP也可以，而gRPC干脆就用了HTTP2。Java的Netty也属于这层的东西。

4. 实现高可用RPC框架需要考虑到的问题

既然系统采用分布式架构，那一个服务势必会有多个实例，要解决如何获取实例的问题。所以需要一个服务注册中心，比如在Dubbo中，就可以使用Zookeeper作为注册中心，在调用时，从Zookeeper获取服务的实例列表，再从中选择一个进行调用；

如何选择实例呢？就要考虑负载均衡，例如dubbo提供了4种负载均衡策略；

如果每次都去注册中心查询列表，效率很低，那么就要加缓存；
客户端总不能每次调用完都等着服务端返回数据，所以就要支持异步调用；

服务端的接口修改了，老的接口还有人在用，这就需要版本控制；
服务端总不能每次接到请求都马上启动一个线程去处理，于是就需要线程池；

5. 服务端如何处理请求？有哪些方式？

参考答案：服务端接收到客户端的请求后，常见的处理方式有三种，分别是BIO、NIO和AIO。

同步阻塞方式（BIO）：客户端发一次请求，服务端生成一个对应线程去处理。当客户端同时发起的请求很多时，服务端需要创建多个线程去处理每一个请求，当达到了系统最大的线程数时，新来的请求就无法处理了。

同步非阻塞方式 (NIO)：客户端发一次请求，服务端并不是每次都创建一个新线程来处理，而是通过 I/O 多路复用技术进行处理。就是把多个 I/O 的阻塞复用到同一个 select 的阻塞上，从而使系统在单线程的情况下可以同时处理多个客户端请求。这种方式的优势是开销小，不用为每个请求创建一个线程，可以节省系统开销。

异步非阻塞方式（AIO）：客户端发起一个 I/O 操作然后立即返回，等 I/O 操作真正完成以后，客户端会得到 I/O 操作完成的通知，此时客户端只需要对数据进行处理就好了，不需要进行实际的 I/O 读写操作，因为真正的 I/O 读取或者写入操作已经由内核完成了。这种方式的优势是客户端无需等待，不存在阻塞等待问题。


### 消息队列 作用

（Message Queue, MQ）在分布式系统和微服务架构中起着关键的作用，它是一种中间件，用于在不同的组件或服务之间异步传递消息。以下是消息队列的主要作用：

- 解耦（Decoupling）：
消息队列允许生产者（发送方）和消费者（接收方）独立工作，无需直接知道对方的存在或状态。这样，系统组件可以独立开发、部署和扩展，降低耦合度。

- 异步处理（Asynchronous Processing）：
生产者发布消息后立即返回，无需等待消费者的响应。这使得系统能够快速响应，提高吞吐量，因为消费者可以在合适的时间处理消息，而不是立即处理。

- 流量削峰（Load Leveling）：

在高并发时期，消息队列可以暂时存储大量请求，避免系统因瞬时流量过大而崩溃。消费者按照自己的处理能力逐步消费消息，平滑系统负载。

- 容错性（Fault Tolerance）：

如果消费者出现问题，消息不会丢失，它们会在队列中保留，直到消费者恢复后继续处理。

- 可扩展性（Scalability）：

添加更多的消费者可以并行处理消息，从而水平扩展系统处理能力。

- 顺序保证（Ordering）：
根据队列的特性，消息通常按照FIFO（先进先出）原则处理，可以保证消息的顺序。

- 任务调度（Task Scheduling）：

消息队列可以用于延迟任务或定时任务，例如，将某些任务放入队列，设定在未来某个时间点执行。

- 消息广播（Broadcasting）：

一个消息可以被多个消费者订阅和处理，实现广播式通信。
简化复杂性（Simplifying Complexity）：

复杂的同步问题可以通过消息队列简化，因为它们提供了可靠的消息传递机制，处理分布式系统中的通信挑战。
通过以上功能，消息队列能够提高系统的灵活性、稳定性和可扩展性，是现代软件架构中的重要组成部分。




### etcd 

Etcd 是一个分布式的、一致性的键值存储系统，常被用作服务发现和配置管理的注册中心。在微服务架构中，Etcd 提供了以下核心功能来支持服务发现：

服务注册：

服务提供者（Service Provider）在启动时将自己的元数据（如服务名称、IP 地址、端口等）注册到 Etcd 中。这个过程通常是自动化的，服务提供者向 Etcd 发送 HTTP API 请求来创建或更新一个键（key），该键对应服务的信息。
服务发现：

服务消费者（Service Consumer）通过查询 Etcd 来找到服务提供者的地址。消费者可以订阅特定服务的关键字，当服务提供者注册或注销时，Etcd 会通知消费者，使消费者能够动态地发现可用的服务实例。
服务健康检查：

Etcd 支持健康检查机制，服务提供者可以定期向 Etcd 报告其健康状态。如果服务不可用，Etcd 可以从服务列表中移除相应的条目，确保服务消费者只使用健康的实例。
服务分组与版本管理：

服务可以被组织成不同的版本或组，Etcd 允许对这些组进行版本控制，以便进行滚动升级或回滚。
强一致性保证：

Etcd 使用 raft 协议保证数据的一致性和高可用性，这意味着即使在集群的一部分节点失败的情况下，服务发现仍然可以正常工作。
API 接口：

Etcd 提供了一套简单的 HTTP RESTful API，使得集成到各种编程语言中非常容易。
在实践中，服务提供者通常会使用客户端库（如 Go 的 go.etcd.io/etcd/clientv3）来与 Etcd 交互，这些库封装了注册、发现和健康检查的细节。服务消费者则通过监听 Etcd 的事件或者定期查询来获取服务列表。