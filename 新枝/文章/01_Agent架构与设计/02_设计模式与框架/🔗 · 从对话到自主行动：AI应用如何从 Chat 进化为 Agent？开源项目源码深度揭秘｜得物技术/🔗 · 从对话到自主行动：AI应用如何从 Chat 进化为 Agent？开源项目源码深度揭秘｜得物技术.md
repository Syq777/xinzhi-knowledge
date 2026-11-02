---
作者:
  - "得物技术"
原文链接: https://mp.weixin.qq.com/s?__biz=MzkxNTE3ODU0NA==&amp;mid=2247538302&amp;idx=1&amp;sn=f85057dbe21821f68f9d9cd3b72fb8cb&amp;chksm=c02953b110fea8c2268853a14e41ad462e492842871fcb2a1db74d7b6873179e88838d1ae708&amp;mpshare=1&amp;scene=1&amp;srcid=0415vnntC84dsy79Nhz6YVxJ&amp;sharer_shareinfo=2dfd34e8a5be64ede5294addd90dfce6&amp;sharer_shareinfo_first=2dfd34e8a5be64ede5294addd90dfce6#rd
发布时间: ""
收藏时间: "2025-04-15"
关联日记: "[[2025-04-15]]"
tags:
  - 文章
---
**目录**

一、引言

二、以「对话为中心」的ChatBot

三、以「交付为中心」的多智能体Agent

三、什么是智能体Agent

1. 从Prompt到思维链

2. ReAct架构

3. Agent

4. Manus：一个Agent典型案例

5.大模型上下文协议（MCP）

四、智能体Agent实现的源码剖析（OpenManus项目）

1. 准备

2. 代码

五、总结

**一**

**引言**

从2022年12月份OpenAI发布ChatGPT产品至今已有2年多的时间，当大家已经习惯于在对话框中与AI交互，习惯于通过各种Prompt技巧让AI更好的理解并回答我们的问题，似乎默认这就是一种比较好与AI的交互方式了。

然而，这就是我们期盼的与AI交互的形式嘛？这是一种高效的方式嘛？

显然，这是不够的。

我们期望的是：**告诉AI我们想要的目标或者任务，AI能够理解深度理解并分析我们的意图、自动的进行任务的拆解、自动的寻找可以使用的工具、自动的进行结果数据的汇总过滤、自动的呈现符合任务的展示形式。同时在任务处理过程中，可以自己完成异常的检测和修改。**就如同一位优秀的同学，我们告诉他任务的目标，他可以自己寻找飞书文档、搜索网络知识、使用内部系统、自己编码验证方案可行性，并最终给一份好的解决方案。

**二**

**以「对话为中心」的ChatBot**

我们发送一条指令，AI被动的响应指令。即完成一轮人与AI的交互。

**三**

**以「交付为中心」的多智能体Agent**

我们发送一个任务，AI自动分析任务、调用可用的工具、分析结果、过滤数据并自动处理异常，最终呈现解决方案。

完成这样的一个任务，需要多智能体Agent间的协作以及对常用工具的调用。那什么是智能体Agent呢？

**四**

**什么是智能体Agent**

**从Prompt到思维链**

随着大模型的发展，Prompt工程已成为撬动大模型潜能的核心技术。即使我们普通用户在与大模型的交互中，也通过角色定义（如"资深工程师"）或示例引导来优化输出效果，但这类简单提示往往难以突破模型固有的逻辑天花板——就像给赛车装自行车轮胎，再怎么调整也难以突破速度极限。

但偶然间，人们发现了一个神奇的咒语：只需要告诉大模型，**你的 think 要 step by step**。研究者发现只要加了这个prompt，就能极为显著地改善大模型做数学题的正确率。

大模型的数学与逻辑能力短板，是所有体验过其对话功能的用户都能直观感受到的痛点。这一缺陷严重制约了大模型的商业化落地进程，毕竟没有人敢轻易信任一个逻辑混乱的智能系统能输出可靠的决策结果。于是，提升大模型数学能力，被所有做基础模型的公司当作了第一目标。

