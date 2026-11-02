---
作者:
  - "TesterHome社区"
原文链接: https://mp.weixin.qq.com/s?__biz=MzkxMDM1NDQ0OA==&amp;mid=2247520473&amp;idx=1&amp;sn=8913ceef3f8796b06df5aa6ff203896a&amp;chksm=c08056ea86cfc4d4c32939e613f5d85e7ec6790cd15a09663b14577285ecfab1460488b74fe2&amp;mpshare=1&amp;scene=1&amp;srcid=03273j7xihS6l7ks9Bsncyyb&amp;sharer_shareinfo=612c365d74c3f85f74d38d9319477fc9&amp;sharer_shareinfo_first=612c365d74c3f85f74d38d9319477fc9#rd
发布时间: ""
收藏时间: "2025-03-27"
关联日记: "[[2025-03-27]]"
tags:
  - 文章
---
![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67e4d0ec550f8e59d94f8eb2/c77c517c-1d16-440a-b756-c7ffca30cb62.webp)

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67e4d0ec550f8e59d94f8eb2/7bc1aa63-c7b5-409f-a1e3-b0d7d41a752f.webp)

**来源｜**TesterHome社区

**作者（ID）｜**亦攸

## 先看最终成果

本篇文章将介绍一下几个AI赋能的场景的实践：

AI 赋能需求文档产生测试用例：

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67e4d0ec550f8e59d94f8eb2/55c60a28-11dc-413f-8a22-130ceb912839.png)



![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67e4d0ec550f8e59d94f8eb2/06da470e-557b-4262-86c1-a8f87f1fcd0c.png)

AI 赋能自动化：

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67e4d0ec550f8e59d94f8eb2/4aaf87a6-458a-41b9-9ced-0f0c8437bba9.png)

## 前言

大家好，上次发出的文章：[专栏文章 《质量保障系统的落地实践 (七)-AI 落地&指标评估》](https://mp.weixin.qq.com/s?__biz=MzkxMDM1NDQ0OA==&mid=2247520313&idx=1&sn=ce838121670b5e4368582612720748e0&scene=21#wechat_redirect)收到了一些同学们的留言反馈，大家讨论比较集中的点在于：**若是需要将测试点一一录入，再生成测试用例，是否真的提效？**或者说的更直接一些，**AI 编写测试用例是否有用？**

**就我所在团队使用的AI模型所产出的测试用例，占比能达到30%-40%。并且生成的内容可用性也较高，但是不可避免的是测试人员需要对AI生成的测试用例进行润色。这部分手动工作无法被省略的根本原因在于：AI并不清楚业务的上下文**，所以他能做的，只是尽可能丰富你给出的测试场景派生出的测试用例，**弥补上下文的不足则是测试人员的核心竞争力，也是测试人员很难被AI完全替代的护城河**。

有了这个基本观点，再回头看 AI 编写测试用例是否有用这个问题，就不难回答了，**AI替代不了测试人员**，**AI只能赋能测试人员**，**一定程度上解放测试人员**。

## AI赋能左移与右移的可行性分析

[上一篇文章中](https://mp.weixin.qq.com/s?__biz=MzkxMDM1NDQ0OA==&mid=2247520313&idx=1&sn=ce838121670b5e4368582612720748e0&scene=21#wechat_redirect)，介绍了AI赋能中的一块内容：编写测试用例。那么AI还能在别的环节中赋能测试岗位吗？是有的，还是以我当前的实际项目为例，与大家分享。

我们先回到这张图：

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67e4d0ec550f8e59d94f8eb2/b9e0f86c-b803-4db6-a959-1dc90eab8642.png)

测试人员的工作流程一般可以归为上图的阶段，每个阶段各有各的产出：需求阶段的产出是需求文档，交互阶段的产出是交互文档/设计稿等等。目前已经实现了**AI 赋能测试用例**的功能，那么比较自然地能考虑到 AI 能否进行**左移**、**右移**？答案是可以的。

首先，产品经理产出的需求文档，设计师产出的交互文档/设计稿是为了描述清楚需求的场景以及页面关联，前后端开发产出的技术文档是为了描述需求背后的技术细节。以上的内容到了测试人员这，测试人员要做的就是从这些资料中提取出测试场景，基于提炼后的测试场景，手动编写测试用例。

而现在已经实现了 AI 基于测试场景编写测试用例的功能：

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67e4d0ec550f8e59d94f8eb2/341346a1-97a9-4fdb-80e3-e3787c588793.png)

那么只要考虑如何**将这几份材料的内容提取成测试场景**，是不是就可以实现**AI 赋能左移**？

等到项目发布后，测试人员需要补充自动化脚本，对于脚本的编写，尽管场景、接口不同，但是大体上编写格式是一致，是可以**抽象出一定的规则**，以我司的 RobotFramework 为例：

