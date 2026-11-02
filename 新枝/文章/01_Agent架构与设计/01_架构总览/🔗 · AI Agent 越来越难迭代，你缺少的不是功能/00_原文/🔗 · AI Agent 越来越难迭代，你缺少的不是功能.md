---
作者:
  - "阿里云云原生"
原文链接: https://mp.weixin.qq.com/s?__biz=MzUzNzYxNjAzMg==&amp;mid=2247582747&amp;idx=1&amp;sn=6cb8b19e1670ef371859dbc98bb8498a&amp;chksm=fb32bcc4180cbd088b6e2fde3686639a11afe7f3a7145f1b9576a6b43fb44440b8c66fd2e049&amp;mpshare=1&amp;scene=1&amp;srcid=0316QQJPSIrwWiMZFBIMUXEF&amp;sharer_shareinfo=498aed3c8a10c8bdd45933a4a5024f66&amp;sharer_shareinfo_first=498aed3c8a10c8bdd45933a4a5024f66#rd
发布时间: ""
收藏时间: "2026-03-16"
关联日记: "[[2026-03-16]]"
tags:
  - 文章
---
AI 应用做着做着就会走到一个尴尬阶段：功能看起来都在，但你越来越不敢动它。多 Agent、工具调用、RAG、记忆……链路一长，问题就变成：到底发生了什么？上下文什么时候变了？是哪一步导致耗时骤增？一次回答的成本究竟多少？更麻烦的是，很多信息藏在模型的黑盒里，你想调都不知道从哪下手。

LoongSuite Python 探针就是为解决这些问题而生的：不改一行业务代码，把可观测能力接进来，让你能把一次请求从头到尾捋顺：哪一步访问了什么模型、调用了什么工具、召回了哪些文档、花费了多少 token、上下文发生了什么变化等等，帮助你清晰地掌握 AI Agent 的真实运行情况，更加轻松地实现对 Agent 的分析、评估和优化。

**01**

***AI 应用可观测性：***

***三个绕不开的难题***

*Cloud Native*

传统微服务的可观测，关注的是性能和可用性；AI 应用不一样，核心是把“运行时的上下文和行为”变得可追踪、可复现、可分析。工程上最绕不过去的难题，有以下三点：

▍**1.1 数据回流怎么做，才不会变成负担**

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/69b745f407203f095b74cd7d/75a34bee-858f-441c-b6e8-fb168fa24190.png)

传统微服务中，代码逻辑是核心资产。AI 应用真正有价值的是运行时所产生的数据：对话、工具调用、检索结果、记忆读写，以及图片、音频、视频等多模态输入输出……这些运行时数据会成为你优化 Agent 及模型的重要参照，指引你 AI 应用的优化方向，让你的 Agent “越用越聪明”。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/69b745f407203f095b74cd7d/73304068-3721-4c2f-99fd-e566df9e0905.png)

这些运行时数据，要确保能完整采集，对应用运行无影响，还不能让链路变慢。存在以下难点：

- 上下文的管理是灵活的，它既有可能在框架内部发生变化，又有可能被业务逻辑管控——如何通过一套体系，轻量地捕获框架内与业务代码中的上下文变化？
- 当用户上传一张图片、一段语音时，这些大体积内容如果直接塞进链路，会拖慢整个系统——如何在不阻塞业务的前提下，把它们“剥离”出来、妥善存储？


▍**1.2 可观测数据语义不统一，等于白采集**

各类采集工具相当丰富，如 OpenTelemetry、OpenInference、Langfuse，一些成熟的框架本身也可以产生一些可观测数据，如 AgentScope、LangChain（LangSmith）等。这些可观测数据的命名、属性（标签）及其含义各不相同，我们一般称其为“数据语义”。数据采集到了，但如果各数据源各说各话，彼此语义不一致，就会出现：

- 底层存储难复用：各类可观测存储介质支持的数据协议不同，用其他工具采集上来的数据可能无法被正确接受、处理和存储；
- 消费逻辑难复用：即便数据满足同一类数据协议（如 OTLP），数据的语义也可能各不相同，同类指标可能在不同的采集工具中叫不同的名字，也可能有不同的标签，某些采集工具所采集的数据可能并不能被其他可观测平台正常展示和处理。


这些限制会导致可观测数据的选择相当受限——为了使用某个可观测服务的功能，开发者不得不使用它提供的配套的数据采集工具。而如果这个采集工具不支持我正在使用的框架，问题则更为棘手。开发者就只能去学习这个可观测服务的语义规范，然后手动编写代码以创建对应的可观测数据。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/69b745f407203f095b74cd7d/0d767719-e833-4ff6-9ab1-027b0a0dbf02.png)

