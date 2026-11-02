---
作者:
  - "阿里云云原生"
原文链接: https://mp.weixin.qq.com/s?__biz=MzUzNzYxNjAzMg==&amp;mid=2247573535&amp;idx=1&amp;sn=f8f34337393f99d65a610feb6969c072&amp;chksm=fb16c92c498536356b69503e8cb1c75c0ef92d04b9531965d4e365342f093be82fc405854148&amp;mpshare=1&amp;scene=1&amp;srcid=04125xhonZysblAimHJQRiij&amp;sharer_shareinfo=c55fd26f2bbc2cae74240bef8a79dbf3&amp;sharer_shareinfo_first=c55fd26f2bbc2cae74240bef8a79dbf3#rd
发布时间: ""
收藏时间: "2025-04-12"
关联日记: "[[2025-04-12]]"
tags:
  - 文章
---
![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67f9c032837e6d746359dd33/22e38120-f0f9-40a1-8b9b-adbd59de2d8c.gif)

编者按：应用越智能，背后的设计会越复杂。软件的本质是解决复杂性问题，MCP 虽打开了智能的创意上限，但也给后端的设计带来了无限的复杂度。本文旨在从 MCP 的技术原理、降低 MCP Server 构建复杂度、提升 Server 运行稳定性等方面出发，分享我们的一些实践心得。文章内容较长，以下是导读大纲。（点击阅读原文，获取 78 页完整版 PPT）

1、介绍 MCP 的概念及其运作机制。

2、解释 MCP 和 Function Calling 之间的区别。

3、讲述 MCP 的本质和挑战，包括描述 MCP 信息的系统提示词的挑战，MCP Client 与 MCP Server 之间协同关系的挑战，快速构建 MCP Server，自建 Dify 的痛点等。

4、分析如何解决 MCP 的各个挑战，包括 MCP Register、MCP Server 和 Promt 的统一管理、MCP 效果验证体系和安全性保障、MCP 网关、MCP Server 的动态服务发现、Streamable HTTP、弹性效率、可观测等。

5、最后探讨 MCP 对 AI 应用架构新范式的影响，并介绍 MCP Server First 的理念。

***AI Agent 现状及架构***

*Cloud Native*

人工智能（AI）在商业领域的应用正日益成为推动创新和效率提升的核心力量。其核心在于多个 AI Agent 的协作，这些 AI Agent 通过分工与合作，共同承载 AI 应用所支持的业务需求。这种协作模式不仅优化了企业运营，还展现了 AI 在解决高影响力挑战中的潜力。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67f9c032837e6d746359dd33/9f53e394-9e90-4546-889c-5d6747afb271.png)

当前的 AI Agent，无论是和各种 Tools（各类业务服务接口）交互，还是和各类 Memory（各类存储服务接口）交互，亦或是和各类 LLMs（各类大语言模型）交互，都是通过 HTTP 协议的，除了 LLM 因为基本都遵循 OpenAI 范式以外，和其他的 Tools 和 Memory 交互都需要逐一了解它们的返回格式进行解析和适配。当一个 AI 应用包含多个 AI Agent 时，或者一个 AI 应用需要和多个业务服务接口和存储服务接口交互时，整体的开发工作量是很大的，主要体现在 3 个方面：

- 找适合该 AI 应用的业务接口和存储服务接口：


- 找三方服务接口。在公司内部找合适的服务的接口。找不到就自己先开发接口。


- 解析接口的返回格式：无论是三方服务接口还是公司内部的服务接口，返回格式可能都千奇百怪，需要逐一进行了解和解析。
- 编排多个 AI Agent：


- 有 Dify 这类流程可视化的工具辅助编排，减轻了很多编排工作，但复杂度依然不低，且运行效率和性能方面还是有瓶颈的。通过编码方式做编排（比如使用 Spring AI Alibaba 或 LangChain 等），虽然性能上更优，但是复杂度更高，编排效率和灵活性都有不足。


所以目前很多 AI 应用就只有少数几个 AI Agent，甚至很多 AI 应用背后就只有一个 AI Agent。这也是目前 AI 应用背后的 AI Agent 依然还处在第一个阶段（Siloed, Single-Purpose Agents）的原因。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67f9c032837e6d746359dd33/02ca3658-c6d3-42aa-bdb9-0715f1c0bfe8.png)

为了能使 AI Agent 进入到第二阶段（Platform-Level Agents），我们使用云原生 API 网关做了统一的接入层，通过一个网关三种不同角色的方式，解决了一部分复杂度：

- 作为南北向流量网关，统一管理 AI Agent 的入口流量，核心做转发、负载、鉴权认证、安全、流控等。
- 作为 AI 网关，代理各类 LLMs，向 AI Agent 屏蔽了繁杂的接入，并且解决了很多生产级的问题，比如多模型切换、模型 Fallback、多 API Key 管理、安全、联网搜索等。


- AI网关代理LLMs的详细文章参见：[](https://mp.weixin.qq.com/s?__biz=MzUzNzYxNjAzMg==&mid=2247573215&idx=1&sn=f77c5dd8423a9480afb6a03fce0d997c&scene=21#wechat_redirect)[https://mp.weixin.qq.com/s/tZ0wsTlZK67r9IxNZ57TDQ](https://mp.weixin.qq.com/s?__biz=MzUzNzYxNjAzMg==&mid=2247573215&idx=1&sn=f77c5dd8423a9480afb6a03fce0d997c&scene=21#wechat_redirect)


- 作为东西向网关，统一管理来自不同源（ACK、ECS、函数计算 FC、SAE、三方服务）的各类服务，供 AI Agent 使用。


但如我所说，这只解决了一部分复杂度问题，更核心的**找接口**和**解析接口**这两个问题依然没有解决。直到 MCP（Model Context Protocol）的出现，让我们看到了真正通往第二阶段（Platform-Level Agents）的路，甚至可以尝试触摸第三阶段（Universal Agents, Multi-Agents）。

***MCP 是什么***

*Cloud Native*

MCP 是模型上下文协议（Model Context Protocol）的简称，是一个开源协议，由 Anthropic（Claude开发公司）开发，旨在让大型语言模型（LLM）能够以标准化的方式连接到外部数据源和工具。它就像 AI 应用的通用接口，帮助开发者构建更灵活、更具上下文感知能力的 AI 应用，而无需为每个 AI 模型和外部系统组合进行定制集成。MCP 被设计为一个通用接口，类似于 USB-C 端口，允许 LLM 应用以一致的方式连接到各种数据源和工具，如文件、数据库、API 等。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67f9c032837e6d746359dd33/06cb4bde-6db1-4ddb-b3d3-6f35b53f30bb.jpeg)

