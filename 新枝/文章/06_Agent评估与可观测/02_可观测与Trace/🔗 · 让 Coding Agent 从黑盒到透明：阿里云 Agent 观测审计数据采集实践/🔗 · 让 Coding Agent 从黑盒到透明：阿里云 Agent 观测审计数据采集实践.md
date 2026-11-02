---
作者:
  - "阿里云云原生"
原文链接: https://mp.weixin.qq.com/s?__biz=MzUzNzYxNjAzMg==&amp;mid=2247584211&amp;idx=1&amp;sn=8c23d35c0f023ddce1531a4893dde754&amp;chksm=fbb8e8521590234d96f4041777a01282fff6f0622dcfd45a99e6a4e589b997e466539e401b87&amp;mpshare=1&amp;scene=1&amp;srcid=0602aGsd3X6SmfAbytwSBTei&amp;sharer_shareinfo=10f95921728815a9ee91cbdf8acba109&amp;sharer_shareinfo_first=10f95921728815a9ee91cbdf8acba109#rd
发布时间: ""
收藏时间: "2026-06-02"
关联日记: "[[2026-06-02]]"
tags:
  - 文章
---
**01**

***引言***

*Cloud Native*

2025 年，AI Agent 从实验室走向规模化生产落地。从开发者日常使用的代码助手到企业服务场景下的智能客服，到复杂度持续升级的多智能体协同系统，AI Agent 正在以前所未有的速度重塑软件开发方式和业务运转流程。

然而，当 Agent 真正跑起来之后，一个尖锐的问题浮出水面：AI Agent 的实际运行行为难以感知、追溯与管控。

代码类 Agent 深夜擅自修改核心配置文件，变更内容、修改动因无从知晓；智能客服 Agent 自主下达“取消订单”指令，决策逻辑、工具调用链路、Token 资源消耗无法复盘；多智能体协同任务中途失败，故障节点与根因难以定位。

这些问题指向一个共同的诉求：AI Agent 需要完备的可观测能力。而且，这种可观测性不能仅停留在“请求成功/失败”的浅层统计维度，必须深入覆盖 LLM 调用、工具执行、多轮推理、记忆检索等 AI Agent 特有的运行环节中去。

阿里云基于 OpenTelemetry (OTel) 社区标准，结合自身在可观测领域的深度实践，打造了一套覆盖三大类 Agent 形态的完整数据采集方案，并在 OTel GenAI 语义规范基础上推出了 LoongSuite GenAI 可观测语义规范。本文将系统介绍这套方案的设计理念、技术实现和使用方法。

**02**

***Agent 形态分类与可观测挑战***

*Cloud Native*

当前 AI Agent 市场百花齐放，不同类型 Agent 的运行模式、部署环境、使用场景差异显著，对应的观测、审计需求也各有侧重。我们将市面上主流 AI Agent 划分为三大类别：

### ▍2.1 三大 Agent 形态

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6a1eb568eb5f77400650c57f/ccb533c1-6833-4dd2-857c-8662caeebe67.png)

### ▍2.2 三大核心挑战

无论采用何种形态，AI Agent 在规模化使用后，均会遭遇三大共性难题：

- 执行过程黑盒化。Agent 的执行过程涉及 LLM 调用、工具执行、多轮推理、记忆检索等环节，传统的 Metrics + Log + Trace 三板斧无法有效刻画这一新型计算范式。例如一轮包含 10 次 ReAct 推理的 Agent 任务，传统方案仅能识别出 10 条独立 HTTP 请求，无法还原分层、有序的完整决策流程。
- 行为轨迹难追溯。Agent 具备较高的自主操作权限，可读写本地文件、执行系统命令、调用第三方 API。在缺少专项审计能力的前提下，无法完整追溯 Agent 的全部操作行为，在企业安全、合规管控场景中存在极大风险。
- 成本难度量。大模型 Token 消耗是 Agent 的主要成本来源，多轮迭代和工具调用会指数级放大消耗。若缺少按 Agent、用户、任务维度的精细化成本拆分能力，企业将无法开展预算管控与投入产出评估。


**03**

***差异化采集方案：***

***适配 Agent 原生运行形态***

*Cloud Native*

核心设计原则：让数据采集能力适配 AI Agent 原生运行模式，而非强制 Agent 改造适配采集工具。

### ▍3.1 Coding Agent：LoongSuite Pilot 端侧轻量数据采集平台

Coding Agent 运行在开发者本地设备，所有代码编辑、文件新建、终端命令执行等核心行为均发生在本地环境，传统服务端探针完全无法感知，为此我们推出 LoongSuite Pilot 端侧数据采集平台，专门适配代码类 Agent。

