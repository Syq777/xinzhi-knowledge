---
作者:
  - "技术人说"
原文链接: https://m.okjike.com/originalPosts/6a1068ff7f82528246eb69df?s=ewoidSI6ICI2MzAxMDVhZmM2Y2VmNmJkMjYxMDNhYzYiCn0%3D&amp;utm_source=wechat_session
发布时间: ""
收藏时间: "2026-05-23"
关联日记: "[[2026-05-23]]"
tags:
  - 文章
---
Anthropic今年三月上线了一个叫AnthropicAcademy的课程平台。目前一共十八门课，全部免费，每门学完发一张官方证书，可以直接挂到LinkedIn上。注册只需要一个邮箱，不需要Anthropic账号。

十八门课分五个方向，从完全不写代码的人到做agent开发的程序员都能找到对应的内容。按三类人来说。

先说不写代码的人。

AIFluency:Framework&Foundations是最值得非技术人员先上的一门。十四节课，大概一小时出头，教的是怎么跟AI有效协作。它提了一个4D框架：委托、描述、辨别、勤勉。展开讲的是怎么给AI布置任务、怎么把你想要的描述清楚、怎么判断AI给的结果靠不靠谱、怎么保持对输出质量的把控。如果你天天在用Claude但觉得用得不够好，这门课值得花一小时走一遍。

Claude101更基础，讲Claude的功能和常见用法，适合完全没用过的人。AICapabilitiesandLimitations讲大模型到底能做什么、不能做什么，包括幻觉和上下文长度限制这些常见坑。

另外还有四门按场景细分的版本：给教育工作者的、给学生的、给非营利组织的、给小型企业的，都是在通用框架上叠加了具体行业的用法。还有一门TeachingAIFluency专门教老师怎么在课堂上教AI素养，附带了可以直接用的教学材料。

再说开发者。

这部分课程量最大。BuildingwiththeClaudeAPI是整个平台的重头课：八十四节课、八个多小时视频、十个测验，从认证到流式传输到工具调用到检索管道，把用API做Claude应用的全链路走了一遍。如果只有时间上一门开发课，选这门。

ClaudeCode有两门。ClaudeCode101讲基础工作流：探索、规划、写代码、提交，以及怎么在终端、VSCode、JetBrains这些环境里安装和使用。ClaudeCodeinAction进一步，十五节课一小时，讲怎么把ClaudeCode融进日常开发，包括文件操作、命令执行和GitHub集成。

MCP协议也是两门。入门课讲MCP的架构、用PythonSDK搭服务端和客户端、调试工具怎么用。进阶课讲生产环境的部署模式：采样、通知、文件系统访问、传输机制。两门都需要Python和JSON基础。

跟agent相关的有三门。IntroductiontoAgentSkills六节课半小时，教你在ClaudeCode里写Skill，就是可复用的Markdown指令，Claude会自动在合适的任务里调用它。IntroductiontoSubagents四个动手模块，教怎么把任务拆给子agent，每个子agent有独立的上下文窗口，不会污染主对话。IntroductiontoClaudeCowork讲Anthropic新出的桌面agent工具，用来做文件管理和多步骤任务的自动化。

最后说用云平台的人。

ClaudewithAmazonBedrock和ClaudewithGoogleCloudVertexAI两门课分别讲怎么在AWS和谷歌云里接入Claude。如果你们公司已经在用这两个平台，对应的课会告诉你怎么在现有架构上集成。

有一件事需要提前知道：所有课程目前只有英文，没有中文版。视频有英文字幕但没有翻译。当然这个也很容易，有太多AI工具可以翻译了。

怎么选取决于你是谁。非技术人员先上AIFluency再上Claude101。开发者想系统学Claude开发，直接上BuildingwiththeClaudeAPI。已经在用ClaudeCode的，去看AgentSkills和Subagents。对MCP感兴趣的先入门再进阶。

