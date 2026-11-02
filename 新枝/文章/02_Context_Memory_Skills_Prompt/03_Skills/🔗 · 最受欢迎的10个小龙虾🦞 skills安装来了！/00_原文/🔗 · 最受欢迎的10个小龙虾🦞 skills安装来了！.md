---
作者:
  - "Datawhale"
原文链接: https://mp.weixin.qq.com/s?__biz=MzIyNjM2MzQyNg==&amp;mid=2247720076&amp;idx=1&amp;sn=95286afc7806fc3434df4c8b29d528d1&amp;chksm=e9f0dc352b6377c7d62897929b447c68b7c94cf32d3d5368f2e94b502513fcc8f76d4ce96e7c&amp;mpshare=1&amp;scene=1&amp;srcid=0303BEbHblciHq2EuOGlLZzG&amp;sharer_shareinfo=8e2800cb3646eb10310390bea24a6d24&amp;sharer_shareinfo_first=8e2800cb3646eb10310390bea24a6d24#rd
发布时间: ""
收藏时间: "2026-03-03"
关联日记: "[[2026-03-03]]"
tags:
  - 文章
---
## Datawhale干货 作者：王熠明、刘伟鸿，Datawhale成员

最近科技圈的“小龙虾”特别火——也就是 OpenClaw。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/69a61c55f0c88e76c8ec7d78/a511d5fb-960f-4617-bfca-e641f43d55eb.webp)

OpenClaw 的核心优势是“技能包（Skills）”系统——它就像一个万能工具箱，AI 遇到什么任务就掏什么工具，专具专用，高效不卡顿。

目前社区里已经有几百个这样的“工具”了，直接挑花了眼。上周，我们专门为新手筛选出了 [**10 个最建议安装的 Skills**](https://mp.weixin.qq.com/s?__biz=MzIyNjM2MzQyNg==&mid=2247719882&idx=1&sn=bb0e4da8922fc2418172041a84375f86&scene=21#wechat_redirect)**。****今天我们来点****进阶干货。**

**通过X上大家讨论和推荐的实用/高频技能（基于社区反馈、安装量、使用场景，排除明显恶意类），我整理出了下面这些被多次提到“很推荐”“必装”“日常用”的，基本覆盖核心需求：**

**1. tavily-search**

联网搜索技能（AI优化版），让Agent能实时查最新资讯、数据，避免“闭眼编”。几乎所有人都说“没这个跟瞎子一样”。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/69a61c55f0c88e76c8ec7d78/e8bc620f-8fec-4c09-9eb5-2653982d34cd.png)

安装：npx clawhub@latest install tavily-search

**2. find-skills**

让Agent自己去ClawHub搜并安装需要的技能，解决“不知道用哪个工具”的痛点。 

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/69a61c55f0c88e76c8ec7d78/06398e1b-2b42-4874-9c5a-9b83c97df402.png)

安装：npx clawhub@latest install find-skills

**3. proactive-agent**

（或旧版proactive-agent-1-2-4） 给Agent加“主动性”和自我迭代能力，能记住历史、优化行为、减少重复问。长期用很香。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/69a61c55f0c88e76c8ec7d78/49842b77-6243-4258-94de-02f268c94177.png)

安装：clawhub install proactive-agent

**4. github**

GitHub集成，能自动管repo、issue、PR、code search。开发者必备。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/69a61c55f0c88e76c8ec7d78/155384de-7992-4552-a6ce-91163d83e843.png)

安装：npx clawhub@latest install github

**5. gog**

Google Workspace全家桶（Gmail、日历、Drive、Docs），办公自动化神器。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/69a61c55f0c88e76c8ec7d78/6a466957-3db6-4c02-8568-43f0cc663587.png)

安装：npx clawhub@latest install gog

**6. skill-vetter** / **clawsec**

安装前扫描技能安全，防恶意代码。**安全第一步**，很多人后悔没先装这个。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/69a61c55f0c88e76c8ec7d78/2711b88e-7854-432c-8ed7-42b1f99534dc.png)

安装：npx clawhub@latest install skill-vetter 或类似安全扫描类

**7. automation-workflows**

工作流编排，把多个技能串起来干复杂事（自动邮件+报告+数据同步等）。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/69a61c55f0c88e76c8ec7d78/584a0874-7984-4b37-a86e-b5a8e42c25f5.png)

安装：npx clawhub@latest install automation-workflows

**8. bird**

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/69a61c55f0c88e76c8ec7d78/0d847175-9a91-4a24-83d3-5a3a64ae4e6e.png)

X/Twitter集成，能发帖、搜趋势、管理账号（但小心伪装恶意版）。（社区提到，但慎用高赞的“Twitter”相关）

**9. self-improving-agent**

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/69a61c55f0c88e76c8ec7d78/838984aa-ea3e-4ac4-a94c-9ab50a14cca3.png)

加记忆+自我优化，长期交互越用越聪明。 

安装：npx clawhub@latest install self-improving-agent

**10. feishu-doc**（针对国内用户） 飞书文档/云盘集成，企业/团队协作常用。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/69a61c55f0c88e76c8ec7d78/487527b4-5377-4137-93d7-52276a4025be.png)

安装：npx clawhub@latest install feishu-doc

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/69a61c55f0c88e76c8ec7d78/92e505b0-3559-4f86-acb4-0dd4d96e2804.webp)

**一起“点赞”三连↓ **

