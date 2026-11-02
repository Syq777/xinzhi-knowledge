---
作者:
  - "XEngineer 新工科计划"
原文链接: https://mp.weixin.qq.com/s?__biz=MzIwMzQ4ODU1NQ==&amp;mid=2247488182&amp;idx=1&amp;sn=22916ade0ddc329542ebdecc18ab402a&amp;chksm=97c75e8922cff4b6793dccfea54a00bab86867bc74ce6454d4562a56ec44f5a926ac1877cf2d&amp;mpshare=1&amp;scene=1&amp;srcid=0805FmJYnLo8FFdw8Daaawi7&amp;sharer_shareinfo=d1450fa379e2ae68dce6d3a757873d54&amp;sharer_shareinfo_first=d1450fa379e2ae68dce6d3a757873d54#rd
发布时间: ""
收藏时间: "2026-08-05"
关联日记: "[[2026-08-05]]"
tags:
  - 文章
---
你让它给系统增加邮件通知，它很快就能完成；接着再增加短信、Slack 和 Webhook，它也会继续沿着已有方案向前推进。等到业务提出重试、审计、限流和统一错误处理时，AI 仍然能够迅速交付。每一个需求单独验收，似乎都没有问题。

可当企业微信成为下一个渠道时，事情开始变得不对劲。原有发送流程要改，重试和审计要重新接入，限流与错误处理也要再补一遍。功能确实越来越多，但任何一次改动都会触碰越来越大的范围。系统看起来拥有了更多能力，实际却在失去演进能力。

这可能是 AI Coding 时代最容易被忽略的矛盾：AI 大幅降低了增加代码的成本，却不会自动降低理解、修改和维护系统的成本。如果一个新需求总是对应一段新实现，增长就只能以加法发生。真正的构架工作，是找到那些可以被反复组合的稳定机制，让能力增长不再要求复杂度同步增长。

所谓“少即是多”，不是追求更少的文件、类或代码，而是用少数稳定概念控制大量行为。

01-当“增加功能”变得太便宜

回到通知系统。最初只有邮件时，只要完成“把消息发出去”这一件事就够了。后来短信、Slack 和 Webhook 陆续到来，团队很自然地为每一种渠道分别完成发送。这种做法并没有明显错误，它甚至是最直接、最容易验收的选择。

问题出现在另一类需求到来之后。重试、审计和限流并不属于某个特定渠道，它们横跨全部发送行为。如果系统没有清楚表达“一次发送究竟经历什么”，这些规则就只能散落在不同渠道里。

于是需求开始以一种很有迷惑性的方式增长：

- 增加邮件，完成一次发送；
- 增加短信，再完成一次发送；
- 增加 Slack，再完成一次发送；
- 要求失败重试，分别给三种渠道补上；
- 要求记录审计，分别给三种渠道再补一遍；
- 要求限流和统一错误处理，修改范围继续扩大。


每一次交付都可以成功，每一次交付也都让下一次修改变得更昂贵。这里真正重复的不是某几行实现，而是三个没有被说清楚的系统机制。

系统需要一种渠道选择机制，用来决定谁负责发送、如何适配外部协议，以及怎样处理渠道特有的错误。其次，一次发送有共同的生命周期：任务被创建、执行，最终形成成功或失败的结果。最后，重试、审计、限流和超时属于通用策略，它们不应该随着渠道数量一起复制。

当这些机制没有自己的名字时，每增加一个渠道，我们就会重新实现一次整个系统。

02-从反复修改里找出稳定机制

构架的起点不是画图，也不是把所有渠道塞进一个更大的入口，而是在第三个相似需求出现时，暂时停止复制。

此时最值得问的不是“实现长得像不像”，而是“哪些规则在不同场景里反复成立”。在通知系统中，邮件、短信和 Slack 的接入方式不断变化，但一次发送从创建到完成的过程相对稳定；外部渠道的身份认证和消息格式不断变化，但重试、审计和限流的业务规则相对稳定。