#### 核心优势

- 一次部署，全域覆盖。Pilot 不是针对某一个 Agent 的专属方案，而是一个统一平台。目前已支持 Claude Code、Codex、Cursor、Qoder、QoderWork 五大主流 Coding Agent。开发者仅需完成一次安装，即可自动对所有已使用的代码助手完成数据采集，无需重复配置。
- 后台静默运行，零使用干扰。Pilot 以本地守护进程形式常驻后台，自动识别设备内已安装的 Coding Agent 并完成能力部署。全程无需开发者修改 Agent 配置、改变使用习惯，在无感状态下完整记录大模型调用、工具执行、代码修改等全量行为。
- 断点续采，数据稳定可靠。针对本地设备网络波动、设备重启、终端关闭等不稳定场景，内置断点续采机制。进程异常中断重启后，不会出现数据重复、数据丢失问题，保障采集数据完整性。
- 采集粒度灵活，兼顾观测与数据安全。不同团队对数据安全的要求不同。Pilot 支持按 Agent 类型灵活配置采集粒度：需要完整审计时，可采集消息内容、工具参数等详细信息；在数据敏感场景下，可仅上报元数据（模型名、Token 消耗、耗时等），在观测需求与数据安全之间取得精准平衡。
- 插件化架构，快速兼容新 Agent。Pilot 采用插件化架构，针对不同 Agent 的数据形态（Hook 日志、IDE 快照、SQLite 数据库、会话文件等）预置了开箱即用的采集基类。接入全新 Coding Agent 仅需实现 2-3 个抽象方法，可快速跟进生态迭代。


#### 已支持的 Coding Agent 及覆盖能力

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6a1eb568eb5f77400650c57f/be1f8978-f9a0-464d-93ac-7f49f9e7142c.png)

### ▍3.2 个人通用助理：一行命令接入完整观测和审计

个人通用助理通常以独立服务的形式运行，面向终端用户提供对话和任务执行能力。针对这类 Agent，我们提供了专用插件，实现一行命令即可接入完整链路追踪。

#### 设计理念

以 OpenClaw 为例，其内置的 diagnostics-otel 扩展虽然能输出 Metrics 和部分 Trace，但采用的是事件驱动架构，每个事件独立创建 Span，彼此之间没有父子关系和 Trace Context 传播，本质上是一组“独立打点”。而 LoongSuite 的 openclaw插件从设计上就是完整的链路追踪——所有 Span 共享同一个 traceId，通过显式的父子关系串联成一棵调用树。

#### Span 语义模型

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6a1eb568eb5f77400650c57f/7ca5aca4-fae9-424b-8f20-2bd23a0d4373.png)

各类 Span 通过父子关系串联为完整 Trace 调用树，运维人员可直观查看单条请求的大模型调用次数、Token 消耗、工具调用清单、耗时节点与故障信息。

#### 与内置观测的本质差异

LoongSuite 的插件相比 OpenClaw 内置的观测能力，核心差异体现在两个维度：

链路完整性。内置观测通常是扁平化独立打点，事件之间缺乏关联；而我们的插件基于 OTel Context 传播机制，确保 ENTRY → AGENT → STEP → LLM / TOOL 形成完整的调用树，能够还原一次请求的全貌。

数据丰富度。内置观测往往只记录模型用量等基础指标；而我们的插件完整记录 gen_ai.input.messages、gen_ai.output.messages、gen_ai.system.instructions、gen_ai.tool.call.arguments、gen_ai.tool.call.result 等字段，满足深度审计和故障排查的需求。

同样的插件机制已覆盖 Hermes Agent、QwenPaw 等个人通用助理。

### ▍3.3 高低代码框架Agent：LoongSuite Python Agent 零代码探针插桩

针对 LangChain、AgentScope、Dify 等框架开发的 Agent 应用，其运行方式与传统 Python 应用一致。我们提供 LoongSuite Python Agent（基于 OpenTelemetry Python Contrib 深度定制），通过一行命令实现零代码自动插桩。

#### 快速开始

```
# 1. 安装 LoongSuite Python Agent
pip install loongsuite-distro
# 2. 自动检测并安装所需的插桩库
loongsuite-bootstrap
# 3. 一行命令启动，自动注入探针
loongsuite-instrument \
  --traces_exporter otlp \
  --service_name my-agent-app \
  python my_agent_app.py
```

loongsuite-bootstrap会自动扫描当前环境中已安装的框架（如 langchain、dashscope、mcp 等），并安装对应的插桩包——开发者无需手动挑选和安装。

