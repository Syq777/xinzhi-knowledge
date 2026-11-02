---
作者:
  - "海外独角兽"
原文链接: https://mp.weixin.qq.com/s/DfQFOgOZxhReNiXbYG8ybA
发布时间: ""
收藏时间: "2026-08-12"
关联日记: "[[2026-08-12]]"
tags:
  - 文章
---
[![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6a7bd45ce3d6f8391555511e/e97f2923-4e5b-4f4f-9d17-761e7249540f.png)](https://mp.weixin.qq.com/mp/appmsgalbum?__biz=Mzg2OTY0MDk0NQ==&action=getalbum&album_id=4157672299245862924&scene=21#wechat_redirect)

作者：Celia

编辑：Siqi

AI 的产品形态可能又到了一个新的范式迁移点。

　⁠

一个月前，Anthropic 在 Slack 里上线了 Claude Tag，这个产品并没有引起太多讨论和关注，外界只是把它当成 Anthropic 随手发的小功能。

　⁠

但实际上， Anthropic 内部对这个产品的期待远远超过外界感知，他们正在明确地把它当作下一代爆款产品来建设。在他们看来，Tag 可能是一种 10x Claude Code 的产品形态，对应万亿美元级别的市场空间。

　⁠

借用 Andrej Karpathy 的判断，Claude Tag 意味着 AI 产品的交互方式会真正开始迈入第三个阶段: Chat → Local Coding Agent → AI Coworker。

　⁠

这背后是三种工作模式同时发生迁移：从单人到多人，从被动到主动，从同步单次到异步长程。

　⁠

Coding 只是 AI 进入生产力场景的第一步，Claude Tag 以及它所代表的 AI Coworker 类产品形态可能会让 AI 真正走入 “替代白领” 的阶段。

　⁠

这种变化在 Anthropic 内部已经非常明显。团队的工作正在快速从 Claude Code 向 Claude Tag 迁移：目前产品团队超过 65% 的代码已经由 Tag 完成，一些员工甚至 90% 的工作都已经在使用 Tag 而非 Claude Code。

　⁠

为了理解这次变化，我们做了一些研究，也和一些关注这个方向的从业者聊了聊。在这里分享一些我们的观察，也欢迎感兴趣的朋友来继续找我们交流。

01.

## Introduction

　⁠

先做一些简单介绍，Claude Tag 相当于 Anthropic 正式推出的一个数字员工，Claude 可以以团队成员的身份直接加入公司的 Slack 频道，获得团队全部 context，用户只需在聊天框、文档等地方 @claude ，就能直接调用它来处理任务。

　⁠

目前整个产品仍在 beta 测试阶段，需要同时拥有 Claude 企业账号和 Slack 企业账号才能试用。

　⁠

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6a7bd45ce3d6f8391555511e/70466412-0cf9-4cbd-90da-799daffee7b4.gif)

Claude Tag 的几个核心能力包括：

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6a7bd45ce3d6f8391555511e/73b3b576-ec54-4982-bc20-a601e0c39132.png)

　⁠

除此之外，也支持配置 skills，支持设置长期目标，定时任务等。

　⁠

模型方面，目前可以接入 Fable 5、Opus 5、Sonnet 5、Opus 4.8 和 Opus 4.7，只有企业管理员可以在后台切换模型，普通员工则可以直接对 Claude 说 “这个用 Opus 5”，为具体任务临时切换模型。

　⁠

•定价：

　⁠

Tag 只支持在 Slack 的公共频道里面使用，以 usage-based 方式记账，记在企业账上，和 API 价格一致。

　⁠

如果要在 Slack 内跟 Claude 私聊，则不属于 Tag 的使用范围，需要绑定自己的 Claude 账号，走自己的会员套餐。

　⁠

•工具调用：

　⁠

支持几乎所有 MCP 集成，可以自由接入 GitHub、Notion、Google Drive、Snowflake 等。

　⁠

•运行机制：

　⁠

Runtime 全部由 Anthropic 云端托管，每个 thread 起一个临时 sandbox 跑完整 agent loop，底层复用的是 claude managed agent 的 tech stack。

　⁠

　⁠

02.

## Research 的三个核心要素

　⁠

Claude Tag 并不是一个多新的产品形态。过去半年多，市面上已经出现了非常多把 AI 放进协作场景、让大家像 @同事一样派活的产品。最早的是 Devin，最火的可能是 OpenClaw。