研究者试图通过强化思维链来突破这一瓶颈。一个直观的思路是：让模型像人类解题时在草稿纸上推演那样，通过 "step by step" 的方式展开逻辑链条 —— 在这个过程中，包含假设、演绎、反思、纠错等一系列思维活动。既然人类通过这种结构化的思考方式能够有效解决数学问题，那么大模型是否也能通过类似机制实现能力跃迁？这一猜想推动着研究向纵深发展，最终形成了思维链技术的核心框架。这样的观念经过继续钻研，最终就构成了思维链，思维链是一个能以最小的代价，而非常显著提升模型智力水平（逻辑能力、解题能力、代码能力）的技术。

值得注意的是，2025 年春节期间引发广泛关注的 DeepSeek 大模型，正是思维链技术的成功实践典范。尽管 DeepSeek 并非首创者，但其通过创新性地融合混合专家（MoE）架构与强化学习技术，显著提升了思维链推理的计算效率与性能表现。这种技术优化使得 DeepSeek 在保持高精度推理的同时，大幅降低了计算成本，最终实现了屠榜级表现。

**ReAct架构**

如果说思维链（COT）是给 AI 装上了人类的 "草稿纸"，那么 ReAct 框架就是为它配备了 "双手"—— 让 AI 不仅能在脑子里推演，还能主动采取行动获取信息。这种 "思考 + 行动" 的组合，正在把大模型从 "纸上谈兵" 的理论家，变成能解决现实问题的实干家。

ReAct 的核心在于将**推理（Reasoning）与行动（Action）**紧密结合。当模型面对复杂问题时，会先像人类一样拆解思考步骤，然后根据中间结果调用外部工具（如搜索引擎、数据库、计算器）获取实时数据，再把这些信息整合到后续推理中。

其实，实现一个ReAct很简单，只需要构建Prompt+提供工具+循环执行即可，笔者在这里不进行详细的介绍，只需要给一个Prompt例子，读者就能理解：

> 尽可能最好地为用户回答接下来的问题，你可以使用以下工具来辅助你：{tools} 使用以下格式：- 问题：你需要回答的输入问题- 思考：你需要持续思考下一步采取什么行动 - 行动：要采取的行动，应该是 [{tool_names}] 中的一个，以及该行动的输入内容 - 观察：行动并观测结果，并判断结果是否合理 ...（这个思考 / 行动 / 观察可以重复 N 次，直到你认为知道了最终答案 - 最终答案：原始输入问题的最终答案 开始！ - 问题：{input}

Tools支持开发者自定义，比如给予LLM一个查询天气的接口、计算器接口等。

ReAct架构实现了一种**"问题拆解-工具调用-结果整合"**的**闭环机制**，使得开发者仅需通过定义工具集（如天气API、计算器、知识图谱接口）和设计任务引导词，就能将大模型转化为可执行多步骤决策的智能体。最终可以使大模型突破纯文本推理的局限，真正具备了在动态场景中解决开放性问题的工程化能力。

**Agent**

Agent作为大模型技术的集大成者，通过整合思维链（CoT）的推理能力和ReAct框架的行动机制，构建了具备自主决策与执行能力的智能系统。其核心突破在于将**“大脑”与“四肢”**有机统一，标志着大模型从被动应答迈向主动干预现实的质变。

在架构上，Agent与ReAct差别不大，ReAct是Agent的核心实现范式之一，Agent**进一步整合**记忆存储、多智能体协作等模块，形成更完整的自主决策系统。下图是一个简单的Agent架构图：

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67fdee3c837e6d7463760840/30b43563-e576-4b61-a15d-b2f8eb39cdf2.png)

**Agent处理流程**

1-4步会循环进行，直到LLM认为问题已被回答。

**1.规划（Planning）：**

