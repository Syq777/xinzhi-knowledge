---
作者:
  - "腾讯云开发者"
原文链接: https://mp.weixin.qq.com/s?__biz=MzI2NDU4OTExOQ==&amp;mid=2247691827&amp;idx=1&amp;sn=b9d42b56b1f3edb43bbe7c8a96845d75&amp;chksm=eb829b876033e52e3e5d13600390d190005b9dea0351eaa26e2f030d91a4f622bb32ddf1c8a6&amp;mpshare=1&amp;scene=1&amp;srcid=0819G0o6O5a0l9kk25HTrn4q&amp;sharer_shareinfo=582ae442c166483ad99a5060d7d4deb1&amp;sharer_shareinfo_first=582ae442c166483ad99a5060d7d4deb1#rd
发布时间: ""
收藏时间: "2025-08-19"
关联日记: "[[2025-08-19]]"
tags:
  - 文章
---
![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68a3d74ee38d7338d585632c/13fc7926-7c0a-4701-9e6e-959fae7883ac.webp)

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68a3d74ee38d7338d585632c/0faac4ae-1598-4a60-807f-5023a6263bfb.gif)

👉目录

1 LLM (大语言模型)

2 Transformer (自注意力机制)

3 Prompt (提示词)

4 理解API

5 Function Calling (函数调用)

6 Agent (智能体)

7 MCP (模型上下文协议)

8 A2A (Agent通信协议)

9 未来假想

本文尽量用最简单的方式, 帮读者理解 LLM, Transformer, Prompt, Function calling, MCP, Agent, A2A 等这些基本概念。表述时不追求绝对准确, 尽量通俗易懂。部分内容有个人理解的成份, 内容难免疏漏, 欢迎指正。注意: 本文需要你有基本的代码阅读能力。当然非开发阅读也不会很困难。关注腾讯云开发者，一手技术干货提前解锁👇鹅厂程序员面对面直播继续，这次将邀请鹅厂大佬讲讲自己从大专到腾讯的心路历程。更有蛇年公仔等精美周边等你来拿，记得提前预约直播～👇

## 01

LLM (大语言模型)

本质就是文字接龙。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68a3d74ee38d7338d585632c/978b1023-cfa4-47a0-b45b-1915174c188b.png)

把问题当成输入，把大模型当成函数，把回答当成输出。

大模型回答问题的过程，就是一个循环执行函数的过程。

另外有必要了解一下，AI技术爆发于2023年，ChatGPT经过了几次迭代才崭露头角。

- Transformer架构。
- 参数爆发增长。
- 人工干预奖励模型。


思考题: 语言能代表智能吗?

## 02

Transformer (自注意力机制)

自注意力机制就是动态关联上下文的能力。如何实现的呢？

- 每个分词就是一个 token
- 每个token 都有一个 Q, K, V 向量 (参数)
- Q 是查询向量
- K 是线索向量
- V 是答案向量
- 推理的过程:
- 当前token 的Q 与 前面所有的 K 计算权重
- 每个 token 的V加权相加得到一个 token预测值
- 选择 N 个与预测值最接近的 token, 掷骰子选择


最简化示例: 小明吃完冰淇淋，结果 => 肚子疼。

首先分词及每个token的 Q, K, V向量。

tokenQ（查询）K（键）V（值）语义解释小明[0.2, 0.3][0.5, -0.1][0.1, 0.4]人物主体吃完[-0.4, 0.6][0.3, 0.8][-0.2, 0.5]动作（吃完）冰淇淋[0.7, -0.5][-0.6, 0.9][0.9, -0.3]食物（冷饮，可能致腹泻）结果[0.8, 0.2][0.2, -0.7][0.4, 0.1]结果（需关联原因）

接着开始推理:

###### 1. 使用最后一个 token 的 Q（“结果”的 Q 向量）

Q_current = [0.8, 0.2]

###### 2. 计算 Q_current 与所有 K 的点积（相似度）

点积公式：Q·K = q₁*k₁ + q₂*k₂

