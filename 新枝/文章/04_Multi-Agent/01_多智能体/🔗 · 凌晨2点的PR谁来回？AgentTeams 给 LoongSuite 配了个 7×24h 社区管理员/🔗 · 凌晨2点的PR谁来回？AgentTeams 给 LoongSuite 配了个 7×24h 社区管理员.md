---
作者:
  - "阿里云云原生"
原文链接: https://mp.weixin.qq.com/s?__biz=MzUzNzYxNjAzMg==&amp;mid=2247585023&amp;idx=1&amp;sn=fb2ab904ceb7712d6ed14a5b87563474&amp;chksm=fb220c372c619095ff58f9eb08680b4458b801530b13a32ba0c810ee29c620eb200b94794140&amp;mpshare=1&amp;scene=1&amp;srcid=0714tPsY5SZYR5onvJmK9Z3j&amp;sharer_shareinfo=79602ba168032ae379659a3fe11e697d&amp;sharer_shareinfo_first=79602ba168032ae379659a3fe11e697d#rd
发布时间: ""
收藏时间: "2026-07-14"
关联日记: "[[2026-07-14]]"
tags:
  - 文章
---
作者：张乎兴(望陶)、邵丹(营火)

> 这是「AgentTeams 多 Agent 落地实践」系列的第一篇，记录从单 Agent 巡检到多 Agent 协作的演进过程。

凌晨 2 点，一个来自纽约的开发者提交了他在 LoongSuite 的第一个 PR。不到 1 小时，他收到了详细的代码审查意见——每条评论锚定在具体代码行上，附带修改建议。同时，一条钉钉消息 @ 了我：“首次贡献者 PR 已审查，CI 通过，建议 merge。”

没有人在熬夜。做这件事的是一个运行在 AgentTeams 上的数字员工，我们叫它 github-manager。

从 2026 年 6 月中旬上线至今约三周，它覆盖了 PR 审查、Issue 评估、CI 监控、贡献者沟通等核心场景，累计处理 108 个 PR、48 个 Issue，24 次直接修复代码并推送至贡献者分支。这篇文章记录了这个实践的全过程——包括做对了什么，以及踩了哪些坑。

**01**

***我们遇到了什么问题***

*Cloud Native*

LoongSuite 是阿里巴巴开源的统一可观测数据采集套件，本次实践覆盖其中两个仓库（loongsuite-pilot、loongsuite-python）：

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6a561510d8f54550e9263105/be0369a8-70ff-4393-8c39-5c28142232db.png)

做过开源项目维护的人都知道那种感觉：PR 不断涌入，但你还有自己的本职工作。响应慢一点，贡献者的热情就凉了——根据我们的社区观察经验，PR 超过 48 小时无响应，贡献者流失率将大大提升。再加上 CI 环境复杂、Issue 分类琐碎、跨时区覆盖不可能，维护压力一直在涨。

我们需要一个能 7x24 运转的“数字同事”，不是简单地跑 CI 脚本，而是能真正理解代码、做出判断、和人协作的那种。

**02**

***为什么选 AgentTeams***

*Cloud Native*

最初我们尝试过自己拼凑方案——GitHub Actions + 自定义脚本 + LLM API 调用。能跑，但很快就撞墙了：

- Agent 生命周期管理要自己写：定时触发、超时控制、会话上下文保持、失败恢复……胶水代码越写越多。
- 凭证管理是定时炸弹：GitHub PAT、LLM API Key 散落在各个脚本和环境变量里，Agent 直接持有明文凭证。一旦 Agent 行为异常或被注入，密钥随时可能泄露。
- 没有协作基础设施：多个 Agent 之间、Agent 和人之间没有统一的通信层，状态同步全靠文件和数据库轮询。
- 可观测性为零：出了问题只能翻日志，没有端到端的追踪。


这些不是“优化项”，而是把 Agent 放上生产环境的基本门槛。自己造这些轮子的成本，远超我们的预期。

AgentTeams 吸引我们的点很具体：它是一个多 Agent 协作与治理平台，不是又一个 Agent 框架。它不替换你用的 LLM 或 Agent 实现，而是在上层提供了一层“操作系统”级的能力——Agent 运行时、定时调度、安全治理、协作通信、可观测性，这些我们正缺的东西，它都是现成的。