MCP 目前一共有 3 个核心概念：

- MCP Server：


- 基于各语言的 MCP SDK 开发的程序或服务。基于某种**神秘的机制**将现存的程序或服务进行了转换，使其成为了 MCP Server。


- MCP Tool：


- MCP Tool 所属于 MCP Server，一个 MCP Server 可以有多个 MCP Tool。可以理解为一个类里有多个方法，或者类似一个服务里有多个接口。


- MCP Client：当一段代码，一个 Agent，一个客户端，基于 MCP 的规范去使用、去调用 MCP Server 里的 MCP Tool 时，它就是 MCP Client。


**MCP 的运作机制**

要真正理解 MCP 是什么，我们需要了解它的运作机制，然后你就能知道 MCP 的调用方式和传统的 HTTP 调用方式有什么不同，可能也能隐约体会到为什么我说 MCP 可以让 AI Agent 进入第二阶段。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67f9c032837e6d746359dd33/1ebdf107-7e48-42c5-85dc-87a205604772.png)

如上图所示，一次基于 MCP 的调用，一共有 6 个核心的步骤。我们先拟定一个前提：

- 我要开发一个获取时间的 AI Agent，用户在使用这个 AI Agent 时，只需要问类似“现在几点了？”这种问题即可。
- 我已经有了一个关于处理时间的 MCP Server，这个 MCP Server 里有 2 个 MCP Tool，一个负责获取当前时区，一个负责获取当前时间。


调用步骤解析：

- 第一步：用户向 AI Agent 问“现在几点了？”，此时 AI Agent 就是 MCP Client，它会把用户的问题和处理时间的 MCP Server 以及 MCP Tool 的信息一起发送给 LLM。
- 第二步：LLM 拿到信息后开始推理，基于用户的问题和 MCP Server 的信息，选出解决用户问题最合适的那个 MCP Server 和 MCP Tool，然后返回给 AI Agent（MCP Client）。


- 这里 LLM 返回给 AI Agent 的信息是：“你用 time 这个 MCP Server 里的 get_current_time 这个 MCP Tool 吧，它可以解决用户的问题”


- 第三步：AI Agent（MCP Client）现在知道该使用哪个 MCP Server 里的哪个 MCP Tool 了，直接调用那个 MCP Tool，获取结果。


- 调用 time 这个 MCP Server 里的 get_current_time 这个 MCP Tool。


- 第四步：Time MCP Server 返回结果（当前的时间）给 AI Agent（MCP Client）。
- 第五步：AI Agent（MCP Client）也很懒啊，把用户的问题和从 Time MCP Server 处拿到的结果再一次给了 LLM，目的是让 LLM 结合问题和答案再规整一下内容。
- 第六步：LLM 把规规整整的内容返回给 AI Agent（MCP Client），最后 AI Agent（MCP Client）再原封不动的返回给了用户。


在 MCP 的整个调用过程中有一个非常核心的点就是 MCP Server 以及 MCP Tool 的信息。从第一步，第二步可以看出，这个信息非常关键，是它让 LLM 知道了该如何解决用户的问题，这个信息就是 MCP 中最重要的 System Prompt，本质上就是 PE 工程。

**MCP System Prompt**

MCP 不像传统的协议定义，它没有一个确定的数据结构。它的核心是通过自然语言描述清楚有哪些 MCP Server，承担什么作用，有哪些 MCP Tool，承担什么作用，然后让大语言模型通过推理去选择最合适的 MCP Server 以及 MCP Tool。所以它的核心本质上还是提示词工程。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67f9c032837e6d746359dd33/beb0ddf6-f0fc-49a4-905e-689ea7bbd554.png)

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67f9c032837e6d746359dd33/f5d3bf6b-7b71-4c2c-9525-5ea9439bf809.png)

上面两张图是 Cline（一个 MCP Client）中的 System Prompt，可以清晰的看到它对 MCP Server 和 MCP Tool 都有明确的描述。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67f9c032837e6d746359dd33/45c9fbc7-8059-40f7-ba5b-d808830312d7.png)

上图是流程中的第一步，将用户的问题和 System Prompt 一起发送给 LLM 的内容。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67f9c032837e6d746359dd33/38f2dcbb-dbd4-4804-8757-9f666d6f5e06.png)

上图是流程中的第二步，LLM 返回了解决用户问题明确的 MCP Server 和 MCP Tool 信息。

**MCP 和 Function Calling 之间的区别**

看到这，我想大家应该对 MCP 是什么有一定感觉了。MCP 是不是解决了**找接口**和**解析接口**的问题？因为这两个工作都交给了 LLM。

- LLM 负责帮 AI Agent 找到最合适的接口。
- AI Agent 调用接口，压根不用做返回结果的解析，原封不动再交给 LLM。
- LLM 结合用户问题和接口返回的结果，做内容规整处理。


那么可能有小伙伴会问，MCP 和 LLM 的 Function Calling 又有什么区别呢？核心区别是是否绑定模型或模型厂商：

- MCP 是通用协议层的标准，类似于“AI 领域的 USB-C 接口”，定义了 LLM 与外部工具 / 数据源的通信格式，但**不绑定任何特定模型或厂商**，将复杂的函数调用抽象为客户端-服务器架构。
- Function Calling **是大模型厂商提供的专有能力**，由大模型厂商定义，不同大模型厂商之间在接口定义和开发文档上存在差异；允许模型直接生成调用函数，触发外部 API，依赖模型自身的上下文理解和结构化输出能力。


![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67f9c032837e6d746359dd33/a788b634-3c6b-4a58-8e35-f913d4740bf6.png)

如上图所示，LLM Function Calling 需要 LLM 为每个外部函数编写一个 JSON Schema 格式的功能说明，精心设计一个提示词模版，才能提高 Function Calling 响应的准确率，如果一个需求涉及到几十个外部系统，那设计成本是巨大，产品化成本极高。而 MCP 统一了客户端和服务器的运行规范，并且要求 MCP 客户端和服务器之间，也统一按照某个既定的提示词模板进行通信，这样就能通过 MCP 加强全球开发者的协作，复用全球的开发成果。

**MCP 的本质和挑战**

