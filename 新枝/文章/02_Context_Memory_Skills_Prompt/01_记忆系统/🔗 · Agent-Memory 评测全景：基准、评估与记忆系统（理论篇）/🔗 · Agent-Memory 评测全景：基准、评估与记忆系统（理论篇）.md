---
作者:
  - "大淘宝技术"
原文链接: https://mp.weixin.qq.com/s?__biz=MzAxNDEwNjk5OQ==&amp;mid=2650543910&amp;idx=1&amp;sn=4359b93141cc75aaa1976382d4cb39df&amp;chksm=820eb22cdea8e4169ba0e8858164d3b776002deb77c3253f36505d50ddb761c5914ca25746a7&amp;mpshare=1&amp;scene=1&amp;srcid=0603LZayCcBtaggSUwmzNyPb&amp;sharer_shareinfo=93f341e786c9802a085c664b612555c8&amp;sharer_shareinfo_first=93f341e786c9802a085c664b612555c8#rd
发布时间: ""
收藏时间: "2026-06-03"
关联日记: "[[2026-06-03]]"
tags:
  - 文章
---
《Evaluating Memory in LLM Agents via Incremental Multi-Turn Interactions》

- 基本信息


数据集part1数据集part2场景重构多个现有数据集并引入新数据集EventQA和FactConsolidation评估LLM的记忆能力：准确检索、测试时学习、长程理解和冲突解决

LLM-Agent的评估主要集中在推理、规划和执行能力上，而记忆能力的评估则相对不足。记忆能力包括如何记忆、更新和检索长期信息。

本文识别出四个对记忆代理至关重要的核心能力：

1. 准确检索 (Accurate Retrieval, AR)：指agent从长对话历史中识别并检索重要信息的能力。

2. 测试时学习 (Test-Time Learning, TTL)：指agent动态获取新技能的能力，而无需额外训练。类似于LLM)的上下文学习，通过对话历史中的少量示例学习新任务。

3. 长程理解 (Long-Range Understanding, LRU)：指agent在长对话中形成抽象的、高层次理解的能力，能够回答需要整体理解的问题。

4. 冲突解决 (Conflict Resolution, CR)：指agent在面对新旧信息冲突时，检测并解决矛盾的能力。agent能够识别并舍弃过时或错误的信息，以反映最新的现实状态。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6a1fff302c5c27139381b6cf/22d1282d-7b0a-423d-891e-8665e7a038c9.png)

- 数据集构建


1. 本文识别出四个对记忆代理至关重要的核心能力：准确检索（Accurate Retrieval）、测试时学习（Test-Time Learning）、长程理解（Long-Range Understanding）和冲突解决（Conflict Resolution）。
2. MemoryAgentBench结合了重新构建的现有数据集，并引入新数据集EventQA和FactConsolidation，分别用于评估准确检索和冲突解决能力。
3. 提供了一个统一的评估框架，允许不同类型的记忆代理在相同的条件下进行比较，从而揭示其在记忆能力上的差异。
4. 本文评估了三种主要类型的记忆代理：长上下文代理、检索增强生成（RAG）代理和代理记忆代理，揭示了当前方法在处理动态记忆更新和长程一致性任务时的局限。


Limitation：本文指出，当前使用的合成数据集可能无法完全反映真实用户对话的特征，未来的工作将致力于收集和整理更具现实性的真实数据集。

> 评估了三种主要类型的记忆代理：长上下文代理（Long-Context Agents）： 现代语言模型通常支持扩展的上下文窗口（从128K到超过1M tokens）。一种直接的策略是维护一个最近token的上下文缓冲区。检索增强生成（RAG）代理（RAG Agents）： RAG代理通过将过去的信存储在外部记忆池中，并在需要时检索相关内容来解决上下文限制。代理记忆代理（Agentic Memory Agents）： 代理记忆代理通过采用代理循环（agentic loops）来超越静态记忆存储，代理可能会重新表述问题、进行记忆查找并更新其工作记忆。定期更新的数据集池。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6a1fff302c5c27139381b6cf/bab6848d-61df-4ac9-b4fe-aecccabe11ea.png)

