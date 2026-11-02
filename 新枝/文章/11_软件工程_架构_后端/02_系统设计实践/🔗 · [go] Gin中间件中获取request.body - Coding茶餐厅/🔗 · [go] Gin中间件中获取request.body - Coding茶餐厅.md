---
作者:
  - "By"
原文链接: http://razil.cc/post/2019/04/go_gin_middleware_request_body/
发布时间: ""
收藏时间: "2024-11-15"
关联日记: "[[2024-11-15]]"
tags:
  - 文章
---
## [go] Gin中间件中获取request.body

2019年04月21日

## 背景

[参考issue](https://github.com/gin-gonic/gin/issues/1295)

线上有个中间件开发需求，需要对请求内容进行部分过滤。由于默认http.Request.Body类型为`io.ReadCloser`类型,即只能读一次，读完后直接close掉,后续流程无法继续读取。这对于在http handler之前需要对body进行处理就带来了麻烦。实际上针对这种需求，其他框架有自己的解决方案。 在beego中开启 `beego.BConfig.CopyRequestBody = true`后,Controller对应gin的Context中即包含了request.body的拷贝值，可以直接在中间件和Handler中传递。 但是Gin实际上并未提供该功能，issue中的GetRawBody本质也未能解决这个问题。 最后在stackoverflow找到问题解决方案,在这里做个记录,[how-to-get-the-json-from-the-body-of-a-request-on-go](https://stackoverflow.com/questions/47186741/how-to-get-the-json-from-the-body-of-a-request-on-go/47295689#47295689) > ps:该解决方案同样适用于http原生路由http.ServeMux处理方法。

## 解决方案

解决思路: 由于 Request.Body 为公共变量,我们在对原有的buffer读取完成后,只要手动创建一个新的buffer然后以同样接口形式替换掉原有的Request.Body即可。

```
var bodyBytes []byte // 我们需要的body内容

// 从原有Request.Body读取
bodyBytes, err := ioutil.ReadAll(c.Request.Body)
if err != nil {
	return 0, nil, fmt.Errorf("Invalid request body")
}

// 新建缓冲区并替换原有Request.body
c.Request.Body = ioutil.NopCloser(bytes.NewBuffer(bodyBytes))

// 当前函数可以使用body内容
_ := bodyBytes
```

## 引用

- [issue](https://github.com/gin-gonic/gin/issues/1295)
- [解决](https://stackoverflow.com/questions/47186741/how-to-get-the-json-from-the-body-of-a-request-on-go/47295689#47295689)


