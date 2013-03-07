# -*- coding: utf-8 -*-

from anwen.index import IndexHandler, NodeHandler, TagHandler
from anwen.index import WelcomeHandler, RecommendedHandler, CollectionsHandler
from anwen.user import LoginHandler, JoinusHandler, LogoutHandler
from anwen.user import UserhomeHandler, UserlikeHandler
from anwen.user import SettingHandler, ChangePassHandler, UsersHandler
from anwen.share import ShareHandler, EntryHandler, CommentHandler, LikeHandler
from anwen.share import FeedHandler, SharesHandler, CommentsHandler
from anwen.share import ImageUploadHandler
from ande.ande import AndeHandler
from ande.videomeet import VideoMeetHandler, VideoMsgHandler
from anwen.talk import TalkHandler, ChatSocketHandler
from anwen.talk import MsgNewHandler, MsgUpdatesHandler
from anwen.other import EditHandler, ErrHandler, FeedbackHandler

handlers = [
    (r"/", IndexHandler),
    (r"/welcome", WelcomeHandler),
    (r"/recommended", RecommendedHandler),
    (r"/collections", CollectionsHandler),

    (r"/node/([^/]+)", NodeHandler),

    (r"/user/([^/]+)", UserhomeHandler),
    (r"/userlike/([^/]+)", UserlikeHandler),
    (r"/users/?", UsersHandler),
    (r'/users/([0-9a-f]{24})', UsersHandler),

    (r"/share/image_upload", ImageUploadHandler),
    (r"/share/?", ShareHandler),
    (r"/sharecomment", CommentHandler),
    (r"/sharelike/([^/]+)", LikeHandler),
    (r"/share/([^/]+)", EntryHandler),
    (r"/feed", FeedHandler),
    (r"/shares/?", SharesHandler),
    (r"/shares/([0-9a-f]{24})", SharesHandler),
    (r"/tag/?", TagHandler),
    (r"/tag/([^/]+)", TagHandler),

    (r"/comments/?", CommentsHandler),
    (r"/comments/([0-9a-f]{24})", CommentsHandler),

    (r"/login", LoginHandler),
    (r"/joinus", JoinusHandler),
    (r"/logout", LogoutHandler),
    (r'/setting', SettingHandler),
    (r'/changepass', ChangePassHandler),

    (r'/ande', AndeHandler),
    (r'/videomeet', VideoMeetHandler),
    (r'/videomeet/message', VideoMsgHandler),

    (r"/chat", TalkHandler),
    (r"/chats", TalkHandler),
    (r"/talk", TalkHandler),
    (r"/chatsocket", ChatSocketHandler),
    (r"/a/message/new", MsgNewHandler),
    (r"/a/message/updates", MsgUpdatesHandler),

    (r"/feedback", FeedbackHandler),
    (r"/edit", EditHandler),
    (r'/404/?', ErrHandler),

    (r'/(.*)', EntryHandler),

    # Custom 404 ErrHandler, always put this at last

]
