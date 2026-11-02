---
作者:
  - "玄姐聊AGI"
原文链接: https://mp.weixin.qq.com/s?__biz=MzIzODIzNzE0NQ==&amp;mid=2654453627&amp;idx=1&amp;sn=896de1346343350ff9816f109639ad51&amp;chksm=f3f02b4b212a7960c59b5201d97e2f5cc27a961be0d9ecf9208faa5ebe12b0e01e2fe46d3dcb&amp;mpshare=1&amp;scene=1&amp;srcid=0414OoNlIDEYWklhO645UHbF&amp;sharer_shareinfo=0ea363bb56f07280b5c404604fba4f36&amp;sharer_shareinfo_first=0ea363bb56f07280b5c404604fba4f36#rd
发布时间: ""
收藏时间: "2025-04-14"
关联日记: "[[2025-04-14]]"
tags:
  - 文章
---
大家好，我是玄姐。

本文提供了一个全面的视角，来看待如何利用模型上下文协议（MCP）实现 AI 应用架构设计新范式的落地实现，核心内容主要是以下5点：

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67fc4b06837e6d746367ab94/60707bd5-f657-4e35-86d8-c07f54be9b37.webp)

- MCP 概念与机制。
- MCP 与 Function Calling 区别。
- MCP 本质与挑战：挑战包括系统提示词的准确性、Client 与 Server 协同、快速构建 Server、自建 Dify 的痛点等。
- 解决 MCP 挑战的方法：通过 MCP Register、统一管理 Server 和 Prompt、建立效果验证体系与安全保障、设置 MCP 网关、动态服务发现、Streamable HTTP、弹性效率、可观测等手段解决。
- AI 应用架构设计新范式：MCP 推动 AI 应用架构向新范式发展，并通过 Server First 理念，提升应用性能和用户体验。


下面详细介绍之。

***—1****—*

**AI Agent 现状与架构**

**AI 大模型在商业领域的应用正成为推动创新和效率提升的核心力量。其关键在于多个AI Agent 的协作，这些 AI Agent 通过分工与合作，共同承载 AI 应用所支持的业务需求。这种协作模式不仅优化了企业运营，还展现了 AI 在解决高影响力挑战中的潜力。**

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67fc4b06837e6d746367ab94/62e3e052-af80-46d8-a87e-a61cf2878808.png)

目前 AI Agent 与各种 Tools（业务服务接口）、Memory（存储服务接口）以及 LLMs（大语言模型）的交互主要通过 HTTP 协议实现。除了 LLMs 基本遵循 OpenAI 范式外，与其他 Tools 和 Memory 的交互需要逐一了解它们的返回格式进行解析和适配，这增加了开发的复杂性。

当一个 AI 应用包含多个 AI Agent，或者需要与多个业务服务接口和存储服务接口交互时，开发工作量显著增加，主要体现在以下三个方面：

第一、寻找合适的接口

- 寻找三方服务接口。
- 在公司内部寻找合适的服务接口。
- 如果找不到，就需要自行开发接口。


第二、解析接口返回格式

- 无论是三方服务接口还是公司内部的服务接口，返回格式可能千差万别，需要逐一了解和解析。


第三、编排多个 AI Agent

- 使用如 Dify 这类流程可视化的工具辅助编排，虽然减轻了一些工作量，但复杂度依然较高，且在运行效率和性能方面存在瓶颈。
- 通过编码方式编排（比如：使用 Spring AI Alibaba 或 LangChain 等），虽然性能更优，但复杂度更高，编排效率和灵活性不足。


因此，目前许多 AI应用只包含少数几个 AI Agent，甚至很多应用背后只有一个 AI Agent。这也是目前 AI 应用背后的 AI Agent 仍处于第一阶段（Siloed, Single-Purpose Agents）的原因。

为了使 AI Agent 进入第二阶段（Platform-Level Agents），我们使用云原生 API 网关作为统一的接入层，通过网关的三种不同角色，解决了部分复杂度问题：

第一、作为南北向流量网关

- 统一管理 AI Agent 的入口流量，核心功能包括转发、负载均衡、鉴权认证、安全和流控等。


第二、作为 AI 网关

- 代理各类 LLMs，向 AI Agent 屏蔽了繁杂的接入，并解决了许多生产级问题，比如：多模型切换、模型 Fallback、多 API Key 管理、安全和联网搜索等。


第三、作为东西向网关

- 统一管理来自不同源（ACK、ECS、函数计算FC、SAE、三方服务）的各类服务，供 AI Agent 使用。


然而，上述方法仅解决了部分复杂度问题，更核心的寻找接口和解析接口的问题仍未得到解决。直到 MCP（Model Context Protocol）的出现，我们看到了真正通往第二阶段（Platform-Level Agents）的道路，甚至有望触及第三阶段（Universal Agents, Multi-Agents）。

***—2****—*

**MCP 架构设计剖析**

1、MCP 是什么？

MCP（模型上下文协议，Model Context Protocol）是由Anthropic（Claude 的开发公司）开发的开源协议，旨在为大语言模型（LLM）提供一种标准化的方式，以便它们能够连接到外部数据源和工具。它就像是 AI 应用的“通用接口”，帮助开发者构建更灵活、更具上下文感知能力的 AI 应用，而无需为每个 AI 模型和外部系统组合进行定制集成。

MCP 的设计理念类似于 USB-C 端口，允许 AI 应用以一致的方式连接到各种数据源和工具，如文件、数据库、API 等。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67fc4b06837e6d746367ab94/e0ca527c-1813-475a-8a59-df1c86a520c0.png)

MCP 包含三个核心概念：

第一、MCP Server

- 基于各语言的 MCP SDK 开发的程序或服务。它通过某种机制将现有的程序或服务转换为 MCP Server，使其能够与 AI 应进行交互。


第二、MCP Tool

- MCP Tool 属于 MCP Server，一个 MCP Server 可以有多个 MCP Tool。可以将其理解为一个类中有多个方法，或者一个服务中有多个接口。


第二、MCP Client

