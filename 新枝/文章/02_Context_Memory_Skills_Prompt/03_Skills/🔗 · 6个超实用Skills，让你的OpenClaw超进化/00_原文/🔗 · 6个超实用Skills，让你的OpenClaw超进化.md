---
作者:
  - "鹅厂技术派"
原文链接: https://mp.weixin.qq.com/s?__biz=MzA5NzU3MDczNA==&amp;mid=2247489800&amp;idx=1&amp;sn=29e3c6040d902c5da7c3ada24d832500&amp;chksm=91a04828152d911468500e7ae05ce99cb5bb4aeba63187ddb5a226f476a0d462a4f3de8b2d92&amp;mpshare=1&amp;scene=1&amp;srcid=0206tarpsQUhpQ6en9UGZ3es&amp;sharer_shareinfo=322c21afe163f56ffa3bf93f0483bbad&amp;sharer_shareinfo_first=322c21afe163f56ffa3bf93f0483bbad#rd
发布时间: ""
收藏时间: "2026-02-06"
关联日记: "[[2026-02-06]]"
tags:
  - 文章
---
鹅厂技术派

**你的OpenClaw是“龙虾小兵”还是“铁螯龙虾”，取决于你如何使用skills。**

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6985a6c3d2cbf46c2667ce66/2e3825d9-1787-4976-a985-d54893eb549d.jpeg)

在 AI 时代，很多人还停留在“调戏大模型”的阶段，问它一些泛泛而谈的问题。但如果你是一名需要面对海量课件、复杂论文和严苛进度表的学生或者职场人，**只会“聊天”的 AI 远远不够。**

OpenClaw 的强大之处在于其 Skills生态。如果把大模型比作“大脑”，Skills 就是它的手脚、眼睛和专业工具箱。

今天，我将以《世界电影史》这门课为例，带你通过 6个硬核 Skills，实现从“找资源”到“高分结课”的全流程自动化学习。

前置要求: 需要先购买一台轻量应用服务器 Lighthouse 部署好 OpenClaw。3分钟，即可在腾讯云 Lighthouse 上完成部署、可视化接入大模型以及 IM 软件。

> 接入教程：https://cloud.tencent.com/developer/article/2626151

接下来，所有 skills 都可直接把相应 skill 网页链接发给 OpenClaw，让其自行安装。

阶段一：资源掘金——让 AI 替你跑腿

**核心 Skill：**agent-browser【此Skill已经默认集成在腾讯云Lighthouse最新版OpenClaw镜像中，不需要额外下载】

面对《世界电影史》这种跨度上百年的课程，第一件事就是找教材。

- **核心技能描述：** agent-browser 是你的“网络手脚”。它不仅能进行多引擎搜索，还能**模拟真实浏览器行为**：点击链接、解析复杂的网页层级、绕过干扰信息，并直接执行文件下载任务。


- **实战场景：**“启动 agent-browser，帮我搜索《世界电影史》资源。找到后，直接下载到我的 workspace 目录下。”


阶段二：拒绝”大而化之“，精准结构知识点

**核心 Skill：diagram-generator | pptx**

面对老师几十兆的 PPT，直接问大模型往往只能得到简略的概述。我们需要“手术刀”级别的解析。

#### 1. 视觉化降维：diagram-generator

- **核心技能描述：**该技能能够将复杂的文本逻辑转化为**可视化图表**。它支持 Mermaid 等多种格式，擅长处理时间轴、流程图和思维导图。
- 实战操作：“根据教材生成一份‘世界电影史’的思维导图。”


![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6985a6c3d2cbf46c2667ce66/fd34a1b1-80e9-481b-ada6-654c14208da3.png)

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6985a6c3d2cbf46c2667ce66/6702c0fd-b028-4fe2-803c-3f3035e213ca.png)

#### 2. 课件深度解析：pptx

- **核心技能描述：**这是一个专门处理幻灯片的“手术刀”。它能将 .pptx **直****接转****换为**** Markdown ****格式**供 AI 深度阅读，甚至可以解构幻灯片的 XML 原始数据来提取备注、评论和隐藏的图文排版信息。
- 实战操作：“用 pptx 技能读取我上传的老师课件，总结出‘德国表现主义’在视觉呈现上的核心考点。” 


![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6985a6c3d2cbf46c2667ce66/b758ba56-f2ed-4905-bc80-1b857878a1d0.png)

我们甚至可以让它帮我们生成精简版PPT

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6985a6c3d2cbf46c2667ce66/33d69584-c2e1-4f0f-bd2b-689d81664263.png)

阶段三：从“学习计划”到“行动闭环”

**核心 Skill：ship-learn-next **

普通 AI 会给你一份“早起、读书、睡觉”的废话清单，但 ship-learn-next 关注的是**产出**。

