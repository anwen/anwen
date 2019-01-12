安问API文档
========


作为完美主义者以及语义网和自然语言理解开发者，希望内容质量高的同时，接口也简洁清晰、语义化。

## endpoint
- <https://anwensf.com/api>

## RESTful风格的API设计规范
- 我们尽量遵循RESTful风格的API设计规范。（时间有限，可能部分接口还不太规范）。
- 使用 HTTPS。 增强网站的安全性
- 以资源为中心的 URL 设计
- 选择合适的状态码
- 错误处理：给出详细的信息
- 验证和授权
- 限流 rate limit （TODO）
-  Hypermedia API (HATEOAS)  在返回结果中提供链接，连向其他API方法，使得用户或者机器人不查文档，也知道下一步应该做什么。比如 <https://anwensf.com/api>
- 编写优秀的文档。 如果HATEOAS做得足够好，这一条可以省略
- 注意：目前接口没有status 和msg，之后会补上。
- 所有POST接口的内容都以json的形式发送
- 代码和小程序源码已开源（尽量及时更新）：<https://github.com/anwen/anwen>

## 目前开放的接口
### 文章相关
- <https://anwensf.com/api/shares> 全部文章 GET page per_page
- <https://anwensf.com/api/shares?has_vote=1> 支持投票的文章 GET
- <https://anwensf.com/api/shares?tag=杂文> 按照tag选文章的文章 GET
- <https://anwensf.com/api/shares/33> 具体的一篇文章 GET
- <https://anwensf.com/api/my_like> 喜欢的文章 GET page per_page
- <https://anwensf.com/api/my_collect> 收藏的文章 GET page per_page

### 文章相关信息
- <https://anwensf.com/api/comment?share_id=34> GET为列出所有评论，POST为添加评论
- <https://anwensf.com/api/tags> 列出全部tags

### 授权相关
- <https://anwensf.com/api/authorizations>  授权接口（邮箱和密码 登录，暂未支持注册）。支持basic auth 和token auth GET
- <https://anwensf.com/api/wxlogin>  授权接口（微信）。目前不太规范只支持 GET
- <https://anwensf.com/api/me>  **需授权**  获取和更新用户信息接口，支持GET  POST  字段: tags(string)
- <https://anwensf.com/api/like/addlike>  **需授权**  POST params: `entity_id entity_type` return: newlikes   其中 entity_type为：share comment viewpoint（分别是文章、评论和观点） 其实还有取消喜欢，不喜欢和取消不喜欢的接口，应该暂时不需要
- <https://anwensf.com/api/like/addcollect>  **需授权**  POST params: `entity_id entity_type`      其中 entity_type为：share comment viewpoint（分别是文章、评论和观点）


### 详细说明

    // GET /api/wxlogin  params: code  return {'token': the_token}
    // 参考代码:
    wx.request({
        url: 'https://anwensf.com/api/wxlogin',
        data: {code: code},
        header: {
            'content-type': 'application/json' // 默认值
        },
        success: function(res) {
            getApp().globalData.token = res.data.token;
        }
    }
    // --------- 之后需要授权才能访问的接口需要header中带token ------------------
    // POST /api/me  params: nickName city  say（其他头像等显示暂时没有支持，say是个性签名，各参数都是选填）  return 各项用户信息
    // 参考代码:
    wx.request({
        url: 'https://anwensf.com/api/me',
        method: 'POST',
        data: info,
        header: {
            'content-type': 'application/json', // 默认值
            'Authorization': 'token '+app.globalData.token
        },
        success: function(res) {
            app.globalData.userInfo = e.detail.userInfo
            app.globalData.hasUserInfo = true
            that.setData({
              userInfo: e.detail.userInfo,
              hasUserInfo: true
            })
        }
    })


## 参考资料
- <http://cizixs.com/2016/12/12/restful-api-design-guide>  5星
- [Restful API 首次被提出的论文：Architectural Styles and the Design of Network-based Software Architectures](http://www.ics.uci.edu/~fielding/pubs/dissertation/top.htm)
- <http://www.ruanyifeng.com/blog/2011/09/restful.html>
- <https://github.com/aisuhua/restful-api-design-references> 资源汇总
- <http://www.ruanyifeng.com/blog/2014/05/restful_api.html> 简单教程
- <https://www.jianshu.com/p/65b9e54dee7d>  科普
- <https://zhuanlan.zhihu.com/p/20034107> 一些细节