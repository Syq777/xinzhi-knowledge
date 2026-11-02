---
作者:
  - "Datawhale"
原文链接: https://mp.weixin.qq.com/s?__biz=MzIyNjM2MzQyNg==&amp;mid=2247722227&amp;idx=1&amp;sn=91cdeb9ed199ea27bf816d8f58822044&amp;chksm=e93340dec6f7b99e09332e9f47ccf53fac4b2706f456679e2c8451e5318c3ac202090509b446&amp;mpshare=1&amp;scene=1&amp;srcid=0423kuPPa14mf1kRTRT3y21j&amp;sharer_shareinfo=e71eb130422b5d1c688964e36e043639&amp;sharer_shareinfo_first=e71eb130422b5d1c688964e36e043639#rd
发布时间: ""
收藏时间: "2026-04-23"
关联日记: "[[2026-04-23]]"
tags:
  - 文章
---
## Datawhale开源 作者：Datawhale Hello-GA项目团队

> 多年以后，当你的 Agent 只用两千个 token 就完成了别人两万个 token 才能启动的任务，你会回想起第一次点开这个教程部署 GA 的那个午后

一、开源初心

短短几个月，Hermes、Claude Code、OpenClaw 这些名字你大概率都不陌生。但真用下来，几个毛病躲不掉：

一句 "Hello" 发过去，账单先跳出来，系统提示词吃掉几万 token；装了二十个Skill，越装越慢，连最基本的事都开始卡；上周刚教会的操作，这周又忘了，每次都像第一次见面。

Generic Agent（GA）把这个问题解得很漂亮，只用一条原则：**上下文信息密度最大化**。不追求上下文有多长，只追求每一个 token 都在为当前决策服务。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/69ea364e8800f73e4a6f11fa/f6da6038-d00f-4f31-8066-94626233d83f.png)

这个项目最近特别火：半个月涨了 5k star，登上了 GitHub trending 第一。但中文社区几乎没有文档，新手想上手只能啃源码、翻 Issue、泡社区，大量时间花在"搞清楚怎么用"上，而不是真正用它解决问题。

好工具值得一份好教程。于是我们把这段时间的使用经验梳理了一遍，整理出从安装到原理的完整最佳实践，帮每一位想上手的人跳过踩坑阶段！

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/69ea364e8800f73e4a6f11fa/e14abb16-cde9-4593-88f8-5593e3ac4011.png)

开源地址：https://datawhalechina.github.io/hello-generic-agent/

二、Generic Agent：比 Hermes 省 10 倍 Token

先说 Generic Agent 是什么。

它是一个极简、可自我进化的自主 Agent 框架，核心代码大约 3K 行，9 个原子工具，Agent Loop 只有 100 行左右。就这么点东西，能赋予任意一个大模型对本地计算机的系统级控制——浏览器、终端、文件系统、键鼠输入、屏幕视觉，连移动设备都能接。

听起来不太可能，但它真能做到。秘密就在开源初心里提到的那条原则：上下文信息密度最大化。

效果有多夸张？同样装了 20 个技能，对一个最简单的 "Hello" 请求：

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/69ea364e8800f73e4a6f11fa/43401186-31d7-498a-b858-b452a2a1bdc9.png)

别人的起步价是 1 万 7，GA 只要 2 千。

差 10 倍，是整个设计哲学层面的 10 倍，不是只靠优化出来的。别人还在给 Agent 加瑞士军刀，GA 一直在做减法，把每个 token 的价值榨到最高。

三、教程全览：理解背后的 Harness Engineering

教程分为三大部分，像一座阶梯，带你从会用到懂原理再到能实战。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/69ea364e8800f73e4a6f11fa/d5d8e1ff-25e2-4060-80ee-404219116cbd.png)

Part 1 · 应用指南：零门槛上手

6 章内容，覆盖从安装到精通的完整路径：

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/69ea364e8800f73e4a6f11fa/b3e7e443-9f31-431e-bc10-8401eb8c948b.png)

不需要有任何编程基础，跟着教程一步步走，就能拥有一个能帮你操作浏览器、自动执行任务、还能接入微信和飞书的专属 AI 助手。

Part 2 · 原理篇：拆解背后的 Harness 哲学

7 章深度解析，带你理解Generic Agent为什么能用 1/10 的资源做到同样甚至更好的效果。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/69ea364e8800f73e4a6f11fa/b10fe265-a9b3-4932-88e4-912f723114ae.png)

这部分是整个教程的重点。Part 1 是教你用，Part 2 是告诉你它为什么能这么用。顺着这七章读下去，你会慢慢看懂一件事——**怎么给 LLM 搭一副刚刚好的骨架，让它既能干事，又不被自己的工具和上下文拖垮**。这件事有个名字，叫 Harness Engineering。

**三大核心看点**

**1. 9 个工具打天下。**Claude Code 有 53 个工具，80% 的调用集中在 3 个上，剩下 50 个每轮白白吃上下文预算。GA 只保留 9 个原子工具，覆盖文件操作、代码执行、网页交互、记忆管理、人机协作，任务成功率 100%。

**2. 三阶进化，Token 省 89.6%。**同一个任务执行 9 轮，全程无人干预：

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/69ea364e8800f73e4a6f11fa/0821d89d-438f-4cda-a791-d68a47826bc1.png)

3. 3300 行代码涌现出一切。没有子 Agent 管理器、事件总线、调度守护进程，但子 Agent 分发、看门狗监控、定时任务调度全都能做。Agent Loop 核心代码只有 92 行！

Part 3 · 案例篇（即将上线 🚧）

手把手教你用 GA 办公、娱乐、挖宝——把前两部分学到的知识融会贯通。

写在最后：好的工具值得一份好的教程

2026 年 4 月，Datawhale 正式开源「Hello Generic Agent」。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/69ea364e8800f73e4a6f11fa/96add892-1641-4e65-94f2-cec9373352a6.png)

📖 在线阅读：

https://datawhalechina.github.io/hello-generic-agent/

⭐ GitHub：

https://github.com/datawhalechina/hello-generic-agent

🔗 Generic Agent 主仓库：

https://github.com/lsdefine/GenericAgent

真正激励我们的，从来不是 GA 本身能做什么。

而是当你第一次看到自己的 Agent，用 2000 个 token 完成了别人 20000 个 token 才能启动的任务时，那种「原来还能这样」的惊喜。

好的工具值得一份好的教程。如果这个项目对你有帮助，请给我们一个 ⭐ Star。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/69ea364e8800f73e4a6f11fa/7fd7400e-103e-4a68-85ae-47da0027e34b.webp)

开源贡献，**点赞**在看↓