- 定义：规划是Agent的思维模型，负责拆解复杂任务为可执行的子任务，并评估执行策略。
- 实现方式：通过大模型提示工程（如ReAct、CoT推理模式）实现，使Agent能够**精准拆解任务**，分步解决。


**2.记忆（Memory）：**

- 定义：记忆即信息存储与回忆，包括短期记忆和长期记忆。
- 实现方式：**短期记忆**用于存储会话上下文，支持多轮对话；**长期记忆**则存储用户特征、业务数据等，通常通过向量数据库等技术实现快速存取。


**3.工具（Tools）：**

- 定义：工具是Agent感知环境、执行决策的辅助手段，如API调用、插件扩展等。
- 实现方式：通过接入外部工具（如API、插件）扩展Agent的能力，如ChatPDF解析文档、Midjourney文生图等。


**4.行动（Action）：**

- 定义：行动是Agent将规划与记忆转化为具体输出的过程，包括与外部环境的互动或工具调用。
- 实现方式：**Agent根据规划与记忆执行具体行动**，如智能客服回复、查询天气预报、AI机器人抓起物体等。


**Manus：一个Agent典型案例**

在读完前一节关于智能体（Agent）的技术解析后，读者也许会认为这类系统的工程实现并非难事，实际上也确实是这样。近期爆火的 Agent 产品 Manus 便是典型案例。当用户提出 "定制 7 天日本旅行计划" 的需求时，Manus 能够基于目标，自主进行网络搜索并将信息整合，展现出**高度拟人化的任务执行逻辑**。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67fdee3c837e6d7463760840/30a143b8-ddcf-46ab-aa07-f932b1c66dc3.png)

尽管 Manus 目前尚未向普通用户开放，且采用邀请制注册的封闭运营模式，但其通过官方演示视频呈现的强大智能化表现，已在技术圈引发广泛关注。值得关注的是，随着Agent技术的热度攀升，开源社区已迅速涌现出 OpenManus、OWL 等多个复刻项目。

因为Manus并非开源，我们很难了解其技术细节。但好在：

1. "Manus 的部分技术细节，包括其提示词设计、运行机制等内容被网友通过非官方渠道披露，感兴趣的读者可自行查阅相关公开资料。
2. 我们可以了解一下**大模型上下文协议**（Model Context Protocol，MCP），这是 Anthropic (Claude) 主导发布的一个开放的、通用的、有共识的协议标准，虽然Manus不一定用了这个协议，但目前一些相关开源项目也是基于MCP的，本文会在下面介绍MCP。
3. 目前已有复刻的开源项目Openmanus，笔者会在接下来的章节剖析其源码。


**大模型上下文协议（MCP）**

**MCP是做什么的？**

MCP（Model Context Protocol）作为一项开放协议，旨在为应用程序与大型语言模型（LLMs）之间的上下文交互提供标准化框架。其设计理念可类比为数字时代的 "USB-C 接口"—— 正如 USB-C 统一了设备与外设的连接标准，MCP 通过标准化的上下文交互接口，实现了 AI 模型与多样化数据源、工具之间的无缝对接。

如下图所示，图中的MCP server都可以看成一个个工具(如搜索引擎、天气查询)，通过“接口”连接到MCP clients(大模型)上，大模型可以使用各种MCP server来更好地处理用户的问题。

此外，下游工具的开发者也可以更好的开发其工具，目前在MCP官网即可了解其各种编程语言的SDK和相关概念。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67fdee3c837e6d7463760840/d0b2339a-f0af-4b60-9c92-de0a6cc0ff68.png)

**MCP架构**

MCP 的核心采用客户端-服务器架构，其中 host 可以连接到多个服务器，读者简单看看即可：

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67fdee3c837e6d7463760840/11881d1c-4db0-4876-b597-f5a276bac1a3.png)

