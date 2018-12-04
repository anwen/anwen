# -*- coding: utf-8 -*-
from db.model import connection
from db.model_user import User
from db.model_share import Share

Tag = connection.Tag
Viewpoint = connection.Viewpoint
Comment = connection.Comment
Like = connection.Like
Hit = connection.Hit
Feedback = connection.Feedback
Admin = connection.Admin
Ande = connection.Ande
Talk = connection.Talk
Webcache = connection.Webcache
# Vote = connection.Vote

connection.register([User])
connection.register([Share])
User = connection.User
Share = connection.Share