#### 框架覆盖

目前 LoongSuite Python Agent 已覆盖 17 个插桩库，涵盖主流 AI Agent 开发框架：

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6a1eb568eb5f77400650c57f/7041794e-1d1f-4c2b-b22b-ec0d61b0e51f.png)

#### 自动识别的 Span 类型

#### 探针会自动识别并生成多种 GenAI Span 类型，覆盖 Agent 全生命周期：

- ENTRY：请求入口。
- AGENT：Agent 执行单元。
- STEP：ReAct 推理-行动迭代步骤。
- LLM：大模型调用，含请求参数、Token 消耗、输入输出消息。
- TOOL：工具调用，含工具名、参数、结果。
- MCP：MCP 协议调用。
- CHAIN：链式调用编排。
- RETRIEVER：检索操作。
- EMBEDDING：向量化操作。
- RERANKER：重排序操作。
- WORKFLOW：工作流编排。


**04**

***观测与审计效果***

*Cloud Native*

接入上述采集能力后，用户可以获得以下维度的可观测视图。以 Claude Code 为例，如果要接入 Agent 可观测，只需要登录云监控 2.0 控制台**[1]**，在接入中心点击对应的卡片，按照步骤操作，一行命令即可完成安装和接入。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6a1eb568eb5f77400650c57f/fe22aba2-6ad3-40bc-b0af-dfa501ef6274.png)

### ▍4.1 全链路调用链视图

Agent 的完整执行过程以 Trace 树形式呈现，从用户请求入口（ENTRY）到 Agent 决策（AGENT）、推理步骤（STEP）、LLM 调用（LLM）、工具执行（TOOL），层级关系一目了然。对于多轮 ReAct 的复杂任务，可以通过 Step Span 快速定位到哪一轮迭代出现问题，再深入到该轮内的 LLM 或 Tool Span 分析根因。

排查范式：当 Agent 执行包含 10 轮 ReAct 过程时，先通过 Step Span 定位是哪一轮出现问题，然后再深入分析该轮中具体是哪一步出错——这种 Top-down 的排查方式，大幅提升了复杂 Agent 的故障定位效率。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6a1eb568eb5f77400650c57f/3291cb99-1108-4711-821b-3f289ed077b4.png)

### ▍4.2 Token 消耗与成本追踪

基于 gen_ai.usage.input_tokens、gen_ai.usage.output_tokens、gen_ai.usage.total_tokens 以及阿里云扩展的成本字段（input_cost、output_cost、total_cost），实现：

- 单次请求的 Token 消耗明细。
- 按 Agent / 按用户 / 按时间的成本聚合。
- 缓存 Token 字段（cache_read.input_tokens、cache_creation.input_tokens）评估缓存策略有效性。


![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6a1eb568eb5f77400650c57f/a293fc16-fe93-445e-bf12-a8ed6bb58237.png)

### ▍4.3 会话与多轮对话追踪

通过gen_ai.session.id、gen_ai.turn.id、gen_ai.step.id 构建三级标识体系，实现：

- 跨多轮对话的完整会话追溯。
- 单轮对话内的 Step 级细粒度分析。
- 会话路径分析和用户行为洞察。


![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6a1eb568eb5f77400650c57f/badd3963-f940-4717-a810-b511d8e9b570.png)

### ▍4.4 工具调用审计

完整记录 Agent 调用了哪些工具、传入什么参数、返回什么结果、耗时多久。对于 Coding Agent，这意味着每一次文件读写、每一次命令执行都有据可查。对于 MCP 协议调用，同样提供完整的请求-响应审计。

#### 行为分析大盘

顶部计数卡片将工具调用按行为类型拆解为命令执行、文件读写、搜索、网页浏览、MCP 调用等维度，并以醒目的红色/橙色标注调用量异常偏高的类别，提供整体行为构成的快速快照。右侧同时展示活跃会话数和用户数，便于关联行为热度与使用规模。下方会话统计表以 Session 为粒度展开，记录每个会话在各行为维度上的调用量，支持定位高频操作集中在哪些会话和用户。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6a1eb568eb5f77400650c57f/33182cfd-8caa-4748-82a3-a14e19404e6c.png)

#### 工具调用分布

工具调用分布页从两个视角呈现工具使用结构。左侧饼图展示所有工具调用的类型占比（如 Read、Write、Bash、TodoWrite 等），帮助团队了解 Agent 最依赖哪些工具能力；右侧饼图独立展示 MCP 工具调用的分布，揭示跨系统集成中哪些外部能力被频繁调用。下方趋势对比图以时间轴展开各工具类型的调用量变化，便于识别调用模式的阶段性异动——例如某一天 Bash 调用骤增可能意味着批量脚本任务或异常行为。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6a1eb568eb5f77400650c57f/b6c39eae-f2de-4f96-948f-a55c6d4f6b78.png)

