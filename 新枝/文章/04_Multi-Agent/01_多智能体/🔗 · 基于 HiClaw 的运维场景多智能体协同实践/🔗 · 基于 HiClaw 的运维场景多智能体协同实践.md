---
作者:
  - "阿里云云原生"
原文链接: https://mp.weixin.qq.com/s?__biz=MzUzNzYxNjAzMg==&amp;mid=2247583292&amp;idx=1&amp;sn=b70311e0884b6f613823b0b1ecba4a15&amp;chksm=fba49a0e71467ac0d60302a6facb1f94687cd55b617d8f29327df38ff2dc2beb3d4a9f90235e&amp;mpshare=1&amp;scene=1&amp;srcid=0408a11dXGxWijIsXBVGJ3RH&amp;sharer_shareinfo=1f0cbb68122ab2775304fcc38a5024d5&amp;sharer_shareinfo_first=1f0cbb68122ab2775304fcc38a5024d5#rd
发布时间: ""
收藏时间: "2026-04-08"
关联日记: "[[2026-04-08]]"
tags:
  - 文章
---
从搜索指数看，个人养虾已经降温了，但不会消失，AI 的普及是一个循环向上的过程，不同人群之间会存在较大的温差。

事实上，Claw 已经成为不少个人或团队每天调用模型不可替代的入口，尤其是在一些线上巡检、定时发布的周期性任务上，以及一些团队协作的场景，非常适合多线程工作的人士。

另一边，有了个人养虾的背书，企业养虾开始进入决策期，评估通过企业采购行为设计虾场的应用场景和短中长期的目标，甚至有企业已经将此作为业务创新的牵引力。

以下分享一个我们在 SRE 场景下 Agent Team 的协作实践。

**01**

***HiClaw 是什么***

*Cloud Native*

HiClaw 是一个面向企业的分布式多 Agent 运行平台，核心定位是让多个 Agent 在一个受控、可审计的环境中协同工作，人类全程可见、可介入。

与常见的单进程个人 AI 助手不同，HiClaw 自己不实现 Agent 逻辑，而是编排和管理多个 Agent 容器（Manager 和众多 Workers），这些 Agent 可以运行 OpenClaw 或 CoPaw 作为智能内核，后续还将支持 NanoClaw、ZeroClaw，甚至通过 CLI 方式接入企业自建 Agent。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/69d635492d289a10eca1fe8d/79cac863-87a6-4b39-be2f-ad91fafd062b.png)

官方网站：https://hiclaw.io/

“泰山”是我们团队支持阿里云上的云原生产品的 SRE 系统。我们将在此系统上的隔离环境里，部署一套 HiClaw，并应用于我们的运维场景。

**02**

***构建 HiClaw 组织***

*Cloud Native*

HiClaw 初始化之后的状态：

- **唯一的真人账号：**admin。通过对话使唤 manager 干活儿的权利。
- **唯一的数字人：**manager。具备操作操作 HiClaw 所有资源的权限，所有执行都需要通过 Manager；manager 本身就是一个 OpenClaw，内置任务与项目管理、系统管理、worker 管理等 Skills。Manager 默认是 OpenClaw 内核，未来会支持其他智能内核。


▍组建 Human 团队

与 manager 对话创建 Human 团队：

```
任务：组建一个SRE团队，用于SRE（运维和测试）日常事务的沟通，并创建一个团队管家数字人叫做（sre-bot）
团队组成：团队中包含一个团队管家和n个真人用户
- 团队管家：是一个worker数字人，负责任务分解、成员协调、进度同步，唯一对接 Manager
- 真人用户：都用于 @mention 团队管家的权利，让团队管家做事情的权利。
- 真人账号参考附件来建立，登录账号为工号，名字为可见姓名，密码随机（账户密码请写入到文件中，我需要Matrix中下载）
权限要求：
- 团队管家数字人，响应团队中所有真人账户派发的任务
- manager不响应除了admin之外的真人用户
```

下发指令之后，Manager 做了这么几件事情：

- 提取 xlsx 文件中的用户名和工号创建 Matrix 账号。
- 创建 SRE 数字人管家 sre-bot（选择 CoPaw 作为智能内核）。
- 创建 SRE 团队。
- 将 sre-bot 拉入到群中，并邀请 SRE 同事到群中。


![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/69d635492d289a10eca1fe8d/60dfaa58-2b00-4c65-88ce-db36a54e298a.jpeg)

以上界面是 HiClaw 内置的的 Matrix 客户端 Element，默认是英文界面，可以改为中文界面。此外，也可以按照 OpenClaw 原生的方式接入钉钉、Discord、飞书等。

