---
作者:
  - "字节跳动技术团队"
原文链接: https://mp.weixin.qq.com/s?__biz=MzI1MzYzMjE0MQ==&amp;mid=2247513432&amp;idx=1&amp;sn=4b7c3096878e5fee05140f99b6256996&amp;chksm=e8a18a47ec40807711c293a67aabfeb698d000ceee1738f34c2efede9e7238dcb02c0404308c&amp;mpshare=1&amp;scene=1&amp;srcid=0219MbIRFZqZIFvc7REAuGjw&amp;sharer_shareinfo=8695de2c6b6f528dfc839eb46d098e1a&amp;sharer_shareinfo_first=8695de2c6b6f528dfc839eb46d098e1a#rd
发布时间: ""
收藏时间: "2025-02-19"
关联日记: "[[2025-02-19]]"
tags:
  - 文章
---
![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67b55a6c0537f80c2fab5d53/ff2f56fa-98b0-46a7-a213-914c2c50fcdf.gif)

开发基于大模型的软件应用，就像指挥一支足球队：**组件**是能力各异的队员，**编排**是灵活多变的战术，**数据**是流转的足球。

Eino 是字节跳动开源的大模型应用开发框架，拥有稳定的内核，灵活的扩展性，完善的工具生态，可靠且易维护，背靠豆包、抖音等应用的丰富实践经验。初次使用 Eino，就像接手一支实力雄厚的足球队，即使教练是初出茅庐的潜力新人，也可以踢出高质量、有内容的比赛。

下面就让我们一起踏上新手上路之旅！

**认识队员**

Eino 应用的基本构成元素是功能各异的组件，就像足球队由不同位置角色的队员组成：

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67b55a6c0537f80c2fab5d53/42d7f32c-4638-4822-ad71-2e7b28339445.webp)

这些组件抽象代表了固定的输入输出类型、Option 类型和方法签名：

```
type ChatModel interface {
    Generate(ctx context.Context, input []*schema.Message, opts ...Option) (*schema.Message, error)
    Stream(ctx context.Context, input []*schema.Message, opts ...Option) (
       *schema.StreamReader[*schema.Message], error)
    BindTools(tools []*schema.ToolInfo) error
}
```

真正的运行，需要的是具体的组件**实现**：

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67b55a6c0537f80c2fab5d53/c873f7cc-6c0c-471b-b218-eaa23826a37b.webp)

Eino 的开发过程中，首先要做的是决定 “我需要使用哪个组件抽象”，再决定 “我需要使用哪个具体组件实现”。就像足球队先决定 “我要上 1 个前锋”，再挑选 “谁来担任这个前锋”。

组件可以像使用任何的 Go interface 一样单独使用。但要想发挥 Eino 这支球队真正的威力，需要多个组件协同编排，成为一个相互联结的整体。

**制定战术**

在 Eino 编排场景中，每个组件成为了 “节点”（Node），节点之间 1 对 1 的流转关系成为了 “边”（Edge），N 选 1 的流转关系成为了 “分支”（Branch）。基于 Eino 开发的应用，经过对各种组件的灵活编排，就像一支足球队可以采用各种阵型，能够支持无限丰富的业务场景。

足球队的战术千变万化，但却有迹可循，有的注重控球，有的简单直接。对 Eino 而言，针对不同的业务形态，也有更合适的编排方式：

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67b55a6c0537f80c2fab5d53/f2bf90ee-a225-4eb3-a24b-0fecd97dedd8.webp)

Chain，如简单的 ChatTemplate + ChatModel 的 Chain：

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67b55a6c0537f80c2fab5d53/86c4e8ed-1601-42ea-a624-42e6b86373bf.webp)

```
chain, _ := NewChain[map[string]any, *Message]().
           AppendChatTemplate(prompt).
           AppendChatModel(model).
           Compile(ctx)
chain.Invoke(ctx, map[string]any{"query": "what's your name?"})
```

