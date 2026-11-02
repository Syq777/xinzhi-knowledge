---
作者:
  - "DeepNoMind"
原文链接: https://mp.weixin.qq.com/s?__biz=MzU2MTgxODgwNA==&amp;mid=2247492612&amp;idx=1&amp;sn=cb97e081661165250888e775b71ea7bc&amp;chksm=fdc5e8c5dcadfcd4f76ff1f12f3a5d43508beaa046b96d852489b565369ffc1f2698e6b1c7a0&amp;mpshare=1&amp;scene=1&amp;srcid=0426Fssc2UAakvMFcepTWQkD&amp;sharer_shareinfo=e82aceb09e136008ee048991d1b52397&amp;sharer_shareinfo_first=e82aceb09e136008ee048991d1b52397#rd
发布时间: ""
收藏时间: "2026-04-26"
关联日记: "[[2026-04-26]]"
tags:
  - 文章
---
> *智能体化 DevOps 通过将自主 AI 智能体嵌入代码编写、构建维护和运维三个阶段，实现从需求规格到生产故障自动修复的完整闭环工作流。Azure MCP Server 让任何智能体都成为 Azure 专家，GitHub Copilot 编码智能体异步处理基础设施更新，Azure SRE Agent 自动检测、调查和修复生产故障，三者在人类监督下协同工作，彻底改变了软件构建和运维方式。原文：Agentic DevOps Is Here: How Azure MCP Server, GitHub Copilot, and SRE Agent Are Rewriting the Software Lifecycle[1]*

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/69eda9ad8800f73e4a8f8f8d/ce64226b-de12-4157-8e01-40e0ccb5d940.png)

我一直在探索 AI 智能体如何改变构建、部署和运维云应用的方式。工具正在快速成熟，相信我们已经到达了转折点。微软最近将 Azure MCP Server、GitHub Copilot 编码智能体、SpecKit 和 Azure SRE Agent 整合到统一的工作流中，覆盖了整个软件开发生命周期，从编写第一行代码到自动修复生产故障。本文将带你深入了解这个技术栈的组件，解释架构，展示每个部分如何连接，让你马上就能尝试所有功能。无论你是开发者、平台工程师还是 SRE，这里的内容都可以为你节省时间、解决麻烦。

## 什么是智能体化 DevOps？

智能体化 DevOps 代表 AI 参与软件开发生命周期的根本性转变。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/69eda9ad8800f73e4a8f8f8d/48ae8acc-4947-477a-abb4-21f5a153a6e6.png)

不要将 AI 视为编辑器中孤立的自动补全功能，智能体化 DevOps 将自主 AI 智能体嵌入三个截然不同的阶段：**代码**、**构建维护**和**运维**。

在深入工具之前，需要先理解一下三个核心理念：

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/69eda9ad8800f73e4a8f8f8d/94e21f1c-8be7-4125-a1bb-6ce6616db84b.png)

**从 AI 增强转向 AI 原生。** 不是将 AI 作为次要功能硬塞到现有工具上，而是将智能体直接嵌入工作流、IDE、仓库和运维仪表盘中。它们理解 Azure 上下文、订阅资源、部署目标和故障响应流程。

**提升整个生命周期的生产力。** 生产力提升不仅限于代码生成，而是延伸到基础设施配置、异步代码审查、Pull Request（PR）生成、故障检测、根因分析和修复。

**加速 AI 应用和智能体的交付。** 当开发工具本身就是 AI 原生时，构建 AI 驱动的应用会显著加快，因为工具理解正在部署到的 AI 服务。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/69eda9ad8800f73e4a8f8f8d/82f90d70-f46e-4172-8859-6f66dc9877e2.png)

为了具体说明，我们考虑以下场景：一个应用使用 SpecKit 从规格构建，部署到 Azure Container Apps，被 PagerDuty 检测到生产故障，由 Azure SRE Agent 使用 Datadog 遥测数据自动分诊和缓解，然后长期修复作为 GitHub issue，由 GitHub Copilot 编码智能体接手，通过更新基础设施即代码的 Pull Request 解决。所有这些都在最小人工干预下发生。下面分解每个部分。

