# -*- coding:utf-8 -*-

import markdown2
import time
from random import randint
import tornado.web

from utils.avatar import get_avatar
from base import BaseHandler
from db import User, Share, Comment, Like, Hit
from base import CommonResourceHandler


class ShareHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        id = self.get_argument("id", None)
        share = None
        if id:
            share = Share.by_sid(id)
        self.render("share.html", share=share)

    @tornado.web.authenticated
    def post(self):
        id = self.get_argument("id", None)
        res = {
            'title': self.get_argument("title"),
            'markdown': self.get_argument("markdown"),
            'sharetype': self.get_argument("type"),
            'updated': time.time(),
        }

        if id:
            share = Share.by_sid(id)
            if not share:
                self.redirect("/404")
            print res['markdown']
            share.update(res)
            print share['markdown']
            share.save()
            print share['markdown']
        else:
            share = Share
            res['id'] = share.find().count() + 1
            res['user_id'] = int(self.current_user["user_id"])
            share.new(res)
            user = User.by_sid(self.current_user["user_id"])
            user.user_leaf += 10
            user.save()
        self.redirect("/share/" + str(share.id))


class EntryHandler(BaseHandler):
    def get(self, id):
        if id.isdigit():
            share = Share.by_sid(id)
        else:
            share = Share.by_slug(str(id))
        if not share:
            self.redirect("/404")
        share.hitnum += 1
        share.save()
        share.markdown = markdown2.markdown(share.markdown)
        comments = Comment.find({'share_id': share.id})
        for comment in comments:
            user = User.by_sid(comment.user_id)
            comment.name = user.user_name
            comment.domain = user.user_domain
            comment.gravatar = get_avatar(user.user_email, 50)

        if self.current_user:
            hit = Hit.find(
                {'share_id': share.id},
                {'user_id': int(self.current_user["user_id"])},
            )
            if hit.count() == 0:
                hit = Hit
                hit['share_id'] = share.id
                hit['user_id'] = int(self.current_user["user_id"])
                hit.save()
        else:
            if not self.get_cookie(share.id):
                self.set_cookie(str(share.id), "1")
        posts = Share.find()
        suggest = []
        for post in posts:
            post.score = 100 + post.id - post.user_id + post.commentnum * 3
            post.score += post.likenum * 4 + post.hitnum * 0.01
            post.score += randint(1, 999) * 0.001
            if post.sharetype == share.sharetype:
                post.score += 5
            if self.current_user:
                is_hitted = Hit.find(
                    {'share_id': share._id},
                    {'user_id': int(self.current_user["user_id"])},
                ).count() > 0
            else:
                is_hitted = self.get_cookie(share.id)
            if is_hitted:
                post.score -= 50
            suggest.append(post)
        suggest.sort(key=lambda obj: obj.get('score'))
        suggest = suggest[:5]
        self.render(
            "sharee.html", share=share, comments=comments,
            suggest=suggest)


class CommentHandler(BaseHandler):
    def post(self):
        commentbody = self.get_argument("commentbody", None)
        share_id = self.get_argument("share_id", None)
        html = markdown2.markdown(commentbody)
        comment = Comment
        comment['user_id'] = self.current_user["user_id"]
        comment['share_id'] = share_id
        comment['commentbody'] = commentbody
        comment.save()
        share = Share.by_sid(share_id)
        share.commentnum += 1
        share.save()
        name = tornado.escape.xhtml_escape(self.current_user["user_name"])
        gravatar = get_avatar(self.current_user["user_email"], 50)
        newcomment = ''
        newcomment += ' <div class="comment">'
        newcomment += '<div class="avatar">'
        newcomment += '<img src="' + gravatar + '" />'
        newcomment += '</div>'
        newcomment += '<div class="name">' + name + '</div>'
        newcomment += '<div class="date" title="at"></div>'
        newcomment += html
        newcomment += '</div>'
        self.write(newcomment)


class LikeHandler(BaseHandler):
    def post(self):
        share_id = self.get_argument("share_id", None)
        likenum = self.get_argument("likenum", 0)
        like = Like
        like['user_id'] = self.current_user["user_id"]
        like['share_id'] = share_id
        like.save()
        share = Share.by_sid(share_id)
        share.likenum += 1
        share.save()
        user = User.by_sid(share.user)
        user.user_leaf += 4
        user.save()
        user = User.by_sid(self.current_user["user_id"])
        user.user_leaf += 2
        user.save()
        likenum = int(likenum) + 1
        newlikes = ':) ' + str(likenum)
        self.write(newlikes)


class FeedHandler(BaseHandler):
    def get(self):
        shares = Share.find()
        self.set_header("Content-Type", "application/atom+xml")
        self.render("feed.xml", shares=shares)


class SharesHandler(CommonResourceHandler):
    res = Share

    def pre_post(self, json_arg):
        new_obj = self.res()
        new_obj.update(json_arg)
        if self.res.by_slug(new_obj.slug):
            self.send_error(409)
        else:
            new_obj.save()
            return new_obj
