---
作者:
  - "程序员平安"
原文链接: http://mp.weixin.qq.com/s?__biz=MzkxOTUyMzEzMw==&amp;mid=2247491442&amp;idx=1&amp;sn=7d99060d030494b2481a0dfc77bddb63&amp;chksm=c0c448c4323281896ba62abf7f5df94d17d4b8720117e4b1dbfb456b271f24fdc9fe524fdbb0&amp;mpshare=1&amp;scene=1&amp;srcid=10228AyqKxNL35IYIyIo0utS&amp;sharer_shareinfo=6d039b0f4dd23d5bc228fd43af7b596f&amp;sharer_shareinfo_first=6d039b0f4dd23d5bc228fd43af7b596f#rd
发布时间: ""
收藏时间: "2024-10-22"
关联日记: "[[2024-10-22]]"
tags:
  - 文章
---
点击“**程序员平安**”，关注，置顶公众号

每日技术文章，第一时间收到！

分享计算机相关的398本PDF电子书给你

来源：blog.csdn.net/qq_33905217/article/details/129211947

- 导言
- Redis的分页实现
- Redis的多条件模糊查询实现
- Redis的分页+多条件模糊查询组合实现
- 实现思路性能优化方案
- 总结


## 导言

Redis是一个高效的内存数据库，它支持包括String、List、Set、SortedSet和Hash等数据类型的存储，在Redis中通常根据数据的key查询其value值，Redis没有模糊条件查询，在面对一些需要分页、排序以及条件查询的场景时(如评论，时间线，检索等)，只凭借Redis所提供的功能就不太好不处理了。

本文不对Redis的特性做过多赘述。由于之前基于业务问题需要实现基于Redis的条件查询和分页功能，在百度上查询了不少文章，基本不是只有分页功能就是只有条件查询功能的实现，缺少两者组合的解决方案。因此，本文将基于Redis提供条件查询+分页的技术解决方案。

> 注：本文只提供实现思路，并不提供实现的代码

本文将从四个部分进行说明：

- 分页实现
- 模糊条件查询实现
- 分页和模糊条件查询的组合实现
- 优化方案


大家可以直接跳到自己需要的部分进行阅读。

## Redis的分页实现

我们通常习惯于在Mysql、Oracle这样持久化数据库中实现分页查询，但是基于某些特殊的业务场景下，我们的数据并未持久化到了数据库中或是出于查询速度上的考虑将热点数据加载到了缓存数据库中。因此，我们可能需要基于Redis这样的缓存数据库去进行分页查询。

Redis的分页查询的实现是基于Redis提供的ZSet数据结构实现的，ZSet全称为Sorted Set，该结构主要存储有序集合。下面是它的指令描述以及该指令在分页实现中的作用：

- ZADD ：SortedSet的添加元素指令`ZADD key score member [[score,member]…]`会给每个添加的元素member绑定一个用于排序的值score，SortedSet就会根据score值的大小对元素进行排序。我们为通常习惯于将数据的时间属性当作score用于排序，当然大家也可以根据具体的业务场景去选择排序的目标。
- ZREVRANGE ：SortedSet中的指令`ZREVRANGE key start stop`可以返回指定区间内的成员，可以用来做分页。
- ZREM ：SortedSet的指令`ZREM key member`可以根据key移除指定的成员，能满足删评论的要求。


所以SortedSet用来做分页是非常适合的。下面是分页实现的演示图，包含插入新记录后的查询情况。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67177ef4cb341455ad5b0e55/5943e759-0a85-421f-bb59-073575ceefd4.webp)

图片

事实上，Redis中的List结构也是可以实现分页，但List无法实现自动排序，并且Zset还可以根据score进行数据筛选，取出目标score区间内数据。

所以在实现上，ZSet往往更加适合我们。当然如果你需要插入重复数据的情况下，分页就可能就需要借助List来实现了。具体使用那种结构来实现分页还是需要根据实际的业务场景来进行选择的。

## Redis的多条件模糊查询实现

