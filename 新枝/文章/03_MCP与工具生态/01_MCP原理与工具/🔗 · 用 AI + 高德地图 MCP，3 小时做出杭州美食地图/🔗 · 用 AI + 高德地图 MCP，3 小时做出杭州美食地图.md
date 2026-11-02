---
作者:
  - "阿里云开发者"
原文链接: https://mp.weixin.qq.com/s?__biz=MzIzOTU0NTQ0MA==&amp;mid=2247550987&amp;idx=1&amp;sn=f1f779ee6da4e575084605d781115519&amp;chksm=e87fbb5fb3baebaf0f50cda8e7954c5ad1af655e506491f7d7e4a95748715e04f4d0dbe24869&amp;mpshare=1&amp;scene=1&amp;srcid=0710BAI4zdz5XnCdSRv6hM7z&amp;sharer_shareinfo=b05b3b0b381ef6bfb85d3ac6e5ed60cd&amp;sharer_shareinfo_first=b05b3b0b381ef6bfb85d3ac6e5ed60cd#rd
发布时间: ""
收藏时间: "2025-07-10"
关联日记: "[[2025-07-10]]"
tags:
  - 文章
---
![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/686f108a066ea7649c557bcd/c4686203-68fd-4ff6-aa5e-2097799b8358.jpeg)

阿里妹导读

本文记录了一次从灵光一现到快速落地的 AI + 地图服务实践，通过结合 Cursor 与高德 MCP 地图服务平台，作者仅用几个小时就实现了一个可交互、可筛选、可推荐的杭州美食地图应用。

最近刷到一篇热帖，一位在阿里五年的同学总结了一份她这五年（吃的每一口记录）收集的杭州美食排行榜，为“美食荒漠”正名。也让我回忆起自己初到杭州进入团队时也曾想整理一份“美食地图”，却因种种原因而作罢。恰逢最近团队准备选团建的餐厅，于是立马把这篇帖子分享给投食官。投食官仔细调研后感慨道，“这篇文章真是太好了，如果能在地图上看到它们的位置就更好了。”

这让我萌生了为这个美食排行榜做一个杭州美食地图的想法，以便能快速地看到餐厅的位置并进行选择。实现方法上 AI coding 加高德 MCP 有没有搞头？

> 文末附源码和项目地址供大家参考和取用。

安装高德MCP server

过程参考 ：Cursor快速接入高德MCP server

https://lbs.amap.com/api/mcp-server/gettingstarted

只需准备好你的高德 key，在 cursor 上设置里如下配置即可。

```
{
  "mcpServers": {
    "amap-amap-sse": {
      "url": "https://mcp.amap.com/sse?key=您在高德官网上申请的key"
    }
  }
}
```

配置好后检查 mcpserver 的状态，如下图则是正常可用的。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/686f108a066ea7649c557bcd/015fbd11-90f1-4545-ac3b-71b98c063ab3.png)

给 AI 提需求-构建工程提示词

```
1. 在当前文件夹下进行编写项目，尽量少的创建文件，只创建必要文件。
2. 根据给定的杭州推荐的美食店，制作一份可以预览的美食地图。最终的产物使用便捷的方式呈现，如使用html进行展示。
3. 地图上标注下面每个店铺精确的位置，为每个类型的餐厅用不同的合适的图标表示。
4. 地图采用真实的杭州市地图。
5. 点击图标可显示餐厅更多信息，餐厅优势，预约电话，推荐指数等。
6. 过程中可以借助任何工具和能力实现这一目标，如 高德MCP工具。
7. 展示的店铺已给定的为准，最终给出的数据要真实可靠。
8.将下列数据，通过amp-amp-sse 的 mcpserver，制作成适配高德地图的 json 格式数据。若没有找到餐厅，不要编造数据，坐标字段设为空值即可。
餐厅数据如下：
如*：主厨团队对传统杭帮菜的解构能力堪称艺术，招牌鱼圆弹润如凝脂，黄酒鹅肝配牛小排的组合既有东方韵味又有西式巧思。景观位虽为日式下沉设计，但私密性极佳，适合重要纪念日。唯一提醒：订位时建议直接对接主理人确认细节，米其林加身后服务响应速度有提升空间。
金*厅：四季酒店的镇店之宝，时令菜单每月更新，清明前的香椿嫩芽配河虾仁、霜降后的桂花糖藕都是必尝限定。脆皮鸡的表皮酥脆度堪比艺术品，和牛炒饭的镬气十足，适合带海外友人感受中式烹饪的精细度。
八*杯：里园的孪生品牌，早期的黄鱼锅贴仍是教科书级别，但近年创新菜式如松茸酿饭口感层次稍显单薄。建议避开周末午市，工作日晚间用餐能更好体会主厨团队的匠心。
集*楼：庭院里的江南美学展，青梅鹅肝配茉莉花茶冻的创意值得点赞。近期推出的「盲盒套餐」性价比突出，适合想体验高端杭菜又怕踩雷的新客。
木*溪：宋宴主题套餐需提前三天预订，茶点与菜肴的搭配暗合二十四节气，但每道菜量控制在2-3口刚好尝鲜。特别推荐茶艺师现场点茶，宋代七汤点茶法视觉效果震撼。
桂*房：满觉陇店的露台夜景是最大卖点，桂花酿醉虾的甜度把控精准。若多人聚餐可尝试「山房九宫格」拼盘，冷热荤素搭配考究，但需注意部分创意菜式如黑松露猫耳朵口味较重。
【浙菜】
锦*湖：原乾胧汇班底升级之作，龙翔桥店的脆皮鸡改良自港式烧味，外皮的焦糖层厚度比EFC店更均匀。推荐搭配店家自酿的青梅酒，解腻效果出众。
算*挡：滨江园区的宝藏食堂，人均150可吃到现拆的蟹粉豆腐和炭烤鳗鱼。建议4人以上拼单，把招牌菜凑齐分着吃更划算。
【创意菜】
雅*：西溪湿地内的隐秘据点，荷叶包蒸东山羊是夏季限定，肉质软烂入味。划船至码头需提前预约接驳船，整体体验像私人会所。
【融合菜】
乔*：阿里园区周边的老牌宴请场所，最近推出的「数字化点餐系统」可实时查看后厨烹饪进度。推荐黑椒牛排配龙井茶汤，西式主菜与杭帮调味的结合恰到好处。
略...
```

