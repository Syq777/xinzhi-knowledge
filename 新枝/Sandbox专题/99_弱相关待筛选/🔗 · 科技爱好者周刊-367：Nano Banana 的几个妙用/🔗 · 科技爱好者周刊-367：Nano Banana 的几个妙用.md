---
作者:
  - "阮一峰的网络日志"
原文链接: https://mp.weixin.qq.com/s?__biz=MzI4NjAxNjY4Nw==&amp;mid=2650241965&amp;idx=1&amp;sn=40b6f3ac5aea46831c9dfff9e7cc5815&amp;chksm=f2e2b711fce41a69547c7d8d14b8cf2070ea74defec1e9b5fd87959e5e70ea3890e90c7bfe8a&amp;mpshare=1&amp;scene=1&amp;srcid=09269YMX86TnWHHNLGz3qfif&amp;sharer_shareinfo=2dfa8143867c4185c974ea03bf02ea18&amp;sharer_shareinfo_first=2dfa8143867c4185c974ea03bf02ea18#rd
发布时间: ""
收藏时间: "2025-09-26"
关联日记: "[[2025-09-26]]"
tags:
  - 文章
---
这里记录每周值得分享的科技内容，周五发布。（**[通知] 下周十一假期，周刊休息。**）

本杂志开源[1]，欢迎投稿[2]。另有《谁在招人》[3]服务，发布程序员招聘信息。合作请邮件联系[4]（yifeng.ruan@gmail.com[5]）。

## 封面图

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68d6144a9a76d4094fa0463e/ade2f1e3-c753-4d16-9146-fe568eef9b55.jpeg)

香港举办“维港海上大巡游”，会在维多利亚港岸边，展示四个大型充气玩偶雕塑。这是正在运送充气玩偶。（via[6]）

## Nano Banana 的几个妙用

上个月，谷歌发布了图像模型 Gemini 2.5 Flash Image（项目名 Nano Banana[7]）。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68d6144a9a76d4094fa0463e/94f1a6fc-dbde-4a24-aae9-499952ea2caf.jpeg)

谷歌称它是目前“**最先进的图像生成和编辑模型**”。

我试用后，感觉确实很强，而且免费使用，打开官网[8]（下图）就能用。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68d6144a9a76d4094fa0463e/9b5470b8-2b82-4644-aae1-9a376d33857a.jpeg)

（备注：如果你访问不了官网，周刊讨论区也有接入官方 API 的第三方网站[9]，不过大部分要收费。）

对于这个模型，网友发现了各种神奇的用法，有人甚至收集成了一个 Awesome 仓库[10]。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68d6144a9a76d4094fa0463e/0a5b4761-701b-477d-ac09-95f8c9e2fb4a.jpeg)

我从这个仓库里面，挑了几个很实用的例子，分享给大家。需要说明的是，我想其他图像模型也能做这些事，大家可以试试。

### （1）人像处理

图像模型的最常见任务，一定是人像处理。我们先上传一张生活照片。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68d6144a9a76d4094fa0463e/b819f673-daee-4493-9134-792b5c166f15.jpeg)

然后，让模型将其转成证件照，提示词如下。

> 请为照片里面的人物生成1寸证件照，要求白底，职业正装，睁眼微笑。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68d6144a9a76d4094fa0463e/e733a9e9-39dd-4771-a04d-e8fdd534b7bb.jpeg)

这个效果有点惊人啊。它意味着，人物的表情、发型、妆容、服饰、姿势都是可以改变的。

下面就是改变人物表情，让其侧脸对着镜头微笑。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68d6144a9a76d4094fa0463e/c36e27d7-593b-4fd8-a471-36cb94bbdcf2.jpeg)

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68d6144a9a76d4094fa0463e/208aa051-557b-44bd-b0e8-db8074d76ed5.jpeg)

改变人物的姿势，“将下面第二张图片的人物，改成第一张图片的姿势。”

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68d6144a9a76d4094fa0463e/e64cd89d-2f2d-4b0c-a311-1abffd18ff9b.jpeg)

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68d6144a9a76d4094fa0463e/1838e071-a64d-4f2f-9421-15391e7f9652.jpeg)

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68d6144a9a76d4094fa0463e/30e50505-6691-4a19-a9f8-e3f83e300b03.jpeg)