根据上文的一系列解释，我们可以总结一下 MCP 的本质：**模型上下文协议（Model Context Protocol）并不是一个确定的数据格式或数据结构，它是**描述 MCP Server/MCP Tool 信息的系统提示词**和 **MCP Server 与 LLM 之间的协同关系**的结合，解决的是**找接口**和**解析接口**的问题**。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67f9c032837e6d746359dd33/8780b593-73d2-44b2-9a50-6246fe80c777.png)

明确了 MCP 本质之后，将其带入到企业级生产应用中，你就会发现，这两个核心点上会有很多挑战，或者说不足。

### 描述 MCP 信息的系统提示词的挑战

- 系统提示词的安全性如何保证？


- 这个最核心的系统提示词如果被污染了，LLM 就不能准确知道你有哪些 MCP Server，有哪些 MCP Tool，甚至可能告诉 LLM 错误的，有安全漏洞的 MCP Server 和 MCP Tool，那么对你的 AI 应用来说将是巨大的风险，会导致整个 MCP 流程的瘫痪。


- 系统提示词如何管理？


- MCP Server 或者 MCP Tool 有了新版本，系统提示词应该也许要有对应的版本管理策略。


- 系统提示词写的不好，如何方便的快速调试？能不能实时生效？


- 系统提示词是没有标准定义的，理论上每个企业可以定义自己的系统提示词模板，类似 PE 工程。提示词不可能一次性就能写好，需要反复调试，需要有机制做快速的调整，并且可以做到使其实时生效。


- 如果 MCP Server 很多，那么系统提示词会非常长，岂不是很消耗 Token？如何缩小或精确 MCP Server 和 MCP Tool 的范围？


- 如果你有几十个或更多 MCP Server，那么就有可能有上百个或更多 MCP Tool，所有的信息描述下来放在系统提示词后，这个提示词模板会非常大，显而易见的对 Token 消耗非常大，变相的就是成本高。应该需要一套机制，基于用户的问题，预圈选 MCP Server 和 MCP Tool 的范围，减少 Token，提高效率，很类似联网搜索里的意图识别。


### MCP Client 与 MCP Server 之间协同关系的挑战

- 负责做协同的是 MCP Client，但目前 MCP Client 很少，比如 Cline， Claude，Cursor 等，而且都是 C/S 工具，支持的都是 SSE 协议，企业级的 AI 应用该如何结合？能不能结合？


- 基本上目前市面中的 MCP Client 都无法和企业级的 AI 应用做结合，SSE 这种有状态的协议有很多弊端，比如不支持可恢复性，服务器需要维持长期连接，仅支持服务器 → 客户端消息，无法灵活进行双向通信等。


- 现存的传统业务能快速转成 MCP Server 吗？能 0 代码改动的转换吗？


- 开发一个 MCP Server 是强依赖各语言的 MCP SDK 的，目前只支持 Python、Java、TS、Kotlin、C#。那如果是 Go 或者 PHP 技术栈的企业怎么办？并且那么多现存的业务全部用 MCP SDK 重构一遍，工作量巨大，也很不现实。


- MCP Server 会很多，如何统一管理？


- 有自己开发的 MCP Server，有三方的 MCP Server，还有大量通过某种神秘机制将传统业务转换而来的 MCP Server。这些都应该有一个类似 MCP Hub 或 MCP 市场的东西统一管理起来，方便 MCP Client 去使用。


- 企业级 AI 应用中，身份认证、数据权限、安全这些如何做？


- 在企业级的应用中，无论哪种协议，哪种架构，哪种业务。身份认证、数据权限、安全防护这些问题都是永远绕不开的。那么在 MCP 这种协同方式下如何实现。


***AI 应用架构新范式***

*Cloud Native*

我们结合 MCP 范式，以解决上述挑战点为目的，将 AI Agent 的架构进行了重构。在云原生 API 网关**，**微服务引擎 Nacos**两个产品中做了 MCP 增强能力，解决了上述大部分的挑战点。在**函数计算 FC**，**Serverless 应用引擎 SAE**两个产品中做了 MCP 增强能力，前者解决快速开发 MCP Server 的问题，后者解决开源 Dify 性能的问题。共同构建了基于 MCP 的 **AI 应用开发新范式。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67f9c032837e6d746359dd33/be6d7069-8af2-4add-8850-2b4e69639f52.png)

**AI 应用架构新范式剖析**

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67f9c032837e6d746359dd33/0bed552d-fc86-4634-b219-407ac083d09a.png)

首先我对图中的 8 步核心调用链路做以解析：

- 第一步：用户向 AI 应用发起请求，请求流量进入流量网关（云原生 API 网关）。
- 第二步：云原生 API 网关侧维护管理了不同类型的 AI Agent 的 API 或路由规则，将用户请求转发至对应的 AI Agent。
- 第三步：AI Agent 无论以哪种方式实现，只要其中的节点需要获取数据，便向 MCP 网关（云原生 API 网关）请求获取可用的 MCP Server 及 MCP Tool 的信息。
- 第四步：因为 MCP 网关处可能维护了很多 MCP 信息，可以借助 LLM 缩小 MCP 范围，减少 Token 消耗，所以向 AI 网关（云原生 API 网关）发请求和 LLM 交互。（这一步可选）
- 第五步：MCP 网关将确定好范围的 MCP Server 及 MCP Tool 的信息 List 返回给 AI Agent。
- 第六步：AI Agent 将用户的请求信息及从 MCP 网关拿到的所有 MCP 信息通过 AI 网关发送给 LLM。
- 第七步：经过 LLM 推理后，返回解决问题的一个或多个 MCP Server 和 MCP Tool 信息。
- 第八步：AI Agent 拿到确定的 MCP Server 和 MCP Tool 信息后通过 MCP 网关对该 MCP Tool 做请求。


实际生产中 ③ - ⑧ 步会多次循环交互。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67f9c032837e6d746359dd33/001c8bf7-8119-4edb-beba-ea7289df4377.jpeg)

我们依然基于 MCP 的两个本质来刨析这个新的架构。

### 如何解决 MCP 提示词的各个挑战

我们团队是中间件开源最多的团队，比如 Nacos，Higress，Sentinel，RocketMQ，Seata 等，并且还维护着 Spring Cloud Alibaba，Spring AI Alibaba，Dubbo 这些开源开发框架，在微服务架构领域有着丰富的经验。所以在 MCP Server 和 MCP 提示词统一管理这个点上，天然的就想到了微服务领域里基于 Nacos 做服务注册发现和配置统一管理的模式，我们将其转嫁到了 MCP 范式，大家可以想一下以下这些对应关系：