沿着这条边界，原本缠绕在一起的工作可以被压缩成四个人人都能理解的概念。

- 消息: 回答“发送什么、发给谁”，但不决定最终使用邮件还是企业微信。
- 渠道: 回答“怎样通过某个外部平台发出去”，负责消化每个平台自己的认证、格式和失败方式。
- 通用规则: 回答“失败是否重试、过程是否审计、速度是否受限”。
- 投递记录: 则代表一次可以追踪的发送，保存它正在进行、已经成功还是最终失败。


整个系统由此获得了一个更稳定的表达：

消息 × 渠道 × 通用规则 → 一次可追踪的投递

这个公式的意义不在于形式漂亮，而在于它改变了能力增长的方式。假设系统有四个渠道和三套策略，加法式实现很容易长成十二套相互缠绕的逻辑；一旦渠道和策略可以独立组合，十二种能力便不再要求十二套实现。

构架中的“乘法”，就是让新增能力主要来自已有要素的重新组合，而不是来自稳定内核的持续膨胀。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6a733b30fe52c220cf447cee/cdc32003-ad52-4ef5-b82f-d5671aa43260.png)

03-第 N+1 个需求会暴露抽象的真假

任何抽象在纸面上都可以显得优雅，真正的考验来自下一个同类需求。

如果系统现在要增加企业微信，加法式方案会再次改动原有发送流程，把重试、审计、限流和错误处理接入一遍。采用前面的模型后，主要工作应该集中在增加一种企业微信渠道，并把它接到统一发送入口。消息、投递过程和通用规则应当直接复用，邮件、短信等已有渠道也不应该被重新修改。

这并不意味着原有系统绝对不能修改。更实际的判断标准是：变化是否集中在“增加一种渠道”这件事上，还是继续扩散到发送过程、重试、审计、限流和所有已有渠道。

因此，第 N+1 个需求像一面镜子。它会暴露我们得到的究竟是一个可扩展的抽象，还是仅仅把所有特殊情况藏进了同一个入口。如果新增同类场景时仍然必须修改原有流程、复制通用规则，并重新检查全部渠道，那么复杂度并没有被消除，只是被重新包装。

04-好的抽象不仅能够接纳，也能够拒绝

“少即是多”很容易被误解为：应该找到一个足够强大的抽象，把所有相关需求都塞进去。这样做的结果往往不是统一，而是一个充满特殊字段、例外状态和条件开关的庞然大物。

假设通知系统随后需要支持双向实时客服。它同样涉及消息，却还包含持续会话、用户回复、消息顺序和在线状态。原来的投递模型主要描述“一条消息如何通过某个渠道可靠送达”，实时客服处理的却是“一个长期存在的双向会话如何持续交互”。

两者可以共享基础设施，却未必共享同一个核心语义。强行把实时客服包装成另一种发送渠道，会让原本清晰的单向投递模型背负大量例外。

好的抽象必须清楚说明自己压缩了什么重复、保持什么不变量、允许哪些变化，以及在哪个场景下会失效。它不仅需要接纳同类变化，也需要拒绝语义不同的问题。

05-方块为什么能够生成一个世界

通知系统只是一个业务案例。把视线移向更成熟的系统，会发现很多强大产品都依赖同一种结构：它们没有为每一种最终能力单独建造一套机制，而是找到了足够小、足够稳定的生成原语。

2009 年，Minecraft 第一次公开出现时，游戏工业正在竞相追逐更逼真的画面、更庞大的制作预算和更完整的剧情体验。它看起来却像一个反方向的实验：粗糙的像素方块、没有固定任务线，也没有替玩家预先建好的宏大世界。

2011 年正式版发布后，这个看似简陋的实验开始跨越 PC、主机和移动设备；

2014 年，微软以 25 亿美元收购 Mojang；到 2023 年，它的累计销量已经突破 3 亿份。

这场竞争最有张力的地方在于，Minecraft 并没有在画面精度和预制内容数量上击败那些大制作游戏。它改变了战场。别的游戏不断增加制作者交付给玩家的内容，它把“生产内容”的能力交给了玩家。房屋、城市、机关、冒险地图和多人服务器不必全部由 Mojang 逐项开发，而是由玩家在同一套规则上持续生成。