## 架构：全闭环智能体工作流

在深入单个工具之前，先看看每个组件如何连接成一个闭环系统。以下是流程：

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/69eda9ad8800f73e4a8f8f8d/66083ea5-dbc3-4645-9176-73ca67848fb9.png)

1. **Azure Container Apps** 托管应用。这是运行时环境。应用崩溃或开始抛出 500 错误，终结实时站点的可用性。
2. **PagerDuty** 检测到故障并创建 P1 警报。这是故障管理层。
3. **Azure SRE 智能体**接收 PagerDuty 故障并开始自主调查。SRE 智能体通过 Azure Native Integration for Datadog 和 Datadog MCP 服务器从 **Datadog** 拉取遥测数据，还可以通过 Azure CLI 拉取 Azure Monitor 日志。
4. SRE 智能体通过 **PagerDuty 子智能体**（使用子智能体构建器构建）来生成 AI 驱动的操作手册并将其附加到 PagerDuty 故障。
5. SRE 智能体执行短期缓解措施，例如扩缩 Container Apps 计划以处理 CPU 和内存压力。
6. SRE 智能体打开一个 **GitHub issue**，包含用于长期修复的完整故障上下文。配置了 **Azure MCP Server** 的 **GitHub Copilot 编码智能体**接手 issue，更新 Bicep 基础设施即代码文件，并打开一个 Pull Request。PR 经过审查、合并，基础设施与修复措施保持同步。


这是一个完整闭环：代码、部署、检则测、调查、缓解、修复和更新基础设施，全部由智能体编排，在关键决策点有人类监督。下面详细介绍每个阶段。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/69eda9ad8800f73e4a8f8f8d/6cea1e01-fa00-45b1-92a5-f3fbe383b339.png)

### 阶段 1：使用 Azure MCP Server 编写代码

Azure MCP Server 是基础组件，让任何智能体都成为 Azure 专家。MCP 代表模型上下文协议，这是一个开放标准，为大语言模型提供工具以便能与外部服务交互。Azure MCP Server 专门为 Azure 实现这个协议，为任何 MCP 兼容的智能体提供关于 Azure 订阅、已部署资源和 Azure 最佳实践的深层上下文。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/69eda9ad8800f73e4a8f8f8d/c3577d63-f2af-4d8c-ac5f-ffa714bc1c1e.png)

#### Azure MCP Server 提供什么

Azure MCP Server 向 LLM 提供四大类能力：

**Azure 上下文和资源感知。** 服务器给 LLM 访问 Azure 订阅的能力。它可以枚举已部署的资源，按区域分组，识别你在 Azure AI Foundry 中部署了哪些 AI 模型，找到存储账户 URL，并为正在工作的任何资源组提供直接链接到 Azure 门户。

**始终最新的文档和最佳实践。** 服务器始终内置最新的 Azure 文档、最新的 SDK 版本和当前最佳实践。当它生成代码时，通过 DefaultAzureCredential 使用托管身份，而不是硬编码密钥。它了解 Bicep 的 Azure Verified Modules，能够引用保护应用的最新模式。

**控制平面和数据平面操作。** MCP 服务器暴露的工具既能查询资源（控制平面），也能与它们交互（数据平面）。可以通过要求它创建一个禁用公共访问的新 Blob Storage 容器来测试这一点，智能体调用了适当的存储工具并在实时创建了容器。

**基础设施即代码生成。** 服务器通过引用 Azure Verified Modules 和当前架构定义，帮助编写 Bicep 和 Terraform 模板。它创建遵循推荐模式的 Bicep 文件，包括针对目标计算服务的托管身份配置和推荐资源设置。

#### GA 发布和覆盖范围