- 当一段代码、一个 AI Agent 或一个客户端基于 MCP 的规范去使用或调用 MCP Server 中的 MCP Tool 时，它就被称为 MCP Client。


2、MCP 的运作机制

要真正理解 MCP，我们需要深入其运作机制，这不仅能揭示 MCP 调用方式与传统 HTTP 调用方式的差异，还能让你明白为何 MCP 能够助力 AI Agent 迈向第二阶段。

以开发一个获取时间的 AI Agent 为例，用户只需提问“现在几点了？”即可。假设我们已有一个处理时间的 MCP Server，其中包含两个 MCP Tool：一个用于获取当前时区，另一个用于获取当前时间。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67fc4b06837e6d746367ab94/668a8d86-d5d8-46ef-afd9-298bb20bd6ef.png)

基于 MCP 的调用过程分为六个核心步骤：

第一、用户提问

- 用户向 AI Agent 提问“现在几点了？”。此时，AI Agent 作为 MCP Client，将用户问题连同处理时间的 MCP Server 及 MCP Tool 信息一并发送给 LLM。


**第二、LLM 推理**

- LLM 接收到信息后，根据用户问题和 MCP Server 信息，筛选出最合适的 MCP Server 和 MCP Tool 来解决问题，并将结果反馈给 AI Agent（MCP Client）。LLM 返回的信息可能是：“使用 time MCP Server 中的 get_current_time MCP Tool，它能解决用户的问题。”


**第三、调用 MCP Tool**

- AI Agent（MCP Client）依据 LLM 的建议，调用 time MCP Server 中的 get_current_time MCP Tool，获取当前时间。


**第四、返回结果**

- time MCP Server 将当前时间的结果返回给 AI Agent（MCP Client）。


**第五、内容规整**

- AI Agent（MCP Client）将用户问题和从 time MCP Server 获取的结果再次提交给 LLM，请求 LLM 结合问题和答案规整内容。


**第六、最终反馈**

- LLM 将规整后的内容返回给 AI Agent（MCP Client），AI Agent 再将结果原封不动地返回给用户。


在整个 MCP 调用过程中，MCP Server 及 MCP Tool 的信息至关重要。从第一步和第二步可以看出，这些信息为 LLM 提供了解决问题的关键线索。这些信息本质上就是 MCP 中的 System Prompt，其核心作用是为 LLM 提供清晰的指导，帮助其更好地理解用户需求并选择合适的工具来解决问题。

3、MCP System Prompt

MCP（模型上下文协议）与传统协议定义不同，它并没有固定的数据结构。其核心在于通过自然语言清晰地描述 MCP Serve r和 MCP Tool 的功能及作用，让大语言模型（LLM）通过推理来选择最合适的 MCP Server 和 MCP Tool。因此，MCP 的本质仍然是提示词工程（Prompt Engineering）。

以下是一些关键的示例和步骤解析：

#### 第一、 MCP Client（Cline）中的 System Prompt

Cline 是一个 MCP Client，其 System Prompt 对 MCP Server 和 MCP Tool 都有明确的描述。比如：它会详细说明每个 MCP Server 的功能以及其中包含的 MCP Tool 的作用。这种描述为 LLM 提供了足够的上下文，使其能够理解每个工具的用途。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67fc4b06837e6d746367ab94/45126010-76c6-420a-9194-0b92ddd00c49.png)

上图告诉 LLM：

- 告诉 LLM 你有一堆工 具可以用。告诉 LLM 每次你只能选一个工具用。告诉 LLM 工具是通过 XML 描述定义的。并详细描述了 XML Tag 的定义。并给出了样例。本质就是告诉 LLM 你选择完后该返回什么样的格式。


![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67fc4b06837e6d746367ab94/2cf393bd-b02c-4d20-8f4a-af22c5a811bc.png)

上图告诉 LLM：

- 向 LLM 解释了什么是 MCP。
- 对每个 MCP Server 和 MCP Tool 做了详细描 述。包括传参格式。


#### 第二、流程第一步：发送问题和 System Prompt

在调用流程的第一步，用户的问题（如“现在几点了？”）和 System Prompt 一起被发送给 LLM。System Prompt 的作用是为 LLM 提供清晰的指导，帮助其理解用户问题的背景和可用的工具。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67fc4b06837e6d746367ab94/c5c491f3-9b88-4f58-a64a-bb2373a9291b.png)

#### 第三、流程第二步：LLM 返回解决方案

在第二步，LLM 根据用户问题和 System Prompt 中的信息，推理出最合适的 MCP Server 和 MCP Tool，并返回明确的解决方案。比如：LLM 可能会返回：“使用 time MCP Serve r中的 get_current_time MCP Tool 来解决用户的问题。”并以 XML 格式 返回给 Client/Agent。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67fc4b06837e6d746367ab94/9ff22c2d-3013-48bc-87a7-ba79db5a8986.png)

通过这种方式，MCP 利用自然语言描述和 LLM 的推理能力，动态地选择和调用最适合的工具，从而实现灵活且高效的 AI 应用开发。

4、MCP 与 Function Calling 区别

通过前面的介绍，相信大家对 MCP 有了清晰的认识。MCP 是否解决了找接口和解析接口的问题呢？答案是肯定的。因为这两个任务都交给了 LLM（大语言模型）来完成。

**第一、LLM 负责为 AI Agent 找到最合适的接口**。

**第二、AI Agent 调用接口时，无需解析返回结果**，而是将结果原封不动地交给LLM。

**第三、LLM 结合用户问题和接口返回的结果，进行内容规整处理**。

那么，MCP 与 LLM 的 Function Calling 有什么区别呢？核心区别在于是否绑定特定的模型或模型厂商：

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67fc4b06837e6d746367ab94/afb33300-d38a-4145-b62c-b27e61f82deb.png)

**第一、MCP 是通用协议层的标准**，类似于“AI 领域的 USB-C 接口”，定义了 LLM 与外部工具/数据源的通信格式，但不绑定任何特定模型或厂商。它将复杂的函数调用抽象为客户端-服务器架构，使得不同模型和工具之间的交互更加灵活和通用。

