---
作者:
  - "大淘宝技术"
原文链接: https://mp.weixin.qq.com/s?__biz=MzAxNDEwNjk5OQ==&amp;mid=2650541404&amp;idx=1&amp;sn=7cbcd6b92f9944226c48890129be0bec&amp;chksm=82dc496af37c233942a29188bb1c125e28211107117ebc734640158e9c817de03d04bcf93133&amp;mpshare=1&amp;scene=1&amp;srcid=0901VuSySieRk24OXUTH0jJy&amp;sharer_shareinfo=4c8fbc92de3eb1a0c9560b46cb7404c7&amp;sharer_shareinfo_first=4c8fbc92de3eb1a0c9560b46cb7404c7#rd
发布时间: ""
收藏时间: "2025-09-01"
关联日记: "[[2025-09-01]]"
tags:
  - 文章
---
![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68b57984ad843515e3b67b62/f11efd84-d258-475d-8775-a872eb697487.gif)

本文通过分享将AI Agent技术应用于“智能播报助手”和“批量建任务”两个真实业务场景的实践历程，深刻阐述了当下将AI Agent与传统工程系统深度融合，而非追求完全替代，才是实现业务提效和价值落地的有效路径。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68b57984ad843515e3b67b62/75cc8d07-ab3d-4fe2-92cb-00eed3d9369d.webp)

引言

Agent随着Agent相关技术的快速发展，验证其在企业实际业务场景中的价值已成为当务之急。脱离应用场景的技术创新终将沦为“空中楼阁”。本文分享我将agent与工程结合并应用于两个业务场景的历程，并在最后给出agent与工程的选型总结。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68b57984ad843515e3b67b62/7fb10f9f-a172-4892-8c73-cf2579c3c04c.png)

Agent + MCP 打造智能播报助手

▐** 2**.1 业务背景与问题

在我们的日常工作中会制作或使用大量统计报表。淘天会在一款数据产品上制作报表相关内容，制作好的报表会由关心报表数据的同学每隔一定周期去查看报表的数据是否出现异常。比如每天早上十点查看表A的数据、大促上下线时每隔半小时查看表B的数据。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68b57984ad843515e3b67b62/d7f1dac8-acd3-4a24-9fa7-49e1a9c93c79.jpeg)

定时看报表的整体流程，简单概括就是打开网页，找到异常数据，基于异常数据采取某些行为。FBI拥有定时播报的能力，但是存在以下局限性：

- 表格类型报表只能播报图片，若要导出报表数据，只能选择「邮件格式」并且只能把数据导出为excel格式。若用工程（编码）处理，需要对每一个表格类型定义接收对象。


![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68b57984ad843515e3b67b62/730b355b-3b80-412e-9b33-2acf80c5ad66.jpeg)

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68b57984ad843515e3b67b62/6fa6c1c6-cf77-419c-9fbd-6922bf495c17.jpeg)

- 文本类型报表可以定义异常指标，但只能修改异常指标的展示样式，满足不了「只有某指标出现异常时才播报给某些特定的联系人」的需求，并且无法基于异常数据进行后续动作。


![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68b57984ad843515e3b67b62/e4593ae2-b24e-43f2-9152-d51a00072c7a.jpeg)

- 虽然底表的数据我们可以直接获取，但无法拿到FBI加工过的数据如日环比。比如下图中，定义异常数据为「指标1 < 10%或指标2 < 30%」。同学甲只关注A-aa1的数据、同学乙只关注A-aa2的数据、同学丙只关注B-bb1的数据。那么就期望在周期到达时，向同学甲和同学丙播报异常数据，甚至是基于异常数据进行下一步动作。FBI目前做不到这一点。


![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68b57984ad843515e3b67b62/998c0ddb-a0e5-47bf-9aaf-d6503111f5a5.jpeg)

▐** 2**.2 MCP介绍

事情的转折点在于LLM的不断进化（如claude4）以及MCP的横空出世。MCP （Model Context Protocol） ，翻译过来就是模型上下文协议，简单来说，它定义了一套标准规则，让LLM模型能够安全、有序地访问和使用各种外部资源，从而大大扩展Agent的能力边界。MCP中有两个重要角色：MCP Client和MCP Server。MCP Server提供各种各样的能力与工具，MCP Client是MCP Server的调用者。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68b57984ad843515e3b67b62/0638f413-cf5b-4b88-b567-9a2d8f45a620.jpeg)

