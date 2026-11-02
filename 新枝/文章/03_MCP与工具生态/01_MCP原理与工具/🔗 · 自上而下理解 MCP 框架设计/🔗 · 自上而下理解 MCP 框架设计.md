---
作者:
  - "蛮荆"
原文链接: https://mp.weixin.qq.com/s?__biz=MzI1MzI3OTA5OQ==&amp;mid=2247489345&amp;idx=1&amp;sn=bba2d29d9eed3cff332c3bef3812523c&amp;chksm=e889e2b1fa4dea637ff01e8424acc4245d68cc1e769781196a037b229d1b3e53b8a2ab2c65eb&amp;mpshare=1&amp;scene=1&amp;srcid=0610Y0GQm7ov9fHdaFkEFVwn&amp;sharer_shareinfo=3d8deaf36817b6f125393278c93ae892&amp;sharer_shareinfo_first=3d8deaf36817b6f125393278c93ae892#rd
发布时间: ""
收藏时间: "2026-06-10"
关联日记: "[[2026-06-10]]"
tags:
  - 文章
---
## 1. 定位

> MCP（Model Context Protocol），模型上下文协议，是一个开源标准，用于将 AI 应用和外部系统连接起来。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6a28b62ea671ad09c217abae/7269e747-5a8a-4386-b53b-92470d5733e7.png)

图片来源: https://modelcontextprotocol.io

在 MCP 出现之前，每个 LLM, AI 应用都在重复发明轮子。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6a28b62ea671ad09c217abae/1e569e73-c2c7-486c-b487-2904df642168.png)

如果有 N 个应用，每个应用定义 N 套接口格式，那么最终的系统集成就会混乱低效，成本复杂度变为：

MCP 通过分层，将 LLM 与外部系统集成的具体细节进行解耦，成本复杂度 (近似) 优化为：

所以，MCP 的本质就是 **一套标准化的 LLM 与外部系统的交互规范**。

## 2. 核心概念

MCP 也采用客户端 - 服务端架构，对于服务端 (一般指外部系统) 来说，需要将自身可以提供的功能，暴露三个核心能力，让上层 Agent/客户端 按 MCP 发现并调用。

### 2.1 四个角色

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6a28b62ea671ad09c217abae/027bb067-1174-40ee-b7f3-57136083ced0.png)

1. **Host** : 发起请求的 LLM 应用（例如 Claude Code Cli、Cursor 等）
2. **Client** : Host 内部连接 MCP Server 的协议客户端
3. **Server** : 对外暴露能力的服务端服务
4. **LLM** : 决策引擎，决定调用服务端的哪些能力


### 2.2 三个能力

1. **Tool**: 更偏向 “写操作”，Agent 可以直接调用的操作（例如文件操作、API 调用、数据库 CRUD）
2. **Resource**: 更偏向 “可读取的数据或上下文”，Agent 拉取数据作为上下文输入（例如文件内容、数据库记录、API 响应）
3. **Prompt**: prompt 的可复用模板，**预置的结构化提示词，封装复杂指令，保证输出格式一致性**，主要供 LLM 加载后按框架输出，Agent 加载后可以让 LLM 按模板结构输出 （例如系统提示、少数样本示例）


通过这种对 LLM 更加友好的能力划分方式，保证 LLM / Agent 在使用外部系统时，不会把数据读取和操作执行混在一起，更不可能把 prompt 当作接口参数调用。MCP 的核心价值并不仅仅是 “让模型能够调用工具”，而是 “让模型能够发现可调用的工具，并理解它们的结构化语义”，让 LLM 充分自主决策，尽可能充分做到 **工具可调用 -> 工具可发现 -> 工具可正确使用**。

### 2.3 生命周期

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6a28b62ea671ad09c217abae/8c5c3e10-9a7e-4e76-a414-2a8b751699bf.png)

1. 初始化阶段，Client 请求 Server 支持的协议版本和能力集合
2. 发现阶段，Client 获取 Server 的 schema 列表，主要就是感知 Server 的三个能力的具体细节
3. 执行阶段，LLM 进行决策，然后 Client 发起对应的调用，Server 执行后返回结果
4. 关闭阶段，Client 主动发起关闭，具体行为取决于传输模式：stdio 模式下直接终止子进程；SSE 模式下断开 HTTP 连


### 2.4 框架设计

从框架设计的角度来看，MCP Server 的核心工作可以拆解为三件事：