2024 年，也就是游戏诞生十五周年时，官方统计玩家一年内探索了超过 8500 万个生物群系、破坏了超过 3000 亿个方块。

这些数字真正说明的不是地图有多大，而是一个仍在高速发生的创造活动。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6a733b30fe52c220cf447cee/f4ba93a2-f6d3-4aae-8669-83ce4b9c803e.png)

支撑这一切的核心并不复杂。Minecraft 没有为山脉、洞穴、房屋、城市和机关分别设计一套世界系统，而是把世界的可组合结构压缩成方块。

方块记录类型、状态和空间位置，世界系统再用相对统一的生成、放置和邻接规则解释它们。地形、建筑和红石机关的巨大差异，来自同一种原语在空间中的不同排列。

方块 × 空间位置 × 组合规则 → 一个可以持续生成的世界

复杂度由组合产生，而不是由原语数量产生。这正是 “Block is all you need” 想表达的含义。未来的 Minecraft 仍然会加入新生物、新地形和新玩法，但它最重要的增长方式不是不断替换底层世界模型，而是让新内容继续进入方块、物品、实体和规则构成的组合系统。十五年之后，它仍然活着，恰恰因为这个世界没有被一次性做完。

当然，Minecraft 并不真的只有方块。生物、玩家、时间和事件仍然需要其他概念。方块之所以强大，不是因为它解释了一切，而是因为它准确覆盖了“世界的可组合结构”这一边界。

06-单元格为什么能够承载无数模型

电子表格的故事开始于一个极其具体的痛点。1979 年，VisiCalc 登上 Apple II，把纸面表格中最折磨人的工作——一个数字改变后手工重算整张表——交给了计算机。它很快成为推动个人电脑进入企业的“杀手级应用”。1983 年，Lotus 1-2-3 针对 IBM PC 提供更快的计算，并把表格、图表和数据能力装进同一个产品，很快反超 VisiCalc。1985 年，Excel 首先在 Macintosh 上发布，1987 年进入 Windows，电子表格的主战场又从字符界面转向图形界面。

这是一场持续了几十年的产品战争，但胜负并不只取决于谁拥有更多菜单。VisiCalc 赢在让商业用户可以自己建立模型；Lotus 赢在保留单元格心智模型的同时，把速度和集成能力推到 IBM PC 的极限；Excel 则把同一个模型带进图形界面和 Office 生态。后来 Google Sheets 又把实时协作变成新的竞争维度，迫使电子表格从桌面文件继续演进为云端共享计算空间。每一代胜出者都增加了新的能力，却没有要求用户放弃“把值和公式放进格子、让引用自动传播”的基本方法。

2025 年，Excel 已经发布四十年。微软当年财报披露 Microsoft 365 消费订阅用户达到 8900 万——这不是 Excel 的独立用户数，却足以说明它所在的生产力平台仍然具有庞大而增长中的用户基础。与此同时，Excel 已经把动态数组、Power Query、Python 和 Copilot 接到传统工作表上。它未来可能越来越像一个由 AI 辅助的数据与计算环境，但 AI 生成的公式、Python 结果和自然语言分析，最后仍需要落回一个用户能够查看、引用和重算的模型。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6a733b30fe52c220cf447cee/e61b52a6-0c8d-41af-9c93-19a3041c6c6e.png)

电子表格看起来与 Minecraft 毫无关系，却采用了相似的构造方式。预算、排班、库存、实验记录和财务模型差异巨大，电子表格不需要为每张报表开发一套程序，因为它把计算压缩成了单元格。

一个单元格可以保存值，也可以保存公式；公式又可以引用其他单元格。引用关系把大量单元格连接成依赖图。当上游数据发生变化，计算引擎沿着依赖关系重新计算下游结果。

单元格 × 引用关系 × 自动重算 → 一个可以持续扩展的计算模型

