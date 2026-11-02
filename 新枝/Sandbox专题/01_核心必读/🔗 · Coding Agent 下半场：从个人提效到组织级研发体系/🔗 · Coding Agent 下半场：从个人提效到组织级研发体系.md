---
作者:
  - "阿里云云原生"
原文链接: https://mp.weixin.qq.com/s?__biz=MzUzNzYxNjAzMg==&amp;mid=2247584473&amp;idx=1&amp;sn=dd31a7e2ba152010135590eb091d12a7&amp;chksm=fbfa27a36bf18100267a35dea33a34bec9e856c3fedf782b49940ad5c9ebe0305ac35548110c&amp;mpshare=1&amp;scene=1&amp;srcid=061298N3Qnp0lKHk2YkwQ8Sp&amp;sharer_shareinfo=5bc9008af8fcb09737abec0f9cb9eb1d&amp;sharer_shareinfo_first=5bc9008af8fcb09737abec0f9cb9eb1d#rd
发布时间: ""
收藏时间: "2026-06-12"
关联日记: "[[2026-06-12]]"
tags:
  - 文章
---
当下还在古法手搓代码的开发者都是在奔着非遗传承人的目标去了，绝大多数都已经用上了 Claude Code、Cursor 这类 Coding Agent。方向对了，但场景不同，解法也不同 —— 开发者自己在本地装个 AI 助手提效，和在组织内部搭起一套 AI 驱动的研发协作体系，是完全两个维度的事情。前者已经有成熟的产品了，后者才刚刚开始。本文聊的就是后者。

***什么是组织级 Coding Agent，***

***都有谁在做？***

*Cloud Native*

2025 年底到 2026 年初，一件有意思的事情发生了：Stripe、Ramp、Coinbase 这三家公司几乎同时公开了各自的内部 Coding Agent —— Stripe 叫 Minions，Ramp 叫 Inspect，Coinbase 叫 Cloudbot。三家公司独立开发，没有互相参考，最终却不约而同地收敛到了几乎相同的架构上。

这不是巧合。当你把 Coding Agent 从“一个人在终端里用”升级成“整个团队通过 Slack / GitHub Issue 随时触发”，你就会被同一组工程问题逼到同一条路上去——你需要沙箱隔离执行环境，需要让 Agent 在中断后能续上之前的工作，需要让它接得住 Slack、GitHub、飞书各种入口，需要防止一个用户的失控循环把全公司的模型额度烧光。

LangChain 团队看到了这个规律。2026 年 3 月，他们发布了 Open SWE—— 一个把 Stripe/Ramp/Coinbase 的共同模式提炼成开源框架的项目。Open SWE 的 README 开头写得很直接：

> Elite engineering orgs like Stripe, Ramp, and Coinbase are building their own internal coding agents — Slackbots, CLIs, and web apps that meet engineers where they already work.

"Meet engineers where they already work" —— 这句话点出了组织级 Coding Agent 的核心设计理念：不是让工程师学一个新工具，而是让 Agent 钻进工程师已经在用的 Slack 频道、GitHub Issue、IM 对话里，变成团队工作流的一部分。

AgentScope Java 2.0 的 AgentScope Harness 模块走的是同一条路。本文以官方示例 agentscope-examples/agents/agentscope-codingagent 为线索，讲清楚一个生产级 Coding Agent 是怎么用 Harness 拼出来的 —— 每一行配置解决了什么问题，怎么从本地 CLI 一路演进到挂在 GitHub Webhook 后面的企业服务。

***先把定位说清楚***

*Cloud Native*

在往下走之前，必须把“我们要做的”和“Claude Code / Cursor 这类本地工具”区分清楚。

Claude Code 优化的是“我一个人写代码更快” —— 你打字、它干活、你看着它干活、你随时打断纠正。状态在你本机，触发者就是你自己，信任边界就是你信你自己的机器。

