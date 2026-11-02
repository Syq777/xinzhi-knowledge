---
作者:
  - "腾讯技术工程"
原文链接: https://mp.weixin.qq.com/s?__biz=MjM5ODYwMjI2MA==&amp;mid=2649796189&amp;idx=1&amp;sn=edc8db54287983686dd354c0a2beb208&amp;chksm=bf2d7ddee8fc0ccfd1abbfec33b8ef9f69434d9813d30f8ad8a31895a372092377738132dd0e&amp;mpshare=1&amp;scene=1&amp;srcid=1020YJuGNc30FodisGwXubIj&amp;sharer_shareinfo=3585268e25cd020f6550b24c2e61e7ab&amp;sharer_shareinfo_first=3585268e25cd020f6550b24c2e61e7ab#rd
发布时间: ""
收藏时间: "2025-10-20"
关联日记: "[[2025-10-20]]"
tags:
  - 文章
---
![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68f6074c0919ce667808ca47/5a4de3df-700a-437f-8efb-460f064d083f.gif)

> 「Agent不稀奇，能“自己想、自己干、自己复盘”的才是好Agent」可一到落地，名词、框架和坑一起涌来：设计模式、强自治、可控流程、多代理协作.... 到底该不该用 Agent？该选哪一类框架？需要用到什么程度？这篇文章用直观的图表、清晰的示例，为你讲清什么是Agent、什么场景适合使用Agent以及各类主流Agent框架，希望能帮各位少走弯路，迅速判断技术路径。

### 1.Workflow和Agent的区别

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68f6074c0919ce667808ca47/47d9489d-3f1c-4bb2-9a69-92fc4ed42d3d.png)

### 2.Agent框架选择

核心依赖Github上Star数以及市场热度，综合选取5款Agent框架：

1.**AutoGPT：**Github 17.8w Star

2.**LangGraph：** Github 13.1w Star

3.**Dify：** Github 11.2w Star

4.**CrewAI：**Github 3w Star

5.**AutoGen：**微软开源 Github 5w Star

### 3.各Agent框架对比结论

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68f6074c0919ce667808ca47/9a3d6b15-77d2-4234-b31f-d259cceb3604.png)

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68f6074c0919ce667808ca47/e94d2e04-5b37-4074-8194-b6aabc6d05fe.png)

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68f6074c0919ce667808ca47/f04f2dcf-6119-4e24-abc2-3c168e0ee36f.png)

### 4.为什么需要使用Agent框架

**结论：**只要“问题不可完全穷举、要跨多系统查证、并且需要在对话中澄清/协商/决策”，就更应该用 Agent 框架，而不是纯 Workflow。

为什么？用一个真实的ToC场景客服链路来说明。

#### 4.1纯 Workflow 在智能客服里的“天花板”

Workflow（无论是 Dify 的可视化编排，还是 LangGraph 的状态机）非常适合步骤确定 + 条件有限的流程，比如：

1.查询订单 → 格式化答复

2.退货→生成标签→发通知

3.FAQ 检索→返回片段

一旦进入长尾问题，Workflow 就会遇到“分支爆炸”：

**例：**同一条“包裹没到”诉求，可能要综合 ①承运商状态 ②发货 SLA ③节假日政策 ④地址异常 ⑤是否会员 ⑥是否已报缺货 ⑦是否已部分签收 ⑧是否叠加优惠券/补发 等。

如果你用固定分支描述：

假设有 5 个意图 × 6 种物流状态 × 3 种用户等级 × 3 个政策时段（平日/大促/假期） × 3 种地理区域，共5×6×3×3×3=810 条潜在路径。

这还没算异常（报损、拒收、欺诈信号）与“对话澄清”的分支。维护成本和上线速度都会被拖垮。此外，Workflow 对 **对话中的“澄清—再决策—再行动** 并不天然友好，需要把每一步提问、回答、重试都画成节点，复杂而脆弱。

#### 4.2Agent 框架解决的核心问题

以 AutoGen/CrewAI 这类 Agent 框架为例，它们把“在对话里动态规划与调用工具”作为第一性能力：

**场景：**用户说“我 8 月 1 号下的单今天还没到，收件地址其实要换，而且我被重复扣费了。”

一个合格的客服 Agent 团队会做什么？

1.**意图识别 + 澄清**

● Planner Agent：拆出多意图（物流异常、改址、计费异常），先问关键澄清（订单号/新地址/扣费凭证）。

