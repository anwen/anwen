# -*- coding:utf-8 -*-
from .api_base import JsonHandler
from db import Share, User, Like, Comment, Viewpoint, Hit, Webcache
import markdown2
from random import randint
import random
from utils.avatar import get_avatar
import requests
from readability import Document
import html2text


class ShareHandler(JsonHandler):  # 单篇文章

    def get(self, slug):
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
        if not share:
            return self.write_error(404)
        share.hitnum += 1
        share.save()
        share.pop('_id')
        share.published = int(share.published * 1000)
        share.updated = int(share.updated * 1000)
        # share.content = markdown2.markdown(share.markdown)
        user = User.by_sid(share.user_id)
        share.user_name = user.user_name
        share.user_domain = user.user_domain

        user_id = int(
            self.current_user["user_id"]) if self.current_user else None
        like = Like.find_one(
            {'share_id': share.id, 'user_id': user_id})
        share.is_liking = bool(like.likenum % 2) if like else None
        share.is_disliking = bool(like.dislikenum % 2) if like else None

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
        viewpoints = Viewpoint.find({'share_id': share.id}, {'_id': 0})
        # if share.link:
        #     # share.url = '<a href="{}">{} {}</a>'.format(
        #     #     share.link, share.title, share.link)
        #     share.url = '<a href="{}">{}</a>'.format(
        #         share.link, share.title)
        d_share = dict(share)
        if d_share.get('link'):
            doc = Webcache.find_one({'url': d_share['link']}, {'_id': 0})
            if doc and doc['markdown']:
                d_share['markdown'] += '\n\n--预览--\n\n' + doc['markdown']

        # thumbnails
        d_share['post_img'] = 'https://anwensf.com/static/upload/img/' + d_share['post_img'].replace('_1200.jpg', '_260.jpg')

        print(d_share.get('link'))
        if d_share.get('link'):
            # share.url = '<a href="{}">{} {}</a>'.format(
            #     share.link, share.title, share.link)
            d_share['url'] = '预览： <a href="{}">{}</a>'.format(
                share.link, share.title)
        d_share['viewpoints'] = list(viewpoints)
        # comment suggest
        self.res = d_share
        self.write_json()


class SharesHandler(JsonHandler):

    def get(self):
        cond = {}
        cond['status'] = {'$gte': 1}
        vote_open = self.get_argument("vote_open", None)
        has_vote = self.get_argument("has_vote", None)
        if vote_open:
            if not vote_open.isdigit():
                return self.write_error(422)
            cond['vote_open'] = int(vote_open)
        if has_vote:
            cond['vote_title'] = {'$ne': ''}
        shares = Share.find(cond, {'_id': 0}).sort('_id', -1)
        shares = [fix_time(share) for share in shares]
        self.res = list(shares)
        return self.write_json()


def fix_time(share):
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
            # response.encoding = 'utf-8'
            doc = Document(response.text)
            title = doc.title()
            summary = doc.summary()
            markdown = html2text.html2text(summary)
            markdown = markdown.replace('-\n', '-')
            res = {}
            res['url'] = url
            res['title'] = title
            res['markdown'] = markdown
            webcache = Webcache
            webcache.new(res)
            self.res = res
            self.write_json()

        except Exception as e:
            print(e)


def get_suggest():
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


def get_tags(share):
    tags = ''
    if share.tags:
        tags += 'tags:'
        for i in share.tags.split(' '):
            tags += '<a href="/tag/%s">%s</a>  ' % (i, i)
    return tags