Graph，如 ReAct Agent：

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67b55a6c0537f80c2fab5d53/92c0ca67-005c-4a2d-bdfe-1e5d17bbd38d.webp)

```
graph := NewGraph[map[string]any, *schema.Message]()
_ = graph.AddChatTemplateNode("node_template", chatTpl)_ = graph.AddChatModelNode("node_model", chatModel)_ = graph.AddToolsNode("node_tools", toolsNode)_ = graph.AddLambdaNode("node_converter", takeOne)
_ = graph.AddEdge(START, "node_template")_ = graph.AddEdge("node_template", "node_model")_ = graph.AddBranch("node_model", branch)_ = graph.AddEdge("node_tools", "node_converter")_ = graph.AddEdge("node_converter", END)
compiledGraph, err := graph.Compile(ctx)if err != nil {    return err}out, err := r.Invoke(ctx, map[string]any{"query":"Beijing's weather this weekend"})
```

**了解工具**

现在想象下你接手的足球队用了一些黑科技，比如：在每个队员接球和出球的瞬间，身上的球衣可以自动的记录接球和出球的速度、角度并传递给场边的服务器，这样比赛结束后，就可以统计出每个队员触球的情况和处理球的时间。

在 Eino 中，每个组件运行的开始和结束，也可以通过 Callbacks 机制拿到输入输出及一些额外信息，处理横切面需求。比如一个简单的打日志能力：

```
handler := NewHandlerBuilder().
    OnStartFn(
       func (ctx context.Context, info *RunInfo, input CallbackInput) context.Context {
           log.Printf("onStart, runInfo: % v, input: % v", info, input)
           return ctx
    }).
    OnEndFn(
        func (ctx context.Context, info *RunInfo, output CallbackOutput) context.Context {
           log.Printf("onEnd, runInfo: % v, out: % v", info, output)
           return ctx
    }).
    Build()

// 注入到 graph 运行中
compiledGraph.Invoke(ctx, input, WithCallbacks(handler))
```

再想象一下，这个足球队的黑科技不止一种，还可以让教练在比赛前制作 “锦囊” 并藏在球衣里，当队员接球时，这个锦囊就会播放教练事先录制好的妙计，比如 “别犹豫，直接射门！”。

听上去很有趣，但有一个难点：有的锦囊是给全队所有队员的，有的锦囊是只给一类队员（比如所有前锋）的，而有的锦囊甚至是只给单个队员的。如何有效的做到锦囊妙计的分发？

在 Eino 中，类似的问题是 graph 运行过程中 call option 的分发：

```
// 所有节点都生效的 call optioncompiledGraph.Invoke(ctx, input, WithCallbacks(handler))
// 只对特定类型节点生效的 call optioncompiledGraph.Invoke(ctx, input, WithChatModelOption(model.WithTemperature(0.5)))
// 只对特定节点生效的 call optioncompiledGraph.Invoke(ctx, input, WithCallbacks(handler).DesignateNode("node_1"))
```

**发现独门秘笈**

现在，想象一下你的球队里有一些明星球员（中场大脑 ChatModel 和锋线尖刀 StreamableTool）身怀绝技，他们踢出的球速度如此之快，甚至出现了残影，看上去就像是把一个完整的足球切成了很多片！

面对这样的 “流式” 足球，对手球员手足无措，不知道该如何接球，但是你的球队的所有队员，都能够完美的接球，要么直接一个片一个片的接收 “流式” 足球并第一时间处理，要么自动的把所有片拼接成完整的足球后再处理。身怀这样的独门秘笈，你的球队具备了面对其他球队的降维打击能力！

在 Eino 中，开发者只需要关注一个组件在 “真实业务场景” 中，是否可以处理流式的输入，以及是否可以生成流式的输出。根据这个真实的场景，具体的组件实现（包括 Lambda Function）就去实现符合这个流式范式的方法：