- MCP 主机（MCP Hosts）：指需要通过 MCP 协议获取数据的应用程序，涵盖 AI 开发工具（如 Claude Desktop）、集成开发环境（IDEs）等智能应用场景。
- MCP 客户端（MCP Clients）：作为协议的执行者，每个客户端与对应的 MCP 服务器建立一对一的专属连接，负责协议层面的通信交互。
- MCP 服务器（MCP Servers）：轻量化的功能载体，通过标准化的 Model Context Protocol 对外开放特定能力，可视为连接模型与工具的智能桥梁。
- 本地化数据源（Local Data Sources）：包括服务器可安全访问的本地文件系统、数据库及专有服务，构成数据交互的近端生态。
- 远程服务（Remote Services）：通过互联网连接的外部系统，例如各类 API 接口服务，拓展了模型的能力边界。


**为什么要用MCP？**

从技术演进视角看，MCP 的诞生是提示工程（Prompt Engineering）发展的必然产物。研究表明，结构化的上下文信息能显著提升大模型的任务表现。在传统提示工程中，我们往往需要人工从数据库筛选信息或通过工具检索相关内容，再手动将这些信息注入提示词。然而，随着复杂任务场景的增多，这种手工注入信息的操作变得愈发繁琐且低效。

为解决这一痛点，主流大模型平台（如 OpenAI、Google）先后引入了**函数调用（Function Call）机制**。该机制允许模型在推理过程中主动调用预定义函数获取数据或执行操作，极大提升了自动化水平。然而，函数调用机制存在显著局限性：其一，不同平台的函数调用 API 存在较大差异，例如 **OpenAI 与 Google 的实现方式互不兼容**，开发者在切换模型时需重新编写代码，徒增适配成本；其二，该机制在安全性、交互性及复杂场景的扩展性方面仍存在优化空间。

在此背景下，MCP 协议通过标准化的上下文交互接口，为大模型构建了更具普适性的工具调用框架。它不仅**解耦**了模型与工具的依赖关系，还通过统一的协议规范解决了跨平台兼容性问题。更重要的是，MCP 将上下文管理提升到系统架构层面，为大模型在复杂业务场景中的深度应用提供了可扩展的技术底座。这种从碎片化的提示工程到体系化的上下文协议的演进，标志着大模型应用正在向更高效、更规范的方向迈进。

**四**

**智能体Agent实现的源码剖析（OpenManus项目）**

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67fdee3c837e6d7463760840/ee6e2919-0560-4ce1-844e-32d572601297.png)

OpenManus 是一个基于 MCP 协议的开源智能体实现项目，旨在通过标准化的上下文协议实现大模型与工具的高效协同。当前项目仍处于快速迭代阶段，本文以其 2025 年 3 月 12 日的版本为分析对象。选择该项目的原因如下：

- **团队背景与代码质量**：项目作者来自MetaGPT，具备深厚的工程经验，代码结构清晰且注释完善，兼顾了技术实现与可读性。
- **部署便捷性**：只需通过虚拟环境安装依赖并配置大模型 API Key（如 OpenAI 的 API 密钥），即可快速启动，降低了技术门槛。
- **技术前沿性**：项目紧跟大模型技术发展，且目前仍在不断迭代的过程中。


在经过前面对相关概念的讨论，我们可以得知实现Agent有几个关键的点，读者可以带着问题在项目中寻找答案：

- **Prompt**：其结构化的Prompt是什么样的？通过Prompt可以对其架构有一个初步认识。
- **OpenManus**：怎么通过大模型思考和处理问题？
- **工具相关**：怎么进行工具注册、工具管理的？工具执行逻辑是什么的？


**准备**

项目地址：

https://github.com/mannaandpoem/OpenManus/tree/main

**构建环境**

**创建一个python=3.12的虚拟环境**

- 笔者测试了一下，非3.12版本会有一个package不兼容。
- 可以用conda或python内置的uv，项目文档提供了详细的指令。


**安装playwright**

- 如果第一次使用，需要安装playwright。


```
playwright install
## 或者
python -m playwright install
## 以上命令会安装所有浏览器，如果只需要安装一个浏览器比如firefox
python -m playwright install firefox
```

**配置大模型API Key**

