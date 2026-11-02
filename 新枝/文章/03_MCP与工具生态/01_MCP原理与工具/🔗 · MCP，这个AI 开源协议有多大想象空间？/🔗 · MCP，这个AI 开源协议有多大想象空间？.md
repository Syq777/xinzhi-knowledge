---
作者:
  - "腾讯技术工程"
原文链接: https://mp.weixin.qq.com/s?__biz=MjM5ODYwMjI2MA==&amp;mid=2649792633&amp;idx=1&amp;sn=4b89473b82ccce3fff6b5a3afa0a729a&amp;chksm=bfe62f32f5e316b9865491c672bf754efb785c7e0e6dc1c918659309f844e805f83d7b83c94a&amp;mpshare=1&amp;scene=1&amp;srcid=0409Bk5JPaXjSDMROLH1m57D&amp;sharer_shareinfo=0670b9d4ff8b187f759dde4631d61119&amp;sharer_shareinfo_first=0670b9d4ff8b187f759dde4631d61119#rd
发布时间: ""
收藏时间: "2025-04-09"
关联日记: "[[2025-04-09]]"
tags:
  - 文章
---
![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67f64c880077a829a7336d43/31666441-2925-4b97-92e4-be04e37e4b2c.gif)

### 话题背景

在AI技术迅猛发展的今天，模型的开源与协作方式正以前所未有的速度演化。

随着模型体量的激增、功能模块的碎片化，以及对复用与定制化需求的增加，传统的模型发布与管理模式已经难以满足行业对效率与创新的双重追求。

正是在这样的背景下

，MCP（Model Collaboration Protocol，模型协作协议）作为一个全新的开源协议框架被提出，它试图重塑模型开发、集成与协作的方式。

**那么，MCP究竟能针对传统软件利用到何种程度，MCP的开源开发热潮，预计会在什么时候崛起，哪些具体应用中又能最快实现对MCP的应用?**

今天就让我们一起来聊聊MCP。

### 鹅厂工程师的看法

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67f64c880077a829a7336d43/f2856755-f55d-405f-8712-8e292b6a1fee.jpeg)

**@mikael-行业咨询**
▼

从我的理解，MCP让只能人机交互的大模型转化为了能够快速对接各类业务系统的生产力大脑。
传统的做法其实是xxx+AI，也就是各个业务系统融入一些AI能力；

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67f64c880077a829a7336d43/8dfc7357-decd-4893-9e99-0bccb62f32c1.png)

有了MCP，是可以构建AI+xxx，把AI作为新业务的中心，通过将业务系统的api封装后提供MCP接入能力，让各类新业务按需调用，这样就是新的重构了。
毕竟已经有一堆业务系统了，全部重做其实代价很高。但是新建一两个AI为中心驱动的系统，用MCP方式快速接入原有系统的业务能力，这个比较实际。尤其是to b、to g场景。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67f64c880077a829a7336d43/5da79ee2-ea45-4b9d-a0fa-6550d2c3322e.jpeg)

**@ivan-产品策划**
▼

作为提问者，我也说下我个人的观点:
1.针对传统软件，我个人认为MCP能做到 直接干掉GUI，变成更高效的生产工具的核心要素，后续依赖 大模型蒸馏+微调+知识库，结合MCP对传统软件的调用大模型就可以直接应用到生产各流程中来。这里好处是:
a.舍弃低效的GUI操作路径
b.软件使用者/开发者 会因为开发成本的降低，反复迭代和优化MCP 逐步提供更好的价值。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67f64c880077a829a7336d43/cd58390c-8f2e-45f1-9d32-d90e25a06d46.png)

2.MCP的开源热潮，个人觉得今年内就能看到，甚至 在25年H1就能席卷起来(我说的开源热潮,实际上是公司的开源热潮,非行业的)3.毫无质疑是开发岗位的应用中会率先应用，但是个人认为，引起巨大震动的，应该是美术资产生产/管理方向，甚至是产品通道工具(office套件等) 会更明显4.在 资产生产软件里面(美术资产管理，3d建模，游戏关卡设计，游戏引擎)领域，可能是最迫切有效的，通过引入大模型优化重复的脚本操作，解决复杂资产管理的问题。有点类似在 文件管理中 引入 cursor 这类编辑器，协助建设索引文档，批量编辑。届时 必然会对整体效率带来巨大提升(欢迎真正技术管线的同学过来指导经验，外行对这块workflow理解浅薄，只是从底层原理上反推)

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67f64c880077a829a7336d43/8f791ff2-1fd1-4da0-b25e-74b28374e001.jpeg)

