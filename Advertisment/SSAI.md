# SSAI

SSAI，全称为 Server-Side Ad Insertion（服务器端广告插入），也称为动态广告插入 (DAI)，是一种在流媒体内容中动态插入广告的技术。通常用于直播电视、点播视频和OTT（Over-The-Top）服务。与客户端侧广告插入（Client-Side Ad Insertion, CSAI）不同，SSAI 在视频内容到达终端用户设备之前，在服务器端完成广告的拼接，这样可以绕过一些广告拦截软件，并且能够更好地控制广告的展示和追踪。

## 关键模块：

广告决策服务 (ADS): 这个模块负责基于用户信息、地理位置、观看历史等因素做出广告选择。它会生成一个广告播放列表或者直接返回广告的URL。

广告服务器: 广告服务器存储广告内容，并响应ADS请求，提供广告媒体文件。这个模块可以是第三方广告平台或内部部署的广告系统。

内容分发网络 (CDN): CDN用于高效地向终端用户传输视频内容和广告。SSAI系统通常与CDN集成，以确保广告和视频内容的快速和可靠传输。

视频编码和封装: 视频编码器将原始视频转换为适合流媒体传输的格式，如HLS或DASH。封装器则将视频切片成多个片段，并在每个片段之间预留广告插槽。

SSAI中间件: 这个模块负责在视频流中插入广告。它接收来自ADS的广告决策，并在视频片段之间插入广告，同时处理广告的无缝过渡，例如通过使用适当的缓冲策略。

元数据和信号传递: SSAI系统依赖于元数据来确定何时插入广告。这可能包括视频的播放列表、广告位置标记、以及与广告插入相关的其他信息。

用户身份验证和授权: 为了个性化广告，系统需要识别用户并应用相应的广告政策。这涉及到用户登录和权限检查。

报告和分析: SSAI系统收集关于广告展示和用户互动的数据，用于分析和优化广告效果。

错误处理和恢复: 系统需要有机制来处理广告加载失败的情况，可能需要备选广告或跳过广告的逻辑。

合规性和版权管理: 确保广告和内容符合当地法律法规，并且尊重版权。

这些模块协同工作，使得广告能够无缝地插入到视频流中，同时提供广告商和观众所需的体验。SSAI的实现可以非常复杂，具体取决于服务的规模、内容的多样性以及广告商的需求。

## 步骤：

广告请求： 当用户请求观看视频内容时，SSAI 服务会根据用户信息和广告规则，向广告服务器发送请求获取适合的广告。

广告选择与插入： 广告服务器返回广告元数据，SSAI 服务根据这些信息在视频流中插入广告片段。这通常是在视频内容的播放列表（如 HLS 的 m3u8 文件）中进行，通过修改播放列表来添加广告片段的位置。

内容与广告的拼接： 在用户请求视频内容时，SSAI 服务会实时或按需生成包含广告的播放列表，这个过程可能涉及重新编码或转码广告和内容，确保它们在格式和编码上兼容。

用户接收内容： 用户设备从服务器获取包含广告的播放列表，播放器按照列表顺序播放主内容和广告。

广告追踪与报告： SSAI 还需要收集广告展示和互动的数据，以便向广告商提供报告和计费依据。

SSAI 技术对于视频流媒体服务商来说，可以提高广告的精准度和效果，同时减少用户体验上的负面影响。在实现上，SSAI 可以利用各种编程语言和技术栈，例如使用 Elixir 进行高并发处理，或者使用 ExoPlayer 这样的播放器框架来支持广告插入功能。