增加第十三个月、增加一组情景参数，或者增加一个新指标，通常只是在扩展依赖图，而不是重写计算引擎。“Cell is all you need” 的力量，来自最小计算单元、引用关系与统一重算机制的组合。

07-Git 为什么能够让分支如此便宜

Git 不是在一间安静的实验室里慢慢设计出来的。Linux 内核在 1991 年到 2002 年间主要依靠补丁和归档文件协作，后来使用分布式版本控制系统 BitKeeper。2005 年，Linux 社区与 BitKeeper 背后的商业公司关系破裂，免费使用安排也随之终止。Linus Torvalds 面对的不是“做一个更好用的小工具”，而是必须尽快为一个拥有大量并行贡献者的大型项目重建协作基础。

当时的版本控制战场上，CVS 和 Subversion 代表的是更常见的集中式路线，BitKeeper 已经证明分布式协作可行，Mercurial 等新工具也在同一时期出现。Git 给自己的目标非常激进：快、简单、完全分布式，能够支持成千上万条并行分支，并高效处理 Linux 内核这样的项目。它早期并不以易用著称，却把最困难的规模问题压进了一套非常小的对象模型。

Git 后来的胜出也不是单靠一个命令行工具完成的。GitHub 从 2008 年开始把远程仓库、Fork、Pull Request 和社交协作连接起来，让 Git 的分布式对象模型获得了网络效应。到了 2025 年，GitHub 报告平台上已有超过 1.8 亿开发者和 6.3 亿个项目；一年内产生了接近 10 亿次代码推送。AI 正在让代码产生得更快，但这没有削弱版本历史，反而让“哪些状态可以信任、一次变化如何审查、何时可以回退”变得更重要。未来的协作者可能越来越多是智能体，Git 的快照和引用仍然是它们交换、审查和归并结果的共同底座。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6a733b30fe52c220cf447cee/31e63300-c37d-45e2-a0fb-a542e62409c8.png)

Git 的例子说明，稳定原语不一定是可见的界面元素，也可以是一种状态表达。

如果版本控制系统只维护一条越来越长的文件差异链，那么提交、分支、标签和合并都会被差异之间的复杂关系拖累。Git 选择把项目理解为一系列快照，并把内容组织成不可变、可复用的对象。

Blob 保存文件内容，Tree 保存目录结构，Commit 指向一次项目快照，分支则主要表现为指向 Commit 的可移动引用。对象通过内容寻址被复用，没有发生变化的内容不必重复保存。

复用旧快照 + 增加一次提交 + 移动一个引用 → 一条新的版本线

分支之所以便宜，不是因为 Git 少保存了历史，而是因为大量历史能够通过不可变对象共享。“Snapshot is all you need” 描述的是一种用稳定状态原语承载版本演进的方式。

08-Unix 工具为什么可以自由组合

1969 年，Ken Thompson、Dennis Ritchie 等人在贝尔实验室一台闲置的 PDP-7 上开始创造 Unix。1973 年，系统被改写为 C，这让操作系统第一次能够更容易地离开原来的硬件；1975 年，第六版开始广泛走出贝尔实验室，进入大学和研究机构。Unix 传播得如此成功，以至于成功本身制造了危机：厂商各自发展出不兼容的版本，AT&T System V 与 BSD 阵营长期分裂，1980 年代末甚至爆发了著名的“Unix wars”。

如果把竞争理解成某个商业产品垄断市场，Unix 并没有获得一个干净利落的胜利。Windows 赢得了个人电脑桌面，Linux 也不是简单由原版 Unix 代码延续而来。Unix 真正赢下的是更深的一层：它的进程、文件、Shell、管道和系统接口逐渐成为软件世界的共同语言。1988 年 POSIX.1 发布，1994 年 Single UNIX Specification 出现，竞争从“所有人必须运行同一份代码”转向“不同系统可以遵守同一组契约”。后来 Linux、BSD、macOS、云服务器和容器工具链把这种设计继续扩散。