#### 安全审计总览

总览页以指定时间窗口内的多维高危操作计数为核心，将 AI Agent 的安全态势压缩为一屏可读的风险快照。左侧发现问题漏斗从全量会话逐级收敛到存在安全风险的会话，直观展示风险面占比。右侧高危命令执行、网页请求外发、命令行外发、敏感文件访问、提示词注入等指标并列呈现，配合环比数据，帮助安全团队在无需深入明细的情况下快速判断当前风险水位是否异常。

尤为值得关注的是提示词注入事件后的高危操作计数。普通高危操作可能源于任务本身的合理需求，而注入后触发的高危行为则是强烈的威胁信号——这意味着注入的恶意指令已驱动 Agent 付诸执行。即便存在误判，此类信号也应触发最高级别的人工复核，而非等待进一步确认。因此，“注入后工具调用的会话数”是整个总览中威胁置信度最高的信号，3 个此类会话的优先级往往高于数百次普通高危命令。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6a1eb568eb5f77400650c57f/15b7b442-1b07-411b-b9dd-0e037843e1a9.png)

#### 高风险会话追溯

下方提供两级下钻能力。上层为高危会话风险评分表，以 Session 为单位聚合各维度风险计数（注入命中数、高危操作数、敏感文件访问数、外发信息数等），通过综合风险评分自动排序，将最需要人工介入的会话置顶呈现。安全团队无需逐条筛查日志，直接从风险最高的 Session 开始溯源，大幅压缩从发现到响应的时间窗口。

下层为高危事件汇总表，将风险钻取到单条事件粒度——具体的时间、用户、会话、事件类型、涉及工具名称、威胁类型以及完整的上下文内容，为安全分析师提供最终定性所需的原始证据。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6a1eb568eb5f77400650c57f/ae6bba8a-bbff-43a7-b748-0d803f523e92.png)

**05**

***基于 OTel GenAI 语义规范的深度扩展***

*Cloud Native*

阿里云 AI Agent 可观测体系的数据能力，依托自研 LoongSuite GenAI 可观测语义规范构建。该规范在社区 OTel GenAI 规范标准基础上，补齐真实业务场景的语义空白。

### ▍5.1 为什么需要在社区标准之上扩展

OpenTelemetry 早在 2024 年初就开始推动 GenAI 语义规范建设，目标是建立统一的可观测数据语言。社区标准已经奠定了重要基础：

- gen_ai.operation.name：标准化操作类型（chat、embeddings、execute_tool 等）。
- gen_ai.span.kind：区分 LLM、CHAIN、AGENT、TOOL、RETRIEVER 等 Span 类型。
- gen_ai.request.model/ gen_ai.response.model：模型标识。
- gen_ai.usage.input_tokens /output_tokens / total_tokens：Token 用量。
- gen_ai.input.messages / gen_ai.output.messages：输入输出消息。
- gen_ai.response.finish_reasons：模型停止原因。


然而，社区标准的建设天然需要兼顾广泛适用性与长期稳定性，演进节奏相对谨慎。当前 OTel GenAI 语义规范仍处于 Development 状态，很多新概念、新场景还在持续吸收和收敛中。

在阿里巴巴和蚂蚁集团的实践中，我们遇到了大量更复杂和细化的真实场景。例如，一个看似简单的“用千问点奶茶”场景，背后实际涉及千问 Agent、闪购 Agent、高德 Agent、支付宝 Agent 等多个业务系统的跨域协同。这些场景对语义表达提出了更高要求。

为此，我们基于 OTel GenAI 社区标准，沉淀内部海量实战经验，推出 LoongSuite GenAI 可观测语义规范**[3]**。2026 年，该规范已正式开源，作为 OTel GenAI 的厂商增强标准，后续将逐步把优化能力贡献至社区上游。

### ▍5.2 部分核心扩展

#### 扩展一：Entry Span 与 Step Span — 让复杂 Agent 调用链可读

问题背景：当 Agent 执行长程任务时，单个 Trace 中可能包含成百上千个 Span，原生标准无法区分业务层级，调用链杂乱难分析。

语义建模：

