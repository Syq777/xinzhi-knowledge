---
作者:
  - "Datawhale"
原文链接: https://mp.weixin.qq.com/s?__biz=MzIyNjM2MzQyNg==&amp;mid=2247705223&amp;idx=1&amp;sn=658c032c16650cc0336b8cab7866fbf2&amp;chksm=e95edcef7f348e68bd905fb2488ab11497de2c1bc8d3dd95c463b4361e528cf3d10037920e49&amp;mpshare=1&amp;scene=1&amp;srcid=0429VvzRsfe0GB8OPJtNhLaP&amp;sharer_shareinfo=6deba1999f01566969374bf1f265ecbb&amp;sharer_shareinfo_first=6deba1999f01566969374bf1f265ecbb#rd
发布时间: ""
收藏时间: "2025-04-29"
关联日记: "[[2025-04-29]]"
tags:
  - 文章
---
Datawhale干货 

**作者：宋志学、姜舒凡，Datawhale成员**

五一小长假来临，你还在为做攻略焦头烂额？做攻略时，收藏夹堆成山；导航时：直线距离 600 米，跟着导航绕出 3 公里；到了后：景不对图，网红景点滤镜拉满。

别担心，现在人人可以成为旅游达人！我们用当下最火的高德 MCP + 星火 X1 制作了一个私人行程规划师；还进阶多智能体框架 CAMEL + 星火 X1，打造真正的“AI 导游天团”，彻底颠覆传统旅游方式！

Agent 使用地址：https://udify.app/chat/WtfvOfoxARHN4oGX

Multi-agent 开源项目地址：https://github.com/datawhalechina/handy-multi-agent

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6810de7ca70f521eb3060434/17401b49-fa2a-42ca-becc-bbb3f3afe5b7.png)

## Agent 智能体：你的私人行程规划师

核心能力：

- 需求精准解析：支持 "非特种兵版武汉游" 等模糊需求输入，自动锁定黄鹤楼、东湖等经典景点
- 多工具协同作业：通过 6 轮 MCP 工具调用完成景点检索→定位→路线串联全流程
- 结构化输出：自动生成含门票价格、交通耗时、美食推荐的全要素攻略（实测生成三天武汉游完整方案）


技术突破点：

- 讯飞星火 X1 展现强大任务拆解能力，自主规划 maps_text_search→maps_geo 工具调用链路。
- 在国产算力支持下实现复杂指令跟随（严格匹配 MCP 服务器参数规范）


实际演示与工作流讲解

![Image](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6810de7ca70f521eb3060434/9715c290-a81d-4f09-946f-8eb6b741bb20.png)

星火 X1 给出的这份“非特种兵版”武汉旅游攻略挺不错的，武汉的主要景点黄鹤楼、湖北省博、东湖、江汉路步行街等等都给出来了，并且也给出了景点的门票价格，经典之间的交通方式和交通花费时间，甚至也给出了美食攻略。我们来看下星火 X1 是如何使用 MCP 来完成这份旅游攻略的呢？

旅游 Agent 的整体结构如下所示，MCP 的选择和使用部分都在 Agent 节点进行处理。

![Image](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6810de7ca70f521eb3060434/8c2f87f5-287b-478a-a7a8-815cfa71d38a.png)

星火 X1 进行了六轮迭代调用，我们看看星火 X1 都做了什么吧～

![Image](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6810de7ca70f521eb3060434/93d192cb-81fd-4329-a435-73ad4ae647dd.png)

第一步：使用 MCP 服务器中的 maps_text_search 工具查询武汉的热门景点有哪些。

![Image](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6810de7ca70f521eb3060434/6a4dee14-cb4b-49ed-9486-4c307d4945e3.png)

第二步：使用 MCP 服务器中的 maps_geo 工具获取黄鹤楼的具体地点。

![Image](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6810de7ca70f521eb3060434/6a426441-9fdf-4abc-a00e-a5a312ca2a9f.png)

第三步：使用 MCP 服务器中的 maps_geo 工具获取湖北省博的具体地点。

![Image](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6810de7ca70f521eb3060434/8f84b308-b6ca-4136-b496-19631869f9c6.png)

第四步：使用 MCP 服务器中的 maps_geo 工具获取东湖听涛区的具体地点。

![Image](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6810de7ca70f521eb3060434/9c9b628b-48df-41d4-a3e3-f7b6b6ac6213.png)

第五步：使用 MCP 服务器中的 maps_geo 工具获取汉口江滩的具体地点。

![Image](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6810de7ca70f521eb3060434/fd733a15-3ae0-4d99-95c7-b444fca9af79.png)

最后一步：整理以上的位置信息，制定武汉旅游攻略！

![Image](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6810de7ca70f521eb3060434/df16bac9-6f9c-4e7a-9391-d37387aa6c7c.png)

星火 X1 首先搜索武汉所有的热门景点，然后从中挑选了四个主要景点进行旅行规划，在最后的调用中整合前面得到的景点信息，星火 X1 制定了一份近乎完美的武汉三天非特种兵版旅行攻略。

制定一份这样的攻略需要模型具备很强的规划能力（合适的 MCP 工具调用顺序）、逻辑推理能力（理解用户的需求）、指令跟随能力（按照 MCP 服务器的参数进行调用）等等。综合来说星火 X1 的数学、代码、逻辑推理、文本生成、语言理解、知识问答能力提升，实至名归！

👍

动手能力强的小伙伴可以在 Dify 平台直接导入这份旅行攻略大师的 DSL 文件自行体验～

需要去高德地图开放平台获取一个 Key 哦～

https://lbs.amap.com/api/mcp-server/create-project-and-key

## Multi-Agent 多智能体：你的 AI 导游天团

角色-任务-大模型能力对照表：

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6810de7ca70f521eb3060434/f1424849-b268-4604-bcb9-efb4512bc45f.png)

实际演示与完整工作流讲解教程

## 讯飞星火X1：规划师和导游团的 AI 大脑

根据前几天官方的介绍，讯飞星火 X1 在数学、代码、逻辑推理、文本生成、语言理解、知识问答等通用任务效果显著提升，在模型参数比业界同类模型小一个数量级的情况下，整体效果对标 OpenAI o1 和 DeepSeek R1，再次证明了基于国产算力训练的全栈自主可控大模型具备登顶业界最高水平的实力和持续创新的潜力。

![Image](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6810de7ca70f521eb3060434/c6d4fc86-0630-44a1-b7d8-394a734b6cac.png)

在算力困局加剧、芯片技术"卡脖子"风险持续攀升的特殊时期，每一项基于国产算力的自研AI大模型突破都值得密切关注。

在 MCP 和 多智能体的场景下，讯飞星火 X1 作为两个系统的大脑，真正做到了：

- 精准理解用户没说出口的需求
- 智能协调多个工具 / 数据源
- 动态生成带人情味的方案
- 应对突发情况灵活调整


从今天起，你的每次旅程都是中国 AI 技术的里程碑。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6810de7ca70f521eb3060434/65cea995-ac44-4614-9b87-20082586602b.webp)

开源贡献，**点赞**在看↓


新枝标签： #llm