输入“需求文档”后，cursor 会进入 Plan 模式进行规划整体设计方案。

```
已开始为你的美食地图收集真实的高德地图数据。以下是实现方案和进度说明：
实现方案
数据收集：为每个餐厅通过高德地图API检索真实的地理位置（经纬度）、地址、照片等信息。若未找到则坐标为空。

数据格式：整理为适配高德地图MCP的JSON格式，包含必要的字段（如名称、类型、坐标、推荐指数、电话、优势等）。

地图展示：最终生成一个HTML文件，使用高德地图JS API进行可视化。不同类型餐厅用不同图标，点击可弹窗显示详细信息。

文件结构：只创建必要的文件（如index.html和数据JSON），保证项目简洁。

进度说明
已完成“如*”“金*厅”真实数据检索，获取了精确坐标和相关信息。
正在依次为所有餐厅检索真实数据，确保数据可靠。
检索不到的餐厅将坐标设为空，不会编造信息。

请确认：
是否需要为每家餐厅都补充“推荐指数、预约电话、优势”等字段？如无公开数据，是否允许留空或用描述性文字？

是否需要将所有数据单独导出为JSON文件，还是直接嵌入HTML中？

如无异议，将继续批量检索并整理数据，随后生成地图预览HTML。你可随时查看进度或指定展示细节。
```

十几分钟写完“需求文档”，晚饭时间到，提给 AI 让它先写着，我们去吃饭～

AI coding-开始寻找杭州美食之旅

**调用高德 MCP Server-获取餐厅准确位置和信息**

### 第一轮-模糊查询找到候选餐厅

AI 会先调用高德 MCP Server 的 maps_text_search 方法通过模糊查询，查到候选餐厅信息。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/686f108a066ea7649c557bcd/3f56cc56-c66e-4a42-92ea-a47ebc1beb60.png)

**输入**

```
{
  "keywords": "如院餐厅 杭州",
  "city": "杭州",
  "citylimit": true
}
```

**输出**

可以看到，查出了一系列餐厅，其中有如*餐厅的基本信息，取出 id，作为下一轮的输入。

```
{
  "pois": [
    ...
    {
      "id": "B0JA5UF6R*",
      "name": "如*餐厅",
      "address": "玉泉路1*号",
      "typecode": "0501**",
      "photo": "http://store.is.autonavi.com/showpic/b08795ab6adeba25a0115d74130862**"
    }, 
    {
      "id": "B023B019A*",
      "name": "群*饭店(信*路店)",
      "address": "滨安路119*号(近信*路)",
      "typecode": "0501**",
      "photo": "http://store.is.autonavi.com/showpic/2ac9e95efffe6e27a8eda43ef82711**"
    },
    ...
  ],
  "suggestion": {
    "keywords": "",
    "ciytes": {
      "suggestion": []
    }
  }
}
```

### 第二轮-通过 id 获取餐厅详情

可以看到紧接着 AI 会调用高德 MCP Server 的`maps_search_detail`能力，通过 id 来获取餐厅详情。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/686f108a066ea7649c557bcd/a49719da-2614-4554-8bda-aab4d58d1da1.png)

**输入**

```
{
  "id": "B0JA5UF6R*"
}
```

**输出**

可以看到这里获取到了餐厅的详情信息，包含名称、经纬度、地址、照片、营业时间、评分等。

```
{"id":"B0JA5UF6R*","name":"如*餐厅","location":"120.122175,30.253356","address":"玉泉路1*号","business_area":"西湖旅游区中心片区","city":"杭州市","type":"餐饮服务;中餐厅;中餐厅","alias":"","photo":"http://store.is.autonavi.com/showpic/b08795ab6adeba25a0115d74130862a*","cost":"","opentime2":"周一至周日 11:30-14:00,17:30-21:00","rating":"4.7","open_time":"11:30-14:00 17:30-21:00","meal_ordering":"0"}
```

AI 会将高德 MCP Server 中获取的数据格式化，整理到 json 文件中，作为数据源。

**编写页面**

数据收集完后，就开始根据需求，编写代码了，通过引入高德 API 展示杭州地图，然后将上一步整理的数据引入进来，标出餐厅的位置。并且支持点击餐厅的名称，弹框展示餐厅的详情，餐厅的推荐理由。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/686f108a066ea7649c557bcd/1a33cd5c-ca8a-47ee-a4ff-ce3abc0e1a8f.png)

虽然没有关注代码具体怎么实现的，但是它就这样水灵灵的工作起来了～

但我认为我们还是需要理解 AI 写的每一行代码，对代码质量有一个评估，一方面自己能有所进步，一方面不能让 AI 自由发挥的太过，到后面一行也看不懂，改也改不动的时候，项目就崩了。自己不理解的代码，可以让 AI 为代码都加上注释，方便理解。

调试页面

AI 写完了主体页面和功能点后，预览一下，还是有挺多细节需要修改的，如名称大小、背景框样式、弹框点击关闭逻辑等，这些和 AI 沟通，说明需要修改的位置和要求即可，如果说不清的时候，可以直接截图给 AI，告诉它要改什么，理解意图上还是十分强大的。

**找素材**

但是 AI 有一点不足的是不太方便从外部直接获取资源，比如试图让 AI 自己去网上找合适的素材图标，但是失败了，它会让我去给它下载，不然它会自己画一个丑陋抽象的 SVG 图标。

实在忍不了，只能去网上找素材，可以说整个过程中，花的最多的时间就是这里了。找合适的素材，尝试下载，要收费？换一个地方找，终于是免费的了，下载下来，传到图床上，变成公网可访问的链接。

整个找素材的过程十分痛苦，如果 AI 可以自己找就好了，也许是使用的姿势不太对，还需要继续研究。

好在最终找到了一个非常棒的平台，那就是**阿里巴巴图标矢量库**，还是自家兄弟好，素材非常的全且好用，大力推荐。

地址：https://www.iconfont.cn/?spm=a313x.search_index.i3.d4d0a486a.2dff3a81XH4Q3q

**餐厅分类与筛选**

对于之前的收集的餐厅的数据，没有一个很好的分类进行表达，于是让AI 重新分析一下整个餐厅数据，结合餐厅的信息，进行分类，然后将餐厅类型与图标素材再进行一个匹配。得到一个分类好的餐厅列表，与图标的映射关系。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/686f108a066ea7649c557bcd/1dc39b31-e483-4828-9c3f-45f0dcc0137b.png)