- SpringCloud 服务/Dubbo 服务/Go 服务 -> 各类 MCP Server
- SpringCloud 服务/Dubbo 服务/Go 服务暴露的接口 -> 各类 MCP Server 提供的 MCP Tool
- SpringCloud 服务/Dubbo 服务/Go 服务暴露的接口描述 -> 各类 MCP Server 提供的 MCP Tool 的描述
- SpringCloud 服务/Dubbo 服务/Go 服务的配置文件 -> 各类 MCP Server 的系统提示词


![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67f9c032837e6d746359dd33/3deae6b5-6df7-4d2f-91cf-8ab2b709647c.png)

所以在 MSE Nacos 这个产品中，我们做了一系列增强 MCP 的能力，使 MSE Nacos 成为统一管理 MCP Server 的 MCP Register（MCP Server 注册/配置中心）。是 AI 应用开发新范式的核心组件。

另外，MCP 官方的 Roadmap 中，也在规划 MCP Register 的能力，我们会基于 Nacos 作为 MCP Register 的方案和 MCP 在开源侧进行共建。

#### MCP Register（MCP Server 注册/配置中心）

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67f9c032837e6d746359dd33/442c0d12-827b-41ac-9b76-202009b7e3ab.png)

##### MCP Server 统一管理

MCP Server 注册到 MSE Nacos 有两种方式：

- 在 MSE Nacos 控制台手动创建。也就是将 MCP Server 的 Endpoint 配置到 MSE Nacos 中。
- 通过 Nacos SDK，自动将 MCP Server 注册进 Nacos。和当前 Java SpringCloud，Java Dubbo 服务逻辑一样。


在 MSE Nacos 中对 MCP Server 进行统一管理，可以实现对 **MCP Server 的健康检查，负载均衡，描述信息 Json 向 XML 转换，MCP Server 上下线管控等功能**。

##### MCP Prompt 统一管理

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67f9c032837e6d746359dd33/9fc7cdd4-0296-4eb7-9b7f-f758fdbe58ef.png)

在 MSE Nacos 中维护 MCP Server 的 Prompt 有两种方式：

- 手动创建 MCP Server 的配置信息，配置文件的 Data ID 的命名格式为`[MCP Server name]-mcp-tools.json`。


- 在配置文件中管理 MCP Tool 的提示词信息，比如整体作用描述，入参描述等。


- 结合 MSE 治理的能力，如果是 Java 或者 Go，可以自动感知服务的 Schema，自动生成 MCP Server 和 MCP Tool 的提示词信息。


在 MSE Nacos 中对 MCP Server 提示词进行统一管理，可以实现 **MCP 提示词版本管理（回滚），MCP 提示词灰度管理，MCP 提示词安全管理，MCP 提示词动态调优实时生效等功能**。

##### MCP 效果验证体系（进行中）

上文中提到当 MCP Server 很多时，MCP Server 的各描述信息会很多，也就是 Prompt 会很长，Token 消耗很大，所以需要有机制基于用户的输入缩小 MCP Server 范围，减少 Token 消耗，增加 LLM 推理效率。除此以外，大家知道，只要是和 LLM 交互的场景，提示词的好坏是需要多次调试的，MCP 的整个流程强依赖提示词工程，如果提示词调整不好，LLM 无法返回准确的 MCP Server 和 MCP Tool，那么整个流程就是不可用的状态了。所以在 Nacos 中我们正在做一个 MCP 效果验证的体系。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67f9c032837e6d746359dd33/84a4b6c1-6d85-4092-9942-ca9fc4ccadbb.png)

核心的原理是我们会提供一个基于 Spring AI Alibaba 开发的 AI Agent，通过用户配置的业务输入、LLM、圈定的 MCP Server 和 MCP Tool 的集合不断的做验证，将结果以视图的方式展现出来（比如成功率等）。用户可以在 Nacos 中动态的对成功率低的 MCP Server 的提示词做调整优化。

##### MCP 安全性保障（持续完善中）

无论哪种架构，哪种模式，安全性在企业生产中必然都是第一位的，MCP 领域也不例外，并且需要考虑的环节更多。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67f9c032837e6d746359dd33/4c6bbff7-ac10-4a73-8cef-45191ff18705.png)

- MCP Server 敏感信息安全管理：注册进 MSE Nacos 的各类 MCP Server 都会有类似 API Key、AK/SK、密钥、登录密码等敏感信息。MSE Nacos 和阿里云 KMS 深度集成，可以对这些敏感信息做加密处理。
- MCP Prompt 安全管理：同样依托于 MSE Nacos 和 KMS 的深度集成，可以将 MCP Server，MCP Tool 完整的 Prompt（描述信息）做加密处理，避免 Prompt 污染。
- MCP Prompt 安全校验：结合上述的验证体系以及与内容安全做集成，实现 MSE Nacos 对 MCP Server 的 Prompt 的合法性校验。


### 如何解决 MCP Client 与 MCP Server 之间协同关系的挑战

在 MCP 范式中，其实是三个角色在互相协同：

- MCP Client -> LLM
- MCP Client -> MCP Server


这两类协同关系本质上还是服务提供方和服务消费方之间的关系，涉及到**代理协作**和**流量管控**两个核心点。在传统开发范式下，通常是由网关来负责的。所以我们在云原生 API 网关中增强了 LLM 代理和 MCP Server 代理的能力，使其同时具备流量网关，AI 网关（LLM 代理）和 MCP 网关的能力。是 AI 应用开发新范式的核心组件。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67f9c032837e6d746359dd33/43df1709-ffb1-4ff9-8f76-60cf94e4b5c0.png)

所以在企业的整体系统架构中，只需要一个云原生 API 网关，即可作为流量网关、API 网关、微服务网关、AI 网关、MCP 网关，在代理和流量管控层面实现传统业务和 AI 业务的大统一，并且再结合 AI 应用开发的新范式，平滑的将 AI 业务和传统业务相结合。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67f9c032837e6d746359dd33/f336b8bf-9128-4d08-a609-15b9d32f1487.png)

#### 云原生 API 网关 Dog Food

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67f9c032837e6d746359dd33/b4a683a3-3788-4f88-ad13-9239197b44bf.png)

