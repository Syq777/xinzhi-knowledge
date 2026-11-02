---
作者:
  - "阿里云云原生"
原文链接: https://mp.weixin.qq.com/s?__biz=MzUzNzYxNjAzMg==&amp;mid=2247584314&amp;idx=1&amp;sn=3d08dd04e5a9d8e6b5601df2d81f3729&amp;chksm=fba912df14b83e00cc6da319775b3d3d564eca304f0af5d1caac76de9f7995439bbd1af4e897&amp;mpshare=1&amp;scene=1&amp;srcid=0605ErPY2Ol6AAsfFkPhvX5z&amp;sharer_shareinfo=7affc05651ad05956dd4a447ed3215f8&amp;sharer_shareinfo_first=7affc05651ad05956dd4a447ed3215f8#rd
发布时间: ""
收藏时间: "2026-06-05"
关联日记: "[[2026-06-05]]"
tags:
  - 文章
---
![image.png](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6a22b04e95975857e515b238/564ab36f-93ac-43fe-b96a-3fe8ccf8e7c1.png)

**01**

***概述***

*Cloud Native*

随着 AI 模型能力越来越强、Agent 框架越来越完善，Agent 正从一问一答的答疑助手，走向可以自主执行任务的个人助手，可以代替人做自动化的工作。定时任务是 Agent 自主工作的主要方式，最近流行的通用智能体（比如 OpenClaw）都内置了定时任务功能。

在当前算力持续紧张、企业 IT 支出越来越高的背景下，Agent 普遍面临资源利用率低、成本高昂的困境。阿里云中间件 MSE 团队正式推出 AI 任务调度**[1]**产品，统一管理和调度 Agent 的定时任务，提供高稳定、高安全、可观测的 AI 任务解决方案，结合 Agent Sandbox**[2]**运行时，可以做到动态休眠/唤醒 Agent，帮助成本下降 90% 以上。

**02**

***AI Agent 为什么成本高***

*Cloud Native*

对于个人用户来说，Agent 部署在本地 PC 电脑，配置了几个定时任务自动干活，并没有给用户带来额外成本。但是个人电脑不可能 7*24 小时一直开机，所以对于企业用户来说，都会选择把 Agent 部署在云端。

传统的 Web 应用，计算层和存储层一般是分离的，可以做到无状态，且计算层和存储层都可以多租共享，资源利用率比较高。而 Agent（以 OpenClaw 为例）有如下特点：

- **有状态：****会话、记忆、任务配置都存在本地磁盘，销毁会全部丢失。**
- **安全隔离：****Agent 可能需要操作文件系统、操作浏览器、运行代码，需要完全隔离。**
- **资源利用率低：****大部分时间空闲，资源利用率低。**


这决定了 OpenClaw 这类 Agent 不能像传统 Web 应用一样，通过多租共享资源来提升资源利用率，如下图所示：

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6a22b04e95975857e515b238/7b2be7c6-a4f6-4686-9d35-e5f212367cc2.png)

**总结**：AI Agent 出于上下文隔离和安全需求，需要独占；大部分时间空闲，资源利用率低，但是本地持久化、有状态等原因，无法销毁和缩容；导致 Agent 成本比传统 Web 应用高很多。

**03**

***AI 任务调度+Sandbox 解决方案***

*Cloud Native*

Agent Sandbox 是面向 AI Agent 的沙箱运行时，可以实现 Agent 的安全隔离。以阿里云容器计算服务 ACS 的 Agent Sandbox**[3]**为例，它是阿里云容器推出的一款面向生产级 AI 智能体的沙箱算力，提供 MicroVM 级别的隔离运行环境，内存级休眠唤醒、Checkpoint 克隆能力，最高每分钟 15K Sandbox 的大规模弹性扩展能力，全面兼容 Kubernetes 原生生态、无缝对接 E2B SDK、AgentScope 等主流 AI Agent 框架和工具。