本文要搭的东西解决的是另一个问题：“**团队里某个小任务我都不用自己看，扔给 Agent 跑完开 PR 我 review 一下就行”**。触发者可能是任何一个 Issue 评论者，Agent 在远端跑十几分钟到一小时，没人盯着。Stripe 的工程师在 Slack 里 @Minions 说句“帮我修这个 bug”，回头收到一个 draft PR —— 这就是组织级 Coding Agent 该有的样子。

这两种形态在功能集上有交集 —— 都能写代码、跑命令、改文件，但底层的工程约束完全不同。一个类比：Claude Code 是你自己的私家车，你信任驾驶员（你自己），所以不需要安全气囊以外的防护。组织级 Coding Agent 是出租车公司的运营车辆 —— 乘客（触发者）不是车主，驾驶（执行）发生在远端，你需要行车记录仪、GPS 追踪、里程限制、紧急制动，还得保证一辆车坏了不影响整个车队。

Open SWE 把这个哲学总结成一句话：**"Isolate first, then give full permissions inside the boundary."**先隔离，再放权。AgentScope Harness 的设计一模一样。

### ▍那厂商的 Cloud Agent 呢？

事实上很多厂商也在提供 SaaS 的产品服务，比如 GitHub Copilot Coding Agent 已经可以在 Issue 上 assign 触发，在云端跑完自动开 draft PR；Claude Code 也有 headless 模式，能在 CI 里被程序化调用。

理念上没有本质区别 —— 沙箱隔离、异步触发、PR 驱动产出 —— 厂商是把头部公司验证过的模式产品化了，做成了开箱即用的 SaaS 服务。而 Stripe、Ramp、Coinbase 这些公司选择自建，更多是出于自身工程体系的特殊性：内部系统的深度集成、数据合规的要求、工作流的定制程度，这些因素让它们走了自建这条路。

两条路不矛盾，哪条更合适，取决于组织自身的约束和需求。AgentScope Harness 要做的事情是把实现这套系统的工程问题（如沙箱、会话恢复、多通道接入、长期记忆等）抽象成可组合的基础能力，让选择自建的团队不用从零开始。

***5 分钟跑通：先有感性认识***

*Cloud Native*

最快的体验路径 —— 一个环境变量、一个 Maven 命令，本地文件系统上跑一个交互式 REPL。无需 Docker、无需 webhook、无需 GitHub App。

```
# 1. 设置模型 key（默认 DashScope；OpenAI / Anthropic 也支持）
export DASHSCOPE_API_KEY=sk-...
# 2. 在仓库根目录构建依赖（之后跑可以省略）
cd agentscope-java
mvn install -pl agentscope-examples/agents/agentscope-codingagent -am -DskipTests -q
# 3. 启动 CLI
mvn exec:java -pl agentscope-examples/agents/agentscope-codingagent
```

启动后会出 banner，然后到You>提示符。Agent 工作在自己的 workspace~/.agentscope/codingagent/workspace/—— 标准玩法是把目标仓库克隆进来再操作：

```
You> write hello.txt with a haiku about Java
You> clone https://github.com/owner/repo into the workspace and tell me what it does
You> review https://github.com/owner/repo/pull/42
You> /exit
```

什么都没配，跑起来就有完整的工作区、会话持久化和长期记忆。这是 AgentScope Harness 价值的第一层。

想让每个 session 隔离到 Docker 沙箱？多一步：

```
docker build \
  -t agentscope/coding-sandbox:latest \
  agentscope-examples/agents/agentscope-codingagent/src/main/docker/coding-sandbox/
export SANDBOX_TYPE=docker
mvn exec:java -pl agentscope-examples/agents/agentscope-codingagent
```

这就引出了组织级 Coding Agent 真正的工程核心。

***真正的难题：从“能跑一次”***

***到“7×24 服务一个团队”***

*Cloud Native*

