---
作者:
  - "哔哩哔哩技术"
原文链接: https://mp.weixin.qq.com/s?__biz=Mzg3Njc0NTgwMg==&amp;mid=2247501708&amp;idx=1&amp;sn=3eacbd4445fe9a5c31e1f186fdb606bb&amp;chksm=cefdbbc7896f16b253589946a5edf4cdca8d6249d567e60531bb3237677b00b061f344e3d369&amp;mpshare=1&amp;scene=1&amp;srcid=1213CbDIt5mHvvJs861HIlEj&amp;sharer_shareinfo=6700eeee4dae8538c6f46a58f6578978&amp;sharer_shareinfo_first=6700eeee4dae8538c6f46a58f6578978#rd
发布时间: ""
收藏时间: "2024-12-13"
关联日记: "[[2024-12-13]]"
tags:
  - 文章
---
**1. 背景**

评论是 B站生态的重要组成部分，涵盖了 UP 主与用户的互动、平台内容的推荐与优化、社区文化建设以及用户情感满足。B站的评论区不仅是用户互动的核心场所，也是平台运营和用户粘性的关键因素之一，尤其是在与弹幕结合的情况下，成为平台的标志性特色。

在社会热点事件发生时，评论区的读写流量会急剧增加，直接影响业务运行，对用户体验、内容创作和社区文化等多个方面产生负面影响，所以评论服务的稳定性至关重要。

评论系统对缓存命中率要求非常高，一旦发生缓存失效，大量请求会直接访问 TiDB，如果 TiDB 出现问题，将导致评论服务不可用。所以评论需要构建一套可靠的容灾系统，并具备自动降级能力，以提升评论服务的整体稳定性。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/675bf6e46101f514ee938e64/c9f0ecaa-e754-431b-a51f-da24e154a797.png)

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/675bf6e46101f514ee938e64/97a20946-5633-4ff2-ba66-e8f648d95fe5.png)

**2. 架构设计**

评论系统架构主要依赖 Redis 缓存和 TiDB 存储，列表接口中依赖多种排序索引，如点赞序、时间序、热度序等，这些索引通过 Redis 的 Sorted Set 数据结构进行存储。

在大评论区中查询这些排序索引，当 Redis 缓存 miss 时需要回源 TiDB 查询，因数据量过大、查询耗时较长，慢查询会占用大量 CPU 和内存，进而导致其他查询的延迟或阻塞，严重影响整个 TiDB 的吞吐量和性能。例如查询点赞序排序索引：

```
SELECT id FROM reply WHERE ... ORDER BY like_count DESC LIMIT m,n
```

为了避免 TiDB 故障导致评论服务不可用，我们希望建立一套新的存储系统，解决 TiDB 单点故障问题。该系统不仅为业务提供容灾能力和自动降级通道，还能在大流量查询场景下提供更优的查询性能，从而提升整体评论服务的稳定性。

基于 B站自研的泰山 KV 存储（Taishan），我们搭建了「多级存储架构」，整体设计方案的核心思路包括：

- 将排序索引的存储从「结构化」转为「非结构化」
- 将排序索引查询从「SQL」转换为性能更高的「NoSQL」
- 通过「写场景的复杂度」来换取「更优的读场景性能」


![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/675bf6e46101f514ee938e64/3cd71ff8-8ab9-4821-80c5-9e99baf59a7d.png)

**3. 存储设计**

**存储模型**

在评论的业务场景中，我们抽象了两种数据模型：排序索引（Index）、评论物料（KV）

**抽象数据模型****TiDB 模型****Taishan 模型****说明**IndexSecondary IndexSorted Set排序索引，例如点赞序、时间序的排序索引KVPrimary Key & RowKey-Value包含元数据、内容等必要的评论物料

