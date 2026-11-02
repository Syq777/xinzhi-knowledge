---
作者:
  - "京东技术"
原文链接: https://mp.weixin.qq.com/s?__biz=MzU1MzE2NzIzMg==&amp;mid=2247501258&amp;idx=1&amp;sn=dfc474ed4e45f09477fd391fa9e7169a&amp;chksm=fa30703e9ff8615ad9019d94be6bfea6f7194dd56f9c3306b92da722e33e332bde6cfd716e6a&amp;mpshare=1&amp;scene=1&amp;srcid=1009VCvSV2AVNoHE6hRB409I&amp;sharer_shareinfo=7650dba9cbb5f9e827dde4ed9d5e2695&amp;sharer_shareinfo_first=7650dba9cbb5f9e827dde4ed9d5e2695#rd
发布时间: ""
收藏时间: "2025-10-09"
关联日记: "[[2025-10-09]]"
tags:
  - 文章
---
![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68e7b8a49a76d4094ffe5977/8f1b2006-2353-47f1-adee-a455e011e4a0.gif)

**RAG是什么？**

**RAG（Retrieval-Augmented Generation，检索增强生成）**, 一种AI框架，将传统的信息检索系统(例如数据库)的优势与生成式大语言模型(LLM)的功能结合在一起。不再依赖LLM训练时的固有知识，而是在回答问题前，先从外部资料库中“翻书”找资料，基于这些资料生成更准确的答案。

RAG技术核心缓解大模型落地应用的几个关键问题：

- **知识新鲜度**：大模型突破模型训练数据的时间限制


- **幻觉问题**：降低生成答案的虚构概率，提供参照来源


- **信息安全**：通过外挂知识库而不是内部训练数据，减少隐私泄露


- **垂直领域知识**：无需训练直接整合垂直领域知识


**RAG核心流程**

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68e7b8a49a76d4094ffe5977/b183a861-d4fc-42d6-bd68-da4a898cdbc9.png)

2.1 知识准备阶段

### 2.1.1 数据预处理

### a. 文档解析

**输入**：原始文档（如Markdown/PDF/HTML）

**操作**：

- 提取纯文本（如解析Markdown标题、段落）


- 处理特殊格式（如代码块、表格、图片、视频等）


例如：

```
[标题] 什么是 ROMA？
[段落] ROMA 是一个全自主研发的前端开发基于自定义DSL(Jue语言)，一份代码，可在iOS、Android、Harmony、Web四端运行的跨平台解决方案。
[段落] ROMA 框架的中文名为罗码。
[标题] 今天天气
[列表项] 今天的室外温度为35°C，天气晴朗。
```

#### 文档的解析过程需要考虑不同文档内容例如文本、图片、表格等场景，以及文档的语言，布局情况，可以考虑使用一些优秀的三方工具或者一些视觉模型，布局分析模型，语义理解模型来辅助解析。

#### b. 数据清洗与标准化处理

提升文本质量和一致性，使向量表示更准确，从而增强检索相关性和LLM回答质量；同时消除噪声和不规则格式，确保系统能正确理解和处理文档内容。包括: 

- 去除特殊字符、标签、乱码、重复内容。


- 文本标准化，例如 时间、单位标准化（如“今天” → “2025-07-17”）。


- 其他处理


数据的清洗和标准化过程可以使用一些工具或**NLTK、spaCy**等NLP工具进行处理。

例如: 

```
<p>ROMA框架</p>
处理： 
"ROMA框架"
今天的室外温度为35°C，天气晴朗。
处理：
"2025-07-17 的室外温度为35°C，天气晴朗"
```

c. 元数据提取

关于数据的数据，用于描述和提供有关数据的附加信息。

- **文档来源**：文档的出处，例如URL、文件名、数据库记录等。


- **创建时间**：文档的创建或更新时间。


- **作者信息**：文档的作者或编辑者。


- **文档类型**：文档的类型，如新闻文章、学术论文、博客等。