**第二、Function Calling 是大模型厂商提供的专有能力**，由大模型厂商定义，不同厂商在接口定义和开发文档上存在差异。它允许模型直接生成调用函数，触发外部 API，依赖模型自身的上下文理解和结构化输出能力。

例如，LLM Function Calling 需要为每个外部函数编写一个 JSON Schema 格式的功能说明，并精心设计一个提示词模板，才能提高 Function Calling 响应的准确率。如果一个需求涉及几十个外部系统，那么设计成本将是巨大的，产品化成本极高。

而 MCP 统一了客户端和服务器的运行规范，并且要求 MCP 客户端和服务器之间也统一按照某个既定的提示词模板进行通信。这样，通过 MCP 可以加强全球开发者的协作，复用全球的开发成果，降低开发成本，提高开发效率。

5、MCP 的本质与挑战

通过前面的讨论，我们可以总结 MCP（模型上下文协议）的本质：MCP 并非一个固定的数据格式或结构，而是系统提示词与 MCP Server 和 LLM 之间协同关系的结合。它通过自然语言描述 MCP Server 和 MCP Tool 的功能，让 LLM 能够推理出最适合的工具来解决问题，从而解决了找接口和解析接口的问题。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67fc4b06837e6d746367ab94/a0e04297-4da8-4352-82cb-2a5c146b5a7d.png)

然而，将 MCP 引入企业级生产应用时，会面临诸多挑战：

### 第一、描述 MCP 信息的系统提示词的挑战

- **系统提示词的安全性**：系统提示词是 MCP 的核心，如果被污染，LLM 可能会被误导，选择错误甚至存在安全漏洞的 MCP Server 和 MCP Tool，从而导致整个 MCP 流程瘫痪，给 AI 应用带来巨大风险。系统提示词的管理：当 MCP Server 或 MCP Tool 更新时，系统提示词也需要相应地进行版本管理，以确保 LLM 能够获取最新的工具信息。系统提示词的调试与实时生效：系统提示词没有标准定义，每个企业都可以自定义模板。由于提示词需要反复调试，因此需要一种机制能够快速调整并实时生效。系统提示词的 Token 消耗：如果 MCP Server 和 MCP Tool 数量众多，系统提示词会变得非常长，消耗大量 Token，增加成本。因此，需要一种机制基于用户问题预筛选 MCP Server 和 MCP Tool 的范围，减少 Token 消耗，提高效率。


第二、MCP Client 与 MCP Server 之间协同关系的挑战

- **MCP Client 的稀缺性**：目前市面上的 MCP Client（比如：Cline、Claude、Cursor 等）数量有限，且大多基于 C/S 架构，仅支持 SSE 协议。这种有状态的协议存在诸多弊端，比如：不支持可恢复性、服务器需维持长期连接、仅支持单向通信等，难以与企业级 AI 应用结合。现存业务的转换难题：开发 MCP Server 依赖于特定语言的 MCP SDK （目前仅支持 Python、Java、TS、Kotlin、C#）。对于使用 Go 或 PHP 等其他技术栈的企业，转换为 MCP Server 的工作量巨大，且不现实。MCP Server 的统一管理：企业可能拥有自建的 MCP Server、第三方的 MCP Server 以及通过某种机制转换而来的 MCP Server。需要一个类似 MCP Hub 或 MCP 市场的平台来统一管理这些 Server，方便 MCP Client 使用。企业级应用中的安全与权限问题：在企业级应用中，身份认证、数据权限和安全防护是关键问题。在 MCP 的协同模式下，如何实现这些功能是亟待解决的挑战。


总之，尽管 MCP 为 AI 应用开发带来了灵活性和效率提升，但在企业级应用中，仍需克服系统提示词的安全性、管理、调试以及 MCP Client 与 MCP Server 之间的协同关系等多方面的挑战。

***—3****—*

**AI 应用架构设计新范式**

为了解决 MCP 在企业级应用中面临的诸多挑战，对 AI Agent 的架构进行了深度重构。通过在云原生 API 网关和注册配置中心 Nacos 中引入 MCP 增强能力，成功解决了大部分挑战点。同时，分别针对快速开发 MCP Server 和提升开源 Dify 性能的问题提供了有效解决方案。这些举措共同构建了一个基于 MCP 的 AI 应用开发新范式，推动了 AI 应用的高效开发与部署。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67fc4b06837e6d746367ab94/b55a464f-b19a-40e3-a58b-77cfaad86f1b.png)

云原生 API 网关与 Nacos 的 MCP 增强：通过这两个产品的增强能力，解决了系统提示词的安全性、管理、调试以及 MCP Client 与 MCP Server 之间的协同关系等核心挑战。云原生 API 网关提供了强大的流量管理和安全防护功能，而 Nacos 则在服务发现和配置管理方面发挥了关键作用，确保了 MCP Server 和 LLM 之间的高效协同。

通过这些增强能力的实现，解决了 MCP 在企业级应用中的关键挑战。

3.1、AI 应用架构新范式剖析

AI 应用架构结合 MCP，我们定义了 AI 应用架构的新范式。

一个云原生 API 网关三种角色，具备统一的管控底座，同时又实现各角色的协同调度。

Nacos 发挥注册中心优势，增加 MCP Server 的注册能力，实现普通服务和 MCP Server 的统一管理，结合网关实现现存业务0改造转换为 MCP Server。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67fc4b06837e6d746367ab94/bb233290-12fc-44be-80e1-822583e457e1.png)

以下是对图中8步核心调用链路的解析：

第一步用户请求：用户向 AI 应用发起请求，请求流量首先进入流量网关（云原生 API 网关）。

第二步请求转发：云原生 API 网关维护管理不同类型的 AI Agent 的 API 或路由规则，将用户请求转发至对应的 AI Agent。

第三步获取 MCP 信息：AI Agent 在需要获取数据时，向 MCP 网关（云原生 API 网关）请求获取可用的 MCP Server 及 MCP Tool 信息。

第四步 LLM 交互（可选）：MCP 网关可能维护大量 MCP 信息，借助 LLM 缩小 MCP 范围，减少 Token 消耗，向 AI 网关（云原生 API 网关）发请求与 LLM 交互。