```
// ChatModel 实现了 Invoke（输入输出均非流）和 Stream（输入非流，输出流）两个范式
type ChatModel interface {
    Generate(ctx context.Context, input []*Message, opts ...Option) (*Message, error)
    Stream(ctx context.Context, input []*Message, opts ...Option) (
       *schema.StreamReader[*Message], error)
}

// Lambda 可以实现任意四种流式范式

// Invoke is the type of the invokable lambda function.
type Invoke[I, O, TOption any] func(ctx context.Context, input I, opts ...TOption) (
    output O, err error)

// Stream is the type of the streamable lambda function.
type Stream[I, O, TOption any] func(ctx context.Context,
    input I, opts ...TOption) (output *schema.StreamReader[O], err error)

// Collect is the type of the collectable lambda function.
type Collect[I, O, TOption any] func(ctx context.Context,
    input *schema.StreamReader[I], opts ...TOption) (output O, err error)

// Transform is the type of the transformable lambda function.
type Transform[I, O, TOption any] func(ctx context.Context,
    input *schema.StreamReader[I], opts ...TOption) (output *schema.StreamReader[O], err error)
```

Eino 编排能力会自动做两个重要的事情：

1. 上游是流，但是下游只能接收非流时，自动拼接（Concat）。

2. 上游是非流，但是下游只能接收流时，自动流化（T -> StreamReader [T]）。

除此之外，Eino 编排能力还会自动处理流的合并、复制等各种细节，把大模型应用的核心 —— 流处理做到了极致。

**一场训练赛 -- Eino 智能助手**

好了，现在你已经初步了解了 Eino 这支明星球队的主要能力，是时候通过队员 (组件)、战术 (编排)、工具 (切面、可视化) 来一场训练赛，去亲自体验一下它的强大。

**场景设定**

Eino 智能助手：根据用户请求，从知识库检索必要的信息并按需调用多种工具，以完成对用户的请求的处理。工具列表如下：

- DuckDuckGo：从 DuckDuckGo 搜索互联网信息
- EinoTool：获取 Eino 的工程信息，比如仓库链接、文档链接等
- GitClone：克隆指定仓库到本地
- 任务管理 (TaskManager)：添加、查看、删除 任务
- OpenURL：使用系统的默认应用打开文件、Web 等类型的链接


这里呈现一个 Demo 样例，大家可根据自己的场景，更换自己的知识库和工具，以搭建自己所需的智能助手。

先来一起看看**基于 Eino 搭建起来**的 Agent 助手能实现什么效果：

构建这个 Eino 智能助手分两步：

- Knowledge Indexing（索引知识库）：将我们在特定领域沉淀的知识，以分词、向量化等多种手段，构建成索引，以便在接收用户请求时，索引出合适的上下文。本文采用向量化索引来构建知识库。
- Eino Agent（Eino 智能助手）：根据用户的请求信息以及我们预先构建好的可调用的工具，让 ChatModel 帮我们决策下一步应该执行什么动作或输出最终结果。Tool 的执行结果会再次输入给 ChatModel，让 ChatModel 再一次判断下一步的动作，直至完成用户的请求。


**任务工作流**

**索引知识库 (Knowledge Indexing)**

将 Markdown 格式的 Eino 用户手册，以合适的策略进行拆分和向量化，存入到 RedisSearch 的 VectorStore 中，作为 Eino 知识库。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67b55a6c0537f80c2fab5d53/1d2ab517-6894-48ea-a257-ae2321199522.webp)

**Eino 智能体 (Eino Agent)**

根据用户请求，从 Eino 知识库召回信息，采用 ChatTemplate 构建消息，请求 React Agent，视需求循环调用对应工具，直至完成处理用户的请求。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67b55a6c0537f80c2fab5d53/26576d0f-4c0c-4d81-a9f3-2a30a8c931a6.webp)

**所需工具**

在从零开始构建「Eino 智能助手」这个实践场景中，需要下列工具：

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67b55a6c0537f80c2fab5d53/be770091-c14a-496d-ac5a-5a8888ade6a9.webp)

**索引知识库**

> 示例的仓库路径：https://github.com/cloudwego/eino-examples/tree/main/quickstart/eino_assistant下文中，采用相对于此目录的相对路径来标识资源位置