api 层：

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67e4d0ec550f8e59d94f8eb2/c4ad6728-bf2b-4743-ad87-85a1358b5773.png)

关键字层：

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67e4d0ec550f8e59d94f8eb2/b2f75214-d210-455e-ac47-efbd61475eaa.png)

TC层:

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67e4d0ec550f8e59d94f8eb2/9848c032-0ea4-4239-83ec-6bf7f149e724.png)

以上的每一层都可以抽象成这样的模板，然后动态生成。而这种**相对复杂 (可清楚描述)，规则明确**的部分，就很适合AI来执行。

至于最后**业务文档的沉淀**，基本上是记录**需求核心测试点**，**核心逻辑**，而这些内容其实在测试场景的梳理过程中已经输出了，只是在测试过程中没有沉淀下来，需要后期去补充，而这一部分也完全可以通过非手工的方式实现。
至此**AI 赋能右移**的可行性也分析完成了。

## AI赋能左移 - 需求文档

测试人员在阅读需求文档的过程中，主要做了几件事：

1、过滤无效描述，如需求背景、需求目标、版本说明等信息；

2、提取有效正文，如功能点的描述、表单描述、附件等信息；

3、基于有效正文梳理测试点；

4、基于测试点，生成测试场景。

而这个过程是可以交付AI执行的，因为这些流程可以通过语言描述，使得 AI 理解我们的目的 (当然，也要选择合适的 AI 模型)。

我司的需求文档以语雀维护，通过语雀的api，可以拿到整篇文章的 html 结构。接下来我们只需要描述清楚 prompt，就可以交付 AI 帮助我们提炼测试场景：

```
1. 从HTML文档中，仅提取标题为"需求说明"板块下的所有正文内容。                           #过滤无效描述
2.排除其他标题下的任何正文内容，不对其进行分析。                                              #过滤无效描述
3.如果在"需求说明"板块内遇到表格：
    -忽略表格的第一行（通常是表头）。                                                                #过滤无效描述
    -提取表格的第一列和最后一列的内容，作为正文内容的一部分。                            #提取有效正文
4.基于提取到的正文内容，尽可能详尽地分析出以下信息：                                        #梳理测试点、生成测试场景
    -"需求测试点"：根据内容总结出的需求关键点。
    -"测试场景"：为每个需求测试点设计具体的测试场景，按次序分点列出，格式如下：
        1.测试场景1：......
        2.测试场景2：......
        3.测试场景3：......
        多个场景之间换行展示）
5.将每个"需求测试点"及其对应的"测试场景"按照以下格式组织成一个JSON对象：           #格式化输出
    -{"name":"需求测试点","description":"测试场景"}
6.将所有生成的JSON对象append至一个数组中。
7.支持分段输出：如果内容较多，可以分段输出，但每段输出的内容前后不要加任何分割符，确保最终拼接后是一个完整的、标准的JSON数组，内部不包含其他内容。
8.最终仅返回该数组内容，输出结果不使用```json及```包裹，输出结果需为标准JSON格式。
```

那么为什么要以这样的格式：{"name": "需求测试点", "description": "测试场景"}输出呢？那是出于**体系化的考虑**，需求文档中提炼出的测试场景完全可以用于生成**初版测试用例**，注意，这里说的是**初版**，结合上已经实现了的测试场景生成测试用例的功能：

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67e4d0ec550f8e59d94f8eb2/6de50a1f-ad36-4e03-b468-7e357015f2e1.png)

只需要 for 循环这个 AI 返回的数组内容，就可以直接渲染出一个测试场景表单：

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67e4d0ec550f8e59d94f8eb2/dbdb85e4-ab26-4330-8ba7-0d3095236288.png)

这样一来，就直接打通了**AI 解析需求文档**与**AI 基于测试场景生成测试用例**两个功能之间的壁垒。

## AI赋能右移 - 业务文档

既然 AI 解析需求文档的功能已经实现了，测试点也被梳理了，其实只要在这个阶段，将这些内容保存下来，就可以作为**初版业务文档**，注意，还是**初版**。

我司使用语雀维护业务文档，所以使用对应的 api 创建业务文档：

```
# 封装业务文档信息
document_body =""
forindex,child_descriptioninenumerate(child_descriptions):
    try:
        name=child_description["name"]
        description=child_description["description"]
        mark_uuid=child_description.get("mark_uuid",None)
    exceptKeyError:
        continue
    document_body+=f"### {name}\n{description}\n\n\n\n"

document_data=createDocument(group_login,book_slug,root_description,document_body)
doc_slug=document_data["slug"]
document_url=f"{YUQUE_HOST}/{group_login}/{book_slug}/{doc_slug}"

updateDocument(group_login,book_slug,doc_slug,root_description,document_body)
```

