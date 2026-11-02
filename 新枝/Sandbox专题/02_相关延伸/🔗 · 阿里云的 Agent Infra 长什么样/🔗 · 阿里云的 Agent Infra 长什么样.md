---
作者:
  - "阿里云云原生"
原文链接: https://mp.weixin.qq.com/s?__biz=MzUzNzYxNjAzMg==&amp;mid=2247583929&amp;idx=1&amp;sn=2063a452e45293b841a4592f8c6640f9&amp;chksm=fb280c7be940bfc981c70319adda7e6b20552483e95c6c619588cafb4d84821e7e2ea3a50a3f&amp;mpshare=1&amp;scene=1&amp;srcid=0520jlFeKkUhfGOgIiy8yflx&amp;sharer_shareinfo=0379a3df773bb073c58150dea6625429&amp;sharer_shareinfo_first=0379a3df773bb073c58150dea6625429#rd
发布时间: ""
收藏时间: "2026-05-20"
关联日记: "[[2026-05-20]]"
tags:
  - 文章
---
和 Harness 工程一样，Agent Infra 也是一个时常被从业者反复提起的 Buzzword。但关于 Agent Infra 应该包含什么，大家在实践中还没有绝对的共识。

今天，2026 阿里云云峰会上，阿里云智能首席技术官李飞飞分享了阿里云的 Agent Infra 长什么样，包括六大基础设施能力，包括 Agent 运行时、Agent 编排、Agent 治理、Agent 记忆、Agent 数据平面和 Agent 安全，以应对 Agent 的六大挑战，包括 Agent 无规律突发负载、Agent 大规模动态编排、Agent 短生命周期、Agent 数据模态和存储形式复杂、Agent 动态环境依赖、Agent 任务级安全可控。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6a0d90b804060802528d94c3/bc30916e-05c4-4760-ac83-ed53d920c995.png)

在 Agent Native 基础设施分论坛上，阿里云智能云原生应用平台产品负责人李国强分享了团队在 Agent 工程化领域的完整思考与产品实践，从构建、部署到规模化运行，如何用一套 Agent Infra 覆盖智能体的开发-运行-治理-运维-优化全周期。以下是本次分享的核心内容。

**01**

***企业构建 Agent 时的五大痛点***

*Cloud Native*

当前，企业投产 Agent 的热情空前高涨。Gartner 预测，70% 的企业将在 2026 年底在生产环境运行 AI Agents，40% 企业应用将嵌入 Agents 以获得新的业务增长，而 2025 年初这一比例还不到 5%。但“大炼钢”似的加速落地过程中，工程化的挑战开始进入真正的深水区。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6a0d90b804060802528d94c3/36349d4d-3dba-4c92-ad51-7b7c0120145d.png)

第一，智能体架构依赖多，如何快速构建部署。开发框架多、依赖多，运行环境对隔离性和弹性要求极高。从本地 IDE 到生产上线，中间要穿越沙箱、运行时、模型接入、凭证管理等多层链路。环节一多，落地周期就被拉长。

第二，多智能体如何治理与协作。多智能体已经成为企业落地的趋势。但多个 Agent 各自为政、通信黑盒，如何进行统一的治理及管控？如何让人和 Agent、Agent 和 Agent 高效协同，而非各自为战？

第三，如何洞察运行状态，做到成本可控。Agent 弹性高、依赖多、调用链长。一旦 Token 消耗失控，成本便成“黑洞”。企业需要从运维和运营双重视角实时掌握 Agent 的运行态势。

第四，效果评估难，不知道如何持续优化。Agent 效果是关键生命线，但运行过程是黑盒，传统的测试手段难以胜任。如何建立评估体系并驱动 Agent 自主进化，是摆在所有团队面前的课题。

第五，复杂架构下运维问题发现慢、修复难。智能体进一步增加了系统的复杂性，传统 SRE 方式已力有不逮。需要用智能化手段来保障新兴智能业务的连续性。

这五大痛点，分别指向 Agent 生命周期的不同阶段。而阿里云给出的回答，是一套完整的 Agent Infra 产品矩阵。

**02**

***Agent Infra 产品全景：***