举一个通俗的例子，把MCP Client 想象成DVD播放器，DVD播放器可以放入不同的碟片（MCP Server），不同的碟片有不同的内容（能力），但肯定不能向DVD播放器中放入磁带（不符合MCP的Server）。在AI场景下，就是给予Agent通用地调用各种各样工具的能力。

可能会有同学好奇：让Agent调用工具难道是最近才有的能力吗？其实并不是这样，工具调用（Function Calling）是早于MCP提出来的能力，也就是说agent在MCP出现前就可以进行工具调用。过去只有Function Calling时，不同厂商（OpenAI、Anthropic......）的Function Calling协议都不同，并且许多开源模型不支持Function Calling。比如为OpenAI的某个模型开发了一个tool，想要复用到Anthropic（Claude的开发者）的某个模型，先要查看模型是否支持Function Calling，若支持还需要重新对tool进行适配开发。而MCP提供了一套通用的协议，免去了重复开发工具的问题，大大降低了工具使用的复杂度。

MCP目前有三种通讯方式：STDIO（Standard Input/Output）、SSE（Server-Sent Events，基于HTTP的单向数据流传输方式）和StreamableHttp。Mcp Client和Mcp Server部署在同一台机器上，通过标准输入输出通信的方式就是STDIO模式。部署在不同机器通过Http请求通信就是SSE模式和StreamableHttp模式。STDIO因为在本地运行，是绝对安全的；但SSE和StreamableHttp模式若暴露连接方式，可能会有安全问题。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68b57984ad843515e3b67b62/822db8b8-9e60-46ff-9ba0-49bb90ca2b54.jpeg)

cherryStudio中连接类型设置

2025年3月26日，Anthropic在MCP规范中正式弃用SSE传输，全面转向StreamableHttp。为什么要用StreamableHttp替换SSE？SSE的原理是MCP Client与MCP Server通过HTTP建立SSE长链接，之后MCP Server就可以不断向Client发送数据，而不需要每次都进行三次握手；MCP Client可以主动关闭SSE长链接。问题在于SSE的整个通讯过程都需要依赖SSE长链接，一旦出现网络毛刺（短暂中断），那么MCP Server向MCP Client发送的数据就会丢失，并且MCP Server无法感知到数据的丢失。而Streamable方式中，MCP Server可以感知到数据丢失，连接恢复时可以持续地将没有发送给MCP Client的数据再次发送，保证长链接的高可用性。

随着MCP的流行，其社区也不断壮大，出现了越来越多符合MCP的工具，相关平台也在积极适配MCP模块。（mcp.so、魔搭社区）MCP就是模型进行工具调用的未来。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68b57984ad843515e3b67b62/4c8b6399-43f5-4c30-915b-525eafd4f461.jpeg)

mcp.so

▐** 2**.3 agent + MCP快速上手

没有使用过MCP的同学可以按照以下步骤快速上手体验一下，非常简单。

1.首先需要一个AI对话客户端。ideaLab就是这样的产品，但ideaLab目前不支持STDIO模式。市场上现在有大量的客户端，我们选择Cherry Studio快速体验。首先安装客户端。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68b57984ad843515e3b67b62/e74abd0b-9407-4043-8945-c6e8fe831d5a.jpeg)

Cherry Studio官网

2.安装完成后，点击设置--模型服务--添加。随便填写“提供商名称”。若使用ideaLab的sk，提供商类型选择默认的OpenAI。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68b57984ad843515e3b67b62/fd9b36d3-ed9d-43d9-9ae2-b2e369a4ebe0.jpeg)

3.添加完成后，输入ideaLab的sk，填入API地址。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68b57984ad843515e3b67b62/d8e956ae-1543-44b3-a2a8-547131028908.jpeg)

4.点击模型平台中的“添加”，这里需要填入模型ID。进入ideaLab提供的模型清单，复制模型ID，填入即可。注意，选择的模型必须要有工具调用能力。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68b57984ad843515e3b67b62/31bebf1a-43cc-49ac-8ba1-002e9050e218.jpeg)

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68b57984ad843515e3b67b62/a211e94f-1f36-4f88-a415-53ae9876fde7.jpeg)

ideaLab模型清单

5.点击“助手”，选择配置的模型，测试连通性。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68b57984ad843515e3b67b62/d80f500c-728a-4216-8e29-92d72db1e8e3.jpeg)

6.回到设置，选择“MCP设置”，点击添加服务器--快速创建。（若需要安装依赖，跟着客户端教程无脑安装即可）

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68b57984ad843515e3b67b62/1264c697-5b22-4285-b743-5408bf132e38.jpeg)