元数据在RAG中也非常重要，不仅提供了额外的上下文信息，还能提升检索质量：

1. **检索增强**


- 精准过滤：按时间、作者、主题等缩小搜索范围
- 相关性提升：结合向量相似度和元数据特征提高检索准确性


ii. 上下文丰富

- 来源标注：提供文档来源、作者、发布日期等信息


- 文档关系：展示文档间的层级或引用关系


iii. 常见的元数据提取方式:

- 正则/HTML/... 等解析工具，提取标题、作者、日期等


- 自然语言处理: 使用NLP技术（如命名实体识别、关键词提取）从文档内容中提取元数据，如人名、地名、组织名、关键词等


- 机器学习模型:  训练机器学习模型来自动提取元数据


- 通过调用外部API（如Google Scholar API、Wikipedia API）获取文档的元数据


例如：

```
complete_metadata_chunk1 = {
    'file_path': '/mydocs/roma_intro.md',
    'file_name': 'roma_intro.md',
    'chunk_id': 0,
    'section_title': '# 什么是 ROMA？',
    'subsection_title': '',
    'section_type': 'section',
    'chunking_strategy': 3,
    'content_type': 'product_description',
    'main_entity': 'ROMA',
    'language': 'zh-CN',
    'creation_date': '2025-07-02',  # 从文件系统获取
    'word_count': 42  # 计算得出,
    'topics': ['ROMA', '前端框架', '跨平台开发'],
    'entities': {
        'products': ['ROMA', 'Jue语言'], # 实体识别
        'platforms': ['iOS', 'Android', 'Web']
    },
}
```

### 2.1.2 内容分块(Chunking)

在RAG架构中，分块既是核心，也是挑战，它直接影响检索精度、生成质量，需要在检索精度、语境完整性和计算性能之间取得平衡。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68e7b8a49a76d4094ffe5977/619fbdd6-198e-4618-a15d-6ffbb779739f.png)

内容分块将长文档切分成小块，可以解决向量模型的token长度限制，使RAG更精确定位相关信息，提升检索精度和计算效率。

- AutoBots(JoyAgent)功能分块：


![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68e7b8a49a76d4094ffe5977/efff5588-c1e4-4e87-9e43-a7f94e4700ac.png)

实际RAG框架中按照文档的特性选择合适的分块策略进行分块。

- 常见的分块策略：


**a. 按大小分块**

按固定字符数进行分块，实现简单但可能切断语义单元。

优点：实现简单且计算开销小，块大小均匀便于管理。

**缺点**：可能切断语义单元，如句子或段落被分到不同块中。

例如：

```
第一段：# ROMA框架介绍ROMA是一个全自主研发的前端开发框架，基于自定义DSL(Jue语言)。
一份代码，可在iOS、Android、Harmony
第二段：、Web三端运行的跨平台解决方案。ROMA框架的中文名为罗码。
```

句子被截断，"一份代码，可在iOS、Android、Harmony" 和 "、Web三端运行的跨平台解决方案" 被分到不同块，影响理解。

b. 按段落分块

以段落为基本单位进行分块，保持段落完整性，但段落长度可能差异很大。

**优点**：尊重文档自然结构，保留完整语义单元。

**缺点**：段落长度差异大，可能导致块大小不均衡。

例如：

```
第一段：# ROMA框架介绍ROMA是一个全自主研发的前端开发框架，基于自定义DSL(Jue语言)。
一份代码，可在iOS、Android、Harmony、Web三端运行的跨平台解决方案。ROMA框架的中文名为罗码。
第二段：# 核心特性1. 跨平台：一套代码运行于多端2. 高性能：接近原生的性能表现3. 可扩展：丰富的插件系统
```

第一段包含标题和多行内容，而其他段落相对较短，可能导致检索不均衡。

**c. 按语义分块**

基于文本语义相似度进行动态分块，保持语义连贯性，但计算开销大。

**说明**：基于文本语义相似度动态调整分块边界。