第五步返回 MCP 信息：MCP 网关将确定范围的 MCP Server 及 MCP Tool 信息列表返回给 AI Agent。

第六步发送至 LLM：AI Agent 将用户请求信息及从 MCP 网关获取的所有 MCP 信息通过 AI 网关发送给 LLM。

第七步 LLM 推理：LLM 经过推理，返回解决问题的一个或多个 MCP Server 和 MCP Tool 信息。

第八步调用 MCP Tool：AI Agent 拿到确定的 MCP Server 和 MCP Tool 信息后，通过 MCP 网关对该 MCP Tool 发起请求。

在实际生产中，步骤3至8会多次循环交互。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67fc4b06837e6d746367ab94/19887552-74b7-4863-9e45-b0f0a051f12d.png)

基于 MCP 的两个本质——系统提示词和 MCP Server 与 LLM 之间的协同关系，我们可以深入剖析这个新架构。

3.1.1、MCP Register（MCP Server 注册中心）

在 MCP Server 和 MCP 提示词的统一管理方面，借鉴了微服务领域中 Nacos 的服务注册发现和配置统一管理的模式，并将其应用于 MCP 范式。以下是这些概念之间的对应关系：

- SpringCloud 服务/Dubbo 服务/Go 服务 → 各类 MCP Server
- SpringCloud 服务/Dubbo 服务/Go 服务暴露的接口 → 各类 MCP Server 提供的 MCP Tool
- SpringCloud 服务/Dubbo 服务/Go 服务暴露的接口描述 → 各类 MCP Server 提供的 MCP Tool 的描述
- SpringCloud 服务/Dubbo 服务/Go 服务的配置文件 → 各类 MCP Server 的系统提示词


![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67fc4b06837e6d746367ab94/6b778095-8ac8-4107-9233-ddac22518ee7.png)

基于这些对应关系，在 Nacos 产品中实现了一系列增强 MCP 的能力。通过这些增强，Nacos 成为了统一管理 MCP Server 的 MCP Register（MCP Server 注册/配置中心），成为 AI 应用开发新范式的核心组件。

第一、MCP Server 统一管理

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67fc4b06837e6d746367ab94/28660000-f58d-4240-90a2-8d0bef475756.png)

MCP Server 注册到 Nacos 有两种方式：

- 手动创建：在 Nacos 控制台手动创建，将 MCP Server 的 Endpoint 配置到 Nacos 中。


- 自动注册：通过 Nacos SDK 自动将 MCP Server 注册到 Nacos，逻辑与当前 Java SpringCloud、Java Dubbo 服务类似。


在 Nacos 中对 MCP Server 进行统一管理，可以实现以下功能：

- 健康检查：监控 MCP Server 的健康状态。
- 负载均衡：合理分配流量，提高系统稳定性。
- 描述信息转换：支持从 JSON 到 XML 的格式转换。
- 上下线管控：灵活控制 MCP Server 的上线和下线。


第二、MCP Prompt 统一管理

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67fc4b06837e6d746367ab94/09abf236-bbf9-4218-b07b-918cc1847a55.png)

在 Nacos 中维护 MCP Server 的 Prompt 有两种方式：

- 手动创建：手动创建 MCP Server 的配置信息，配置文件的 Data ID 命名格式为 [MCP Server name]-mcp-tools.json。在配置文件中管理 MCP Tool 的提示词信息，比如：整体作用描述、入参描述等。
- 自动感知：结合治理能力，如果是Java或Go语言，可以自动感知服务的 Schema，自动生成 MCP Server 和 MCP Tool 的提示词信息。


通过 Nacos 对 MCP Server 提示词进行统一管理，可以实现以下功能：

- 版本管理：支持版本回滚，确保系统稳定运行。
- 灰度管理：支持灰度发布，逐步推广新版本。
- 安全管理：确保提示词的安全性，防止被污染或篡改。
- 动态调优：支持动态调整提示词，实时生效，提高系统灵活性。


第三、MCP 效果验证体系

当 MCP Server 数量较多时，描述信息会变得复杂，导致 Prompt 过长，消耗大量 Token，降低 LLM 推理效率。因此，需要一种机制基于用户输入缩小 MCP Server 范围，减少 Token 消耗，提高推理效率。此外，提示词的好坏需要多次调试，MCP 流程强依赖提示词工程。如果提示词调整不当，LLM 无法返回准确的 MCP Server 和 MCP Tool，整个流程将无法使用。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67fc4b06837e6d746367ab94/37e1e52d-1d10-4119-bd1f-6137e566626b.png)

在 Nacos 中，构建一个 MCP 效果验证体系。核心原理是提供一个基于 Spring AI Alibaba 开发的 AI Agent，通过用户配置的业务输入、LLM、圈定的 MCP Server 和 MCP Tool 集合进行验证，并将结果以视图形式展示（如成功率等）。用户可以在 Nacos 中动态调整成功率低的 MCP Server 的提示词，进行优化。

第四、MCP 安全性保障

在企业生产中，安全性始终是第一位的，MCP 领域也不例外。需要考虑的环节更多，包括：

敏感信息安全管理：注册到 Nacos 的 MCP Server 可能包含 API Key、AK/SK、密钥、登录密码等敏感信息。Nacos 与阿里云 KMS 深度集成，对这些敏感信息进行加密处理。

Prompt 安全管理：同样依托于 Nacos 与 KMS 的深度集成，对 MCP Server 和 MCP Tool 的完整 Prompt（描述信息）进行加密处理，防止 Prompt 被污染。

Prompt 安全校验：结合验证体系和内容安全集成，实现 Nacos 对 MCP Server Prompt 的合法性校验，确保系统安全运行。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67fc4b06837e6d746367ab94/af200a04-86de-46a6-8a51-0e80fa3e4197.png)

通过以上措施，Nacos 不仅实现了 MCP Server 和 MCP Prompt 的统一管理，还构建了效果验证体系和安全保障体系，为 AI 应用开发提供了高效、灵活、安全的开发环境。

