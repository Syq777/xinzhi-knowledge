---
作者:
  - "阿里云开发者"
原文链接: https://mp.weixin.qq.com/s?__biz=MzIzOTU0NTQ0MA==&amp;mid=2247548288&amp;idx=1&amp;sn=8ea1b42d8c6c62edead33774b3b6bb85&amp;chksm=e839807064743b2cbce536ceb33adfca0027c41687046e65d7a5bac213e739f74b853542129b&amp;mpshare=1&amp;scene=1&amp;srcid=0410cXL1J9XzBBsLDmhR25j8&amp;sharer_shareinfo=957ae4f115c4e4b688d7507031e41038&amp;sharer_shareinfo_first=957ae4f115c4e4b688d7507031e41038#rd
发布时间: ""
收藏时间: "2025-04-10"
关联日记: "[[2025-04-10]]"
tags:
  - 文章
---
![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67f7bd0269e61d546dadaca5/df402815-3a50-410b-8427-891077059d40.jpeg)

阿里妹导读

本文分享如何基于利用MCP协议，配置MCP Server，以调用大数据开发与治理平台DataWorks Open API搭建智能体Agent，实现通过自然语言完成数据集成与数据开发等任务。文章还介绍了MCP协议的基本知识，帮助大家了解背后实现原理。大家可以通过自行配置体验数据工作流智能自动化运行。

一、前言

您是否常常为数据集成的繁琐配置而烦恼？是否因为数据开发的手撕SQL语句而头疼呢？传统的数据开发工作就像在迷宫中穿行，据统计，开发者平均每天执行137次点击操作，60%时间消耗在功能检索而非核心逻辑，效率十分低下。试想：如果能够有一个平台，通过自然语言输入就能智能化自动创建和运行数据集成和数据开发任务就好了。现在，阿里云大数据开发治理平台DataWorks的智能体Agent（基于MCP协议）即可实现这个想法，下面让我们来了解下具体实现方式吧！

二、什么是MCP？

Model Context Protocol（MCP）是人工智能领域提出的一种标准化协议框架，其全称“Model Context Protocol”直译为“模型上下文协议”。该协议的核心目标是为大模型（如超大规模语言模型、多模态模型等）提供统一的上下文接口标准，使其能够无缝连接外部数据源、工具和服务。通过标准化的数据交互规范和功能调用机制，MCP打破了传统AI系统中模型与外部资源之间的“孤岛效应”，使模型能够像调用自身内置功能一样灵活地利用外部资源。

该协议通过定义四⼤核⼼原语实现交互标准化：

1. 资源（Resources）：结构化数据⽚段，如实时⾏情数据、历史报表等，为大模型提供决策依据；

2. ⼯具（Tools）：封装的可执⾏函数，⽀持 SQL 查询、可视化渲染等专业操作；

3. 提示（Prompts）：预定义的任务指令模板，引导 LLM ⽣成符合业务规范的输出；

4. 采样（Sampling）：异步调⽤机制，允许服务器向 LLM 请求多轮推理结果。

其设计理念可类比软件开发从汇编语言到高级语言的演进，通过协议抽象降低AI应用开发门槛。

DataWorks MCP Server基本介绍

**基本架构**

DataWorks新版数据开发DataStudio的个人开发环境，在阿里云原生的能力上搭建了用户专属的开发环境，环境中内置了VSCode客户端，登录DataWorks后可通过浏览器访问，您可以选择安装MCP Client插件（如Cline），通过配置DataWorks开源的MCP Server，输入指令即可完成DataWorks的数据开发运维等动作。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67f7bd0269e61d546dadaca5/212c3367-9d13-4dbf-8f90-3c747dee57f1.jpeg)

**基本概念**

- DataWorks个人开发环境：DataWorks提供的云原生开发环境，一个用户专属可控的安全的操作系统。
- alibabacloud-dataworks-mcp-server：DataWorks开源的MCP Server，实现了DataWorks OpenAPI的封装。
- DataWorks OpenAPI：DataWorks各模块提供的开放API，支持用户完成对DataWorks上资源的管理。


如上图所示，个人开发环境本质上是用户在DataWorks上创建出来的一台服务器，除了DataWorks的开发运维，还能安装开源生态的各种插件，比如：

- 通过filesystem实现对文件的读写操作。
- 通过git实现对Git工作空间的git操作。


不局限于此，还可以添加各种开源的mcp servers到个人开发环境。

DataWorks智能体Agent是什么？

阿里云大数据开发治理平台DataWorks基于MCP协议搭建的DataWorks 智能体Agent，内置 DataWorks MCP Server V1.0，支持在DataWorks Data Studio中通过自然语言交互来自动化操作DataWorks上的产品功能，完成数据集成、数据开发等一些复杂的操作，使得Data Studio平台实现了从"工具操作"向"语义理解"的演进。