秉承着自己吃自己狗粮的原则，云原生 API 网关在阿里集团内部已经有很多业务在深度使用，在企业级产品能力，稳定性，性能方面已经有多个大体量业务的背书。

#### AI 网关

MCP Client 与 LLM 之间的交互和传统业务与 LLM 之间的交互本质是一样的，只要应用上生产，都会有一系列的问题需要去解决：

- 成本平衡问题：比如部署 DeepSeek R1 671B 满血版模型，至少需要 2 台 8 卡 H20 机器，列表价年度超过 100W，但 2 台的 TPS 有限，无法满足生产部署中多个用户的并发请求。即使 Meta 新发布的 Llama4，也至少需要一张 H100 去运行。所以需要有方案找到 TPS 和成本之间的平衡点。
- 模型幻觉问题：即使是 DeepSeek R1 671B 满血版模型，如果没有联网搜索，依然有很严重的幻觉问题。
- 多模型切换问题：单一模型服务有较大的风险和局限性，比如稳定性风险，比如无法根据业务（消费者）选择最优模型。目前也没有开源组件和框架解决这类问题。
- 安全合规问题：企业客户需要对问答过程做审计，确保合规，减少使用风险。
- 模型服务高可用问题：自建平台性能达到瓶颈时需要有一个大模型兜底方案，提升客户大模型使用体验。
- 闭源模型 QPS/Token 限制问题：商业大模型都有基于 API Key 维度的 QPS/Token 配额限制，需要一个好的方式能够做到快速扩展配额限制。


以上问题都是实实在在的客户在使用过程中遇到的问题，有些是模型自身问题，有些是部署架构问题，如果要客户一个一个去解决，复杂度和时间成本都是比较高的。所以就需要 AI 网关的介入来快速的，统一的收敛掉这些核心问题。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67f9c032837e6d746359dd33/022bee62-b140-4d6e-8ac9-e3ce6ef323ec.png)

云原生 API 网关的 AI 网关增强能力主要有四部分：

- 多模型适配：可以代理市面上所有主流的模型托管服务，以及兼容 OpenAI 协议的 AI 服务。在这个模块中包括协议转换、多 API Key 管理、Fallback、多模型切换等多个核心功能。
- AI 安全防护：安全防护分为三个层面，一个是输入输出的内容安全防护，另一个是保护下游 LLM 服务的稳定，以及管控 AI 接口消费者。在这个模块中包括内容审核、基于 Token 的限流降级、消费者认证等多个核心功能。
- AI 插件：AI 网关的灵活扩展机制我们使用插件的形式来实现，目前有很多预置的插件，用户也可以开发自定义插件来丰富 AI 场景流量的管控。比如基于 AI 插件机制我们实现了结果缓存、提示词装饰器、向量检索等能力。
- AI 可观测：AI 场景的可观测和传统场景的可观测是有很大区别的，监控和关注的指标都是不同的，云原生 AI 网关结合阿里云日志服务和可观测产品实现了贴合 AI 应用业务语义的可观测模块和 AI 观测大盘，支持比如 Tokens 消费观测，流式/非流式的 RT，首包 RT，缓存命中等可观指标。同时所有的输入输出 Tokens 也都记录在日志服务 SLS 中，可供用户做更详细的分析。


AI 网关代理 LLM 更详细的方案可以参见我之前的文章：[](https://mp.weixin.qq.com/s?__biz=MzUzNzYxNjAzMg==&mid=2247573215&idx=1&sn=f77c5dd8423a9480afb6a03fce0d997c&scene=21#wechat_redirect)

[https://mp.weixin.qq.com/s/tZ0wsTlZK67r9IxNZ57TDQ](https://mp.weixin.qq.com/s?__biz=MzUzNzYxNjAzMg==&mid=2247573215&idx=1&sn=f77c5dd8423a9480afb6a03fce0d997c&scene=21#wechat_redirect)

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67f9c032837e6d746359dd33/25612747-739b-4966-b5ee-dea61998ba54.png)

#### MCP 网关

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67f9c032837e6d746359dd33/4d686611-378f-450c-ae61-5632755f7329.png)

MCP Client 和 MCP Server 之间的交互和传统的服务提供者和服务消费者之间的交互就有所区别了，所以我们在云原生 API 网关中增加了 MCP 相关的能力，但从产品版本划分层面，MCP 相关的能力依然包含在 AI 网关的能力范畴内。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67f9c032837e6d746359dd33/c4877ec0-3b39-4bb7-83e5-31735dcf5fc1.png)

##### MCP Server 动态发现

上文中介绍了 MSE Nacos 作为 MCP Server 注册/配置中心，那么 MCP Client 如何来发现呢？如果是 MCP Client 直接和 MSE Nacos 交互，那么又会在 MCP Client 中引入 Nacos SDK，增加了编码的复杂度。

鉴于云原生 API 网关和 MSE Nacos 在传统服务领域早已做了深度集成，打通了云原生 API 网关自动发现注册在 MSE Nacos 中的服务，所以在 MCP 范式下，我们同样实现了云原生 API 网关自动发现注册在 MSE Nacos 中的 MCP Server 的能力。

通过这种方式，MCP Client 只需要使用云原生 API 网关的接入点，即可自动的、动态的获取到所有注册在 MSE Nacos 中的 MCP Server。云原生 API 网关（MCP网关）就变成了一个 MCP Hub，无论如何更新、变更 MCP Server，都只需要在 MSE Nacos 操作即可，MCP Client 无需做任何修改。

##### 将传统服务 0 代码改造转换为 MCP Server

在 AI 的时代下，我认为最有价值的是使用 AI 增强、提升客户的现存业务，使其变成一个 AI 应用或 AI 加持的业务，而不是完全新开发一套 AI 应用。

所以开发一个 AI 应用或者做现存业务的 AI 增强，AI Agent 是需要和大量现存业务做交互的，MCP 虽然统一的协议，但将现存业务重构为 MCP Server 的成本是非常高的，并且目前支持的开发语言有限，像 Go，PHP 都没有对应的 MCP SDK，所以会让很多企业想拥抱 MCP，但又无从下手。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67f9c032837e6d746359dd33/8c984313-a7d1-4310-908f-d31d74832023.png)

网关最擅长做的事情就是协议转换，Nacos 在传统微服务场景下已经注册了很多现存的传统服务，那么两者一拍即合，通过网关将注册在 Nacos 中的传统服务 0 代码改造的转换为 MCP Server。