这套体系今天仍然在演进。2024 年，The Open Group 发布 Single UNIX Specification Version 5，其核心同时成为 POSIX.1-2024；在 2025 年 11 月的 TOP500 榜单中，全球五百台最强超级计算机的操作系统家族全部是 Linux。严格地说，Linux 不等于认证 UNIX，但这组事实仍然说明：五十多年前形成的接口思想没有成为博物馆展品，它已经进入现代计算基础设施的日常语法。未来无论底层运行的是云主机、容器还是 AI 计算集群，只要工具仍能围绕文件、进程和数据流组合，这套契约就还在继续生长。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6a733b30fe52c220cf447cee/a0644d75-f0e7-43f9-b973-f21f8d08b2d3.png)

Unix 展示的正是这种“少”：极小的接口契约。

一个过滤工具不需要认识所有可能的上游和下游。它只需要从标准输入读取数据，完成自己的局部变换，再把结果写到标准输出。管道负责连接这些工具。

数据流 → 一次局部处理 → 数据流 → 下一次局部处理

读取、过滤、排序、去重、统计和格式化因此不必形成两两依赖。新增能力通常只需要增加一个新的变换，再把它插入已有管道。

“Stream is all you need” 并不是说所有软件都应该传递无结构的字节流。结构化事务、双向协议和复杂一致性仍然需要更强的契约。它说明的是：在适合流式处理的问题里，一个足够小且被共同遵守的输入输出协议，可以让工具数量增加，而组合成本保持稳定。

09-Kubernetes 为什么能够不断自愈

Minecraft、电子表格、Git 和 Unix 都把大量能力压缩到了稳定原语或接口上。Kubernetes 的特殊之处在于，它压缩的不是数据形态，而是系统改变状态的方式。

它的起点来自两股力量的相遇。Google 已经用 Borg 和 Omega 积累了十多年大规模工作负载管理经验；2013 年，Docker 又让普通开发者第一次如此容易地打包和运行容器。Docker 解决了“如何把应用装进一个可移植容器”，却把更大的问题暴露出来：当容器从一台机器扩展到成百上千台机器时，谁来调度、扩容、恢复和升级？

2014 年 6 月 6 日，Kubernetes 的第一个提交进入 GitHub；四天后，Google 在 DockerCon 上公开项目；2015 年 7 月，Kubernetes 1.0 发布并捐赠给新成立的 CNCF。当时的容器编排战场并不空旷，Docker Swarm、Mesos/Marathon、Cloud Foundry 以及各家自研系统都在争夺同一个入口。Kubernetes 早期甚至以复杂和难学闻名，它并不是凭借最短的安装命令取得优势的。

它真正改变竞争格局的，是把厂商能力放到可扩展边界之外，把“期望状态”留在一个开放、声明式的 API 里。云厂商可以提供网络和存储插件，企业可以增加自己的资源与控制器，但所有扩展仍然围绕同一种收敛机制工作。2015 年进入 CNCF 又让它不再只是 Google 的内部经验输出，而成为 AWS、微软、Red Hat、IBM、VMware 等竞争者也能共同投资的中立层。Kubernetes 没有消灭基础设施差异，而是让这些差异不必进入核心控制模型。

这场胜利留下了可观测的数据。到 2024 年 Kubernetes 十周年时，官方统计项目已经拥有超过 8.8 万名贡献者，来自 8000 多家公司；CNCF 的 2025 年度调查则显示，82% 的容器用户已经在生产环境运行 Kubernetes，高于 2023 年的 66%。它显然还是一个活的场景：下一阶段，GPU、分布式训练、推理服务和大规模批处理会给调度与资源管理带来新压力。Kubernetes 社区正在为 AI 和高性能计算调整硬件管理与批处理能力，但它不需要为每种新负载发明一套全新的中央编排流程。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6a733b30fe52c220cf447cee/683e1a97-2646-4dcf-aa8a-f18b65b6ac26.png)