为了抹平各类采集组件语义的差异，数十家头部云厂商、AI 厂商、可观测厂商共同组织了 OpenTelemetry GenAI SIG**[1]**，讨论并整理出了一套 AI 应用系统通用的可观测语义规范**[2]**。这套规范明确了 GenAI 场景下各类关键调用需要采集哪些信息、叫什么名字、以什么样的形式采集。

Langfuse、Arize 等众多 AI 领域常见的可观测平台都纷纷支持了这一语义规范，它很好地解耦了可观测后端与采集工具之间的绑定关系。一旦采集的数据遵守 GenAI 的语义规范，后续的可视化、消费、迭代都会轻松很多。

然而要正确理解并实现 OpenTelemetry GenAI 语义规范，成本和难度都不低，急需一些手段来简化这个流程。

▍**1.3 端到端全链路：只看到进程内，会误判问题**

实际生产中，多 Agent 和工具服务往往跨进程、跨服务。如果只观测“进程内”的 LLM 调用，很多问题看不出来：链路关联不上、耗时归因不清、请求到哪里也说不明白。端到端串起来，才有排查和优化的基础。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/69b745f407203f095b74cd7d/47c74715-6b69-4063-83e3-2bc9adb50101.png)

要让整条链路完整串联起来，单一的框架原生的可观测性不再能够满足需求，对 MCP、A2A、httpx、flask 等涉及跨进程通信的组件的观测支持变得不可或缺。

**02**

***解决方案：LoongSuite Python 探针***

*Cloud Native*

针对上述三个难题，LoongSuite Python 探针提供了一套开箱即用的方案。

LoongSuite Python 探针是 OpenTelemetry Python 探针的阿里云开源发行版，致力于让 AI 应用的可观测性更敏捷、更高效——既承接上游标准，又沉淀商业化实践，并持续将新特性贡献回社区。

▍**2.1 它是怎么工作的？**

基于 OpenTelemetry 标准，LoongSuite 探针通过自动插桩的方式，无侵入地采集 AI 应用运行时的可观测数据。你不需要改业务代码，只需在启动命令前加一层“包装”：

1. 自动发现：根据你环境中已安装的库（DashScope、LangChain、Flask 等），自动加载对应的插桩；

2. 统一语义：各种数据遵循 OpenTelemetry GenAI 语义约定，下游可视化、消费无需重复适配；

3. 多维度覆盖：既追踪 AI 调用（LLM、Agent、Tool、RAG、Memory），也追踪微服务调用（HTTP、gRPC、数据库等）——这是实现全链路可观测的基石；

4. 灵活导出：通过 OTLP 协议导出到 Jaeger、Langfuse、阿里云可观测等任意兼容 OTLP 协议的后端。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/69b745f407203f095b74cd7d/5720d154-30d4-4726-b63d-78f228405e31.png)

▍**2.2 快速上手：三步启动**

Step 1：从 PyPI 安装 LoongSuite Distro

```
pip install loongsuite-distro
```

Step 2：安装探针包本体

```
loongsuite-bootstrap -a install --version 0.1.0
```

注：该命令会将所有的 AI 相关的 instrumentation 全部安装到环境中，你也可以通过添加 --auto-detectflag 来按需安装，或使用 --whitelist精确控制需要安装的 instrumentation。

Step 3：引导启动 AI 应用

```
# 请将 OTLP endpoint 指向你的 OTLP 服务地址，默认是 gRPC 协议
OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317 \
# 开启对大模型调用输入输出的统计
OTEL_SEMCONV_STABILITY_OPT_IN=gen_ai_latest_experimental \
OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT=SPAN_ONLY \
loongsuite-instrument python app.py
```

通过以上三步，你已经为你的 AI 应用引入了可观测的能力！

效果展示

使用后，你可以在 Jaeger/Langfuse/阿里云可观测等任何一个支持 OTLP 协议的平台查看：

- 完整的调用链：各类大模型调用与常规微服务调用，一目了然；
- 详细的性能指标：每个调用过程的耗时、错误；
- 真实的上下文记录：采集关键调用的上下文，方便后续评估和其他数据消费。


![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/69b745f407203f095b74cd7d/e4265783-f18e-4b05-b257-97baf83f5d3c.png)

**03**

***LoongSuite 与 OpenTelemetry：***

***一句话说清楚***

*Cloud Native*

LoongSuite Python 探针是 OpenTelemetry Python Contrib 的 Fork，在保持与上游兼容的前提下，扩展了对 GenAI 框架的可观测性支持，并更敏捷地响应国内生态需求。

▍**3.1 为什么需要独立发布？**

