---
作者:
  - "阿里云云原生"
原文链接: https://mp.weixin.qq.com/s?__biz=MzUzNzYxNjAzMg==&amp;mid=2247572462&amp;idx=1&amp;sn=427d6929735cd72e0c594070f5bc7ebb&amp;chksm=fb773c98138864b67ce2bc275514414581f5732e4284f4b310da8fbce74b7877c2379c4d1ab8&amp;mpshare=1&amp;scene=1&amp;srcid=0316dPenRCrM34CMetGRSdUI&amp;sharer_shareinfo=202bc50ebea216afd5f86a377fc5938a&amp;sharer_shareinfo_first=202bc50ebea216afd5f86a377fc5938a#rd
发布时间: ""
收藏时间: "2025-03-16"
关联日记: "[[2025-03-16]]"
tags:
  - 文章
---
*本文为 《AI 原生开发实战营-杭州站》 的分享文字稿*

在过去一年里大模型领域主要有两大领域的热点，一个是 LLM，几乎每月速度革新，大家关心的是效果和成本。另一个是 AI Agent，大家尝试解决各个领域应用问题，大家关心的是场景和竞争力。下面我们重点分享一下 AI Agent 的趋势和实践。

***AI Agent 洞察***

*Cloud Native*

## AI Agent 在从单 Agent 到多 Agent 加速演进；以数据为核心的智能体平台会加速形成；构建高质量数据和持续优化数据质量能力会是智能体成功的关键。

AI Agent 架构和发展趋势

**什么是智能体？**

AI Agent 是一种能够感知环境、自主决策并执行行动的智能实体，具备通过独立思考和调用工具逐步完成目标的能力。

**为什么要智能体呢？**

因为 LLM 只是模拟人脑神经元推理过程，如果要完成一个具体的现实任务，还是需要像人一样有言耳鼻舌身的感知系统，有记忆和经验辅助决策，最后行动。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67d6995e24d87101a28ebb00/f9401d44-6c9f-4548-befc-e3ce86fdfb8d.png)

**智能体的发展趋势**

在过去 1 年时间里大家更多在探索各种固定的，单任务的智能体，解决一个个具体小问题。从今年开始大家开始构建智能体平台和范式，提升多 Agent 协同，编排，优化数据质量体系。终态是具备一个超级智能体，一站式解决所有问题，通用人工智能真正到来。

考虑到通用性和专业性，很多时候需要平衡，成本和效果也需要平衡，AGI 到来仍需要一定时间，因此我们判断未来主要方向是以数据为中心的多智能体协同模式。

**AI Agent 竞争力构建**

AI Agent 构建过程中我们思考第一个问题是，智能体的核心竞争力是什么？

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67d6995e24d87101a28ebb00/7e9c7500-0394-438e-91bd-5f8b0053492d.png)

我们认为**模型 + 数据 + 场景**是构建 AI 产品竞争力的三个关键点。

1、模型把公域数据挖掘的比较充分了，下一步重点可能是成本和性能（DeepSeek在加速推动发生）。

2、私域数据是每个公司的核心壁垒，需要做的是充分挖掘私域数据，沉淀好数据，持续优化数据，释放最大客户价值。生产资源足够好，有底层模型生产力加持，可以持续演进。

3、找到自己领域高频，结构化和风险可控的场景，逐步延伸场景的专业性，帮助客户提升效率。如我们 DEVOPS 领域的智能编码，灵码在代码辅助高频场景突破，通过灵码提升大家构建智能体效率。

**AI Agent 数据飞轮**

大家都知道数据是核心竞争力，那如何打造自己领域高质量数据呢？

首先我们每个应用能够从客户收集和沉淀数据，这部分数据是个性化和专业性的前提。其次我们每个领域都有自己的专业数据和 SOP，可以结合客户数据高效解决客户问题。

当我们构架好智能体要发布客户，需要提前对数据和效果构建数据评测集，以便满足客户对 SLA 的确定性要求。上线后我们需要收集客户反馈数据，通过反馈数据分析优化我们的行业数据，工具集，场景。

通过左边评估数据体系持续优化右边私域高质量数据体系。完成客户诉求到数据的高质量匹配。从而让这个飞轮持续转起来，持续优化企业竞争力！

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67d6995e24d87101a28ebb00/0e4c1cdd-c482-41df-b0dd-3e9b8c43876e.png)

**AI Agent：构建以数据为中心智能体平台**

上面四类数据用什么系统去承载和流转呢？

我们的答案是**构建以数据为中心的智能体平台。**

1、构建好企业知识库，通过平台工具将数据转换成 Markdown，然后推到向量数据库，构建领域数据；通过工具集帮助Agent获取结构化客户数据。

2、构建数据评测集和自动化智能化数据评估体系。

3、在前台构建客户反馈和跟踪体系。