　⁠

但这些产品最终没有大规模铺开。小龙虾年初一度非常火，现在却也基本没有留存，背后的核心原因是模型能力还不成熟，Anthropic 的团队认为，其实模型只有到了 Mythos 级别，才算真正解锁了 AI Coworker 的产品形态。

　⁠

Claude Tag 不是第一个提出这个概念的产品，但它可能标志着这个品类开始真正走向成熟。

　⁠

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6a7bd45ce3d6f8391555511e/3c3232f0-7120-455d-b3b3-2bc26a7c17c6.png)

　⁠

这背后做了大量针对性的训练和打磨，Anthropic 在访谈里提到，Claude Tag 之所以好用，Research 层面核心是做好了三件事：

　⁠

1.Long-horizon autonomy

　⁠

模型能自主工作的时间，最大程度上决定了 AI 最合适的产品形态。

　⁠

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6a7bd45ce3d6f8391555511e/98421ce6-e53e-4032-b20e-bb58fed0d8ce.png)

　⁠

•当模型只能连续自主工作几分钟时，最合适的是 chat 或 autocomplete，需要全程 human in the loop；

　⁠

•当它能推进约 1 小时的任务时，local coding agent 开始成立，它可以在一个相对完整的工作流里读代码、改文件、跑测试，但仍然应该运行在用户身旁，方便随时接手；

　⁠

•只有稳定工作数小时之后，才值得做 async agent：用户下班了，Agent 仍在云端自主推进，最后带着结果回来。

　⁠

在 Anthropic 看来，Chat、local coding agent、async agent，本质上是不同 task horizon 下的阶段性最优产品。

　⁠

按照最新的 METR 评测，Mythos 已经能完成大约相当于人类专家连续工作 16 小时的任务。

　⁠

Claude Tag 又在此基础上增加了 Self-schedule。它可以先完成当前能做的部分，再把下一步安排到未来，比如，下周三回来检查实验数据。于是，单次 16 小时的执行能力可以被连续串联起来，变成持续几个月的长期任务。中间的等待、唤醒和衔接，都由模型自己完成。

　⁠

2.Memory

　⁠

记忆对 Tag 很重要，模型需要能真正记住人类交代的 to-do、方法和风格偏好，并把单次经验迁移到未来的任务中。

　⁠

Anthropic 尝试过很多记忆方案，最后发现，最好用的就是最朴素的文件系统，给模型一块可以长期读写的空间，放手让它自己维护。

　⁠

当然，这并不意味着每只 Claude 都可以随意翻看全公司的信息。Tag 的记忆会按照权限分层，不同频道之间默认像一间间彼此隔离的办公室：每只 Claude 只能看到自己所属频道里的 Context，只有获得授权后，它才能走出房间，去其他频道浏览信息。

　⁠

最终，Tag 的整套记忆库分成三层，所有记忆都可查、可改、可删。

　⁠

•Thread context：当前任务相关的对话和工作过程；

　⁠

•Channel memory：这个频道长期稳定的规则、决策、项目背景；

　⁠

•Workspace memory：整个公司的记忆，可以被同一 workspace 的其他公共 channel 复用。

　⁠

Anthropic 提到，他们尝试了好多年想把记忆做对，到现在这个节点才感觉终于跑通了。

　⁠

这其实也是 SOTA model 能真正拉开差距的地方：

　⁠

“我发现的一些最有意思的东西是：低阶模型和高阶模型之间的主要区别，就在于蒸馏（distillation）能力。高阶模型更能判断出怎么对记忆进行高维抽象，它们不只是记录一个具体事件，而是会真正思考，这段经验以后还能泛化到什么地方。”

　⁠

3.EQ

　⁠

Anthropic 还专门训练了 Claude Tag 的情商和分寸感，让它能判断出来什么时候该主动帮忙，什么时候该退居幕后。

　⁠

(我们自己试用完也觉得 Tag 比 Claude Code 情商明显高一个 level，沟通起来非常舒服，很有活人感，表情包也用得相当熟练。)

　⁠

　⁠

03.

## Use Case

　⁠

短期来看，Claude Tag 主要接手的还是基础执行工作，角色更像一个初级运营、行政或工程师。

　⁠

相比 Claude Code，它主要解锁了两类工作：

　⁠

1.高协作密度、高 context 密度类工作

　⁠

