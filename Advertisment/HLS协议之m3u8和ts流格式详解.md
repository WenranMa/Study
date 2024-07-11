# HLS协议之m3u8和ts流格式详解

## 简介
m3u8 文件其实是 HTTP Live Streaming（缩写为 HLS） 协议的部分内容，而 HLS 是一个由苹果公司提出的基于 HTTP 的流媒体网络传输协议。

HLS 的工作原理是把整个流分成一个个小的基于 HTTP 的文件来下载，每次只下载一些。当媒体流正在播放时，客户端可以选择从许多不同的备用源中以不同的速率下载同样的资源，允许流媒体会话适应不同的数据速率。在开始一个流媒体会话时，客户端会下载一个包含元数据的 extended M3U (m3u8) playlist文件，用于寻找可用的媒体流。

HLS 只请求基本的 HTTP 报文，与实时传输协议（RTP）不同，HLS 可以穿过任何允许 HTTP 数据通过的防火墙或者代理服务器。它也很容易使用内容分发网络来传输媒体流。

简而言之，HLS 是新一代流媒体传输协议，其基本实现原理为`将一个大的媒体文件进行分片`，将该`分片文件资源路径记录于 m3u8 文件（即 playlist）内`，其中附带一些额外描述（比如该资源的多带宽信息···）用于提供给客户端。客户端依据该 m3u8 文件即可获取对应的媒体资源，进行播放。

因此，客户端获取 HLS 流文件，主要就是对 m3u8 文件进行解析操作。

## M3U8 文件简介
m3u8 文件实质是一个播放列表（playlist），其可能是一个`媒体播放列表（Media Playlist`），或者是一个`主列表（Master Playlist）`。但无论是哪种播放列表，其内部文字使用的都是 utf-8 编码。

当 m3u8 文件作为媒体播放列表（Meida Playlist）时，其内部信息记录的是一系列媒体片段资源，顺序播放该片段资源，即可完整展示多媒体资源。其格式如下所示：

```m3u8
#EXTM3U
#EXT-X-TARGETDURATION:10

#EXTINF:9.009,
http://media.example.com/first.ts
#EXTINF:9.009,
http://media.example.com/second.ts
#EXTINF:3.003,
http://media.example.com/third.ts
```

对于点播来说，客户端只需按顺序下载上述片段资源，依次进行播放即可。而对于直播来说，客户端需要 `定时重新请求` 该 m3u8 文件，看下是否有新的片段数据需要进行下载并播放。

当 m3u8 作为主播放列表（Master Playlist）时，其内部提供的是同一份媒体资源的多份流列表资源（Variant Stream）。其格式如下所示：

```m3u8
#EXTM3U
#EXT-X-STREAM-INF:BANDWIDTH=150000,RESOLUTION=416x234,CODECS="avc1.42e00a,mp4a.40.2"
http://example.com/low/index.m3u8
#EXT-X-STREAM-INF:BANDWIDTH=240000,RESOLUTION=416x234,CODECS="avc1.42e00a,mp4a.40.2"
http://example.com/lo_mid/index.m3u8
#EXT-X-STREAM-INF:BANDWIDTH=440000,RESOLUTION=416x234,CODECS="avc1.42e00a,mp4a.40.2"
http://example.com/hi_mid/index.m3u8
#EXT-X-STREAM-INF:BANDWIDTH=640000,RESOLUTION=640x360,CODECS="avc1.42e00a,mp4a.40.2"
http://example.com/high/index.m3u8
#EXT-X-STREAM-INF:BANDWIDTH=64000,CODECS="mp4a.40.5"
http://example.com/audio/index.m3u8
```

该备用流资源指定了多种不同码率，不同格式的媒体播放列表，并且，该备用流资源也可同时提供不同版本的资源内容，比如不同语言的音频文件，不同角度拍摄的视屏文件等等。客户可以根据不同的网络状态选取合适码流的资源，并且最好根据用户喜好选择合适的资源内容。

## m3u8 文件格式简解
m3u8 的文件格式主要包含三方面内容：

### 文件播放列表格式定义
播放列表（Playlist，也即 m3u8 文件） 内容需严格满足规范定义所提要求。下面罗列一些主要遵循的条件：
1. m3u8 文件必须以 utf-8 进行编码，不能使用 Byte Order Mark（BOM）字节序， 不能包含 utf-8 控制字符（U+0000 ~ U_001F 和 U+007F ~ u+009F）。

2. m3u8 文件的每一行要么是一个 URI，要么是空行，要么就是以 `#` 开头的字符串。不能出现空白字符，除了显示声明的元素。

3. m3u8 文件中以 `#` 开头的字符串要么是注释，要么就是标签。标签以 `#EXT` 开头，大小写敏感。

### 属性列表（Attribute Lists）

某些特定的标签的值为属性列表。标签后面的属性列表以 逗号 作为分隔符，分离出多组不带空格的 属性/值 对。
属性/值 对的语法格式如下：

`ATTRIBTUENAME=AttributeValue`