- **核心技能描述：**这是一个**行动派规划工具**。它摒弃了传统的死记硬背计划，而是基于“Ship（交付）- Learn（学习）- Next（下一步）” 循环。它会将你的学习目标拆解为一个个具体的 “Rep（练习回合）”，强制你通过产出作品（如写一段影评、剪一段拉片视频）来驱动学习。
- 实战操作：“把这本教材的内容丢给 ship-learn-next，目标是让我三个月后能像专业影评人一样分析镜头语言。”


![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6985a6c3d2cbf46c2667ce66/a39700f1-f568-4d1e-9b09-79d9411f9845.png)

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6985a6c3d2cbf46c2667ce66/d9a743f7-9c71-4cd5-86e5-8def794d7e24.png)

阶段四：终结“遗忘曲线”，OpenClaw是你的超级脑干

**核心 Skill：personal-assistant**

- **核心技能描述：**对话式 AI 通常“记性不好”，关闭对话框就忘了你是谁。但 personal-assistant 赋予了它**持久记忆**。它像是一个 24 小时待命的管家，记录你的目标、偏好和每一个 Skills 的执行进度。 它跨越了对话 session 的限制，让 AI 真正“认识”你的学习习惯。
- 实战指令：“查看我的学习进度，对比 ship-learn-next 给我的计划。如果我落后了，请帮我重新安排这周的时间表，并在明天早上提醒我完成 Rep 2。”


![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6985a6c3d2cbf46c2667ce66/59122579-ac50-4559-9519-fee1755be44c.jpeg)

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6985a6c3d2cbf46c2667ce66/5798fbb4-25cd-4a76-ba37-1e067186deb4.png)

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6985a6c3d2cbf46c2667ce66/65f769f1-2d07-4a68-ade6-4696e15133c6.png)

阶段五：终结润色，赋予文字“人类灵魂”

**核心 Skill：Humanizer-zh**

到了论文提交阶段，虽然 AI 能帮你整理逻辑，但其生成的语言往往生硬。

- **核心技能描述：**论文写完后，如果读起来像说明书，那大概率是 AI 的痕迹太重。这个Skill专门针对中文语境开发，通过重组长短句、注入情感逻辑，对文字进行细颗粒度的重构，让文本彻底告别“翻译腔”和“机器味”。
- 实战策略：将生成的电影史论文初稿投喂给它：“调用 Humanizer-zh 润色这篇论文，让它读起来像是一个资深电影系学生的独立观察报告，而不是机器生成的陈述句组合。”


![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6985a6c3d2cbf46c2667ce66/67d8cd1c-8f7f-498b-b55f-8685922c0742.png)

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/6985a6c3d2cbf46c2667ce66/d0b0dd27-c63e-482d-880f-fecf9cc91e6b.png)

**结语：从“大号对话框”到你的私人“贾维斯”**

回想起 OpenClaw 刚问世时，不少人的第一反应是：“这不就是一个大号的 ChatGPT 吗？换个壳子聊天而已。”

但随着我们对**Skills 生态**的深度发掘，这种偏见正在烟消云散。通过《世界电影史》的这个实战案例，你会发现：当 AI 拥有了执行力（agent-browser）、结构化思维（diagram-generator）、产出导向（ship-learn-next）、深度解析力（pptx）以及持久记忆（personal-assistant）时，它就不再是一个只会“接话茬”的复读机，而是一个真正能下地干活的**数字生命**。

今天的“学习助手”玩法，仅仅是 OpenClaw 进化之路上的一个微小截面。

我们正在经历一场从“对话”到“协作”的范式转移。从自动化的信息掘金，到复杂的决策支持，越来越多的硬核玩法证明了：**AI 不应只是被动回答问题，而应主动解决问题。**

我们坚信，那个“人手一个贾维斯”的时代不再是科幻电影里的特效，它正潜伏在这些不断涌现的 Skills 插件中，潜伏在你每一次对流程的优化里。现在的 OpenClaw，就是那个正在不断进化的、属于你的钢铁侠管家雏形。

腾讯云热点技术有奖征文|OpenClaw云端创意实践赛火热进行中！

- 接进聊天工具？


- 变成情绪助理/工作分身？
- 搞个离谱但好玩的自动化？


只要是基于腾讯云Lighthouse部署OpenClaw的创意场景，都能投稿！

✅马歇尔黑金音响、庆余年联名键盘、王者荣耀耳机......超丰厚奖池等你来赢！提交符合要求的参赛文章，即可获得保底奖品腾讯定制萌鹅便利贴2件套。

✅2026.1.26OpenClaw发布后，所有基于腾讯云Lighthouse部署OpenClaw的场景玩法类文章，均可添加本次比赛指定标签参与投稿。

详情速戳：https://cloud.tencent.com/developer/article/2627198