- 数据集指令


![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6a1fff302c5c27139381b6cf/ca5b8b71-d9ec-4f59-bbf3-fb5ee0a0b452.png)

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6a1fff302c5c27139381b6cf/2afea41e-c6c1-424d-9a97-ab1f7d9a2952.png)

- 评估


1. RAG方法在准确检索任务中表现优越，RAG代理在准确检索类别的任务中优于GPT-4o-mini，RAG代理在提取回答问题所需的小段文本方面表现出色。
2. 其次，长上下文模型在测试时学习（TTL）和长范围理解（LRU）任务中表现最佳。RAG方法仅能从过去的上下文中检索部分信息，缺乏对输入的整体理解能力。
3. 所有现有方法在冲突解决（CR）任务上均表现不佳，尤其是在多跳场景中，准确率最高仅为6%。只有长上下文代理在单跳场景中取得了相对合理的结果。


### ▐ LONGMEMEVAL

《LONGMEMEVAL: BENCHMARKING CHAT ASSISTANTS ON LONG-TERM INTERACTIVE MEMORY》

- 基本信息


特点数量场景提出一种统一框架，优化记忆设计：会话分解、事实增强的键扩展和时间感知的查询扩展LONGMEMEVAL-S（约115k个tokens）和LONGMEMEVALM（500个会话，约150万tokens）评估聊天助手的长期记忆能力：信息提取、多会话推理、时间推理、知识更新和拒绝回答

会话分解（Session Decomposition）：在长期记忆系统中，用户与助手的会话往往内容繁多且涵盖多个话题。将每个会话作为一个整体存储可能导致检索效率低下，而过度压缩会丢失细节信息，影响系统对复杂问题的回答能力。将会话分解为多个“轮次”，并进一步提取摘要、关键短语或用户事实。

事实增强的键扩展（Fact-Augmented Key Expansion）：传统方法使用会话或轮次内容作为键，可能无法有效捕捉到查询与记忆之间的关联。键扩展策略通过提取value中的摘要、关键短语、用户事实和时间戳事件来增强键。

时间感知的查询扩展（Time-Aware Query Expansion）：在涉及时间的查询任务中，单纯依赖相似性搜索可能无法满足需求。在索引阶段，从文本中提取时间戳事件；在检索阶段，从查询中推断时间范围，并据此过滤掉不相关的信息。

- 数据集构建


LONGMEMEVAL基准由500个问题组成。每个问题从一个或多个多轮任务导向的用户-助手对话中提取信息。两种配置：LONGMEMEVAL-S（约115k个tokens）和LONGMEMEVALM（500个会话，约150万tokens）。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6a1fff302c5c27139381b6cf/b183d594-4387-4fac-a32f-4ab69ed15e52.png)

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6a1fff302c5c27139381b6cf/4774eb99-20c8-4caf-b1bc-aa78748d28e0.png)

- 数据集指令


![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6a1fff302c5c27139381b6cf/144082e9-efa0-4199-a77a-60c9544a717f.png)

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6a1fff302c5c27139381b6cf/00d840e0-9f5f-4d5e-8afe-8ff805a942f0.png)

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6a1fff302c5c27139381b6cf/15fd0c75-8e87-4964-8626-b7ac9b21600c.png)

- 评估


1. 评估过程中，采用了四个关键阶段的统一框架：索引、检索、读取和评估。在索引阶段，比较不同的值表示策略--会话分解和用户事实提取。在检索阶段，采用时间感知的查询扩展策略，以提高时间推理问题的准确性。在读取阶段，采样Chain-of-Note和结构化提示格式，以提升模型的读取准确性。
2. 现有的商业聊天助手和长上下文LLM在LONGMEMEVAL基准上表现不佳，准确率下降30%至60%。当前的记忆机制在处理复杂的长期交互时仍存挑战，需要更复杂的记忆机制，提高个性化和可靠性。


### ▐ MemBench

《MemBench: Towards More Comprehensive Evaluation on the Memory of LLM-based Agents》

- 基本信息