构建一个命令行工具，递归遍历指定目录下的所有 Markdown 文件。按照标题将 Markdown 文件内容分成不同的片段，并采用火山云的豆包向量化模型逐个将文本片段进行向量化，存储到 Redis VectorStore 中。 

> 指令行工具目录：cmd/knowledge_indexingMarkdown 文件目录：cmd/knowledge_indexing/eino-dcos

开发「索引知识库」应用时，首先采用 Eino 框架提供的 Goland EinoDev 插件，以可视化拖拽和编排的形式构建 KnowledgeIndexing 的核心应用逻辑，生成代码到 eino_graph/knowledge_indexing 目录。

代码生成后，首先手动将该目录下的各组件的构造方法补充完整，然后在业务场景中，调用 BuildKnowledgeIndexing 方法，构建并使用 Eino Graph 实例。

接下来将逐步介绍，KnowledgeIndexing 的开发过程：

**大模型资源创建**

火山引擎是字节跳动的云服务平台，可从中注册和调用豆包大模型（有大量免费额度）。

- 创建 doubao-embedding-large 作为知识库构建时的向量化模型，以及创建 doubao-pro-4k 资源作为 agent 对话时的模型。
- 「火山引擎在线推理」：https://console.volcengine.com/ark


![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67b55a6c0537f80c2fab5d53/6dc7d24e-bfee-466b-adda-c9c00814c859.gif)

**启动 Redis Stack**

本文将使用 Redis 作为 Vector Database，为方便用户构建环境，Docker 的快捷指令如下：

- 在 eino-examples/quickstart/eino_assistant 提供 docker-compose.yml
- 在 eino-examples/quickstart/eino_assistant/data 目录下提供了 Redis 的初始知识库


直接用 redis 官方的 redis stack 镜像启动即可

```
# 切换到 eino_assistant 目录cd xxx/eino-examples/quickstart/eino_assistant
docker-compose up -d
```

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67b55a6c0537f80c2fab5d53/91826f5a-bd66-47ef-90a5-828fe46e9660.gif)

- 完成启动后，打开本地的 8001 可进入 redis stack 的 web 界面


```
在浏览器打开链接：http://127.0.0.1:8001
```

**可视化开发**

> 「Eino 可视化开发」是为了降低 Eino AI 应用开发的学习曲线，提升开发效率。对于熟悉 Eino 的开发者，也可选择跳过「Eino 可视化开发」阶段，直接基于 Eino 的 API 进行全码开发。

1. 安装 EinoDev 插件，并打开 Eino Workflow 功能

- Graph name: KnowledgeIndexing
- Node trigger mode: Triggered after all predecessor nodes are executed
- Input type: document.Source
- Import path of input type: github.com/cloudwego/eino/components/document
- Output type: [] string
- 其他置空


![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67b55a6c0537f80c2fab5d53/079aa8fa-c2a8-42fc-a1d5-a0bf3a9c5c82.webp)

2. 按照上文**「索引知识库」**中的流程说明，从 Eino Workflow 中选择需要使用的组件库，本文需要用到如下组件： 

- document/loader/file —— 从指定 URI 加载文件，解析成文本内容，以 schema.Document 列表形式返回。
- document/transformer/splitter/markdown —— 将从 FileLoader 中加载到的文本内容，进一步拆分成合适的大小，以平衡向量化计算 / 存储的尺寸限制和召回的效果。
- indexer/redis —— 将 schema.Document 的原文、索引字段 存储在 Redis Vector Database 中
- embedding/ark —— 采用 Ark 平台的向量化模型，对 schema.Document 中的 Content 等内容进行向量化计算


3. 将选中的组件按照预期的拓扑结构进行编排，完成编排后，点击 “生成代码” 到指定目录。

- **「索引知识库」**的代码生成到：eino_assistant/eino/knowledgeindexing
- 本示例可直接复制 eino/knowledge_indexing.json 中的 Graph Schema，来快速构建示例中的图