跑通一个 demo 很快。难的是让它在生产环境里稳定地服务一整个团队，一天接几十个 Issue、几十个 PR，每个都跑到底、不串台、不爆内存、不烧穿额度。

这些工程难题，Stripe、Ramp、Coinbase 各自踩了一遍坑，Open SWE 在框架层做了一层抽象，AgentScope Harness 也给出了自己的解法。下面我们按问题域展开。

### ▍沙箱：让 Agent 可以放心 rm -rf

Coding Agent 最大的工程矛盾是：你要让模型有真正的执行能力——git clone、npm install、mvn test、任意 shell 命令 —— 但又不能让它误伤宿主。

Coinbase 用自建的沙箱基础设施解决这个问题。Ramp 用 Modal 的云端容器。Open SWE 做了一层抽象，支持 Modal、Daytona、Runloop 等多种后端。AgentScope Harness 也做了同样的抽象 —— FilesystemSpec 是统一接口，Docker 容器、远端 KV、本机文件系统都是可插拔的实现。以 Docker 后端为例：

```
HarnessAgent agent = HarnessAgent.builder()
    .name("coding")
    .model(model)
    .workspace(workspace)
    .filesystem(new DockerFilesystemSpec()
        .image("agentscope/coding-sandbox:latest")
        .isolationScope(IsolationScope.SESSION))
    .build();
```

只要这一行 .filesystem(...)，read_file、write_file、execute 等所有内置工具自动改走沙箱后端，Agent 代码完全不用动。IsolationScope.SESSION 保证每个 GitHub Issue / PR / IM 对话各跑各的——最自然也最安全。

### ▍跨调用恢复：第二轮 call() 才是真考验

用户在 PR 上评了一条“再补个测试”。Agent 必须能接着上一轮的环境继续干——重新 git clone + npm install等五分钟，谁也受不了。

这是 Open SWE 用“persistent sandbox”解决的问题 —— 同一个 thread 的 follow-up message 复用同一个沙箱。AgentScope Harness 的方案更精细，沙箱在每次 call()结束时把工作区状态打包成快照存起来，下次按需恢复：

- 容器还在 → 直接接着用（最快）。
- 容器没了 → 拿快照重新起一个，恢复工作区。
- 没快照 → 全量初始化（冷启动）。


快照后端可选 LocalSnapshotSpec（本地单机）、OssSnapshotSpec（S3 兼容，多副本场景）、RedisSnapshotSpec（低延迟，小工作区），生产环境加一行配置就够了：

```
.filesystem(new DockerFilesystemSpec()
    .image("agentscope/coding-sandbox:latest")
    .snapshotSpec(new OssSnapshotSpec(ossClient, "my-bucket", "agentscope/")))
```

### ▍长会话记忆：上下文窗口不是无限的

一个长 Issue 跑几十轮对话，git diff输出上万字符，mvn test 日志几十 K——模型的上下文窗口很快就撑爆。

AgentScope Harness 的解法是四套独立可组合的机制。**对话摘要压缩**在消息条数过多时自动触发，保留尾部原文、前面的压缩成摘要。**大工具结果卸载**把超过 80K 字符的输出写到工作区文件，上下文里只留首尾各约 2K + 一个 read_file 路径提示 —— Agent 想看全文自己再读一遍。**参数截断**把write_file 的大入参也截掉，因为这些内容已经写进文件了，后续对话不需要再看。**溢出兜底**在真的撞到 context_length_exceeded 时做紧急压缩后重试。

```
HarnessAgent.builder()
    .compaction(CompactionConfig.builder()
        .triggerMessages(50)
        .keepMessages(20)
        .truncateArgs(CompactionConfig.TruncateArgsConfig.builder()
            .maxArgLength(2000).build())
        .build())
    .toolResultEviction(ToolResultEvictionConfig.defaults())
    .build();
```

这不是可选项。Coding Agent 一定会跑长会话，一定会输出大 diff，不开这两个早晚撞墙。