- OTel 上游支持的框架矩阵与国内生态契合度不高
- 支持 DashScope、AgentScope、Dify、MCP、Mem0 等国内常用框架与组件
- OTel 上游 opentelemetry-util-genai 开发进展缓慢，支持能力有限
- 我们需要扩展多模态上传、更多 Span 类型、更新的语义规范
- 阿里云商业化用户沉淀大量使用经验，亟需回馈至开源社区
- ReAct 轮次维度的展示与评估Session 维度分析与 Trace 自动关联


通过独立发布的机制，使用者可以使用 loongsuite-distro 封装的命令。我们会定期同步上游代码，并及时将下游新特性贡献回 OpenTelemetry 社区，与上游社区保持良好的协同工作关系。

▍**3.2 模块与发布策略**

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/69b745f407203f095b74cd7d/5d2d06f3-6429-4c95-83a9-a7cee24abbbb.png)

**04**

***LoongSuite GenAI Util：***

***OTel GenAI Util 的“增强版”***

*Cloud Native*

在实际的 AI Agent 搭建中，许多开发者并不会完全使用 LangChain、AgentScope 等框架预先包装好的成熟能力，而是会根据业务或架构需求，对过程有一些自定义，例如使用 RESTful API 访问自部署的 LLM/网关，自主实现 ReAct 迭代过程，甚至整个 Agent 都直接用代码“手搓”，来让上下文管理变得更加灵活、高效。

这些自定义的关键过程并不能自动被 LoongSuite Python 探针识别和自动插桩，需要开发者通过手动埋点来保证其可观测性。这些手动埋点往往需要考虑以下问题：

- 与其他 Span 的父子关系是否正常
- 产生的可观测数据是否符合 GenAI 语义规范
- 错误、异常是否正确捕获
- 记录指标、创建日志
- 采用统一开关控制是否记录输入输出海量数据
- 多模态数据分离上报
- ……


为了简化这个过程，保证这些手动埋点产生的数据和自动插桩产生的内容一样完整准确，OTel GenAI SIG 推出了 OpenTelemetry GenAI Util**[4]**，帮助开发者更加轻松地完成手动埋点——你要做的所有事情就是构建一个 Invocation 对象，然后选词填空，所有后续的工作由 Util 自动完成。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/69b745f407203f095b74cd7d/12b8bb13-49d3-4f7f-ae5e-719a844950aa.png)

然而，OpenTelemetry GenAI Util 发展速度相对较慢，有许多 feature 都还在计划阶段，生产尚不可用。于是我们在上游项目的基础上开发并发布了 LoongSuite GenAI Util**[5]**，协助开发者更快地、更方便地将 Util 用于复杂的生产环境。

▍**4.1 支持的操作类型**

LoongSuite GenAI Util（loongsuite-util-genai）是一个独立发布的 PyPI 包，可单独安装使用。它基于 OpenTelemetry GenAI Util 扩展，在 Span 类型覆盖、多模态处理、语义规范等方面走得更远。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/69b745f407203f095b74cd7d/e8d2c337-0cff-4ef2-bd59-80cece027e68.png)

▍**4.2 多模态数据分离上报：大文件不再“拖累”链路**

图片、音频、视频等多模态内容体积大，如果直接塞进 span/event，会拖慢链路、增加存储压力。LoongSuite GenAI Util 提供「多模态剥离上传」：把大体积内容异步上传到 OSS/SLS/本地，在消息中只保留可引用的 URI。

1. PreUploader：识别 Base64/Blob/Uri，生成上传任务，将消息中的多模态 part 替换为 URI；

2. Uploader：异步入队上传，不阻塞业务线程，支持幂等（相同内容不重复上传）；

3. 存储协议：支持 file://、oss://、sls:// 等，可对接阿里云 OSS、SLS。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/69b745f407203f095b74cd7d/947ea889-7b17-4e99-a00e-bfd42656df7f.png)

▍**4.3 快速实践：使用 LoongSuite GenAI Util**

安装：

```
pip install loongsuite-util-genai
# 如需多模态上传能力
pip install loongsuite-util-genai[multimodal_upload]
```

环境变量配置示例：

```
export OTEL_SEMCONV_STABILITY_OPT_IN=gen_ai_latest_experimental
export OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT=SPAN_AND_EVENT
export OTEL_INSTRUMENTATION_GENAI_EMIT_EVENT=true
# 多模态上传（可选）
export OTEL_INSTRUMENTATION_GENAI_MULTIMODAL_UPLOAD_MODE=both
export OTEL_INSTRUMENTATION_GENAI_MULTIMODAL_STORAGE_BASE_PATH=file:///var/log/genai/multimodal
```

