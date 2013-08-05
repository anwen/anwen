# -*- coding: utf-8 -*-

from anwen.index import WelcomeHandler
from anwen.index import IndexHandler, StartHandler, ExploreHandler
from anwen.index import NodeHandler, TagHandler

from anwen.user import LoginHandler, JoinusHandler, LogoutHandler
from anwen.user import GoogleLoginHandler, DoubanLoginHandler
from anwen.user import ForgotPassHandler, SetPassHandler
from anwen.user import SettingHandler, ChangePassHandler
from anwen.user import UserhomeHandler, UserlikeHandler
from anwen.user import UsersHandler

from anwen.share import ShareHandler, EntryHandler, CommentHandler, LikeHandler
from anwen.share import FeedHandler
from anwen.share import ImageUploadHandler
from anwen.share import SharesHandler, CommentsHandler

from anwen.admin import AdminHandler, BecomeAdminHandler
from anwen.admin import AdminShareHandler

from anwen.other import EditHandler, ErrHandler, FeedbackHandler, ScoreHandler

from ande.ande import AndeHandler

from atalk.talk import TalkHandler, ChatSocketHandler
from atalk.talk import MsgNewHandler, MsgUpdatesHandler

from anwen.other import AppHandler

handlers = [
    (r"/welcome", WelcomeHandler),
    (r"/", IndexHandler),
    (r"/start", StartHandler),
    (r"/explore", ExploreHandler),

    (r"/node/([^/]+)", NodeHandler),
    (r"/tag/?", TagHandler),
    (r"/tag/([^/]+)", TagHandler),

    (r"/login", LoginHandler),
    (r"/joinus", JoinusHandler),
    (r"/logout", LogoutHandler),
    (r"/google_login", GoogleLoginHandler),
    (r"/douban_login", DoubanLoginHandler),
    (r'/forgotpass', ForgotPassHandler),
    (r'/setpass', SetPassHandler),
    (r'/setting', SettingHandler),
    (r'/changepass', ChangePassHandler),
    (r"/user/([^/]+)", UserhomeHandler),
    (r"/userlike/([^/]+)", UserlikeHandler),
    (r"/users/?", UsersHandler),
    (r'/users/([0-9a-f]{24})', UsersHandler),

    (r"/share/image_upload", ImageUploadHandler),
    (r"/share/?", ShareHandler),
    (r"/share/([^/]+)", EntryHandler),
    (r"/sharecomment", CommentHandler),
    (r"/sharelike/([^/]+)", LikeHandler),
    (r"/feed", FeedHandler),

    (r"/shares/?", SharesHandler),
    (r"/shares/([0-9a-f]{24})", SharesHandler),
    (r"/comments/?", CommentsHandler),
    (r"/comments/([0-9a-f]{24})", CommentsHandler),

    (r"/admin/become/?", BecomeAdminHandler),
    (r"/admin/share/?", AdminShareHandler),
    (r"/admin/?", AdminHandler),

    (r"/score/([^/]+)", ScoreHandler),
    (r"/feedback", FeedbackHandler),
    (r"/edit", EditHandler),
    (r'/404', ErrHandler),

    (r'/ande', AndeHandler),

    (r"/chat", TalkHandler),
    (r"/chats", TalkHandler),
    (r"/talks", TalkHandler),
    (r"/talk", TalkHandler),
    (r"/chatsocket", ChatSocketHandler),
    (r"/a/message/new", MsgNewHandler),
    (r"/a/message/updates", MsgUpdatesHandler),

    (r"/app", AppHandler),

    (r'/(.*)', EntryHandler),
    # Custom 404 ErrHandler, always put this at last

]