7.配置MCP Server。这里以魔搭社区提供的文件系统服务为例。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68b57984ad843515e3b67b62/b1349435-4c0f-420d-9faf-c23711077cd9.jpeg)

魔搭社区

8.进入后可以看到服务提供的工具，我们以stdio方式安装。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68b57984ad843515e3b67b62/1d634e1b-1732-4cbf-8813-fe2f7efe0aaa.jpeg)

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68b57984ad843515e3b67b62/4a3a8b12-163d-4f64-b59e-1176b6b3ac67.jpeg)

9.点击助手--MCP设置，选择刚才配置好的MCP Server。（再次强调，模型必须要有工具调用能力）

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68b57984ad843515e3b67b62/3c759b3d-4a0b-412e-a14c-233ebf3b1278.jpeg)

10.测试工具调用效果。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68b57984ad843515e3b67b62/11cffcbd-a71f-40f9-9205-93c06606715a.jpeg)

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68b57984ad843515e3b67b62/bd7d364f-5b27-4663-827e-e7c43073d002.jpeg)

实际体验后，不知道大家有没有体会到MCP的作用：MCP Client使用统一的配置方式，可以快速接入各种各样的工具。没有工具调用能力的agent，最多就是充当「百科全书」的角色。而当agent可以进行工具调用，就可以把agent当作是一个「人」来看待了。工具调用大大拓展了agent的能力边界，它可以像我们一样写文件或是操作浏览器。那么上述的看报表场景痛点，或许可以通过agent + MCP的方式解决。

▐** 2**.4 浏览器操作探索过程

- 2.4.1. 服务选择


浏览器相关的MCP Server主要分为以下两类：

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68b57984ad843515e3b67b62/6ef49920-7c86-4b46-81e8-d7d07d718b15.png)

playwright-mcp：一个模型上下文协议（MCP）服务器，利用 Playwright 提供浏览器自动化功能。该服务器使大型语言模型能够通过结构化的可访问性快照与网页进行交互，无需依赖截图或视觉调优模型。目前仍在活跃更新中。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68b57984ad843515e3b67b62/f37e21c9-c2d2-48e5-90f3-6894085a70ab.jpeg)

playwright Releases版本

其提供的工具列表如下，可以直接在github中查看：

能力工具解释核心自动化功能browser_click点击操作browser_close关闭浏览器browser_console_messages获取控制台消息browser_drag按住鼠标左键进行拖拽browser_evaluate评估JavaScriptbrowser_file_upload上传文件browser_hover将鼠标悬停在页面上的某元素browser_navigate导航到指定URLbrowser_navigate_back返回上一页browser_navigate_forward前进到下一页browser_network_requests获取所有网络请求browser_press_key模拟键盘操作browser_resize调整浏览器窗口大小browser_select_option在下拉列表选择选项browser_snapshot获取页面快照browser_take_screenshot截图browser_type在可编辑元素中输入文本browser_wait_for等待文本出现或消失，或等待指定时间标签页管理browser_tab_close关闭标签页browser_tab_list列出标签页browser_tab_new打开新标签页browser_tab_select选择标签页浏览器安装browser_install安装配置中指定的浏览器基于坐标使用 --caps=vision开启browser_mouse_click_xy点击指定坐标browser_mouse_drag_xy按住鼠标左键，拖拽到指定坐标browser_mouse_move_xy把鼠标移动到指定坐标PDF生成使用 --caps=pdf开启browser_pdf_save将页面另存为PDF

测试playwright-mcp的效果，还是以cherry studio举例。

1.在设置--MCP服务器中，添加一个服务器，类型选择「stdio」，命令输入「npx」，写入参数如图。-y 可以让agent自动进行工具调用而无需等待用户同意；@playwright/mcp@0.0.27 指定安装的工具及版本，也可以指定@playwright/mcp@latest；--headless开启无头模式，agent的浏览器操作不会打开一个可见的浏览器，如果想要看浏览器的调用过程就移除这个参数。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68b57984ad843515e3b67b62/887bc383-2517-4cdc-b7f7-c715127e68db.jpeg)

2.回到聊天助手页面，打开MCP服务器，选择刚才配置好的MCP Server。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68b57984ad843515e3b67b62/4bfc2de6-dc6d-4d80-a9c6-fd2f35f8af46.jpeg)