特点场景包含事实记忆和反思记忆的多场景数据集，并引入参与和观察两种互动场景评估LLM-agent记忆能力，多指标评估（准确率、召回率、容量和效率）

已有研究对LLM-Agent的记忆能力进行了评估，但这些评估局限性。首先，许多研究主要集中在事实记忆的评估上，而忽视了反思记忆的评估。其次，现有评估大多局限于参与场景，未能充分考虑观察场景的影响。此外，现有研究往往只关注记忆机制的有效性，而未考虑其效率和容量，这在实际应用中同样重要。

事实记忆 (Factual Memory)：涉及用户或与其相关实体的事实属性，例如亲属的年龄或职业、事件的时间细节等。这些信息通常在用户与代理的日常对话中。通过提出有关这些属性的问题，测试代理的多种记忆能力，包括信息提取、跨会话推理、知识更新、时间推理等。

反思记忆 (Reflective Memory) ：指基于用户表达的低级偏好（例如具体的事实属性，如用户对某道菜的喜爱）和总结出的高级偏好（例如口味偏好等更高层次的信息）。这种机制使得代理能够通过分析用户的低级偏好，推断出用户的高阶偏好或总结出其整体的行为模式或倾向。

参与场景 (Participation Scenario)：代理与用户进行互动。代理不仅要记住用户信息，还要记住自己生成的响应。这种场景是代理的典型使用场景。

观察场景 (Observation Scenario)：代理仅作为观察者，记录用户输入的信息。代理在此场景中不执行任何动作，因此不会影响记忆。

- 数据集构建


1. 数据集包括两种主要的互动场景：参与场景和观察场景。在参与场景中，代理与用户进行互动，而在观察场景中，代理作为观察者被动接收用户输入的信息。数据集的构建过程包括用户关系图的采样和记忆数据的生成，旨在涵盖事实记忆和反思记忆两种不同层次的记忆内容。参与者是常见方式，观察者是创新点。
2. 数据集的设计考虑了多层次的记忆：事实记忆和反思记忆。事实记忆涉及用户或相关实体的具体属性，例如年龄或事件的时间细节，而反思记忆则关注从用户的低层次偏好中提取和总结高层次偏好。通过这种方式，能够全面评估代理在信息提取、跨会话推理、知识更新和时间推理等任务中的记忆能力。
3. 多指标评估：记忆准确性、记忆召回率、记忆容量和记忆效率。记忆准确性通过比较代理的选择与真实选择来计算，记忆召回率则反映了代理有效存储和组织记忆内容的能力。记忆容量评估代理在达到一定记忆内容量时的表现变化，而记忆效率则关注代理在处理记忆时的时间成本。
4. 采用用户关系图采样的方法，结合推荐系统的数据，生成了高层次的偏好属性。并通过自对话方法扩展了参与场景的数据。此外，数据集还包括了多轮对话和用户消息列表，以模拟真实的用户交互过程。这种方法不仅增强了数据集的多样性，还提高了评估的有效性。


Limitation：1）当前的数据集主要集中在结构化数据的评估上，未来可以探索如何评估智能体在用户情感记忆等非结构化数据方面的能力。2）如何在长时间交互中保持反思记忆的能力，也是一个值得深入研究的问题。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6a1fff302c5c27139381b6cf/16f9f1ee-b69a-44b4-a9bb-0e39d139bcb0.png)

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6a1fff302c5c27139381b6cf/18b07ce0-ad29-4e48-8ff0-0496b8916fa2.png)

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6a1fff302c5c27139381b6cf/b5da0d51-3f8f-40b5-9e0d-6074b5c7a149.png)

- 评估


![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6a1fff302c5c27139381b6cf/9593c0f3-4761-4c6d-be47-3a6eb49b8214.png)

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6a1fff302c5c27139381b6cf/baeabc84-8481-4c8b-89b2-112339073ccc.png)

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6a1fff302c5c27139381b6cf/2fb0d8a3-7302-4ddb-b98e-e811e448f612.png)

## Memory System

### ▐ THEANINE&TeaFarm

《Towards Lifelong Dialogue Agents via Timeline-based Memory Management》

- 基本信息