2.**跨系统取证**

● OMS/物流工具：查轨迹与 SLA；

● 计费/支付工具：核对重复扣款交易；

● CRM：看是否 VIP、是否有历史补偿记录。

3.**政策推理与合规**

● Policy/Critic Agent：套用“假期延误 + VIP + 改址”的组合条款，评估可给的补偿区间、是否可免费改址、是否触发风控人工复核。

4.**方案生成与协商**

● 提出“改址 + 走加急补发 / 或原包裹拦截 + 退款差额 + 账单冲正”的可行方案，并在对话中按用户反馈实时调整。

5.**执行与闭环**

● 调用工单/票据工具，落账/发券/改单/寄件，写入 CRM 备注；

● 生成总结，告知时限与跟踪号；

● 若任一步失败，自动选择备选策略或升级人工。

这些动作里，很多步骤**无法事先“画”成固定分支，需要在对话上下文里做决策、需要跨工具动态组合、需要“问一句 → 查一下 → 再决定”，**这正是 Agent 的强项。

### 5.各Agent详细介绍

#### 5.1AutoGPT

**简介：**AutoGPT是第一个爆火的自主AI Agent框架，提供一系列工具让用户构建和使用自治代理。其功能涵盖代理创建模块“Forge”、性能评测基准agbenchmark、排行榜以及易用的UI和CLI接口。

**主要特点：**AutoGPT支持“思考-行动-反馈-学习”的循环，让代理不断生成子任务并执行。并且拥有丰富的插件和工具接口，允许代理访问浏览器、文件系统、API等资源，从而完成复杂的链式任务。

**典型应用场景：**需要让Agent自动拆解目标并执行的，如市场调研、行程规划、代码编写等

**优势与不足：**

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68f6074c0919ce667808ca47/4c198af1-5719-4dcb-8e27-bf03c94a825f.png)

**使用示例：基于AutoGPT让Agent帮我写一篇介绍AutoGPT的文章**

1.创建Agent及配置名称、角色以及目标

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68f6074c0919ce667808ca47/5b717d1a-96c2-45ed-af01-a62d3915a292.png)

2.Agent 自主思考、规划、执行

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68f6074c0919ce667808ca47/fefc1f15-5e67-4427-837b-2d1d0d709bb3.jpeg)

3.最终输出

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68f6074c0919ce667808ca47/338a2730-cfc1-422f-a89c-9655cdbb1c12.png)

#### 5.2LangGraph

**简介：**LangGraph 是由 LangChain 团队推出的**有状态、持久运行、多智能体**应用的编排框架。核心将Agent建模成一个**图（Graph）**：每个节点是计算步骤（LLM 调用、工具函数、任意 Python 代码等），边控制流转（含条件与循环），并最终实现既定目标。并且在今年6月提供了**预构建模式**，对常见的多智能体场景提供了抽象封装，开发者只需定义少量参数（如参与的子智能体、主体提示词等）即可快速生成完整的多 Agent 协作系统。

**Graph和预构建模式的示意图：**

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68f6074c0919ce667808ca47/0643b9c7-10c9-416c-ae04-ce978bb1431e.png)

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68f6074c0919ce667808ca47/e219b256-33b4-431b-b30c-e0a80e0ef052.png)

**主要特点：**支持图式编排、可人工干预、可中断/续跑。LangGraph可形成可控的分支/循环流程，可在每个节点中加入人工干预环节，适合需要人工审批/修订的业务场景，并且基于持久化状态可方便中断、续跑、回溯。

**典型应用场景：**可明确拆解任务步骤的场景，如RAG类、文章生成、日程助手等。

**优势与不足：**

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68f6074c0919ce667808ca47/9e4cb366-2ec9-4860-a27b-bccd6bc08543.png)

**使用示例：基于LangGraph让Agent帮我写一篇介绍LangGraph的文章**

1.构建工作流（Workflow）

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68f6074c0919ce667808ca47/a82a6fc6-246c-4f4b-8072-e458272435ac.png)

附工作流运行逻辑：

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68f6074c0919ce667808ca47/e0d17c41-e559-4e4d-85e0-4262ebb1047b.png)

2.最终输出

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68f6074c0919ce667808ca47/6bd429f3-08f3-40b7-8cd9-084f014145c7.png)

#### 5.3Dify