3.让agent总结网页内容，效果如下。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68b57984ad843515e3b67b62/9536dfb3-4332-4807-88d1-d2eb3ee59c7f.jpeg)

- 2.4.2. 环境准备


若要在项目环境中使用agent和mcp服务，需要以下准备。

1.工程dockerFile中需安装playwright，并解决大量的依赖问题。（也可以新建docker，但只能用sse或streamableHttp模式）

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68b57984ad843515e3b67b62/d72d9a10-00bb-4121-8a47-47e6383eb39d.jpeg)

2.Java工程中需要使用Spring-Ai或Spring-Ai-Alibaba框架进行Agent开发。创建MCP Client时需确保是无头模式且要指定playwright的无头浏览器路径。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68b57984ad843515e3b67b62/26f55d67-d8b6-454b-a238-3fe65672f2b0.jpeg)

- 2.4.3. agent构建


有了工具的支持，就可以设置定时任务让agent看报表了。对于不同的报表场景，定时时间、具体的网页操作、要关注的指标、联系人等都各不相同。对数据类型进行划分，主要分为以下两类。

配置类：触发agent补充信息类：agent拿到后执行具体任务与生成结果模型相关配置（选择什么模型，模型的温度）、定时时间、触发提示词。如图就是一段期望每天早上09:30执行的场景配置。![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68b57984ad843515e3b67b62/d1869f0d-b948-4d88-b749-2c32ef577232.jpeg)不同场景的工作流、要打开的url、浏览器窗口大小、结果标题与内容格式、规定异常数据、具体示例等。![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68b57984ad843515e3b67b62/24b70c80-0d47-43c1-ad7d-70ea1ace7a45.jpeg)

构建系统提示词时，先使用agent生成一个提示词框架（[Agent构建：Prompt工程、工作流设计与知识库优化实战](https://mp.weixin.qq.com/s?__biz=MzIzOTU0NTQ0MA==&mid=2247552381&idx=1&sn=966dfc91ab7e75d349fcc82f0713ab04&scene=21#wechat_redirect)），然后基于agent的行为与结果不断调整。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68b57984ad843515e3b67b62/6137090f-c141-444f-9aeb-b8a96103b636.jpeg)

最开始构建时，我把不同的场景全部放到了系统提示词中，通过mermaid的选择节点来区分不同的场景，如下图。但随着场景的增多，会导致流程描述越来越复杂，这种方案肯定是不行的。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68b57984ad843515e3b67b62/a2c9f443-c083-439c-88ea-27a495497ecd.jpeg)

于是想到把不同场景的不同信息保存到向量数据库中，但向量数据库更适合保存非结构化文本。现在需要保存的是不同场景的元数据信息，不太适合保存到向量数据库中。于是尝试把数据保存到关系型数据库中，表结构中我设置了keywords列，用户提问后agent会先查询keywords，进行语意匹配，返回最适合的id，再查询id对应的其他信息。若没有匹配的keywords，则按照用户提供的信息进行任务，这一步其实就是RAG做的事情。流程如下。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68b57984ad843515e3b67b62/f9a6bc9b-8ba6-4396-a9ac-01b4009f2bed.jpeg)

若担心agent生成危险的sql，也可以直接在系统提示词中写好需要执行的sql，并且创建一个只用来让agent调用的数据库，不要直接让agent调用线上的库表，降低风险。

- 2.4.4. 消息推送


消息推送可以在工程中结合钉钉机器人实现。只需要在知识库（数据库）中配置好场景结果的联系人工号或群id，让agent按照指定JSON格式返回结果，工程解析后就可以实现钉钉消息推送。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68b57984ad843515e3b67b62/7092d85c-2b72-439d-9850-06c810e9c649.jpeg)

为了避免把消息发送给无关的人或群，在Switch中配置工号/群号白名单，工程中作强校验。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68b57984ad843515e3b67b62/b59161f4-b349-4bc4-a232-ef5f836113b6.jpeg)

- 2.4.5. 已有场景介绍


目前有如下三个场景已验证且稳定执行，并且有其他场景待接入：

1.每天09:30查看某报表是否存在异常数据（指定日环比小于-20%），如果有异常数据，就发送钉钉消息给相应负责人。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68b57984ad843515e3b67b62/a5ab80b3-66c3-45c3-bc4b-9a6452ac3074.jpeg)

2.大促上线时，每半小时查看某任务的的执行情况并在群中播报。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68b57984ad843515e3b67b62/50c78f79-4ec2-4494-b0c5-bb22a0d3dc6b.jpeg)