THEANINE框架TeaFarm数据集构建基于时间和因果关系的记忆图，保留重要的上下文信息；提取和精炼记忆时间线，增强了响应生成的质量。以无人工干预的方式评估代理在整合过去记忆方面的表现

- 数据集构建


1. 为了评估 THEANINE 的有效性，提出了 TeaFarm，一个基于反事实的评估基准。通过设计反事实问题来测试对话代理的记忆引用能力，确保代理能够在面对不真实的陈述时正确引用过去的对话。
2. 在 TeaFarm 中，代理被“误导”生成错误的响应，其任务是通过正确引用过去的对话来避免被误导。例如，通过生成一个非事实的声明（如“Speaker B 不拥有一辆车”），对话代理必须识别并引用真实的对话历史（如“Speaker B 事实上拥有一辆车”）来生成正确的响应。
3. 在 TeaFarm 的流程中，对话代理首先会经过一个对话会话的总结，然后通过一个问题生成器（LLM）以时间顺序输入这些总结，生成从两个对话者角度出发的反事实问题及其正确答案。接下来，对话代理会在一个新的对话会话中被询问这些问题，其响应的正确性将被评估。


![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6a1fff302c5c27139381b6cf/4bf88aaf-7652-471b-9011-a4786429ebff.png)

- 数据集指令


![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6a1fff302c5c27139381b6cf/f524e0b8-166c-4787-b0d4-e3af5bd03f5e.png)

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6a1fff302c5c27139381b6cf/b3113e91-9876-4ea8-bacc-2e7e6c929fbf.png)

### ▐ RMM

《In Prospect and Retrospect: Reflective Memory Management for Long-term Personalized Dialogue Agents》

- 基本信息


主要内容主要操作提出了反思记忆管理（RMM）机制，以解决LLM在长期个性化对话中无法有效保留和检索信息的问题RMM结合了前瞻性反思和回顾性反思两种方法：前者通过将对话历史总结为主题，优化未来检索；后者则利用在线强化学习动态调整检索机制

- 研究背景


LLM在长期交互中保持用户的个性化信息和对话连续性方面存在局限。现有方法面临两个主要挑战：固定的记忆粒度无法有效捕捉对话的自然语义结构，导致信息的碎片化和不完整；固定的检索机制无法适应多样化的对话上下文和用户交互模式。

- 主要操作


反思记忆管理（Reflective Memory Management, RMM）机制：旨在解决大语言模型（LLMs）在长期个性化对话中面临的记忆保持和信息检索的挑战。RMM框架结合了前瞻性反思（Prospective Reflection）和回顾性反思（Retrospective Reflection）两种机制，以实现更灵活和细致的记忆管理。

前瞻性反思：通过将对话历史动态总结为主题基础的记忆表示，优化未来的检索能力。

回顾性反思：利用在线强化学习（RL）方法，基于LLMs生成的引用证据迭代精炼检索过程。

### ▐ M3-Agent

《Seeing, Listening, Remembering, and Reasoning: A Multimodal Agent with Long-Term Memory》

https://github.com/ByteDance-Seed/m3-agent

- 基本信息


M3-Agent算法内容M3-Bench具备长期记忆的多模态智能体框架实时处理视觉和听觉输入构建和更新记忆M3-Bench-robot：100个真实世界视频M3-Bench-web：929个网络视频

- 算法框架


1. M3-Agent：一种具备长期记忆的多模态智能体框架。通过实时处理视觉和听觉输入，构建和更新其长期记忆。
2. 记忆生成与存储：情节记忆记录观察到的具体事件，而语义记忆则提取一般知识。记忆以图形结构存储，每个节点代表一个独特的记忆项。通过增量添加新节点或更新现有节点，在长期记忆中保持一致性。
3. 控制过程与推理：通过强化学习（reinforcement learning）优化，允许智能体在多轮交互中逐步获取信息，而不是依赖单轮检索增强生成（RAG）。M3-Agent能够自主决定调用哪种搜索功能，以便有效地检索所需的记忆。


![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6a1fff302c5c27139381b6cf/4d279b7d-9fb5-4758-874c-1a2ea692f65f.png)