其中：属性ATTRIBTUENAME是由 `[A..Z],[0..9] 和 -` 组成的不带引号的字符串。因此，属性ATTRIBTUENAME只能使用`大写字母`，不能使用小写字母，并且ATTRIBTUENAME和=中间不能有空格，同理，=和AttributeValue之间也不能有空格。

值AttributeValue的只能取以下类型：

- 十进制整型（decimal-interger）：由 [0..9] 之间组成的十进制不带引号的字符串，范围为 0 ~ 2^{64}（18446744073709551615），字符长度为 1 ~ 20 之间。
- 十六进制序列：由 [0..9] 和 [A..F] 且前缀为 0x 或 0X 组合成的不带引号的字符串。其序列的最大长度取决于他的属性名AttributeNames。
- 带符号十进制浮点型（signed-decimal-floating-point）：由 [0..9]，-和.组合成的不带引号的字符串。
- 字符串（quoted-string）：由双引号包裹表示的字符串。其中，0xA，0xD 和 双引号"不能出现在该字符串中。该字符串区分大小写。
- 可枚举字符串（enumerated-string）：由AttributeName显示定义的一系列不带引号的字符串。该字符串不能包含双引号"，逗号,和空白字符。
- decimal-resolution：由字符x进行隔离的两个十进制整型数。第一个整型表示水平宽度大小，第二个整型数表示垂直方向高度大小（单位：像素）。

### 标签
标签用于指定 m3u8 文件的全局参数或在其后面的切片文件/媒体播放列表的一些信息。
标签的类型可分为五种类型：
- 基础标签（Basic Tags）
- 媒体片段类型标签（Media Segment Tags）
- 媒体播放列表类型标签
- 主播放列表类型标签
- 播放列表类型标签

#### 1. 基础标签（Basic Tags）：
可同时适用于媒体播放列表（Media Playlist）和主播放列表（Master Playlist）。具体标签如下：

- EXTM3U：表明该文件是一个 m3u8 文件。每个 M3U 文件必须将该标签放置在第一行。
- EXT-X-VERSION：表示 HLS 的协议版本号，该标签与流媒体的兼容性相关。该标签为全局作用域；每个 m3u8 文件内最多只能出现一个该标签定义。如果 m3u8 文件不包含该标签，则默认为协议的第一个版本。

#### 2. 媒体片段类型标签（Media Segment Tags）：

每个切片 URI 前面都有一系列媒体片段标签对其进行描述。有些片段标签只对其后切片资源有效；有些片段标签对其后所有切片都有效，直到后续遇到另一个该标签描述。媒体片段类型标签不能出现在主播放列表（Master Playlist）中。具体标签如下：

- EXTINF：表示其后 URL 指定的媒体片段时长（单位为秒）。每个 URL 媒体片段之前必须指定该标签。该标签的使用格式为：

```
#EXTINF:<duration>,[<title>]
```
其中：duration可以为十进制的整型或者浮点型，其值必须小于或等于 EXT-X-TARGETDURATION 指定的值。

注：建议始终使用浮点型指定时长，这可以让客户端在定位流时，减少四舍五入错误。但是如果兼容版本号 EXT-X-VERSION 小于 3，那么必须使用整型。

- EXT-X-BYTERANGE：该标签表示接下来的切片资源是其后 URI 指定的媒体片段资源的局部范围（即截取 URI 媒体资源部分内容作为下一个切片）。该标签只对其后一个 URI 起作用。

- EXT-X-DISCONTINUITY：该标签表明其前一个切片与下一个切片之间存在中断。当以下任一情况变化时，必须使用该标签：
    - 文件格式（file format）
    - 数字（number），类型（type），媒体标识符（identifiers of tracks）
    - 时间戳序列（timestamp sequence）
    - 编码参数（encoding parameters）
    - 编码序列（encoding sequence）

**注：EXT-X-DISCONTINUITY 的一个经典使用场景就是在视屏流中插入广告，由于视屏流与广告视屏流不是同一份资源，因此在这两种流切换时使用 EXT-X-DISCONTINUITY 进行指明，客户端看到该标签后，就会处理这种切换中断问题，让体验更佳。
更多详细内容，请查看：Incorporating Ads into a Playlis**

- EXT-X-KEY：媒体片段可以进行加密，而该标签可以指定解密方法。

该标签对所有 媒体片段 和 由标签 EXT-X-MAP 声明的围绕其间的所有 媒体初始化块（Meida Initialization Section） 都起作用，直到遇到下一个 EXT-X-KEY（若 m3u8 文件只有一个 EXT-X-KEY 标签，则其作用于所有媒体片段）。多个 EXT-X-KEY 标签如果最终生成的是同样的秘钥，则他们都可作用于同一个媒体片段。

- EXT-X-MAP：该标签指明了获取媒体初始化块（Meida Initialization Section）的方法。该标签对其后所有媒体片段生效，直至遇到另一个 EXT-X-MAP 标签。

- EXT-X-PROGRAM-DATE-TIME：该标签使用一个绝对日期/时间表明第一个样本片段的取样时间。

- EXT-X-DATERANGE：该标签定义了一系列由属性/值对组成的日期范围。