Claude Code 本质上还是单人模式。它可能对用户有所了解，却不了解业务每天发生的原始细节和动态进展，需要人类先把 Context 压缩、整理，再喂给模型。

　⁠

Claude Tag 则常驻在公司群聊里，天然了解一件事情的来龙去脉，所有人也都可以直接跟它协作，随时补充和纠偏。

　⁠

2.主动响应类工作

　⁠

Chat/Code/Cowork 都是人类主动发起的，得等人类意识到 “该干这件事了” 才会去用，Tag 则可以主动发现问题并揽下工作。

　⁠

比如下面这个 demo，线上突然出事了，它可以自己拉取监控、定位问题、编写修复，然后找相关负责人审批，人只需要点个最终同意。

　⁠

　⁠

还有一种情况是，很多时候组织内存在盲区，Claude 可以很好地补位，比如有人提了个 edge case 没人跟进、客户反馈里藏着一个重复 pattern。很多事情没人觉得这是自己的职责，Claude Tag 有能力自行提出来，自行包揽。

　⁠

总体来看，(1) 越需要协作的、 (2) 越依赖 context 的、 (3) 越需要及时响应的、 (4) 越碎片越 dirty 没人愿意做的，越适合交给 Claude Tag。

　⁠

Tag 的最佳用例其实就是 Anthropic 自己，在 Anthropic 内部，Tag 已经大量接管团队的日常工作：

　⁠

产品团队约 65% 的代码都由它生成；新人遇到法务、HR 等 onboarding 问题会直接 @Tag；客户反馈频道里的 bug 和数据频道里的所有查数问题，也普遍先交给它处理。

　⁠

不少员工还会把它当成一个贴身秘书，让它在几十上百个 Slack 频道中筛选重要信息、跟进多个 feature，并自动生成总结。

　⁠

长期来看，如果模型质量提高，Claude Tag 则可以完整替代一个人类员工，甚至成为整个公司的 OS 系统。

　⁠

现在 Anthropic 内部已经有了一些苗头，由于他们内部现在接的是更先进的模型，我们也可以通过这个看一下他们内部模型，加上 tag，能做到什么程度。

　⁠

最让我们惊艳的有三点：

　⁠

（1）Claude Tag 现在在 Anthropic 内部已经有点成为了一个 "全知全能的共享大脑"。

　⁠

人类只能同时进行一场对话，而 Claude 可以同时进行几千场，而且这一切都运行在一个共享的记忆层之上。

　⁠

所以，Tag 能同时整合所有的产品决策、工程决策和 GTM 决策，把很多分散的线索串起来，并主动提示每个人可能的盲区。

　⁠

Claude Code 设计负责人 Meaghan 在播客中提到，她现在和 Tag 聊着聊着，它常常会突然插一句：“某某刚就你之前问的那件事做了决定，你可能要调整一下构想”；或者“另一边刚决定把这个改名了，提醒你一下，我会把这里的文案也一并改掉。”

　⁠

为了让 Claude Tag 拥有全部的 raw context，Anthropic 也在刻意营造高度公开的文化，尽量把工作放在公开频道，减少私聊。

　⁠

（2）Tag 已经有了一点数字分身的雏形。

　⁠

Meaghan 还讲到，长期让 Tag 参与设计 review 之后，它慢慢学会了她做设计时的偏好和提问角度，比如这是为谁做的？想传达什么？这个跟我们的设计系统对得上吗... 于是它可以变成一个自动化的数字分身，直接在同事的设计草稿上迭代出一个更好的版本。

　⁠

现在，它甚至不必等 Meaghan 下指令，而会根据历史 PR、未来产品方向主动提案；有时还会找到相关同事，替她发起讨论。“嘿，Meaghan 之前是这么想的，这里有个原型你可以点点看，感受一下她的思路。”

　⁠

可以看出，Tag 已经能开始提炼员工的隐性知识。而这可能才是 Tag 对企业更大的长期价值：把优秀员工的经验、Taste 持续提取出来，变成整个组织都能调用的公共能力。

　⁠

（3）Claude Tag 已经开始完整接手一些复杂的大项目。

　⁠

比如 Anthropic 会直接让 Claude Tag 为某个渠道的留存率负责。

　⁠

Tag 会自己跑完整个循环：每周读数据 → 定位问题 → 提出多种假设 → 改代码提 PR → 小范围发布 → 在 Datadog 中监控 → 到可评估的节点通知负责人，中途发现异常也会主动提醒。

