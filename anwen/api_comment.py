# -*- coding:utf-8 -*-
from .api_base import JsonHandler
from db import Share, Comment, User
import tornado.escape
from utils.avatar import get_avatar_by_wechat
# , get_avatar_by_feed, get_avatar
import options
# IMG_BASE = 'https://anwensf.com/static/upload/img/'


class CommentHandler(JsonHandler):

    def get(self):  # list all comments of a article
        # log api usage
        share_id = self.get_argument("share_id", None)
        comments = []
        comment_res = Comment.find({'share_id': int(share_id)})
        for comment in comment_res:
            comment = dict(comment)

            # comment['_id'] = str(comment['_id'])
            comment.pop('_id')
            comment['pushlished'] = int(comment['commenttime'] * 1000)
            comment['content'] = comment['commentbody']

            user_id = comment['user_id']
            comment['avatar'] = options.site_url+get_avatar_by_wechat(user_id)
            # 这里节省数据库查询
            # user = User.by_sid(comment['user_id'])
            # get_avatar(user.user_email, 50)

            # if user.user_email.endswith('@wechat'):
            #     comment['avatar'] = options.site_url + \
            #         get_avatar_by_wechat(user_id)
            # if user.user_email.endswith('@anwensf.com'):
            #     comment['avatar'] = options.site_url + \
            #         get_avatar_by_feed(user_id)
            # else:
            #     comment['avatar'] = options.site_url + \
            #         get_avatar(user_user_email, 100)

            comment.pop('commenttime')
            comment.pop('commentbody')
            comment.pop('user_id')

            comment['likeNum'] = comment['likenum']
            comment['dislikeNum'] = comment['dislikenum']
            comment['userName'] = comment['user_name']
            comment.pop('likenum')
            comment.pop('dislikenum')
            comment.pop('user_name')

            comments.append(comment)
        self.res = {
            'comments': comments,
        }
        self.write_json()

    # replyId: 2, // 对回复的评论ID (选填)
    # images: ['', ''], // 评论的图片链接

    @tornado.web.authenticated
    def post(self):
        share_id = self.get_argument("id", None)
        commentbody = self.get_argument("content", None)
        if not share_id:
            share_id = self.get_argument("share_id", None)
        if not commentbody:
            commentbody = self.get_argument("commentbody", None)
        comment = Comment
        doc = {}
        doc['user_id'] = self.current_user["user_id"]
        user = User.by_sid(self.current_user["user_id"])
        # user_name in current_user is not the newest
        if not user["user_name"]:
            user["user_name"] = '-'
        doc['user_name'] = user["user_name"]
        doc['share_id'] = int(share_id)
        doc['commentbody'] = commentbody
        comment.new(doc)
        share = Share.by_sid(share_id)
        share.commentnum += 1
        share.save()
        # name = tornado.escape.xhtml_escape(self.current_user["user_name"])
        # gravatar = get_avatar(self.current_user["user_email"], 50)
        # self.res = {
        #     'success': True,
        # }
        self.write_json()