具体来说，AgentTeams 基于同名开源内核，底层用 Matrix 协议做全透明的 Agent 协作网络，上层通过 AI 网关实现零信任的凭证隔离（Agent 不持有任何密钥），并且原生支持 Team Leader-Worker 的分层架构。对我们来说，这意味着可以把精力集中在“让数字员工干什么”上，而不是“怎么让它跑起来”。

**03**

***怎么搭的***

*Cloud Native*

### ▍3.1 整体架构

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6a561510d8f54550e9263105/1611966c-e292-40da-acd2-0185013497bb.png)

这张图反映了 AgentTeams 作为多 Agent 协作平台的分层设计。最上面是管理员通过 Team Room 实时监督 Agent 的工作，所有交互基于 Matrix 协议，全程留痕可审计。平台层通过 AI 网关实现零信任凭证隔离——Agent 不直接持有任何密钥，所有外部调用都经由网关统一鉴权；ACS Sandbox 则提供实例级的资源隔离和网络隔离，确保安全边界清晰。

在我们的场景中，github-manager 是一个 Worker Agent，运行在 AgentTeams 托管的 QwenPaw 运行时上。它的“大脑”是大语言模型，“身体”则由平台提供：定时调度、工具调用、消息通信、凭证管理，全部开箱即用。

值得注意的是，即使是这个看似“单 Agent”的场景，已经体现了 AgentTeams 的混合引擎编排能力。github-manager 在涉及代码分析、Spec 生成、代码修改时，会将任务委托给代码引擎（Qoder CLI）——后者本质上是一个专精代码理解的独立 Agent，有自己的运行环境和工具链。流程 Agent 负责编排和沟通，代码 Agent 负责技术执行，两者通过安全 wrapper 对接。这正是 AgentTeams Team Leader-Worker 分层架构的一个最小化实践——只是当时我们还没有自觉地往那个方向走。

### ▍3.2 Cron 调度：数字员工的心跳

AgentTeams 内置了 Cron 调度能力，我们给 github-manager 配了 5 个定时任务，实现 7x24 自动巡检：

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6a561510d8f54550e9263105/80d7c28d-d060-4941-b7d1-d73798fdfd8b.png)

另有一个每日工作总结任务「20:00（北京时间）」，自动把当天的工作汇总通过钉钉发给管理员。

### ▍3.3 Skill 模块化：数字员工的“专业技能”

AgentTeams 的能力扩展单元叫 Skill——每个 Skill 是一个包含操作手册（SKILL.md）和脚本的目录，Agent 按需加载。这个设计非常灵活，我们为 github-manager 搭建了 11 个 Skill：

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6a561510d8f54550e9263105/5f32b80a-3593-445c-939e-17a6890d5313.png)

这里的关键不是这些 Skill 本身有多复杂，而是 AgentTeams 的 Skill 架构让“教 Agent 做事”变成了一个可沉淀、可复用的过程。每解决一个新问题，就把方案写成 Skill，下次遇到同类问题 Agent 自动加载。三个月后，这个 Skill 库本身就是一份团队运维知识库。

### ▍3.4 通知闭环：只在需要人的时候找人

AgentTeams 通过 MCP 工具链集成了钉钉消息能力。我们的原则是：Agent 能处理的就自己处理，需要人介入的才通知。具体触发通知的场景包括：首次贡献者 PR、merge 冲突、CI 不可自动修复、Approved 后超 24h 未 merge。

配合每日工作总结推送，管理员每天只需要花几分钟看一条汇总消息，就知道数字员工一天做了什么。真正需要人工判断的事项——merge 决策、架构讨论、社区沟通——才会到人手里。

**04**

***实际效果***

*Cloud Native*

### ▍4.1 三周运营数据

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6a561510d8f54550e9263105/421d5a1e-818e-4e6e-a364-640304692aa1.png)

### ▍4.2 几个关键变化

PR 首次响应时间：从数天到 1 小时内。之前取决于维护者什么时候上线，现在 heartbeat 每小时跑一次，绝大多数 PR 在提交后 1 小时内就能收到审查意见。对首次贡献者来说，这个体验差异是决定性的。

CI 故障从“等人看”变成“自动修”。举个真实案例：PR #229 的 CI 因缺少 Apache 2.0 license header 失败。Bot 自动 clone 仓库、fetch PR 分支、为 11 个文件补上 license header、推送到贡献者 fork，然后评论说明修复内容和 commit SHA。同时它发现 crewai 测试在 main 分支也持续失败（VCR cassette 匹配问题），单独创建了 Issue #230 跟踪，避免贡献者误以为是自己的问题。这种“区分 PR 引入 vs main 分支已有问题”的判断，以前完全靠人盯着。