Azure MCP Server 现已正式发布（GA），覆盖 47 种不同的 Azure 服务，横跨资源管理、诊断、监控、计算、数据服务等。所有内容都通过 Azure Identity 保护，意味着它以通常通过开发者工具进行的方式进行身份验证。

它适用于 VS Code、Visual Studio 2026（开箱即用）、IntelliJ、GitHub Copilot 编码智能体和 Copilot CLI，也可以用它来构建自己的自定义智能体。

**Azure MCP Server GitHub 仓库：** https://github.com/microsoft/mcp

**Microsoft Learn 上的 Azure MCP Server 文档：** https://learn.microsoft.com/en-us/azure/developer/azure-mcp-server/overview?WT.mc_id=AZ-MVP-5000671

**GitHub Copilot for Azure 文档：** https://learn.microsoft.com/en-us/azure/developer/github-copilot-azure/introduction?WT.mc_id=AZ-MVP-5000671

#### 实际中的样子

下面分享一些使用 VS Code 智能体模式下的 Azure MCP Server 运行的场景：

**资源发现。** 我问"我部署了哪些 AI 模型？"，智能体调用了 Azure MCP Server 的 Foundry 能力，枚举我的资源，并返回按区域和模型类型（GPT-4 Mini、GPT-4.1 等）分组的清晰列表。仅此一点就让我在需要快速查询时不需要访问门户。

**资源创建。** 要求智能体为照片创建一个新的存储容器。它了解了可用的存储能力，调用了创建工具，并确认容器已禁用公共访问方式创建。无需门户，无需 CLI 脚本。

**最佳实践代码生成。** 要求创建 Python 脚本将文件上传到特定存储容器，包含错误处理和托管身份。智能体首先调用了最佳实践工具，然后使用带 DefaultAzureCredential 的 Azure SDK 生成代码。无硬编码密钥，无废弃模式。

**基础设施即代码。** 要求 Bicep 配置 Azure Container Apps。智能体获取了最佳实践，引用了 Azure Verified Modules，并生成了生产就绪的 Bicep。如果你更喜欢 Terraform，同样的工作流也适用。

### 阶段 1.5：使用 SpecKit 进行规格驱动开发

在跳到构建阶段之前，我想强调一个真正改变我处理新应用方式的工作流。它结合了 VS Code、GitHub Copilot、Azure MCP Server 和 **SpecKit**，这是 GitHub 上用于规格驱动开发的开源项目。

#### 什么是 SpecKit？

SpecKit 帮助你创建为 LLM 工作优化的结构化规格。与其输入模糊提示词并希望智能体能理解你的意思，不如通过结构化过程定义想要构建的内容，然后智能体生成忠实遵循该规格的代码。

以下是关键命令及其功能：

**Constitution（/speckit.constitution）**：这是为项目定义不可协商原则的地方，可以把它想象成架构护栏。在我的案例中，指定了：始终使用 Azure MCP Server，始终检查最佳实践，托管在 Azure Container Apps 中，始终使用托管身份，使用 Microsoft Agent Framework 构建 AI 智能体。Constitution 命令将这些简短语句扩展为智能体能遵循的详细、结构化指令。

**Specify（/speckit.specify）**：这是描述想要构建什么的地方。我描述了一个健身工作室查找网站，包含类别、教练、工作室、一个推荐 AI 智能体和基本页面导航。SpecKit 将其扩展为详细的用户故事和功能规格。

**Clarify（/speckit.clarify）**：这是我最喜欢的功能。规格生成后，Clarify 对照 constitution 和所有现有上下文分析，识别歧义或缺失信息，并提出针对性问题。例如，它询问了教练与位置之间的关系，以及如何处理性能需求失败。每个答案都会自动更新规格。仅此一步就防止了你和智能体之间的大量误解。

**Plan（/speckit.plan）**：创建技术实现计划，根据 constitution 和需求选择特定技术。

**Tasks（/speckit.tasks）**：将工作分解为检查点，有机会在每个阶段审查、本地测试和引导实现。

#### 结果

