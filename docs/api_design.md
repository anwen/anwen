better api
========

## 已公布的 OpenAPI 规范目标
定义标准的、独立于语言的指向 REST API 的接口，使得服务能力无需访问源代码、文档，或是借助于网络流量检查，就可被人类和计算机发现并理解。通过对 OpenAPI 做适当定义后，消费者可使用最小数量的实现逻辑理解远程服务，并与远程服务交互。







http://localhost:8888/api
https://anwensf.com/api


current_user_url: 'user'
authorizations_url: 'authorizations'
user_url: 'users/{user}'
gists_url: 'gists{/gist_id}'


GraphQL

## Features
Emphasis on REST
Authentication
Rate Limiting

Full range of CRUD operations
Filtering and Sorting
Pagination
HATEOAS
Data Validation


emails_url: 'user/emails'
followers_url: 'user/followers'
following_url: 'user/following{/target}'

emojis_url: 'emojis'
events_url: 'events'
feeds_url: 'feeds'
rate_limit_url: 'rate_limit'


current_user_authorizations_html_url: 'https://github.com/settings/connections/applications{/client_id}'
code_search_url: 'search/code?q={query}{&page,per_page,sort,order}'
commit_search_url: 'search/commits?q={query}{&page,per_page,sort,order}'
issue_search_url: 'search/issues?q={query}{&page,per_page,sort,order}'
hub_url: 'hub'
issues_url: 'issues'
keys_url: 'user/keys'
notifications_url: 'notifications'
organization_repositories_url: 'orgs/{org}/repos{?type,page,per_page,sort}'
organization_url: 'orgs/{org}'
public_gists_url: 'gists/public'
repository_search_url: 'search/repositories?q={query}{&page,per_page,sort,order}'
current_user_repositories_url: 'user/repos{?type,page,per_page,sort}'
team_url: 'teams'
user_repositories_url: 'users/{user}/repos{?type,page,per_page,sort}'
user_search_url: 'search/users?q={query}{&page,per_page,sort,order}'

repository_url: 'repos/{owner}/{repo}'
starred_url: 'user/starred{/owner}{/repo}'
starred_gists_url: 'gists/starred'
user_organizations_url: 'user/orgs'



/users/:username/repos
/users/:org/repos
/repos/:owner/:repo
/repos/:owner/:repo/tags
/repos/:owner/:repo/branches/:branch

GET /repos/:owner/:repo/issues
GET /repos/:owner/:repo/issues/:number
POST /repos/:owner/:repo/issues
PATCH /repos/:owner/:repo/issues/:number
DELETE /repos/:owner/:repo

比如“喜欢”一个 gist，就增加一个 /gists/:id/star 子资源，然后对其进行操作：“喜欢”使用 PUT /gists/:id/star，“取消喜欢”使用 DELETE /gists/:id/star 。


X-RateLimit-Limit: 用户每个小时允许发送请求的最大值
X-RateLimit-Remaining：当前时间窗口剩下的可用请求数目
X-RateLimit-Rest: 时间窗口重置的时候，到这个时间点可用的请求数量就会变成 X-RateLimit-Limit 的值


如果允许没有登录的用户使用 API（可以让用户试用），可以把 X-RateLimit-Limit 的值设置得很小，比如 Github 使用的 60。没有登录的用户是按照请求的 IP 来确定的，而登录的用户按照认证后的信息来确定身份。


对于超过流量的请求，可以返回 429 Too many requests 状态码，并附带错误信息。而 Github API 返回的是 403 Forbidden，虽然没有 429 更准确，也是可以理解的。