业务代码中手动使用 ExtendedTelemetryHandler，捕获特定类型的操作：

```
from opentelemetry.util.genai.extended_handler import get_extended_telemetry_handler
from opentelemetry.util.genai.extended_types import InvokeAgentInvocation
from opentelemetry.util.genai.types import InputMessage, OutputMessage, Text
# 以下三行用于初始化环境变量读取流程，如果你使用了 2.2 节中的方式启动 Python 应用，则不需要这一步
from opentelemetry.instrumentation._semconv import _OpenTelemetrySemanticConventionStability
if not _OpenTelemetrySemanticConventionStability._initialized:
    _OpenTelemetrySemanticConventionStability._initialize()
# 1. 获取 telemetry handler，该 handler 可以单例化
handler = get_extended_telemetry_handler()
# 2. 构造 InvokeAgent Invocation，填写相关信息
invocation = InvokeAgentInvocation(
    provider="dashscope",
    request_model=request["model"],
    agent_name="OrderAgent",
    input_messages=[
        InputMessage(role="user", parts=[Text(content="帮我查询单号为 101 的订单状态")]),
        InputMessage(role="system", parts=[Text(content="你是一个订单管理员，负责调用工具查询订单信息")]),
    ]
)
with handler.invoke_agent(invocation) as invocation:
    # 3. 执行 InvokeAgent
    # ... Invoke Agent ...
    # 4. 补充 InvokeAgent 结果信息
    invocation.output_messages = [
        OutputMessage(role="assistant", parts=[Text(content="好的，我来帮您查询……您的订单信息暂未找到，请确认您的单号是否正确。")], finish_reason="stop")
    ]
    invocation.input_tokens = 15
    invocation.output_tokens = 20
```

**05**

***Release Note***

*Cloud Native*

要查看完整的 Release Note，请参见：https://github.com/alibaba/loongsuite-python-agent/releases

1. 发行版与生态

a. loongsuite-distro 正式发布：提供loongsuite-bootstrap 和 loongsuite-instrument 命令，支持一键安装与运行；

b. 更贴近国内生态的插件矩阵：自研 instrumentation-loongsuite 支持 DashScope、AgentScope、Dify、MCP、Mem0、LangChain、Google ADK、Claude Agent SDK、Agno 等。

2. LoongSuite GenAI Util

a. 多模态分离上传：支持将 Base64Blob/Blob/Uri 自动上传到 OSS/SLS/本地，消息中保留 URI 引用，默认异步上传；

b. 更多 Span 类型：invoke_agent、create_agent、execute_tool、retrieve、rerank、embedding、memory；

c. 增强语义属性：gen_ai.usage.total_tokens、gen_ai.response.time_to_first_token；

d. Data URI 与本地路径支持：多模态预上传管道增强，支持 Data URI 和本地文件路径；

e. 可配置 Hook：支持 PreUploader/Uploader 的 entry point 扩展。

**06**

***写在最后***

*Cloud Native*

本次 LoongSuite Python 探针发布只是一个开始，我们的目标很清晰：

1. 更敏捷：快速响应国内 AI 生态需求，持续扩展插件矩阵；

2. 更高效：通过 LoongSuite GenAI Util 提供更完善的多模态处理、更多 Span/Metric 类型、更新的语义规范；

3. 端到端：AI 调用与微服务调用统一追踪，让多 Agent 全链路可观测成为可能；

4. 与上游协同：定期同步上游，并将下游实践贡献回 OpenTelemetry 社区。

如果你正在构建 AI 应用、关心可观测性，欢迎试用、反馈与贡献：LoongSuite Python 探针**[3]**。

如果本项目对你有帮助，欢迎给我们的 github 项目点一个 star，也欢迎加入我们的开发者社区，一起构建 AI 时代最好用的可观测采集组件！

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/69b745f407203f095b74cd7d/15ee7b74-20a5-4bae-a38f-f9dd08f15957.png)

## 参考资料：

[1] OpenTelemetry GenAI SIG

https://docs.google.com/document/d/1EKIeDgBGXQPGehUigIRLwAUpRGa7-1kXB736EaYuJ2M

[2] OpenTelemetry GenAI Semantic Convention：

https://opentelemetry.io/docs/specs/semconv/gen-ai/

[3] LoongSuite Python 探针

https://github.com/alibaba/loongsuite-python-agent

[4] OpenTelemetry GenAI Util

https://github.com/open-telemetry/opentelemetry-python-contrib/tree/main/util/opentelemetry-util-genai

[5] LoongSuite GenAI Util

https://github.com/alibaba/loongsuite-python-agent/blob/main/util/opentelemetry-util-genai/README-loongsuite.rst