照相馆以后危险了，肖像照、旅游照、集体照都可以交给 AI 了。

### （2）建筑处理

图像模型的另一个用途是家居装潢，要看家装效果图就让 AI 生成，更改装潢配色和家具，都是小 case。

下面是一个难度更高的例子，上传一张户型图，让它变成 3D 模型渲染图。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68d6144a9a76d4094fa0463e/af152a58-182d-442f-af39-72c68393e783.jpeg)

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68d6144a9a76d4094fa0463e/2c191f26-43ff-4907-8741-b808edd90beb.jpeg)

从照片提取建筑模型，也挺神奇。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68d6144a9a76d4094fa0463e/374ecd2f-4ab7-4a65-86e4-53b4f71c1507.jpeg)

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68d6144a9a76d4094fa0463e/19a3f34b-7487-4afa-80f7-fdf31ecab62f.jpeg)

### （3）包装处理

下面，让模型更改物品的包装，“将图二的漫画形象，贴到图一的包装盒，生成一张专业的产品照”。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68d6144a9a76d4094fa0463e/c2c3fd8d-ac8b-49a3-b52d-3dd9d5b36e3d.jpeg)

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68d6144a9a76d4094fa0463e/96fdacb7-71a0-46b3-9d0f-8292412ad500.jpeg)

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68d6144a9a76d4094fa0463e/ff2178d3-c235-4185-8330-3e6e8af6caf7.jpeg)

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68d6144a9a76d4094fa0463e/bb045f23-faf7-4a3f-b681-a0d415a42567.jpeg)

书籍的封面、软件的包装盒，也可以同样生成。

### （4）地图处理

图像模型的另一个大市场是地图应用（地理信息），只不过还没想到可以收费的玩法。下面就是一个创新的用例。

上传一张地图，上面用箭头标注你选定的地点，让模型“生成沿着红色箭头看到的场景。”

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68d6144a9a76d4094fa0463e/840d452b-c043-4955-b39c-a0a2b64d16f3.jpeg)

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68d6144a9a76d4094fa0463e/4418212b-72de-4cf9-89bd-dd272b70f6e8.jpeg)

它甚至可以从地形等高线图，生成红色箭头处的实景图。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68d6144a9a76d4094fa0463e/eb849188-643a-4fd1-9efe-3d376465fd0c.jpeg)

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68d6144a9a76d4094fa0463e/288ea982-5bd4-4328-bc00-6921e1ff23cb.jpeg)

## 科技动态

1、超音速厨师刀[11]

一家美国公司推出了超音速厨师刀。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68d6144a9a76d4094fa0463e/a9169021-14e2-408f-ab1e-19170e4b481e.jpeg)

它的刀柄上有一个按钮，按下后，刀锋就会进入超声波模式。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68d6144a9a76d4094fa0463e/c0148e15-939f-4447-a2a5-2a738d0b0eb5.jpeg)

根据介绍，开启超声波后，刀刃每秒振动超过4万次，使刀具比实际锋利得多，会节省高达50%的切菜力气。

某些情况下，把它放在食物上，它会依靠振动发出的波，自动把食物切开。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68d6144a9a76d4094fa0463e/339ab195-b3aa-4ee4-a81f-6a9621aa1538.jpeg)

这把刀内置了电池，所以还有配套的刀具充电器。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68d6144a9a76d4094fa0463e/e42ce680-c8e7-401c-80a1-ff5186f59737.jpeg)

2、粘土电路板[12]

电路板是电子产品的基础。

一位国外网友，为了演示电路板并不是高深的产品，特别制作了一块粘土电路板。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68d6144a9a76d4094fa0463e/94b89e83-ba14-4277-82f7-31dd053414c8.jpeg)

他把全过程的照片都放上网，先采集泥巴，然后将其压平。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68d6144a9a76d4094fa0463e/68fe3537-57ad-4052-8fd1-efa32be9a691.jpeg)