1. 能力注册


框架通过装饰器/注解方式，将普通方法注册为 MCP 能力，然后在启动初始化时扫描所有注册项，收集方法名、docstring、参数类型注解，就像一份结构化的能力清单，让 LLM 在决策时参考。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6a28b62ea671ad09c217abae/f30b5546-e883-47b0-a82d-ed3d0a53843e.png)

1. Schema 自动生成


框架利用语言运行时特性 (例如反射/类型检查机制)，将方法的参数签名自动转换为 JSON Schema。

例如：

```
def create_issue(title: str, label: str = "bug") -> dict:
    """创建一个新的 Issue。"""
```

自动生成 JSON Schema：

```
{
  "name": "create_issue",
  "description": "创建一个新的 Issue。",
  "inputSchema": {
    "type": "object",
    "properties": {
      "title": { "type": "string" },
      "label": { "type": "string", "default": "bug" }
    },
    "required": ["title"]
  }
}
```

这段 Schema 就是 LLM 理解 Server 能力的唯一依据，LLM 并不关注方法内部做了什么，它只 “理解” 这段 JSON 描述。

1. 请求路由与执行


当 Client 发送 `Tool / Resource` 请求时，框架根据 name 字段路由到对应的方法，将调用参数解码为方法参数，执行后将返回值编码为标准响应格式。这个过程与传统 Web 框架的请求-路由-处理-响应模型基本一致。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6a28b62ea671ad09c217abae/434233ca-05ac-4341-a285-f383aff70800.png)

## 3. 网络协议栈

MCP 直接在传统 OSI / TCP-IP 的应用层之上，**建立了一层新的标准化抽象**，本质上还是应用层，只是 “应用对象” 从Web 客户端变成了 LLM / Agent。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6a28b62ea671ad09c217abae/833cafed-e366-49fc-90cc-2f03a2d8844f.png)

### 3.1 传输模式

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6a28b62ea671ad09c217abae/de000a5c-57ac-4c57-aed2-818eb7988960.jpeg)

MCP 支持三种传输模式：

1. **stdio 模式**


最常见的本地开发模式之一。

Host 把 MCP server 当作子进程启动，通过标准输入输出通信，我们日常使用的 Coding Agent 大多属于这个模式。

1. **SSE 模式**


主要用于云端 LLM 工具的场景，Client 先发送请求，然后持续接收 Server 的数据推送。

1. **Streamable HTTP**


远程双向流式（逐步替代 SSE），本质是：普通 HTTP POST 请求 + 可选的 SSE 响应流，服务端可以根据需要决定返回单次响应还是流式推送。

### 3.2 标准方法

`initialize`协议版本协商Client → Server`tools/list`获取工具列表Client → Server`tools/call`调用工具Client → Server`resources/list`获取资源列表Client → Server`resources/read`读取资源内容Client → Server`resources/subscribe`订阅资源变更Client → Server`prompts/list`获取提示词列表Client → Server`prompts/get`获取提示词内容Client → Server`notifications/xxx`推送Server → Client`logging/setLevel`设置日志级别Server → Client

### 3.3 消息层

RESTful API 用 URL 路径 + HTTP Method 表达语义的方式。

而 MCP 采用 JSON-RPC 2.0 作为消息数据模型，所有请求统一通过同一个端点发送，通常由 HTTP 请求承载 JSON-RPC 消息体，请求都是 POST，通过 method 字段区分不同的操作类型。

1. Request（请求）


```
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "create_issue",
    "arguments": { "title": "登录页布局错乱" }
  }
}
```

1. Response（响应）


```
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "content": [{ "type": "text", "text": "{\"id\": 1, \"status\": \"open\"}" }]
  }
}
```

1. Notification（通知，无需响应）


```
{
  "jsonrpc": "2.0",
  "method": "notifications/progress",
  "params": { "progressToken": "task-1", "progress": 50 }
}
```

MCP 不使用 4xx/5xx 状态码表达错误语义，错误处理遵循 JSON-RPC 2.0 规范，使用标准的 error 对象：

```
{
  "jsonrpc": "2.0",
  "id": 1,
  "error": {
    "code": -32602,
    "message": "Invalid arguments: 'title' is required",
    "data": { "field": "title" }
  }
}
```

### 3.4 框架设计

