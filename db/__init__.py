# -*- coding: utf-8 -*-
from db.model import connection
from db.model_user import User

Tag = connection.Tag
Viewpoint = connection.Viewpoint
Share = connection.Share
Comment = connection.Comment
Like = connection.Like
Hit = connection.Hit
Feedback = connection.Feedback
Admin = connection.Admin
Ande = connection.Ande
Talk = connection.Talk
Webcache = connection.Webcache
# Vote = connection.Vote

# User = connection.User
connection.register([User])