Manager 只是邀请了真人员工，真人员工需要登录到系统并接受邀请才代表真正进入了。接受邀请的界面如下。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/69d635492d289a10eca1fe8d/f55c4ee9-4b20-4dcd-b557-818964996185.png)

▍数字人 Bot 职责设计

```
Human (Admin)
  └─ Manager Agent (唯一入口)
       ├─ Worker A (OpenClaw/CoPaw)
       ├─ Worker B
       └─ Worker C
```

默认情况下，所有任务必须经由 Manager 分配，所有真人用户必须与 Manager 对话，这在企业场景中存在瓶颈：

- Manager 成为单点瓶颈，所有指令都需经过它。
- Worker 之间无法自组织协调。
- 无法映射企业真实团队结构。


为了解决这个问题，引入了“团队管家”数字人。

```
Human (Admin / Human Users)
  └─ Manager Agent (系统管理 + 组织管理)
       ├─ Team A
       │    └─ 团队管家数字 A (Team Leader,任务调度)
       ├─ Team B
       │    └─ 团队管家数字人 B (Team Leader, 任务调度)
       │
       └─ Worker Pool (共享资源池, 按授权分配)
            ├─ Worker 1  ──── 授权 → Team A, Team B
            ├─ Worker 2  ──── 授权 → Team A
            ├─ Worker 3  ──── 授权 → Team B
            └─ Worker 4  ──── 独立 Worker (不属于任何 Team)
```

数字人 Bot 的职责和分工如下：

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/69d635492d289a10eca1fe8d/e9c97b32-5375-4816-ae59-d53a969e707b.png)

Manager**管“系统和组织”，**Leader**管“任务调度”，**Worker** 管“做出来”**。拆分之后的好处：

- Manager 的 SOUL 可以做得很轻（管理类指令集），Team Leader 的 SOUL 可以做得很专（领域任务调度）。各自的 prompt 更聚焦，AI 决策质量更高。
- Admin/Human 的任务请求直接到 Team Leader，不需要绕道 Manager。
- 不同 Team Leader 可以有不同的领域专长（前端团队、后端团队、测试团队），按业务线组织。
- Team 内部的调度逻辑可以独立演进，改一个 Team 的策略不影响其他 Team。
- Manager 挂了只影响系统管理操作（创建/销毁 Worker），已有的 Team 可以继续正常工作。


![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/69d635492d289a10eca1fe8d/be865322-b700-4e99-86e1-d93a43fdcb7e.png)

▍Human 和数字人权限设计

Admin 管平台，团队负责人管团队，团队员工用团队：

- **三种数字人：**Manager 数字人，团队管家数字人，Worker 数字人。
- **三种 Human 角色：****Admin、团队负责人、团队员工。**


![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/69d635492d289a10eca1fe8d/485254e2-6964-4d83-870a-d5a339cdbd00.png)

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/69d635492d289a10eca1fe8d/fe22372c-c85e-43d3-99f5-54e4c971eff0.png)

admin 通过 @sre-bot 设置团队负责人：

```
@sre-bot为团队管家；将隐寒设置为团队负责人，其他人为团队员工，相关的权限配置如下，你需要把下面信息写入到你的rule里面，并严格执行：
| 维度 | Admin（系统管理员） | 团队负责人 | 团队员工 |
| --- | --- | --- | --- |
| **定位** | 管平台 | 管团队 | 用团队 |
| **Manager** | ✅ 直接操作 | ❌ | ❌ |
| **创建/销毁 Team** | ✅ | ❌ | ❌ |
| **创建 Worker** | ✅ 全局 | ✅ 自己 Team | ❌ |
| **创建 Human 账号并拉入团队** | ✅ 全局 | ✅ 自己 Team | ❌ |
| **管理团队管家的 SOUL/Skills** | ✅ 所有 Team | ✅ 自己 Team | ❌ |
| **管理 Worker 的 SOUL/Skills** | ✅ 所有 | ✅ 自己 Team 的 | ❌ |
| **与团队管家对话** | ✅ 所有 | ✅ 自己 Team | ✅ 自己 Team |
| **与 Worker 对话** | ✅ 所有 | ✅ 自己 Team 的 | ✅ 自己 Team 的 |
| **创建 Case** | ✅ 任意 | ✅ 自己 Team | ✅ 自己 Team |
```

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/69d635492d289a10eca1fe8d/1286e3d4-3d28-46e9-890a-13ae8c227da7.png)