**优点**：保持语义连贯性，能识别内容主题边界。

例如：

```
第一段：# ROMA框架介绍ROMA是一个全自主研发的前端开发框架，基于自定义DSL(Jue语言)。
一份代码，可在iOS、Android、Harmony、Web四端运行的跨平台解决方案。
第二段：ROMA框架的中文名为罗码。
## 核心特性1. 跨平台：一套代码运行于多端
```

使用依赖模型质量，相同文本在不同运行中可能产生不同分块结果。

**d. 分块策略总结**

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68e7b8a49a76d4094ffe5977/aad4ca04-71e6-4e55-b575-272af404b9a7.png)

**e. 优化方式**

- **混合分块策略**


结合多种分块方法的优点，如先按段落分块，再根据块大小调整，做到既保持语义完整性，又能控制块大小均匀

- 优化重叠区域


根据内容特性动态调整块之间的重叠区域大小，关键信息出现在多个块中，提高检索召回率

#### f. 常用的分块工具

- **Lang Chain框架**：提供多种分块策略，包括RecursiveCharacterTextSplitter、MarkdownTextSplitter等


- **NLTK**：用于基于自然语言句子的分块
- **spaCy**：提供语言学感知的文本分割


### 2.1.3 向量化

将高维文本数据压缩到低维空间，便于处理和存储。将文本转换为计算机可以理解的数值，使得计算机能够理解和处理语义信息，从而在海量数据文本中实现快速、高效的相似度计算和检索。

简单理解：通过一组数字来代表文本内容的“本质”。

例如，“ROMA是一个跨平台解决方案...”这句话可能被转换为一个384维的向量：

```
[块1] 什么是ROMA？
ROMA是一个全自主研发的前端开发框架，基于自定义DSL(Jue语言)...
[
  {
    "chunk_id": "doc1_chunk1",
    "text": "# 什么是 ROMA？\nROMA 是一个全自主研发的前端开发基于自定义DSL(Jue语言)，一份代码，可在iOS、Android、Harmony、Web端运行的跨平台解决方案。",
    "vector": [0.041, -0.018, 0.063, ..., 0.027],
    "metadata": {
      "source": "roma_introduction.md",
      "position": 0,
      "title": "ROMA框架介绍"
    }
  },
  // 更多文档块...
]
```

- **常用的Embedding模型：**


![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68e7b8a49a76d4094ffe5977/bc527504-3be6-402d-a210-ca2f571f2bb7.png)

### 2.1.4 向量数据库入库

将生成的向量数据和元数据进行存储，同时创建索引结构来支持快速相似性搜索。

- **常用的向量数据库包括：**


![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68e7b8a49a76d4094ffe5977/c36f852a-f961-4672-a948-d45c6cb72c08.png)

## 2.2 问答阶段

## 2.2.1 查询预处理

- 意图识别：使用分类模型区分问题类型（事实查询、建议、闲聊等）。
- 问题预处理：问题内容清洗和标准化，过程与前面数据预处理类似。
- 查询增强：使用知识库或LLM生成同义词（如“动态化” → “Roma”），上下文补全可以结合历史会话总结（例如用户之前问过“Roma是什么”）。


### 2.2.2 数据检索(召回)

### a. 向量化

使用与入库前数据向量化相同的模型，将处理后的问题内容向量化。

例如：

```
问题: "ROMA是什么?"
处理后
{
    "vector": [0.052, -0.021, 0.075, ..., 0.033],
    "top_k": 3,
    "score_threshold": 0.8,
    "filter": {"doc_type": "技术文档"}
}
```

#### b. 检索

- 相似度检索：查询向量与所存储的向量最相似(通过余弦相似度匹配)的前 top_k 个文档块。


- 关键词检索：倒排索引的传统方法,检索包含“Roma”、“优势”等精确关键词的文档。


- 混合检索：合并上面多种检索结果，效果最优。