同时，MEMORY.md 会从每天的对话流水账里周期性合并出长期事实。Coding Agent 跑久了，MEMORY.md里可能就长出这样的内容：

```
- 仓库 owner/repo 的测试命令是 `mvn -pl module test`，根目录 `mvn test` 太慢不要用
- main 分支受保护，必须通过 PR 合并；feature 分支命名约定为 `feat/`
- CI 用 GitHub Actions，配置文件在 .github/workflows/ci.yml
```

Agent 自己学会了团队的规矩，下次就不用再问了。所有用同一 workspace 的对话都受益。

### ▍会话持久化：节点挂了对话不能断

组织级 Coding Agent 是个长生命周期的应用。一个 Issue 可能从早上聊到晚上，期间服务可能滚动发布、扩缩容、副本切换——但用户感知到的应该是“对话不会断”。

默认模式下 AgentScope Harness 用本地文件存储状态，够开发用。多副本生产切 Redis，一行配置：

```
HarnessAgent.builder()
    .stateStore(RedisAgentStateStore.builder().lettuceClient(redisClient).build())
    .build();
```

切到 Redis 之后：节点崩了会话漂到另一个节点，滚动发布时旧 pod 自动保存、新 pod 自动恢复，甚至在 GitHub Issue 里聊到一半切到钉钉继续——只要 sessionId 一致，记忆都在。

***组织级特有的工程问题***

*Cloud Native*

上面讲的沙箱、恢复、记忆、持久化，是让一个 Coding Agent“能在生产环境跑住”的基础设施。但组织级的场景还有一些独有的问题需要解决。

### ▍多通道接入：同一个 Agent 接得住所有入口

Stripe 的 Minions 走 Slack，Coinbase 的 Cloudbot 也走 Slack，Open SWE 同时接 Slack + Linear + GitHub。组织级 Coding Agent 的一个共识是：不要让用户换到一个新的界面去找 Agent，让 Agent 出现在用户已经在用的地方。

Coding Agent 在 AgentScope Harness 之上加了一层**通道适配器**，把不同入口的事件统一映射到（`threadId, message)`：

```
github:issue:owner/repo#42   → SHA-256 → UUID → coding agent thread
dingtalk:<appKey>:<staffId>  → SHA-256 → UUID → coding agent thread
feishu:<tenantKey>:<chatId>  → SHA-256 → UUID → coding agent thread
```

这个确定性映射保证同一个 Issue 的所有评论都路由到同一个 Agent session —— 对话历史自动恢复，不用用户操心。

### ▍多租户隔离：谁和谁不能串

个人工具不需要考虑这个问题——只有一个用户，所有状态天然是隔离的。组织级服务从第一天起就是多租户的：几十个 Issue、几十个 PR、几十个 IM 对话同时在跑，每个都有自己的代码仓库、依赖目录、对话历史和长期记忆，绝不能串台。

AgentScope Harness 用 IsolationScope 控制隔离粒度。SESSION（默认）让每个 sessionId 独立一个沙箱 —— 对 Coding Agent 来说就是每个 Issue / PR / IM 对话各跑各的，最自然也最安全。USER让同一用户的多个对话共享同一份仓库克隆，适合“个人工作台”场景。隔离不只是沙箱层面的 —— 会话状态、记忆、子 Agent 任务也都按同样的粒度隔离，不用开发者自己操心。

### ▍并发控制：一个 thread 同一时间只跑一个推理

Coding Agent 用 RunDispatcher+ MessageQueueHook 强制保证这一点。用户在 Agent 跑着的时候又评了一条，新消息不会打断当前推理，而是入队等下一轮开始前注入 —— 就像 Open SWE 的 check_message_queue_before_modelmiddleware。

同时 ThreadBudgetHook管住每个 thread 的模型调用上限，ModelCallLimitHook 管住全局 —— 一个用户的失控循环不能把全公司的额度烧光。