　⁠

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6a7bd45ce3d6f8391555511e/22285ca0-e48b-45b8-aa1e-3eb3932828d0.png)

这在正常公司里可能要 data scientist、工程师、增长 PM 等好几个人配合，现在 Claude 可以一个人把所有工作串起来，直接端到端为结果负责。

　⁠

　⁠

04.

## Claude Tag 是如何诞生的？

　⁠

我们一直认为，Anthropic 是目前产品能力最强的模型公司。

　⁠

OpenAI 烂尾过无数产品，但 Anthropic 过往几乎没有一个失败的产品线。ChatGPT 之后，AI 行业最重要的产品范式，比如 Claude Code、Cowork、Skills、MCP，都是 Anthropic 引领的。

　⁠

这背后，Anthropic 做产品是有一些清晰的方法论支撑的，所以这里也可以展开一起看看。

　⁠

相比 OpenAI，Anthropic 尤其在两个点上格外重视，Tag 的诞生过程也恰好同时体现了这两点：

（1）Dogfooding

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6a7bd45ce3d6f8391555511e/09a7b158-100b-49e5-b080-5c7e132e1041.png)

　⁠

Anthropic 的产品团队分为两个 Org：

　⁠

1.Product Team，负责持续打磨 Claude Code、Cowork 等已经成熟的产品。

　⁠

2.Labs，负责从 0 到 1 的前沿探索，主要有两个方向：

　⁠

•Close the Gap：缩小 Claude “理论上能做什么” 和 “大多数人日常怎么使用它” 之间的差距。Cowork 就是这条路线的产物。

　⁠

•Advanced Scout：提前判断哪些事情模型现在做得很差，但六个月后可能会突然做得很好。团队会提前把产品搭出来，等待模型能力成熟。

　⁠

因为本身做的就是 Coding/办公类产品，Anthropic 几乎所有 Prototype 的第一批真实用户都是自己的员工。

　⁠

整个公司就像一块大型实验田：

　⁠

Labs 团队会围绕不同的技术判断播下大量种子，再把它们放进 Anthropic 内部的真实工作环境里生长。有些很快因为需求不足而枯萎，有些只是模型能力的季节还没到，暂时进入休眠；只有极少数能在反复的 Dogfooding 中逐渐扎根。

　⁠

最终，一个产品只有在内部目标用户中跑出足够好的周活和留存，才有机会对外发布。Anthropic 现在同时运行着几百个 Prototype，其中绝大多数永远都不会面世。

　⁠

Tag 最早也是这样一个内部实验。它经历了几个月的真实使用和反复打磨，先改变了 Anthropic 自己的工作方式，直到今年 6 月才正式对外发布。

（2）面向未来做产品

Anthropic 更倾向于寻找一种足够宽的产品容器，确保产品可以持续吃到模型进化的红利。

　⁠

Claude Code 就是一个典型的例子。Anthropic 最早也有人提出要做 Cursor 式的 Autocomplete 产品，但领导层认为这种形态的上限不够高，最后转而押注了完整的 Coding Agent。Claude Code 刚发布时无人在意，直到一年后模型能力追上来才成为爆款。

　⁠

因此，Anthropic 今天也经常倒推一个问题：假设 Claude 8 已经存在，人们会怎么使用它？今天应该提前搭好什么？”

　⁠

Claude Tag 就是一种延展性比较强的产品形态。随着模型能力提高，它的价值可以分三层逐步展开：

　⁠

•Tag 的第一层意义是：打通 context 的交互入口。

　⁠

Context Layer 的重要性怎么强调都不过分。模型继续变强后，真正限制产品的不再是 Intelligence，而是 Context 的完整程度。过去大家都在想办法让人类先梳理 Context，再打包喂给模型，但其实现在不如直接让模型住进原始的 Context 里。

　⁠

Tag 第二层意义是：真正的数字员工，拥有记忆、主动性，能独立为完整的项目负责。

　⁠

Tag 的第三层意义是：AI Firm OS。它开始成为公司的共享大脑，能把组织所有的经验和能力都沉淀下来，Anthropic 内部现在已经有了一些雏形。

　⁠

未来，AI 最深远的影响可能不是 individual productivity，而是 collective intelligence。

　⁠

