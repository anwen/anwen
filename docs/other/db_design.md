数据库设计
========

保持简单
sudo service mongod start
sudo service mongod stop
mongod --auth -f /etc/mongod.conf --fork
db.enableFreeMonitoring()

User
Admin
Share
Tag
Comment
Hit
Feedback
Like
Viewpoint

实体
user share comment viewpoint tag
属性-动作
hit like

someone create user
someone create feedback

user follow user
user create share
user create comment
user create viewpoint
user create tag
user create like
user create hit

share has user
share relate share
share has comment
share has viewpoint
share has tag
share has like
share has hit

comment relate user
comment relate share
comment relate comment
comment relate viewpoint
comment has like
comment -- tag
comment -- hit

viewpoint relate user
viewpoint relate share
viewpoint relate comment
viewpoint relate viewpoint
viewpoint has like
viewpoint -- tag
viewpoint -- hit

tag relate user
tag relate share
tag -- comment
tag -- viewpoint
tag -- like
tag -- tag
tag -- hit


entity_zid
entity_type entity_id
设计
user_1
share_1
comment_1
viewpoint_1

全平台贡献 leaf 可以任何时候统计得出

share 被 喜欢，作者获得leaf



Share
title: "",
id: 17,
published: 1352418858,
upload_img: null,
user_id: 1,
post_img: null,

updated: 1359181625.999205,
commentnum: 1,
content: null,
dislikenum: 0,
hitnum: 3413
likenum: 0,
link: "",
markdown: ""
score: 9.559000000000001,
sharetype: "fire",
slug: "ande-growup-log",
status: 0,
suggestscore: 0,
tags: "人工智能",