然后就可以愉快的让 AI 结合这个分类数据，改写一下餐厅的图标啦，并且基于分类，再加上了图例列表，和筛选项的功能，方便展示，不然 100个餐厅全部展示在地图上，也不太方便小伙伴们看。

然后页面的效果如下：

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/686f108a066ea7649c557bcd/e462f8af-a976-4144-bd07-8952a5113779.png)

AI 推荐餐厅

看了地图上标注的餐厅后，才发现，离自己园区的距离都比较远，于是含泪再写一份自己团队的聚餐选点指南，让 AI 帮助推荐餐厅。

```
1. 在当前项目中进行改进，删去图例、筛选项功能。
2. 使用给出的餐厅数据，在地图上进行标注。
3. 我们的出发位置是杭州市阿里巴巴滨江园区，标注出发点位置，用星星图标表示。
4. 图标素材在 resource/icon.txt中.
5. 计算出发点到各个餐厅的位置，在地图上用线连起来进行展示。
6. 分析一下各个餐厅的优劣，离出发点的距离，交通方式，和所需时间，周边配套，列在餐厅详情里。
7. 最后进行一个智能总结，推荐一个餐厅
8.
9. 过程中可以借助任何工具和能力实现这一目标，如 高德MCP工具。
10. 展示的店铺已给定的为准，最终给出的数据要真实可靠。

将下列数据，通过amp-amp-sse 的 mcpserver，制作成适配高德地图的 json 格式数据。若没有找到餐厅，不要编造数据，坐标字段设为空值即可。
1. 海*捞中南乐游城店
2. 黄*海鲜大排档（长河地铁站旁）
3. 群*饭店
4. 龙*·滨江烤全羊(杭州总店)dong'da
5. 东*方保利时光里店
```

有了前面的基础，这次 20 分钟就搞定了，主要在写需求文档和微调页面样式上，可以分析一下各个餐厅的优劣，离出发点的距离，交通方式，和所需时间，周边配套等。 最后进行一个智能总结，推荐一个餐厅，效果如下：

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/686f108a066ea7649c557bcd/10d7bc24-2896-4ece-9956-fa4dc8ad7107.png)

小伙伴们就可以愉快的进行决策，到底选哪个餐厅了～

新的功能正在和我们投食官持续优化中，比如先选择团建地方，再选择聚餐地方，多个地点让 AI 分析推荐等～

发布与部署

公网部署方法挺多的，比如 GitHub、Gitee上提供了静态页面部署的能力，或者可以租一个阿里云服务器申请域名，搭建自己的网站。

**在 GitHub 部署静态页面的简要指南**

以下为 GitHub Pages 静态部署的核心步骤，基于官方文档和工具链实现：

### 1. 创建仓库

- 新建公共仓库，命名格式为`username.github.io`（`username`为你的 GitHub 用户名）。
- 克隆仓库到本地，添加静态文件（如`index.html`），并推送至`main`分支。


### 2. 配置发布源

- 进入仓库**Settings > Pages**，选择发布分支（如`main`或`gh-pages`）或`docs`文件夹作为源。
- 若使用自定义构建工具（如 Hugo、Vue 等），需禁用默认 Jekyll 构建：在源目录根路径创建空文件`.nojekyll`。


### 3. 使用 GitHub Actions 自动部署

- 在工作流配置文件（如`.github/workflows/deploy.yml`）中添加以下步骤：


```
- name: Deploy to GitHub Pages  
  uses: peaceiris/actions-gh-pages@v3  
  with:  
    github_token: ${{ secrets.GITHUB_TOKEN }}  
    publish_dir: ./public  # 替换为你的构建输出目录
```

此 Action 会将指定目录内容部署到`gh-pages`分支。

#### 4. 访问页面

- 页面地址为`https://username.github.io`，更新后通常需等待 1-10 分钟生效。


#### 5. 注意事项

- **权限问题**：若使用 GitHub Actions 推送，需确保管理员已验证邮箱并推送过代码。
- **符号链接**：仓库含符号链接时，需通过 GitHub Actions 部署。


最后

这次的实践我认为还是非常的有趣的，整个开发过程大概 3-4 小时，而且主要花在了找素材和调整样式上了。放在以前，有了一个好的点子，但是可能会因为麻烦，跨技术栈，生产周期长、拖延症等各种因素导致“创业未半而中道崩殂”。

不得不感叹，AI 真的能帮助人们提高效率，并且使之前不可能或者很难完成的事情变得可行。在 AI 时代，可能需要从之前传统的“关注技术栈和专业，关注如何实现”的思维转向聚焦到“扩展思维的宽度和认知，寻找事物的可达路径”上。

另外，高德的小伙伴是否考虑一下，增加一个餐厅、团建的地点投票功能～

可以在高德上发起投票，录入几个候选位置，邀请小伙伴们一起投票。可以很方便的查看当前位置（或者出发地点）距离候选地点的距离、交通方式和用时、候选地点周边配套等。 也可以让 AI 结合需求背景，总结一下各候选地点的优势。然后小伙伴们就可以愉快地投票了！

## 附录

源码如下，需要的小伙伴可自取，在这个基础上改改就能用了。

杭州美食地图