人类可以分工做事，但很难合并大脑。会议、文档和周报，本质上都是人类为了合并集体认知发明的工具，只是它们速度慢、带宽低，而且会损失大量隐性知识，而 Tag 不仅可以轻易 Fork，还可以轻易 Merge。让不同副本并行探索，再把所有副本的经验重新合并。结果是，AI 公司学习、扩张和自我改进的速度，可能远超今天的企业。

　⁠

　⁠

05.

## Claude Tag 能迎来快速爆发吗？

　⁠

接下来，我们好奇的一个问题是：Claude Tag 可能会以多快的速度在企业中落地？

　⁠

今年年初，市场其实已经给出过一次预演。

　⁠

当时有创业公司推出过一款和 Claude Tag 高度类似的产品 Viktor，它同样是让一个共享的 AI 同事进入 Slack / Teams 直接干活，用法跟 Tag 几乎完全一样，最大的区别在于可以自由切换模型。

　⁠

Viktor 的增长曲线相当惊艳：今年 2 月发布，10 周左右就做到 $15M run-rate，12000 多个企业完成下载安装，2000+ 付费客户，这个速度跟 Lovable、Manus 的早期增速差不多，基本上也是历史最高水平。

　⁠

今年 5 月它也完成了一轮很豪华的融资，甚至 Slack 的两个联创都投了它。

　⁠

所以，我们本来也对 Claude Tag 的落地相当乐观。但和几位同方向的创业者聊完后，我们的判断变得保守了一些：这类产品更多是在小型科技公司里找到了 PMF (Viktor 目前的客户也大多是 25 人以内的小公司)，要进入更广泛的企业市场，速度不会像想象中那么快。

　⁠

模型能力方面其实已经 ready 了，Opus 4.6 基本就能解锁这种产品形态，核心是有两大卡点：

　⁠

1.成本

　⁠

这是最大的问题。一家 20 人的小公司，如果彻底放开让所有人使用 Claude Tag，一个月可能烧掉大几万美金。

　⁠

我们自己试用时也被烧钱速度吓到过：接入 Opus 4.8 的情况下，只是让它研究一下如何成功访问某个公司官网，大约就花了 30 人民币；做一次搜集 Claude Tag 用户案例的 Deep Research，则要花 100 人民币左右。

　⁠

现阶段，只有高精行业里的高成本岗位，用 Claude Tag 才明确地比用真人划算。

　⁠

这背后，协作式 Agent 之所以成本非常贵，最核心的原因其实是 cache 命中率低。

　⁠

群聊场景下，Tag 每次都要读取大量上下文，在这个过程中，1V1 对话的上下文是一条相对连续的线。用户每问一句，模型通常只需要沿用上一轮状态，cache 比较容易命中，但多人协作天然是异步的：今天一个人发起任务，半天后另一个人再回来继续，这时 cache 往往已经失效；此外多人共享一个 Agent 时，每个人的权限和上下文都不同，cache 结构和单人使用完全不一样，很难直接复用。

　⁠

更麻烦的是，Connector 的增加会进一步放大这个问题。一个企业 Agent 可能要挂上百个 connector (法务、财务等不同部门各自有不同的 SaaS 工具)。工具一多：一是 agent 每次执行前要从庞大的工具池里检索该用哪个，不同人的用法和权限又不一样，选错重试的概率很高，cache 也很难复用；二是工具描述本身就要占用大量 context window，进一步推高了单次调用的成本。

　⁠

2.安全和权限管理

　⁠

Claude Tag 要想发挥价值，就必须获得大量公司 Context 和系统权限，但这类产品目前还没有办法完美解决安全和权限管理的问题。

　⁠

据我们了解，只有 Fable 5/Opus 5 这个级别的模型才能实现比较可靠的安全隔离，在 system prompt 约束下，基本不太容易发生 jailbreak。

　⁠

这有点像自动驾驶。对于企业权限系统来说，99% 的可靠度仍然不够，剩下的 1% 才真正决定产品能否落地。

　⁠

所以对于小型科技公司来说，组织通常开放透明，架构和权限关系也比较简单，可以大胆用起来。如果要走向更主流的企业市场，大多数客户还无法接受。

　⁠

我们翻看了过去一个月网上关于 Claude Tag 的所有试用反馈，讨论也比较类似，大家整体对它的工作能力还是满意的，真正的问题是用不起，也不敢完全放权。一方面是大量用户抱怨太烧钱；另一方面是不少人担心数据安全和 Lock-in。有人直接评论：