一个长期运行的分布式系统永远在变化。容器会崩溃，节点会失联，负载会上升，新版本会发布，存储容量也会改变。如果我们为每一种故障编写一条从头到尾的恢复流程，流程数量会随着故障组合迅速膨胀。

Kubernetes 采用的是反馈控制。它不断重复同一个动作：

观察现在怎样 → 与希望的状态比较 → 采取缩小差距的行动 → 再次观察

事件在这里主要意味着“某个对象值得再看一次”。真正决定行动的，是控制器重新读取后看到的当前状态，而不是它对历史事件的记忆。即使事件重复、延迟，或者控制器重启，下一轮仍然可以根据当前世界继续收敛。

“Reconcile is all you need” 所指的，正是这种反复比较期望与现实的最小控制结构。十年前它让 Kubernetes 在容器编排战争中建立了共同语法，十年后它仍然可以用同一种语法吸收尚未出现的新型工作负载。

10-Kubernetes 的组件，只负责各自的一小段收敛

Kubernetes 并不是由一个万能控制器完成所有事情。它由许多相对简单的循环共同维持，每个组件观察不同对象、计算不同差距，也只采取自己职责范围内的行动。

ReplicaSet 关心的是副本数量。它观察自己拥有的 Pod，将当前数量与期望数量比较；数量不足便创建新的 Pod 对象，数量过多便删除一部分。它负责维持 Pod 的数量，却不负责选择节点，也不负责在节点上启动容器。

Deployment 关心的是版本演进。当 Pod 模板发生变化时，它观察新旧 ReplicaSet 和可用副本数，按照更新策略逐步放大新版本、缩小旧版本。Deployment 管理的是 ReplicaSet 之间的交接，而不是亲自逐个创建和运行 Pod。

Scheduler 处理的是位置问题。一个新 Pod 被创建时通常还没有节点。Scheduler 读取 Pod 的资源需求、调度约束和集群节点状态，先过滤不可行节点，再为候选节点评分，最终把 Pod 绑定到合适的节点。它只决定“放在哪里”，不负责启动容器。

kubelet 运行在每个节点上，负责把已经分配到本节点的 PodSpec 变成现实。它观察容器运行状态和健康检查结果，根据差距拉取镜像，启动、停止或重启容器。它不决定副本数，也不决定 Pod 应该被放在哪台机器。

HPA 观察 CPU、内存或其他指标，并把当前指标与目标指标比较。当负载上升时，它计算新的期望副本数，把“希望运行几个”的数字调大。真正创建 Pod 的工作仍然会沿着后续控制循环完成。

存储 Provisioner 则说明控制循环可以跨出集群。它观察尚未满足的 PVC 和 StorageClass，判断是否存在符合容量与类型要求的卷；如果没有，就调用外部存储系统创建卷，再把 PV 等结果写回 Kubernetes API。外部世界因此也能通过共享状态进入声明式循环。

这些组件看起来各不相同，内部却反复出现同一结构：观察、比较、行动、再观察。Kubernetes 的复杂能力，不是来自一个无所不知的中央流程，而是来自许多小循环之间的组合。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6a733b30fe52c220cf447cee/857d6588-6c3e-47ea-9af6-f20fed409e07.png)

11-一次扩容如何穿过五个循环

假设系统当前运行三个副本，负载突然上升。HPA 首先观察到指标高于目标，于是把期望副本数从三改成五。Deployment 接收到新的规模目标后，调整自己管理的 ReplicaSet。ReplicaSet 重新统计，发现当前只有三个 Pod，于是创建两个新的 Pod 对象。

新 Pod 还没有运行位置，Scheduler 随后为它们选择节点并完成绑定。目标节点上的 kubelet 看到新的 PodSpec，开始拉取镜像、启动容器，并把运行状态写回集群。

表面上看，这是一次完整的自动扩容；实际上，没有一个中央对象调用了整条流程。HPA 不认识 kubelet，ReplicaSet 也不负责调度。每一层只观察共享状态，并完成自己负责的那一小段收敛。上一层产生的结果，会成为下一层新的期望。