3.每天11:00查看报表某指标，若小于90%，则打开另一个指定页面，筛选后关闭开关。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68b57984ad843515e3b67b62/9040c182-3800-4286-bc5d-6c8da86db4df.jpeg)

- 2.4.6. 问题汇总


使用过程中遇到的问题如下：

1. 浏览器窗口大小会影响快照结果。基于实际经验设置窗口大小为3840*2160可以满足大部分场景。也可以在提示词中说“为了获取完整结果，你需要调整合适的窗口大小”。
2. 表格数据容易出现数据错乱的情况，可能需要在examples中模拟表格数据。需要在灵活性与准确性中找到平衡点。
3. 提示词中约束agent可以获取的快照内容，如“遵守快照内容最小获取原则”。否则容易导致token直接超出限制。
4. 提示词中限制失败重试最大次数，否则agent可能会重复调用失败方法。如“若某操作执行失败，重试三次之后换一种操作方式。若仍然失败，则结束任务”。
5. 浏览器操作最后一定要关闭浏览器。playwright执行新任务会默认打开新的浏览器窗口，若不关闭，可能出现资源泄漏和端口冲突问题。
6. 钉钉markdown消息不支持表格类型，不适合返回大量数据的场景。


- 2.4.7. Agent看报表与FBI播报对比


对比如下表。总体来说，前者可以不局限于FBI平台，任何页面都可以通过agent + playwright-mcp 的方式进行操作处理，并且可以轻松获取页面的数据。但若只是定时播报，直接使用FBI的播报能力即可。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68b57984ad843515e3b67b62/c32ae436-cee2-453e-949c-b9edb38ca925.png)

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68b57984ad843515e3b67b62/7b671fab-7d5d-475c-abdd-fbfbc5a37631.png)

Agent批量建任务

▐** 3**.1 业务背景与问题

在大促与日常切换时，运营会在某平台基于excel的内容进行批量任务的创建与暂停操作。目前存在以下痛点：

1. 任务量过多，任务的配置都不相同，每次操作需一小时左右。
2. 需人肉对比excel中的任务与线上的任务，判断哪些任务应该新增创建、哪些任务应该修改，且要找到所有不存在于excel中的任务并暂停。


![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68b57984ad843515e3b67b62/c45a8a9c-4a56-4d37-b971-9af3dd190412.jpeg)

在这个背景下，尝试引入agent，期望让agent基于excel和已有的任务自动生成结果，解放人力。

▐** 3**.2 Agent批量建任务探索过程

- 3.2.1. 能力尝试：只让Agent处理最简单的场景


首先只考虑最简单的情况，试验可行性：对于上传的所有任务，统一按照新增处理。通过工程解析excel，在ideaLab中配置agent，并在提示词中增加字段转换规则（即将excel的字段内容转换为枚举值）和补充信息规则（即给每个任务添加默认属性和默认值），agent处理流程图如下。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68b57984ad843515e3b67b62/61884edc-3b6f-4b66-80fb-56be49bf01a1.jpeg)

在该场景下，任务范围需要由agent调用工具并基于一定规则进行匹配。可以在ideaLab中添加工具实现。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68b57984ad843515e3b67b62/b0ab9901-c2e3-451f-bc6e-f4b221fb4c04.jpeg)

最终效果如下。Agent可以完成该场景下的“NL2Task”任务。于是继续探索更加复杂的场景。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68b57984ad843515e3b67b62/ab0fcb5d-253a-4019-8d09-8ae9372e578d.jpeg)

- 3.2.2. 初见端倪：完全让Agent处理复杂逻辑


现在需要让agent处理更加复杂的场景，要对比上传的任务和已经存在的任务。agent处理流程图如下。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68b57984ad843515e3b67b62/d4455193-20eb-47bd-99d3-9edf87b1d0cc.jpeg)

相比于初版，复杂点在于：

1. 输入token更多：需要把已经存在的任务信息全部交给agent；
2. 处理更加复杂：需要对比每一个上传对象和已有对象，寻找差异；


在与实际业务结合后，出现了以下问题：

1. 运营每次需要处理50个左右的任务，若一次性让agent处理所有任务，agent的回答速度非常慢且质量很差；
2. 小二工作台限制HSF方法等待时间最大为60s且不支持sse，无法保证agent在规定时间内完成响应；


解决方式如下：