**@jinjing-客户端开发**
▼

现在很多事情需要我们通过 APP 自己去操作 UI，比如出去玩要自己通过不同的 APP 找攻略、订机票、记花销等等，将来可能很多事情都可以通过 AI 结合 MCP 串起来，商业公司也有一种可能会演化为纯粹提供信息和数据服务的形态来提供价值，不再依赖 APP 本身了。
与 AI 对话的交互可能是将来统一甚至唯一的入口，出门有手表之类的穿戴设备就可以了，不再强依赖一个像手机一样移动的屏幕。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67f64c880077a829a7336d43/fdceb8d2-9661-4dc5-9b95-a2af224b7f83.png)

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67f64c880077a829a7336d43/4eef64cc-7264-4718-ad7f-46ae7df6d6a3.jpeg)

**xianga-应用开发****▼**

AI + MCP + everything（app、service、db、blockchain ...） 可以真正实现去中心化世界

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67f64c880077a829a7336d43/c4ff2bd8-7bfa-4bba-be3e-ec6206cfd06c.png)

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67f64c880077a829a7336d43/ac9f32ad-c224-4dd7-8065-2c46ff4c3d8e.jpeg)

**chuan-应用开发****▼**

我对 MCP 了解得很少，但是我看了 ivan 和大家的回答，反而产生了相反的思路：
在友商中台干过的人应该都很熟悉中台的设计目标等于平台能力-商业产品的聚合。
中台最后积重难返导致拆中台其实是组织管理-系统架构的复杂度超过了当时的架构者/管理者能控制的复杂度。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67f64c880077a829a7336d43/011d4706-125f-40a4-ad91-d0a56bb349d6.png)

如果能够用 AI 作为中心能力而不是周边的辅助能力，设计一个生产力大脑，我们会出现一种全新的中台。一种无需处理accidental complexity 的核心系统。因为中心是被 AI 接管的，我们不再需要关注架构清晰这个永恒的问题了。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67f64c880077a829a7336d43/99be2762-816d-473e-9bfa-e725679148c0.jpeg)

**ylva-内容运营****▼**

MCP给传统软件大模型交互拓展，检查语法错误、图像生成美化这些都可以，成本就降低了

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67f64c880077a829a7336d43/dd8a4794-8b04-4330-9bbd-8a5803b60700.jpeg)

**alan-前端开发****▼**

1. 所有提供HTTP API或者其它协议接口的都会再来一遍MCP版接口。
2. 网上举例为USB很巧当。但这个的底层是AI能力要突出。如果本身AI调用不合适，照样拉垮。
3. MCP 远程Server规范今年会推出。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67f64c880077a829a7336d43/f565848e-d164-4632-8d3a-e63706bf18f1.png)

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67f64c880077a829a7336d43/443b079d-107a-461c-9724-adc3840fa257.jpeg)

**jieling-后台开发****▼**

个人认为，下一次MCP的开源开发热潮，会跟随类似manus类似产品的发布热潮，两者相辅相成。根据历史各个公司产品发布时间推测，估计会在6,7月吧

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67f64c880077a829a7336d43/6f46cdb4-6b7b-4bc4-840d-4b703766e7a7.jpeg)

**amer-行业咨询****▼**

软件范式其实已经发生了根本性的改变，saas软件的颠覆是最大的。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67f64c880077a829a7336d43/9e8cb1d6-eb5d-488c-b0eb-a9b4a27b7737.png)

**🎁互动福利🎁****在评论区分享你对MCP的看法****随机抽取5位同学送出30Q币**

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67f64c880077a829a7336d43/a8a46ac8-09ac-4e26-9c3d-754cf836c561.png)

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67f64c880077a829a7336d43/0757c4d9-73f8-48c9-9019-a9b957218325.gif)

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67f64c880077a829a7336d43/0bf40276-1fb1-48b7-81e8-8adf248cc604.webp)

