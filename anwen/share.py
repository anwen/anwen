# -*- coding:utf-8 -*-
import time
# import os
# from .api_base import JsonHandler
from random import randint
import markdown2
import tornado.web
import options
from utils.avatar import get_avatar
from db import User, Share, Comment, Like, Hit, Tag, Viewpoint
from .base import BaseHandler
from log import logger
from anwen.api_share import get_share_by_slug
# 网页版的接口


class OneShareHandler(BaseHandler):

    # 文章正文查看
    def get(self, slug):
        share = get_share_by_slug(slug)
        if not share:
            return self.write_error(404)

        if share.markdown:
            share.content = markdown2.markdown(share.markdown)
        user = User.by_sid(share.user_id)
        share.user_name = user.user_name
        share.user_domain = user.user_domain
        tags = ''
        if share.tags:
            tags += 'tags:'
            for i in share.tags.split(' '):
                tags += '<a href="/tag/%s">%s</a>  ' % (i, i)
        share.tags = tags

        user_id = int(
            self.current_user["user_id"]) if self.current_user else None
        like = Like.find_one(
            {'entity_id': share.id, 'user_id': user_id, 'entity_type': 'share'})
        share.is_liking = bool(like.likenum) if like else False
        share.is_disliking = bool(like.dislikenum) if like else False

        comments = []
        comment_res = Comment.find({'share_id': share.id})
        for comment in comment_res:
            user = User.by_sid(comment.user_id)
            comment.name = user.user_name
            comment.domain = user.user_domain
            comment.gravatar = get_avatar(user.user_email, 50)
            comments.append(comment)

        posts = Share.find()
        suggest = []
        for post in posts:
            post.score = 100 + post.id - post.user_id
            # post.score += post.likenum * 4 + post.hitnum * 0.01 + post.commentnum * 3
            post.score += randint(1, 999) * 0.001
            common_tags = [i for i in post.tags.split(
                ' ') if i in share.tags.split(' ')]
            # list(set(b1) & set(b2))
            post.score += len(common_tags)
            if post.sharetype == share.sharetype:
                post.score += 1  # todo
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
        share.viewpoints = Viewpoint.find(
            {'share_id': share.id}
        )
        # 未登录用户记录cookie
        if not user_id and not self.get_cookie(share.id):
            self.set_cookie(str(share.id), "1")
        self.render(
            "sharee.html", share=share, comments=comments,
            suggest=suggest)
        logger.info('stat hit')
        if user_id:
            hit = Hit.find(
                {'share_id': share.id},
                {'user_id': int(self.current_user["user_id"])},
            )
            if hit.count() == 0:
                hit = Hit
                hit['share_id'] = share.id
                hit['user_id'] = int(self.current_user["user_id"])
                hit.save()


class ShareHandler(BaseHandler):

    # 编辑器
    @tornado.web.authenticated
    def get(self):
        share_id = self.get_argument("id", None)
        sharetype = self.get_argument("sharetype", None)
        editor = self.get_argument("editor", options.default_editor)
        share = None
        if share_id:
            share = Share.by_sid(share_id)
            if 'vote_open' not in share:
                share.vote_open = 0
                share.vote_title = ''
            sharetype = share.sharetype if share else None
        if sharetype == 'goodlink':
            self.render("share_link.html", share=share)
        elif editor:
            self.render("share_wysiwyg.html", share=share)
        else:
            self.render("share.html", share=share)

    # 创建或者修改分享
    @tornado.web.authenticated
    def post(self):
        # print(self.request.arguments)
        share_id = self.get_argument("id", None)
        title = self.get_argument("title", '')
        markdown = self.get_argument("markdown", '')
        content = self.get_argument("content", '')
        sharetype = self.get_argument("sharetype", '')
        slug = self.get_argument("slug", '')
        tags = self.get_argument("tags", '')
        # upload_img = self.get_argument("uploadImg", '')
        post_img = self.get_argument("post_Img", '')
        link = self.get_argument("link", '')
        user_id = self.current_user["user_id"]
        vote_open = self.get_argument("vote_open", '')
        vote_title = self.get_argument("vote_title", '')
        if vote_open.isdigit():
            vote_open = int(vote_open)
        else:
            vote_open = 0
        res = {
            'title': title,
            'markdown': markdown,
            'content': content,
            'sharetype': sharetype,
            'slug': slug,
            'tags': tags,
            # 'upload_img': upload_img,
            'post_img': post_img,
            'link': link,
            'vote_open': vote_open,
            'vote_title': vote_title,
            'updated': time.time(),
        }
        if share_id:
            share = Share.by_sid(share_id)
            if not share:
                self.redirect("/404")
            share.update(res)
            share.save()
        else:
            share = Share
            res['user_id'] = user_id
            share = share.new(res)
            user = User.by_sid(user_id)
            user.user_leaf += 10
            user.save()
        for i in tags.strip().split(' '):
            doc = {
                'name': i,
                'share_ids': share.id
            }
            Tag.new(doc)
        self.redirect("/share/" + str(share.id))