下图以按点赞序排序的前 10 条评论为例，展示了使用 Index + KV 模型实现的具体思路。在更复杂的推荐排序场景中，依然可以通过此模型来实现。具体流程是：首先通过排序索引召回一批评论 ID，再通过推荐算法对这些 ID 进行重排，最终根据重排后的 ID 获取评论详情并返回给用户。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/675bf6e46101f514ee938e64/8e93ff64-b96f-46ef-b9b0-b33478e2f148.png)

将领域对象的存储建模划分为 Index 和 KV 两种模型，可以利用不同的底层存储结构来分别优化查询、扫描、排序、分页等场景。使用 Redis 或 Memcache 作为缓存构建 KV 模型，提升查询性能，使用 Redis 的 Sorted Set 构建 Index 模型，支持增量数据实时更新排序索引，并提供极高效的分页查询性能。在关键词搜索场景，可采用 ElasticSearch 作为检索索引，避免在原始数据库上进行低效的遍历操作；

基于 KV 作为唯一事实表，采用同步全量数据和实时捕获增量数据的方法，将原始数据转换为下游索引表。这样可以灵活构建定制化的排序索引，以应对多变的评论业务需求。同时该方案在不影响原有业务逻辑和存储资源的情况下，实现了业务、代码和数据的解耦。

如果索引的定义和实现不再局限于源数据库的原生索引，而是扩展到应用逻辑，并在其他存储上自行维护物化视图，这必然会带来额外的理解和维护成本，同时引入一致性的难题。然而考虑到评论业务的数据量级和复杂度，该方案的整体优势仍然大于劣势。所以我们需要新的存储方案，既支持基本的 Index 和 KV 模型，又能满足高性能、可用性和扩展性等方面的需求。

**数据类型**

我们期望将数据类型从 SQL 转向 NoSQL，因为 NoSQL 提供了更灵活的数据模型，意味着更可解释的执行计划和更高的优化潜力。例如 Taishan 查询 Redis Sorted Set 的 P999 耗时约 10ms，查询 KV 的 P999 耗时约 5ms，这种高效的查询性能对评论业务尤为重要。

相比 TiDB，Taishan 不支持 ACID 事务、二级索引等功能，提供的能力更为精简。基于之前的经验和问题，有时候“less is more”反而能带来更高的可用性。以下是评论业务在使用 TiDB 时遇到的一些问题：

1. **MVCC 机制：**TiDB 的事务实现基于 MVCC 机制，当新写入的数据覆盖旧数据时，旧数据不会被删除，而是以时间戳区分多个版本，并通过定期 GC 清理不再需要的数据。在热门评论区中，频繁更新点赞数时，排序索引的 MVCC 历史版本过多，导致 TiDB 的读写性能下降。相比之下，不支持 MVCC 的 Taishan 在查询排序索引时能提供更高效、更稳定的性能；
2. **分片策略：**TiDB 不直接支持完全自定义的分片策略，而 Taishan 支持哈希标签（hash tags），可以在 Key 中使用大括号 { } 指定参与哈希计算的部分。这样多个 Key 可以使用相同的 ID 进行分区路由，确保同一评论区的评论位于同一分片。在批量查询评论时，这能大幅降低扇出度，减少长尾耗时的影响。而对于可能出现热点的场景，Taishan 可以选择不使用哈希标签，从而打散请求，为性能要求高的评论业务提供更大的优化空间。


基于现有评论在 TiDB 中的存储结构和索引设计，以时间序和点赞序为例，列举 Taishan 的数据模型如下：

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/675bf6e46101f514ee938e64/f7965d05-44fc-49b2-94dd-9c7641233b96.png)

**4. 数据一致性**

从 TiDB 的结构化数据转变为 Taishan 的非结构化数据，目前缺乏现成的同步工具，需要业务自行实现数据同步。然而数据同步过程中可能出现数据丢失、写入失败、写冲突、顺序错乱和同步延迟等问题，导致数据不一致。由于评论业务对数据一致性要求较高，我们需要一套可靠的数据同步方案，确保两者之间的数据一致性。

**重试队列**