```
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <title>杭州美食地图</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <style>
    html, body, #map { height: 100%; margin: 0; padding: 0; }
    .amap-info-content { font-size: 14px; }
    .legend {
      position: absolute;
      top: 10px;
      left: 10px;
      background: rgba(255,255,255,0.9);
      border-radius: 6px;
      padding: 10px;
      box-shadow: 02px 8px rgba(0,0,0,0.15);
      z-index: 1000;
    }
    .legend-item { display: flex; align-items: center; margin-bottom: 6px; }
    .legend-icon { width: 20px; height: 20px; margin-right: 6px; }
    .marker-label {
      font-size: 16px;
      color: #fff;
      background: rgba(34,34,34,0.75);
      border-radius: 6px;
      padding: 2px 10px;
      box-shadow: 02px 8px rgba(0,0,0,0.15);
      white-space: nowrap;
      transition: background 0.2s;
      border: none;
    }
    .marker-label-hover {
      background: rgba(34,34,34,0.95);
      color: #ffe58f;
      border: none;
    }
    /* 强制覆盖高德地图label的蓝色边框和背景 */
    .amap-marker-label {
      border: none !important;
      box-shadow: none !important;
      background: none !important;
      padding: 0 !important;
    }
    .filter-panel {
      position: absolute;
      top: 40px;
      right: 20px;
      width: 220px;
      background: rgba(255,255,255,0.97);
      border-radius: 10px;
      box-shadow: 02px 16px rgba(0,0,0,0.13);
      padding: 18px 18px 12px 18px;
      z-index: 1200;
      font-family: 'PingFang SC', 'Microsoft YaHei', Arial, sans-serif;
      font-size: 15px;
      color: #222;
      transition: box-shadow 0.2s;
      max-height: 600px;
      overflow-y: auto;
    }
    .filter-title {
      font-size: 18px;
      font-weight: bold;
      margin-bottom: 12px;
      letter-spacing: 2px;
    }
    .filter-section { margin-bottom: 14px; }
    .filter-label { font-size: 14px; margin-bottom: 6px; color: #666; }
    .filter-recommend label, .filter-category label {
      display: inline-block;
      margin-right: 10px;
      margin-bottom: 6px;
      cursor: pointer;
      font-size: 14px;
    }
    .filter-category {
      max-height: 280px;
      overflow-y: auto;
      border-radius: 6px;
      background: #f7f7f7;
      padding: 6px 4px 4px 8px;
      border: 1px solid #eee;
    }
    .filter-category label { width: 120px; }
    .filter-panel input[type="checkbox"] {
      accent-color: #1890ff;
      margin-right: 3px;
      vertical-align: middle;
    }
  </style>
  <!-- 高德地图 JS API -->
  <script src="https://webapi.amap.com/maps?v=2.0&key=「你的高德 apikey」"></script>
</head>
<body>
  <div id="map"></div>
  <div class="legend" id="legend"></div>
  <div id="filter-panel" class="filter-panel">
    <div class="filter-title">杭州美食指南</div>
    <div class="filter-section">
      <div class="filter-label">推荐指数</div>
      <div class="filter-recommend">
        <label><input type="checkbox" name="recommend" value="5"> 5星</label>
        <label><input type="checkbox" name="recommend" value="4"> 4星</label>
        <label><input type="checkbox" name="recommend" value="3"> 3星</label>
        <label><input type="checkbox" name="recommend" value="2"> 2星</label>
        <label><input type="checkbox" name="recommend" value="1"> 1星</label>
      </div>
    </div>
    <div class="filter-section">
      <div class="filter-label">餐厅类别</div>
      <div class="filter-category" id="filter-category-list"></div>
    </div>
  </div>
  <script>
    // 餐厅数据直接嵌入或读取同级目录下文件都可
    const data =  [
  {
    "name": "如*餐厅",
    "type": "中餐厅",
    "location": "120.122175,30.253356",
    "address": "玉泉路1*号",
    "photo": "http://store.is.autonavi.com/showpic/b08795ab6adeba25a0115d74130862aa",
    "cost": "",
    "open_time": "11:30-14:00 17:30-21:00",
    "rating": "4.7",
    "phone": "",
    "advantage": "推荐理由 xxxx",
    "recommend_index": "5",
    "category": "中餐"
  },
  {
    "name": "杭州**湖四季酒店金沙厅",
    "type": "浙江菜",
    "location": "120.129637,30.251887",
    "address": "灵隐路5号杭州**湖四季酒店1层(近曲院风荷)",
    "photo": "http://store.is.autonavi.com/showpic/03f435393b04359460529d3cc484e826",
    "cost": "533.00",
    "open_time": "11:30-14:00 17:30-21:00",
    "rating": "4.8",
    "phone": "",
    "advantage": "推荐理由 xxxx",
    "recommend_index": "5",
    "category": "杭帮菜/浙江菜"
  },
  {
    "name": "门没锁咖啡馆",
    "type": "咖啡馆",
    "location": "120.099355,30.297518",
    "address": "政紫弄23幢**号沿街(**地铁站F口步行210米)",
    "photo": "https://aos-comment.amap.com/B0KUPD8084/comment/A241830B_F0B4_4496_A253_95A1F5385C51_L0_001_1500_2000_1735672012627_76019873.jpg",
    "cost": "",
    "open_time": "10:00-17:00",
    "rating": "4.3",
    "phone": "",
    "advantage": "推荐理由 xxxx",
    "recommend_index": "4",
    "category": "咖啡馆"
  }
  {
    "name": "helloworld",
    "type": "咖啡馆",
    "location": "120.005480,30.280547",
    "address": "欧美金融城西溪丽晶居*幢底商1-13号",
    "photo": "http://store.is.autonavi.com/showpic/72efe174477c732d4264f7373dfaf768",
    "cost": "30.00",
    "open_time": "08:00-18:00",
    "rating": "4.3",
    "phone": "",
    "advantage": "推荐理由 xxxx",
    "recommend_index": "4",
    "category": "咖啡馆"
  }
];
    // 图标映射表，按最新icon.txt
    const typeIcons = {
      '辣椒': '「需要自己准备」',
      '甜点': '「需要自己准备」',
      '咖啡': '「需要自己准备」',
      '中餐': '「需要自己准备」',
      '日料': '「需要自己准备」',
      '快餐': '「需要自己准备」',
      '烤肉': '「需要自己准备」',
      '烧烤': '「需要自己准备」',
      '星星': '「需要自己准备」',
      '火锅': '「需要自己准备」',
      '牛排': '「需要自己准备」',
      '面食': '「需要自己准备」',
      '海鲜': '「需要自己准备」',
      '韩餐': '「需要自己准备」',
      '小吃': '「需要自己准备」',
      '粤菜': '「需要自己准备」',
      'default': '「需要自己准备」'
    };
    // 图例分类，按icon.txt顺序
    const legendTypes = [
      {type: '中餐', label: '中餐/杭帮菜/其他'},
      {type: '粤菜', label: '粤菜'},
      {type: '辣椒', label: '川菜'},
      {type: '火锅', label: '火锅'},
      {type: '烧烤', label: '烧烤'},
      {type: '烤肉', label: '烤肉'},
      {type: '日料', label: '日料'},
      {type: '韩餐', label: '韩餐'},
      {type: '牛排', label: '西餐'},
      {type: '面食', label: '面馆/面食'},
      {type: '小吃', label: '小吃'},
      {type: '甜点', label: '甜品/饮品'},
      {type: '咖啡', label: '咖啡馆'},
      {type: '快餐', label: '快餐'},
      {type: '海鲜', label: '海鲜'}
    ];
    // category到icon的映射规则
    function getCategoryIcon(category){
      if (!category) return typeIcons['default'];
      if (category === '中餐' || category === '杭帮菜/浙江菜' || category === '湘菜' || category === '东北菜' || category === '素食' || category === '私房菜') return typeIcons['中餐'];
      if (category === '粤菜') return typeIcons['粤菜'];
      if (category === '川菜') return typeIcons['辣椒'];
      if (category === '火锅') return typeIcons['火锅'];
      if (category === '烧烤/烤肉') return typeIcons['烤肉'];
      if (category === '烧烤') return typeIcons['烧烤'];
      if (category === '日料') return typeIcons['日料'];
      if (category === '韩餐') return typeIcons['韩餐'];
      if (category === '西餐') return typeIcons['牛排'];
      if (category === '面馆') return typeIcons['面食'];
      if (category === '小吃') return typeIcons['小吃'];
      if (category === '甜品/饮品') return typeIcons['甜点'];
      if (category === '咖啡馆') return typeIcons['咖啡'];
      if (category === '快餐') return typeIcons['快餐'];
      if (category === '海鲜') return typeIcons['海鲜'];
      return typeIcons['default'];
    }
    
    // 初始化地图
    constmap = new AMap.Map('map', {
      center: [120.15507, 30.274085], // 杭州中心
      zoom: 12
    });
    // 移除所有 data.forEach(...) 相关的marker渲染，只保留 renderMarkers() 控制
    // ... existing code ...
    // 图例渲染
    const legend = document.getElementById('legend');
    legend.innerHTML = legendTypes.map(t =>
      `<div class="legend-item"><img class='legend-icon' src='${typeIcons[t.type]}' alt='${t.label}' />${t.label}</div>`
    ).join('');
    // InfoWindow全局变量
    let infoWindow = null;
    // label样式
    const style = document.createElement('style');
    style.innerHTML = `
      .marker-label {
        font-size: 16px;
        color: #fff;
        background: rgba(34,34,34,0.75);
        border-radius: 6px;
        padding: 2px 10px;
        box-shadow: 02px 8px rgba(0,0,0,0.15);
        white-space: nowrap;
        transition: background 0.2s;
        border: none;
      }
      .marker-label-hover {
        background: rgba(34,34,34,0.95);
        color: #ffe58f;
        border: none;
      }
      /* 强制覆盖高德地图label的蓝色边框和背景 */
      .amap-marker-label {
        border: none !important;
        box-shadow: none !important;
        background: none !important;
        padding: 0 !important;
      }
    `;
    document.head.appendChild(style);
    // 动态生成类别筛选项
    const allCategories = Array.from(new Set(data.map(d => d.category).filter(Boolean)));
    const filterCategoryList = document.getElementById('filter-category-list');
    filterCategoryList.innerHTML = allCategories.map(cat =>
      `<label><input type='checkbox' name='category' value='${cat}'> ${cat}</label>`
    ).join('');
    // 默认勾选5星
    document.querySelector('input[name="recommend"][value="5"]').checked = true;

    // 筛选逻辑
    function getSelectedRecommends() {
      return Array.from(document.querySelectorAll('input[name="recommend"]:checked')).map(i => i.value);
    }
    function getSelectedCategories(){
      return Array.from(document.querySelectorAll('input[name="category"]:checked')).map(i => i.value);
    }
    let allMarkers = [];
    function renderMarkers(){
      // 清除旧marker
      allMarkers.forEach(m => m.setMap(null));
      allMarkers = [];
      const selectedRecommends = getSelectedRecommends();
      const selectedCategories = getSelectedCategories();
      let filtered = data;
      // 取交集策略：都选了才展示
      if (selectedRecommends.length) {
        filtered = filtered.filter(d => selectedRecommends.includes(d.recommend_index));
      }
      if (selectedCategories.length) {
        filtered = filtered.filter(d => selectedCategories.includes(d.category));
      }
      // 如果都没选，展示全部
      if (!selectedRecommends.length && !selectedCategories.length) {
        filtered = data;
      }
      filtered.forEach(item => {
        if (!item.location) return;
        const [lng, lat] = item.location.split(',').map(Number);
        const iconUrl = getCategoryIcon(item.category);
        const marker = new AMap.Marker({
          position: [lng, lat],
          icon: new AMap.Icon({
            image: iconUrl,
            size: new AMap.Size(32, 32),
            imageSize: new AMap.Size(32, 32)
          }),
          title: item.name,
          offset: new AMap.Pixel(-16, -36),
          label: {
            content: `<span class='marker-label'>${item.name}</span>`,
            direction: 'top',
            offset: new AMap.Pixel(0, -16),
            clickable: true
          }
        });
        marker.on('mouseover', () => marker.setLabel({ ...marker.getLabel(), content: `<span class='marker-label marker-label-hover'>${item.name}</span>` }));
        marker.on('mouseout', () => marker.setLabel({ ...marker.getLabel(), content: `<span class='marker-label'>${item.name}</span>` }));
        marker.on('click', () => showInfo(item));
        marker.on('labelClick', () => showInfo(item));
        marker.setMap(map);
        allMarkers.push(marker);
      });
    }
    // 监听筛选项变化
    document.querySelectorAll('.filter-panel input[type="checkbox"]').forEach(input => {
      input.addEventListener('change', renderMarkers);
    });
    // 初始化时渲染一次
    renderMarkers();

    function showInfo(item){
      // 关闭已有 infoWindow
      if (infoWindow) {
        infoWindow.close();
      }
      // 构建详情内容
      const content = `
        <div style="min-width:220px;max-width:320px;">
          <div style="font-size:18px;font-weight:bold;margin-bottom:6px;">${item.name}</div>
          <div style="margin-bottom:4px;">${item.address ? '📍 ' + item.address : ''}</div>
          ${item.photo ? `<img src="${item.photo}" style="width:100%;max-height:120px;object-fit:cover;border-radius:6px;margin-bottom:6px;">` : ''}
          <div>类型：${item.category || item.type || ''}</div>
          <div>推荐指数：${item.recommend_index || ''}</div>
          <div>评分：${item.rating || ''}</div>
          <div>人均：${item.cost ? '￥' + item.cost : ''}</div>
          <div>营业时间：${item.open_time || ''}</div>
          <div>电话：${item.phone || ''}</div>
          <div style="margin-top:4px;">${item.advantage || ''}</div>
        </div>
      `;
      // 取坐标
      const [lng, lat] = item.location.split(',').map(Number);
      infoWindow = new AMap.InfoWindow({
        content,
        offset: new AMap.Pixel(0, -36)
      });
      infoWindow.open(map, [lng, lat]);
    }

    // 点击地图空白处关闭详情弹窗
    map.on('click', function() {
      if (infoWindow) infoWindow.close();
    });
  </script>
</body>
</html>
```