3.1.2、如何解决 MCP Client 与 MCP Server 之间协同关系的挑战

在 MCP 范式中，主要涉及三个角色之间的协同工作：

- **MCP Client**：与 LLM 交互，发起请求并接收响应。
- **LLM**：处理 MCP Client 的请求，推理并选择合适的 MCP Server 和 MCP Tool。
- **MCP Server**：提供具体的工具和功能，执行实际的任务。


**MCP Client 与 LLM **以及 **MCP Client 与 MCP Server **之间的协同关系，本质上是服务提供方与服务消费方之间的关系。这涉及到两个核心点：**代理协作**和**流量管控**。在传统的开发范式中，这些功能通常由网关来负责。因此，我们在云原生 API 网关中增强了 LLM 代理和 MCP Server 代理的能力，使其具备了流量网关、AI 网关（LLM 代理）和 MCP 网关的功能。这使得云原生 API 网关成为 AI 应用开发新范式的核心组件。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67fc4b06837e6d746367ab94/23daf146-a157-4427-8388-58f727a58afe.png)

在企业的整体系统架构中，通过使用云原生 API 网关，可以实现流量网关、API 网关、微服务网关、AI 网关和 MCP 网关的功能。这不仅在代理和流量管控层面实现了传统业务和 AI 业务的统一，还通过结合 AI 应用开发的新范式，平滑地将 AI 业务与传统业务相结合。这种整合方式极大地简化了企业的技术栈，提高了系统的灵活性和可维护性，同时也降低了开发和运维的复杂性。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67fc4b06837e6d746367ab94/d6b5fe6c-a530-4de8-8ab0-8460d2709861.png)

第一、云原生 API 网关

云原生 API 网关在业界得到了广泛应用，众多业务深度依赖其强大的企业级产品能力、稳定性和性能。因此云原生 API 网关的可靠性和高效性就变得极其重要。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67fc4b06837e6d746367ab94/140a5459-e2ba-414d-8c85-5c277389d94b.png)

第二、AI 网关

MCP Client 与 LLM 之间的交互，以及传统业务与 LLM 之间的交互，本质上都面临一系列共性问题。这些问题在应用生产环境中尤为突出，具体如下：

- **成本平衡问题**：部署大语言模型（比如：DeepSeek R1 671B 满血版）需要高昂的成本，至少需要2台8卡 H20 机器，年度费用超过100万元，且其 TPS 有限，难以满足多用户并发请求。即使是 Meta 新发布的 Llama4，也需要至少一张 H100 显卡来运行。因此，需要找到 TPS 与成本之间的平衡点。
- 模型幻觉问题：即使是性能强大的 DeepSeek R1 671B 满血版模型，在没有联网搜索的情况下，也会出现严重的幻觉问题。
- 多模型切换问题：单一模型服务存在较大风险和局限性，比如：稳定性风险，以及无法根据不同业务（消费者）需求选择最优模型。目前缺乏开源组件和框架来解决这类问题。
- 安全合规问题：企业客户需要对问答过程进行审计，以确保合规并降低使用风险。
- 模型服务高可用问题：当自建平台性能达到瓶颈时，需要一个大模型兜底方案，以提升客户对大模型的使用体验。
- 闭源模型 QPS/Token 限制问题：商业大模型通常基于 API Key 维度设置 QPS/Token 配额限制，需要一种有效方式快速扩展配额限制。


这些问题都是客户在实际使用过程中遇到的，有些源于大模型自身特性，有些则是部署架构导致。如果让客户逐一解决这些问题，不仅复杂度高，而且时间成本也很大。因此，需要 AI 网关的介入，以快速、统一地解决这些核心问题。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67fc4b06837e6d746367ab94/3d12d33b-8312-4905-b223-4f1727a635ac.png)

云原生 API 网关的 AI 网关增强能力主要体现在以下四个方面：

- **多模型适配**：能够代理市面上所有主流的模型托管服务，以及兼容 OpenAI 协议的 AI 服务。该模块包括协议转换、多 API Key 管理、Fallback、多模型切换等多个核心功能。


- **AI 安全防护**：安全防护涵盖三个层面：输入输出的内容安全防护、保护下游 LLM 服务的稳定，以及管控 AI 接口消费者。该模块包括内容审核、基于 Token 的限流降级、消费者认证等多个核心功能。


- **AI 插件**：AI 网关的灵活扩展机制通过插件形式实现，目前提供许多预置插件，用户也可以开发自定义插件来丰富 AI 场景流量的管控。比如：基于 AI 插件机制实现了结果缓存、提示词装饰器、向量检索等能力。


- **AI 可观测**：AI 场景的可观测性与传统场景有很大区别，监控和关注的指标也不同。云原生 AI 网关结合阿里云日志服务和可观测产品，实现了贴合 AI 应用业务语义的可观测模块和 AI 观测大盘，支持 Tokens 消费观测、流式/非流式的 RT、首包 RT、缓存命中等可观指标。同时，所有输入输出 Tokens 都记录在日志服务 SLS中，可供用户进行更详细的分析。


第三、MCP 网关

在 MCP 范式下，MCP Client 与 MCP Server 之间的交互模式与传统的服务提供者和服务消费者模式有所不同。为了更好地支持这种交互模式，在云原生 API 网关中增加了 MCP 相关的能力。尽管从产品版本划分层面，这些能力仍然属于 AI 网关的范畴，但它们专门针对 MCP 场景进行了优化。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67fc4b06837e6d746367ab94/2b662e47-1399-4414-82e9-1193f5429cc6.png)

1. MCP Server 动态发现

在前面的内容中，提到 Nacos 作为 MCP Server 的注册和配置中心。那么，MCP Client 如何发现这些注册的 MCP Server 呢？如果让 MCP Client 直接与 Nacos 交互，就需要在 MCP Client 中引入 Nacos SDK，这无疑会增加编码的复杂度。

鉴于云原生 API 网关和 Nacos 在传统服务领域已经实现了深度集成，能够自动发现注册在 Nacos 中的服务，我们在 MCP 范式下也实现了云原生 API 网关自动发现注册在 Nacos 中的 MCP Server 的能力。