- 注册在 MSE Nacos 中的现存业务服务（SpringCloud 服务、Dubbo 服务、Go 服务）不需要做任何改变。
- 在 MSE Nacos 中新增`[Server Name]-mcp-tools.json`命名规范的配置文件，在配置文件中使用 MCP 规范对现存业务的接口进行描述。
- 通过云原生 API 网关（MCP 网关），MCP Client 侧自动发现由传统服务转换来的 MCP Server。


##### 将 SSE 转换为 Streamable HTTP

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67f9c032837e6d746359dd33/f51980df-8b56-4044-bd59-af50005eb18a.png)

MCP 范式默认的传输协议是 SSE（Server Sent Event），本质上是一种长连接，有状态的传输协议。这种协议在企业级应用中有很多弊端：

- 不支持可恢复性（Resumability）：连接断开后，客户端必须重新开始整个会话。
- 服务器需要维持长期连接（High Availability Requirement）：服务器必须保持高可用性，以支持持续的 SSE 连接。
- SSE 仅支持服务器 → 客户端消息，无法灵活进行双向通信。
- 目前只有少数几个 C/S 架构的客户端和 MCP 提供的用于测试验证的 Web 客户端支持 MCP 范式和 SSE 协议。无法用在企业级的生产应用中。


好在 MCP 官方也意识到了该问题，所以在 3 月下旬，发布了新的 Streamable HTTP 协议。Streamable HTTP 改变了 MCP 的数据传输方式，让协议变得更灵活、更易用、更兼容：

- 更灵活：支持流式传输，但不强制。
- 更易用：支持无状态服务器。
- 更兼容：适用于标准 HTTP 基础设施。


简单来说，原来的 MCP 传输方式就像是你和客服通话时必须一直保持在线（SSE 需要长连接），而新的方式更像是你随时可以发消息，然后等回复（普通 HTTP 请求，但可以流式传输）。

这里大家可以思考一下：

- Streamable HTTP 打破了目前几个 C 端 MCP Client 的壁垒。也就意味着任何请求方（甚至就是一段简单的 HTTP Request 代码），都可以像请求标准 HTTP API 的方式一样和 MCP Server 交互。
- 换句话说，当可以使用标准 HTTP API 的方式和 MCP Server 交互后，是不是就不存在所谓的 MCP Client了？


虽然 Streamable HTTP 还在草案阶段，但云原生 API 网关作为 MCP 网关已经支持了将 SSE 传输协议自动转换为 Streamable HTTP 传输协议。或者说，通过云原生 API 网关（MCP 网关）代理的 MCP Server 同时支持 SSE 和 Streamable HTTP 两种传输协议供 Client 使用。

##### MCP 模式下的身份认证和权限管控

身份认证和权限管控在任何架构，任何业务场景下都是刚需，在 MCP 范式下也不例外，这里有两个层面的权限管控：

- Client 有权使用哪些 MCP Server。有权使用某 MCP Server 里的哪些 MCP Tool。
- Client 通过 MCP Tool 有权获取到哪些数据。


![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67f9c032837e6d746359dd33/69b0a4dc-5fc2-47f1-b63d-c9ffeb2df883.png)

###### MCP Server 和 MCP Tool 的使用权限

大家设想一下，当传统业务可以 0 代码转换为 MCP Server 后，注册在 Nacos 中的 MCP Server 和 MCP Tool 肯定会有很多，从业务领域来说，可能有和财务相关的 MCP Server，有和销售相关的 MCP Server，有和售后服务相关的 MCP Server。在返回 MCP Server 和 MCP Tool 信息时不可能将所有信息都返回，肯定只能返回 Client 身份有权使用的 MCP Server 信息。

云原生 API 网关作为 MCP 网关，通过成熟的插件机制提供了 HTTP Basic Auth，OAuth2.0，JWT，API Key，外部认证等多种认证方式，以及基于消费者认证功能，可以让用户灵活的管理和控制 Client 的身份认证和 MCP Server/MCP Tool 使用权限。

###### MCP Server 和 MCP Tool 的数据权限

当 MCP Server 是数据类服务时会比较常见，比如 Mysql MCP Server，Redis MCP Server 等。权限会下探到库级别，表级别。在这种场景下，云原生 API 网关作为 MCP 网关，可以通过插件机制，改写或增加 Request Header 的值，结合 MSE 治理将 Header 的值透传下去，然后在服务内部进一步做数据权限管控。

我举例一个通过这种方式实现的数据库读写分离的场景：

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67f9c032837e6d746359dd33/316d17b3-c8a5-45cd-a239-d196622d137f.png)

### 如何快速构建 MCP Server

众所周知，AI 应用里涉及到 LLM 推理的场景，大都用在调用相对稀疏的场景，MCP 范式强依赖 LLM 推理，所以无论是基于 HTTP API 模式的 AI 应用开发架构还是基于 MCP 的 AI 应用开发架构，目前也都是应用在相对稀疏调用的场景。所以这里可以延伸出两个问题：

- 在稀疏调用的场景下，运行 MCP Server 的计算资源如何优化资源利用率，说的再直白一些就是如何能做到成本最优。
- 在新的业务中，如何快速构建 MCP Server。


在所有的计算产品中，函数计算（FC）这种 Serverless FaaS 类型的计算产品，在资源粒度、弹性策略、弹性效率方面都是最适合稀疏调用场景的。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67f9c032837e6d746359dd33/1e89784d-06b0-4d64-afbf-2a20c890bc67.png)

函数计算（FC）目前支持了 Python 和 NodeJS 两种语言的 MCP 运行环境（其他语言的 MCP 运行环境也马上会支持）。用户选择 MCP 运行环境创建函数后，只需要编写 MCP Tool 的业务逻辑即可，不需要考虑如何使用 MCP SDK。并且云原生 API 网关和函数计算（FC）有深度集成，可以天然适配 AI 应用开发的新范式。

#### MCP Server 的弹性效率

基于函数计算（FC）构建的 MCP Server 在弹性效率方面可以从两个维度来看：

- 资源规格细粒度管控。
- 完全按请求弹性。


函数计算（FC）的实例规格从 0.05C 128MB 到 16C 32GB 不等，有几十种规格的组合方式，可以灵活的根据不同 MCP Server 承载的业务选择合适的资源规格。另外，在 AI 应用中，尤其是流程式构建的模式中，大多数 AI Agent 的职责都是单一的，计算逻辑不复杂的任务，所以都可以用较小资源规格的函数承载。资源规格小，在资源调度，弹性效率方面自然就会有优势。