- Entry Span（gen_ai.span.kind = ENTRY）：在 Agent 调用的入口处创建，用于还原模型和用户的原始输入、输出，形成对话历史。确保在处理下游任务时，数据不受 System Prompt 或框架 Prompt 的污染，能够获取最原始的客户请求。
- Step Span（gen_ai.operation.name = react）：代表 Agent 在每次 ReAct 过程中的层次化表达。每次 ReAct 完成“反思 → 工具调用 → 模型调用”的循环，通过 gen_ai.react.round 标识轮次。逐轮的 Span 结构使每轮循环的轨迹一目了然。


该语义规范已在 OpenClaw、QwenPaw、Hermes Agent 等多个场景中落地。

#### 扩展二：Skill 语义 — 让业务功能域可观测

问题背景：在电商购物助手等 Agent 场景中，用户指令由 Agent 理解意图后路由到对应的 Skill（技能）完成执行。现有语义规范缺少对 Skill 这一业务功能聚合层的抽象。

语义建模：新增 gen_ai.skill.*属性族：

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6a1eb568eb5f77400650c57f/f4990766-e466-436d-a9f8-515ac1f60997.png)

当前阶段这些属性附着在 execute_tool Span 上快速落地，同时我们已实现独立的invoke_skill Span 方案，并向 OTel 社区提交了提案（#3540）。

下游价值：可观测平台可以按功能域聚合分析——快速定位“哪个 Skill 错误率最高”、对比“新版本 Skill 上线后延迟是否劣化”、度量“LLM 调用占 Skill 总耗时的比例”。

### ▍5.3 工程化落地：GenAI Utils

语义规范的价值不仅在于文档，更在于工程化落地。我们在探针中实现了 GenAI Utils，作为 LoongSuite SemConv 的工程化能力层：

- 插桩层只做数据提取：各框架插桩库通过 Hook/Monkey-Patch 拦截框架调用，将数据填充到对应的 Invocation 数据对象中。
- GenAI Utils 统一收口遥测输出：所有 Span 创建、属性挂载、Metrics 记录、Event 发送、Context 管理均由 ExtendedTelemetryHandler内部完成。
- 规范升级只改一处：当 LoongSuite SemConv 新增字段或调整结构时，只需修改 GenAI Utils，所有下游插桩库自动生效。


支持的 Invocation 类型包括 LLMInvocation、InvokeAgentInvocation、CreateAgentInvocation、ExecuteToolInvocation、EmbeddingInvocation、RetrieveInvocation、RerankInvocation、MemoryInvocation，覆盖 GenAI 全生命周期操作。

GenAI Utils 拥有 Python，Node.js，Go 的版本，Java 版本也即将发布，其中 Python 和 Node.js 版本已经开源，其余部分也会陆续开源。

**06**

***总结***

*Cloud Native*

阿里云 Agent 观测和审计方案适用于以下场景：

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6a1eb568eb5f77400650c57f/eb9d0e34-c153-47cd-a2a7-5c8644ef2319.png)

AI Agent 的普及大幅提升生产与办公效率，也对可观测、可审计、可治理能力提出全新要求。区别于传统微服务、Web 应用，AI Agent 融合了大模型调用、工具执行、多轮推理等新型运行模式，必须配套专属的数据采集与语义标准。

阿里云 LoongSuite 整套解决方案，针对三类主流 Agent 形态实现全覆盖：

- 端侧的 LoongSuite Pilot让本地运行的 Coding Agent（Claude Code、Cursor、Codex、Qoder、QoderWork 等）行为不再黑盒。
- 专用插件（OpenClaw、Hermes Agent、QwenPaw）让个人通用助理获得完整的链路追踪能力。
- LoongSuite Python 探针**[****4]**（开源，17 个框架插桩库）让基于 LangChain、AgentScope、Dify、MCP 等框架开发的 Agent 应用实现零代码接入。


更重要的是，我们在 OTel GenAI 语义规范基础上推出的 LoongSuite GenAI 可观测语义规范（已开源），通过 Entry/Step Span、Skill 语义等关键语义扩展，填补了社区标准在真实业务场景中的语义空白。配合 GenAI Utils 的工程化封装，实现规范统一落地、高效迭代。

统一语义规范的最终目标，不是产出一份文档，而是让所有使用该套规范的用户和厂商，能够为快速增长的 GenAI 应用真正做到可看见、可分析、可治理、可演进。

相关链接：

[1] 云监控 2.0 控制台

https://cmsnext.console.aliyun.com/

[2] AgentLoop 控制台

https://agentloop.console.aliyun.com/

[3] 语义规范

https://github.com/alibaba/loongsuite-semantic-conventions-genai/

[4] LoongSuite Python 探针

https://github.com/alibaba/loongsuite-python-agent