通过这种方式，MCP Client 只需使用云原生 API 网关的接入点，即可自动、动态地获取所有注册在 Nacos 中的 MCP Server。云原生 API 网关（MCP 网关）变成了一个 MCP Hub，无论 MCP Server 如何更新或变更，只需在 Nacos 中操作即可，MCP Client 无需做任何修改。

2. 传统服务零代码改造为 MCP Server

在 AI 时代，最有价值的是使用 AI 增强和提升客户的现有业务，而不是完全重新开发一套 AI 应用。因此，在开发 AI 应用或进行现有业务的 AI 增强时，AI Agent 需要与大量现有业务进行交互。虽然 MCP 提供了统一的协议，但将现有业务重构为 MCP Server 的成本非常高，且目前支持的开发语言有限，像 Go 和 PHP 都没有对应的 MCP SDK。这使得许多企业虽然想拥抱 MCP，但却无从下手。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67fc4b06837e6d746367ab94/bde44bfe-69c2-4bce-afcb-1698738bc82c.png)

网关最擅长的是协议转换。Nacos 在传统微服务场景下已经注册了许多现有服务，因此我们将两者结合起来，通过网关将注册在 Nacos 中的现有服务零代码改造为 MCP Server。

注册在 Nacos 中的现有业务服务（比如；SpringCloud 服务、Dubbo 服务、Go 服务）无需做任何改变。

在 Nacos 中新增 [Server Name]-mcp-tools.json 命名规范的配置文件，在配置文件中使用 MCP 规范对现有业务的接口进行描述。

通过云原生 API 网关（MCP 网关），MCP Client 侧自动发现由传统服务转换而来的 MCP Server。

3. 将 SSE 转换为 Streamable HTTP

MCP 范式默认的传输协议是 SSE（Server Sent Event），本质上是一种长连接、有状态的传输协议。这种协议在企业级应用中存在许多弊端：

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67fc4b06837e6d746367ab94/0b8120af-a572-4707-9474-11cb3f6aa615.png)

- 不支持可恢复性（Resumability）：连接断开后，客户端必须重新开始整个会话。
- 服务器需要维持长期连接（High Availability Requirement）：服务器必须保持高可用性，以支持持续的 SSE 连接。SSE 仅支持服务器→客户端消息，无法灵活进行双向通信。目前只有少数几个C/S架构的客户端和 MCP 提供的用于测试验证的 Web 客户端支持 MCP 范式和 SSE 协议，无法应用于企业级的生产应用中。


幸运的是，MCP官方也意识到了这个问题，并在3月下旬发布了新的 Streamable HTTP 协议。Streamable HTTP 改变了 MCP 的数据传输方式，使协议更加灵活、易用和兼容：

- 更灵活：支持流式传输，但不强制。更易用：支持无状态服务器。更兼容：适用于标准 HTTP 基础设施。


简单来说，原来的 MCP 传输方式就像你和客服通话时必须一直保持在线（SSE 需要长连接），而新的方式就像你随时可以发消息，然后等待回复（普通 HTTP 请求，但可以流式传输）。

这里可以思考一下：

- Streamable HTTP 打破了目前几个 C 端 MCP Client 的壁垒，意味着任何请求方（甚至是一段简单的 HTTP Request 代码）都可以像请求标准 HTTP API 一样与 MCP Server 交互。
- 换句话说，当可以使用标准 HTTP API 的方式与 MCP Server 交互时，所谓的 MCP Client 可能就不存在了。


尽管 Streamable HTTP 仍在草案阶段，但云原生 API 网关作为 MCP 网关已经支持将 SSE 传输协议自动转换为 Streamable HTTP 传输协议。也就是说，通过云原生 API 网关（MCP 网关）代理的 MCP Server 同时支持 SSE 和 Streamable HTTP 两种传输协议供 Client 使用。

4. MCP 模式下的身份认证和权限管控

身份认证和权限管控在任何架构和业务场景下都是刚需，MCP 范式也不例外。这里有两个层面的权限管控：

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67fc4b06837e6d746367ab94/dcbfc06b-c717-4833-bf12-8b8ce75f49f2.png)

- Client 有权使用哪些 MCP Server：Client 有权使用哪些 MCP Server，以及有权使用某 MCP Server 中的哪些 MCP Tool。
- Client 通过 MCP Tool 有权获取哪些数据：当 MCP Server 是数据类服务时，权限会下探到库级别、表级别。


5. MCP Server 和 MCP Tool 的使用权限

当传统业务可以零代码转换为 MCP Server 后，注册在 Nacos 中的 MCP Server 和 MCP Tool 肯定会有很多。从业务领域来说，可能有与财务相关的 MCP Server、与销售相关的 MCP Server、与售后服务相关的 MCP Server等。在返回 MCP Server 和 MCP Tool 信息时，不可能将所有信息都返回，只能返回 Client 身份有权使用的 MCP Server 信息。

云原生 API 网关作为 MCP 网关，通过成熟的插件机制提供了 HTTP Basic Auth、OAuth2.0、JWT、API Key、外部认证等多种认证方式，以及基于消费者认证功能，让用户可以灵活地管理和控制 Client 的身份认证和 MCP Server/MCP Tool 的使用权限。

6. MCP Server 和 MCP Tool 的数据权限

当 MCP Server 是数据类服务时，权限会下探到库级别、表级别。在这种场景下，云原生 API 网关作为 MCP 网关，可以通过插件机制改写或增加 Request Header 的值，结合治理将 Header 的值透传下去，然后在服务内部进一步做数据权限管控。

比如：通过这种方式可以实现如下图的数据库读写分离的场景。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67fc4b06837e6d746367ab94/5a2d3765-b1e1-4bc8-9c25-37d4addb8d80.png)

3.1.3、如何快速构建 MCP Server

在 AI 应用中，涉及 LLM 推理的场景通常调用频率较低，属于稀疏调用场景。由于 MCP 范式强依赖 LLM 推理，无论是基于 HTTP API 的传统 AI 应用开发架构，还是基于 MCP 的新架构，目前都主要应用于这些稀疏调用场景。这引发了两个关键问题：