#### 3. 媒体播放列表类型标签
媒体播放列表标签为 m3u8 文件的全局参数信息。这些标签只能在 m3u8 文件中至多出现一次。媒体播放列表（Media Playlist）标签不能出现在主播放列表（Master Playlist）中。
媒体播放列表具体标签如下所示：

- EXT-X-TARGETDURATION：表示每个视频分段最大的时长（单位秒）。该标签为必选标签。

- EXT-X-MEDIA-SEQUENCE：表示播放列表第一个 URL 片段文件的序列号。每个媒体片段 URL 都拥有一个唯一的整型序列号。每个媒体片段序列号按出现顺序依次加 1。如果该标签未指定，则默认序列号从 0 开始。

- EXT-X-DISCONTINUITY-SEQUENCE：该标签使能同步相同流的不同 Rendition 和 具备 EXT-X-DISCONTINUITY 标签的不同备份流。

- EXT-X-ENDLIST：表明 m3u8 文件的结束。
该标签可出现在 m3u8 文件任意位置，一般是结尾。

- EXT-X-PLAYLIST-TYPE：表明流媒体类型。全局生效。
该标签为可选标签。type-enum可选值如下：
    - VOD：即 Video on Demand，表示该视屏流为点播源，因此服务器不能更改该 m3u8 文件；

    - EVENT：表示该视频流为直播源，因此服务器不能更改或删除该文件任意部分内容（但是可以在文件末尾添加新内容）。

注：VOD 文件通常带有 EXT-X-ENDLIST 标签，因为其为点播源，不会改变；而 EVEVT 文件初始化时一般不会有 EXT-X-ENDLIST 标签，暗示有新的文件会添加到播放列表末尾，因此也需要客户端定时获取该 m3u8 文件，以获取新的媒体片段资源，直到访问到 EXT-X-ENDLIST 标签才停止）。

- EXT-X-I-FRAMES-ONLY：该标签表示每个媒体片段都是一个 I-frame。I-frames 帧视屏编码不依赖于其他帧数，因此可以通过 I-frame 进行快速播放，急速翻转等操作。该标签全局生效。

#### 4. 主播放列表类型标签
主播放列表（Master Playlist）定义了备份流，多语言翻译流和其他全局参数。
主播放列表标签绝不能出现在媒体播放列表（Media Playlist）中。
其具体标签如下：

- EXT-X-MEDIA：用于指定相同内容的可替换的多语言翻译播放媒体-列表资源。

- EXT-X-STREAM-INF：该属性指定了一个备份源。该属性值提供了该备份源的相关信息。

- EXT-X-I-FRAME-STREAM-INF：该标签表明媒体播放列表文件包含多种媒体资源的 I-frame 帧。

- EXT-X-SESSION-DATA：该标签允许主播放列表携带任意 session 数据。

- EXT-X-SESSION-KEY：该标签允许主播放列表（Master Playlist）指定媒体播放列表（Meida Playlist）的加密密钥。这使得客户端可以预先加载这些密钥，而无需从媒体播放列表中获取。

#### 5. 播放列表类型标签
以下标签可同时设置于主播放列表（Master Playlist）和媒体播放列表（Media Playlist）中。但是对于在主播放列表中设置了的标签，不应当再次设置在主播放列表指向的媒体播放列表中。
同时出现在两者播放列表的相同标签必须具备相同的值。这些标签在播放列表中不能出现多次（只能使用一次）。具体标签如下所示：

- EXT-X-INDEPENDENT-SEGMENTS：该标签表明对于一个媒体片段中的所有媒体样本均可独立进行解码，而无须依赖其他媒体片段信息。
该标签对列表内所有媒体片段均有效。

- EXT-X-START：该标签表示播放列表播放起始位置。
默认情况下，客户端开启一个播放会话时，应当使用该标签指定的位置进行播放。

## 其余一些注意事项
- 有两种请求 m3u8 播放列表的方法：
    1. 通过 m3u8 的 URI 进行请求，则该文件必须以 .m3u8 或 .m3u 结尾；
    2. 通过 HTTP 进行请求，则请求头Content-Type必须设置为 application/vnd.apple.mpegurl或者audio/mpegurl。

- 空行和注释行在解析时都忽略。

- 媒体播放列表（Media Playlist）的流资源总时长就是各切片资源的时长之和。

- 每个切片的码率（bit rate）就是切片的大小除以它对应的时长（EXTINF 指定的时长）。

- 一个标签的属性列表的同一个属性AttributeName只能出现一次。

- EXT-X-TARGETDURATION 指定的时长绝对不能进行更改。通常该值指定的时长为 10 秒。

## ts文件
ts文件为传输流文件，视频编码主要格式h264/mpeg4，音频为acc/MP3。

ts文件分为三层：ts层Transport Stream、pes层 Packet Elemental Stream、es层 Elementary Stream. es层就是音视频数据，pes层是在音视频数据上加了时间戳等对数据帧的说明信息，ts层就是在pes层加入数据流的识别和传输必须的信息。