使用这个工作流，我构建了一个功能完整的健身工作室网站，具有可浏览的工作室、教练资料、详情页面以及一个能根据活动偏好推荐教练的集成 AI 智能体。我没有手写一行代码，整个应用通过需求引导从规格生成。当智能体走到部署步骤时，它从我的 constitution 知道使用 AZD（Azure 开发者 CLI），所以创建了所有 Bicep 模板并为部署准备了一切。

**SpecKit GitHub 仓库：** https://github.com/github/spec-kit

**VS Code 的 Azure 工具扩展包：** 此扩展包包括 Azure MCP Server 以及 App Service、Functions、Container Apps 等的所有 Azure 扩展。它保持更新，所以你始终拥有最新工具。

### 阶段 2：使用编码智能体构建和维护

GitHub Copilot 编码智能体异步运行，就像团队中的另一个开发者。你将 GitHub issue 分配给它，它在仓库中独立工作，生成供审查的 Pull Request。

#### 将编码智能体连接到 Azure

这里的关键推动器是 Azure 开发者 CLI 的 `azd coding-agent config` 命令。此命令自动在 GitHub Copilot 编码智能体和 Azure MCP Server 之间建立安全连接。它在你的 Azure 订阅中创建托管身份，为 GitHub Actions 配置联合凭据，并提供一个 JSON 片段让你粘贴到仓库的 Copilot 编码智能体设置中。

配置后，编码智能体能访问你在 VS Code 中使用的相同 Azure MCP 工具。可以指定它能访问哪些工具，还可以创建具有特定指令和提示配置的自定义智能体。我创建了一个"Azure 智能体"，它知道始终使用 MCP 工具，并为项目提供了定制提示词。

**将 Copilot 编码智能体连接到 Azure MCP Server：** https://learn.microsoft.com/en-us/azure/developer/azure-mcp-server/how-to/github-copilot-coding-agent?WT.mc_id=AZ-MVP-5000671

**Azure 开发者 CLI 编码智能体扩展：** https://learn.microsoft.com/en-us/azure/developer/azure-developer-cli/extensions/copilot-coding-agent-extension?WT.mc_id=AZ-MVP-5000671

#### 如何使用

我在仓库中为生成示例数据、添加新 API 端点或更新基础设施等任务创建 issue。我将 issue 分配给自定义 Azure 智能体，编码智能体开始在后台异步工作。当它完成时，我会收到一个供审查的 Pull Request。这解放了我，让我专注于架构和设计决策，而智能体处理实现工作。

异步模型很重要，因为这意味着编码智能体可以并行处理例行任务、基础设施更新和样板工作。

### 阶段 3：使用 Azure SRE 智能体运维

这是技术栈真正强大的地方。Azure SRE 智能体是专为站点可靠性工程设计的 AI 驱动服务，能够自动化故障响应，用遥测数据增强工单，并能在你批准下执行缓解措施。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/69eda9ad8800f73e4a8f8f8d/37772d9e-449b-45b7-b383-36691b5d1060.png)

#### 为什么存在这个功能

如果你曾经在凌晨 2 点被叫醒去检查仪表盘，等待图表回落，然后再去睡觉，就知道 SRE 智能体能够解决的问题。运维大规模 Azure 基础设施的团队面临巨大的工单量。单个工单可能需要几分钟到几小时的手动分诊，需要查询五个不同的界面，从多个来源关联日志，在开始修复之前弄清楚发生了什么。

SRE 智能体已被微软工程师内部使用了九个月。从这种内部使用中学到的关键教训很清楚：工程师不想要一个取代他们的黑盒，而是想要助手，通过自动化故障响应的重复部分来帮助他们，同时保持对流程的控制。内部使用显示 95% 的智能体发起解决方案，意味着智能体监听传入的工单并开始自主调查和修复。

#### 关键功能