若是手动修改了测试场景，也需要同步至业务文档中：

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67e4d0ec550f8e59d94f8eb2/d81605bb-e69c-4351-b5eb-2d65bbe6f0ed.png)



![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67e4d0ec550f8e59d94f8eb2/10a2e4a0-b099-4792-8d54-0938186c1bd8.png)

## AI赋能右移 - 自动化

回到这三张图，要实现 AI 赋能自动化，实现的过程也比较简单，主要是 prompt 的描述：

api 层:

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67e4d0ec550f8e59d94f8eb2/e9c2c36d-1562-4e54-88c2-8fedf8371068.png)

关键字层：

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67e4d0ec550f8e59d94f8eb2/8245064b-2dd7-4fb6-b4b0-2c58893f6e2e.png)

TC 层：

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67e4d0ec550f8e59d94f8eb2/4e77203d-3411-430f-ae62-58d6986beedb.png)

prompt：

```
请根据以下模板和数据，生成完整的 RobotFramework测试套件，包括Keywords和TestCase部分。
数据以数组形式传入，动态生成内容，并确保后缀为-api的关键字排在最前面，其次是-keyword后缀的关键字，最后是-TC后缀的测试套件。

要求：
1、去重规则：
    -如果传入的数据中，"session别名"、"domain"、"请求方法"和"接口路径"相同，则只生成一个-api后缀的关键字。
    -该-api后缀的关键字以"session别名"、"domain"、"请求方法"和"接口路径"的组合作为唯一标识。

2、复用规则：
    -在生成-keyword后缀的关键字时，复用相同的-api后缀关键字。
    -根据"接口描述"的不同，生成多个-keyword后缀的关键字，但调用同一个-api后缀的关键字。

3、测试套件规则：
    -每个-keyword后缀的关键字都必须有一个对应的-TC后缀的测试套件。
    -测试套件的数量与-keyword后缀的关键字数量保持一致。

4、动态生成：
    -根据传入的数据，动态生成-api、-keyword和-TC后缀的关键字。

    -排序规则：
        -所有后缀为-api的关键字排在最前面。
        -其次是-keyword后缀的关键字。
        -最后是-TC后缀的测试套件。

5、模板规则：
    -在API请求模板中：
        -如果"请求方法"为Get请求（忽略大小写），使用第一套模板。
        -否则，统一使用第二套模板。
        -替换${domain}、${接口描述}、${请求方法}、${session别名}、${接口路径}为实际值。

    -在Keyword模板中：
        -替换${api请求关键字}为对应的API请求模板生成的关键字名称。
        -将数据校验部分的${接口变量名}替换为"接口参数列表"中的每个参数，并展开为多条独立的校验语句。

    -在TestCase模板中：
        -替换${接口描述}为实际值。
        -将${request_data}的构造部分展开为平铺的键值对形式（如name=、age=、gender=）。
        -替换${keyword请求关键字}为对应的Keyword模板生成的关键字名称。

6、输出格式：
    -支持分段输出：如果内容较多，可以分段输出，但每段输出的内容前后不要加任何分割符，确保最终拼接后是完整的可执行的RobotFramework文件，内部不包含其他内容。
    -禁止使用```robot及```包裹输出结果
```

我们要做的就是整理出交付给 AI 的数据结构：

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67e4d0ec550f8e59d94f8eb2/b8a1c983-790f-42e0-ac1a-efe96e34f3b4.png)

```
prompt_data =[]
prompt_item={
    "接口描述":description,
    "请求方法":method,
    "session别名":domain,
    "domain":domain,
    "接口路径":path,
    "接口参数列表":all_params_name_list
}
prompt_data.append(prompt_item)

# 封装最终的prompt
prompt=f"""
    {ci_prompt}\n
    数据：{prompt_data_}\n
    返回最终生成结果
"""
```

实现效果：

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67e4d0ec550f8e59d94f8eb2/a9fe53eb-e80c-492f-a8db-8fa4d76a8c54.png)

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67e4d0ec550f8e59d94f8eb2/7852f2f7-a640-4eda-b3b4-9f43c5d1d6ae.png)

## AI赋能左移 - 技术文档

测试人员阅读技术文档，目的更多的是确定研发的实现方案会不会有风险，如是否使用缓存，使用 ES 等技术手段，基于技术文档编写测试用例的比例不高，所以在我的实践过程中，技术文档更多的是为后续的自动化代码服务。若是写的**完善**、**规范**的技术文档 (注意，是**完善**、**规范**的技术文档)，此次需求中涉及的新增、改造接口均已列明，有了前面处理需求文档的实践，处理技术文档的方式也是类似的，编写对应的 prompt 提取出接口信息和参数信息，交付给 AI 生成自动化脚本的功能即可。

