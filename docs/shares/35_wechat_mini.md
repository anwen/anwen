安问小程序开发
========


一直支持开放的互联网，微信还是太封闭了。
所以很晚才注册微信订阅号，也直到现在才注册小程序。
知己知彼，才能打败封闭的互联网。

刚开始开发，以下是一些用到的参考资料，按照需求google搜索得到，不成体系。

## 设计准则
- 对于获取用户信息不做旧版本兼容，面向未来开发
- 不强制获取用户信息

## 参考资料
- <https://www.jianshu.com/p/f82262002f8a> 布局
- <https://blog.csdn.net/u013778905/article/details/54349373> 启动页面
- <https://developers.weixin.qq.com/blogdetail?action=get_post_info&lang=zh_CN&token=1394082127&docid=0000a26e1aca6012e896a517556c01&devtools=1&idescene=3> 关于获取用户头像和名称信息（没有唯一id，不等于登录）
- <https://www.jianshu.com/p/4d8365cfa7ee>  微信 unionid openid 区别
- <https://www.huxiu.com/article/36734/1.html> UnionID和微信登陆的野心是“连接一切”
- <https://blog.csdn.net/qq_33616529/article/details/79080141>  有图，很清晰
- <https://www.jianshu.com/p/c5f6c98b2685>  微信小程序中用户登录和登录态维护
- <https://github.com/gusibi/python-weixin>  encryptedData解密  或者参考官方sample代码。 （如果靠code去使用js2code接口和微信换取openid的话，这个openid是不可靠的，需要使用getuserinfo的加密数据解密之后的openid和之前js2code接口获取的openid对比之后，才能保证这个openid的可靠。？？？）
- <https://blog.csdn.net/towtotow/article/details/78064911> 获取access_token 暂时没发现怎么用