**子智能体构建器。** 这是直接来自客户反馈的功能。你可以构建自己的子智能体，覆盖特定类型故障的默认行为。每个子智能体都有自定义指令、交接规则和特定工具集。例如，我构建了一个 Datadog 子智能体，使用 Datadog MCP 服务器工具获取日志、指标和跟踪，以及一个 PagerDuty 子智能体，生成操作手册并管理故障生命周期。你完全控制故障响应的发生方式。

**MCP 服务器支持。** SRE 智能体现在支持消费任何拥有 MCP 服务器的第三方工具的数据：Dynatrace、New Relic、Datadog 等。这很关键，可以在不迁移可观测性技术栈的情况下，就能满足需求。

**计划任务。** SRE 智能体可以按定义的计划运行任务，从而主动介入而不仅仅被动响应。我设置了一个计划任务，在缓解后每五分钟查询 Datadog 日志两次小时，以验证修复是否有效。你还可以在每周发布窗口后运行健康扫描。

**知识库上传和 Azure DevOps Wiki 集成。** 可以将文档上传到 SRE 智能体的知识库或将其直接连接到 Azure DevOps 开发者 wiki。这让智能体能访问组织内关于如何处理特定类型故障的制度知识，使其越来越智能。

**调试跟踪视图。** 在构建子智能体时，你可以使用调试跟踪视图在测试环境中测试和改进提示词，然后再部署到生产环境。这对于在智能体接触真实故障之前正确调整智能体行为至关重要。

**智能体间集成。** SRE 智能体与 PagerDuty 和 New Relic 等供应商集成，用于跨云的故障管理工作流。

**Azure SRE 智能体概览：** https://learn.microsoft.com/en-us/azure/sre-agent/overview?WT.mc_id=AZ-MVP-5000671

**Azure SRE 智能体故障管理：** https://learn.microsoft.com/en-us/azure/sre-agent/incident-management?WT.mc_id=AZ-MVP-5000671

**创建和使用智能体：** https://learn.microsoft.com/en-us/azure/sre-agent/usage?WT.mc_id=AZ-MVP-5000671

**使用 SRE 智能体和 Azure Container Apps 进行故障排查：** https://learn.microsoft.com/en-us/azure/sre-agent/troubleshoot-azure-container-apps?WT.mc_id=AZ-MVP-5000671

**SRE 智能体计费：** https://learn.microsoft.com/en-us/azure/sre-agent/billing?WT.mc_id=AZ-MVP-5000671

**SRE 智能体常见问题：** https://learn.microsoft.com/en-us/azure/sre-agent/faq?WT.mc_id=AZ-MVP-5000671

## 完整故障生命周期实战

下面我带你了解所有这些如何在真实场景中连接。

**设置：** 应用在 Azure Container Apps 上运行，并开始在其中一个端点上抛出 500 错误。PagerDuty 检测到故障并创建 P1 故障。Azure Native Integration for Datadog 将应用级和基础设施级日志都流转到 Datadog。Datadog MCP 服务器和我的 PagerDuty 子智能体已在 SRE 智能体中配置。

Datadog 的 Azure Native Integration 的新门户面板现在允许你直接从 Datadog 集成页面启用 SRE 智能体及其关联的 MCP 服务器，你可以选择 SRE 智能体并直接在那里添加 MCP 服务器，这大大简化了设置。

**PagerDuty 子智能体生成操作手册。** 使用 SRE 智能体聊天中的 @agent 命令，调用 PagerDuty 子智能体并要求它为我的特定故障 ID 生成操作手册并找到分派人员。子智能体生成综合操作手册，包含分步故障排查、缓解步骤、缓解后验证、回滚指导和分派人员。无需额外提示，它就会将此操作手册附加回 PagerDuty 故障，为它自己和其他响应者提供上下文。

**Datadog 子智能体获取遥测数据。** 在单独线程中，Datadog 子智能体检索与 PagerDuty 故障相关的所有 Datadog 日志。它向我显示 500 错误和请求数据，然后提议设置一个计划任务，每五分钟查询 Datadog，以监视复发错误。此验证循环确保 SRE 智能体应用的任何修复确实有效。

