# -*- coding: utf-8 -*-

from anwen.index import IndexHandler, NodeHandler, TagHandler
from anwen.user import LoginHandler, JoinusHandler, LogoutHandler
from anwen.user import UserhomeHandler, UserlikeHandler
from anwen.user import SettingHandler, ChangePassHandler, UsersHandler
from anwen.share import ShareHandler, EntryHandler, CommentHandler, LikeHandler
from anwen.share import FeedHandler, SharesHandler
from ande.ande import AndeHandler
# from ande.andenew import AndeNewHandler
from anwen.talk import TalkHandler, ChatSocketHandler
from anwen.talk import MsgNewHandler, MsgUpdatesHandler
from anwen.other import EditHandler, ErrHandler

handlers = [
    (r"/", IndexHandler),

    (r"/node/([^/]+)", NodeHandler),

    (r"/user/([^/]+)", UserhomeHandler),
    (r"/userlike/([^/]+)", UserlikeHandler),
    (r"/users/?", UsersHandler),
    (r'/users/([0-9a-f]{24})', UsersHandler),


    (r"/share/?", ShareHandler),
    (r"/sharecomment", CommentHandler),
    (r"/sharelike", LikeHandler),
    (r"/share/([^/]+)", EntryHandler),
    (r"/feed", FeedHandler),
    (r"/shares/?", SharesHandler),
    (r"/shares/([0-9a-f]{24})", SharesHandler),
    (r"/tag/?", TagHandler),
    (r"/tag/([^/]+)", TagHandler),

    (r"/login", LoginHandler),
    (r"/joinus", JoinusHandler),
    (r"/logout", LogoutHandler),
    (r'/setting', SettingHandler),
    (r'/changepass', ChangePassHandler),

    (r'/ande', AndeHandler),
    # (r'/andenew', AndeNewHandler),

    (r"/chat", TalkHandler),
    (r"/chats", TalkHandler),
    (r"/talk", TalkHandler),
    (r"/chatsocket", ChatSocketHandler),
    (r"/a/message/new", MsgNewHandler),
    (r"/a/message/updates", MsgUpdatesHandler),

    (r"/edit", EditHandler),

    (r'/(.*)', EntryHandler),
    # Custom 404 ErrHandler, always put this at last
    (r'/404/?', ErrHandler),

]