- **在稀疏调用场景下，如何优化运行 MCP Server 的计算资源利用率，实现成本最优？****在新的业务中，如何快速构建 MCP Server？**


在所有计算产品中，函数计算（FC）这种 Serverless FaaS 类型的计算产品，在资源粒度、弹性策略、弹性效率方面最适合稀疏调用场景。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67fc4b06837e6d746367ab94/9750e044-0054-421a-bc1b-062e4f9af1fc.png)

第一、函数计算（FC）支持 MCP 运行环境

### 阿里云函数计算（FC）目前支持 Python 和 NodeJS 两种语言的 MCP 运行环境（其他语言的 MCP 运行环境也将很快支持）。用户选择 MCP 运行环境创建函数后，只需编写 MCP Tool 的业务逻辑，无需考虑如何使用 MCP SDK。此外，云原生 API 网关与函数计算（FC）深度集成，天然适配 AI 应用开发的新范式。

### 第二、MCP Server 的弹性效率

基于函数计算（FC）构建的 MCP Server 在弹性效率方面有显著优势，主要体现在两个维度：

#### 1、资源规格细粒度管控

函数计算（FC）提供从 0.05C 128MB 到 16C 32GB 的多种实例规格，用户可以根据不同 MCP Server 承载的业务灵活选择合适的资源规格。在 AI 应用中，尤其是流程式构建的模式中，大多数 AI Agent 的职责单一，计算逻辑简单，因此可以用较小资源规格的函数承载。较小的资源规格在资源调度和弹性效率方面具有天然优势。

#### 2、完全按请求弹性

函数计算（FC）的弹性机制完全基于请求，根据 QPS 自动拉起对应数量的实例，且实例可以复用。当 QPS 下降时，空闲实例会自动释放，整个过程无需用户介入。此外，用户还可以设置按时间定时弹性或按指标阈值弹性策略，进一步满足复杂多变的业务场景，实现资源成本最优。

### 第三、MCP Server 的可观测性

函数计算（FC）具备完善的可观测体系，这意味着基于函数计算（FC）构建的 MCP Server 同样具备指标、链路、日志三个维度的可观测能力。通过这套可观测体系，用户可以清晰地了解每个 MCP Server 的各类运行状态，从而更好地管理和优化 MCP Server 的性能和成本。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67fc4b06837e6d746367ab94/a9b4b90c-b384-4dde-9bb2-79df82273917.png)

通过函数计算（FC）的这些特性，企业可以高效地构建和管理 MCP Server，优化资源利用率，降低成本，同时快速响应业务需求，提升 AI 应用的开发和部署效率。

3.1.4、AI 应用可观测体系

结合阿里云可观测产品 ARMS 和链路追踪 OpenTelemetry，我们构建了覆盖 AI 应用全环节的可观测体系。这一体系的构建主要围绕两个核心部分展开：数据采集和数据串联与分析。

### 第一、观测数据采集

数据采集的核心是覆盖足够广泛的范围，这主要体现在两个层面：

#### 1、编程语言和开发框架的支持

- **支持范围广**：支持 AI 应用开发的主流编程语言，比如：Python、Java、Go，并且相比社区规范提供更加精细化的埋点和属性。
- **框架支持**：支持常见的 AI 框架和模型，包括 Spring AI Alibaba、LLamaIndex、Langchain、通义千问2、OpenAI、PromptFlow 等。


#### 2、云产品数据上报

- **标准统一**：AI 应用架构新范式中涉及的云产品需要以相同的标准上报数据。
- **网关支持**：云原生 API 网关支持 OpenTelemetry 协议，网关自身和插件都会基于 OpenTelemetry 上报观测数据。
- **深度集成**：函数计算 FC 和 Serverless 应用引擎 SAE 均与应用监控 ARMS 以及链路追踪 OpenTelemetry 产品深度集成。


通过以上措施，我们实现了数据采集的全覆盖，确保了可观测体系的完整性。

### 第二、数据串联与分析

在应用监控 ARMS 中，专门构建了 LLM 应用监控模块，为 AI 应用场景提供了完善的可观测体系。这一模块从纵向和横向两个维度提供了丰富的监控指标和分析功能。

#### 1、纵向指标

- 在线 AI 应用数
- Trace 数
- Span 数
- 大模型数
- Token 使用情况
- 会话数
- 用户数
- 模型调用次数
- Token 消耗情况
- 模型调用耗时
- Token 消耗排行


#### 2、横向链路分析

- **Span 列表**：展示每个 Span 的详细信息。
- **Trace 列表**：提供完整的 Trace 记录。
- **散点图**：通过散点图分析性能分布。
- **全链路聚合**：对整个调用链进行聚合分析。
- **全链路拓扑**：展示调用链的拓扑结构。
- **错/慢 Trace 分析**：分析错误和慢 Trace 的原因。
- **调用链展示**：在调用链的每个环节展示输入、输出和 Token 消耗情况。


通过这些功能，用户可以清晰地了解 AI 应用的运行状态，快速定位问题，优化性能，确保 AI 应用的稳定运行。

***—4****—*

**AI 应用架构设计新范式对企业的影响**

随着企业级 AI 应用架构新范式的逐步成熟，企业的运营、产品、研发、运维团队之间的组织结构和协作关系，以及应用或系统的开发模式，都将迎来一系列变革。以下是我的一些畅想：

第一、MCP Server First 理念的兴起

API First 与前后端分离：API First 和前后端分离的概念在海外企业中得到了较好的实践，但在国内的应用相对较少。这可能是因为国内企业面临着较重的历史包袱，难以快速转型。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67fc4b06837e6d746367ab94/1366b6fb-2b08-466f-b420-42d37e3acddf.png)

Serverless 架构的实践：在 Serverless 计算领域，AWS Lambda、Azure Functions、Azure App Service、GCP CloudFunction 和 GCP CloudRun 等架构方案已被广泛研究和应用。然而，在国内，除了高德等少数企业通过函数计算重构系统实现了 API First 和前后端分离模式外，大多数企业仍处于探索阶段。