**自主缓解。** SRE 智能体确认 PagerDuty 故障，使用 Azure CLI 搜索 Container App 日志，发现过去 30 分钟的 500 错误，运行关联分析以识别相关问题，生成错误模式可视化，并确定需要扩缩 Container Apps 计划以处理 CPU 和内存压力。执行扩缩命令后，它搜索关联的 GitHub 仓库中与此更改相关的基础设施即代码文件。它找到相关 Bicep 文件并打开一个包含完整故障上下文的 GitHub issue：PagerDuty 故障 ID、订阅信息、Azure 实时日志以及长期修复的具体建议。

**Copilot 闭环。** 该 GitHub issue 被分派给 GitHub Copilot 编码智能体。因为编码智能体配置了 Azure MCP Server，它接手 issue，开始会话，使用 MCP 服务器获取 Bicep 架构，更新基础设施即代码以匹配修复，并打开一个 Pull Request。我审查并合并 PR，基础设施定义现在与修复措施同步。

闭环完成。

## 今天就开始

上面涵盖的所有内容现在就可用。以下是参考链接：

**Azure SRE 智能体：** https://learn.microsoft.com/en-us/azure/sre-agent/?WT.mc_id=AZ-MVP-5000671

**Azure MCP 服务器文档：** https://learn.microsoft.com/en-us/azure/developer/azure-mcp-server/overview?WT.mc_id=AZ-MVP-5000671

**Azure MCP 服务器（GitHub）：** https://github.com/microsoft/mcp

**SpecKit（GitHub）：** https://github.com/github/spec-kit

**将 Copilot 编码智能体连接到 Azure MCP 服务器：** https://learn.microsoft.com/en-us/azure/developer/azure-mcp-server/how-to/github-copilot-coding-agent?WT.mc_id=AZ-MVP-5000671

**VS Code 的 Azure AI 工具包：** https://learn.microsoft.com/en-us/azure/ai-studio/?WT.mc_id=AZ-MVP-5000671

**Visual Studio 2026 中的 Azure MCP 服务器：** https://learn.microsoft.com/en-us/azure/developer/azure-mcp-server/how-to/visual-studio?WT.mc_id=AZ-MVP-5000671

## 最终思考

我在 Azure 上构建了很久，可以告诉你，我们现在看到的不仅仅是又一个增量工具更新，而是软件构建和运维方式的真正转变。

想想我描述的工作流实际上意味着什么。你写下想要构建的内容的简短描述，一个智能体将其变成完整规格，向你询问问题来填补空白，生成内置安全最佳实践的生产就绪代码，部署，然后在生产环境中监控。当出现问题，另一个智能体检测到问题，从可观测性平台拉取日志，编写操作手册，修复即时问题，并为长期解决方案打开工单。第三个智能体接手该工单，更新基础设施即代码，并提交供审查的 Pull Request。你在每一步中都可以进行控制，但繁琐、重复、易出错的工作都为你处理了。

最让我兴奋的部分是可扩展性。MCP 协议意味着这不会锁定单一供应商。如果团队使用 Datadog，可以插入 Datadog MCP 服务器。如果使用 Dynatrace 或 New Relic，也可以。子智能体构建器意味着编码了团队知识和流程，而不是别人的通用剧本。SpecKit 的 constitution 意味着架构标准随每个项目、每个智能体、每个 Pull Request 一起演进。

你可以选择这个技术栈的一部分，在真实项目上试用，亲眼看看。可以从 VS Code 中的 Azure MCP 服务器开始，快速获得反馈。如果团队被运维琐事淹没，就设置 SRE 智能体。如果厌倦了 AI 智能体构建错误的东西，就试试 SpecKit。

参考资料

[1] 

Agentic DevOps Is Here: How Azure MCP Server, GitHub Copilot, and SRE Agent Are Rewriting the Software Lifecycle: *https://medium.com/codex/agentic-devops-is-here-how-azure-mcp-server-github-copilot-and-sre-agent-are-rewriting-the-0a9d18632a28*