“去哪吃”源码

```
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <title>去哪吃-AI推荐餐厅</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <style>
    html, body, #map { height: 100%; margin: 0; padding: 0; }
    .amap-info-content { font-size: 14px; }
    .legend {
      position: absolute;
      top: 10px;
      left: 10px;
      background: rgba(255,255,255,0.9);
      border-radius: 6px;
      padding: 10px;
      box-shadow: 02px 8px rgba(0,0,0,0.15);
      z-index: 1000;
    }
    .legend-item { display: flex; align-items: center; margin-bottom: 6px; }
    .legend-icon { width: 20px; height: 20px; margin-right: 6px; }
    .marker-label {
      font-size: 16px;
      color: #fff;
      background: rgba(34,34,34,0.75);
      border-radius: 6px;
      padding: 2px 10px;
      box-shadow: 02px 8px rgba(0,0,0,0.15);
      white-space: nowrap;
      transition: background 0.2s;
      border: none;
    }
    .marker-label-hover {
      background: rgba(34,34,34,0.95);
      color: #ffe58f;
      border: none;
    }
    /* 强制覆盖高德地图label的蓝色边框和背景 */
    .amap-marker-label {
      border: none !important;
      box-shadow: none !important;
      background: none !important;
      padding: 0 !important;
    }
    .filter-panel {
      position: absolute;
      top: 40px;
      right: 20px;
      width: 220px;
      background: rgba(255,255,255,0.97);
      border-radius: 10px;
      box-shadow: 02px 16px rgba(0,0,0,0.13);
      padding: 18px 18px 12px 18px;
      z-index: 1200;
      font-family: 'PingFang SC', 'Microsoft YaHei', Arial, sans-serif;
      font-size: 15px;
      color: #222;
      transition: box-shadow 0.2s;
      max-height: 600px;
      overflow-y: auto;
    }
    .filter-title {
      font-size: 18px;
      font-weight: bold;
      margin-bottom: 12px;
      letter-spacing: 2px;
    }
    .filter-section { margin-bottom: 14px; }
    .filter-label { font-size: 14px; margin-bottom: 6px; color: #666; }
    .filter-recommend label, .filter-category label {
      display: inline-block;
      margin-right: 10px;
      margin-bottom: 6px;
      cursor: pointer;
      font-size: 14px;
    }
    .filter-category {
      max-height: 280px;
      overflow-y: auto;
      border-radius: 6px;
      background: #f7f7f7;
      padding: 6px 4px 4px 8px;
      border: 1px solid #eee;
    }
    .filter-category label { width: 120px; }
    .filter-panel input[type="checkbox"] {
      accent-color: #1890ff;
      margin-right: 3px;
      vertical-align: middle;
    }
    .detail-panel {
      position: absolute;
      top: 40px;
      right: 20px;
      width: 400px;
      background: rgba(255,255,255,0.98);
      border-radius: 14px;
      box-shadow: 04px 32px rgba(0,0,0,0.13);
      padding: 28px 28px 18px 28px;
      z-index: 1200;
      font-family: 'PingFang SC', 'Microsoft YaHei', Arial, sans-serif;
      font-size: 16px;
      color: #222;
      max-height: 80vh;
      overflow-y: auto;
      transition: box-shadow 0.2s;
      display: none;
    }
    .detail-title {
      font-size: 22px;
      font-weight: bold;
      margin-bottom: 10px;
      color: #1890ff;
      letter-spacing: 1px;
    }
    .detail-recommend {
      background: #fffbe6;
      color: #faad14;
      border-radius: 8px;
      padding: 8px 14px;
      font-size: 18px;
      font-weight: bold;
      margin-bottom: 16px;
      box-shadow: 02px 8px rgba(250,173,20,0.08);
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .detail-photo {
      width: 100%;
      max-height: 180px;
      object-fit: cover;
      border-radius: 8px;
      margin-bottom: 10px;
      box-shadow: 02px 8px rgba(0,0,0,0.08);
    }
    .detail-field { margin-bottom: 8px; }
    .detail-label { color: #888; margin-right: 6px; }
    .detail-analysis {
      background: #f6ffed;
      color: #389e0d;
      border-radius: 8px;
      padding: 10px 14px;
      margin-top: 12px;
      font-size: 15px;
      box-shadow: 02px 8px rgba(56,158,13,0.06);
    }
    .detail-panel-title {
      font-size: 20px;
      font-weight: bold;
      text-align: center;
      margin-bottom: 18px;
      color: #222;
      letter-spacing: 1px;
    }
  </style>
  <!-- 高德地图 JS API -->
  <script src="https://webapi.amap.com/maps?v=2.0&key=「你的高德 apikey」"></script>
</head>
<body>
  <div id="map"></div>
  <div id="detail-panel" class="detail-panel"></div>
  <script>
    // 直接嵌入餐厅数据
    const data = [
      {
        "name": "杭州市阿里巴巴滨江园区（出发点）",
        "type": "出发点",
        "location": "120.190371,30.189600",
        "address": "杭州市滨江区网商路6**号",
        "photo": "https://gw.alicdn.com/imgextra/i2/O1CN014DVQlb1oVqsnsrbiT_!!6000000005231-2-tps-64-64.png",
        "cost": "-",
        "open_time": "-",
        "rating": "-",
        "phone": "-",
        "advantage": "公司园区，交通便利，地铁直达，周边配套齐全。",
        "recommend_index": "-",
        "category": "出发点",
        "is_origin": true
      },
      {
        "name": "海*捞火锅(中南乐游城店)",
        "type": "火锅",
        "location": "120.190309,30.193994",
        "address": "江南大道10**号",
        "photo": "https://aos-comment.amap.com/B0GU9MT4N7/comment/6845185a8eedb6301996b74240ba088b_2048_2048_80.jpg",
        "cost": "80.00",
        "open_time": "09:00-07:00",
        "rating": "4.7",
        "phone": "-",
        "advantage": "服务优质，环境舒适，适合聚餐。",
        "recommend_index": "5",
        "category": "火锅",
        "distance_m": 2030,
        "duration_s": 459,
        "traffic": "驾车约8分钟，公交便利，地铁近。",
        "surrounding": "中南乐游城、知嘛家等商场，生活便利。",
        "analysis": "距离适中，交通便利，配套丰富，适合团队聚餐。"
      },
      {
        "name": "黄*海鲜大排档(滨江店)",
        "type": "海鲜",
        "location": "120.195922,30.197039",
        "address": "浙商发展大厦*座1-2楼(**地铁站G口)",
        "photo": "https://aos-comment.amap.com/B0J1B5R0EY/comment/0e8ed310fa3bb3135ddbefe27244562f_2048_2048_80.jpg",
        "cost": "139.00",
        "open_time": "11:00-15:30 17:30-02:30",
        "rating": "4.7",
        "phone": "-",
        "advantage": "菜品新鲜，适合多人聚餐，夜宵丰富。",
        "recommend_index": "5",
        "category": "海鲜",
        "distance_m": 2395,
        "duration_s": 478,
        "traffic": "驾车约8分钟，地铁直达，公交便利。",
        "surrounding": "知嘛家等商场，夜生活丰富。",
        "analysis": "交通便利，夜宵丰富，适合下班聚会。"
      },
      {
        "name": "群*饭店(信诚路店)",
        "type": "中餐",
        "location": "120.174707,30.183901",
        "address": "滨安路11**号(近信诚路)",
        "photo": "http://store.is.autonavi.com/showpic/2ac9e95efffe6e27a8eda43ef8271134",
        "cost": "66.00",
        "open_time": "11:00-13:30 16:00-20:30",
        "rating": "4.7",
        "phone": "-",
        "advantage": "家常菜，性价比高，适合日常用餐。",
        "recommend_index": "4",
        "category": "中餐",
        "distance_m": 2797,
        "duration_s": 757,
        "traffic": "驾车约13分钟，公交可达。",
        "surrounding": "周边无大型商场，环境安静。",
        "analysis": "性价比高，适合小团队日常聚餐。"
      },
      {
        "name": "龙*·滨江烤全羊(杭州总店)",
        "type": "烤肉",
        "location": "120.195890,30.184231",
        "address": "长河路47*号和瑞科技广场S*幢楼下",
        "photo": "http://store.is.autonavi.com/showpic/45d72ae00c69cf56d4fe514b1346c55c",
        "cost": "132.00",
        "open_time": "11:00-21:00",
        "rating": "4.8",
        "phone": "-",
        "advantage": "烤全羊特色，适合聚会，环境宽敞。",
        "recommend_index": "5",
        "category": "烤肉",
        "distance_m": 1226,
        "duration_s": 254,
        "traffic": "驾车约4分钟，公交可达。",
        "surrounding": "保利·时光里等商场，配套齐全。",
        "analysis": "距离最近，评分最高，配套好，强烈推荐。"
      },
      {
        "name": "东*方(杭州保利时光里店)",
        "type": "中餐",
        "location": "120.197088,30.182094",
        "address": "长河街道长河路与滨康路交叉口保利时光里*楼13号楼2017商铺",
        "photo": "http://store.is.autonavi.com/query_pic?id=st1ef630c8-39ef-4d63-93ce-ba3a9732851e&user=search&operate=original",
        "cost": "-",
        "open_time": "-",
        "rating": "4.8",
        "phone": "-",
        "advantage": "环境优雅，适合家庭聚餐。",
        "recommend_index": "5",
        "category": "中餐",
        "distance_m": 2088,
        "duration_s": 491,
        "traffic": "驾车约8分钟，公交便利。",
        "surrounding": "保利·时光里等商场，生活便利。",
        "analysis": "评分高，环境好，适合家庭和小型聚会。"
      }
    ];
    // 图标映射表
    const typeIcons = {
      '辣椒': '「需要自己准备」',
      '甜点': '「需要自己准备」',
      '咖啡': '「需要自己准备」',
      '中餐': '「需要自己准备」',
      '日料': '「需要自己准备」',
      '快餐': '「需要自己准备」',
      '烤肉': '「需要自己准备」',
      '烧烤': '「需要自己准备」',
      '星星': '「需要自己准备」',
      '火锅': '「需要自己准备」',
      '牛排': '「需要自己准备」',
      '面食': '「需要自己准备」',
      '海鲜': '「需要自己准备」',
      '韩餐': '「需要自己准备」',
      '小吃': '「需要自己准备」',
      '粤菜': '「需要自己准备」',
      'default': '「需要自己准备」'
    };
    function getCategoryIcon(category){
      if (!category) return typeIcons['default'];
      if (category === '出发点') return typeIcons['星星'];
      if (category === '中餐' || category === '杭帮菜/浙江菜' || category === '湘菜' || category === '东北菜' || category === '素食' || category === '私房菜') return typeIcons['中餐'];
      if (category === '粤菜') return typeIcons['粤菜'];
      if (category === '川菜') return typeIcons['辣椒'];
      if (category === '火锅') return typeIcons['火锅'];
      if (category === '烧烤/烤肉' || category === '烤肉') return typeIcons['烤肉'];
      if (category === '烧烤') return typeIcons['烧烤'];
      if (category === '日料') return typeIcons['日料'];
      if (category === '韩餐') return typeIcons['韩餐'];
      if (category === '西餐') return typeIcons['牛排'];
      if (category === '面馆') return typeIcons['面食'];
      if (category === '小吃') return typeIcons['小吃'];
      if (category === '甜品/饮品') return typeIcons['甜点'];
      if (category === '咖啡馆') return typeIcons['咖啡'];
      if (category === '快餐') return typeIcons['快餐'];
      if (category === '海鲜') return typeIcons['海鲜'];
      return typeIcons['default'];
    }
    // 初始化地图
    constmap = new AMap.Map('map', {
      center: [120.190371, 30.189600],
      zoom: 14
    });
    let allMarkers = [];
    let allLines = [];
    function renderMarkers(){
      // 清除旧marker和线
      allMarkers.forEach(m => m.setMap(null));
      allMarkers = [];
      allLines.forEach(l => l.setMap(null));
      allLines = [];
      if (!data.length) return;
      // 出发点
      const origin = data.find(d => d.is_origin);
      // 餐厅
      const restaurants = data.filter(d => !d.is_origin);
      // 出发点marker
      if (origin) {
        const [lng, lat] = origin.location.split(',').map(Number);
        const marker = new AMap.Marker({
          position: [lng, lat],
          icon: new AMap.Icon({
            image: getCategoryIcon('出发点'),
            size: new AMap.Size(40, 40),
            imageSize: new AMap.Size(40, 40)
          }),
          title: origin.name,
          offset: new AMap.Pixel(-20, -40),
          label: {
            content: `<span class='marker-label'>${origin.name}</span>`,
            direction: 'top',
            offset: new AMap.Pixel(0, -20),
            clickable: true
          }
        });
        marker.setMap(map);
        allMarkers.push(marker);
      }
      // 餐厅marker和连线
      restaurants.forEach(item => {
        if (!item.location) return;
        const [lng, lat] = item.location.split(',').map(Number);
        const iconUrl = getCategoryIcon(item.category);
        const marker = new AMap.Marker({
          position: [lng, lat],
          icon: new AMap.Icon({
            image: iconUrl,
            size: new AMap.Size(32, 32),
            imageSize: new AMap.Size(32, 32)
          }),
          title: item.name,
          offset: new AMap.Pixel(-16, -36),
          label: {
            content: `<span class='marker-label'>${item.name}</span>`,
            direction: 'top',
            offset: new AMap.Pixel(0, -16),
            clickable: true
          }
        });
        marker.on('mouseover', () => marker.setLabel({ ...marker.getLabel(), content: `<span class='marker-label marker-label-hover'>${item.name}</span>` }));
        marker.on('mouseout', () => marker.setLabel({ ...marker.getLabel(), content: `<span class='marker-label'>${item.name}</span>` }));
        marker.on('click', () => showInfo(item));
        marker.on('labelClick', () => showInfo(item));
        marker.setMap(map);
        allMarkers.push(marker);
        // 连线
        if (origin && origin.location) {
          const [olng, olat] = origin.location.split(',').map(Number);
          const line = new AMap.Polyline({
            path: [ [olng, olat], [lng, lat] ],
            strokeColor: '#1890ff',
            strokeWeight: 4,
            strokeOpacity: 0.7,
            isOutline: true,
            outlineColor: '#fff'
          });
          line.setMap(map);
          allLines.push(line);
        }
      });
    }
    // 智能推荐（评分最高且距离最近）
    function showRecommend(){
      if (!data.length) return;
      const restaurants = data.filter(d => !d.is_origin);
      // 评分优先，距离次之
      let best = restaurants[0];
      restaurants.forEach(r => {
        if (
          Number(r.rating) > Number(best.rating) ||
          (r.rating === best.rating && r.distance_m < best.distance_m)
        ) {
          best = r;
        }
      });
      showInfo(best, true);
    }
    // 右侧详情面板
    function showInfo(item, isRecommend = false){
      const panel = document.getElementById('detail-panel');
      if (!item) { panel.style.display = 'none'; return; }
      let html = '';
      html += `<div class='detail-panel-title'>AI推荐餐厅</div>`;
      if (isRecommend) {
        html += `<div class='detail-recommend'>🌟 智能推荐：<span>${item.name}</span></div>`;
      }
      html += `<div class='detail-title'>${item.name}</div>`;
      if (item.photo) html += `<img class='detail-photo' src='${item.photo}' alt='${item.name}'>`;
      html += `<div class='detail-field'><span class='detail-label'>类型：</span>${item.type || ''}</div>`;
      html += `<div class='detail-field'><span class='detail-label'>地址：</span>${item.address || ''}</div>`;
      if (item.distance_m) html += `<div class='detail-field'><span class='detail-label'>距离：</span>${(item.distance_m/1000).toFixed(2)} km</div>`;
      if (item.duration_s) html += `<div class='detail-field'><span class='detail-label'>车程：</span>${Math.round(item.duration_s/60)} 分钟</div>`;
      if (item.cost && item.cost !== '-') html += `<div class='detail-field'><span class='detail-label'>人均：</span>￥${item.cost}</div>`;
      if (item.open_time && item.open_time !== '-') html += `<div class='detail-field'><span class='detail-label'>营业时间：</span>${item.open_time}</div>`;
      if (item.rating && item.rating !== '-') html += `<div class='detail-field'><span class='detail-label'>评分：</span>${item.rating}</div>`;
      if (item.phone && item.phone !== '-') html += `<div class='detail-field'><span class='detail-label'>电话：</span>${item.phone}</div>`;
      if (item.traffic) html += `<div class='detail-field'><span class='detail-label'>交通：</span>${item.traffic}</div>`;
      if (item.surrounding) html += `<div class='detail-field'><span class='detail-label'>周边配套：</span>${item.surrounding}</div>`;
      if (item.advantage) html += `<div class='detail-field'><span class='detail-label'>优点：</span>${item.advantage}</div>`;
      if (item.analysis) html += `<div class='detail-analysis'>${item.analysis}</div>`;
      panel.innerHTML = html;
      panel.style.display = 'block';
    }
    // 地图点击空白关闭详情
    map.on('click', function() {
      document.getElementById('detail-panel').style.display = 'none';
    });
    renderMarkers();
    showRecommend();
  </script>
</body>
</html>
```

**10分钟微调：让0.6B模型媲美235B模型**

大参数模型效果好，但成本高、响应慢。针对该问题，可以用大参数模型的输出去微调小参数模型，使其在特定任务中的表现接近大参数模型，这一过程也被称为模型蒸馏。本方案介绍如何通过模型蒸馏提升 Qwen3-0.6B 模型在特定任务的表现（本案例中准确率从14%提升至90%以上）。

点击阅读原文查看详情。