　⁠

“Claude Tag is like giving Anthropic your entire company, then renting it back from them.”

　⁠

　⁠

06.

## 一些延伸思考

　⁠

## 1. Claude Tag 可能会真正开启下一个产品范式

　⁠

走到现在，AI 产品大概经历了三个阶段：

　⁠

Chat → Coding Agent (Synchronous local agent) → AI Coworker (Asynchronous remote agent)

　⁠

Chat 是回答问题；Claude Code 开始执行任务；Claude Tag 则进一步进入组织，与多人协作、主动发现问题，并完整接手工作。

　⁠

这里的每一次跃迁，都可能比之前大一个数量级。

　⁠

Chat 对应的是信息和内容市场，付费意愿最低；Coding 让 AI 真正变成了生产工具，用户 ARPU 拉高几十倍，对应数千亿美金的市场空间。再往 Coworker 走，AI 开始进入全部白领工作。单个白领的 ARPU 可能低于程序员，但人数和 Task 总量远远更大，至少会打开数万亿美金的市场空间。

　⁠

对 Tag 来说，Slack 还只是第一站，Teams 版本也会很快发布，已经开放 waiting list。未来，Anthropic 还可以继续与 Zoom、电子邮件和项目管理工具做原生集成，让 Tag 出现在公司的每一条工作流里，并逐渐打通整个组织的记忆。

　⁠

可以想见的是，Tag 未来也可以和企业版的个人 Claude 账号打通。

　⁠

到那时，当员工在自己的 Claude Code 里工作时，对面的 Claude 不仅了解个人背景，还能记住全公司的 Context。那就不只是团队的共享同事，也是每个员工各自的数字分身。

2. Claude Tag 很可能有利于 Anthropic 进一步积累企业数据，扩大它在模型能力上的领先优势

最近我们聊到的不少数据专家[都提到](https://mp.weixin.qq.com/s?__biz=Mzg2OTY0MDk0NQ==&mid=2247526280&idx=1&sn=ba35ad25750dea3e621b78e36679f465&scene=21#wechat_redirect)，“Coding 之后，价值越来越集中在企业里真实的长尾数据，这是最值得继续爬坡的地方”，而 Claude Tag 是采集企业数据一个很好的载体。它的逻辑和 Cursor 类似，先把使用门槛压到最低 (@ 一下就能用)，再用换来的真实工作流筛出高质量数据。

　⁠

而且它产生的这些 Agent trajectories 格外优质——链路长、上下文完整、带有结果反馈，Anthropic 可以借此看到几千家公司是怎么真实干活的。

　⁠

当然，这里有一个限制，根据商业服务条款，Anthropic 不能直接使用客户的原始数据训练模型。但它仍然可以通过一些方式改进模型：

　⁠

(1) 隐私政策明确允许观察匿名聚合后的规律，了解哪些任务增长最快、哪些工作失败率最高，这些规律可以进一步用于设计新的评测集或合成数据；

　⁠

(2) 当员工主动提交 Rating 或反馈时，相关数据默认可以被用于训练 (但企业可以在后台关闭授权)；

　⁠

(3) Anthropic 推出了 Development Partner Program，让企业自愿共享 Claude Code 原始数据，并曾通过 Token 折扣提供激励。未来，这套机制也完全可以复制到 Claude Tag。

　⁠

同时，Claude Tag 这个形态还有一层防守价值：Agent 的中间过程全都发生在云端，外界通常只能看到最终结果，无法通过中转站拿到完整的 trajectories。开源模型的数据来源被掐断，Anthropic 的数据来源在加厚，开源和闭源的差距可能会因此拉大。

　⁠

## 3. Tag 类产品可能让大模型公司开始形成一些护城河

　⁠

这种护城河不一定来自模型记住了多少公司信息，因为记忆是可以被完整导出的，更关键的是，Claude Tag 会逐渐持有公司的一部分“运行状态”。

　⁠

比如在 Anthropic 内部，Boris 一个人现在就在同时运行数百个 Tag 任务，其中很多是长程任务，每个都有不同的权限、数据源、与其他任务的依赖关系，它们可能正在等某个客户回复，等一项实验达到发布阈值，或者记着某个尚未完结的 PR 和工单。

　⁠

如果后面要更换模型供应商，相当于替换一大批正在工作的员工，成本很高，也会担心迁移过程中漏掉某个承诺、或者新 agent 在关键场景下出现未知行为，不再像 ChatGPT/Claude Code 一样没有切换成本了。

　⁠

这也是为什么 Tag 这种形态对模型公司是更重要的。

　⁠

现在模型层的竞争越发胶着：单代模型的训练成本越来越高，商业生命周期却越来越短。Anthropic 和 OpenAI 很难真正拉开差距，开源模型可能也只有三个月左右的身位差。一代模型即使短暂领先，真正有效的变现窗口可能也只有两个月。

　⁠

在智能加速通缩的情况下，模型公司需要尽快做出更有黏性的产品，趁着有限的领先窗口，把智能优势固化成迁移成本。

　⁠

4. 但问题是，这道护城河最后会归谁？

AI coworker 的控制权目前有四类玩家都在争，各自握着不同的筹码：

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6a7bd45ce3d6f8391555511e/233fde6d-235e-423c-b828-44c4762a9de3.png)

