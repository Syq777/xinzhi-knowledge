---
作者:
  - "高德技术"
原文链接: https://mp.weixin.qq.com/s?__biz=MzE5ODQ3MDM4Mw==&amp;mid=2247491105&amp;idx=2&amp;sn=1b6e6979ed4ce97f52def0d8d3dada70&amp;chksm=97e8f395824cb38263cff3cf4b25471a4bd8ce6090145aaaaad18367303bde2ba30a13ed6933&amp;mpshare=1&amp;scene=1&amp;srcid=061019XBR7v7e4R4dBeqB21M&amp;sharer_shareinfo=8975cea13d67465dc41b460ef89023cc&amp;sharer_shareinfo_first=8975cea13d67465dc41b460ef89023cc#rd
发布时间: ""
收藏时间: "2026-06-10"
关联日记: "[[2026-06-10]]"
tags:
  - 文章
---
本期导读

我们在营销算法团队构建了一套 AI Agent 系统：只需输入一句话目标（如"训练发券模型，目标击败 online baseline"），它便能自主完成"提出假设 → 拼接样本 → 训练模型 → 离线评估 → 迭代决策"的全链路闭环。过去，工程师完成一次完整的模型迭代通常需要 3–5天，期间还要反复处理数据调度异常、单点登录过期、隐性训练失败等琐碎但高频的工程问题；而该 Agent 系统可在1–2天内无人值守地跑通同等流程，将工程师从重复性的流程执行中释放出来，专注于更高价值的策略设计与创新探索。

一、它是什么

一个 AI Agent 系统, 专做一件事: 替算法工程师跑完 Uplift 模型迭代的完整生命周期 (Uplift 模型预测的是"给用户发券能多撬动多少 GMV", 是营销算法的核心资产)。

输入: 一段自然语言 (例: "训练旅游 uplift 模型, 目标 sim 胜率 > 50%")。

输出: 1-2 天后给你一个训练完的模型 + AUUC 评估报告 + 整个过程的审计日志。中间不需要人介入——除非碰到企业平台权限审批 (它会主动停下来等人, 后面讲)。

它管的事: 

1. 想清楚: 决定本轮假设方向 (改样本 / 改模型架构 / 调参数 / 加特征 四选一) 

2. 写 SQL: 从各业务线源表口径里, 拼出训练样本 

3. 跑数据: 在数据开发平台上调度 30+ 天的 backfill 出训练集、测试集 

4. 训练模型: 在训练平台上发布 pipeline、跑 GPU 训练、拉日志 

5. 评估: AUC/AUUC/离线仿真对比 online baseline 

6. 审核自己: 每一步出错了, 自己查日志、定根因、改代码、重跑 

7. 存档: 整个过程每一步都落进事件日志, 进程崩了能从断点续上

简单说: 过去工程师手工干的所有事, 它现在自己干; 它干不了的, 就停下来等你 (例如申请数据表权限——这是企业治理动作, Agent 没权限干)。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6a28b56ea671ad09c2177dbf/3cfa14f8-8d6b-4cd3-bb83-68c0167f742d.png)

图 1 · 五层 long-running Agent harness · L2 LLM Sub-Agents 在 L1 长跑引擎 + L3 工具适配层上跑

二、三个核心能力

### 能力 1: 不知疲倦, 不丢进度

每个有副作用的步骤 (跑 SQL、提交训练、抓日志) 都被记成一个"任务"; 任务状态变化 (开始 / 完成 / 失败) 即时写入本地数据库——append-only, 向 git 提交记录, 永远不删。

为什么这事重要: 一次完整迭代要 1-2 天 wall clock。中间任何一刻——你合上 laptop 睡觉、SSO token 过期、进程被 kill -9、电脑突然死机——下次重启时, 系统扫一遍记录, 从最近一个"已完成"的步骤继续往下跑, 进行中的步骤直接用之前存的外部任务 ID 续 polling, 不会重新提交浪费 GPU 配额。

实际案例：跑到第 9 小时 laptop 睡眠了, 第 11 小时唤醒, 整个训练在云上自己跑完了——系统重启后直接用之前的训练任务 ID 拿结果继续, 工程师介入次数 = 0。

### 能力 2: 能审稿自己, 能修自己的错

8 个 LLM Agent 各管一摊——Planner 想方向、SampleDesigner 出 SQL、Coder 写代码、Critic 审稿、LogTriage 查根因、Repair 出补丁——之间通过 explicit handoff 互相交接。

关键设计: Critic 不靠"另一个 LLM 当裁判" (这是业界普遍翻车的方式, 学术 benchmark 报告 80% 的 Agent 实验结果是 LLM 编造的), 而是直接跑确定性 Python `assert`——读真实数据库行数、查真实训练指标、读真实评估 CSV——任何一条 assert 失败, 触发 LogTriage→Repair 闭环。

为什么这事重要: LLM 最容易在"评估自己工作"时编结果。强制把"对错判断"交给 Python 解释器跑真实 assert (不是 LLM 自我评价), 编不了。

