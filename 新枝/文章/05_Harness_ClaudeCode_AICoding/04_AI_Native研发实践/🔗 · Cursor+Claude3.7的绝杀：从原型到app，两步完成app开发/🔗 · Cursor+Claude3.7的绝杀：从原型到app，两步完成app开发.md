---
作者:
  - "花叔"
原文链接: https://mp.weixin.qq.com/s?__biz=Mzg2OTA1OTAxNA==&amp;mid=2247484951&amp;idx=1&amp;sn=20647797476343561319366f8bb7c325&amp;chksm=cf8ee0b17f614e84d2f3183e8c953feb87552039aef7ecb6196016c4669d373b060538ffbd44&amp;mpshare=1&amp;scene=1&amp;srcid=0323CBIbc0qnplsJRQojubDs&amp;sharer_shareinfo=81657635da1297bad9ab4bc95e4c64d5&amp;sharer_shareinfo_first=81657635da1297bad9ab4bc95e4c64d5#rd
发布时间: ""
收藏时间: "2025-03-23"
关联日记: "[[2025-03-23]]"
tags:
  - 文章
---
最近在X上看到了一些人在用Claude 3.7 Sonnet生成 app原型图的尝试，受到启发，发现这么先生成不同界面的原型图再让Cursor基于原型图开发app会是很好的尝试。尤其是，你也可以不两步直接生成，而是在过程中更可视化地思考你要生产的原型，这对于非专业的产品经理来说，会是好得多的方式。

我今天做了些尝试后，效果让我感到惊艳。这里给大家介绍下具体的操作方式。

## 步骤一：新开项目文件生成HTML原型图

可以参考我的提示词，修改其中的要求。

```
我想开发一个ai自动记账app，现在需要输出原型图，请通过以下方式帮我完成app所有原型图片的设计。
1、思考用户需要ai记账app实现哪些功能
2、作为产品经理规划这些界面
3、作为设计师思考这些原型界面的设计
4、使用html在一个界面上生成所有的原型界面，可以使用FontAwesome等开源图标库，让原型显得更精美和接近真实
我希望这些界面是需要能直接拿去进行开发的
```

```
这里有三个关键点：
```

1、选择Claude 3.7 Sonnet模型，不建议thinking

2、选择composer normal模式，或者说0.46版本中editor模式，不要选择agent，不要选择agent！

3、由于一次性生成的html代码文件会太长，中间可能会截断或创建失败，你可以点击生成失败的代码文件，cursor会提醒你是否创建文件，然后把已经生成的一部分代码复制到新创建的文件中；接着，@对应代码文件，要求cursor继续补全文件。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67df60bef4a5e20709eb619a/723d9a5a-3bbf-4dac-bcd6-39cd78fee079.png)

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67df60bef4a5e20709eb619a/6e431974-6257-4906-a15d-be19882f52c0.png)

然后，打开补全完成的html，你就获得了类似下面的整个app所有主要界面的原型图👇

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67df60bef4a5e20709eb619a/744cd2fa-f18b-4725-8e5f-aa34018b9654.png)

步骤二：让Cursor根据原型图创建app

用Xcode创建一个新项目，然后在Cursor中打开项目的根目录（如果从来没开发过iOS项目，不知道这一步如何操作的，可以先去看我之前的iOS app开发视频）

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67df60bef4a5e20709eb619a/f6d6d40d-5b95-4c7e-a845-b504efc2c718.png)

在Cursor打开的iOS app开发项目根目录中发送上面得到的app原型图，然后要求：

```
请根据我提供的原型图完成这个app的设计
```

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67df60bef4a5e20709eb619a/1bd07a6e-d538-4d03-9ca7-96737d9bb41e.png)

```
这一步依然有三个关键点：
```

1、选择Claude 3.7 Sonnet模型，thinking或非thinking都可以试试

2、选择agent模式，必须选择agent！

3、这个过程中不断accept生成的代码文件就好了，创建完成后如果在Xcode调试出现bug，可以把xcode的报错提示复制回cursor，修bug场景建议使用thinking模型。

我这次测试过程中，两个步骤分别出现了一次cursor生成出错和一次Xcode报错，其他都一切顺利，得到的结果远超我的预期了。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67df60bef4a5e20709eb619a/decd31a1-954b-49ff-8e43-d08fc2f6e92b.png)

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67df60bef4a5e20709eb619a/c71f623e-50f1-4178-bf17-cd5c15db65b7.png)

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67df60bef4a5e20709eb619a/c682013b-838f-409a-bf0a-5ba253e1b342.png)

甚至，这个app大部分功能都已经是可以正常操作，逻辑正常的。

这个两步生成app的策略其实都离不开Claude 3.7的能力，核心用到了两点：

1、Claude 3.7生成原型的能力惊人

2、Cursor agent模式+Claude 3.7基于原型图多步骤完成任务能力惊人

下面是其他一些原型图

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67df60bef4a5e20709eb619a/88b8f8a0-aec2-4bf8-905e-885d85d00b8b.png)

本文首发于我的知识星球「AI编程：从入门到精通」：https://t.zsxq.com/BFTPI ，如果你对此感兴趣，可以「阅读原文」查看更多信息