![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67b55a6c0537f80c2fab5d53/b04a937a-e28d-44cb-a8b7-21ee087084ae.webp)

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67b55a6c0537f80c2fab5d53/a71926f8-981b-4fa7-8812-254163ad4008.webp)

4. 按需完善各个组件的构造函数，在构造函数中补充创建组件实例时，需要的配置内容

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67b55a6c0537f80c2fab5d53/08151824-7dbc-487b-8534-ad1ce0ec0a8d.webp)

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67b55a6c0537f80c2fab5d53/f5f39925-64a8-4e5d-a6f7-cc40de3e4052.webp)

5. 补充好组件的配置内容后，即可调用 BuildKnowledgeIndexing 方法，在业务场景使用

**完善代码**

- 通过可视化开发，生成的 Eino 编排代码，无法保证可直接使用，需要人工阅读和检查下代码的完整性
- 生成核心函数是 BuildKnowledgeIndexing ()，用户可在需要的地方调用此方法，创建实例进行使用


在「索引知识库」的场景下，需要将 BuildKnowledgeIndexing 封装成一个指令，从环境变量中读取模型配置等信息，初始化 BuildKnowledgeIndexing 的配置内容，扫描指定目录下的 Markdown 文件，执行对 Markdown 进行索引和存储的操作。

> 详细代码可查看：cmd/knowledgeindexing/main.go

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67b55a6c0537f80c2fab5d53/0a311549-9bb1-4839-9669-567d3ef2ed9a.webp)

**运行**

> PS: 示例项目中，已经内置了 eino 的一部分文档向量化到 redis 中

1. 在 .env 文件中按照注释说明，获取并填写 ARK_EMBEDDING_MODEL 和 ARK_API_KEY 的值，按如下指令，运行 KnowledgeIndexing 指令

```
cd xxx/eino-examples/quickstart/eino_assistant # 进入 eino assistant 的 example 中
# 修改 .env 中所需的环境变量 (大模型信息、trace 平台信息)source .env
# 因示例的Markdown文件存放在 cmd/knowledgeindexing/eino-docs 目录，代码中指定了相对路径 eino-docs，所以需在 cmd/knowledgeindexing 运行指令cd cmd/knowledgeindexinggo run main.go
```

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67b55a6c0537f80c2fab5d53/e8e94e66-db1e-4cc5-801e-9d1cc42eee04.gif)

2. 执行运行成功后，即完成 Eino 知识库的构建，可在 Redis Web UI 中看到向量化之后的内容

> 在浏览器打开链接：http://127.0.0.1:8001

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67b55a6c0537f80c2fab5d53/6bb27d30-ec47-4835-9e59-a76da92d8509.webp)

**Eino 智能体**

> 示例的仓库路径：https://github.com/cloudwego/eino-examples/tree/main/quickstart/eino_assistant下文中，采用相对于此目录的相对路径来标识资源位置

构建一个基于从 Redis VectorStore 中召回的 Eino 知识回答用户问题，帮用户执行某些操作的 ReAct Agent，即典型的 RAG ReAct Agent。可根据对话上下文，自动帮用户记录任务、Clone 仓库，打开链接等。 

**大模型资源创建**

继续使用「索引知识库」章节中创建的 doubao-embedding-large 和 doubao-pro-4k

**启动 RedisSearch**

继续使用「索引知识库」章节中启动的 Redis Stack

**可视化开发**

1. 打开 EinoDev 插件，进入到 Eino Workflow 页面，新建一张画布

- Graph Name: EinoAgent
- Node Trigger Mode: Triggered after all predecessor nodes are executed
- Input Type Name: *UserMessage
- Input Package Path: ""
- Output Type Name: *schema.Message
- Output Import Path: github.com/cloudwego/eino/schema
- 其他置空


2. 按照上文**「Eino 智能体」**中的流程说明，从 Eino Workflow 中选择需要使用的组件库，本文需要用到如下组件：

- lambda: 将开发者任意的函数 func (ctx context.Context, input I) (output O, err error)，转换成可被编排的节点，在 EinoAgent 中，有两个转换场景：