第二、AI 应用时代的变革

API 调用的本质：在 AI 应用时代，尽管本质上依然是对各种 API 的调用，但将 HTTP API 改为 REST API 的改造成本巨大。MCP 的出现为这一问题提供了新的解决方案，使得企业能够以0代码的方式快速转型到 AI 应用架构新范式。

MCP Server First 的可能性：MCP Server First 理念的提出，意味着企业可以将更多的精力放在构建和维护 MCP Server 上，而无需过多关注统一返回格式和开发语言的统一。

第三、团队角色的重新定义

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67fc4b06837e6d746367ab94/8d6e83e7-5728-4ef9-90b8-cbbf6d0d319a.png)

运维团队：负责云产品的维护（比如：云原生 API 网关、Nacos、Serverless 应用引擎、PAI 等产品的开通和升配），以及可观测体系的维护。运维团队还将与云厂商保持持续沟通，确保系统的稳定运行。

研发团队：专注于理解公司业务的原子化能力，负责构建 MCP Server 池。研发团队将更加专注于后端服务的开发和优化，而无需过多关注前端展示逻辑。

运营/市场/产品团队：通过低代码可视化方式构建业务流程（业务编排），用大白话描述业务需求，快速完成业务流程的搭建或 AI 应用的构建。这些团队将更加专注于业务逻辑的梳理和需求的快速实现。

第四、未来展望

企业级 MCP Server市场：未来，每个企业都可能拥有自己的 MCP Server 市场。在这个市场中，MCP Server 将被分门别类，每类 MCP Server 由专门的研发团队负责。这种模式将极大地提高开发效率，减少重复工作。

业务需求的快速实现：当运营、市场、产品等业务方有新的业务需求或产品功能需求时，可以通过统一界面快速构建 AI 应用。MCP 和 LLM 的结合将实现业务编排，推动“PRD 即产品”（PRD as a Product）的新开发模式。

第五、总结

企业级 AI 应用架构新范式的出现，不仅为企业的技术转型提供了新的思路，也为团队协作和开发模式带来了新的变革。通过 MCP Server First 理念的实践，企业可以更加高效地构建和维护 AI 应用，提升整体运营效率。未来，随着技术的不断发展和成熟，企业级 AI 应用架构将更加灵活、高效和智能。

PS：

【全新推出】为了帮助大家更好的掌握 AI 大模型适合的应用落地场景、应用开发技能，推荐大家加入《3天大模型应用开发项目实战直播训练营》，通过3天直播，带你快速掌握** Agent、RAG、Fine-tuning 微调、MCP、Prompt ** 等技能，让大家快速掌握企业级 AI 大模型应用实战能力。此训练营刚上新，**原价199元**，为了回馈粉丝的支持，早鸟价**19元**，点击以下报名。

***—5****—*

**3天大模型应用开发项目实战直播课**

3天的直播课，带你快速掌握** Agent、RAG、Fine-tuning 微调、MCP、Prompt ** 等 AI 大模型应用开发核心技术和企业级项目实践经验。

**直播模块一：Agent 智能体开发实战篇**

1. Agent 智能体技术原理深度解读
2. Agent 规划能力深度剖析与实践 
3. Agent 行动能力深度剖析与实现
4. Agent 工具调用之 MCP 深度剖析 
5. Agent 智能体 ReAct 机制深度解读 
6. 从0到1,手搓代码实现企业级智能客服


**直播模块二：RAG 知识库 & Fine-tuning 微调篇**

1. RAG 知识库核心技术解读 
2. RAG 知识库知识切分剖析与实践 
3. RAG 知识库两阶段检索剖析与实践 
4. RAG 知识库项目全流程深度实践
5. LoRA 微调技术原理剖析 
6. RAG 和 Fine-tuning 微调技术选型


**直播模块三：综合案例实战：Agent + RAG + Fine-tuning 微调 + MCP + Prompt 案例实战篇**

1. Agentic RAG 项目需求分析
2. Agentic RAG 架构设计--知识库管理
3. Agentic RAG 架构设计--在线联网问答
4. Agentic RAG 架构设计--效果评估
5. Agentic RAG 架构设计--模型弹性扩容
6. Agentic RAG 核心代码实现


基于 Agent、RAG、Fine-tuning 微调、MCP、Prompt，从需求分析、架构设计、架构技术选型、硬件资料规划、核心代码落地、服务治理等全流程实践，深度学习企业级 AI 大模型应用落地项目全流程重点难点问题解决。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67fc4b06837e6d746367ab94/640d1bd1-1119-46ea-b0f9-4c920248736a.jpeg)

3天时间，**你能学会什么？**

在真实项目实践中，你会**获得4项硬核能力：**

**第一、全面掌握 **DeepSeek 大模型**、Agent、RAG、Fine-tuning 微调、MCP、Prompt 的原理、架构和实现方法，掌握核心技术精髓。**

**第二、熟练使用 AI 大模型应用开发**平台：LangChain、LangGraph、LlamaIndex、AutoGen、Spring AI Alibaba、Swarm 等主流开发框架，为企业级技术实践打下坚实基础。

**第三、通过企业级项目实战演练**，能够独立完成基于 Agent、RAG、Fine-tuning 微调、MCP、Prompt 的 AI 大模型应用的适用场景、设计开发和维护，真正学会解决企业级实际问题的能力。

**第四、为职业发展提供更多可能性**，无论是晋升加薪还是转行跳槽，提升核心技术竞争力。

#### 限时优惠：

【全新推出】，刚上线，原价199元，**回馈粉丝们支持**，早鸟价**19元**！赶快加入把~~

***—6****—*

**添加助教直播学习**

**购买后，一定记得添加助理，否则无法进行直播学习👇**

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67fc4b06837e6d746367ab94/b38ceead-eea5-41a8-a174-10b584558edb.webp)

参考来源：

https://mp.weixin.qq.com/s/r1wKHJDzUgWncZvNko2O2Q

**⬇戳”阅读原文“，立即报名！**

END


新枝标签： #llm #mcp