4、通过多 Agent 架构进行数据和任务的自动流转。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67d6995e24d87101a28ebb00/51ea7a4a-23c8-4dd4-8445-ec1619ba3cb8.png)

**AI Agent：全局技术架构**

那如何构建多 Agent 架构呢？

阿里巴巴在去年云栖大会推出了 Spring-AI-Alibaba 框架和生态工具集合，助理企业构建智能体。

- 通过 Higress 一键集成系统数据和工具集，获取私域客户数据。
- 通过 Otel 观测体系完成全链路的数据质量观测。
- 通过 Nacos 动态更新提示词数据，实时查看优化效果。
- 通过 Apache RocketMQ 动态更新 RAG 数据，实时反馈和优化数据。


![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67d6995e24d87101a28ebb00/e1f5be75-71c8-4aeb-95d3-4e819e41c1e4.png)

***AI Agent 实践***

*Cloud Native*

## 通过上面介绍大家构建以数据为中心智能体的重大意义和趋势。下面我们重点分享阿里巴巴在落地 AI Agent 的最佳实践，以便给大家做一个参考，加速 AI 时代到来～

**AI Agent 实践（Higress：一键集成多种数据源）**

Higress 是阿里开源的 AI 原生 API 网关，具备行业最全 AI 生态插件，能够帮助开发者一键集成多种数据源。

- 支持对接多种模型，Higress 可以一键集成多种模型，统一协议，统一权限，统一容灾；
- 通过搜索工具获取领域数据，通过 MCP Server 获取客户数据，整合推理需要的完整数据。
- 统一数据格式转换，通过缓存和向量检索构建长短期记忆数据，降低 LLM 调用，降低成本，提升性能和吞吐。
- 集成可观测体做数据合规，数据质量评估。


![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67d6995e24d87101a28ebb00/81df606f-7715-4f37-b86d-1b3c46f43ec4.png)

**AI Agent 实践（Otel：全链路数据质量追踪）**

我们基于 Otel 观测体系能够自动的分析推理过程中效果，召回效果。效果不好，可以全链路追踪客户整个检索和推理过程，分析是知识库问题，RAG 问题，还是工具集问题，提升优化数据效率。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67d6995e24d87101a28ebb00/5c865776-00b2-480c-9850-1c5e28e064b1.png)

**AI Agent 实践（Nacos：动态更新提示词数据）**

Agent 中有大量提示词，算法等参数，通过 Nacos 可以做到动态实时推送，及时获得优化的效果。如果系统上线担心修改提示词效果不符合预期，还可以通过灰度配置逐步观测优化提示词数据的效果。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67d6995e24d87101a28ebb00/874a443e-0830-4c58-bc41-9a1292e3ebbd.png)

**AI Agent 实践（Apache RocketMQ：提升 RAG 数据实时性）**

系统数据和客户数据都是不断更新的，我们可以通过 RocketMQ 把变更事件和数据实时同步，以便每次推理能拿到最及时数据和效果。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67d6995e24d87101a28ebb00/d15b457a-42df-46a5-8247-b2b0ff2bd767.png)

**AI Agent 实践（AI 行业专家解决方案）**

我们通过上面技术体系构建开源 AI 专家和阿里云云原生 API 网关和微服务引擎 MSE 两个产品的智能诊断体系，解决 95% 以上咨询问题，解决 85% 以上异常问题。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67d6995e24d87101a28ebb00/2cd45b78-39c8-42e3-b4ac-a7473110062d.png)

通过 Higress 屏蔽底层多个模型，工具体系，构建数据安全链路和账号安全体系， 通过 Spring-AI-Alibaba 构建 Agent 和编排，提供 chat 模式解决咨询问题， Composer 模式解决客户异常问题。

**AI Agent 实践（DeepSeek 联网搜索+数据安全解决方案）**

DeepSeek 很火，用过的同学都知道，能联网的 DeepSeek 还是真正的满血版。

目前大量客户通过 Higress 一键集成 DeepSeek 和联网能力，集成夸克搜索数据，体验最佳能力。通过 Higress 能够在模型访问链路上全链路 TLS，保护链路数据安全。通过内容安全解决数据合规安全问题。通过 API-Key 集中管理，提高并发度，对 Agent 提供内部 API-Key，防止 API-Key 泄漏风险，并且可以根据内部 API-Key 做流量和额度控制，防止代码 bug 导致巨大 token 调用和巨大费用支出。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67d6995e24d87101a28ebb00/6ae8e398-5eca-40a8-9ba6-a8b6b631b875.png)

## 更多交流，欢迎加群～

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67d6995e24d87101a28ebb00/3f04cfb3-ad90-477f-982a-2dc8cfc2a7e7.png)

## 招聘

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67d6995e24d87101a28ebb00/05d51e0c-fc87-443f-b28f-7a6d9c321c19.png)