Redis是key-value类型的内存数据库，通过key直接取数据虽然很方便，但是并未提供像mysql那样方便的sql条件查询支持。因此我们需要借助Redis提供的结构和功能去自己实现模糊条件查询功能。

事实上，Redis的模糊条件查询是基于Hash实现的，我们可以将数据的某些条件值作为hash的key值，并数据本身作为value进行存储。然后通过Hash提供的HSCAN指令去遍历所有的key进行筛选，得到我们符合条件的所有key值（hscan可以进行模式匹配）。

为了方便，我们通常将符合条件的key全部放入到一个Set或是List中。这样一来，我们就可以根据得到的key值去取出相应的数据了。下面是模糊查询的演示图(其中field中的命名规则为`<id>:<姓名>:<性别>`，value为用户详情的json串)。

查询所有性别为女的用户

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67177ef4cb341455ad5b0e55/ad135c7b-9b06-4138-99de-01b15d360e42.webp)

图片

查询所有名字中姓阿的用户

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67177ef4cb341455ad5b0e55/b36e05ae-33ed-445b-bfd3-e7d969fac977.webp)

图片

HSCAN虽然为我们提供了模式匹配的功能，但这种匹配是基于遍历实现的，每一次匹配都需要遍历全部的key，效率上并不高。因此在下面一节会这方面进行补充，本节只谈如何实现模糊匹配。

## Redis的分页+多条件模糊查询组合实现

前面分别单独叙述了如何实现Redis的分页和多条件某查询。在实际使用中，单独使用ZSet实现分页已经能够展现不错的性能了，但存在一个问题是我们所分页的数据往往是伴随着一些动态的筛选条件的，而ZSet并不提供这样的功能。

面对这种情况，我们通常有两种解决方案：

1. 如果数据已经存储在了持久化数据库中，我们可以每次在数据库中做好条件查询再将数据放入Redis中进行分页。
2. 在Redis中实现多条件模糊查询并分页。


前者方案其实是一个不错的选择，但缺点在于数据有时候并不一定都在持久化数据库中。在有些业务场景下，我们的数据为了展现更好的并发性以及高响应，我们的数据会先放置在缓存数据库中，等到某个时间或者满足某种条件时再持久化到数据库中。

在这种情况下我们第一个方案就不起作用了，需要使用第二个方案。因此，下面将介绍如何实现多条件模糊查询的基础上进行分页。

### 实现思路

首先我们可以采用多条件模糊查询章节所说的方式，将我们所涉及到的条件字段作为hash的field，而数据的内容则作为对应value进行存储(一般以json格式存储，方便反序列化)。

我们需要实现约定好查询的格式，用前面一节的例子来说，field中的命名规则为`<id>:<姓名>:<性别>`，我们每次可以通过"`*`"来实现我们希望的模糊匹配条件，比如“`*：*：男`”就是匹配所有男性数据，“`100*：*：*`”就是匹配所有id前缀为100的用户。

当我们拿到了匹配串后我们先去Redis中寻找是否存在以该匹配串为key的ZSet，如果没有则通过Redis提供的HSCAN遍历所有hash的field，得到所有符合条件的field，并将其放入一个ZSet集合，同时将这个集合的key设置为我们的条件匹配串。如果已经存在了，则直接对这个ZSet进行分页查询即可。对ZSet进行分页的方式已经在前面叙述过了。通过这样的方式我们就实现了最简单的分页+多条件模糊查询。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67177ef4cb341455ad5b0e55/0656d478-39cd-4ba4-ae14-5136c12dc918.webp)

图片

上图中，由于并未在缓存数据库中找到符合的ZSet集合，我们将根据匹配串生成一个新的集合用于分页。

### 性能优化方案

虽然上文实现了多条件模糊查询+分页的功能，但是在时间开发中，我们不能无限制的生成新的集合，因为匹配串是很多样化的，这会给缓存带来巨大的压力。

因此我们在生成集合时可以赋予这个集合一个过期时间，到期集合会自动销毁。因为根据时间局部性原理，我们在一段时间内不访问的数据大概率在很长一顿时间内也不会再访问。而对于命中的集合，我们将更新其过期时间。