DataWorks Agent ，现已支持将 DataWorks 数据集成、数据开发、任务运维相关的OpenAPI作为Tools的DataWorks MCP Server，可为开发者提供智能Agent服务，开发者无需再到平台UI中到处查找功能界面，给出自然语言指令即完成相关工作，“所言即所得”，大大提升了工作效率和体验。

DataWorks Agent 核心功能

DataWorks Agent当前支持通过自然语言指令自动化创建和启动实时/离线数据同步任务，一键查看同步任务配置信息和执行概况；支持快速批量创建和修改数据开发节点，避免了用户繁琐重复的机械性操作；支持运行任务的智能分析，针对需要重跑的任务自动化执行重跑操作，有效提升任务运维的效率。

现在，DataWorks Agent正全面推进面向数据开发、数据治理、任务运维等场景应用能力的上线，未来，DataWorks将具备开发者通过使用自然语言即可完成数据开发与治理全链路的能力，真正进入数据开发与治理的新纪元。

如何配置DataWorks MCP Server

### 1、没有个人开发环境

- 安装并启动个人开发环境实例，镜像选择dataworks-mcp:py3.11-ubuntu22.04


参考地址：https://help.aliyun.com/zh/dataworks/user-guide/serveride/#a47aea58f20q0?utm_content=g_1000403230

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67f7bd0269e61d546dadaca5/85e8f76a-a073-46cf-9d66-d40bc9c25769.png)

安装并启动个人开发环境实例

### 2、已有个人开发环境升级

- 打开terminal，执行以下脚本：


![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67f7bd0269e61d546dadaca5/bb43235f-b7f1-4e5a-b034-b966a43982c6.png)

```
wget https://nodejs.org/dist/v20.19.0/node-v20.19.0-linux-x64.tar.xz
tar xf node-v20.19.0-linux-x64.tar.xz
mv /etc/dsw/node /etc/dsw/node14
mv node-v20.19.0-linux-x64 /etc/dsw/node

bash <(curl -s https://dataworks-notebook-${REGION}.oss-${REGION}.aliyuncs.com/public-datasets/aone-release/dwcode-server/scripts/update.sh)  0.2.169
```

- 刷新页面后，从VSCode的应用市场搜索Cline进行安装


![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67f7bd0269e61d546dadaca5/1a5f57c8-bedb-4606-9417-ec1bdf6986f9.png)

### 3、配置LLM APIKey，支持您配置使用不同的LLM模型（此处以阿里云百炼的API为例）

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67f7bd0269e61d546dadaca5/d5c64ecf-0558-44c3-b052-393a14728418.png)

完成模型配置。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67f7bd0269e61d546dadaca5/be3732ca-622d-4cf0-ac0e-fa4ae2feaf44.png)

### 4、安装MCP Servers

#### 通过界面打开DataWorks MCP Server的配置界面-Configure MCP Servers。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67f7bd0269e61d546dadaca5/5968d102-9fe6-4f20-bd18-60133831b4ca.png)

在配置界面填入如下配置，注意修改其中的REGION信息：

```
{
  "mcpServers": {
    "alibabacloud-dataworks-mcp-server": {
      "command": "npx",
      "args": [
        "alibabacloud-dataworks-mcp-server"
      ],
      "env": {
        "REGION": "cn-beijing",
        "ALIBABA_CLOUD_CREDENTIALS_URI": "http://localhost:7002/api/v1/credentials/0",
        "TOOL_CATEGORIES": "SERVER_IDE_DEFAULT"
      },
      "disabled": false,
      "autoApprove": [],
      "timeout": 60
    }
  }
}
```

看到如下加载成功的Tools可确认alibabacloud-dataworks-mcp-server已安装成功：

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67f7bd0269e61d546dadaca5/d34e3796-850c-4e47-ad35-7336884168b4.png)

在任务界面，您可以输入“我有哪些工作空间？”开始测试

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67f7bd0269e61d546dadaca5/26346eca-9e16-4c5c-8496-dfcc78ac2696.gif)

#### 进阶玩法：安装其他MCP Servers进行探索

您可以参考mcp-servers安装其他的MCP Servers到个人开发环境。参考地址：https://github.com/modelcontextprotocol/servers/

实操演示

目前，DataWorks Agent支持安装并启用应用市场的多种MCP Server，接下来我们以Hologres MCP Server为例，演示如何使用DataWorks Agent实现为Hologres数据源设置实时数据同步任务，并在完成数据同步的基础上对Hologres的数据进行查询和分析。

目前，参与DataWorks Data Studio新版公测即可使用DataWorks Agent，欢迎使用DataWorks产品进行体验！

点击阅读原文开始体验吧～