审查质量不是橡皮图章。Agent 会读完整 diff，从 correctness、performance、tests、compatibility 四个维度分析，每条意见通过 GitHub Review API 锚定到具体代码行。我们在早期确实犯过“为了清积压批量 APPROVE”的错误（后面会讲），纠正后审查质量稳定了下来，确实能发现实质性问题。

管理员时间释放。以前维护者每天花在社区事务上的时间不固定，经常被 CI 失败、重复性 Issue、PR 分类等琐事打断。现在这些事情由数字员工处理，管理员只需要处理需要人工判断的事项。

### ▍4.3 运行规模

- 5 个定时任务 7x24 运行，每小时触发 3-4 次扫描。
- 21 个开放 PR、63 个开放 Issue 持续监控。
- 30+ 篇每日笔记，记录工作日志和教训。
- 1 个长期记忆文件（MEMORY.md），持续迭代——Agent 踩过的坑不会再踩。


**05**

***踩过的坑***

*Cloud Native*

这部分我犹豫过要不要写，因为它暴露了不少问题。但想来想去，这些坑本身可能是这篇文章里最有用的内容——如果你也打算搭建类似的数字员工，大概率会碰到类似的情况。

### ▍5.1 超时配置：沉默的杀手

上线初期，所有 heartbeat 的timeout_seconds设的是 120 秒，但实际 PR 巡检需要 3-5 分钟。结果：任务被超时杀掉，但 cron 框架报告 status=success。从外部看一切正常，实际上连续多天没有执行任何扫描，14 个 PR 积压未审查。

更要命的是，cron-audit 自检任务也只有 120 秒超时——它自己也在被杀掉，所以发现不了其他任务的问题。

修复：所有任务超时对齐到 900s，cron-audit 单独提高。教训：“成功”不等于“完成”。定时任务系统必须区分“正常退出”和“完成了全部工作”。

### ▍5.2 橡皮图章：自动化不等于质量

批量清理积压 PR 时，Agent 为了快速清完，只看了文件名列表 + CI green 就全部 APPROVE，没有读 diff、没有发行级评论。被我们发现后，dismiss 了 9 个橡皮图章 approve，让下次 heartbeat 重新走完整流程。

修复：在 Skill 的操作手册中明确禁止“用一行命令跳过完整审查流程”。教训：自动化的价值在于提高效率，不是降低标准。Agent 必须走完整流程：读 diff → 分析 → 有问题则发行级评论，没问题才 approve。

### ▍5.3 自我识别：防止反馈闭环

Agent 发出的评论，被自己的后续扫描误识别为外部输入——比如把自己的评论中的 /approve 当成社区反馈，触发再次处理。

修复：每次任务启动时通过 gh api user 动态获取自身 login，在所有扫描中过滤自己的内容。教训：自治系统必须有自我感知能力，否则会产生反馈闭环。

### ▍5.4 几个技术细节的坑

- Cron shell 转义：--text 参数中的 $(date +%Y-%m-%d) 在创建时就被当前 shell 展开为固定值，而非运行时动态求值。必须用反斜杠转义。
- APPROVE 幂等性：去重逻辑只看“bot 是否 review 过”不够，必须检查“当前 HEAD SHA 是否已 APPROVED”。GitHub API 的 gh pr view --json reviews 返回的 commit_id 是 null，必须用 REST API 获取。
- 事件日志性能：逐条调用外部脚本写日志，每次 spawn 一个 python3 进程约 4 秒，20 个事件就超时了。改成批量发射器后解决。在 LLM Agent 环境中，“每次调用一个外部进程”的代价远高于传统环境。


**06**

***回头看：什么有效，什么还不够***

*Cloud Native*

### ▍有效的部分

AgentTeams 的 Skill + Cron 组合是核心。定时调度提供触发频率，LLM Agent 提供灵活判断，Skill 保证每次执行有章法。这比传统的 CI/CD bot 更智能（能理解代码、做判断），比人工更持续（7x24，不会忘，不会累）。

Matrix 协议带来的透明性。AgentTeams 底层用 Matrix 协议做协作通信，所有 Agent 的操作和对话都留存在 Room 中，可追溯、可审计。这不是一个“用了就明显”的功能，但在排查问题时你会发现它的价值——你能完整看到 Agent 在每一步做了什么、为什么做。