再看函数计算（FC）的弹性机制，它是完全按照请求弹性的，有多少 QPS，就拉起对应数量的实例，并且实例可以复用，当 QPS 降下来后，空闲的实例会自动释放，整个过程完全不需要用户介入参与。在默认按请求弹性的的基础上，用户还可以自行设置按照时间定时弹，或按照指标阈值弹的策略，进一步满足复杂多变的业务场景，做到资源成本最优。

#### MCP Server 的可观测

函数计算（FC）有完善的可观测体系，也就意味着，基于函数计算（FC）构建的 MCP Server 同样具备指标、链路、日志三个维度的可观测能力。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67f9c032837e6d746359dd33/e9e83529-35b3-417e-87a5-d40bc9bf9f4d.png)

通过这套可观测体系，用户可以清晰的了解每个 MCP Server 的各类运行状态。

### 如何解决开源自建 Dify 的痛点问题

目前，Dify 基本已是可视化流程编排 AI Agent 使用最广泛的工具，但是目前还没有任何一家云厂商有 Dify 托管产品，所以很多基于开源自建 Dify 平台的客户会遇到很多共性的问题，尤其是从个人开发者、开发 Demo 转向企业级生产应用构建时，这些问题往往都是致命的。

企业基于开源自建 Dify 遇到的问题：

- 流量防护弱：基于开源自建没有任何防护措施，很容易被穿透。
- 管控与数据链路耦合：AI 应用设计与 Agent 的执行耦合在一起，在高并发场景下无法保证稳定性。
- 负载均衡问题：在大流量情况下，Dify 的核心服务可能会因为流量负载不均导致稳定性下降。
- 可观测缺失：开源 Dify 本身不带可观测能力，需要额外搭建可观测体系。


为了解决这些问题，阿里云上的 Serverless PaaS 类型的计算产品 Serverless 应用引擎（SAE）做了企业生产级别的 Dify 托管部署方案，旨在解决上述问题，让企业在使用 Dify 的时候不用再关心稳定性、健壮性、性能这些问题。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67f9c032837e6d746359dd33/bb6f02d4-7101-4f9f-a5cb-bf0b9dbd7d26.png)

#### 快速部署 Dify

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67f9c032837e6d746359dd33/f475cb47-4f19-4c7b-88cc-fa927cbdb500.png)

SAE 提供了 Dify 应用模板，可以一键拉起 Dify 应用，并且提供可视化构建的能力，可以对 Dify 里的每一个环节进行单独调整。

#### 保障 Dify 稳定高可用

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67f9c032837e6d746359dd33/a81772ad-0348-418d-94da-f30f8f64d65f.png)

SAE 部署 Dify 支持配置化，三 AZ 部署，实例粒度的自动化迁移，结合云原生 API 网关和 SAE 内置的服务治理能力，保障负载均衡稳定性，同时还支持 Dify 6 个核心服务的健康检查，以及无损上下线。

同样依托于底层 Serverless 架构，部署在 SAE 中的应用同样具备优秀的横向扩展效率，并且支持多种方式的弹性规则配置，使整套 Dify 服务可以根据不同的业务场景进行弹缩，在保证高可用的同时，又兼具成本优势。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67f9c032837e6d746359dd33/a888787e-ab73-4b5b-a783-2582e7936a5c.png)

除此以外，SAE 还支持小流量预热，CPU Burst 等能力，进一步保证 Dify 应用在极端情况下的稳定性。

#### Dify 任务调度方案

定时执行工作流做 AI 数据处理是通用的业务场景，Dify 官网已经把通过定时任务做Dify工作流的定时执行和状态监控作了最佳实践，可以参考https://docs.dify.ai/zh-hans/learn-more/use-cases/dify-schedule。但是该实践中的 Dify Schedule 比较简陋，通过 Github Actions 做定时调度，只能调度公网的 dify 工作流，且不是一个企业级解决方案。

开源 Dify 在调度方面的痛点主要有 3 点：

- 执行记录过多会导致慢查询。


- 执行历史记录存储在数据库中，数量太多会影响 Dify 性能，导致慢查询。


- 执行记录查询不支持条件过滤。


- 比如通过时间区间查询，通过任务状态查询，这些都是通用的需求，但开源 Dify 都不支持。


- 没有报警监控。


- 任务调度系统需要监控工作流的执行状态，工作流运行失败，需要报警给对应的负责人，开源无报警监控能力。


我们的方案是通过 MSE 任务调度（SchedulerX）来解决上述问题。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67f9c032837e6d746359dd33/a6b8c489-08cc-476d-a191-bd13261d50ec.png)

- 用户在 MSE 任务调度中配置 Dify 的 Endpoint，MSE 任务调度通过 Dify API 拉取工作流应用。
- 用户通过 MSE 任务调度配置定时调度和报警监控。
- Dify 工作流定时调度的时候，MSE 任务调度通过 Dify 提供的 API 调度用户的 Dify 应用，并且实时拉取执行结果和详情，存储在 MSE 的 AI 任务调度中。
- 通过 AI 任务调度做报警监控、可观测增强。


MSE 任务调度集成 Dify 方案对比开源方案有以下 7 点优势：

功能MSE任务调度 + Dify开源Dify定时调度有无监控告警有无执行记录保留时长保留最近2个月无限制，但数据量太大会导致查询性能太差执行记录查询支持时间区间、状态等多种查询条件过滤条件有限权限管理操作级别精细化权限管理用户级别限流应用限流、Token限流无失败自动重试有无

### AI 应用可观测体系

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67f9c032837e6d746359dd33/18d4bdb8-a83f-4fdd-ac2c-998448dad7d6.png)

结合阿里云可观测产品 ARMS，链路追踪 OpenTelemetry，我们构建了 AI 应用全环节的可观测体系。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67f9c032837e6d746359dd33/30e9dfdf-9b96-4706-b46e-b97dd44a502d.png)

AI 应用整体的可观测体系构建主要有两部分核心：

- 数据采集。
- 数据串联与分析。


#### 观测数据采集

数据采集的核心是要覆盖足够的广，这里又分两个层面：

- 编程语言，开发框架要支持的足够广，足够全。
- AI 应用架构新范式里涉及到的云产品也需要以相同的标准上报数据。