### ▍工作区：人格、记忆、技能都是文件

AgentScope Harness 把所有跨调用、跨重启需要保留的东西组织成一个目录 —— workspace。行业里现在把这类设计叫“Context Engineering”。有意思的是，几乎所有主流 Coding Agent 都独立走到了同一个模式：Claude Code 有CLAUDE.md，GitHub Copilot 有 .github/copilot-instructions.md，Open SWE 有 AGENTS.md——repo 级别的规约不应该硬编码在 system prompt 里，而应该是文件，能版本化、能 CR、能独立更新。

```
~/.agentscope/codingagent/workspace/
├── AGENTS.md            ← 人格 + 行为约定
├── MEMORY.md            ← 长期记忆
├── skills/              ← 可复用技能（提交规范、测试规范等 SOP）
├── subagents/           ← 子 agent 声明
├── knowledge/           ← 领域知识（API 文档、代码规范）
└── plans/               ← Plan Mode 计划文件
```

三个工程价值：

**团队规范以文件形式生效。**

想让所有 PR 遵循 commit message 规范？写成一份 skill 放进 skills/commit-style/SKILL.md，所有 Agent 实例下次 call() 就生效，不用重启、不用改代码。

**Agent 在用的过程中越来越懂团队。**

第一次它问“我们用哪个测试框架”，你告诉它“JUnit 5 + Mockito”。下次 call() 它就记得了 —— 所有用同一 workspace 的对话都受益。

**workspace 当 Git 管理。**

AGENTS.md + skills/ + subagents/ + knowledge/ 是 Agent 的“配置仓库” —— 用 Git 管理，CI 验证，部署时 hydrate 进所有副本。频繁变化的应该是 workspace 里的内容，而不是 Java 代码。

### ▍子 agent：把独立任务委派出去

Open SWE 用 Deep Agents 的 task tool 做子 Agent 派发，Stripe 的 Minions 用 Blueprints 编排，Ramp 的 Inspect 用 Sessions + Child Sessions。AgentScope Harness 也支持子 Agent，而且用法很轻量 —— 在 workspace 里写一个 markdown 文件就行：

```
# workspace/subagents/researcher.md
---
description: 调研子 agent。当需要先了解一个外部仓库或文档再做修改时使用。
workspace:
  mode: isolated
tools: [read_file, grep_files, fetch_url, web_search]
---
你是调研助手。fetch_url / web_search 收集材料，read_file / grep_files 看代码，
给主 agent 一份带要点和引用的简报。
```

主 Agent 调用agent_spawn agent_id="researcher" task="调研 ABC 库的 v2 升级要点"，子 Agent 在隔离上下文里跑完，结果返回给主 Agent。后台调用加个 timeout_seconds=0，主 Agent 不 block，跑完后框架自动把结果注入下一轮推理。

### ▍Plan Mode：大改之前先想清楚

让 Coding Agent 直接上手做“重构整个鉴权模块”是高风险的 —— 它可能边想边改、改坏一片。AgentScope Harness 的 Plan Mode 把这件事固化成“先想 → 写计划 → 人确认 → 再动手”的流程。开启后 Agent 进入只读阶段，只能调用读取工具和 plan 相关的四个白名单工具，退出 plan 需要人类确认。

这和 Coinbase Cloudbot 的“Agent Councils”理念类似 —— 在高风险操作前加入人类审批节点，用流程约束代替“祈祷模型别出错”。

### ▍工具精选与确定性兜底

Stripe 在公开分享 Minions 经验时提过一个观察：他们的 Agent 有约 500 个工具，但强调“tool curation matters more than tool quantity” —— 工具不是越多越好，精选和维护比堆数量重要。Open SWE 也跟进了这个理念，只暴露约 15 个核心工具。Harness 的做法类似，内置工具集控制在文件操作 + shell 执行 + 记忆检索这个范围内，业务工具通过toolkit.register(...)按需注册。

