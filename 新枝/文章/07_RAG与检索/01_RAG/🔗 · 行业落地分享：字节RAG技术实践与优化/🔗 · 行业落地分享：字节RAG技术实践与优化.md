---
作者:
  - "Coggle数据科学"
原文链接: https://mp.weixin.qq.com/s?__biz=MzIwNDA5NDYzNA==&amp;mid=2247508891&amp;idx=1&amp;sn=0d0ee9a2057680f64beece21da1767db&amp;chksm=9713a95a4fff77a7561328f59ec74de21bdda7a848e98b90c20e04c6d6ce65d1f14537b2758d&amp;mpshare=1&amp;scene=1&amp;srcid=040824ZjSh7hDCSkz9Crgryq&amp;sharer_shareinfo=a1469ef8d3705c26f9d3155a2b833b3a&amp;sharer_shareinfo_first=a1469ef8d3705c26f9d3155a2b833b3a#rd
发布时间: ""
收藏时间: "2025-04-08"
关联日记: "[[2025-04-08]]"
tags:
  - 文章
---
在大模型时代，如何高效地存储、管理和分析海量数据，是每个企业亟待解决的问题。**我们将深入探讨 RAG 技术的各个环节，从技术简介到实践应用。**

- RAG 的工作原理
- 高性能向量检索技术
- 全文检索 & 混合检索
- GraphRAG 实践


## RAG技术

RAG技术是一种将检索（Retrieval）和生成（Generation）相结合的方法。它通过检索模块从海量数据中快速找到与问题相关的文档片段，然后利用生成模块对这些片段进行整合和优化，最终生成高质量的答案。

### Naive RAG

最基础的RAG实现方式，直接将检索到的文档片段输入到生成模型中，生成答案。这种方法简单直接，但在处理复杂问题时可能不够灵活。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67f53fb48f829978dec681a3/93e127b8-8507-414a-af42-ff4e73c4a2e9.jpeg)

### Hybrid Search（混合检索）

结合向量检索（语义检索）和全文检索（关键词检索）的优点，同时考虑语义和关键词信息，提升检索的准确性和效率。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67f53fb48f829978dec681a3/9b83a5df-80f4-4d76-b4f0-50b01e033be1.jpeg)

### GraphRAG

将文本数据通过大模型转化为图结构，利用图的关联性检索全局信息。这种方法适合处理涉及多个实体和关系的问题，例如：“哪些公众人物在各种娱乐文章中被反复提及？”

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67f53fb48f829978dec681a3/77c632b5-7468-46ca-999c-7d088f7889fd.jpeg)

### Agentic RAG

一种更智能的RAG实现方式，通过代理（Agent）决定是否需要检索，以及如何处理检索结果。它可以根据问题的复杂性动态调整检索和生成策略。具体实现可以参考LangGraph的Agentic RAG教程。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67f53fb48f829978dec681a3/2a7ce2df-622c-4009-9f6f-27051eb6a04f.jpeg)

### Adaptive RAG

通过学习问题的复杂性，动态调整检索策略的RAG方法。这种方法能够根据问题的具体需求，灵活调整检索和生成的流程，提升系统的适应性。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67f53fb48f829978dec681a3/3c3d5b69-0297-4174-908d-0601a357c581.jpeg)

## RAG 相关技术需求

RAG技术的核心目标是解决大模型在利用外部知识时面临的挑战，主要包括以下几点：

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67f53fb48f829978dec681a3/69f1d73b-3769-4477-aaf4-ae141377f5b3.jpeg)

- 如何获取准确的相关数据


在海量的外部知识库中，如何快速、准确地找到与问题相关的信息，是RAG技术的关键。这不仅需要高效的检索技术，还需要确保检索结果的相关性和准确性。

- 如何让大模型有效利用检索数据


检索到的数据需要与大模型的生成能力相结合。如何将检索到的信息高效地融入生成过程中，使生成的答案既准确又符合用户需求，是RAG技术的核心挑战。

- 性能优化 在实际应用中，RAG系统的性能至关重要。如何优化数据处理流程，提升检索和生成的速度，是RAG技术需要解决的另一个


## RAG技术的关键环节

### 数据处理

数据处理是RAG技术的基础，主要包括以下步骤：

1. **文本切分**：将长文本切分为适合检索和生成的片段，确保每个片段都能提供有效的上下文。
2. **向量提取**：通过嵌入模型将文本转换为向量表示，便于后续的相似度计算。


### 高性能检索技术

RAG技术依赖于高效的检索技术，主要包括以下几种：

1. **向量检索（Dense & Sparse）**：通过向量空间模型，快速找到与查询最相似的文档。
2. **全文检索（关键词搜索）**：基于关键词的检索技术，适用于处理明确的查询。
3. **图检索**：利用图结构的关联性，检索全局信息。
4. **结构化信息检索**：针对结构化数据的检索，适用于处理表格和数据库。


### 大模型交互与性能优化

1. **Prompt Engineering**：通过设计高效的提示模板，将检索结果与大模型的输入相结合。
2. **Agents**：引入智能代理（Agent），动态决定是否需要检索，以及如何处理检索结果。
3. **SFT for RAG**：通过监督微调（SFT），优化大模型对检索结果的利用。
4. **Retrieval优化**：优化检索模块，提升检索效率和准确性。
5. **幻觉消除及推理优化**：通过技术手段减少大模型生成中的幻觉问题，提升生成内容的可信度。


## 高性能向量检索技术