**简介：**Dify（Do It For You）是一个开源的低代码平台，旨在简化大模型（LLM）驱动的AI应用开发与部署。它融合了“后端即服务 (BaaS)”与 LLMOps 概念，提供涵盖模型接入、提示设计、知识库检索、智能代理、数据监控等在内的一站式解决方案。通过直观的可视化界面和预构建组件，开发者和非技术人员都可以快速构建如聊天机器人、内容生成、数据分析等各类生成式AI应用。

**主要特点：**低代码、可视化工作流构建、检索增强生成（RAG）管道、开放工具市场

**典型应用场景：**可明确拆解任务步骤的场景，如RAG类、文章生成、日程助手等

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68f6074c0919ce667808ca47/5d985e98-e776-4acb-9f89-5f223c0ea18e.png)

**使用示例：**

1.**工作流Workflow类型**

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68f6074c0919ce667808ca47/844cdba5-a816-4f0e-abf0-abc5cefd5de0.png)

2.**Agent类型（Function Call）**

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68f6074c0919ce667808ca47/a1c682eb-7899-4986-a5fe-8404b1d22af5.png)

#### 5.4CrewAI

**简介：**CrewAI 是一个多智能体（multi-agent）编排框架，其核心理念是让多个具备特定角色的 AI **代理**协同合作（组成“crew”团队）来完成复杂任务。每个代理被赋予特定的角色、目标和背景知识，通过相互分工与配合，自动地进行任务委派和问询，最终以团队形式完成用户交给的工作。

**主要特点：**多工具及生态集成、支持Workflow和AI Agent两种模式

**优势与不足：**

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68f6074c0919ce667808ca47/69a785ff-fe01-4da5-b1bc-1857387de86a.png)

**使用示例：研究AIagent领域的最新进展**

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68f6074c0919ce667808ca47/3e4b6cd8-c721-45c5-84bd-925324b0b1ec.png)

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68f6074c0919ce667808ca47/ea9e82dc-c75f-4bf1-8515-a1442c2725eb.png)

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68f6074c0919ce667808ca47/e8bbfb37-cc3f-45ee-86c2-7c7eb0147c23.png)

#### 5.5AutoGen

**简介：**AutoGen 是微软开源的一个面向 Agentic AI（代理式人工智能）的编程框架，用于构建 AI 智能体并促进多个智能体协作完成复杂任务。AutoGen 支持事件驱动的分布式架构，具有良好的可扩展性和弹性，可用于搭建可自主行动或在人类监督下运行的多代理 AI 系统。

**主要特点：**微软开源、原生多Agent支持、灵活对话控制

**优势与不足：**

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68f6074c0919ce667808ca47/efb6e337-07ae-41f9-ae4e-c58dab63e758.png)

Swarm模式下的机票退订助手示例：

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68f6074c0919ce667808ca47/efee33e6-e1ad-41a8-8651-7c632789c65c.png)

### 6.总结

本篇文章主要介绍了目前 WorkFlow 和 Agent 的区别，以及什么时候应该采用 Agent 框架：当问题复杂、长尾且多变，Agent 才是主力。同时也简要的介绍了目前几类框架如AutoGPT、LangGraph、Dify、CrewAI、AutoGen，希望能在技术路线的选择与框架选型上帮助到各位读者。

腾讯云TDAI（TencentDB AI Service，简称TDAI）团队也在积极探索数据库与 AI 的结合，并正式推出数据库AI服务，为赋予 Agent 长上下文理解与个性化交互能力，腾讯云在数据库AI服务中推出面向 Agent 记忆场景的产品——Agent Memory，负责存储、检索并管理历史交互信息，让AI能够记住并运用这些信息，从而在持续的互动中表现出更强的连贯性、上下文理解力和个性化服务能力。

可以看到，Agent 不只是新的技术名词，更是一种全新的思维方式——让智能系统从“执行命令”走向“理解目标”。未来，在复杂、多变的业务世界中，腾讯云TDAI团队将持续探索从底层存储、索引到记忆调用的完整链路能力，为客户提供 Agent 的基础组件，奠定AI转型的坚实起点。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68f6074c0919ce667808ca47/d84e9a65-ba69-4366-a26a-6f4a1e85642c.gif)

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68f6074c0919ce667808ca47/1ef8ee39-5d2b-4708-9dc8-df239b184c0b.png)


新枝标签： #Agent