***五大平台覆盖全周期***

*Cloud Native*

阿里云 Agent Infra 的设计逻辑，是让企业“聚焦效果，工程交给基础设施”。围绕 Agent 开发、运行、治理、运维、优化五个阶段，五大核心产品各司其职：

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6a0d90b804060802528d94c3/769fcad8-bc5a-46f5-bad7-60dd3adf0f3f.png)

- AgentRun：一站式智能体开发构建平台
- AgentTeams：多智能体治理与协作平台
- AgentLoop - 可观测：智能体全栈可观测
- AgentLoop- 评估与优化：Agent 持续优化
- STAROps：全域智能运维平台


接下来，我们按照 Agent 生命周期从构建到运维的顺序逐一拆解。

**03**

***AgentRun：以高代码为核心的***

***一站式 Agentic AI 基础设施[1]***

*Cloud Native*

AgentRun 基于函数计算（Function Compute），是一个以高代码为核心、生态开放、灵活组装的一站式 Agentic AI 基础设施平台，为企业级 Agent 提供开发、调试、部署、运维的全生命周期管理。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6a0d90b804060802528d94c3/8f4ddf23-ce64-4cd6-a358-2480f1fb4552.png)

它的核心设计理念是“高代码灵活定制 + 低代码快速验证”双轨并行：

- 在高代码侧，AgentRun 提供完整的运行时（Runtime）、沙箱（Sandbox）、可观测（Observability）、Agent 评估（Evaluation）、记忆与知识库（Context Engineering）、模型接入（Model Connector）以及凭证与安全管理（Credential）等模块，开发者可以根据业务需求灵活组装。
- 在低代码侧，它兼容阿里云百炼、ModelScope 等无代码/低代码平台，以及 MCP 协议和 SDK，实现开箱即用的快速验证能力。同时，通过 AI 网关 Higress 统一接入开源模型和微调模型（on PAI & FC & ACS），打通模型推理链路。


一句话概括：AgentRun 是让 Agent 从“能跑”到“跑好”的工程底座。

**04**

***AgentTeams：***

***让 AI Agent 组成真正的团队***

*Cloud Native*

如果说 AgentRun 解决的是“单个 Agent 怎么构建”的问题，AgentTeams 回答的则是“多个 Agent 怎么协作”的命题。这是从微服务治理向多智能体治理的产品升级。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6a0d90b804060802528d94c3/f5d692d3-6670-4ac0-a090-67e2e9f10887.png)

2024-2025 年是单 Agent 试用期，2025-2026 年进入部门级多 Agent 试点，2026-2027 年将迎来企业级大规模部署。企业面临的新问题是：各部门 Agent 散落无统一管控视角、Agent 间通信黑盒人类无法有效监督、Agent 直持凭证存在安全风险、Token 消耗无监控导致成本不可控。

AgentTeams 是一站式企业多智能体治理与协作平台，聚焦四大核心诉求：统一治理（多源 Agent 纳管，不绑定单一厂商）、协作编排（Leader-Worker，人在回路）、安全合规（企业级 SSO 集成，全链路审计）、成本可控（按量计费，Token 监控限额）。

- 多源 Agent 统一纳管：所有 Agent 通信基于 Matrix 协议，实现协议级解耦。一个 Team 可以混编 OpenClaw、QwenPaw、Claude Code、自研 Agent 等异构智能体，消除框架绑定。
- Leader-Worker 协作编排：基于 Leader-Worker 架构的协同底座，Leader Agent 负责意图理解、任务拆解与进度监控，Worker Agent 分工执行。Human-in-the-Loop 设计确保过程 100% 可见，用户像看工作群聊一样洞悉 Agent 之间的交流，随时干预纠偏。
- IM 原生集成：内置 Matrix 原生 IM，同时集成钉钉、飞书、企业微信等企业主流 IM 工具。员工在熟悉的聊天窗口即可发起任务、实时监督、审批干预，Agent 执行结果回传 IM，像“数字同事”一样协作。
- Agent 资产管理（AI Registry）：统一注册 Skill、MCP Server、Agent 和 Team 模板，按 Team 分配、版本化管理、安全审核、运行态热加载。REST 到 MCP 支持零代码转换，现存业务无需改造即可接入。
- 企业级安全治理：采用零信任架构，Agent 不持有凭证，网关集中管控。身份权限、成本计量、审计合规、数据安全四维覆盖 Agent 全生命周期，满足金融、医疗、制造等行业的合规要求。
- 全链路可观测：基于 OpenTelemetry Trace 实现从用户请求到模型调用、工具执行的全链路追踪。Token 成本按 Team / Agent / 模型维度分析，联合 AgentLoop 驱动 Agent 持续进化。