PlanetScale 在《The feedback loops behind Kubernetes》中把这种关系解释为级联控制：多个反馈循环层层连接，外层循环的输出成为内层循环的输入。系统能够自愈，不是因为某个组件掌握了一切，而是因为每个组件都遵守相同的反馈结构，同时守住了自己的职责边界。

12-把加法式开发变成乘法式构架

这些系统并没有共享同一种具体实现。

方块是数据原语，单元格是计算原语，快照是状态原语，数据流是接口契约，Reconcile 是控制循环。它们真正相似的地方，是都找到了一个稳定的生成规则，让后来出现的能力能够通过组合或重复解释产生。这种思考可以落回日常 AI Coding。

当第三个相似需求出现时，首先需要暂停继续复制。此时要寻找的不是相似实现，而是反复出现的过程、状态变化和业务规则。接下来应当把相对稳定的机制与真正变化的部分分开，为变化建立清楚的边界，而不是让特殊情况继续渗入原有流程。

抽象形成以后，还需要用下一个同类需求检验它。如果新增能力仍然要求修改原有流程、重新接入旧能力并扩大检查范围，说明变化并没有真正独立。与此同时，还要寻找一个语义不同的反例，确认抽象没有为了追求复用而越过自己的边界。

这个过程可以概括为五个动作：

- 停：第三个相似需求出现时，先停止继续复制；
- 找：寻找反复出现的业务过程和规则；
- 分：分开稳定机制与真正变化的部分；
- 抽：用少数概念表达共同结构；
- 证：用 N+1 和一个反例同时检验。


AI 很适合探索多个候选方案、比较修改范围，并实现已经明确的变化轴。但“哪些问题应该被压缩到一起”“哪个不变量值得保留”“什么场景必须被拒绝”，仍然需要清楚的构架判断。

这也意味着，给 AI 的任务不能只剩下一句“增加企业微信”。即使完全不看实现，我们仍然可以先要求它用业务语言回答五个问题：

- 现有四种发送方式，每次发送共同经历哪些阶段？
- 哪些规则应该对所有渠道保持一致？
- 企业微信只带来了哪些差异？
- 新增它以后，哪些旧能力不应该重新实现？
- 如果下一个需求是钉钉，系统还需要改动哪些部分？


接着，让 AI 给出两种方案，用“这次要改多少、旧能力能复用多少、下一次新增要付出多少成本”进行比较。构架判断因此不再依赖阅读实现细节，而变成任何产品负责人、业务专家或 Vibe Coding 使用者都能参与的验收。

13-结语

AI 时代当代码和功能都可以高速增加以后，构架第一次如此直接地决定一个系统会不会被自己的增长拖垮。

构架不是一组高级名词，也不是一张模块很多的图。它发生在一个非常具体的瞬间：当相似需求再次出现时，我们不再立刻增加一套实现，而是开始追问，是否存在一个更稳定、更小的生成规则。

方块生成世界，单元格生成模型，快照生成版本线，数据流生成处理管道，反馈循环生成自愈系统。它们共同说明，真正强大的系统并不依赖无休止地增加能力，而是依赖少数概念被不断重新组合。

少数稳定概念，乘以明确变化轴，才能产生大量可组合能力。这才是 AI 时代真正的“少即是多”。

我是在增加系统能力，还是只是在增加系统复杂度？

附: 参考与来源说明

