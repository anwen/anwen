# -*- coding:utf-8 -*-

import markdown2
from random import randint

from utils.fliter import filter_tags
from utils.avatar import get_avatar
from base import BaseHandler
import options
from db import User, Share, Comment, Like, Hit
from pymongo import DESCENDING  # ASCENDING


class IndexHandler(BaseHandler):
    def get(self):
        page = self.get_argument("page", 1)
        share_res = Share.find().sort(
            '_id', DESCENDING).limit(10).skip((int(page) - 1) * 10)

        pagesum = (share_res.count() + 9) / 10
        print share_res.count()
        shares = []
        for share in share_res:
            user = User.by_sid(share.user_id)
            share.name = user.user_name
            share.domain = user.user_domain
            share.markdown = filter_tags(
                markdown2.markdown(share.markdown))[:100]
            share.gravatar = get_avatar(user.user_email, 16)
            shares.append(share)
        members = User.find().sort('_id', DESCENDING).limit(20)  # ASCENDING
        members_dict = []
        for member in members:
            member.gravatar = get_avatar(member.user_email, 25)
            members_dict.append(member)
        node = 'home'
        node_about = options.node_about[node]
        self.render(
            "node.html", shares=shares, members=members_dict,
            pagesum=pagesum, page=page, node=node, node_about=node_about)


class NodeHandler(BaseHandler):
    def get(self, node):
        page = self.get_argument("page", 1)
        share_res = Share.find({'sharetype': node}).sort(
            '_id', DESCENDING).limit(10).skip((int(page) - 1) * 10)
        pagesum = (share_res.count() + 9) / 10

        shares = []
        for share in share_res:
            user = User.by_sid(share.user_id)
            share.name = user.user_name
            share.domain = user.user_domain
            share.markdown = filter_tags(
                markdown2.markdown(share.markdown))[:100]
            share.gravatar = get_avatar(user.user_email, 16)
            shares.append(share)
        members = User.find().sort('_id', DESCENDING).limit(20)
        members_dict = []
        for member in members:
            member.gravatar = get_avatar(member.user_email, 25)
            members_dict.append(member)
        node_about = options.node_about[node]
        self.render(
            "node.html", shares=shares, members=members_dict,
            pagesum=pagesum, page=page, node=node, node_about=node_about)


class SpecialHandler(BaseHandler):
    def get(self):
        slug = self.request.path[1:]
        share = Share.by_slug(str(slug))
        if not share:
            self.redirect("/404")
        else:
            share.markdown = markdown2.markdown(share.markdown)
            if self.current_user:
                share.is_liking = Like.find(
                    {'share_id': share._id},
                    {'user_id': int(self.current_user["user_id"])},
                ).count() > 0
            comments = Comment.find({'share_id': share._id})
            for comment in comments:
                user = User.find({'_id': comment.user_id})
                comment.name = user.user_name
                comment.domain = user.user_domain
                comment.gravatar = get_avatar(user.user_email, 50)
            share.update({"$inc": {'hitnum': 1}})
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
            suggest = {}
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
                suggest[post.score] = post.id
            realsuggest = []
            i = 1
            for key in sorted(suggest.iterkeys(), reverse=True):
                post = Share.by_sid(suggest[key])
                share_post = {
                    'id': post.id,
                    'title': post.title, }
                realsuggest.append(share_post)
                i = i + 1
                if i > 3:
                    break
            self.render(
                "sharee.html", share=share, comments=comments,
                realsuggest=realsuggest)


class NotyetHandler(BaseHandler):
    def get(self):
        self.render("404.html")