实际案例：美食业务源表的某个 JOIN key 字段在该业务上 100% 为空, 直接套酒店模板会得到 0 行训练样本。Critic 跑数据库 COUNT 发现行数严重不足直接拦下; LogTriage 查上游表口径文档发现该字段不适用; Repair 改 JOIN key 到另一个字段; 重跑出 7 位数行——全程无人干预。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6a28b56ea671ad09c2177dbf/5c9993c2-7fc4-4464-9efe-af41ae731c43.png)

图 2 · 能力 2 视觉化 · Critic / 状态日志 / LogTriage→Repair / 浏览器子 Agent 互相依赖

### 能力 3: 能跟企业平台对话, 卡住会等人

两个通道并行——能用 API 的全走 API; 只有浏览器界面的操作 (例如训练平台的代码发布、多节点日志聚合) 走 Playwright 自动化 + 一个三分浏览器子 Agent (Planner / Actor / Validator), 录制成功脚本后按"前端版本指纹"缓存, 下次直接回放; 网页改版了脚本失效就重新生成。

关键设计: 碰到 Agent 干不了的事 (例如申请数据表权限——属于企业治理) 主动暂停, 把当前状态标记成"等审批", 产出申请单, 等工程师 approve 后从同一个断点继续往下跑。

为什么这事重要: 企业 AI 跟 Kaggle 沙盒最大的区别就是 平台不开放、规则零碎、权限分割。会自治的 Agent 不难做; 知道什么时候应该停下来等人的 Agent 才是 production-grade。

实际案例: 某次跑 OBS 子任务连续多日产出 0 行, Critic 拦下; LogTriage 定位到调度账号没读某张标签表的权限——这是企业身份治理问题, Agent 无法自行解决; 系统暂停所有依赖步骤, 产出申请单 payload; 工程师走完权限申请流程后 approve, 系统从断点自动恢复继续往下跑。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6a28b56ea671ad09c2177dbf/de43750a-f95b-48ba-90bc-7edb9fd77c7b.png)

图 3 · 能力 3 视觉化 · API 走 SDK · UI 走 Playwright + 浏览器子 Agent

三、一次完整迭代长什么样

案例 1

酒店 Uplift 模型一次完整迭代:

```
T+00h  Planner 决策走 sample_change, 锁定 31 天观测样本 + 7 天 RCT 样本
T+04h  数据 DAG 跑完, 单步并行 ~31 个实例, 产出 ~26 万训练 / ~3 万验证
       Critic 通过 treatment 平衡度校验
T+09h  laptop 进入睡眠; 状态日志里此步骤标 started, 未 completed
T+11h  唤醒, 系统自动续接训练 (已在云上自己跑了 30 分钟)
T+12h  训练成功, Critic 通过模型指标校验
T+18h  SSO 过期, 浏览器子 Agent 自动重新登录, 续接评估 CSV 拉取
T+42h  离线仿真 AUUC 较 online 基线**数量级提升**
       Planner 决策 ACCEPT, 迭代收尾

```

1 天 18 小时全程, 工程师介入次数 = 0; 期间 2 次 laptop 睡眠 + 1 次 SSO 过期, 全部自动恢复。

四、其他 3 个行业

案例行业关键点2美食Critic 找出业务侧非显式约束 (某字段在该业务 100% 空), 自动切 JOIN key3旅游一句自然语言冷启动新行业; 工程师投入从 ~3 人天降到 ~1 人天 (-67%)4充电行业知识包已就绪, 端到端首跑 in 进行

整体工程指标:

维度数值端到端跑通行业数3 (酒店/美食/旅游), 充电就绪端到端跑通迭代次数4单条假设迭代周期1-2 天无人值守 vs 人工 3-5 天单元测试通过率16/16 (含进程崩溃续跑 + harness primitive 测试)工程师投入同等任务下从 ~3 人天降到 ~1 人天 (-67%)

五、行业对话: Agent Harness的范式演进与对齐

本章节旨在深入探讨技术底层逻辑，主要面向 AI Agent 领域的开发者及研究人员。非工程背景的读者可根据兴趣选择性阅读，或直接跳转至第六部分。

### 5.1 业界 2024-2026 怎么定义 "Agent Harness"

过去两年, 业界关于"造一个能跑长任务的 AI Agent 系统应该长什么样"这件事已经基本对齐:

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6a28b56ea671ad09c2177dbf/355abacd-4f6a-4823-b04e-42ac3fe2278c.png)

业界已经把"造Agent该有哪些零件"讲清楚了——真正缺的是把这套范式跑在企业生产平台上的公开案例 (不是 Docker 沙盒、不是 Kaggle、不是写论文)。这正是我们走的路。

### 5.2 本系统与业界主流范式的对齐程度评估

业界 harness 范式里有 10 件具体的事 (业界定义"primitives", 可以理解为 10 块乐高积木; 一个真正能跑生产的 agent 系统这 10 块都得有)。我们做了一次诚实 audit:

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6a28b56ea671ad09c2177dbf/9ac182a1-0943-4c7a-89db-e18f36697558.jpeg)

图 4·10 个 harness primitive 的 audit 结果