在上面挖出电路，然后进行烧制。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68d6144a9a76d4094fa0463e/06b5c4d4-68a4-4a3b-9fe6-a221397cb796.jpeg)

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68d6144a9a76d4094fa0463e/ade3e27f-23ed-424d-925e-1e83db507d45.jpeg)

最后，装上铜线和电子元件，电路板就做好了。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68d6144a9a76d4094fa0463e/83d7f230-0652-4443-bad8-03e1aadd77aa.jpeg)

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68d6144a9a76d4094fa0463e/30413b80-afc6-4d9c-9d25-9a4842f04f45.jpeg)

3、IT 行业的就业岗位[13]

根据知名分析师玛丽·米克尔的 AI 报告，如果从 IT 行业中剔除 AI 相关岗位，美国 IT 行业的就业人数多年来一直处于持平或下降趋势。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68d6144a9a76d4094fa0463e/b34702c5-8309-4b12-becb-236a953b56d0.jpeg)

上图中，蓝线是 IT 行业的总就业人数，绿线是剔除 AI 岗位的就业人数，中间的高峰是疫情期间。

这就是说，虽然 IT 行业本身一直在扩张，但是全部就业增长都发生在 AI 领域。

## 文章

1、超越沙盒[14]（英文）

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68d6144a9a76d4094fa0463e/cd1a8023-3249-4c74-9090-59dd348928d6.jpeg)

如何在网页上安全地运行第三方代码？谷歌提出一个全新的解决方案 SafeContentFrame。

它是一个 JS 库，会将第三方代码加载到一个单独域名 googleusercontent.com 上面，再用 iframe 将其插入当前网页，这样就提供了最大限度的隔离。

2、离线应用为什么尚未流行？[15]（英文）

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68d6144a9a76d4094fa0463e/69ded6a0-ab82-48a7-b54a-84d7734ba73c.jpeg)

离线使用功能一直没有流行起来，作者认为，离线使用就相当于建立一个分布式系统，面临着复杂的同步问题，很难做对。

3、Elasticsearch 不适合用作数据库[16]（英文）

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68d6144a9a76d4094fa0463e/0fdb6a07-bd62-46d5-89ca-80f0229c8817.jpeg)

Elasticsearch 是目前主流的搜索服务，能否把它用作主要数据库？本文告诉你不可以，它不是为数据库而设计的。

4、如何使用 Python 生成音频的文字稿[17]（英文）

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68d6144a9a76d4094fa0463e/6f04bfa4-2fb0-47ac-ab6b-7dd5bf7e74a7.jpeg)

一篇简单的入门教程，一步步教你自己写 Python 脚本，通过 Whisper 模型提取音频的文字稿。

5、避免使用 @ts-ignore[18]（英文）

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68d6144a9a76d4094fa0463e/37ecc864-e281-4f35-b447-3634c5c51d24.jpeg)

TypeScript 的 @ts-ignore 标注，用来关闭下一行的所有报错。作者认为不应该使用它，宁愿改用 @ts-expect-error 标注或者 any 类型。

6、Apple 的私有 CSS 属性，为网页添加“液态玻璃“效果[19]（英文）

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68d6144a9a76d4094fa0463e/bb5dfc6f-405e-468e-abb7-37b7c2ef39fd.jpeg)

作者发现，苹果为 Safari 浏览器添加了一个没有公开的 CSS 属性，让网页元素呈现“液态玻璃”效果。

7、如何调整 systemd 加快启动[20]（英文）

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68d6144a9a76d4094fa0463e/b14c88b2-6c2d-416c-ae76-a10d4e5d9ab2.jpeg)

一篇初学者教程，教你5个技巧，通过调整 systemd 设置，缩短启动时间。

## 工具

1、gpu-kill[21]

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68d6144a9a76d4094fa0463e/cf4d4ab3-48a1-4362-a840-83b1522e5d40.jpeg)

显示 GPU 运行信息的一个工具，自带 Web 管理面板，支持 Nvidia/AMD/Intel/Apple 各种品牌。