- 可以用DeepSeek或通义千问的API Key，其中通义有免费额度，DeepSeek虽然收费但价格便宜，测试一次使用约1000token,成本不到0.01元。
- 根据项目文档配置cofig.yaml即可，但项目调用大模型是使用基础的OpenAI API，如果使用其他大模型，可能需要基于对应的官方文档小改一下。


**代码**

**OpenManus客户端**

**Python OpenManus/main.py**即可在终端运行OpenManus，读者也可以尝试其Web版本。

- 具体会调用20行代码，执行Manus类的方法run()。


![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67fdee3c837e6d7463760840/fdf02422-db29-490e-8e7e-129867b856cf.png)

进入OpenManus/app/agent/manus.py查看Manus类，可以发现它继承了ToolCallAgent类，再进入会发现又是继承，有点复杂，这里我画一张关系图。

- act()执行时使用execute_tools()进行具体的工具执行。
- 总体来说，Manus类定义了Prompt和可使用的工具。
- Base类定义了run()，在run()中会循环执行ReAct类的方法step()，直到Finish或达到max_step。
- step()类会顺序执行ToolCallAgent类的think()和act()。


当然，这里只罗列了重要的组件和方法，一些方法没有画在图中。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67fdee3c837e6d7463760840/1ee0d6a7-5cb7-46c8-83de-f359f01a6471.jpeg)

**Prompt**

一般来说，输入给LLM的prompt分为两种：1）**系统 prompt**，用于定义模型的角色定位和行为规则；2）**用户 prompt**(OpenManus称为Next Step Prompt)，用于传达具体的任务指令或信息需求。

在OpenManus/app/prompt/manus.py中即可看到Manus的Prompt，这里展示一下中文版，读者基于此可对OpenManus架构有一个初步认识：

- **系统Prompt（SYSTEM_PROMPT）**：“你是 OpenManus，一个全能的人工智能助手，旨在解决用户提出的任何任务。你拥有各种可使用的工具，能调用这些工具高效地完成复杂的请求。无论是编程、信息检索、文件处理还是网页浏览，你都能应对自如。”
- **下一步Prompt（NEXT_STEP_PROMPT）**：“你可以使用 PythonExecute 与计算机进行交互，通过 FileSaver 保存重要的内容和信息文件，使用 BrowserUseTool 打开浏览器，并使用 GoogleSearch 检索信息。根据用户的需求，主动选择最合适的工具或工具组合。对于复杂的任务，你可以将问题分解，逐步使用不同的工具来解决它。在使用完每个工具后，清晰地解释执行结果并给出下一步的建议。


当然，在实际执行时会对prompt有进一步优化，不过核心的系统定位与任务指导原则是不会改变的。

**Manus类**

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67fdee3c837e6d7463760840/bedd38fd-7b69-4d28-a697-d4acc91d1e64.png)

我们先看一下OpenManus拥有的工具，工具也支持自定义，会在后文进行介绍。

- PythonExecute：执行 Python 代码以与计算机系统交互、进行数据处理、自动化任务等等。
- FileSaver：在本地保存文件，例如 txt、py、html 等文件。
- BrowserUseTool：打开、浏览并使用网络浏览器。如果你打开一个本地 HTML 文件，必须提供该文件的绝对路径。
- GoogleSearch：执行网络信息检索。
- Terminate：如果LLM认为回答完毕，会调用这个工具终止循环。


**Base类**

**run()**

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67fdee3c837e6d7463760840/ae4b89d7-1a51-4c1f-ae9a-1a2325a68562.png)

- 首先，输入的request就是用户输入的提问。


**状态管理**

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67fdee3c837e6d7463760840/13cd5e1f-043d-4f02-a300-7ccdafe79363.png)

- 执行时首先检查代理的当前状态是否为` IDLE`（空闲状态）。如果不是空闲状态，会抛出` RuntimeError `异常，因为只有在空闲状态下才能启动代理的执行。


