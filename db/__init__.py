# -*- coding: utf-8 -*-
from db.model import connection
from db.model_user import User
from db.model_share import Share
from db.model_collect import Collect
from db.model_like import Like
from db.model_tag import Tag


connection.register([User])
connection.register([Share])
connection.register([Collect])
connection.register([Like])
connection.register([Tag])

User = connection.User
Share = connection.Share
Collect = connection.Collect
Like = connection.Like
Tag = connection.Tag


Hit = connection.Hit
Comment = connection.Comment
Feedback = connection.Feedback
Admin = connection.Admin
Ande = connection.Ande
Webcache = connection.Webcache
Viewpoint = connection.Viewpoint
Talk = connection.Talk
# Vote = connection.Vote


# db.auth(username, password)
# db.col1.ensureIndex({'tags':1})
# db.getCollectionNames()
# db.Share_Col.getIndexes()
# db.Share_Col.ensureIndex({'tags': 1})
# db.Share_Col.ensureIndex({'id': 1})
# db.Share_Col.find({'tags': '科幻'})
