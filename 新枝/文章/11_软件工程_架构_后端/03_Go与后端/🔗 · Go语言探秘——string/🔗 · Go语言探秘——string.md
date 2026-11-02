---
作者:
  - "IT杨秀才"
原文链接: https://mp.weixin.qq.com/s?__biz=Mzk0MTYxNDgyNA==&amp;mid=2247483721&amp;idx=1&amp;sn=57040bfed7bf41e14888faa8301cecd7&amp;chksm=c3ea4ce77bae5c4ac9a98ea6c37e36b67944be4e4697ac8710ce3baa4156a09199a70b04a9da&amp;mpshare=1&amp;scene=1&amp;srcid=0902VNtuiCmVzBRj3Rd1xWpY&amp;sharer_shareinfo=00f9cfe5701e488f5ab1f4adb69484b8&amp;sharer_shareinfo_first=00f9cfe5701e488f5ab1f4adb69484b8#rd
发布时间: ""
收藏时间: "2025-09-02"
关联日记: "[[2025-09-02]]"
tags:
  - 文章
---
string是什么

在我们编程过程中，字符串可以说是我们使用的最多的一个数据结构了，凡是涉及到文本处理的地方，我们都会用到字符串。在go语言中，字符串其实就是一串由UTF-8编码的字符序列。

接下来我们看一下官方库对string的一个描述

```
var text string
```

在IDE里面定义一个text的string变量，点击string跳转到其类型定义的地方，可从源代码看到对string的描述，源代码的位置在src/builtin/builtin.go，描述如下：

```
// string is the set of all strings of 8-bit bytes, conventionally but not
// necessarily representing UTF-8-encoded text. A string may be empty, but
// not nil. Values of string type are immutable.
type string string
```

翻译一下，可以这样理解：

- 字符串是所有8bit 字节的集合，但不一定是 UTF-8 编码的文本
- 字符串可以为empty，但不能为 nil ，empty字符串就是一个没有任何字符的空串""
- 字符串不可以被修改，所以字符串类型的值是不可变的


所以字符串的本质是一串字符数组，每个字符在存储时都对应一个整数，也有可能对应多个整数，具体要看字符串的编码方式，可以看个例子：

```
package main

import (
   "fmt"
   "time"
)

func main() {
   ss := "Hello"
   for _, v := range ss {
      fmt.Printf("%d\n", v)
   }
}
```

运行结果：

```
s[0]: 72
s[1]: 101
s[2]: 108
s[3]: 108
s[4]: 111
```

可以看到，字符串的位置每个字符对应这个1个整数

string数据结构

go语言在src/runtime/string.go文件中对string的结构进行了定义

```
type stringStruct struct {
   str unsafe.Pointer
   len int
}
```

stringStruct 包含两个字段，str 类型为unsafe.Pointer，还有一个int类型的len字段。

- **str指向字符串的首地址**
- **len表示字符串的长度**


定义一个word字符串：

```
word := "Hello"
```

其底层结构如下图：

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68b649fead843515e3bda495/1ffc01f0-599a-46bf-a2c4-89f0e8ecde2d.png)

在本例中，len的长度为5，表示word这个字符串占用的字节数，每个字节的值如图中所示。这里需要注意，len字段存储的是实际的字节数，而不是字符数，所以对于非单字节编码的字符，其结果可能多于字符个数

我们知道了在runtime里string的定义，但是我们平常写代码似乎并没有用到stringStruct 结构，它是在什么地方被用到呢？

其实stringStruct 是字符串在运行时状态下的表现，当我们创建一个string的时候，可以理解为有两步：

1. 根据给定的字符创建出stringStruct 结构
2. 将stringStruct 结构转化为string类型


通过观察字符串的结构定义我们可以发现，其定义中并没有一个表示容量(Cap)的字段，所以意味着字符串类型并不能被扩容，字符串上的写操作包括拼接，追加等等都是通过拷贝来实现的。

string与[]byte互相转换

前面我们说了，string是只读的，不可以被改变，但是我们在编码过程中，进行重新赋值也是很正常的，既然可以重新赋值，为什么说不能被修改呢，这不是互相矛盾吗？

这里要弄弄清楚一个概念，字符串修改并不等于重新赋值。我们在开发中所使用的，其实是对字符串的重新赋值

```
str := "Hello"
str = "Golang"   // 重新赋值
str[0] = "I"     // 修改，不允许
```

示例：

```
package main

import "fmt"

func main() {
   var ss string
   ss = "Hello"
   ss[1] = "A"
   fmt.Println(ss)
}
```

运行结果：

```
.\main.go:8:2: cannot assign to ss[1] (value of type byte)
```

程序会报错，提示string是不可修改的。

这样一分析，那么可不可以将字符串转化为字节数组，然后通过下标修改字节数组，再转化回字符串呢，答案是可行的，相互转化的语法如下例所示：

```
package main

import "fmt"

func main() {
   var ss string
   ss = "Hello"
   strByte := []byte(ss)
   strByte[1] = 65
   fmt.Println(string(strByte))
}
```

运行结果：

```
HAllo
```

Hello变成了HAllo，好像达到了我们的目的。这里需要注意，虽然这种方式看似可行，修改了字符串Hello，但其实并不是我们所见的这样。最终得到的只是ss字符串的一个拷贝，原字符串并没有变化。

string与[]byte转换原理

string与[]byte的转化其实会发生一次内存拷贝，并申请一块新的切片内存空间，

byte 切片转化为string，大致过程分为三步：

1. 新申请切片内存空间，构建内存地址为addr，长度为len
2. 构建 string对象，指针地址为addr，len字段赋值为len（string.str = addr；string.len = len）
3. 将原切片中数据拷贝到新申请的string中指针指向的内存空间


![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68b649fead843515e3bda495/81ce4ae1-cd07-4ce7-b3cb-363d1e80f8b1.png)

string转化为byte数组同样简单，大致分为两步：

1. 新申请切片内存空间
2. 将string中指针执行内存区域的内容拷贝到新切片


![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68b649fead843515e3bda495/8135446e-da96-4466-af26-9b7db2770b4d.png)

string声明

go语言中以字面量来声明字符串有两种方式，双引号和反引号:

```
str1 := "Hello World"
str2 := `Hello
Golang`
```

使用双引号声明的字符串和其他语言中的字符串没有太多的区别，但是这种使用双引号的字符串只能用于单行字符串的初始化，当字符串里使用到一些特殊字符，比如双引号，换行符等等需要用\进行转义。但是，反引号声明的字符串没有这些限制，字符内容即为字符串里的原始内容，所以一般用反引号来声明比较复杂的字符串，比如json串。

```
json := `{"hello": "golang", "name": ["zhangsan"]}`
```

string为什么这么设计

可能大家都会考虑到，为什么一个普通的字符串要设计这么复杂，还需要使用指针。暂时没找到官方文档的说明，

个人猜想，当遇到一个非常长的字符时，这样做使得 string 变得非常轻量，可以很方便的进行传递而不用担心内存拷贝。虽然在 Go 中，不管是引用类型还是值类型参数传递都是值传递。但指针明显比值传递更节省内存。