![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67fdee3c837e6d7463760840/15d241d9-6f34-4c7b-918a-1305f456bc53.png)

- 当进入循环时前，使用 `state_context`上下文管理器将代理的状态临时切换到 `RUNNING`（运行状态）。在上下文管理器中执行的代码块会**在进入时**将状态切换为指定状态，**在退出时**恢复到之前的状态。如果在执行过程中**发生异常**，会将状态切换为 `ERROR`。


**Memory管理**

我们调用大模型的API，本质是向大模型提供方发http请求，http请求是无状态的。

- 也就是说，服务端不会保留任何会话信息。对于每次都完成一个独立的任务，无状态是没有任何问题的。但对持续聊天来说，就会出现对之前会话一无所知的情况。


所以为了让大模型持续与用户的对话，一种常见的解决方案就是把聊天历史告诉大模型。

- 因此，在OpenManus中会进行Memory的管理。


![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67fdee3c837e6d7463760840/c97cb3f4-986e-4420-9efd-42201eadda4e.png)

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67fdee3c837e6d7463760840/76f0b101-171d-4dbf-8c97-0af6dfa9d6e5.png)

- 用户提供的 `request` 参数，调用 `update_memory` 方法将该请求作为用户消息添加到代理的Memory中。
- 除了这个函数，Manus也在进行think()、act()时也会更新Memory，同时Memory容量也不是无限大的，容量满时需要删除老的Message。


**主循环**

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67fdee3c837e6d7463760840/4db84308-fb73-45de-83d7-3a7d75cdde3b.png)

agent本质就是循环执行。

- step实现参考react step。
- 循环结束条件：max_steps或者FINISHED状态。
- 每次执行一个step并获得result——step_result = await self.step()。
- `is_stuck` 方法用于检查代理是否陷入了循环（即是否出现了重复的响应）。如果是，则调用 `handle_stuck_state` 方法处理这种情况，例如添加一个提示来改变策略。


**ReAct**

**step()**

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67fdee3c837e6d7463760840/924b5729-425c-4cf4-94dd-80b763783416.png)

- 这里的逻辑很简单。


**ToolcallAgent**

**Think()**

- 输入：不需要输入，因为用户的question是被存放在Memory中。
- 输出：一个bool类型，当内部LLM判断需要act()时，为True，否则为Fasle。


询问LLM

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67fdee3c837e6d7463760840/2af063ba-7bb0-4c4c-99ce-4af14e9a2eea.png)

- 55行的代码用于调用LLM的API接口，获取回复。


![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67fdee3c837e6d7463760840/3ff70336-01b0-467a-8c38-ca0438698ede.png)

对应到OpenManus/app/llm.py 233行附近，这里就是基于OpenAI提供的API接口进行对话，具体的参数可参考相应官方文档。

- 这里会将之前定义的**下一步Prompt**发给LLM，LLM会根据提供的工具列表，判断是否需要且调用的是哪个工具，当然也可能是：1）不需要工具只进行回复 2）调用Terminate工具结束会话。


下图是一次返回**response结果**。

- 输入的question是“计算Kobe Bryant的BMI？”，LLM先分析出了要通过浏览器查询资料，因此要use the BrowserUseTool。
- 根据传入的工具类型等信息，LLM自动构建了执行工具需要用的tool_name、action等参数。


```
ChatCompletionMessage(
    content="It seems there was an issue with retrieving the information about Kobe Bryant's height and weight through a Google search. To calculate Kobe Bryant's BMI, we need his height and weight. Let's try to find this information by opening a browser and visiting a reliable source. I will use the BrowserUseTool to navigate to a website that provides details about Kobe Bryant's height and weight. Let's proceed with this approach.",
    refusal=None,
    role='assistant',
    annotations=None,
    audio=None,
    function_call=None,
    tool_calls=[
        ChatCompletionMessageToolCall(
            id='call_aez57ImfIEZrqjZdcW9sFNEJ',
            function=Function(
            arguments='{
                "action":"navigate",
                "url":"https://www.biography.com/athlete/kobe-bryant"
                }',
            name='browser_use'),
            type='function')]
)
```