　⁠　⁠

如果看大头会被谁吃掉，国内更可能是大厂的游戏，字节、腾讯、阿里各自本身都有完整的生态：又有协作软件，又都亲自下场做模型。

　⁠

从这个角度，最近飞书并入豆包，其实也非常合理。

　⁠

这半年，市场已经证实，对 AI 来说，B 端是比 C 端更重要的机会，豆包现在核心关注的战略指标也转向了 B 端的人数和收入。从终局看，飞书和豆包要做的事其实都是自动化所有白领工作。一个做大脑，一个做环境，合起来刚好互补。

　⁠

如果看海外，也是模型层的机会更大一些：

　⁠

一是成本差得太远。如果保守假设 Anthropic 的 API 毛利在 80%，第三方调用 Claude 付出的算力成本，就相当于 Anthropic 自己的 5 倍。

　⁠

二是海外 Context 更碎片化，Slack、Salesforce、Zoom、Notion 等各自拥有不同的 context，模型公司反而可以通过连接所有 SaaS，把所有 memory 打通，成为跨应用的认知层。

　⁠

而且只要 AI Coworker 这种产品形态足够重要，Anthropic 等模型公司未来就有可能对 API 业务降权，优先推广 Tag 这种自有产品。比如：

　⁠

•最新模型优先在 Claude Tag 等产品上开放使用 (安全就是一个充分理由，Tag 是 Anthropic 自己掌控 runtime，sandbox、身份、日志、工具等都是可控的，API 则管不到下游)；

　⁠

•给 Claude Tag 提供大量补贴，同时让 API 维持高价 (目前已经有了苗头：Enterprise 开通 Tag 会赠送 25000 美元额度，Team 版本赠送 2500 美元，但需要超过 10 个 seats)；

　⁠

•同款模型在 Claude Tag 中获得更高的 thinking budget。

　⁠

5. Anthropic ARR 有可能重新加速

Claude Tag 相当于在 Claude Code 的基础上，额外叠加了一套增长逻辑：

（1）Tag 可以加快 AI Diffusion 的速度。

相比 Claude Code，Tag 从产品形态到使用门槛都更贴近普通用户。它直接长在群聊里，一个人配置好，整个公司的人都可以使用。

　⁠

有不少网友提到，公司一开始可能只是把 claude tag 拉到了一个 channel 里，用顺手后就会渐渐把它拉到所有的 channel 里。在这个过程中，每个人，甚至包括外部合作方，都能观察公司里最会用 AI 的人是怎么使用 AI 的，好的 workflow 会自然扩散，甚至不再需要专门做 AI 培训。

　⁠

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6a7bd45ce3d6f8391555511e/c215fa2e-d2e0-47d3-952c-d37c5de3bd8f.png)

　⁠

（2）Agent 开始自发、持续地消耗 Token。

过去，Token 的消耗速度取决于人类的调用频率。但现在，Tag 开始接手越来越多的定期任务、长程任务，还会主动找活儿，也就是能主动、持续地燃烧 token。

（3）AI 开始从“工具预算”，走向“人力预算”。

对企业来说，Claude Code 更多还是一个提效工具，花多少钱看的是软件预算，但 Tag 开始能完整替代一些真人员工了。

　⁠

Anthropic 内部思考 Tag 定价时也是直接对标真人工资：如果未来一个岗位年薪 10 万，Tag 完成同样的工作只要小几万，企业就有充分的动力切换。

