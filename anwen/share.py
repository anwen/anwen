# -*- coding:utf-8 -*-
u"""文章分享，非API."""
import time
# import os
# from .api_base import JsonHandler
from random import randint
import markdown2
import tornado.web
import options
from utils.avatar import get_avatar
from db import User, Share, Comment, Like, Hit, Tag, Viewpoint, Webcache
from .base import BaseHandler
from anwen.api_share import get_share_by_slug, add_hit_stat
import requests
import html2text
from readability import Document

try:
    from urllib.parse import urlparse
except:
    from urlparse import urlparse  # Python 2

# 网页版的接口


def format_tags(share):
    tags = ''
    if share.tags:
        tags += 'tags:'
        for i in share.tags.split(' '):
            tags += '<a href="/tag/%s">%s</a>  ' % (i, i)
    return tags


def get_comments(share):
    comments = []
    comment_res = Comment.find({'share_id': share.id})
    for comment in comment_res:
        user = User.by_sid(comment.user_id)
        comment.name = user.user_name
        comment.domain = user.user_domain
        comment.gravatar = get_avatar(user.user_email, 50)
        comments.append(comment)
    return comments


class OneShareHandler(BaseHandler):
    u"""文章正文查看."""

    def get(self, slug):
        share = get_share_by_slug(slug)
        if not share:
            return self.write_error(404)

        # for web
        user = User.by_sid(share.user_id)
        share.author_name = user.user_name
        share.author_domain = user.user_domain
        share.tags = format_tags(share)
        if share.markdown:
            share.content = markdown2.markdown(share.markdown)
        # 对于链接分享类，增加原文预览
        if share.link:
            # Webcache should add index
            doc = Webcache.find_one({'url': share.link}, {'_id': 0})
            # 此文章须经作者同意 转载 禁止转载
            if doc and doc['markdown'] and '禁止转载' not in doc['markdown']:
                doc['markdown'] = doc['markdown'].replace('本文授权转自', '')
                md = share['markdown']
                md += '\n\n--预览--\n\n' + doc['markdown']
                md += '\n\n[阅读原文]({})'.format(doc['url'])

                parsed_uri = urlparse(share.link)
                domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
                md = md.replace('![image](/', '![image]({}/'.format(domain))
                md = md.replace('\n* \n', '\n\n')
                md = md.replace('\n*\n', '\n\n')
                while '\n\n\n' in md:
                    md = md.replace('\n\n\n', '\n\n')
                share.content = markdown2.markdown(md)

        user_id = self.current_user["user_id"] if self.current_user else None
        like = Like.find_one(
            {'entity_id': share.id, 'user_id': user_id, 'entity_type': 'share'})
        share.is_liking = bool(like.likenum) if like else False
        share.is_disliking = bool(like.dislikenum) if like else False

        suggest = []
        comments = get_comments(share)

        share.viewpoints = Viewpoint.find({'share_id': share.id})
        # 未登录用户记录访问cookie
        if not user_id and not self.get_cookie(share.id):
            self.set_cookie(str(share.id), "1")
        self.render(
            "sharee.html", share=share, comments=comments,
            suggest=suggest)
        add_hit_stat(user_id, share)
        return
        # 文章推荐
        suggest = []
        posts = Share.find()
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
                    {'share_id': share.id},
                    {'user_id': int(self.current_user["user_id"])},
                ).count() > 0
            else:
                is_hitted = self.get_cookie(share.id)
            if is_hitted:
                post.score -= 50
            suggest.append(post)
        suggest.sort(key=lambda obj: obj.get('score'))
        suggest = suggest[:5]


class ShareHandler(BaseHandler):
    u"""编辑器."""

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

        if link:
            url = link
            doc = Webcache.find_one({'url': url}, {'_id': 0})
            if not doc:
                try:
                    sessions = requests.session()
                    sessions.headers[
                        'User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36'
                    response = sessions.get(url)
                    # response.encoding = 'utf-8'
                    doc = Document(response.text)
                    doc_title = doc.title()
                    summary = doc.summary()
                    _markdown = html2text.html2text(summary)
                    _markdown = _markdown.replace('-\n', '-').strip()
                    res_webcache = {}
                    res_webcache['url'] = url
                    res_webcache['title'] = doc_title
                    res_webcache['markdown'] = _markdown
                    if _markdown:
                        webcache = Webcache
                        webcache.new(res_webcache)
                except Exception as e:
                    print(e)
                    self.redirect("/")
                    return

        if vote_open.isdigit():
            vote_open = int(vote_open)
        else:
            vote_open = 0
        if not title:
            title = doc_title
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
        if not markdown:
            self.redirect("/")
            return
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