零信任凭证隔离。在生产环境跑 Agent，安全是绕不过去的。AgentTeams 通过 AI 网关统一管理凭证，Agent 不持有任何密钥，这个设计让我们在接入生产仓库时少了很多顾虑。

行级评论能力。Agent 能读 diff、理解代码、在具体行上指出问题，这比“CI green 就 approve”有价值得多。它让自动审查真正变成了一个“审查”，而不只是流水线的一个节点。

### ▍需要改进的部分——也是多 Agent 协作真正发力的地方

审查深度和效率的平衡。大 PR（+4000 行）的完整审查耗时较长，heartbeat 单次能处理的 PR 数量有限。目前靠优先排序（首次贡献者优先）缓解，但更根本的解法是把审查拆成多个专项 Agent 并行工作：一个负责 correctness，一个负责 performance，一个负责测试覆盖率，最后由一个 TL Agent 汇总意见并发出 review。这正是 AgentTeams Team Leader-Worker 架构的设计初衷——我们还在一个 Worker 扛所有的阶段，离"团队作战"还有距离。

Issue → PR 全流程需要 Agent 间的接力。Issue 评估和 PR 审查目前是独立流程。理想状态是一个完整的工作链：Issue Agent 完成分类和验证 → Spec Agent 根据 Issue 生成技术方案 → Code Agent 实现代码并提交 PR → Review Agent 审查。这是一个天然的 TL + 多 Worker 协作场景，每个 Agent 专注自己擅长的环节，通过 Matrix Room 共享上下文，TL 负责流转和异常处理。链路已经搭好，但数据还不够多，后续会重点验证。

跨仓库联动是多 Agent 协作的刚需。LoongSuite 三个仓库（python、pilot、loongcollector）有 API 关联，python 仓库的 SDK 接口变更可能让 pilot 的集成测试全部失败。目前跨仓库检查是手动的。下一步计划用 AgentTeams 搭建一个 Manager Agent 统筹全局，分别为每个仓库配一个 Worker Agent，通过 Team Room 共享变更上下文——当一个仓库的 Agent 检测到 breaking change，自动通知其他仓库的 Agent 进行兼容性检查和修复。这种跨 Agent、跨仓库的实时协作，单靠一个 Agent 是做不到的。

**07**

***什么样的场景适合搭“数字员工”***

*Cloud Native*

做完这个实践之后，我们总结了几条判断标准：

适合的场景：流程相对标准化、判断规则可以写成 Skill、需要 7x24 持续覆盖、涉及多方协作（人和 Agent 或 Agent 和 Agent）。典型如开源社区维护、客服自动应答、定期巡检、数据采集与清洗等。

不太适合的场景：需要大量创造性判断、规则高度模糊且不可枚举、或者容错率极低的场景。Agent 能放大人的能力，但不能替代人对复杂局面的最终判断。

搭建路径大致是：明确 Agent 的职责边界 → 把职责拆解为 Skill → 在 AgentTeams 上配置 Agent + Cron + 工具链 → 先在一个小范围跑通 → 逐步扩大覆盖。AgentTeams 的 Skill 架构让这个过程可以渐进式推进，不需要一步到位。

**08**

***从一个 Agent 到一支 Agent 团队***

*Cloud Native*

做完 LoongSuite 的实践后，我们回头审视整个架构，发现了一条清晰的演进路径——从一个 Agent 做事，到一支 Agent 团队协作。AgentTeams 的平台能力在这条路径上逐层释放：

第一阶段：单 Worker Agent 巡检（当前）。一个 github-manager 包揽 PR 审查、Issue 处理、CI 监控、冲突检测。它的"多 Agent"仅体现在和代码引擎的委托协作上。这个阶段验证了 Agent 的基本可行性：它能读代码、做判断、写评论、推 commit。但也暴露了单 Agent 的瓶颈——职责太多，单次 heartbeat 能处理的事务有限。

第二阶段：专项 Worker 分工（进行中）。把 github-manager 的职责拆给多个专项 Worker Agent：PR Review Agent 专注代码审查，Issue Agent 专注 Issue 分类和验证，CI Agent 专注 CI 诊断和修复。AgentTeams 的混合引擎编排能力在这里发挥关键作用——不同 Worker 可以跑在不同的 Agent 实现上（QwenPaw、OpenClaw、甚至 Claude Code），按每个角色的特点选最合适的引擎。Worker 之间通过 Matrix Room 共享上下文，避免信息孤岛。

