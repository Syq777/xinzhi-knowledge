---
id: "fa9db68ea267e9ea"
标题: "从个人生产力到组织能力：LoongSuite-Pilot×SLS 的 AI Coding 度量实践"
主题: "Harness · ClaudeCode · AICoding"
方向: "纵向"
深度: "D3-深度候选"
关键词: ["Agent架构", "Skills", "AI编程", "工具调用"]
分类状态: "自动初分-待复核"
主题来源: "现有目录"
正文有效字数: 11435
tags: ["文章分类", "方向/纵向", "深度/D3-深度候选", "关键词/Agent架构", "关键词/Skills", "关键词/AI编程", "关键词/工具调用"]
原文: ["[[新枝/文章/05_Harness_ClaudeCode_AICoding/04_AI_Native研发实践/🔗 · 从个人生产力到组织能力：LoongSuite-Pilot×SLS 的 AI Coding 度量实践/🔗 · 从个人生产力到组织能力：LoongSuite-Pilot×SLS 的 AI Coding 度量实践]]"]
主题页: "[[新枝/知识全景/主题/Harness · ClaudeCode · AICoding]]"
---

# 从个人生产力到组织能力：LoongSuite-Pilot×SLS 的 AI Coding 度量实践

围绕具体对象或问题展开；正文识别到机制解释、具体案例、方法步骤、边界权衡、验证证据。

> 自动分类用于导航；D3 是精读候选，不代表论证已核实。正文图片未做 OCR，图片承载内容可能低估。

主题：[[新枝/知识全景/主题/Harness · ClaudeCode · AICoding]]

关键词：[[新枝/知识全景/关键词/Agent架构|Agent架构]] · [[新枝/知识全景/关键词/Skills|Skills]] · [[新枝/知识全景/关键词/AI编程|AI编程]] · [[新枝/知识全景/关键词/工具调用|工具调用]]

## 原文

- [[新枝/文章/05_Harness_ClaudeCode_AICoding/04_AI_Native研发实践/🔗 · 从个人生产力到组织能力：LoongSuite-Pilot×SLS 的 AI Coding 度量实践/🔗 · 从个人生产力到组织能力：LoongSuite-Pilot×SLS 的 AI Coding 度量实践]]

## 初评证据

- **机制解释**：line." 报告引入了 J-Curve（先降后升曲线）概念来解释机制：团队在采纳 AI 工具的初期会经历一段生产力下降期 —— 工作流适配、习惯切换、prompt 调优都是学习成本 —— 只有度过这段谷底，并把回收的 capacity 重新投入减少
- **具体案例**：it to the business." 报告给出了一组模型数据：以一个 500 人工程团队为例，AI 工具年投入约 $8.4M，预期回报 $11.6M，首年 ROI 约 39%。但这个收益并不是自动兑现的。DORA 明确指出，coding speed 的提升不会自动转化为组
- **方法步骤**：才意味着 AI Coding 正在从个人扩散为组织的共同能力。 实现这个判断的关键是用 window function 排名后按百分位切桶： ``` user_token AS ( SELECT a.user_id, sum(a.total_
- **边界权衡**：conventions 是业界公认的起点，但社区标准天然需要兼顾广泛适用性与长期稳定性，当前仍处于 Development 状态。而实际业务中 AI Agent 的调用链往往远比“单用户 × 单模型”复杂，一个请求可能跨越多个 Agent 的协同调用。
- **验证证据**：工具年投入约 $8.4M，预期回报 $11.6M，首年 ROI 约 39%。但这个收益并不是自动兑现的。DORA 明确指出，coding speed 的提升不会自动转化为组织产出： "Initial gains in coding speed are

修订方式：在 `分类修订.json` 中以 `fa9db68ea267e9ea` 为键填写需要覆盖的字段，再运行生成脚本。不要直接修改生成卡片，以免下次覆盖。