（1）将 *UserMessage 消息转换成 ChatTemplate 节点的 map [string] any

（2）将 *UserMessage 转换成 RedisRetriever 的输入 query

- retriever/redis —— 根据用户 Query 从 Redis Vector Database 根据语义相关性，召回和 Query 相关的上下文，以 schema.Document List 的形式返回。
- prompt/chatTemplate —— 通过字符串字面量构建 Prompt 模板，支持 文本替换符 和 消息替换符，将输入的任意 map [string] any，转换成可直接输入给模型的 Message List。
- flow/agent/react —— 基于开发者提供的 ChatModel 和 可调用的工具集，针对用户的问题，自动决策下一步的 Action，直至能够产生最终的回答。 
- model/ark —— Ark 平台提供的能够进行对话文本补全的大模型，例如豆包模型。作为 ReAct Agent 的依赖注入。
- 可调用的工具列表——互联网搜索工具 (DuckDuckGo)、EinoTool、GitClone、任务管理 (TaskManager)、 OpenURL


3. 将选中的组件按照预期的拓扑结构进行编排，完成编排后，点击 “生成代码” 到指定目录。

- 本示例中，**「Eino 智能体」**的代码生成到：eino/einoagent


![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67b55a6c0537f80c2fab5d53/0f9cc01a-9b8c-4229-a06c-c442ad00269b.webp)

- 本示例可直接复制 eino/eino_agent.json 中的 Graph Schema，来快速构建示例中的图


![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67b55a6c0537f80c2fab5d53/905f4101-2207-4e69-814b-7b9c7f83cbca.webp)

4. 按需完善各个组件的构造函数，在构造函数中补充创建组件实例时，需要的配置内容

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67b55a6c0537f80c2fab5d53/4ffdbd09-2944-40e9-ab75-930873cdfc03.webp)

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67b55a6c0537f80c2fab5d53/43f6fb40-4ca9-44d9-95cb-2342d15eea64.webp)

5. 补充好组件的配置内容后，即可调用 BuildEinoAgent 方法，在业务场景使用

**完善代码**

在「Eino 智能体」的场景下，BuildEinoAgent 构建的 Graph 实例可做到：根据用户请求和对话历史，从 Eino 知识库中召回上下文， 然后结合可调用的工具列表，将 ChatModel 循环决策下一步是调用工具或输出最终结果。 

下图即是对生成的 BuildEinoAgent 函数的应用，将 Eino Agent 封装成 HTTP 服务接口：

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67b55a6c0537f80c2fab5d53/2042120c-85fb-4728-998b-1fe6c2d21244.webp)

**运行**

1. 在 .env 文件中按照注释说明，获取并填写对应各变量的值，按如下指令，启动 Eino Agent Server

```
cd eino-examples/eino_assistant # 进入 eino assistant 的 example 中
# 修改 .env 中所需的环境变量 (大模型信息、trace 平台信息)source .env
# 为了使用 data 目录，需要在 eino_assistant 目录下执行指令go run cmd/einoagent/*.go
```

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67b55a6c0537f80c2fab5d53/c51fa991-9a9e-4708-ba90-bdcb661bc592.gif)

2. 启动后可访问如下链接，打开 Eino Agent Web

> Eino Agent Web：http://127.0.0.1:8080/agent/

**观测 (可选)**

如果在运行时，在 .env 文件中指定了 LANGFUSE_PUBLIC_KEY 和 LANGFUSE_SECRET_KEY，便可在 Langfuse 平台中，登录对应的账号，查看请求的 Trace 详情。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67b55a6c0537f80c2fab5d53/2c2f5d68-d11c-4c37-ae38-916283b4d08a.gif)

*相关链接：*

*项目地址：https://github.com/cloudwego/eino，https://github.com/cloudwego/eino-ext*

*Eino 用户手册：https://www.cloudwego.io/zh/docs/eino/*

*项目官网：https://www.cloudwego.io*