例如：检索“ROMA是什么?”

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68e7b8a49a76d4094ffe5977/281af0cf-17f4-45db-bfa2-eaba7c790119.png)

#### c. 重排序(Reranking)

初步检索在精度和语义理解上的不足，通过更精细的上下文分析提升结果相关性。它能更好处理同义词替换、一词多义等语义细微差异，使最终结果准确。

- 原理：使用模型对每个检索结果计算相关性分数。


- 归一化：重排序模型原始输出分数没有固定的范围，它可能是任意实数，将结果归一化处理，将分数映射到 [0, 1] 范围内，使其更容易与向量相似度分数进行比较。


例如：

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68e7b8a49a76d4094ffe5977/032087dc-8b63-4ca5-b353-33c2c6d81d1c.png)

- 常用的重排序模型：


![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68e7b8a49a76d4094ffe5977/689a34d5-38a6-4a4f-8cff-5692900e25be.png)

### 2.2.3 信息整合

格式化检索的结果，构建提示词模板，同时将搜索的内容截断或摘要长文本以适应LLM上下文窗口token。

提示词优化：

1. 限定回答范围

2. 要求标注来源

3. 设置拒绝回答规则

4. ...

例如：

```
prompt 模板：
你是一名ROMA框架专家，请基于以下上下文回答：
参考信息:
[文档1] 什么是 ROMA？
ROMA 是一个全自主研发的前端开发基于自定义DSL(Jue语言)，一份代码，可在iOS、Android、Harmony、Web四端运行的跨平台解决方案。
ROMA 框架的中文名为罗码。
[文档2] Roma介绍？
[Roma介绍](docs/guide/guide/introduction.md)
文档地址: https://roma-design.jd.com/docs/guide/guide/introduction.html
要求：
1. 分步骤说明，含代码示例
2. 标注来源文档版本
3. 如果参考信息中没有相关内容，请直接说明无法回答，不要编造信息
请基于以下参考信息回答用户的问题。如果参考信息中没有相关内容，请直接说明无法回答，不要编造信息。
用户问题: ROMA是什么？
回答: {answer}
```

### 2.2.4 LLM生成

向LLM（如GPT-4、Claude）发送提示，获取生成结果。

- AutoBots(JoyAgent)示例：


![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68e7b8a49a76d4094ffe5977/b4ff4dda-f190-4783-96b8-7689f16100f7.png)

以上，实现了最简单的RAG流程。实际的RAG过程会比上述麻烦更多，包括图片、表格等多模态内容的处理，更复杂的文本解析和预处理过程，文档格式的兼容，结构化与非结构化数据的兼容等等。

最后，展示一下RAG各阶段的优化方式：

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68e7b8a49a76d4094ffe5977/37fd650f-8936-45b8-9d46-c34e24dce18a.png)

**JoyAgent**

推荐阅读

[从理论到实战，送你一份高可用架构踩坑说明书](https://mp.weixin.qq.com/s?__biz=MzU1MzE2NzIzMg==&mid=2247501233&idx=1&sn=96f8cf6e8982dee208262889c87587d8&scene=21#wechat_redirect)

[看我如何用Prompt工程将大模型调教成风控专家](https://mp.weixin.qq.com/s?__biz=MzU1MzE2NzIzMg==&mid=2247501144&idx=1&sn=165bdae383cc9b43bbd590e70f5dbb19&scene=21#wechat_redirect)

[京东发布 AI 全景图，未来三年持续投入构建万亿人工智能生态](https://mp.weixin.qq.com/s?__biz=MzU1MzE2NzIzMg==&mid=2247501227&idx=1&sn=9924a896a499c1433dc83b34d895b8ca&scene=21#wechat_redirect)

[大模型工具的“京东答案”](https://mp.weixin.qq.com/s?__biz=MzU1MzE2NzIzMg==&mid=2247501060&idx=1&sn=695e4ed0ea867f0e9f0595238dfe1449&scene=21#wechat_redirect)

**关注我们**


新枝标签： #RAG