- 数据构建


1. 为评估M3-Agent的记忆有效性和基于记忆的推理能力，研究团队开发了M3-Bench，这是一个新的长视频问答基准。
2. M3-Bench包括来自机器人视角的100个真实世界视频（M3-Bench-robot）和929个来自网络的视频（M3-Bench-web），并为每个视频注释了问题-答案对，以测试智能体在理解人类、提取一般知识和跨模态推理等关键能力上的表现。


![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6a1fff302c5c27139381b6cf/17f2251a-4b05-401f-b5e5-452f99aa7100.png)

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6a1fff302c5c27139381b6cf/baa22a70-8dc6-4fc2-a02a-a3428566fb62.png)

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6a1fff302c5c27139381b6cf/42049eaa-aa14-43ba-86fb-1f9ff495dc9e.png)

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6a1fff302c5c27139381b6cf/97c608a4-be9f-45de-baf0-4f6235a4c7c4.png)

- 实验结果


实验结果表明，经过强化学习训练的M3-Agent在所有基准测试中均优于最强基线，显示出其在记忆生成和推理能力上的卓越表现。具体而言，M3-Agent在M3-Bench-robot、M3-Bench-web和VideoMME-long上的准确率分别提高了6.7%、7.7%和5.3%。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6a1fff302c5c27139381b6cf/d6182917-775f-4950-92cd-6db237048aef.png)

### ▐ Mem0

《Mem0: Building Production-Ready AI Agents with Scalable Long-Term Memory》

https://github.com/mem0ai/mem0

- 基本信息


特点Mem0Mem0g提出Mem0和Mem0g两种记忆架构，提升LLM在长时间对话中的一致性和连贯性通过动态提取、整合和检索对话中的关键信息，提高了单跳和多跳推理的性能引入图形记忆表示，增强了对复杂关系的建模能力

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6a1fff302c5c27139381b6cf/68a8ec80-5321-4625-b435-9ccb5a89ee4c.png)

- 算法框架


Mem0记忆架构：

- 对持续对话的显著信息进行动态捕获、组织和检索。
- 在提取阶段，系统接收一对消息（用户消息和助手响应），利用数据库的对话摘要和最近消息来建立上下文。将这些信息与新消息对结合，生成一个综合提示，用LLM提取重点记忆。
- 在更新阶段，评估提取的候选事实与现有记忆的一致性，通过LLM进行适当的记忆管理操作（如添加、更新、删除或无操作），以确保知识库的一致性和时间一致性。


![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6a1fff302c5c27139381b6cf/b988c06a-7b68-405c-91d0-a957be00d1a1.png)

Mem0g：

- 在Mem0的基础上引入了图形记忆表示，旨在更好地建模对话元素之间的复杂关系。将记忆表示为有向标记图，节点代表实体，边表示实体之间的关系。
- 实体提取模块，识别对话中的关键实体及其类型；关系生成模块，通过分析上下文生成实体之间的关系三元组。结构化的图形表示使Mem0g能在处理复杂查询时进行更高级的推理。


![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6a1fff302c5c27139381b6cf/69e063e5-641f-4774-8a3e-6a4eb8721d21.png)

- 数据构建


使用LOCOMO数据集评估长时间对话记忆的能力：

- 该数据集包含10个扩展对话，每个对话有600个对话轮次和26000个标记，涵盖多个会话。
- 每个对话后附有200个问题，分为单跳、多跳、时间和开放域四类。
- 评估指标包括传统的F1分数和BLEU分数，以及基于LLM的评估方法、提供更全面评估。


![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6a1fff302c5c27139381b6cf/5cb179c2-cff5-4459-93ff-f5566ee45ebf.png)

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6a1fff302c5c27139381b6cf/c0aebec4-e0c7-4e13-ae62-c149036be6a8.png)

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6a1fff302c5c27139381b6cf/2c7068f1-9dc6-40c6-ad9f-ce3031782551.png)

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6a1fff302c5c27139381b6cf/079113ab-2f7a-4d91-b7f5-3a80d531d261.png)

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6a1fff302c5c27139381b6cf/f2e69f69-f48c-489a-ab46-721951ad24fd.png)