在这两个层面，我们通过阿里云应用监控产品 ARMS 和链路追踪 OpenTelemetry 实现了全覆盖：

- 遵循最新 OpenTelemetry 社区 GenAI 语义约定。
- 支持常见的 AI 框架和 AI 模型，包括 Spring AI Alibaba / LLamaIndex / Langchain / 通义千问2 / OpenAI / PromptFlow 等。
- 支持 AI 应用开发的主流编程语言，Python，Java，Go。并且相比社区规范提供更加精细化的埋点和属性。
- 支持在不同的调用链中传播会话信息。
- 云原生 API 网关支持 OpenTelemetry 协议，网关自身和插件都会基于 OpenTelemetry 上报观测数据。
- 函数计算 FC 和 Serverless 应用引擎 SAE 均与应用监控 ARMS 以及链路追踪OpenTelemetry 版产品均做了深度集成。


#### 数据串联与分析

应用监控 ARMS 中，专门构建了 LLM 应用监控模块，针对AI应用场景提供了完善的可观测体系。

纵向的指标有：

- 在线 AI 应用数。
- Trace 数。
- Span 数。
- 大模型数。
- Token 使用情况。
- 会话数。
- 用户数。
- 模型调用次数。
- Token 消耗情况。
- 模型调用耗时。
- Token 消耗排行。
- 等等...


横向链路方面提供了专业的调用链分析功能：

- Span 列表。
- Trace 列表。
- 散点图。
- 全链路聚合。
- 全链路拓扑。
- 错/慢 Trace 分析。
- 调用链上的每个环节都会输入、输出、Token 消耗的展示。


### 更多在途的功能规划

#### Dify DSL 转 Spring AI Alibaba 编码

虽然 Dify 在做 AI Agent 开发时已足够便利，但是受限于 Dify 的开发语言（Python）和流程引擎的实现逻辑。在运行复杂 AI 应用时，性能方面是有缺陷的。所以我们在探索将 Dify 流程的 DSL 自动转换为基于 Spring AI Alibaba 开发框架的代码。

相当于只使用 Dify 低代码可视化构建 AI 应用的皮，运行的内核基于 Spring AI Alibaba 开发框架的代码，这样既具备了便捷的 AI Agent 编排能力，又具备了更好的运行性能。

#### 基于 LLM 编排 MCP Server

目前的 MCP 模式，LLM 针对用户的输入，只返回一个确定的 MCP Server 和 MCP Tool，这是其实是由系统提示词控制的。理论上 LLM 可以针对用户的输入返回多个 MCP Server 和多个 MCP Tool，并且基于 MCP Server 和 MCP Tool 的描述告诉 Client 它们之间的调用顺序，相当于由 LLM 做好了 MCP Server 的编排。这个模式我们还在探索中，很类似现在的 Multi-Agent 的模式。

#### 提高MCP模式的性能

因为 MCP 模式中，会频繁和 LLM 交互，显而易见，相比传统 API 调用，MCP 这种模式的性能是不好的，所以在一些时延敏感的业务场景中，目前大概率还不适合 MCP 模式。

目前我们也在探讨和探索如何提高 MCP 模式下的请求性能问题，比如：

- 固化 MCP Server/MCP Tool 组合，减少和 LLM 的交互。尤其当实现 LLM 编排 MCP Server 后，和 LLM 的交互可能就只存在于开发态或调试态，云形态时使用的都是固化好的 MCP Server 和 MCP Tool 的调用关系。
- 函数计算探索边缘场景，将 MCP Server 运行在离用户更近的地方。


***AI 应用架构新范式对企业的影响***

*Cloud Native*

至此，企业级 AI 应用架构新范式的介绍就结束了，整个架构里有很多环节，每个环节里又有许多细节，在文章中无法一一展开说明。有兴趣的同学可以联系我共同探讨。

我们可以设想一下在这个 AI 应用架构新范式下，企业的运营、产品、研发、运维团队之间的组织结构和协作关系可能会发生哪些变化？应用或系统的开发模式会发生哪些变化？

这里我来分享一下我的畅想。

**MCP Server First**

API First，前后端分离这两个概念已经存在很久了，海外企业遵循和实践的会比较好。因为我深耕在 Serverless 计算领域也有 5 年时间，对 AWS 的 Lambda 架构方案，Azure Functions 架构方案，Azure App Service 架构方案，GCP CloudFunction 架构方案，GCP CloudRun 架构方案有比较多的研究。接触了很多 Serverless FaaS 和 Serverless PaaS 架构的客户案例，包括负责落地了不少从双 A 迁移到阿里云的客户。基本上都是标准的基于 APIG+FaaS 模式的 API First 形态。但是在国内，这个模式实践的并不好，除了高德下决定使用函数计算重构了系统，实现了真正的 API First，前后端分离模式以外，鲜有客户有这种模式的实践，也许是有太重的历史包袱。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67f9c032837e6d746359dd33/a2e604a7-67e4-4e0a-aa1a-353b1f17903a.png)

上图为高德前后的架构对比

在 AI 应用的时代，本质上依然是对各种 API 的调用，但是将 HTTP API 改成 REST API，改造成本是巨大的。但当 MCP 出现后，当我们的方案可以帮助客户 0 代码的转型 AI 应用架构新范式的时候，MCP Server First 是有可能。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67f9c032837e6d746359dd33/4c7c2d89-6045-46dd-a77a-525b5c7355d9.png)

- 运维团队：负责云产品的维护（比如云原生 API 网关，MSE Nacos，Serverless 应用引擎，PAI 这些产品的开通、升配），可观测体系的维护（也是基于云产品），和云厂商保持持续沟通。
- 研发团队：理解公司业务的原子化能力，负责构建 MCP Server 池。
- 运营/市场/产品：通过低代码可视化方式构建业务流程（业务编排），大白话描述业务需求，快速完成业务流程的搭建，或者说 AI 应用的构建。


所以未来很有可能每个企业都有自己的 MCP Server 市场，在 MCP Server 市场里分门别类，每类 MCP Server 有专门的研发团队负责，不用太需要考虑统一返回格式，不用考虑开发语言统一。运营、市场、产品等业务方有业务需求或者有新的产品功能需求时，可以通过统一界面用大白话快速构建 AI 应用，MCP+LLM 来实现业务编排，实现 PRD 即产品（PRD as a Product）的新的开发模式。

点击阅读原文获取 78 页完整版 PPT