　⁠

三件事叠加在一起，Claude Tag 有可能会给 Anthropic 带来第二条增长曲线。

　⁠

而这可能也是整个 AI CapEx 周期接下来最关键的一道验证题。

　⁠

过去两个月，AI 硬件经历了史诗级回撤，走到现在，仅仅证明 “AI 基本面没问题”，已经不足以让腰斩的股价重回高点，市场还需要看到一个新的、足够清晰的跳变，才能重新对 AI 的商业化空间形成共识。

　⁠

这个跳变去年是 RL 和 post-training，今年上半年是 Coding，而下一个最可能的来源会是白领场景的进一步爆发。以 Tag 为代表的 Coworker 产品，或许是其中最重要的催化剂。

　⁠

如果从 Anthropic 内部的情绪和使用体验来看，他们认为 AI 产品已经明确到了这样一个新的范式迁移点。Mythos 的能力跳变叠加 Claude Tag 的形态跃迁，让 AI Coworker 从一个概念变成了真正可用的产品，这种变化不亚于去年底 Opus 4.5 + Claude Code Harness 的成熟。但目前在成本、权限等方面还有一些卡点，尚未达到大规模扩散的临界点。

　⁠

值得观察的是，未来某个节点，它会不会也像今年年初的 Claude Code 一样快速起飞。

排版：陈宇聪

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6a7bd45ce3d6f8391555511e/2ab021fc-e118-4e24-a72a-4a6ce70b9699.png)

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6a7bd45ce3d6f8391555511e/18fe451d-e7e3-487f-abc0-51457feaae71.png)

延伸阅读

[![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6a7bd45ce3d6f8391555511e/7baf7845-c346-4739-bb4a-9fa6ef1ee88f.png)](https://mp.weixin.qq.com/s?__biz=Mzg2OTY0MDk0NQ==&mid=2247526509&idx=1&sn=8c4393e87613584d53225c49a2127197&scene=21#wechat_redirect)

无法蒸馏的美国市场，谁在分食 Frontier Labs 百亿美金数据预算？

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6a7bd45ce3d6f8391555511e/44370113-87f2-42a3-ad09-774ae68f7975.png)

[![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6a7bd45ce3d6f8391555511e/bac04d23-a56e-4028-b429-2e45abba94a6.png)](https://mp.weixin.qq.com/s?__biz=Mzg2OTY0MDk0NQ==&mid=2247526473&idx=1&sn=a6a6583dc8a4aa01a99df4916730f911&scene=21#wechat_redirect)

Agent Infra 赛道更新，一年后为 Agent 设计的基建发展如何？

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6a7bd45ce3d6f8391555511e/85f07997-ff81-4036-bf1d-e5d5761ffc6c.png)

[![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6a7bd45ce3d6f8391555511e/f66fcbcd-e68a-4870-8cb7-ad84bb1c2e2e.png)](https://mp.weixin.qq.com/s?__biz=Mzg2OTY0MDk0NQ==&mid=2247526405&idx=1&sn=84a2cdaf54b8b4907abaf94468701271&scene=21#wechat_redirect)

当 Agent 成为 coworker：如何为新物种设计身份系统？

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6a7bd45ce3d6f8391555511e/fb087e0c-a79d-4b4a-8048-dd1018fa5657.png)

[![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6a7bd45ce3d6f8391555511e/74248a07-1e2f-4d73-b0db-266ebd69d076.png)](https://mp.weixin.qq.com/s?__biz=Mzg2OTY0MDk0NQ==&mid=2247526280&idx=1&sn=ba35ad25750dea3e621b78e36679f465&scene=21#wechat_redirect)

真实工作流，正在成为下一代训练数据

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6a7bd45ce3d6f8391555511e/e981727b-78b9-4ba6-80ca-3ef2c022f921.png)

[![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6a7bd45ce3d6f8391555511e/305d5fab-afc1-4ddb-a159-0a13c6b0709e.png)](https://mp.weixin.qq.com/s?__biz=Mzg2OTY0MDk0NQ==&mid=2247526163&idx=1&sn=de63238edb5a3c24c161ab60c6a3bbf0&scene=21#wechat_redirect)

当开源模型逼近闭源，谁会成为 AI 世界的路由器？

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6a7bd45ce3d6f8391555511e/2db743fa-edf9-421d-8ff8-fd3d74097fbd.png)
