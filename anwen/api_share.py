# -*- coding:utf-8 -*-
from .api_base import JsonHandler
from db import Share, Like, Viewpoint, Hit, Webcache
from random import randint
import random
import requests
from readability import Document
import html2text
from tornado.escape import json_decode
from log import logger
wx_admin_ids = (60, 63, 64)


def add_hit_stat(user_id, share):
    # 访问统计
    logger.info('stat hit')
    if user_id:
        hit = Hit.find(
            {'share_id': share.id},
            {'user_id': user_id},
        )
        # TODO 增加访问次数统计
        if hit.count() == 0:
            hit = Hit
            hit['share_id'] = share.id
            hit['user_id'] = user_id
            hit.save()


def get_share_by_slug(slug):
    # 特殊id ramdom
    if slug == 'random':
        cond = {}
        cond['status'] = {'$gte': 1}
        # shares = Share.find(cond, {'_id': 0})
        shares = Share.find(cond)
        share = random.choice(list(shares))
    elif slug.isdigit():
        share = Share.by_sid(slug)
    else:
        share = Share.by_slug(slug)
    if share:
        share.hitnum += 1
        share.save()
        share.pop('_id')
    return share


class ShareHandler(JsonHandler):

    # 单篇文章
    def get(self, slug):
        share = get_share_by_slug(slug)
        if not share:
            return self.write_error(404)
        # 小程序客户端
        # 时间格式转换
        share.published = int(share.published * 1000)
        share.updated = int(share.updated * 1000)
        # 暂时不显示作者
        user_id = self.current_user["user_id"] if self.current_user else None
        like = Like.find_one(
            {'share_id': share.id, 'user_id': user_id})
        d_share = dict(share)
        d_share['is_liking'] = bool(like.likenum) if like else False
        d_share['is_disliking'] = bool(like.dislikenum) if like else False
        # 对于链接分享类，增加原文预览
        if d_share.get('link'):
            # Webcache should add index
            doc = Webcache.find_one({'url': d_share['link']}, {'_id': 0})
            if doc and doc['markdown'] and '禁止转载' not in doc['markdown']:
                doc['markdown'] = doc['markdown'].replace('本文授权转自', '')
                d_share['markdown'] += '\n\n--预览--\n\n' + doc['markdown']
                d_share['markdown'] += '\n\n[阅读原文]({})'.format(doc['url'])
            # 添加原文链接
            d_share['url'] = '预览： <a href="{}">{}</a>'.format(
                share.link, share.title)

        viewpoints = Viewpoint.find({'share_id': share.id}, {'_id': 0})
        d_share['viewpoints'] = list(viewpoints)
        self.res = d_share
        self.write_json()
        add_hit_stat(user_id, share)


class SharesHandler(JsonHandler):

    # 文章列表
    # 不同权限的用户看到的列表不同
    def get(self):
        user = None
        token = self.request.headers.get('Authorization', '')
        if token:
            key, token = token.split()
            if key == 'token' and token:
                user_json = self.get_secure_cookie('user', token)
                if user_json:
                    user = json_decode(user_json)

        vote_open = self.get_argument("vote_open", None)
        has_vote = self.get_argument("has_vote", None)
        cond = {}

        logger.info('token: {}'.format(token))
        if user:
            logger.info('user_id: {}'.format(user['user_id']))
        if user and user['user_id'] in wx_admin_ids:
            cond['status'] = {'$gte': 1}
        else:
            cond['status'] = {'$gte': 1}
        if vote_open:
            if not vote_open.isdigit():
                return self.write_error(422)
            cond['vote_open'] = int(vote_open)
        if has_vote:
            cond['vote_title'] = {'$ne': ''}
        shares = Share.find(cond, {'_id': 0}).sort('_id', -1)
        shares = [fix_share(share) for share in shares]
        self.res = list(shares)
        return self.write_json()


def fix_share(share):  # time
    if share['post_img']:
        share['post_img'] = 'https://anwensf.com/static/upload/img/' + \
            share['post_img'].replace('_1200.jpg', '_260.jpg')
    share['published'] = int(share['published'] * 1000)
    share['updated'] = int(share['updated'] * 1000)
    return share


class PreviewHandler(JsonHandler):

    def get(self):
        url = self.get_argument("url", None)
        # https://www.ifanr.com/1080409
        doc = Webcache.find_one({'url': url}, {'_id': 0})
        if doc:
            self.res = dict(doc)
            return self.write_json()
        try:
            sessions = requests.session()
            sessions.headers[
                'User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36'
            response = sessions.get(url)
            response.encoding = 'utf-8'  # TODO
            doc = Document(response.text)
            title = doc.title()
            summary = doc.summary()
            markdown = html2text.html2text(summary)
            markdown = markdown.replace('-\n', '-')
            markdown = markdown.strip()
            res = {}
            res['url'] = url
            res['title'] = title
            res['markdown'] = markdown
            if title and markdown:
                webcache = Webcache
                webcache.new(res)
                self.res = res
            self.write_json()

        except Exception as e:
            print(e)


def todo_get_suggest(share, current_user):
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
            post.score += 1  # todo
        if current_user:
            is_hitted = Hit.find(
                {'share_id': share.id},
                {'user_id': int(current_user["user_id"])},
            ).count() > 0
        # else:
            # is_hitted = self.get_cookie(share.id)
        if is_hitted:
            post.score -= 50
        suggest.append(post)
    suggest.sort(key=lambda obj: obj.get('score'))
    suggest = suggest[:5]


def todo_get_tags(share):
    tags = ''
    if share.tags:
        tags += 'tags:'
        for i in share.tags.split(' '):
            tags += '<a href="/tag/%s">%s</a>  ' % (i, i)
    return tags