TokenK向量点积计算结果小明[0.5, -0.1]0.8 * 0.5 + 0.2*(-0.1) = 0.4 - 0.020.38吃完[0.3, 0.8]0.8 * 0.3 + 0.2 * 0.8 = 0.24 + 0.160.4冰淇淋[-0.6, 0.9]0.8*(-0.6) + 0.2 * 0.9 = -0.48 + 0.18-0.3结果[0.2, -0.7]0.8 * 0.2 + 0.2*(-0.7) = 0.16 - 0.140.02

###### 3. Softmax 归一化得到注意力权重

将点积结果输入 Softmax 函数 

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68a3d74ee38d7338d585632c/89ca6bc9-4da7-4938-bd1f-006a2434c428.png)

Token点积指数值（e^x）权重小明0.38e^0.38 ≈ 1.461.46 / 2.74 ≈ 0.53吃完0.4e^0.40 ≈ 1.491.49 / 2.74 ≈ 0.54冰淇淋-0.3e^-0.30 ≈ 0.740.74 / 2.74 ≈ 0.27结果0.02e^0.02 ≈ 1.021.02 / 2.74 ≈ 0.37

4. 加权求和 V 向量生成上下文向量

将权重与对应 V 向量相乘后相加：

Token权重V向量加权 V 向量小明0.53[0.1, 0.4]0.53*[0.1, 0.4] ≈ [0.053, 0.212]吃完0.54[-0.2, 0.5]0.54*[-0.2, 0.5] ≈ [-0.108, 0.27]冰淇淋0.27[0.9, -0.3]0.27*[0.9, -0.3] ≈ [0.243, -0.081]结果0.37[0.4, 0.1]0.37*[0.4, 0.1] ≈ [0.148, 0.037]

最终上下文向量：

[0.053−0.108+0.243+0.148,0.212+0.27−0.081+0.037]=[0.336,0.438]

5. 预测下一个 token

模型将上下文向量 [0.336, 0.438] 与候选 token 的嵌入向量对比：

嵌入向量不作过多解释, 只要知道QKV三个向量可从嵌入向量计算得到即可

候选词嵌入向量相似度（点积）概率肚子疼[0.3, 0.5]0.336 * 0.3 + 0.438 * 0.5 ≈ 0.101 + 0.219 = 0.320最大概率（例如 65%）头疼[0.2, 0.1]0.336 * 0.2 + 0.438 * 0.1 ≈ 0.067 + 0.044 = 0.111次之（例如 20%）开心[-0.5, 0.8]0.336*(-0.5) + 0.438 * 0.8 ≈ -0.168 + 0.350 = 0.182较低（例如 15%）

最终模型选择最高概率的 “肚子疼” 作为下一个 token。

注意在实际场景中，预测的下一个token是不确定的，是因为有一个掷骰子的操作，大模型会在概率最大的几个token中随机挑选一个作为最终输出。

## 03

Prompt (提示词)

对于这个词大家并不陌生。我们用chatGPT时经常会用到， "你是一个......."

但你真的理解它吗？

与ai对话时的这种预设角色，其实并不是严格意义上的 prompt。

为什么这么说呢？先看一下API。

## 04

理解API

我们前面提到过大语言模型的 本质就是文字接龙，相对应的使用大模型也比较简单。可以参见deepseek的文字接龙 api 请求：

https://api-docs.deepseek.com/zh-cn/api/create-chat-completion

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68a3d74ee38d7338d585632c/55de6841-50a2-480b-aefd-a057d7247860.png)

这里比较重要的几个部分，需要理解:

1. temperature 温度

Temperature（温度） 是一个控制生成文本随机性和多样性的关键参数。它通过调整模型输出的概率分布，直接影响生成内容的“保守”或“冒险”程度。看几个典型场景:

场景温度代码生成/数学解题0数据抽取/分析1通用对话1.3翻译1.3创意类写作/诗歌创作1.5

2. tools 工具支持

大模型对 function calling 的支持，后面再详细介绍。