另有一个在线 GPU 性能测试网站 Volume Shader BM[22]。（@BOS1980[23] 投稿）

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68d6144a9a76d4094fa0463e/8c116dbd-5d3e-47c6-ad85-80389a630880.jpeg)

2、RustNet[24]

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68d6144a9a76d4094fa0463e/5e2c6dff-de00-4827-aa1a-80a1c6c1c0a2.jpeg)

监控网络流量的终端工具，会显示连接的详细信息，跨平台。

3、PortNote[25]

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68d6144a9a76d4094fa0463e/4ad26865-a33f-464e-82f8-363115447ef9.jpeg)

一个自托管的仪表盘，列出被各种服务占用的本地端口。与 Compose 文件结合后，可以启动/停止 Docker 容器，参见介绍文章[26]。

4、Atlas[27]

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68d6144a9a76d4094fa0463e/71a268f7-7953-4993-9cb5-bdb7209ade1f.jpeg)

一个 Docker 容器，扫描当前网络，图形化显示网络节点信息。

5、Midnight Commander[28]

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68d6144a9a76d4094fa0463e/dc39d16f-a9ac-4ba8-aa4f-f0bc2454dc79.jpeg)

基于终端的文件管理器，支持 Linux 和 Mac。

另有一个类似的终端文件管理器 Yazi[29]。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68d6144a9a76d4094fa0463e/dbaf8db5-fa31-4b6a-ae97-f57eed122a2d.jpeg)

6、frp-tunnel-cli[30]

内网穿透工具 frp[31] 的一个客户端辅助 Bash 脚本，简化隧道的创建和管理。（@openapphub[32] 投稿）

7、Hamsterbase Tasks[33]

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68d6144a9a76d4094fa0463e/55157bf8-2800-46a3-a35b-9e3e244155a1.jpeg)

开源的任务管理软件，支持 Web/手机/桌面各个平台，可以 Docker 部署。（@CaryTrivett[34] 投稿）

8、db-back-tool[35]

网友自己写的 PostgreSQL/MySQL 数据库的备份工具，可以自动备份、加密、压缩数据库，并将备份文件上传至腾讯云 COS 或阿里云 OSS。（@iKeepLearn[36] 投稿）

9、X-CMD[37]

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68d6144a9a76d4094fa0463e/4fa6ea7a-f518-49eb-b29a-a7f5fdbe370d.jpeg)

一个命令行工具集，一键启用 1000+ CLI 工具，跨平台，支持 AI 功能。（@Zhengqbbb[38] 投稿）

## AI 相关

1、Huxe[39]

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68d6144a9a76d4094fa0463e/ead4db38-46dd-4cf1-9034-026fef28d591.jpeg)

个人语音伴侣，生成类似播客的“每日简报”，供你收听，内容包括当日新闻、兴趣爱好、个人日历和邮件等。

它来自 NotebookLM 的主创人员，他们离开谷歌后的创业产品。目前免费使用，参见介绍文章[40]。

2、AIPex[41]

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68d6144a9a76d4094fa0463e/7aa74724-b81a-4620-8a92-4cdadc841f45.jpeg)

周刊以前介绍过的一个开源 Chrome 插件，功能现在扩展了，可以通过 AI 进行浏览器自动化。（@buttercannfly[42] 投稿）

3、binglish[43]

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68d6144a9a76d4094fa0463e/600214b0-32f6-4fac-9c36-4b543d39afec.jpeg)

一个 Python 脚本，自动为 Windows 更换必应 Bing 每日壁纸，并在壁纸上添加“每日单词”，AI 生成单词解释和例句。（@klemperer[44] 投稿）

4、index-tts-lora[45]

网友基于 B 站开源的 Index-TTS 语音合成模型的微调模型，提升语音的韵律感和自然度。（@asr-pub[46] 投稿）

5、Neovate[47]

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68d6144a9a76d4094fa0463e/aa768b5b-afc7-4c4c-9c6d-ef053528f9c3.jpeg)

