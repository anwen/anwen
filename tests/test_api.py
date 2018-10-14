import requests


api = 'http://localhost:8888/'


# api/shares 全部文章 GET
# api/shares?has_vote=1 支持投票的文章 GET
# api/shares/33 具体的一篇文章 GET
# api/comment?share_id=34 GET为列出所有评论，POST为添加评论
# api/authorizations 授权接口（邮箱和密码 登录，暂未支持注册）。支持basic auth 和token auth GET
# api/wxlogin 授权接口（微信）。目前不太规范只支持 GET
# api/me 需授权 获取和更新用户信息接口，支持GET POST
# api/like/addlike 需授权 POST params: entity_id entity_type return: newlikes
# 其中 entity_type为：share comment viewpoint（分别是文章、评论和观点）
# 其实还有取消喜欢，不喜欢和取消不喜欢的接口，应该暂时不需要


def test_shares():
    url = api + 'api/shares'