3. 角色和信息

这一部分是ai对话的主体。其中role 定义了四个角色。

- system 系统设定。
- user 用户回复。
- assistant 模型回答。
- tool 是配合function call工作的角色，可以调用外部工具。


回到前一章的问题，ai对话时其实是user部分输入的内容，所以system角色的设定内容才应该是严格意义上的Prompt。

这有啥区别呢? (user 与 system?)

个人一个合理的猜测: system的内容在Transformer推理中拥有较高的权重。所以拥有较高的响应优先级。

4. 关于多轮对话

因为LLM是无状态的。我们要时刻记得文字接龙的游戏，因此在实际操作中也是这样的。

- 在第一轮请求时，传递给 API 的 messages 为。


![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68a3d74ee38d7338d585632c/738f74ef-2802-4bb6-8465-23c06e73a86d.png)

- 大模型回答。


![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68a3d74ee38d7338d585632c/ca9c424a-c8c6-41f9-9f92-7428f49d7719.png)

- 当用户发起第二轮问题时，请求变成了这样


![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68a3d74ee38d7338d585632c/5eb079a0-9d1f-4fb3-be6a-914dbcf6a436.png)

## 05

Function Calling (函数调用)

仅仅一个可以回答问题的机器人，作用并不太大。

要完成复杂的任务，就需要大模型的输出是稳定的，而且是可编程的。

因此OpenAI 推出了 function calling的支持。也就是前面提到的 tools参数相关内容。

1. 基本流程

- 工具声明及用户输入


![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68a3d74ee38d7338d585632c/a0695c2d-38ee-439c-8d1d-83ef41901814.png)

- 模型检测到需要使用工具，返回相关工具参数


![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68a3d74ee38d7338d585632c/2083ad1f-a9d2-46fd-9c1d-72388f5091ba.png)

- 开发者根据方法名和参数，调用相关工具方法


![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68a3d74ee38d7338d585632c/3d5e360e-2b0b-4c60-a868-3b304fe5f4e0.png)

- 将工具方法的返回值，附加到请求中，再次请求大模型


![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68a3d74ee38d7338d585632c/63597924-cb4f-4c48-91b1-aeddc359134f.png)

- 得出最终结果


```
"The current temperature in Paris is 14°C (57.2°F)."
```

- 总结一下


![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68a3d74ee38d7338d585632c/c887191b-7b3e-4d61-afc6-033fb07dc7df.png)

2. 实现原理(猜测)

a. 实现方式一: prompt 遵循 (示例)

提前设置规则: 

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68a3d74ee38d7338d585632c/84020789-9a0d-44da-a23d-f4689cead0b3.png)

b. 实现方式二: 模型训练特定优化

对结构化输出有特定要求，可能需要特定训练吧。这个不太确定?

## 06

Agent (智能体)

包含: 大模型，任务规划，上下文记忆，工具调用。它是大模型能力的拓展。其实只要对API进行简单的封装，只要能完成特定任务，都可以称为智能体。比如下面的例子:

1. 创建AI客服系统

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68a3d74ee38d7338d585632c/f2dea496-a317-4738-9fa3-aaeadcaec7ab.png)

这个智能体，主要包括:

1. 配置了一个 prompt: "你是一个电商客服，可查询订单状态"
2. 引入 query_order 工具


2. 其它创建方式

服务商开放接口，供用户创建，比如腾讯元器：

https://yuanqi.tencent.com/my-creation/agent

一个简单的提示词都可以创建智能体：

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68a3d74ee38d7338d585632c/9adb5d60-6767-4b97-8d75-f45ca8a405df.png)

## 07

MCP (模型上下文协议)

通过上面的智能体调用工具的示例我们可以看到，每接入一个工具，都需要编写相应的接入代码。经常写代码的我们都知道，这不是好的架构设计。 好的设计应该把动态改变的部分 ( tools的声名和调用分离出来 )，做为一个独立的模块来拓展。这就有了大众追捧的 MCP: -----(哪有这么玄，都是程序员的常规操作啊....)