针对写失败的问题，我们通过引入重试队列来解决，将写失败的请求放入队列中进行异步重试，确保数据不会因暂时性问题而永久丢失。引入重试队列可能会导致写并发产生数据竞争，进而引发数据最终不一致。虽然可以通过 **CAS（Compare-and-Swap）**来解决数据竞争问题，确保“读取-修改-写回”操作的原子性，但这也可能带来乱序问题。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/675bf6e46101f514ee938e64/51e46bcf-daea-4147-98ee-0bd932632090.png)

**乱序问题**

由于写数据有多个场景来源，包括 binlog 同步、重试队列，这些并发写操作导致数据错误，此外 MQ 消息因 rebalance 可能会被重新消费，导致消息回放，所以数据同步过程中不仅需要保证幂等性，还必须确保消息的顺序性：

例如并发写的场景，评论 A 被点赞两次，点赞数（like_count）为 2，TiDB 会生成两条 binlog 数据：

1. 第一条数据 binlog_0 中，like_count = 1，由于网络原因写入失败，数据被转入重试队列进行异步处理。
2. 第二条数据 binlog_1 中，like_count = 2，写入成功，评论 A 的 like_count 更新为 2，符合预期。
3. 然而，重试队列继续处理 binlog_0，由于无法保证两个写操作的顺序，写入后 like_count 被更新为 1，导致数据不一致。


**回退问题**

在消息回放场景中，假设评论 A 被点赞三次，点赞数（like_count）为 3，TiDB 会生成三条 binlog 数据 [a, b, c]。正常情况下，这三条数据会被顺序消费并处理。如果在消费过程中发生 rebalance，导致消息回放，这三条数据会被重新消费，从而导致点赞数出现短暂的数据回退。

**版本号**

为避免乱序和回退问题导致的数据不一致，我们引入了版本号机制，每次评论数据变更时，版本号会递增。

```
UPDATE reply SET like_count=like_count+1, version=version+1 WHERE id = xxx
```

在 CAS 写操作时，将 binlog 数据中的 version 值与 Taishan 中数据的 version 值进行比对。如果 binlog 中的 version 值大于或等于当前数据的 version 值，则执行更新；否则认为该数据为过期数据，予以丢弃。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/675bf6e46101f514ee938e64/140f343b-4052-479e-b544-5d354f9927bd.png)

**对账系统**

根据 CAP 理论，在保证可用性（Availability）和分区容忍性（Partition）之后，分布式系统无法完全保证一致性（Consistency）。尽管引入了重试机制、CAS 和版本号机制，但由于网络调用的不可避免失败，评论数据之间难免会出现长期或短期的不一致状态。一旦发生不一致，需要有一套对账机制来及时发现并修复这些不一致的数据。

**实时对账**

通过 TiDB 的 Binlog 事件驱动，使用延迟队列延迟 n 秒后消费， binlog 数据关联查询 Taishan 数据，并对比两者的数据。对于发现的异常数据，进行通知并触发数据修复。

**离线对账**

利用 TiDB 和 Taishan 的数仓离线数据，进行 T+1 数据对比，验证数据的最终一致性。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/675bf6e46101f514ee938e64/b62cc2f5-f953-44c3-b303-16dfd74a1795.png)

**5. 降级策略**

评论业务对可用性的要求非常高，尤其是在高并发、实时性强、用户互动频繁的场景下。通过搭建多级存储架构，我们能够在 TiDB 故障时自动降级到 Taishan，确保评论服务持续正常运行，我们的目标是实现每个请求的自动降级。

每次请求时，首先尝试从主存储获取数据。当主存储服务返回错误或长时间无响应时，降级到次要存储服务获取数据。在设计降级策略时，通常采用串行或并行方式，分别影响系统的响应时间和复杂性，而且整体耗时不能超过上游的超时限制，否则降级无效。

**降级策略****优势****劣势**串行简单耗时长，容易整体超时并行耗时短多1倍的请求，浪费资源