向量检索是一种基于向量空间模型的检索技术。它通过将文本或其他数据转换为高维向量，利用向量之间的相似度来衡量数据的相关性。与传统的关键词检索不同，向量检索能够更好地捕捉语义信息，从而实现更精准的检索效果。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67f53fb48f829978dec681a3/e4cfdb39-6438-4ca7-a732-22f05a5e3ace.jpeg)

在自然语言处理中，向量检索主要用于以下几个场景：

1. **语义搜索**：通过将文本嵌入到向量空间，用户可以使用自然语言查询，系统会返回语义最相关的文档。
2. **推荐系统**：利用向量检索技术，可以根据用户的历史行为和偏好，推荐最相关的商品或内容。
3. **知识图谱**：通过向量检索，可以快速找到与目标实体或关系最相关的知识片段。


![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67f53fb48f829978dec681a3/1ab2d5d0-4d14-46d6-a40f-5e2d897077ec.jpeg)

基于表的结构简单高效数据量大时效率低小规模数据检索基于哈希的结构检索速度快准确性可能降低大规模数据检索基于树的结构检索效率高构建索引复杂中等规模数据检索基于聚类的结构处理大规模数据构建索引复杂大规模数据检索基于图的结构检索速度快，准确性高构建索引复杂大规模复杂数据检索

### 基于表的结构（Table-based）

基于表的结构通过将向量存储在表格中，利用哈希表等数据结构快速定位目标向量。这种方法的优点是简单高效，但随着数据量的增加，检索效率会逐渐下降。

### 基于哈希的结构（LSH）

局部敏感哈希（LSH）是一种通过哈希函数将相似向量映射到相同或相近的哈希值的方法。LSH 的优点是检索速度快，适用于大规模数据集，但可能会牺牲一定的准确性。

### 基于树的结构（Tree-based）

基于树的结构（如 KD-Tree 和 Annoy）通过构建树形索引，将向量空间划分为多个区域。这种方法的优点是检索效率高，能够快速定位到目标向量，但构建索引的过程较为复杂。

### 基于聚类的结构（Cluster-based）

基于聚类的结构（如 IVF、SCANN 和 SPANN）通过将向量空间划分为多个聚类，利用聚类中心快速定位目标向量。这种方法的优点是能够处理大规模数据集，并且检索效率较高。

### 基于图的结构（Graph-based）

基于图的结构（如 HNSW、NSG 和 DiskANN）通过构建图结构，将相似向量连接起来，形成一个高效的检索网络。这种方法的优点是检索速度快，能够处理复杂的向量空间，同时保持较高的准确性。

### ANN结构：基于聚类的向量索引

在处理大规模数据集时，向量索引的内存占用是一个关键问题。向量压缩技术通过减少向量的存储空间，以牺牲部分精度为代价，来优化内存使用。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67f53fb48f829978dec681a3/ec5dca52-4c56-4696-b95d-9a1429626bc1.jpeg)

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67f53fb48f829978dec681a3/4c65e0f5-b5dc-4fd9-aacd-7b8681b321e2.jpeg)

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67f53fb48f829978dec681a3/39eecbce-a289-4f17-bf9b-ffc985106c30.jpeg)

## ByteHouse

ByteHouse通过自研优化器和高并发点查技术，显著提升了查询效率。在TPC-DS标准测试中，ByteHouse的查询性能比行业主流开源产品高出16%。

ByteHouse Vector Search的一大亮点是其统一化的向量接入层。这种设计使得ByteHouse能够方便地接入多种类型的索引，包括但不限于：

- **HNSW（Hierarchical Navigable Small World）**：一种基于图的高效近似最近邻搜索索引，适用于大规模数据集。
- **HNSWSQ（HNSW + Scalar Quantization）**：结合标量量化技术，进一步优化存储和检索性能。
- **IVF_PQ_FS（Inverted File + Product Quantization + Filtered Search）**：通过聚类和乘积量化技术，实现高效的向量检索。


![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67f53fb48f829978dec681a3/e8373887-2400-4334-866a-517ff8680918.jpeg)

ByteHouse不仅支持单独的向量检索和全文检索，还支持混合搜索（Hybrid Search），将两者的优势结合起来。混合搜索方法包括：

1. **RRF（Reciprocal Rank Fusion）**：基于排名融合，综合向量检索和全文检索的结果。
2. **MinMax**：基于分数融合，取向量检索和全文检索的最高分数作为最终结果。


![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67f53fb48f829978dec681a3/85a705bd-66c4-4c32-8201-7bfb96d8e66f.jpeg)

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67f53fb48f829978dec681a3/37545809-77d1-4ec0-b1b7-356a86d0d141.jpeg)

## GraphRAG：全局信息检索的新时代

GraphRAG通过引入图结构，将实体和关系以图的形式表示，从而能够更好地处理复杂问题。在GraphRAG中，每个实体是一个节点，每个关系是一条边。通过图检索，我们可以从局部信息扩展到全局信息，从而更准确地回答问题。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67f53fb48f829978dec681a3/f6c9929b-d7ea-4522-95c6-dcfa1f19e1b0.jpeg)

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67f53fb48f829978dec681a3/1e97e2a7-dd56-4de5-8a51-c93db818c6df.jpeg)

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67f53fb48f829978dec681a3/e2bf662e-4dff-4642-a0dd-6ac30ca5efdc.jpeg)

*添加好友领取PDF*

# * 学习大模型 & 讨论Kaggle *#

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67f53fb48f829978dec681a3/e0dca04f-d050-46ef-8509-36431b33f5a1.webp)

△长按添加竞赛小助手

每天大模型、算法竞赛、干货资讯

与 36000+来自竞赛爱好者一起交流~

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67f53fb48f829978dec681a3/d4c25ff1-6b23-429a-8436-dcbff4718c5b.webp)