- 实验结果


1. 比较了六类基线系统，包括LOCOMO基准、开源记忆解决方案、RAG方法、全上下文处理、专有模型和记忆管理平台。
2. Mem0和Mem0g在多种问题类型上表现优越，Mem0在单跳和多跳推理任务中表现出色，Mem0g在时间推理和开放域任务中表现出色、结构化图形表示在捕捉事件序列和时间关系方面存在优势。
3. Mem0和Mem0g在响应延迟和计算效率方面表现出色，尤其是在与全上下文方法的比较中，显著降低了延迟和令牌消耗。


![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6a1fff302c5c27139381b6cf/05d5b8ec-9028-4047-ade3-7001854d1b39.png)

Single-Hop（单跳）：从单个对话轮次中检索单个事实性信息。例如，如果用户询问“某人昨天去了哪里”，且相关信息在对话中直接提到，则系统只需从单个对话中提取答案。

Multi-Hop（多跳）：从多个对话轮次中合成信息。例如，将对话中的两个独立声明结合（如“某人昨天去了某地”和“某地的天气如何”）来推导答案，则需要多跳推理。

Open Domain（开放域）：结合对话中的信息与外部知识。例如，如果用户的问题涉及对话中没有直接提到的内容，需要结合对话中的信息和外部知识库进行回答。

Temporal（时间推理）：正确建模对话中事件的时间顺序、持续时间及其相对时间关系。例如，涉及“某人何时去了某地”，则要利用对话中的时间戳或隐含的时间信息进行推理。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6a1fff302c5c27139381b6cf/3ad1b0a5-0eaa-4790-a09b-ba505ef3dc46.png)

> p50（median）：表示50%的延迟值低于或等于此值，50%的延迟值高于或等于此值。p95（95th percentile）：表示95%的延迟值低于或等于此值，只有5%的延迟值高于此值。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6a1fff302c5c27139381b6cf/0594ecbb-3bee-4d1d-8b51-00e458b32b2d.png)

## 总结与讨论

当 Agent 从单轮对话走向长程任务与跨会话交互，Memory 从“加分项”变成决定体验与能力上限的关键组件：它影响多轮一致性、知识与偏好的持续利用，以及跨任务的经验复用。因此，Agent-Memory 评测不应止于“跑分排名”，而应回答三件事：记什么、怎么记、是否带来可量化的任务收益。

本文沿三条主线梳理：Memory Benchmark（评什么：任务/数据/指标口径）、Memory Evaluation（怎么评：评测协议、对照与消融、误差归因）、Memory System（怎么落地：存储与索引、写入与更新、冲突与时效、隐私权限、与 Agent/RAG/工具链集成），并对代表性方案的取舍进行对比。现有评测仍有共性问题：1）增益难归因（记忆、长上下文、RAG 常叠加）；2）口径不统一，易“命中但无用”，指标与端到端收益脱钩；3）动态更新与遗忘覆盖不足，缺少长期压力测试；4）成本与约束缺位（时延、token/调用、存储、隐私合规）。

面向真实应用，更可用的评测应同时覆盖四个维度：检索正确性、使用有效性、时间维度（跨会话/变化/遗忘）、成本维度（延迟/费用/存储/合规）。只有纳入统一且可复现的框架，评测才能真正指导选型与工程迭代。

我们也在持续探索面向真实业务的 Agent 记忆体系与评测闭环；如你在落地中遇到更新、冲突处理或评测设计问题，欢迎交流。

**[图片]团队介绍**

本文作者阿元，来自淘天集团 - 场景智能技术团队。一支专注于通过 AI 和 3D 技术驱动商业创新的技术团队，依托大淘宝丰富的业务形态和海量的用户、数据，致力于为消费者提供创新的场景化导购体验，为商家提供高效的场景化内容创作工具，为淘宝打造围绕家的场景的第一消费入口。我们不断探索并实践新的技术，通过持续的技术创新和突破，创新用户导购体验，提升商家内容生产力，让用户享受更好的消费体验，让商家更高效、低成本地经营。