至此，群里的 Human 角色都可以 @sre-bot 来下发任务了，但是只有“团队负责人”可以更新 sre-bot 的技能和 soul：

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/69d635492d289a10eca1fe8d/c45779a0-8927-4b5b-a1fd-297ffcc067b8.png)

配置好权限之后，如果 sre-bot 不响应，让 manager 重启下 sre-bot worker，否则虽然配置都对，依然不会生效。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/69d635492d289a10eca1fe8d/f91a050a-8ea9-4485-9660-d01fe8735c7d.png)

▍创建 SRE Worker 数字人

泰山的 SRE 智能体设计如下：

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/69d635492d289a10eca1fe8d/0c8667fc-2cf8-4885-9890-a3415ad2d4c3.jpeg)

可能有人会问，为什么设置 5 个数字人，而不是让一个数字人去执行呢？我们先对两个方案做一个对比：

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/69d635492d289a10eca1fe8d/fd1459f5-04c2-41ac-a6c8-c134d723b34f.png)

然后我们结合两个场景来看看两个方案的不同：

**故障排查场景：生产环境 Pod CrashLoopBackOff**

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/69d635492d289a10eca1fe8d/1be6793a-b91b-412f-8e42-a502e18a5149.png)

**新版发布场景：文档更新 + E2E 验收 + 故障排查**

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/69d635492d289a10eca1fe8d/e78ed74c-ff3d-4ce3-9265-94ce8205067e.png)

**看到这，大家可能有一致的感受，Agent Team 需要花费较多的时间设计数字人的架构，依赖个人经验；从 ROI 角度看，适合周期性任务（一劳永逸）或者复杂、长程任务。**

接下来，我们基于以上架构在 HiClaw 中构建所有 SRE Worker 数字人，并构建 Human 和所有人相关的权限；由于每个 Worker 数字人就是一个 Copaw/OpenClaw，因此相关的配置也非常简单：

```
新增5个 worker 数字人：
| 数字人 | 领域 | 能力 | 涵盖 skill |
| --- | --- | --- | --- |
| 泰山 Knowledge Kit | 知识领域 | 通过 knowledge-kit 命令将文档按指定 spec 转换为结构化知识 Markdown。 | knowledge-skill |
| 泰山 QA/E2E 数字人 | 测试域 | 根据用户提供的验收表（xlsx）、目标 URL 和 Cookies（或通过 Argo UI MCP 自动获取），自主生成 Agent 执行指南并不中断地完成全部功能点验收，最终输出含验收结果的验收表。 | agent-prod-e2e-testing |
| 泰山 QA/OpenAPI 数字人 | 测试域 | 自动为阿里云 Java SDK 产品接口生成测试用例，并自动提交代码、创建 Code Review。 | api-resource-classifier, api-test-auto-submit, api-test-generator |
| 泰山运维/泰山咨询和诊断数字人 | 运维域 | 查询实例的详情，k8s 资源等信息；云产品或者实例的咨询或者诊断专家，但是无法做k8s底层的根因诊断。OXS区产品（HSF (Configserver)、Diamond、Vipserver、MetaQ、SchedulerX2.0）的知识答疑，云产品 FAQ、实例诊断，故障诊断、最佳实践咨询等。 | taishan-instance-query, taishan-ticket-skills |
| 泰山运维/K8S RCA 数字人 | 运维域 | Kubernetes 根因分析和诊断专家，通过k8s clusteruuid、pod等信息来进行问题诊断。当用户遇到 K8s 相关问题（Pod 异常如 Pending/CrashLoopBackOff/ImagePullBackOff/Terminating/Evicted、Deployment/StatefulSet/DaemonSet 状态异常、节点 NotReady、服务无法访问、kubectl 报错、容器/调度/网络/存储问题）时，立即使用此 skill。通过 SOP 驱动的方式，遵循「先规划、后执行」原则，使用 5 Whys 方法定位可行动、防复现的根因。 | k8s-rca-skills |
```

紧接着，admin 让 Manager 赋予 sre-bot 相关权限。

```
@manager: 请赋予 sre-bot 创建worker和管理worker的权限，并可以自由分配任务给worker
```

但是 **sre-bot 并不具备创建 worker 的 skill 能力，最终在 Manager 的协作完成任务。**

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/69d635492d289a10eca1fe8d/6592d6bb-fb50-44de-818c-0b088f53adfd.png)

让 sre-bot 将数字人加入群聊。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/69d635492d289a10eca1fe8d/6e26d0ca-0b6f-484b-914a-bee23c681146.png)

至此，完成 SRE 的 HiClaw 组织构建，下面开始体验一把。

**03**

***HiClaw 多智能体的运维场景***