基于终端的智能编码助手（Code Agent），可以看作是开源的 Claude Code。（@xierenyuan[48] 投稿）

6、FlyCut Caption[49]

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68d6144a9a76d4094fa0463e/206f0825-dec2-4d57-930b-19f8b9835c18.jpeg)

一个基于 Web 的 AI 视频字幕编辑工具，可以视频语音自动转文本，生成字幕，试用 Demo[50]。（@x007xyz[51] 投稿）

7、mcpstore[52]

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68d6144a9a76d4094fa0463e/6a4d12d1-99c3-4d4e-87e1-16df57477d85.jpeg)

一个 MCP 服务的管理工具，接入各种 MCP 服务器，自带 Web 管理面板。（@whillhill[53] 投稿）

## 资源

1、99个物理小实验[54]

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68d6144a9a76d4094fa0463e/c59023f6-822f-4aac-81c3-45c66c94b50e.jpeg)

一本在线的英文书籍，精选了荷兰中学物理的99个小实验，涉及各个领域（力、光、磁、波等等）。

2、NPM 安全最佳实践[55]

最近爆出了一系列 npm 软件包投毒事件，这个仓库收录了各种 npm 安全措施，分为使用者和发布者两大部分。

## 图片

1、**电动车原理**

网上流传的电动车原理图片。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68d6144a9a76d4094fa0463e/9c137b83-658d-4933-821a-1a6162ed5572.jpeg)

2、一道几何题[56]

正方形里面有一个小圆，请问小圆的半径与正方形边长的关系是多少？

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68d6144a9a76d4094fa0463e/ba6f8e56-57aa-4aa9-bcd7-cb12a210d40c.jpeg)

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68d6144a9a76d4094fa0463e/8f748cfa-43fc-4ff9-9c93-2a5e0bf3751c.jpeg)

这道题好像很不容易，答案是正方形边长的 4/33。

## 文摘

1、AI 编程只能解决70%的问题[57]

根据我的观察，公司里面的高级程序员和低级程序员，使用 AI 的方式是不一样的。

**高级程序员并不完全信任 AI 的输出，只是用 AI 加速项目**。他们一般会审查和重构 AI 生成的代码，对于 AI 的架构决策也是抱着怀疑的态度。

初级程序员更倾向于跳过审查和重构，全盘接受 AI 的输出，从而导致“纸牌屋式“的代码：看起来能发挥作用，一旦投入使用就会崩溃。

我不知道，AI 未来会不会替代程序员，但是现阶段，AI 编程还不能解决100%的软件问题，但已经可以解决70%的问题。这相当于，**AI 可以减轻高级程序员70%的工作量**。

剩下的30%，依然需要依靠程序员的经验和专业知识，而**初级程序员恰恰缺少的是这30%**。

所以，听起来可能违反直觉：AI 对高级程序员比对初级程序员帮助更大，更容易产生工作成果。

现阶段的 AI，更像团队中的一个非常有干劲的初级程序员，可以快速编写代码，但需要不断的监督和纠正。**你知道的越多，你就越能指导它。**

所以，AI 的正确用法是，高级程序员用它来加速他们已经知道如何做的事情，初级程序员用它来学习该做什么。

## 言论

1、

AI 会一直扩展，一直到大部分太阳的能量都被用于计算。

-- 马斯克最新访谈[58]

2、

我认为，火星可以在30年内自给自足。每两年，行星会排成一条直线，你就可以出发去火星。所以，30年内大约有10到15个左右的火星出发窗口。

每次出发，运往火星的货物吨位会呈指数级增长，那么30年内，我们可以让火星自给自足。

-- 马斯克最新访谈[59]

3、

软件业悄然兴起一种新的工作“氛围清理”（Vibe Coding cleanup），专门解决“氛围编程”导致的问题。这真是 AI 时代最大的讽刺：人类被雇来清理 AI 的垃圾。

-- 《氛围清理即服务》[60]

4、

AI 泡沫是很有可能的，但对于 Meta 这样的公司来说，更大的风险是犹豫不决。