串行策略无法满足评论业务对响应时间的要求，而并行策略则可能浪费资源。所以我们选择了「对冲策略」（Hedging Policy）。在主节点请求超时后，我们会发起一个「备份请求」（backup request）到次节点。如果主节点返回成功，则直接返回结果，否则等待次节点的响应。通过根据主次节点的耗时特性设置合理的延迟阈值，我们在整体响应时间和资源消耗之间达到了平衡。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/675bf6e46101f514ee938e64/40ab7100-026c-4305-bc74-af67dc95fe40.png)

在实际生产环境中，我们根据具体业务场景设定 TiDB 和 Taishan 的主次关系。对于对数据实时性敏感、查询轻量的场景，设定 TiDB 为主存储，Taishan 为次存储；而对于数据实时性要求较低、大 SQL 查询的场景，则设定 Taishan 为主存储，TiDB 为次存储。

某天凌晨，TiDB 底层的 TiKV 节点宕机，在 TiKV 自愈期间，系统自动降级到 Taishan，评论业务未受影响，线上服务持续稳定运行。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/675bf6e46101f514ee938e64/7052d4a6-9eb7-49ee-86a4-0457dc4598ed.png)

**6. 总结与展望**

B站评论服务对社区业务和用户体验至关重要。我们不仅致力于持续提升评论服务的稳定性，还不断优化评论业务，以便用户能够看到更优质的评论内容，从而增强归属感和认同感，提供更好的消费体验。

最后，发一条友善的评论吧，遇见和你一样有趣的人。

-End-

作者丨rumble、脆鲨鲨

**开发者问答**

**关于评论系统架构设计，大家还有什么优秀的技术方案么？**

欢迎在留言区分享你的见解~

转发本文至朋友圈并留言，即可参与**下方抽奖⬇️**

小编将抽取1位幸运的小伙伴从初**龙年小电视鼠标垫键盘垫**

**抽奖截止时间：12月17日12:00**

如果喜欢本期内容的话，欢迎点个“在看”吧！

**往期精彩指路**

- [【点个赞吧】 - B站千亿级点赞系统服务架构设计](https://mp.weixin.qq.com/s?__biz=Mzg3Njc0NTgwMg==&mid=2247493238&idx=1&sn=15816baafbbd4ae9bfaaf1fbcf337c50&scene=21#wechat_redirect)
- [B站评论系统架构设计](https://mp.weixin.qq.com/s?__biz=Mzg3Njc0NTgwMg==&mid=2247492337&idx=1&sn=adef6d0d16d7f5722569795efbf752aa&scene=21#wechat_redirect)
- [从0到1:哔哩哔哩智能客服系统的设计与实现](https://mp.weixin.qq.com/s?__biz=Mzg3Njc0NTgwMg==&mid=2247495847&idx=1&sn=aac7310cbfc8c531b6c3edf4e5de0318&scene=21#wechat_redirect)


[通用工程](https://mp.weixin.qq.com/mp/appmsgalbum?__biz=Mzg3Njc0NTgwMg==&action=getalbum&album_id=3289447926347317252#wechat_redirect)丨[大前端](https://mp.weixin.qq.com/mp/appmsgalbum?__biz=Mzg3Njc0NTgwMg==&action=getalbum&album_id=2390333109742534656#wechat_redirect)丨[业务线](https://mp.weixin.qq.com/mp/appmsgalbum?__biz=Mzg3Njc0NTgwMg==&action=getalbum&album_id=3297757408550699008#wechat_redirect)

[大数据](https://mp.weixin.qq.com/mp/appmsgalbum?__biz=Mzg3Njc0NTgwMg==&action=getalbum&album_id=2329861166598127619#wechat_redirect)丨[AI](https://mp.weixin.qq.com/mp/appmsgalbum?__biz=Mzg3Njc0NTgwMg==&action=getalbum&album_id=2782124818895699969#wechat_redirect)丨[多媒体](https://mp.weixin.qq.com/mp/appmsgalbum?__biz=Mzg3Njc0NTgwMg==&action=getalbum&album_id=2532608330440081409#wechat_redirect)

