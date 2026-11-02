---
作者:
原文链接: https://golang.dbwu.tech/introduction/func_closures/
发布时间: ""
收藏时间: "2024-10-21"
关联日记: "[[2024-10-21]]"
tags:
  - 文章
---
![Menu](https://golang.dbwu.tech/svg/menu.svg)

**Func Closures**![Table of Contents](https://golang.dbwu.tech/svg/toc.svg)

## 概述 #

闭包的概念参考 [闭包 - 维基百科](https://zh.wikipedia.org/wiki/%E9%97%AD%E5%8C%85_%28%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%A7%91%E5%AD%A6%29) 。

## 例子 #

## 自增序列号生成器 #

```
package main

import "fmt"

// 自增序列号生成器
func incSeq() func() int {
	i := 0
	return func() int {
		i++
		return i
	}
}

func main() {
	next := incSeq()

	fmt.Printf("初始值 = %d\n", next())

	for i := 1; i <= 5; i++ {
		fmt.Printf("第 %d 次迭代后, 值 = %d\n", i, next())
	}
}

// $ go run main.go
// 输出如下 
/**
  初始值 = 1
  第 1 次迭代后, 值 = 2
  第 2 次迭代后, 值 = 3
  第 3 次迭代后, 值 = 4
  第 4 次迭代后, 值 = 5
  第 5 次迭代后, 值 = 6
*/
```

![图片](https://dbwu.tech/images/wechat.png)

## 转载申请

本作品采用 [知识共享署名 4.0 国际许可协议](http://creativecommons.org/licenses/by/4.0/) 进行许可，转载时请注明原文链接，图片在使用时请保留全部内容，商业转载请联系作者获得授权。 

[ © 蛮荆 ](https://dbwu.tech/) | ![图片](https://dbwu.tech/images/%E5%A4%87%E6%A1%88%E5%9B%BE%E6%A0%87.png)[陕公网安备 61011302001681 号](http://www.beian.gov.cn/portal/registerSystemInfo?recordcode=61011302001681) | [陕ICP备2023004378号-1](https://beian.miit.gov.cn/) | [Rendered by Hugo](https://themes.gohugo.io/themes/hugo-book/)