think后续逻辑

- think()后续的逻辑比较简单，主要是更新memory(memory存储单位是message)，最后在100行附近的逻辑，基于self.tool_choices等参数的设置和LLM返回的工具列表，输出bool类型结果。
- 同时，需要被调用的工具会被记录到self.tool_calls这个列表中，后续的act()会执行对应的工具。


**Act()**

- 输入：同think()，不需要输入。
- 输出：results，根据工具结果构建的一个字符串。


![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67fdee3c837e6d7463760840/3d4e7a82-ec38-4506-9108-116f8e0954a8.png)

- 这个函数比较简单，主要是调用execute_tool()函数。


**Execute_tool()**

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67fdee3c837e6d7463760840/670a129f-8378-4ebb-a651-a7f87fa112ba.png)

该函数会调用`Tool`类提供的接口execute()。

- `Tool`类接口会在后面介绍。


同时，对于预设定的**special tool**，会self._handle_special_tool(name=name, result=result)进行特殊处理。

- 当前的**special tool** 只有一个Terminate工具，特殊处理就是设置Agent的状态为AgentState.FINISHED，结束对话。


**工具相关**

我们在之前介绍了MCP相关的概念，如下图所示：

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67fdee3c837e6d7463760840/6badca86-e457-4cd5-871a-ec5c7b2204d6.png)

事实上，OpenManus也是基于MCP的，OpenManus的tool相当于MCP server，根据MCP协议，我们只需要定义tool类**支持的方法和参数等**，每次**注册一个新工具**，根据父类override一个子类即可。

那我们首先要了解父类都定义了什么参数和方法，也就是OpenManus/app/tool/base.py定义的`Basetool`类。

**Base Tool**

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67fdee3c837e6d7463760840/2e9ff6fc-d50b-474d-9153-8bfe6bca159c.png)

可以看出，代码很简单，每个tool包含的参数为:name、description(提供给LLM看的，对工具的介绍)、parameters(执行工具时要用的参数)。

同时，一个tool支持的方法有execute()和to_param()。

- execute()用于执行具体的逻辑，每个子类**需要override这个方法**。
- to_param()将工具调用的结果结构化输出。


当然，这里还有一个python关键字__call__，这个关键字很简单，定义了__call__，该类的实例对象可以像函数一样被调用。

**工具JSON**

可以根据OpenManus预定义的工具json简单了解一下，每个工具执行时需要的参数。

```
[
  {
    "type": "function",
    "function": {
      "name": "python_execute",
      "description": "Executes Python code string. Note: Only print outputs are visible, function return values are not captured. Use print statements to see results.",
      "parameters": {
        "type": "object",
        "properties": {
          "code": {
            "type": "string",
            "description": "The Python code to execute."
          }
        },
        "required": ["code"]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "google_search",
      "description": "Perform a Google search and return a list of relevant links.\nUse this tool when you need to find information on the web, get up-to-date data, or research specific topics.\nThe tool returns a list of URLs that match the search query.\n",
      "parameters": {
        "type": "object",
        "properties": {
          "query": {
            "type": "string",
            "description": "(required) The search query to submit to Google."
          },
          "num_results": {
            "type": "integer",
            "description": "(optional) The number of search results to return. Default is 10.",
            "default": 10
          }
        },
        "required": ["query"]
      }
    }
]
```

**工具示例——google_search**

OpenManus项目在OpenManus/app/tool中定义了bash工具、浏览器工具、谷歌搜索工具等，这里简单看一下谷歌搜索工具。

当然，国内可能比较难使用谷歌搜索，OpenManus社区也有大佬提供了baidu、bing等搜索引擎工具。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67fdee3c837e6d7463760840/a35dc6a7-054c-42cd-8050-3b3a51408967.png)

可以看出，代码很简单，主要做了两件事。