如果我们最终为 AI 浪费了数千亿美元，显然非常不幸，但我实际上认为错过 AI 的风险更高。对于我们来说，风险不是过于激进，而是不够激进。

-- 扎克伯格[61]

5、

今天的计算机是响应者（responder）：你让它做某事，它就会去做。下一阶段的计算机是“代理”（agent），它就像一个盒子里的小人，开始预测你想要什么。它不是帮助你，而是引导你处理大量的信息，就像你在盒子里有一个小伙伴。

-- 乔布斯[62]，1984年的采访

## 往年回顾

[乒乓仓](https://mp.weixin.qq.com/s?__biz=MzI4NjAxNjY4Nw==&mid=2650238316&idx=1&sn=aee84766d54c2a0bc71dfccd9b6afb34&scene=21#wechat_redirect)[63]（#320）

["精益开发"的精益是什么？](https://mp.weixin.qq.com/s?__biz=MzI4NjAxNjY4Nw==&mid=2650234831&idx=1&sn=35d411d7c561cd0c9b3cf146d306a282&scene=21#wechat_redirect)[64]（#270）

[人工智能的机会在哪里](https://mp.weixin.qq.com/s?__biz=MzI4NjAxNjY4Nw==&mid=2650231456&idx=1&sn=a8e97e449484c094db18031c385e30d0&scene=21#wechat_redirect)[65]（#220）

[软件订阅制的胜利](https://mp.weixin.qq.com/s?__biz=MzI4NjAxNjY4Nw==&mid=2650227145&idx=1&sn=f4a22e38664c458c80dbd88d8da4d084&scene=21#wechat_redirect)[66]（#170）

（完）

### References

`[1]` 开源:*https://github.com/ruanyf/weekly*`[2]`投稿:*https://github.com/ruanyf/weekly/issues*`[3]`《谁在招人》:*https://github.com/ruanyf/weekly/issues/7674*`[4]`邮件联系:*mailto:yifeng.ruan@gmail.com*`[5]`yifeng.ruan@gmail.com:*mailto:yifeng.ruan@gmail.com*`[6]`via:*https://ztylez.com/life/play/2025/09/23/331873/*`[7]`Nano Banana:*https://aistudio.google.com/models/gemini-2-5-flash-image*`[8]`官网:*https://aistudio.google.com/prompts/new_chat?model=gemini-2.5-flash-image-preview*`[9]`第三方网站:*https://github.com/search?q=repo%3Aruanyf%2Fweekly+nano+banana&type=issues*`[10]`Awesome 仓库:*https://github.com/PicoTrex/Awesome-Nano-Banana-images*`[11]`超音速厨师刀:*https://seattleultrasonics.com/products/c-200-ultrasonic-8-chefs-knife*`[12]`粘土电路板:*https://feministhackerspaces.cargo.site/Clay-PCB-Tutorial*`[13]`IT 行业的就业岗位:*https://www.derekthompson.org/p/the-25-most-interesting-ideas-ive*`[14]`超越沙盒:*https://bughunters.google.com/blog/6715529872080896/beyond-sandbox-domains-rendering-untrusted-web-content-with-safecontentframe*`[15]`离线应用为什么尚未流行？:*https://marcobambini.substack.com/p/why-local-first-apps-havent-become*`[16]`Elasticsearch 不适合用作数据库:*https://www.paradedb.com/blog/elasticsearch-was-never-a-database*`[17]`如何使用 Python 生成音频的文字稿:*https://www.pavlinbg.com/posts/python-speech-to-text-guide*`[18]`避免使用 @ts-ignore:*https://evanhahn.com/ts-ignore-is-almost-always-the-worst-option/*`[19]`Apple 的私有 CSS 属性，为网页添加“液态玻璃“效果:*https://alastair.is/apple-has-a-private-css-property-to-add-liquid-glass-effects-to-web-content/*`[20]`如何调整 systemd 加快启动:*https://www.xda-developers.com/systemd-tweaks-boost-boot-time/*`[21]`gpu-kill:*https://github.com/kagehq/gpu-kill*`[22]`Volume Shader BM:*https://www.volumeshader.dev/*`[23]`@BOS1980:*https://github.com/ruanyf/weekly/issues/7804*`[24]`RustNet:*https://github.com/domcyrus/rustnet*`[25]`PortNote:*https://github.com/crocofied/PortNote*`[26]`介绍文章:*https://www.xda-developers.com/reasons-why-portnote-port-of-call-on-every-server/*`[27]`Atlas:*https://github.com/karam-ajaj/atlas*`[28]`Midnight Commander:*https://github.com/MidnightCommander/mc*`[29]`Yazi:*https://github.com/sxyazi/yazi*`[30]`frp-tunnel-cli:*https://github.com/openapphub/frpc-cli*`[31]`frp:*https://gofrp.org/zh-cn/docs/overview/*`[32]`@openapphub:*https://github.com/ruanyf/weekly/issues/7785*`[33]`Hamsterbase Tasks:*https://github.com/hamsterbase/tasks*`[34]`@CaryTrivett:*https://github.com/ruanyf/weekly/issues/7792*`[35]`db-back-tool:*https://github.com/iKeepLearn/db-back-tool*`[36]`@iKeepLearn:*https://github.com/ruanyf/weekly/issues/7798*`[37]`X-CMD:*https://github.com/x-cmd/x-cmd*`[38]`@Zhengqbbb:*https://github.com/ruanyf/weekly/issues/7806*`[39]`Huxe:*https://www.huxe.com/*`[40]`介绍文章:*https://www.xda-developers.com/huxe-app-official-launch/*`[41]`AIPex:*https://github.com/AIPexStudio/AIPex*`[42]`@buttercannfly:*https://github.com/ruanyf/weekly/issues/7783*`[43]`binglish:*https://github.com/klemperer/binglish*`[44]`@klemperer:*https://github.com/ruanyf/weekly/issues/7800*`[45]`index-tts-lora:*https://github.com/asr-pub/index-tts-lora*`[46]`@asr-pub:*https://github.com/ruanyf/weekly/issues/7789*`[47]`Neovate:*https://github.com/neovateai/neovate-code*`[48]`@xierenyuan:*https://github.com/ruanyf/weekly/issues/7805*`[49]`FlyCut Caption:*https://github.com/x007xyz/flycut-caption*`[50]`Demo:*https://caption.flycut.co/en/tool*`[51]`@x007xyz:*https://github.com/ruanyf/weekly/issues/7801*`[52]`mcpstore:*https://github.com/whillhill/mcpstore*`[53]`@whillhill:*https://github.com/ruanyf/weekly/issues/7790*`[54]`99个物理小实验:*https://interactivetextbooks.tudelft.nl/showthephysics/Introduction/About.html*`[55]`NPM 安全最佳实践:*https://github.com/bodadotsh/npm-security-best-practices*`[56]`一道几何题:*https://samjshah.com/2025/08/05/sangaku-puzzle-i-cant-solve/*`[57]`AI 编程只能解决70%的问题:*https://addyo.substack.com/p/the-70-problem-hard-truths-about*`[58]`马斯克最新访谈:*https://t.wangbase.com/0ZKey*`[59]`马斯克最新访谈:*https://t.wangbase.com/0ZKey*`[60]`《氛围清理即服务》:*https://donado.co/en/articles/2025-09-16-vibe-coding-cleanup-as-a-service/*`[61]`扎克伯格:*https://finance.sina.cn/7x24/2025-09-19/detail-infqzkhk9726343.d.html*`[62]`乔布斯:*https://simonwillison.net/2025/Sep/18/steve-jobs/*`[63]`乒乓仓:*https://www.ruanyifeng.com/blog/2024/10/weekly-issue-320.html*`[64]`"精益开发"的精益是什么？:*https://www.ruanyifeng.com/blog/2023/09/weekly-issue-270.html*`[65]`人工智能的机会在哪里:*https://www.ruanyifeng.com/blog/2022/08/weekly-issue-220.html*`[66]`软件订阅制的胜利: *https://www.ruanyifeng.com/blog/2021/08/weekly-issue-170.html*