但是更多的时候，技术文档描述并不会那么详尽，那么还有没有别的方式可以获得项目周期内新增的接口呢？

以我司的实际情况为例，我司支持后端的多环境部署，每个环境内部署的代码分支不同，通过比较多环境内服务的 swagger 接口和基准环境内服务的 swagger 接口的差集，就可以获得本次需求涉及的新增接口。

这种方式也还是有一定缺陷的，比如修改的接口无法直接比对出来，需要人工介入。

## 总结

本篇文章主要讲解了AI赋能的实现思路，很多代码无法直接分享出来。但每个公司的基础能力不同，即便给出了代码，大概率也是不能复用的。

所以本篇文章更多的是分享实现思路，想要**AI 赋**能，本质上要做的就两件事：1.**这件事可以被语言清晰描述，规则明确**，prompt 可以高质量的输出；2.找到**合适的模型**。

这两件事中，更重要的是第一点，就拿我当前正在尝试的**使用交互稿生成测试用例**的功能来说，prompt 清晰描述的难度较大，原因在于交互稿的逻辑往往比较复杂，内部的元素众多，页面之间的跳转逻辑判断较多，很难通过一个比较合适的 prompt 适配各种情况的交互稿，目前还在探索。插一句题外话，能处理交互稿生成测试用例功能的视觉模型，要求比较高，目前 Qwen2.5Max 效果相对较好一些，如果各位同学有好的模型，也欢迎留言告诉我，谢谢。

最后我想说，很多同学的实践效果可能不理想，不符合自己的期望，或许只是因为没有找到合适的模型 (因为我也是在不断尝试使用不同的模型过程中，慢慢找到效果比较好的模型来实现功能的)，不断尝试新的模型或许能够带来不少惊喜。

如果觉得这篇文章对你有用，请一键三连，受累了。

**作者在TesterHome社区网站的《质量保障系统的落地实践》专栏链接：**

https://testerhome.com/topics/41867

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67e4d0ec550f8e59d94f8eb2/8b52f9f5-7f8b-44af-8659-dcd4c03ce28f.webp)

**一年一度的软件质量保障行业峰会，MTSC2025第十四届中国互联网测试开发大会，将于7月12日在上海举行，详情点击下方链接：**

[了解MTSC2025中国互联网测试开发大会议程设置！目前大会议题继续征集中！7折抢购大会门票！](https://mp.weixin.qq.com/s?__biz=MzkxMDM1NDQ0OA==&mid=2247520434&idx=3&sn=42b07e470b95101b9e093e3435959571&scene=21#wechat_redirect)

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67e4d0ec550f8e59d94f8eb2/f98ac511-b2b1-4c90-bf9c-e592e854692c.webp)

[1.招聘｜淘天集团2026届校招测试开发实习生（内推）；京东创新零售→招聘测试开发工程师](https://mp.weixin.qq.com/s?__biz=MzkxMDM1NDQ0OA==&mid=2247520434&idx=1&sn=de8ffd77ae7590e809b912809588e6ed&scene=21#wechat_redirect)

[2.全球最热门20家开源初创公司，两家中国公司上榜](https://mp.weixin.qq.com/s?__biz=MzkxMDM1NDQ0OA==&mid=2247520410&idx=1&sn=0ffde38a471c0e52905462a1a4b471f5&scene=21#wechat_redirect)

[3.测试技艺｜在AI极速发展下重塑](https://mp.weixin.qq.com/s?__biz=MzkxMDM1NDQ0OA==&mid=2247520380&idx=1&sn=05aad664c1c4bfeb4ce550dbe97df4cb&scene=21#wechat_redirect)

[4.“杭州六小龙"之群核科技--AI助力测试提效与大模型落地应用实践](https://mp.weixin.qq.com/s?__biz=MzkxMDM1NDQ0OA==&mid=2247520174&idx=1&sn=bce3fa7d14c4b32c690376d41c77c1d4&scene=21#wechat_redirect)

[5.DeepSeek R1模型本地化部署+个人知识库搭建与使用](https://mp.weixin.qq.com/s?__biz=MzkxMDM1NDQ0OA==&mid=2247519588&idx=1&sn=2b8fcc75147380ddbc3ddc71c129013b&scene=21#wechat_redirect)

[6.新书推荐｜人工智能--计算机视觉算法测试与应用指南](https://mp.weixin.qq.com/s?__biz=MzkxMDM1NDQ0OA==&mid=2247520400&idx=4&sn=99ce5041943de93ac7134e34b60fe9f9&scene=21#wechat_redirect)