MCP是工具接入的标准化协议

https://modelcontextprotocol.io/introduction

遵循这套协议，可以实现工具与Agent的解耦。你的Agent 接入MCP协议的client sdk后。接入工具不再需要编写工具调用代码，只需要注册 MCP Server就可以了。而MCP Server可由各个服务商独立提供。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68a3d74ee38d7338d585632c/9401a4c0-1aab-4a2a-a723-4eb6099def84.png)

MCP Server做什么呢? 

1. 声明提供的能力 ListTools。
2. 调用能力的方式 CallTool。


来看一下MCP Server的部分代码 (红框中就是做上面两个事，不难理解) :

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68a3d74ee38d7338d585632c/0541a62f-51b4-46a0-a25f-eb9242303c91.png)

## 08

A2A (Agent通信协议)

A2A本质是对 MCP协议的拓展，按字面意思就是 Agent to Agent. 有兴趣的自己详细看吧。

智能体与智能体之间通信的标准化协议

https://github.com/google/A2A?tab=readme-ov-file#agent2agent-a2a-protocol

在这套协议下，一个智能体要引入其它的智能体的能力，也变得可插拔了。

## 09

未来假想

如同蒸汽机，电，计算机这些伟大的技术一样。AI会成为下一个彻底改变人类生活工作方式的新技术。

1. 现在AI编程能力越来越强，程序员是不是要失业了?

职业不会消失，消失的只有人。但是AI编程的确会重塑整个行业。

我预想几年后，纯粹的业务代码工程师可能会消失。而会增加更多的AI编程工程师。

AI编程工程师的职责是解决AI模糊性的问题。而工具的引入就是增加确定性的手段。

我们程序员可以把自己的积累通过 mcp server的方式，挂载到项目agent 上去。这样我们就可以解放双手，去解决更多有挑战性的问题。

2. 当前我们有哪些工作可以由AI来处理?

理论上一切重复性的工作都可以交由AI完成。保险起见，创造性的工作暂时可以只作为参考。

- 日常的反馈分析。
- 团队知识库。
- 个人知识库。


-End-

原创作者｜马培羽

感谢你读到这里，不如关注一下？👇

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68a3d74ee38d7338d585632c/0d0d45f2-8aa7-4fa2-bf30-70ce27f6d494.webp)

未来五年，“AI 编程工程师”真的会出现吗？欢迎评论留言补充。我们将选取1则优质的评论，送出腾讯云定制文件袋套装1个（见下图）。8月26日中午12点开奖。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68a3d74ee38d7338d585632c/708608f1-5d39-4912-afbf-b3067761c1b7.webp)

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68a3d74ee38d7338d585632c/d3d29a2a-98c0-49d2-adb5-a2d81aab7932.webp)

[![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68a3d74ee38d7338d585632c/909b0f32-ca52-41ee-b348-c4fdd3aeb205.png)](https://mp.weixin.qq.com/s?__biz=MzI2NDU4OTExOQ==&mid=2247691279&idx=1&sn=5da2fbe1159f12e45d3d7f4b673a0108&scene=21#wechat_redirect)

[![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68a3d74ee38d7338d585632c/21ab9370-558c-411b-9e58-18699b8ac0f8.png)](https://mp.weixin.qq.com/s?__biz=MzI2NDU4OTExOQ==&mid=2247691682&idx=1&sn=8eac13cc848ee0779e1a4ab85142d87a&scene=21#wechat_redirect)

[![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68a3d74ee38d7338d585632c/812350e6-b3b2-4b25-a0e5-93bf2e86b45b.png)](https://mp.weixin.qq.com/s?__biz=MzI2NDU4OTExOQ==&mid=2247691610&idx=1&sn=99c2ab7608d2ed7edc1e1aa029dd08ed&scene=21#wechat_redirect)

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68a3d74ee38d7338d585632c/e7d1e269-317e-4314-a0c1-e9297e437436.webp)


新枝标签： #llm