AgentTeams 覆盖四类核心场景：其一，企业数字员工，用户通过企业 IM 发起任务，AgentTeams 按部门调度 Agent Team 执行，全程审计可追溯；其二，Agent Team 服务化，管理员创建 Team 池按角色配置，业务团队通过 RBAC 按需申请接入，独立配额与计费；其三，SaaS Agent Team 赋能，SaaS 厂商为不同租户分配独立 Agent Team，按权限策略控制可访问的 Skills/MCP，数据与调用隔离；其四，存量 Agent 纳管，已部署运行的异构 Agent 无需改造即可统一纳管编排，资产统一沉淀复用。

AgentTeams 的管理层基于开源项目 HiClaw**[2]**（多智能体治理与协作开源框架）实现，智能体内核为阿里云自研的 Agent 引擎 QwenPaw，兼顾灵活性与开箱即用。AgentTeams 当前处于邀测中。

**05**

***AgentLoop：***

***数据飞轮驱动 Agent 持续进化[3]***

*Cloud Native*

效果是 Agent 的生命线。但与传统应用不同，Agent 的“好不好用”很难通过一次上线就定论，它需要一套持续运转的数据飞轮来驱动进化。AgentLoop 正是为此而生的 Agent 全生命周期观测与数据飞轮平台，覆盖“可观测”和“评估与优化”两大领域。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6a0d90b804060802528d94c3/bfb80082-ad2a-4ccd-b042-5bb02e777eb0.png)

▍AgentLoop - 可观测

AgentLoop 可观测的设计目标是“零改造接入、全链路透视”。

在接入层面，AgentLoop 支持自研探针、OpenTelemetry SDK 以及 OTel eBPF 多种采集方式，兼容 QwenPaw、HiClaw、Dify、Hermes-Agent、Coze、AgentScope、阿里云百炼应用、AgentRun、LangChain/LangGraph、OpenAI 等主流 Agent 框架与平台，做到开箱即用、无侵入接入。

在分析层面，AgentLoop 提供多维度性能剖析与智能异常诊断，覆盖延迟分布、调用热点和 Token 成本归因，将“黑盒 Agent”变为“透明 Agent”。

▍AgentLoop - 评估与优化

观测是发现问题，评估与优化则是解决问题。AgentLoop 构建了一套 Collect → Analyze → Evaluate → Optimize 的完整数据飞轮：

- Collect（采集）：无侵入捕获 Agent 全链路交互数据，涵盖输入输出与每一步中间推理过程。
- Analyze（分析）：对采集到的数据进行多维度性能剖析，智能定位瓶颈与异常行为。
- Evaluate（评估）：自动化质量评分，量化 Agent 表现。支持 Agent-as-a-Judge 模式，使评估更精准。
- Optimize（优化）：实验驱动迭代，数据支撑每一次改进。支持智能调优与自主进化，包括 Prompt 优化、Skill 迭代等。


AgentLoop 的评估还具备数据集持续构建与沉淀能力。可观测数据不只是“看看就完了”，而是沉淀为可复用的评估数据集，让每一次线上交互都成为优化 Agent 的燃料。这套飞轮让 Agent 具备真正的“持续加速”能力：用得越多，跑得越好。AgentLoop - 评估与优化预计 6 月发布公测。

**06**

***STAROps：全域智能运维平台[4]***

*Cloud Native*