另一个行业共识是：**不能只靠 prompt 告诉模型“记得跑测试”，关键步骤要用确定性逻辑保证。**GitHub Copilot Coding Agent 跑完后走 repo 现有的 CI pipeline 做验证；Open SWE 有一个 open_pr_if_needed middleware 作为兜底——Agent 忘了开 PR，middleware 自动补上。Harness 的 middleware 机制（MessageQueueHook、ThreadBudgetHook 等）也是同一思路：哪些事交给模型决定，哪些事用确定性代码保证，这条线要画清楚。

还有一点值得提：**Draft PR 作为输出契约**。无论是 Copilot Coding Agent、Open SWE 还是 Stripe Minions，Agent 的产出都是 draft PR，永远需要人类 review 后才能 merge。Agent 不直接改生产代码——这是组织级 Coding Agent 的一个基本安全假设。

***从单机到企业：一条演进路线***

*Cloud Native*

AgentScope Harness 让你从最简的形态开始，按需切换 —— 同一份 Agent 代码逻辑，配置不同就跑出不同的能力。

**Stage 1：本机 CLI。**什么都不配。execute在宿主sh -c跑，状态存本地文件。只在你信任的本机环境用 —— 这就是一个能装记忆、能装技能的加强版本地 Coding Agent。

**Stage 2：本机 + Docker 沙箱。**加一行 .filesystem(new DockerFilesystemSpec()...)，所有执行进容器。这是给 GitHub Webhook 模式用的——每个 Issue/PR 一个临时容器，宿主不暴露攻击面。

**Stage 3：多副本 + 分布式。**stateStore换 Redis，沙箱快照存 OSS，加executionGuard做并发控制。到这一步 Coding Agent 就能横向扩展——挂在负载均衡器后面跑 N 个副本，任何副本都能接住任何用户的任何对话。

```
.filesystem(new DockerFilesystemSpec()
    .image("agentscope/coding-sandbox:latest")
    .isolationScope(IsolationScope.USER)
    .snapshotSpec(new OssSnapshotSpec(ossClient, "bucket", "prefix/"))
    .executionGuard(RedisSandboxExecutionGuard.builder(jedis)
        .leaseTtl(Duration.ofMinutes(30)).build()))
.stateStore(RedisAgentStateStore.builder().lettuceClient(redisClient).build())
```

**Stage 4：可观测与限流。**Spring Boot Actuator 暴露健康探针和 Prometheus 指标，ThreadBudgetHook 和ModelCallLimitHook守住模型预算，`FallbackModel` 应对上游限流。这些组合在一起就是一个“上线后能跑住”的 Coding Agent 应该有的样子。

***总结***

*Cloud Native*

回顾一下本文提到的这些项目 —— Stripe Minions、Ramp Inspect、Coinbase Cloudbot、LangChain Open SWE、GitHub Copilot Coding Agent、Claude Code，再加上 AgentScope Harness —— 它们在语言、生态、部署形态上各不相同，但在核心架构决策上高度一致：per-session 隔离沙箱、确定性的 thread ID 路由、middleware 拦截链、Agent 运行时的 message queue 注入、repo 级指令文件、draft PR 作为输出契约。

Coding Agent 的上半场是个人提效 —— 模型更聪明、补全更准、本地工具更顺手。下相半场的战场转到了工程：怎么把“能跑一次 demo”变成“7×24 稳定服务一整个团队”。从 Stripe 到 GitHub，从 LangChain 到 AgentScope，大家在不同的起点上走向了同的架构。这种趋同本身就是最好的路标。

文中提到的 Coding Agent 是一个完整且可读的示例，但还远不是一个生产可用的产品，建议直接 clone 下来跑一遍再翻源码 —— 它把本文讲的这些工程问题都对应到了真实代码去完善它。

想继续深入了解，推荐大家深入了解 AgentScope 2.0 官方文档：https://java.agentscope.io