- 定义工具参数：name、description、parameters。
- 定义execute：基于googlesearch库提供的函数进行搜索并返回。


**五**

**总结**

OpenManus的代码介绍到这里，主要是介绍一下核心代码，同时，原作者写了planning部分的代码但暂时没有应用到项目中，笔者也没有介绍。如果想对该项目有更进一步的了解，请大家查看github上提供的源码。而且，作者还是非常积极的，每天会有十几个commit。

同时，读者可以简单本地部署玩一下OpenManus，通过几个prompt，就可以知道该项目还是停留在**“玩具阶段”**，比如笔者测试了一下，当询问“计算一下科比的BMI？”，OpenManus可以很准确的实现**谷歌搜索——浏览器访问——python计算**这个过程。但如果询问“计算科比、梅西的BMI并排序？”，无论我改写了几次prompt，OpenManus都没有给我满意的回答。

此外，无论是在工具参数信息、还是prompt、memory管理中，都可以看到agent应用大模型token**消耗量巨大**，即使我们不考虑token成本，但大模型的上下文仍然是有限的，这种资源消耗也会直接导致模型在处理多步骤任务时面临**信息截断的风险** —— 早期的关键信息可能因上下文溢出而被丢弃，进而引发推理链条的断裂。更值得警惕的是，当模型试图在有限的上下文中 “脑补” 缺失的信息时，往往会产生与事实不符的幻觉。

鉴于此，尽管 OpenManus 展示出了利用工具链解决复杂问题的潜力，不过距离成为一个实用、高效且稳定的生产级人工智能助手仍有很长的路要走。未来，开发者们或许需要在优化工具使用逻辑、提升多任务处理能力、降低大模型 token 消耗以及增强上下文管理等方面进行深入探索与改进。同时，对于普通用户而言，在体验这类项目时，也应该保持理性和客观的态度，既看到其创新性和趣味性，也认识到其当前存在的局限性。希望在技术的不断迭代和完善下，OpenManus 以及类似的项目能够早日突破现有的瓶颈，真正为人们的工作和生活带来实质性的帮助。

**往期回顾**

1. [得物技术部算法项目管理实践分享](https://mp.weixin.qq.com/s?__biz=MzkxNTE3ODU0NA==&mid=2247538265&idx=1&sn=46126305e017551fce1c548a0d482d52&scene=21#wechat_redirect)

2. [商家域稳定性建设之原理探索｜得物技术](https://mp.weixin.qq.com/s?__biz=MzkxNTE3ODU0NA==&mid=2247538263&idx=1&sn=78e7e307da19e903656c2de2afb96dc9&scene=21#wechat_redirect)

3. [得物 Android Crash 治理实践](https://mp.weixin.qq.com/s?__biz=MzkxNTE3ODU0NA==&mid=2247538237&idx=1&sn=47a37918d6e1a0123644ea690f7bdaad&scene=21#wechat_redirect)

4. [基于ANTLR4的大数据SQL编辑器解析引擎实践｜得物技术](https://mp.weixin.qq.com/s?__biz=MzkxNTE3ODU0NA==&mid=2247538099&idx=1&sn=b973a4052f5460509f2bd25ed888995e&scene=21#wechat_redirect)

5. [LSM-TREE从入门到入魔：从零开始实现一个高性能键值存储 ｜ 得物技术](https://mp.weixin.qq.com/s?__biz=MzkxNTE3ODU0NA==&mid=2247538072&idx=1&sn=c3506a84400c5cc3c72b2b0ff2291384&scene=21#wechat_redirect)

文 / 汉堡

关注得物技术，每周一、三更新技术干货

要是觉得文章对你有帮助的话，欢迎评论转发点赞～

未经得物技术许可严禁转载，否则依法追究法律责任。

“

**扫码添加小助手微信**

如有任何疑问，或想要了解更多技术资讯，请添加小助手微信：

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67fdee3c837e6d7463760840/d59e67ef-0ed6-433e-8a52-21062dfdf960.jpeg)

