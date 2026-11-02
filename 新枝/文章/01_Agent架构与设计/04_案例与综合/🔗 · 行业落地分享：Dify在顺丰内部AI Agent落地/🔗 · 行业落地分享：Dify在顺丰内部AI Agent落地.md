---
作者:
  - "Coggle数据科学"
原文链接: https://mp.weixin.qq.com/s?__biz=MzIwNDA5NDYzNA==&amp;mid=2247508952&amp;idx=1&amp;sn=fe13a255da0072700a0b7318d2e8b833&amp;chksm=97e9e4bc8ac7ee29cc6ffada8af389b5fd703ad3b6327d0ab9169e2e7ac81aa219a896fa0456&amp;mpshare=1&amp;scene=1&amp;srcid=0323YCB4hOpxSWQ1SzXQHRa5&amp;sharer_shareinfo=56269412172d74aeb78f11cde5002043&amp;sharer_shareinfo_first=56269412172d74aeb78f11cde5002043#rd
发布时间: ""
收藏时间: "2025-03-23"
关联日记: "[[2025-03-23]]"
tags:
  - 文章
---
Dify 是一个开源的大语言模型（LLM）应用开发平台，融合了后端即服务（Backend as a Service, BaaS）和 LLMOps 的理念，旨在帮助开发者快速构建和部署生成式 AI 应用。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67df615ef4a5e20709eb63ae/6faec307-db4d-4d25-a739-98d416460541.jpeg)

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67df615ef4a5e20709eb63ae/5eabf318-09b0-4728-b5b2-f91fc0b21531.jpeg)

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67df615ef4a5e20709eb63ae/226b1e69-2498-4e95-8e33-dee09e99ccce.jpeg)

### Dify核心功能

- **低代码/无代码开发**：提供可视化界面，允许开发者通过拖拽、配置等方式定义 Prompt（提示词）、上下文和插件，无需深入底层技术细节。
- **模块化设计**：采用模块化架构，开发者可以根据需求选择性地使用不同模块来构建 AI 应用。
- **丰富的功能组件**：
- **AI 工作流**：通过可视化画布构建和测试强大的 AI 工作流。**RAG 管道**：支持从文档摄入到检索的完整流程，可从 PDF、PPT 等常见格式中提取文本。**Agent 智能体**：基于 LLM 的推理能力，可以自主规划任务、调用工具，完成复杂任务。**模型管理**：支持数百种专有和开源的 LLM，如 GPT、Llama2 等，并提供模型性能比较功能。
- **支持多种大语言模型**：Dify 已支持主流的模型供应商，如 OpenAI 的 GPT 系列、Claude3 等。
- **数据集管理**：提供强大的数据集管理功能，允许用户上传、管理文本和结构化数据。


![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67df615ef4a5e20709eb63ae/86942cbc-72c0-45dd-8e04-f1424b83bdb4.jpeg)

### Dify 现存缺点

任何技术产品都不可能完美无缺，Dify也不例外。深入了解其局限性，有助于我们在使用过程中更好地权衡利弊，充分发挥其优势，同时规避潜在问题。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67df615ef4a5e20709eb63ae/2000b51b-9af8-4238-a82c-d0f3e0ac364a.jpeg)

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67df615ef4a5e20709eb63ae/61a7e57a-6afa-4545-a840-adf1f86b7cdb.jpeg)

### 改造 Dify 开发平台

### 新增MySQL配置项

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67df615ef4a5e20709eb63ae/e0b5e2c2-c03e-4f59-869e-188d641d1383.jpeg)

1. **新增MySQL配置项**在Dify的配置文件中，我们新增了MySQL的配置选项，允许用户指定MySQL数据库的连接信息，包括主机地址、端口、用户名、密码以及数据库名称。这为用户提供了更多选择，使其可以根据自身需求灵活选择数据库类型。
2. **修改数据库和表结构**由于PostgreSQL和MySQL在语法和数据类型上存在差异，我们需要对Dify的数据库表结构进行适配性修改。这包括调整字段类型、索引定义以及约束条件等，以确保在MySQL环境下能够正常运行。
3. **SQL语句的适配与修改**Dify在运行过程中会执行大量的SQL语句，用于数据的增、删、改、查操作。为了兼容MySQL，我们对这些SQL语句进行了逐一审查和修改，确保它们能够在MySQL中正确执行。这一过程需要仔细处理，以避免因语法差异导致的运行错误。


### 检索增强

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67df615ef4a5e20709eb63ae/4c4e8d68-a554-49dd-b4f1-b3dfde7851dc.jpeg)

- 为Dify新增了对Elasticsearch 8的支持，使其能够充分利用Elasticsearch强大的全文检索、聚合分析以及实时数据处理能力。
- 引入了Contextual Retrieval（上下文检索）功能。通过这一功能，Dify能够在检索时充分考虑查询的上下文背景，从而返回更加符合用户意图的结果。
- 新增了对GraphRAG（图增强检索）和LightRAG（轻量级检索）的支持。这两种检索方式各有优势，能够为开发者提供更多选择。


### 集成内部服务

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67df615ef4a5e20709eb63ae/0fd4f96f-246e-4da9-994a-9ebe8cf6030e.jpeg)

### 落地软件机器人 Agent 场景

Dify作为一个强大的AI开发平台，不仅在开发效率上表现出色，更在数据处理、智能问答、业务流程自动化以及SQL生成等场景中展现了强大的能力。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67df615ef4a5e20709eb63ae/da7a338e-27cd-421a-bae0-829ff74cc608.jpeg)

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67df615ef4a5e20709eb63ae/17696932-a22c-4320-b27c-2805e36c6475.jpeg)

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67df615ef4a5e20709eb63ae/5312207e-3f7c-44aa-9d96-bcb029455816.jpeg)

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67df615ef4a5e20709eb63ae/336a642a-06b5-4b73-b61e-031e1af91c66.jpeg)

### Dify 实践总结

在未使用Dify平台之前，顺丰的开发流程面临着诸多挑战。开发应用前后端、集成和封装LLM能力需要花费大量时间，尤其是开发前端应用时，往往需要从零开始搭建。然而，引入Dify平台后，开发效率得到了显著提升。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67df615ef4a5e20709eb63ae/0abbe7cd-0b57-4935-a9b7-32fd2d71f823.jpeg)

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67df615ef4a5e20709eb63ae/36cdf726-14fb-4dc5-9497-45a9bcfe2982.jpeg)

*添加好友领取PDF*

# * 学习大模型 & 讨论Kaggle *#

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67df615ef4a5e20709eb63ae/cbf4899c-ce03-466c-ae0d-d31ac1c56e2f.webp)

△长按添加竞赛小助手

每天大模型、算法竞赛、干货资讯

与 36000+来自竞赛爱好者一起交流~

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67df615ef4a5e20709eb63ae/f1a7c750-a372-43e6-9cdb-878ffd29a003.webp)