同时，我们数据的实时性也是一个问题，因为我们的集合是在生成集合时的Hash内容决定的，对于新插入到Hash的数据，集合是无法探知的，因此有两种解决方案：

- 第一种是插入到Hash时同时再插入到其他相应的集合中，保证数据一直是最新的，这种方式需要增加特殊前缀用于识别，否则我们也不清楚到底要插入到哪些集合中。
- 第二种方式是定时更新，这种方式比较省力，但无法保证分页数据的实时性。因此具体怎么选择还是取决于业务场景。


## 总结

本文大概地描述了实现分页和多条件模糊查询的方案，希望能够对大家有所帮助。

## 联系我

长按下方二维码添加我为好友！

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67177ef4cb341455ad5b0e55/ca5bb93e-4ed3-4c33-8718-aa385a604957.png)

## 推荐阅读

1. [28个Java开发最常用的软件下载、安装、配置、使用，Java开发必备！](http://mp.weixin.qq.com/s?__biz=MzkxOTUyMzEzMw==&mid=2247488311&idx=1&sn=efe70eaa94311eda0097b3b56fb1c439&chksm=c1a18965f6d6007399d02bebea7e8609909390ad539cad95eb86303c0439512a1542decfbfbb&scene=21#wechat_redirect)
2. [再也不用担心Linux命令记不住了，Linux必会命令，赶紧收藏，方便以后参考！](http://mp.weixin.qq.com/s?__biz=MzkxOTUyMzEzMw==&mid=2247488076&idx=1&sn=cce4a06c445d83b7317389dd2892882e&chksm=c1a1881ef6d6010866411556d4329d1526a94522c10c00bb89377c81802325cb0a1e9a77bd8c&scene=21#wechat_redirect)
3. [赶紧收藏，IDEA安装上这46款神级插件，效率直接起飞](http://mp.weixin.qq.com/s?__biz=MzkxOTUyMzEzMw==&mid=2247486894&idx=1&sn=58b2675842cec779c1158df596884968&chksm=c1a197fcf6d61eeabb1d4916bbfc56a1e222c59e316deb5f7618f58c345d4906b48ef3ec3988&scene=21#wechat_redirect)
4. [SpringBoot葵花宝典！最细SpringBoot教程，赶紧收藏学习！](http://mp.weixin.qq.com/s?__biz=MzkxOTUyMzEzMw==&mid=2247488088&idx=1&sn=03b6e52b21d6163ce044b19443114bee&chksm=c1a1880af6d6011cf3b4442b91389022d8803d09fc9e7263535a9845253cac8d64ab2c6ac4c5&scene=21#wechat_redirect)
5. [培训班？非科班？不懂算法？十大排序算法汇总，轻松学会算法，赶紧收藏学习！](http://mp.weixin.qq.com/s?__biz=MzkxOTUyMzEzMw==&mid=2247488069&idx=1&sn=e7d2a7979f092b93d85c64e2fc7c2e98&chksm=c1a18817f6d6010155bb24b8e6c8a145ac5af8fd18587273db77d03ba6c46c588d36317af3ea&scene=21#wechat_redirect)
6. [IDEA永久激活破解免费使用，支持Windows、Mac（超简单的图文保姆教程）](http://mp.weixin.qq.com/s?__biz=MzkxOTUyMzEzMw==&mid=2247485453&idx=1&sn=d9e68a61c0bcc449e602aab6654171b1&chksm=c1a1925ff6d61b4933999466124ebad46fa765ec85e5ea96a6efb691fdad7d931c20f34a519c&scene=21#wechat_redirect)


-------------------- END --------------------

点击下方，关注公众号程序员平安，观看更多精彩文章！

分享计算机相关的398本PDF电子书给你

原创文章和动画制作真心不易，您的点赞就是最大的支持！

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/67177ef4cb341455ad5b0e55/b3f524bc-77c5-448b-b29c-20f8f640820e.gif)


新枝标签： #模糊查询 #Redis #技术
