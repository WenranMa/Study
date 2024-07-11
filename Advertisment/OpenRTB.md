
#  OpenRTB

（Real-Time Bidding）协议是一种开放的行业标准，由Interactive Advertising Bureau (IAB) 制定，旨在促进程序化广告中的实时竞价流程。以下是OpenRTB协议的一些关键点：

定义：

Publisher（发布者）: 在OpenRTB生态系统中，发布者是指拥有广告位或流量的网站、应用或其他媒体平台。他们通过出售这些广告位的展示机会来赚取收入。
Producer（生产者）: 在上下文中，Producer可能指的是广告交易平台（Ad Exchange）或供应方平台（Supply-Side Platform, SSP），它们负责接收来自发布者的库存信息，并将这些库存暴露给潜在的买家（即广告主或需求方平台DSP）进行实时竞价。

工作流程：

发布者通过SSP或直接通过Ad Exchange发布广告位的元数据，包括用户信息、上下文环境、设备信息等。
Ad Exchange或SSP将这些信息打包成OpenRTB的请求（Request）格式，发送给多个需求方平台（Demand-Side Platform, DSP）。
DSP收到请求后，基于自身的算法和广告主的出价策略，决定是否参与竞价以及出价多少。
最高出价的广告主赢得竞价，其广告将在用户的设备上展示。
成交价格和交易细节通过OpenRTB响应（Response）返回给Ad Exchange或SSP，最终完成交易。
版本：

OpenRTB经历了多个版本，从2.0到2.5，再到更先进的3.0，不断更新以适应市场和技术的变化，比如增加对移动设备、视频广告、数据安全和隐私保护的支持。
协议内容：

包含一系列JSON结构化的数据模型，定义了如何表示广告请求和响应，包括但不限于用户特征、设备信息、广告位详情、广告格式和尺寸、出价限制等。
定义了各种对象和参数，如Imp（印象，代表一次广告展示机会）、User（用户信息）、Device（设备信息）等。
目标：

提高广告交易的效率和透明度，降低中介成本，同时允许更精准的定向广告投放。

相关实体：

Bidder（竞标者）: 通常是DSP，代表广告主参与竞价。
Ad Exchange: 中介平台，连接发布者和需求方。
SSP: 帮助发布者管理库存并将其暴露给竞标者。
OpenRTB协议是现代数字广告生态系统的核心部分，促进了广告市场的自动化和数据驱动决策。

## BidRequest

### 请求头
每个出价请求均有 OpenRTB 协议指定的以下自定义 HTTP 头：

`X-OpenRTB-Version: 2.5`
除自定义 HTTP 头外，Vungle Exchange 还附加了以下标准头：

```
Content-Type: application/json
Accept: application/json`
```

### BidRequest 对象
字段	类型	必填	描述
- id	字符串	是	 
- imp	对象数组 是	
- app	对象	是	请参阅应用程序对象。
- device	对象	是	请参阅设备对象。
- at	integer	是	竞拍类型；例如，'2' 代表二价拍卖。
- tmax	integer	是	提交完整出价响应的最长时间（以毫秒计）
- cur	字符串数组	否	以 ISO-4217-alpha 显示的允许的拍卖货币的列表；例如，["USD", "CNY", "EUR"]。
- bcat	字符串数组	否	请参阅OpenRTB 2.5第5.1部分
- regs	对象	否	请参阅 OpenRTB 2.5第 3.2.3 部分
- test	integer	否	竞价处于测试模式 (1) 还是实况模式 (0)；测试竞价不计费。
- source	对象	是	参阅 IAB SupplyChain Object implementation guide

```json
{
  "id": "1234567890",         // 请求的唯一标识
  "imp": [                   // 广告位列表
    {
      "id": "1",             // 广告位ID
      "banner": {            // banner广告的相关信息
        "w": 300,            // 宽度
        "h": 250,            // 高度
        "pos": 1             // 广告位置（例如：1表示页首）
      },
      "bidfloor": 0.5,       // 最低出价
      "tagid": "slot1"       // 广告位标签ID
    }
  ],
  "user": {                  // 用户信息
    "id": "usr123",          // 用户ID
    "gender": "M",           // 性别
    "yob": 1990              // 出生年份
  },
  "site": {                 // 网站信息
    "id": "site1",           // 网站ID
    "name": "Example Site",  // 网站名称
    "domain": "example.com"  // 网站域名
  },
  "device": {               // 设备信息
    "ua": "Mozilla/...",     // 用户代理字符串
    "geo": {                 // 地理位置
      "lat": 37.781157,      // 经度
      "lon": -122.392486     // 纬度
    }
  },
  "tmax": 100,              // 最大响应时间（毫秒）
  "cur": ["USD"]            // 货币类型
}
```

### BidResponse
响应头
响应header中必须包含`"Content-Type" and "X-OpenRTB-Version" `，且具有其中一个上述请求头接受的值。例如，
```
Content-Type: application/json 
X-OpenRTB-Version: 2.5
```

响应状态代码
所有响应均必须为 200 或 204。任何其他 HTTP 响应代码均有可能对 DSP 的竞价造成负面影响。

```json
{
  "id": "58ed309efa8936087efd1349",
  "bidid": "5508",
  "cur": "USD",
  "seatbid": [
    {
      "seat": "7735",
      "bid": [
        {
          "id": "5508",
          "impid": "58ed309efa8936087efd134a",
          "price": 50,
          "nurl": "http://bidder.com/won?price=${AUCTION_PRICE}",
          "adm": "<VAST version=\"2.0\"><Ad><InLine><AdTitle>YOUR_AD_NAME</AdTitle><Impression><![CDATA[https://YOUR_IMPRESSION_TRACKING_URL?ttdsp_price=${AUCTION_PRICE}]]></Impression><Creatives><Creative id=\"YOUR_CREATIVE_ID\"><Linear><Duration>00:00:18</Duration><TrackingEvents><Tracking event=\"start\"><![CDATA[https://YOUR_IMPRESSION_TRACKING_URL_START_PLAY]]></Tracking><Tracking event=\"complete\"><![CDATA[https://YOUR_IMPRESSION_TRACKING_URL_START_COMPLETE]]></Tracking></TrackingEvents><VideoClicks><ClickThrough><![CDATA[https://YOUR_DESTINATION_URL_TO_DOWNLOAD_BY_CLICK]]></ClickThrough><ClickTracking><![CDATA[https://YOUR_CLICK_TRACKING_URL]]></ClickTracking></VideoClicks><MediaFiles><MediaFile delivery=\"progressive\" type=\"video/mp4\" width=\"1280\" height=\"720\"> <![CDATA[https://YOUR_AD_VIDEO.mp4]]></MediaFile></MediaFiles></Linear></Creative></Creatives><Description>Longer description of ad</Description></InLine></Ad></VAST>",
          "cid": "554d550b418461cc3700014d",
          "crid": "57767c29a63510e75f000073"
        }
      ]
    }
  ]
}
```