第三阶段：Team Leader-Worker 全架构团队（规划中）。引入 Manager Agent 统筹全局（比如跨仓库协调），TL Agent 负责任务拆解和分配（比如一个大 Issue 的端到端处理），多个 Worker Agent 各司其职。这是 AgentTeams 作为多 Agent 协作平台的完整形态——人通过 Team Room 随时介入，Agent 之间点对点加密通信，全链路可观测，AI 资产（Skill、MCP、模型）统一管理和复用。

这三个阶段不是理论推演。从第一阶段到第二阶段的过渡已经在发生——我们搭建的 issue-to-pr Skill 本身就是一个多 Agent 接力的原型。而从第二阶段到第三阶段，AgentTeams 的 Team Leader-Worker 架构已经就绪，缺的只是更复杂的业务场景把它填满。

**09**

***写在最后***

*Cloud Native*

回到开头的场景：凌晨 2 点，一个来自纽约的开发者提交了 PR，15 分钟后收到了审查意见。

这件事以前不可能发生，除非维护者恰好醒着。现在它是常态。

AI 数字员工不是替代维护者，而是放大维护者的能力。维护者的时间应该花在需要人类判断的事上：merge 决策、架构讨论、社区沟通。机械性工作——读 diff 找问题、检查 CI、分类 Issue、提醒冲突——交给 Agent。开源社区的健康度很大程度上取决于响应速度，Agent 的 7x24 覆盖能力让“及时响应”从理想变成了常态。

AgentTeams 在这个过程中扮演的角色，不是一个“Agent 开发框架”，而是一个多 Agent 协作与治理平台——它解决的是 Agent 从单兵作战到团队协作的跃迁问题：安全治理让 Agent 敢上生产，Matrix 协议让多 Agent 之间的协作透明可审计，Team Leader-Worker 架构让 Agent 团队像人类团队一样分工协作，弹性沙箱让规模从 1 个 Agent 扩到 100 个 Agent 不需要重建基础设施。这些能力自己造不是不行，但成本和时间会让大多数团队望而却步。

不过，LoongSuite 只是一个开始。

这篇文章讲的是一支 Agent 团队里“第一个员工”的故事。实际上，我们在 AgentTeams 上搭建的远不止一个开源社区维护 Agent——而是一支包含 10 余种不同职能，将近 100 个 Agent 组成的完整开发团队：从需求分析到架构设计，从代码实现到测试保障，从文档编写到发布运维，每个角色都有对应的专项 Agent，通过 Team Leader-Worker 架构协同工作。

那才是 AgentTeams 作为多 Agent 协作平台的真正用武之地。

后续我们会继续写这个团队的故事——怎么从“一个 Agent 管仓库”演进到“一支 Agent 团队做开发”，中间又踩了哪些只有多 Agent 协作才会遇到的坑。如果你也在考虑用 AI Agent 提升研发效率，这个系列值得持续关注。

AgentTeams 目前在阿里云上线，更多信息和接入方式可点击文末阅读原文，或登录官网了解：https://www.aliyun.com/product/agentteams

**LoongSuite 介绍：**

也欢迎大家关注 LoongSuite 开源社区，如果你想要了解 Agent 在执行复杂任务的执行轨迹，想知道 Agent 执行过程中消耗了多少 token，到底是哪个环节消耗的最多，工具调用是否正确等问题，可以使用 LoongSuite 提供的采集探针，无需修改任何 Agent 代码，即可采集符合 GenAI 语义规范的数据，支持 AgentScope, LangChain 等各种框架以及 Claude Code, Codex 等各种 coding agent。也欢迎给各个项目 star！

相关链接：

[1] LoongSuite Pilot

https://github.com/alibaba/loongsuite-pilot

[2] LoongSuite Python

https://github.com/alibaba/loongsuite-python

[3] LoongCollector

https://github.com/alibaba/loongcollector

[4] LoongSuite JS

https://github.com/alibaba/loongsuite-js

[5] LoongSuite Go

https://github.com/alibaba/loongsuite-go

[6] LoongSuite Java

https://github.com/alibaba/loongsuite-java

本文基于 github-manager 数字员工 2026 年 6-7 月的真实运营数据编写。Agent 运行在 AgentTeams 平台上，管理 alibaba/loongsuite-pilot 和 alibaba/loongsuite-python 两个开源仓库。

