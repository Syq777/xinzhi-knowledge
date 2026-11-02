---
作者:
  - "阿里云云原生"
原文链接: https://mp.weixin.qq.com/s?__biz=MzUzNzYxNjAzMg==&amp;mid=2247586083&amp;idx=1&amp;sn=4c16de7c099d848875e8fd1209a0bc01&amp;chksm=fb97bf6eb500a353a6575fe2c1d76c6054875f6d44b428434f430229a3af832520ba9d50bde6&amp;mpshare=1&amp;scene=1&amp;srcid=08224rVrppne0cVmw8Y9jCGw&amp;sharer_shareinfo=5000b7da5555809ef81fcbf48c742c6c&amp;sharer_shareinfo_first=5000b7da5555809ef81fcbf48c742c6c#rd
发布时间: ""
收藏时间: "2026-08-22"
关联日记: "[[2026-08-22]]"
tags:
  - 文章
---
今天，Agent 评估与优化 · Close the Loop 三城巡演首站北京站圆满落幕。

本场活动联合 Dify 举办，吸引了近百名技术从业者参与，围绕“Observe / 观测与审计”这一主题，深度分享了 Agent 可观测性范式、Dify 可解释性实践、AI Coding 观测与降本等议题，并设置了 AgentLoop 动手实操环节。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6a895b0e2decab61d5057819/63952d2d-d7de-4e2a-9897-8824be73d39d.webp)

关注公众号，后台回复：Loop0821

获取北京站讲师 PPT 合辑

### ▍议题一：Agent 评估与优化全景

分享嘉宾：阿里云 Agentloop 产品经理 涯海

从企业 Agent 落地的六大挑战“看不清、评不准、存不下、改不动、控不住、复制难”开始，提出从 LLMOps 到 AgentOps 的范式升级：治理对象从单次调用变为完整推理轨迹 Trajectory，以“观测→评估→优化→回测”为主线构建数据飞轮：零代码插桩覆盖约 45 个框架，Agent-as-a-Judge 评估与专家一致性达 90%+，归因分析把评分转译为改进动作，变更门禁拦截负向变更。举例了 某游戏客户 3 天跑通优化闭环、客服质检覆盖率从 5% 升至 100%：谁的飞轮转得快，Agent 就越聪明。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6a895b0e2decab61d5057819/c35a5816-bdf1-4e12-a3e8-c5dde73e4d9e.jpeg)

### ▍议题二：Dify 如何让 Agent 的每一步可解释、可比较和可验证

分享嘉宾：Dify 工程师 姜涵煦

涵煦分享了在 Agent 编排平台侧的可观测实践：如何让开发者在可视化工作流中看清每个节点的输入输出与耗时，让不同版本的 Agent 编排可以横向比较，让每一次改动的效果可以被验证而非感觉变好了。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6a895b0e2decab61d5057819/e7770eef-0e78-4144-8c3a-e1665e4b175e.jpeg)

### ▍议题三：AI Coding 的观测和科学降本实践

分享嘉宾：阿里云 Agentloop 研发工程师 马云雷

AI Coding 是当前 Token 消耗最大、调用链最深的 Agent 场景之一。本议题基于真实 AI Coding 场景，分享了两个问题的解法：一是怎么看清调用链，从一次编码任务出发，还原模型调用、工具执行、上下文组装的完整链路，定位耗时与失败点；二是怎么把成本科学地降下来，基于观测数据识别冗余调用与低效上下文，在不牺牲任务完成质量的前提下压缩 Token 开销。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6a895b0e2decab61d5057819/758fcda6-6c18-4e0f-9b78-f3f21c6e4fb5.jpeg)

### ▍动手实操：给 Coding Agent 或其他桌面端 Agent 接入AgentLoop

通过 LoongSuite Pilot 将开发者本机的 AI Coding Agent 运行数据接入 AgentLoop，实现会话、模型调用、工具调用、Token 用量和 Trace 数据的统一观测与分析。

实操文档：https://help.aliyun.com/zh/document_detail/3033878.html

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6a895b0e2decab61d5057819/03b172de-695c-47ae-9064-82807e2b0217.jpeg)

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6a895b0e2decab61d5057819/69a295d6-f70f-4706-9c3f-5b11fc367a30.jpeg)

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6a895b0e2decab61d5057819/5a834c9c-bd1f-470a-88d4-425cc03ed093.jpeg)

### ▍现场花絮

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6a895b0e2decab61d5057819/d07cbdae-44ae-4186-8dbf-accc28150da0.jpeg)

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6a895b0e2decab61d5057819/eb6418eb-94b0-40f5-9dfb-0bc20388f417.jpeg)

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6a895b0e2decab61d5057819/f122499f-f5a4-4de5-aa61-6028df1cd541.jpeg)

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6a895b0e2decab61d5057819/545f6eec-9ced-4e75-bb0c-4fd1fa4867df.jpeg)



Agent 观测与优化 Close the Loop 巡回沙龙，8月29日深圳站将联合 AgentScope 分享“Evaluate / 评估与实验”，9月4日上海站联合 LangChain 分享“Optimize / 进化”。

报名审核制，审核通过将收到短信通知。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6a895b0e2decab61d5057819/245a97d7-1472-4f19-bb3e-de4c825e07a4.webp)