1.Minecraft, [15th Anniversary Timeline](https://www.minecraft.net/en-us/15th-anniversary)、[Minecraft Live 2023 Recap](https://www.minecraft.net/en-us/article/minecraft-live-2023--the-recap-)、[A Year in Blocks 2024](https://www.minecraft.net/en-us/article/a-year-in-blocks-2024)；Microsoft, [Minecraft to join Microsoft](https://news.microsoft.com/source/2014/09/15/minecraft-to-join-microsoft/)。这些官方资料提供了发布时间、收购、销量和年度活动数据。

2. Minecraft, [What is Minecraft?](https://www.minecraft.net/en-us/article/what-minecraft)；Microsoft Learn, [Block JSON and Block Definitions](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/)。本文关于方块作为可组合世界原语的讨论参考了这些资料。

3. Computer History Museum, [The Origins and Impact of VisiCalc](https://computerhistory.org/events/origins-impact-visicalc/)、[Lotus Development Goes Public](https://www.computerhistory.org/tdih/october/6/)、[Mitchell Kapor](https://computerhistory.org/profile/mitchell-kapor/)；Microsoft, [The History of Microsoft — 1985](https://learn.microsoft.com/en-us/shows/history/history-of-microsoft-1985)、[Excel Celebrates 40 Years](https://news.microsoft.com/signal/articles/microsoft-excel-celebrates-40-years/)、[2025 Annual Report](https://www.microsoft.com/investor/reports/ar25/index.html)。这些资料支撑电子表格的产品时间线、竞争演进和当前数据。

4. Microsoft Support, [Overview of formulas in Excel](https://support.microsoft.com/en-us/excel/get-started/overview-of-formulas-in-excel)；[Display the relationships between formulas and cells](https://support.microsoft.com/en-US/Excel/display-the-relationships-between-formulas-and-cells)。本文关于单元格、引用关系和重算依赖的讨论参考了这些资料。

5. Git, [A Short History of Git](https://git-scm.com/book/en/v2/Getting-Started-A-Short-History-of-Git)、[What is Git?](https://git-scm.com/book/en/v2/Getting-Started-What-is-Git%3F)、[Git Objects](https://git-scm.com/book/en/v2/Git-Internals-Git-Objects)、[Branches in a Nutshell](https://git-scm.com/book/en/v2/Git-Branching-Branches-in-a-Nutshell)；GitHub, [Octoverse 2025](https://github.blog/news-insights/octoverse/octoverse-a-new-developer-joins-github-every-second-as-ai-leads-typescript-to-1/)。这些资料支撑 Git 的起源、设计目标、对象模型和当前开发活动数据。

6. The Open Group, [History of UNIX](https://www.unix.org/unix_history.html)、[The Single UNIX Specification V5](https://www.unix.org/overview.html)；TOP500, [Operating System Family: Linux](https://www.top500.org/statistics/details/osfam/1/)；GNU Coreutils, [I/O redirection](https://www.gnu.org/software/coreutils/manual/html_node/I_002fO-redirection.html)。这些资料支撑 Unix 的历史、标准演进、现代基础设施数据和流式组合机制。

7. Kubernetes, [10 Years of Kubernetes](https://kubernetes.io/blog/2024/06/06/10-years-of-kubernetes/)、[The History of Kubernetes and the Community Behind It](https://kubernetes.io/blog/2018/07/20/the-history-of-kubernetes-the-community-behind-it/)；CNCF, [2025 Annual Cloud Native Survey](https://www.cncf.io/reports/the-cncf-annual-cloud-native-survey/)。这些资料提供了 Kubernetes 的项目时间线、社区规模和生产采用率。

8. Fatih Arslan, [The feedback loops behind Kubernetes](https://planetscale.com/blog/the-feedback-loops-behind-kubernetes), PlanetScale, 2026-06-16。本文关于 Kubernetes 闭环控制、level-triggered reconciliation、多个控制循环级联协作的讨论，受到该文启发。

9. Kubernetes, [Controllers](https://kubernetes.io/docs/concepts/architecture/controller/)、[ReplicaSet](https://kubernetes.io/docs/concepts/workloads/controllers/replicaset/)、[Deployment](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)、[Kubernetes Scheduler](https://kubernetes.io/docs/concepts/scheduling-eviction/kube-scheduler/)、[Cluster Architecture](https://kubernetes.io/docs/concepts/architecture/)、[Horizontal Pod Autoscaling](https://kubernetes.io/docs/concepts/workloads/autoscaling/horizontal-pod-autoscale/)、[Dynamic Volume Provisioning](https://kubernetes.io/docs/concepts/storage/dynamic-provisioning/)。本文对各组件职责和边界的说明以这些官方资料为依据。