如果单独使用 Agent Sandbox，没法做到 OpenClaw 的动态休眠/唤醒，因为 OpenClaw 原生的定时任务是内置在 gateway 进程中的，Agent Sandbox 没法感知什么时候有任务要执行，也没法感知什么时间段是空闲的。所以需要结合 AI 任务调度一起使用，如下图：

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6a22b04e95975857e515b238/35a4c7cd-40a9-4c09-8f6f-3d7ccf1a1363.png)

1. 将 OpenClaw 中的定时任务托管到 AI 任务调度平台中进行管理和调度。

2. 将 OpenClaw Agent 纳管到 AI 任务调度平台中，AI 任务调度基于所有任务的调度时间可以算出：

a. 如果某个 OpenClaw 未来 15 分钟没有任务调度，进行休眠。

b. 如果某个 OpenClaw 未来 10 分钟有任务调度，提前唤醒。

AI 任务调度除了可以做到 Sandbox 的定时休眠/唤醒，还有如下能力：

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6a22b04e95975857e515b238/2e2540f6-333b-49c0-8370-7110d27a8869.png)

- **Agent 任务统一管理：****兼容主流开源 OpenClaw/Hermes/Dify 等 Agent 协议，提供定时任务的统一管理、多租户隔离、精细化权限管理等能力。**
- **Agent 资源弹性伸缩：****运行时与定时调度能力解耦，集成 Sandbox 能力，可以在没有任务调度的时候休眠 Sandbox，显著提升 Agent 资源利用率，降低用户成本。**
- **企业级任务治理：****支持任务的会话管理、运维操作、版本管理、全链路可观测、报警监控、问题诊断、限流控制等全生命周期治理能力。**
- **任务评估与自进化：****任务每次运行结束有任务状态，还能进行打分进行结果评估，联合全链路可观测数据，进行任务参数/Prompt 自进化，让任务越跑效果越好。**
- **多 Agent 下任务协调：****基于工作流做多 Agent 的依赖编排，做流水线；智能路由，总体负载均衡；任务批处理，提高任务处理速度。**


**04**

***场景示例，成本下降 90% 以上***

*Cloud Native*

假设 OpenClaw 有 5 个定时任务：

- job 1：每天 8:00 开始运行，8:10 分运行结束。
- job 2：每天 8:00 开始运行，8:30 分运行结束。
- job 3：每天 12:00 开始运行，12:10 分运行结束。
- job 4：每天 18:00 开始运行，18:10 分运行结束。
- job 5：每天 18:00 开始运行，18:30 分运行结束。


使用 AI 任务调度+ Sandbox 休眠能力，可以做到未来 15 分钟没有任务调度则休眠，未来 10 分钟有任务调度则提前唤醒：

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6a22b04e95975857e515b238/57844c7f-53a8-467a-a579-aaef082a6996.png)

如上图所示，一天 24 小时，OpenClaw 仅工作 100 分钟，成本降低 90%+。

**05**

***AI 任务调度免费公测***

*Cloud Native*

AI 任务调度现已开放免费公测：

- **OpenClaw Agent：**集成 OpenClaw Agent 并配置定时任务https://help.aliyun.com/zh/schedulerx/ai-task-scheduling/getting-started/integrate-openclaw-agent-and-configure-scheduled-tasks


- **Hermes Agent：**集成 Hermes Agent 并配置定时任务https://help.aliyun.com/zh/schedulerx/ai-task-scheduling/getting-started/integrate-with-the-hermes-agent-and-configure-scheduled-tasks


如果有任何问题，欢迎加钉钉群（群号 23103656）一起交流 ^^

相关链接：

[1] AI 任务调度

https://mse.console.aliyun.com/#/ai-job/cluster

[2] Agent Sandbox

https://agent-sandbox.sigs.k8s.io/

[3] ACS Agent Sandbox

https://help.aliyun.com/zh/cs/user-guide/agent-sandbox