智能体的规模化部署，必然加剧系统的复杂性。当调用链跨越模型、工具、中间件和基础设施多层时，传统的人工运维方式已经力不从心。STAROps 是阿里云推出的全域智能运维平台，融合大模型能力与可观测数据，自主完成感知、决策、执行、验证全闭环。STAROps 围绕 Sense 全域感知、Target 目标导向，Autonomy 自主性、Resilience 业务韧性，将运维模式从被动响应推向主动自治，为企业提供 7×24 小时不间断的自主运维能力。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6a0d90b804060802528d94c3/026c24d4-2ba4-42fd-b3d8-4279ffaebfa0.png)

围绕这一目标，STAROps 提供了三大核心功能。

- 第一是智能助手：STAROps 将自然语言直接转化为跨域观测数据的统一查询分析结果，告警分析、数据查询、指标解读、日志诊断，全部在一个对话窗口内完成。
- 第二是长期任务机制：STAROps 把运维从“人盯着系统转”变成“智能体替人持续运转”，只需一次目标对齐，后续的巡检、告警分析、异常处置、验证全部自主执行。
- 第三是数字员工：企业可以为每个团队和业务场景构建专属的 SRE 智能体，自定义职责范围、权限边界与技能集，把团队积累的运维规范、处置预案和排障经验固化为可配置的“数字员工”。


**核心技术优势：**

STAROps 进行全域数据统一建模，以统一可观测数据为底座，通过自研 UModel 将日志、指标、链路、事件、拓扑等数据统一建模，构建客户系统专属运维图谱，AI 分析时自动感知服务集群、依赖组件和调用关系，从业务层到基础设施层全链路追溯。并支持按业务场景自定义扩展，实现实时拓扑推演与故障因果自动关联。

数据分析层面，平台内置通用算子与可观测 AI 算子，覆盖指标异常检测、日志聚类、链路分析、性能剖析、变更回溯等典型场景，缩短故障根因定位与处置时间。同时通过算法轻量化与计算策略优化，显著降低模型推理资源开销。

此外，STAROps 构建了贴近生产环境的故障仿真体系，打通“故障注入 - 数据采集 - 智能诊断 - 自动修复”闭环。结合线上态势与线下仿真，持续迭代分析模型与运维策略，形成可评估、可回滚、可自我进化的智能运维飞轮。

**开源贡献：**

伴随产品发布，阿里云同步开源 UModel 统一数据模型项目与 RCA 评测基准集，并联合信通院、小鹏汽车、中科院软件所等 10 逾家行业伙伴与学术机构共同发起《企业通用语义标准行业倡议》。让企业无需被单一厂商绑定，可以基于公开标准灵活构建智能运维体系。UModel 为企业提供可直接复用的实体建模与语义治理标准，免去从零搭建的高昂投入；RCA 评测基准集覆盖 2000 余条评测数据和 700 余个运维场景，为企业提供独立评估运维 AI 能力的公共标尺。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6a0d90b804060802528d94c3/230e3dff-7785-4260-bcaf-00b0b923d1c8.png)

**07**

***展望：AI 时代效果为王***

*Cloud Native*

回顾阿里云整套 Agent Infra 的设计哲学，一个核心理念贯穿始终：AI 时代效果为王。阿里云通过 Agent Infra 助力企业聚焦效果，决胜智能时代的新一轮增长。

AgentRun 让构建变简单，AgentTeams 让协作变透明和安全，AgentLoop 让效果可度量、可进化，STAROps 让运维变智能，形成一个有机的整体。

从确定性系统到概率性智能体的范式迁移已经发生。底层基础设施不再仅仅是资源池，而要成为支持智能体动态运行、持续进化的平台。当工程复杂性被基础设施消化，企业释放出的每一分精力，都将直接转化为业务效果的增量。

相关链接：

[1] https://github.com/agentscope-ai/hiclaw

[2] https://www.aliyun.com/product/fc/agentrun

[3] https://www.alibabacloud.com/help/zh/cms/cloudmonitor-2-0/what-is-agentloop

[4] https://starops.console.aliyun.com/

[5] https://cnops.com.cn/projects/h6nsi0u0v4kronqx4r7a48dc

[6] https://aiops-benchmark.oss-cn-hongkong.aliyuncs.com/rca/rca100/v1.0/README.md

