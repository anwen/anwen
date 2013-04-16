# -*- coding:utf-8 -*-

import markdown2
import time
import os
import Image
import datetime
from random import randint
import tornado.web

import options
from utils.avatar import get_avatar
from utils.img_tools import make_post_thumb
from db import User, Share, Comment, Like, Hit, Tag
from base import CommonResourceHandler, BaseHandler


class ShareHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        share_id = self.get_argument("id", None)
        share = None
        if share_id:
            share = Share.by_sid(share_id)
        editor = self.get_argument("editor", None)
        if editor:
            self.render("share_wysiwyg.html", share=share)
        else:
            self.render("share.html", share=share)

    @tornado.web.authenticated
    def post(self):
        # print self.request.arguments
        share_id = self.get_argument("id", None)
        status = 1 if self.get_argument("dosubmit", None) == u'保存草稿' else 0
        tags = self.get_argument("tags", '')
        upload_img = self.get_argument("uploadImg", '')
        post_img = self.get_argument("post_Img", '')
        post_img = '' if post_img == 'None' else post_img
        user_id = self.current_user["user_id"]
        res = {
            'title': self.get_argument("title"),
            'markdown': self.get_argument("markdown"),
            'sharetype': self.get_argument("type"),
            'slug': self.get_argument("slug", ''),
            'tags': tags,
            'status': status,
            'upload_img': upload_img,
            'post_img': post_img,
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
        for i in tags.split(' '):
            doc = {
                'name': i,
                'share_ids': share.id
            }
            Tag.new(doc)
        if status == 1:
            self.redirect("/share/?id=" + str(share.id))
        self.redirect("/share/" + str(share.id))


class EntryHandler(BaseHandler):
    def get(self, slug):
        share = None
        if slug.isdigit():
            share = Share.by_sid(slug)
        else:
            share = Share.by_slug(slug)
        if share:
            share.hitnum += 1
            share.save()
            share.markdown = markdown2.markdown(share.markdown)
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
                {'share_id': share.id, 'user_id': user_id})
            share.is_liking = bool(like.likenum % 2) if like else None
            share.is_disliking = bool(like.dislikenum % 2) if like else None
            comments = []
            comment_res = Comment.find({'share_id': share.id})
            for comment in comment_res:
                user = User.by_sid(comment.user_id)
                comment.name = user.user_name
                comment.domain = user.user_domain
                comment.gravatar = get_avatar(user.user_email, 50)
                comments.append(comment)

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
            else:
                if not self.get_cookie(share.id):
                    self.set_cookie(str(share.id), "1")
            posts = Share.find()
            suggest = []
            for post in posts:
                post.score = 100 + post.id - post.user_id + post.commentnum * 3
                post.score += post.likenum * 4 + post.hitnum * 0.01
                post.score += randint(1, 999) * 0.001
                common_tags = [i for i in post.tags.split(
                    ' ') if i in share.tags.split(' ')]
                # list(set(b1) & set(b2))
                post.score += len(common_tags)
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
        else:
            old = 'http://blog.anwensf.com/'
            for i in options.old_links:
                if slug in i:
                    self.redirect('%s%s' % (old, i), permanent=True)
                    break
                    return
            self.redirect("/404")


class CommentHandler(BaseHandler):
    def post(self):
        commentbody = self.get_argument("commentbody", None)
        share_id = self.get_argument("share_id", None)
        html = markdown2.markdown(commentbody)
        comment = Comment
        doc = {}
        doc['user_id'] = self.current_user["user_id"]
        doc['share_id'] = int(share_id)
        doc['commentbody'] = commentbody
        comment.new(doc)
        share = Share.by_sid(share_id)
        share.commentnum += 1
        share.save()
        name = tornado.escape.xhtml_escape(self.current_user["user_name"])
        gravatar = get_avatar(self.current_user["user_email"], 50)
        newcomment = ''.join([
            '<div class="comment">',
            '<div class="avatar">',
            '<img src="', gravatar,
            '</div>',
            '<div class="name">', name,
            '</div>',
            '<div class="date" title="at"></div>', html,
            '</div>',
        ])
        self.write(newcomment)


class CommentsHandler(CommonResourceHandler):
    res = Comment


class LikeHandler(BaseHandler):
    def post(self, action):
        share_id = int(self.get_argument("share_id", None))
        user_id = self.current_user["user_id"]
        doc = {
            'user_id': user_id,
            'share_id': share_id
        }
        if action == 'addlike':
            Like.change_like(doc, 'likenum')
            share = Share.by_sid(share_id)
            share.likenum += 1
            share.save()
            user = User.by_sid(share.user_id)
            user.user_leaf += 4
            user.save()
            user = User.by_sid(user_id)
            user.user_leaf += 2
            user.save()
            newlikes = str(share.likenum)
        elif action == 'dellike':
            Like.change_like(doc, 'likenum')
            share = Share.by_sid(share_id)
            share.likenum -= 1
            share.save()
            user = User.by_sid(share.user_id)
            user.user_leaf -= 4
            user.save()
            user = User.by_sid(user_id)
            user.user_leaf -= 2
            user.save()
            newlikes = str(share.likenum)
        elif action == 'adddislike':
            Like.change_like(doc, 'dislikenum')
            share = Share.by_sid(share_id)
            share.dislikenum += 1
            share.save()
            newlikes = str(share.dislikenum)
        elif action == 'deldislike':
            Like.change_like(doc, 'dislikenum')
            share = Share.by_sid(share_id)
            share.dislikenum -= 1
            share.save()
            newlikes = str(share.dislikenum)
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


class ImageUploadHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self):
        img = None
        if 'uploadImg' in self.request.files:
            img = self.request.files['uploadImg'][0]
            ext = os.path.splitext(img['filename'])[1].lower()
            body = img['body']
        if img and len(body) > 2 * 1024 * 1024:
            msg = {"status": "o", "info": "上传的图片不能超过2M"}
        elif ext and ext in ['.jpg', '.jpeg', '.gif', '.png', '.bmp']:
            img_dir = 'static/upload/img'
            now = datetime.datetime.now()
            t = now.strftime('%Y%m%d_%H%M%S_%f')
            img_name = '%s%s' % (t, ext)
            img_path = '%s/%s' % (img_dir, img_name)
            with open(img_path, 'wb') as image:
                image.write(body)
            im = Image.open(img_path)
            width, height = im.size
            if width / height > 5 or height / width > 5:
                os.remove(img_path)  # 判断比例 删除图片
                msg = {"status": "s", "info": "请不要上传长宽比例过大的图片"}
            else:
                make_post_thumb(img_path)  # 创建1200x550 750x230 365x230缩略图
                pic_1200 = '%s_1200.jpg' % t
                # users.save_user_avatar(user_id, avatar)#入库
                msg = {"status": "y", "pic_1200": pic_1200}
        else:
            msg = '{"status": "s", "info": "目前只支持jpg/gif/png/bmp格式的图片。"}'
        print msg
        self.write_json(msg)

    @tornado.web.authenticated
    def delete(self):
        img_name = self.request.body.split('img_name=')[1]
        img_dir = 'static/upload/img'
        for i in os.listdir(img_dir):
            if i.startswith(img_name):
                os.remove(img_dir + '/' + i)
        self.write("s")