1. 拆分任务，并发调用。经过测试，调用ideaLab的agent请求接口最多支持10并发；
2. 从同步等待改为异步轮询，将agent结果保存到redis中；


虽然拆分了任务，减少了每次处理的任务数量，但是我在调试时发现输入token数量非常庞大，一次调用就需要4w左右，再加上我把任务拆成了十份，那么调用一次成本就在40000/1000*0.1*10=40元左右。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68b57984ad843515e3b67b62/473078a6-465f-4d6b-8843-9d9af0bd4daf.jpeg)

成本问题无法避免。并且因为token输入过多，模型响应速度很慢，平均在25s左右才会进行首次响应。且我花费了大量时间调整提示词，生成的结果依旧无法保证比较高的准确性，包括但不限于字段转换错误、范围匹配错误、漏处理任务等问题。

现在回过头来重新考虑这个场景：

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68b57984ad843515e3b67b62/c08425dc-9e58-4de1-9062-203eeeed52a9.jpeg)

前面三点，工程不仅可以干，而且处理的更精准，更快！换句话说，这个事情本来就应该工程做，强行让agent做，耗费大量精力和财力，最终效果也是差到无法交付的地步！

- 3.2.3. 各取所长：工程 + agent结合高效处理


最终对流程进行重构，工程处理除了任务范围的所有工作，agent处理流程图如下。任务范围因为要根据excel的内容基于规则进行语意匹配，还是适合agent处理。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68b57984ad843515e3b67b62/b1fc2323-b1eb-4d35-a0b6-d47928cf0e6e.jpeg)

最终agent只干一件事情，减少了输入输出token，提高了响应速度和回答质量，再结合工程保障准确性，效果非常好。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68b57984ad843515e3b67b62/71b482fb-773b-4531-8c87-5754b576ca55.jpeg)

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68b57984ad843515e3b67b62/c3652069-88e6-4111-a417-195886aa8168.png)

总结

以上两个场景都将agent与工程进行结合并作用于实际业务场景中，目的是为了利用Agent提效。但第二个场景起初让agent做了不适合的工作，反而降低了效率。以下列出agent和工程的能力对比。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68b57984ad843515e3b67b62/48e095e2-a9b5-4e70-aa33-24ab7f5e9ab3.png)

agent的本质还是概率游戏，它并不是万能的，千万不要把任何场景问题都一股脑全部丢给agent，期望它可以给出一个完美的结果。现阶段的最优策略是将agent与工程结合使用，扬长避短。在做技术方案时，要充分考虑每一环适合用什么工具解决。在具体实践时，若发现方向不对且尝试调整过后仍然得不到比较好的结果，就及时更换方向，不要死磕。只有准确理解各种技术的边界和长处，才能构建出真正高效、稳健的解决方案。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68b57984ad843515e3b67b62/2c3c87c6-6df8-4bf7-9d68-bfec0cd87fec.png)

参考链接

- 大模型MCP更高效的通信：StreamableHTTP协议：https://blog.csdn.net/zhangzhentiyes/article/details/147855601
- playwright-mcp：https://github.com/microsoft/playwright-mcp
- 魔搭社区：https://modelscope.cn/mcp
- Cherry Studio：https://www.cherry-ai.com/


**¤ 拓展阅读 ¤**[3DXR技术](https://mp.weixin.qq.com/mp/appmsgalbum?__biz=MzAxNDEwNjk5OQ==&action=getalbum&album_id=2565944923443904512#wechat_redirect) | [终端技术](https://mp.weixin.qq.com/mp/appmsgalbum?__biz=MzAxNDEwNjk5OQ==&action=getalbum&album_id=1533906991218294785#wechat_redirect) | [音视频技术](https://mp.weixin.qq.com/mp/appmsgalbum?__biz=MzAxNDEwNjk5OQ==&action=getalbum&album_id=1592015847500414978#wechat_redirect)[服务端技术](https://mp.weixin.qq.com/mp/appmsgalbum?__biz=MzAxNDEwNjk5OQ==&action=getalbum&album_id=1539610690070642689#wechat_redirect) | [技术质量](https://mp.weixin.qq.com/mp/appmsgalbum?__biz=MzAxNDEwNjk5OQ==&action=getalbum&album_id=2565883875634397185#wechat_redirect) | [数据算法](https://mp.weixin.qq.com/mp/appmsgalbum?__biz=MzAxNDEwNjk5OQ==&action=getalbum&album_id=1522425612282494977#wechat_redirect)


新枝标签： #Agent开发框架