从消息协议的角度来看，MCP 的通信模型非常简洁，只有三种消息类型，框架层面对于消息的处理，几乎只需要实现编码和解码即可。MCP 核心目标解决的是 "通信标准化" 问题，而不是 "业务实现 (已有框架已经实现)" 问题。

## 4. 和传统开发框架的差异

MCP 并不是传统 Web 框架的替代品，而是在 LLM 应用层之上建立的**新一层标准化抽象**，也就是套了个壳儿。

传统的框架甚至不需要大的改造，直接 “简单支持” 一下 MCP 即可，例如 Spring 直接内置了 MCP Server/Client 模块，简单配置即可使用。

Standard MCP Client 配置

```
<dependency>
    <groupId>org.springframework.ai</groupId>
    <artifactId>spring-ai-starter-mcp-client</artifactId>
</dependency>
```

STDIO MCP Server 配置

```
<dependency>
    <groupId>org.springframework.ai</groupId>
    <artifactId>spring-ai-starter-mcp-server</artifactId>
</dependency>
```

### 4.1 保留特性

同时，传统的框架可以直接使用已有的机制，直接映射到 MCP 框架的设计理念，实现无缝衔接，相当于增加一层 “装饰器”。

还是以 Spring 框架为例：

`@mcp.tool()``@Tool` 注解（Spring AI）`@mcp.resource()``@McpResource``@mcp.prompt()``@McpPrompt`

再比如，传统框架中的文档生成 (Swagger / OpenAPI), 在 MCP 中通过 Tool Schema 自动生成即可。

Spring 框架原有的能力几乎可以全部复用，不需要重新造轮子。这也反向证明了：MCP 没有引入任何 Spring 无法表达的新概念， 只是在框架的已有能力上，套了一层标准化的应用协议外壳。

### 4.2 新增特性

传统框架的接口/文档描述，主要面向开发者阅读。MCP 生成的能力描述，主要给 LLM 看（docstring -> JSON Schema）, docstring 的质量直接影响 LLM 的调用准确率。

传统框架所有的 API 接口统一为 HTTP 端点，用 GET/POST 等 HTTP Method 区分读写操作语义，MCP 直接在协议层强制区分 Tool, Resource, Prompt, 主要目的是针对 LLM 决策时，给予更明确的语义引导。

### 4.3 委托外部处理的特性

身份认证（JWT/Session）委托给传输层（HTTPS/进程隔离）RESTful 资源设计（CRUD）被 Tool/Resource 二元模型替代HTTP 状态码语义统一用 JSON-RPC error 对象表达版本化 URL（/v1/v2）通过 initialize 握手协商版本分页、过滤、排序等业务参数并不替代业务参数设计，虽然由 LLM 决策，但是仍然需要通过 schema 明确暴露

### 4.4 框架设计

MCP 不定义认证机制，不定义分页规范，不定义错误码体系，这些全部委托给已有的开发框架。

MCP 也不执行任何业务逻辑，只是一个纯粹的 "注册-发现-路由-编码解码" 中间层，真正的业务逻辑在开发者编写的业务 Tool/Resource 方法中，LLM 的决策逻辑在 Host 端，MCP 就只是负责让两边搭上话。

## 5. 总结

设计一个 MCP 框架的角度来看，需要实现以下模块：

协议解析JSON-RPC 2.0 消息的编码 / 解码传输适配屏蔽 stdio / SSE / Streamable HTTP 的差异能力注册中心维护 Tool / Resource / Prompt 的注册表Schema 生成器从方法签名 + 注释自动生成 JSON Schema生命周期管理器握手、心跳、优雅关闭错误处理器统一将业务异常转换为 JSON-RPC error 对象

MCP 不需要解决的问题：

- LLM 推理质量，主要由模型本身决定
- Tool / Resource 执行的幂等性，由业务代码保证
- 多 Agent 协作，由 A2A 等协议负责
- 限流 / 熔断，由基础框架设施负责


![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6a28b62ea671ad09c217abae/5450a51a-98c5-42fe-84dd-095b33174546.jpeg)

自上而下地从完整设计视角来看，MCP 框架的设计与传统中间件（如消息队列、API Gateway）的定位类似，只是单纯地搬运数据，再加一层 “元信息” 描述，指导 LLM 的自主决策，除此之外的其他所有工作，全部交给已有的基础框架。反过来说，传统框架适配 MCP 的改造成本极低，核心工作只是在已有方法上加注解，适配数据的编码、解码、传输即可。

