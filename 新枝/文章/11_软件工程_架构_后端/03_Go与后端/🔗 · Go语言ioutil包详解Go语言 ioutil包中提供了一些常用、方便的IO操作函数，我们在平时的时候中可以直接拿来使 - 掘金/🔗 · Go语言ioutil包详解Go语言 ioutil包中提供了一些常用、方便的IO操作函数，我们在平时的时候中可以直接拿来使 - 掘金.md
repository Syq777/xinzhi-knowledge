---
作者:
  - "CodePlayer竟然被占用了"
原文链接: https://juejin.cn/post/7070917217776304141
发布时间: ""
收藏时间: "2024-11-15"
关联日记: "[[2024-11-15]]"
tags:
  - 文章
---
本文详解了 Go 语言的 ioutil 包，包括 readAll 等内部方法和 ReadAll 等外部方法，具体介绍了 ReadAll 等的功能、适用场景、使用示例及源码解读，还涵盖了 WriteFile、ReadDir、nopCloser、Discard 等的相关内容，最后总结了 ioutil 包中的各项要点。

关联问题: 如何优化ioutil性能  ioutil适用哪些场景  Discard还有何用途 

> 你必须非常努力，才能看起来毫不费力！微信搜索公众号[ 漫漫Coding路 ]，一起From Zero To Hero !

## 前言

Go语言 ioutil包中提供了一些常用、方便的IO操作函数，我们在平时的时候中可以直接拿来使用。对于IO读操作来说，比较适用于读小文件，因为相关方法都是一次性将内容读入内存，文件太大内存吃不消；对于其它内容，文章通过示例+分析源码的方式做了介绍，一起来看下吧！

