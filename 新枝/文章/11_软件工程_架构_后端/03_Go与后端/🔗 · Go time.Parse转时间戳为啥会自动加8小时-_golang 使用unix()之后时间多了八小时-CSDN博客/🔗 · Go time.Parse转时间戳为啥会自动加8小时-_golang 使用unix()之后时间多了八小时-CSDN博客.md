---
作者:
  - "成就一亿技术人!"
原文链接: https://blog.csdn.net/jxwBlog/article/details/111033829
发布时间: ""
收藏时间: "2025-04-22"
关联日记: "[[2025-04-22]]"
tags:
  - 文章
---
![图片](https://csdnimg.cn/release/blogv2/dist/pc/img/original.png)

[i小明同学](https://blog.csdn.net/jxwBlog)![图片](https://csdnimg.cn/release/blogv2/dist/pc/img/newCurrentTime2.png)于 2020-12-11 13:53:47 发布

版权声明：本文为博主原创文章，遵循[ CC 4.0 BY-SA ](http://creativecommons.org/licenses/by-sa/4.0/)版权协议，转载请附上原文出处链接和本声明。 

今天在Go里面写业务时,遇到了时间转换问题

time.Parse转[时间戳](https://so.csdn.net/so/search?q=%E6%97%B6%E9%97%B4%E6%88%B3&spm=1001.2101.3001.7020)会自动加8小时,然后费解就找原因...

先看下示例代码:

```
package main import time func main() { 	t := time.Now().Unix() 	d := time.Unix(t, 0).Format("2006-01-02 15:04:05") 	tt, _ := time.Parse("2006-01-02 15:04:05", d) println("===========================") println("当前时间戳:", t) println("当前日期:", d) println("从日期得到时间戳:", tt.Unix()) println("再次转化为日期:", time.Unix(tt.Unix(), 0).Format("2006-01-02 15:04:05")) println("===========================") }
```

一脸懵逼:

```
运行结果: =========================== 当前时间戳: 1490019356 当前日期: 2017-03-20 22:15:56 从日期得到时间戳: 1490048156 再次转化为日期: 2017-03-21 06:15:56 ===========================
```

翻了一遍golang[package](https://so.csdn.net/so/search?q=package&spm=1001.2101.3001.7020)，原来 time 还有这个方法:

```
func ParseInLocation(layout, value string, loc *Location) (Time, error)
```

只需要 loc 参数传 time.Local 就OK了

原因是:time默认用utc和我们差8个小时

所以直接使用ParseInLocation就好了:

```
time.ParseInLocation("2006-01-02 15:04:05", time_string, time.Local)
```