*Cloud Native*

我们设定了阿里云 MSE 微服务引擎这款产品，网关变配失败的问题排查场景。

**角色：**L1/L2 客服，产研。

**场景**：在 SPE 环境中，预先购买一个 MSE 云原生网关实例，发现 pod 起不来。

▍真人：发起任务

SRE 团队负责人通过 Team Leader（SI Put）下发诊断指令，触发多智能体协同流程，系统自动创建独立任务空间，隔离上下文，避免干扰其他任务。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/69d635492d289a10eca1fe8d/1c524250-3e7f-419a-a5c5-d19c873daa09.png)

▍SRE 团队管家数字人：分解任务

Team Leader 基于预设 SOP，将“K8s 实例调度失败”问题拆解为三阶段任务：实例状态核查 → 资源瓶颈诊断 → K8s 维度根因分析，并按顺序调度对应 Worker。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/69d635492d289a10eca1fe8d/6fcf3c53-8193-42d9-9882-f0f3c64b251e.png)

▍SRE 团队管家数字人：拉项目群&下发任务

团队管家数字人在群里，把每个人任务下发给对应的数字人（泰山诊断数字人和 K8s RCA 数字人）。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/69d635492d289a10eca1fe8d/dc66c44f-0658-490d-927a-ab83ce82e8ba.png)

▍泰山诊断数字人：实例基础信息获取和实例诊断

泰山诊断数字人调用泰山系统接口，查询目标实例的运行状态，确认其中一个 pod 的状态其处于“Pending”，调度失败。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/69d635492d289a10eca1fe8d/e7da52c3-bb00-44c2-872a-fd26bff5fde2.png)

▍泰山诊断数字人：实例诊断

泰山诊断数字人实例诊断报告，调度失败日志指向“Insufficient CPU/Memory”，初步锁定为节点资源不足，且 PVC 无法绑定 PV。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/69d635492d289a10eca1fe8d/02cc0965-f614-4d6c-bf94-e9db8d755c3d.png)

▍K8s RCA 数字人：K8s 诊断

K8S RC Agent 启动标准诊断流程，发现异常节点（work-a）的 CPU 使用率持续 >95%，内存可用量低于 5%，确认为节点池容量瓶颈，但无法定位具体 Pod 或服务。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/69d635492d289a10eca1fe8d/589893ef-f96c-48ca-9b30-8c86168e284c.png)

按 SOP 依次排查：Pod 调度策略、节点亲和性、Taints/Tolerations、Eviction 阈值，最终确认因节点资源枯竭，K8s 调度器拒绝了新 Pod 的调度请求。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/69d635492d289a10eca1fe8d/659509d2-d88c-4f51-9834-e878442e60b5.png)

▍SRE 团队管家数字人：汇总结果

Team Leader 整合三阶段结果，生成结构化报告，明确根因为“work-a 节点池资源不足导致调度失败”，并推荐执行“扩容 work-a 节点池+2 节点”操作，附带资源预估与影响评估。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/69d635492d289a10eca1fe8d/dd960eff-55df-4c69-8558-1e907845e5ce.png)

整个流程无需人工干预，智能体串行协作完成端到端诊断，输出可直接交付运维团队的标准化操作方案，实现从问题发现到修复建议的自动化闭环。

**04**

***总结***

*Cloud Native*

个人养虾的热度回落，恰恰说明 AI 智能体正在从尝鲜走向日常。Claw 已经成为许多人和团队每天离不开的工具入口，而企业端也开始认真评估规模化建设虾场的路径。我们在 SRE 场景的实践验证了一个核心判断：智能体的价值不在于单体有多强，而在于能否用平台化的方式让它们协同生长。

从实际收益看，HiClaw 带来的变化是多维度的：

- 效率层面，大量重复性的巡检、发布、故障响应工作由 Agent 接管，人工介入频次显著下降，部分周期性任务实现了从“人盯”到“人查”的转变。
- 协作层面，SOUL 和 Skills 作为可复用资产沉淀下来，跨团队共享而非重复建设，新智能体的上线周期从开发级缩短到配置级。
- 更深层的价值在于业务创新——当构建智能体的门槛降低到业务团队可以自主完成，探索新场景的成本也随之降低，AI 不再是平台团队的专属工具，而成为每个团队都能调用的生产力。


HiClaw 让团队把重心从写代码转向写配置，把核心资产沉淀为 SOUL 与 Skills，把复杂问题交给 Team 而非单个 Agent——不是造更强的智能体，而是造能长出智能体的土壤。这条路，无论个人还是企业，逻辑是相通的。