相关知识：[Go 语言 bytes.Buffer 源码详解之1](https://link.juejin.cn/?target=https%3A%2F%2Fmp.weixin.qq.com%2Fs%3F__biz%3DMzU5NzU2NDk2MA%3D%3D%26mid%3D2247484928%26idx%3D1%26sn%3Dfa4a3158e26d5833f500281623adf776%26chksm%3Dfe50cd4fc92744599bc74b546d6e80f7d30471ed54258b232a3c1cd28173f87b086e3851009d%23rd)[Go 语言 bytes.Buffer 源码详解 2](https://link.juejin.cn/?target=https%3A%2F%2Fmp.weixin.qq.com%2Fs%3F__biz%3DMzU5NzU2NDk2MA%3D%3D%26mid%3D2247484955%26idx%3D1%26sn%3D2c042542cb7994dfd21dbc36041a9215%26chksm%3Dfe50cd54c9274442078b31bd7afea6766d7d4412157bcf86d01c1b4abd401909d35ea3f5d046%26token%3D900175827%26lang%3Dzh_CN%23rd)

## readAll

readAll 是一个内部方法，从入参 reader 中读取全部数据，然后返回读取到的数据以及产生的 error，主要是调用 butes.Buffer 的 ReadFrom 方法（读取完数据产生的EOF error 在这里不算做 error，因为目的就是读取完数据）。

```
// io.Reader r : 保存着底层数据，数据从 r 中读取
// capacity： 用于设置保存数据的字节缓冲区的初始容量，但是在读取过程中会自动扩容的

func readAll(r io.Reader, capacity int64) (b []byte, err error) {
	var buf bytes.Buffer

	// 如果字节缓冲区在读取过程中一直扩容，最终超出了系统设置的最大容量，会产生 ErrTooLarge panic，在这里捕获，改为返回一个 error
	// 如果是其他类型的 panic，保持 panic
	defer func() {
		e := recover()
		if e == nil {
			return
		}
		if panicErr, ok := e.(error); ok && panicErr == bytes.ErrTooLarge {
			err = panicErr
		} else {
			panic(e)
		}
	}()

	// 设置默认容量
	if int64(int(capacity)) == capacity {
		buf.Grow(int(capacity))
	}

	// 读取数据
	_, err = buf.ReadFrom(r)
	return buf.Bytes(), err
}
```

## ReadAll

ReadAll 方法，我们比较常用的工具类方法，一次性读取文件的所有内容并返回，适用于读取小文件，如果文件太大会占用太多内存。调用 ReadAll 方法成功，会读取 io.Reader r 的所有内容，返回的 err == nil，而不是 err == EOF，因为读取完所有数据了，完成了我们的任务，此时 EOF 不应当是 error。

**使用示例**

```
func main() {
	file, err := os.Open("test.txt")
	if err != nil {
		fmt.Println("open file err")
		return
	}

	c, err := ioutil.ReadAll(file)
	fmt.Println(err)
	fmt.Println(string(c))
}
```

**源码解读**

```
func ReadAll(r io.Reader) ([]byte, error) {
	// 直接调用内部 readAll 方法，默认容量为 512 字节
	return readAll(r, bytes.MinRead)
}
```

## ReadFile

ReadFile 根据文件名读取文件，返回文件的所有内容以及读取过程中产生的error，与ReadAll类似，读取完文件后，EOF 不算做 error，因为已经完成了任务。

**使用示例**

```
func main() {
	c, err := ioutil.ReadFile("test.txt")
	fmt.Println(err)
	fmt.Println(string(c))
}
```

**源码解读**

```
func ReadFile(filename string) ([]byte, error) {
	f, err := os.Open(filename)
	if err != nil {
		return nil, err
	}
	defer f.Close()

	// 初始化缓冲区的默认容量，如果我们后续获得了文件大小信息，再更新缓冲区容量
	var n int64 = bytes.MinRead

	// 获取文件信息
	if fi, err := f.Stat(); err == nil {
		// 为了防止 Size == 0, 多分配了 MinRead 个字节的容量，并且防止在填充完缓冲区后再次的分配
		// 如果Stat() 方法返回的Size 信息有误，我们要么会浪费一些空间，要么会根据需要重新分配空间，
		// 但是大多数情况下我们能获取到正确的信息
		if size := fi.Size() + bytes.MinRead; size > n {
			n = size
		}
	}
	// 调用 readAll 方法读取数据
	return readAll(f, n)
}
```

## WriteFile

WriteFile 方法将数据写入文件，如果文件不存在，会先新建文件；如果已存在，会把之前的数据先清空再写入

**使用示例**

```
func main() {

	var buffer bytes.Buffer

	for i := 0; i < 100; i++ {
		buffer.WriteString("this is line " + fmt.Sprintf("%d", i) + "\n")
	}

	if err := ioutil.WriteFile("testFile", buffer.Bytes(), 0644); err != nil {
		fmt.Println(err)
	}

}
```

**源码解读**

```
// filename指定了文件名，data是要写入的数据，perm 指定了文件权限（如 0644）
func WriteFile(filename string, data []byte, perm os.FileMode) error {

	// 调用os.OpenFile 方法创建打开文件
	f, err := os.OpenFile(filename, os.O_WRONLY|os.O_CREATE|os.O_TRUNC, perm)
	if err != nil {
		return err
	}

	// 写入数据
	_, err = f.Write(data)
	if err1 := f.Close(); err == nil {
		err = err1
	}
	return err
}
```

## ReadDir

ReadDir 用于获取文件夹下面的所有文件信息(文件夹+文件)，返回的数据是文件名有序的

**使用示例**

```
func main() {
	fileList, err := ioutil.ReadDir("/Users/admin/study")
	for _, f := range fileList {
		fmt.Println(f.Name(), f.IsDir())
	}
	fmt.Println(err)
}

/*
1.log false
composetest true
hello.sh false
student.txt false
wordpress true
<nil>
 */
```

**源码解读**

```
func ReadDir(dirname string) ([]os.FileInfo, error) {
	f, err := os.Open(dirname)
	if err != nil {
		return nil, err
	}
	list, err := f.Readdir(-1)
	f.Close()
	if err != nil {
		return nil, err
	}
	sort.Slice(list, func(i, j int) bool { return list[i].Name() < list[j].Name() })
	return list, nil
}
```

## nopCloser

`nopCloser` 的作用是将一个 io.Reader 类型包装成为了 io.ReadCloser 类型, 实现了 Close() 方法，但什么也没做，只是返回了 nil。

**使用示例**

在我们需要将一个 io.Reader 类型包装成 io.ReadCloser 类型时，可以直接调用该方法，比如Go 原生的 http NewRequestWithContext 方法，就直接使用了该方法：

```
func NewRequestWithContext(ctx context.Context, method, url string, body io.Reader) (*Request, error) {
	
  ......
  
  // 传入的 body 是 io.Reader 类型，如果不是 io.ReadCloser 类型，调用 ioutil.NopCloser 转一下
	rc, ok := body.(io.ReadCloser)
	if !ok && body != nil {
		rc = ioutil.NopCloser(body)
	}
  
  .......
}
```

**源码解读**

```
type nopCloser struct {
	io.Reader
}

func (nopCloser) Close() error { return nil }

// NopCloser 传入一个 io.Reader 类型，返回 io.ReadCloser 类型
func NopCloser(r io.Reader) io.ReadCloser {
	return nopCloser{r}
}
```

## Discard

`Discard` 如名字一样，是一个用于丢弃数据的地方，虽然有时候我们不在意数据内容，但可能存在数据不读出来就无法关闭连接的情况，这时候就可以使用 io.Copy(ioutil.Discard, io.Reader) 将数据写入 Discard。Discard 是 io.Writer 类型，是通过 devNull 定义得来的，devNull 实现了 Write 方法（其实什么都没做，直接返回长度，永远成功）

**使用示例**

Go 原生 http 包，server.go 就使用了 io.Copy(ioutil.Discard, mb)

```
func (globalOptionsHandler) ServeHTTP(w ResponseWriter, r *Request) {
	w.Header().Set("Content-Length", "0")
	if r.ContentLength != 0 {
		// Read up to 4KB of OPTIONS body (as mentioned in the
		// spec as being reserved for future use), but anything
		// over that is considered a waste of server resources
		// (or an attack) and we abort and close the connection,
		// courtesy of MaxBytesReader's EOF behavior.
		mb := MaxBytesReader(w, r.Body, 4<<10)
		io.Copy(ioutil.Discard, mb)
	}
}
```

**源码解读**

```
var Discard io.Writer = devNull(0)


type devNull int

var _ io.ReaderFrom = devNull(0)

// 实现了 Write 方法，什么也不做，直接返回长度
func (devNull) Write(p []byte) (int, error) {
	return len(p), nil
}

// 实现了 WriteString 方法，什么也不做，直接返回长度

func (devNull) WriteString(s string) (int, error) {
	return len(s), nil
}

// sync.Pool 用来做变量复用的，因为我们根本不在意数据内容，只是为了将数据读出来，
// 为了减少内存分配，提高读取时的字节切片复用程度，使用了 sync.Pool，它就像一个黑洞，丢数据进去就行

var blackHolePool = sync.Pool{
	New: func() interface{} {
		b := make([]byte, 8192)
		return &b
	},
}

// 从 blackHolePool 中获取字节切片 bufp ， 将 io.Reader 的数据读入 bufp，
// 然后再将 bufp 丢入 blackHolePool，如此往复，只使用了一个变量
func (devNull) ReadFrom(r io.Reader) (n int64, err error) {
	bufp := blackHolePool.Get().(*[]byte)
	readSize := 0
	for {
		readSize, err = r.Read(*bufp)
		n += int64(readSize)
		if err != nil {
			blackHolePool.Put(bufp)
			if err == io.EOF {
				return n, nil
			}
			return
		}
	}
}
```

## 总结

本篇文章我们介绍了 `ioutil` 包中的相关内容：

- readAll：内部方法，读取所有数据
- ReadAll：外部方法，读取所有数据
- ReadFile：读取文件所有内容
- WriteFile：写入文件内容，如果文件存在会先清空原有内容
- ReadDir：返回文件夹下文件列表
- nopCloser：将io.Reader 类型包装成 io.ReadCloser 类型
- Discard：用于丢弃数据


## 更多

个人博客: [lifelmy.github.io/](https://link.juejin.cn/?target=https%3A%2F%2Flifelmy.github.io%2F)

微信公众号：漫漫Coding路

