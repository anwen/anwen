# -*- coding: utf-8 -*-
# apis
from anwen import api
from anwen import api_user
from anwen import api_share
from anwen import api_shares
from anwen import api_like
from anwen import api_collect
from anwen import api_tag
from anwen import api_comment
from anwen import api_upload
from anwen import api_stat

from anwen import page_welcome


# pages

# from anwen.index import WelcomeHandler
# from anwen.index import IndexHandler
# from anwen.index import ExploreHandler
from anwen.index import NodeHandler
from anwen.index import TagHandler

# from anwen.share import ShareHandler
from anwen.share import OneShareHandler
from anwen.share_by_get import ShareByGetHandler

from anwen.comment import CommentHandler
from anwen.other import FeedHandler
from anwen.other import ViewPointHandler

from anwen.other import EditHandler, ErrHandler, FeedbackHandler, ScoreHandler
from anwen.other import AppHandler
from anwen.other import TogetherHandler


from anwen.users import UsersHandler


from anwen.user import LoginHandler, JoinusHandler, LogoutHandler
# from anwen.user import GoogleLoginHandler, DoubanLoginHandler
from anwen.user import ForgotPassHandler, SetPassHandler
from anwen.user import ChangePassHandler
from anwen.user_setting import SettingHandler
from anwen.user import UserhomeHandler, UserlikeHandler


from anwen.admin import AdminHandler, BecomeAdminHandler
from anwen.admin import AdminShareHandler


from ande.ande import AndeHandler

from atalk.talk import TalkHandler, ChatSocketHandler
from atalk.talk import MsgNewHandler  # MsgUpdatesHandler


handlers = [
    # auth
    (r"/api/authorizations", api_user.AuthorizationsHandler),
    (r"/api/wxlogin", api_user.WxLoginHandler),
    (r"/api/me", api_user.MeHandler),
    # content
    (r"/api/shares/?", api_shares.SharesHandler),
    (r"/api/v2/shares/?", api_shares.SharesV2Handler),

    (r"/api/shares/([^/]+)", api_share.ShareHandler),

    (r"/api/v2/tags", api_tag.TagsV2Handler),
    (r"/api/tags", api_tag.TagsV2Handler),
    (r"/api/v1/tags", api_tag.TagsHandler),
    # (r"/api/tag", api_tag.TagHandler),


    # actions
    (r"/api/my_like", api_like.MyLikeHandler),
    (r"/api/my_collect", api_collect.MyCollectHandler),
    (r"/api/like/([^/]+)", api_like.LikeHandler),
    (r"/api/collect/([^/]+)", api_collect.CollectHandler),
    (r"/api/comment", api_comment.CommentHandler),
    (r"/api/image_upload", api_upload.ImageUploadHandler),

    # debug
    (r"/api/preview", api_share.PreviewHandler),
    # stat
    (r"/api", api.ApiHandler),
    (r"/api/stat", api_stat.StatHandler),


    # delete
    # (r"/api/users", api_user.UsersHandler),


    # pages
    (r"/explore", NodeHandler),  # node=home
    (r"/node/([^/]+)", NodeHandler),

    # static or redirect
    (r"/welcome", page_welcome.WelcomeHandler),
    (r"/", page_welcome.IndexHandler),

    # others
    (r"/share_by_get/?", ShareByGetHandler),
    (r"/share/?", ShareHandler),
    (r"/share/([^/]+)", OneShareHandler),

    (r"/sharecomment", CommentHandler),
    (r"/feed", FeedHandler),

    (r"/viewpoint", ViewPointHandler),

    (r"/users", UsersHandler),

    (r"/tag/?", TagHandler),
    (r"/tag/([^/]+)", TagHandler),

    (r"/login", LoginHandler),
    (r"/joinus", JoinusHandler),
    (r"/logout", LogoutHandler),
    # (r"/google_login", GoogleLoginHandler),
    # (r"/douban_login", DoubanLoginHandler),
    (r'/forgotpass', ForgotPassHandler),
    (r'/setpass', SetPassHandler),
    (r'/setting', SettingHandler),
    (r'/changepass', ChangePassHandler),
    (r"/user/([^/]+)", UserhomeHandler),
    (r"/userlike/([^/]+)", UserlikeHandler),

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
    # (r"/a/message/updates", MsgUpdatesHandler),

    (r"/app", AppHandler),
    (r"/together", TogetherHandler),

    # (r'/(.*)', NotfountHandler),
    # (r'/(.*)', OneShareHandler),
    # Custom 404 ErrHandler, always put this at last

]