### 5.3 企业平台中几类典型的工程痛点

业界文档默认假设 "环境是干净的、平台是开放的、权限是齐的"——企业环境里这三条都不成立。举几个典型补丁:

- 去重必须用外部任务 ID, 不能用 hash: 数据调度平台某些 API 在部署没完成前会快照旧 SQL (业界 SDK 几乎没人提的 race condition), 必须强制 poll 等部署生效, 否则同一任务两次提交会有不同 hash, idempotency 失效
- Critic 必须 grounded, 不能 LLM-as-judge: 训练平台在样本量极小时会 silent failure 返回 AUC=0.0, 业界 LLM judge 会自圆其说"训练成功"; 我们的 `a``ssert auc > 0.5`直接拦下
- 工具层必须有 UI-only 兜底: 训练平台的代码发布只在浏览器里有, 没 Open API, 必须用 Playwright + 三分浏览器子 Agent + 脚本指纹缓存补上


每一条都对应一次真实踩坑——业界范式给你方法论, 企业平台的细节得自己踩。

### 5.4 Audit 驱动落地的三项能力

- Explicit Handoff以前 Agent 之间转交 (例如失败步骤交给 LogTriage、LogTriage 再交给 Repair) 隐含在状态机里, 看 audit log 得逆向推断。新增 `Handoff(from_agent, to_agent, reason, payload)`数据结构 + 3 处发射点, 现在转交链路在 journal 里能直接查
- MCP-style Tool Registry: 以前工具就是裸 Python 函数, 没统一目录。新增装饰器 `@tool(name, description, input_schema)`, 装饰过的函数自动注册到全局 registry, 现在能用 MCP 兼容的 `tools/list`接口枚举所有工具
- Tracing Spans：以前只有平面事件日志 (start / done / fail), 看不出 "Planner 这次推进调用了几次 LLM、每次 LLM 又调用了几个 tool"。新增 spans 表 + 开闭 API, 支持 parent-child 嵌套和耗时记录, 跟业界 OpenTelemetry / OpenAI Agents SDK tracing 接得上


六、更多思考

### vocabulary 是事后命名, 实现是踩坑出来的

这套系统在 3 月 ~ 9 月一步步迭代时碰到的工程问题——崩溃续跑、LLM 编造、Agent 漂移、企业平台权限治理、UI-only 控制台——事后发现恰好对应业界这一轮沉淀的 harness 范式。; 但既然业界已经用同一套词把它们命名清楚, 我们就该用同一套词跟同行对话。

### 一个 framing: test-time compute

我们这套系统本质上是把过去算法工程师手工迭代的过程, 转译为test-time compute allocation per hypothesis(post-o1 / post-R1 术语)——推理便宜, 实验昂贵; 让 inference 多花一些, 换 experiment 少跑几遍。分析师预测 2030 年推理将占 AI compute 75%, 我们让算法团队从 2025 年就开始享受这条曲线。

### 下一步

- 短期: 充电行业首跑端到端跑通
- 中期: 补完 super-step 抽象 + time-travel checkpoint (一次回退到任意过去点的能力, 现在只能 resume 到最近); 把所有工具都接入 tracing span
- 长期: 覆盖更多业务行业, 单团队同时运行 ≥3 个并行迭代


企业 LLM Agent 的下一个台阶不在模型能力, 而在让模型与企业平台之间的接缝消失。我们的赌注就在这里: 当 Critic 直接读数据库、状态日志直接绑训练任务 ID、浏览器 Agent 直接驾驶 UI——模型本身能不能 30% 还是 36% 拿金牌, 已经不是瓶颈。

欢迎做相似探索的同行交流。

参考文献

[1] Anthropic. Introducing the Model Context Protocol. 2024-11. https://www.anthropic.com/news/model-context-protocol

[2] Anthropic. Building Effective Agents. 2024-12. https://www.anthropic.com/research/building-effective-agents — 5 个 workflow patterns (prompt chaining / routing / parallelization / orchestrator-workers / evaluator-optimizer) + augmented LLM 基础块 + autonomous agents。

[3] Anthropic. Effective context engineering for AI agents. 2025-09-29. https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents

[4] LangChain. LangGraph 1.0 GA. 2025-10-22. https://changelog.langchain.com/announcements/langgraph-1-0-is-now-generally-available

[5] Anthropic. Effective harnesses for long-running agents. 2025-11-26. https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents

[6] OpenAI. Agents SDK. 2025. https://openai.github.io/openai-agents-python/

[7] Gartner. Predicts Over 40% of Agentic AI Projects Will Be Canceled by End of 2027. 2025-06-25.

[8] MLR-Bench (arXiv 2505.19955). 报告 agent 实验结果"在 80% 的 case 中是 fabricated"。

[9] Google. MLE-STAR (2025). MLE-Bench-Lite 63% 获奖, 36% 金牌。

## #Agent #营销算法 #LLM工程实践 #DurableExecution

***END***

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6a28b56ea671ad09c2177dbf/7bbc2522-46ce-42f6-bb42-d47c4c2171c1.png)

