# -*- coding:utf-8 -*-
u"""文章分享，非API."""
import time
from random import randint
import markdown2
import tornado.web
import options
from utils.avatar import get_avatar
from db import User, Share, Comment, Hit, Tag, Viewpoint, Webcache
from db import Like, Collect
from .base import BaseHandler
from anwen.api_share import get_share_by_slug, add_hit_stat
import requests
import html2text
from readability import Document
from utils import get_charset
try:
    from urllib.parse import urlparse
except:
    from urlparse import urlparse  # Python 2
from log import logger
# 网页版的接口

from utils.img_tools import make_post_thumb
from PIL import Image
import datetime
import sys
import os
from pymongo import MongoClient
conn = MongoClient()
adb = conn.anwen
adb.authenticate(options.db['username'], options.db['password'])
sys.path.append('.')
from db import Tag, Share  # noqa


def format_tags(share):
    tags = ''
    if share.tags:
        tags += 'tags:'
        for i in share.tags:
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
        share.title = share.title.split('_')[0]
        if share.markdown:
            md = share.markdown
            md = md.replace('>\n', '> ')
            share.content = markdown2.markdown(md)

        # 对于链接分享类，增加原文预览
        if share.link and share.sharetype != 'rss':
            # Webcache should add index
            doc = Webcache.find_one({'url': share.link}, {'_id': 0})
            # 此文章须经作者同意 转载 禁止转载
            # 禁止任何形式的转载
            # ('禁止' not in doc['markdown'] and '转载' not in doc['markdown']):
            if doc and doc['markdown'] and ('禁止转载' not in doc['markdown'] or '禁止任何形式的转载' not in doc['markdown']):
                doc['markdown'] = doc['markdown'].replace('本文授权转自', '')
                md = share['markdown']
                md += '\n\n--预览--\n\n' + doc['markdown']
                md += '\n\n[阅读原文]({})'.format(doc['url'])

                parsed_uri = urlparse(share.link)
                domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
                md = md.replace('![image](/', '![image]({}/'.format(domain))
                md = md.replace('\n* \n', '\n\n')
                md = md.replace('\n*\n', '\n\n')
                md = md.replace('>\n', '> ')
                # md = md.replace('>\n\n', '')  # ???
                while '\n\n\n' in md:
                    md = md.replace('\n\n\n', '\n\n')
                share.content = markdown2.markdown(md)

        user_id = self.current_user["user_id"] if self.current_user else None
        # user_id
        like = Like.find_one(
            {'entity_id': share.id, 'user_id': user_id, 'entity_type': 'share'})
        collect = Collect.find_one(
            {'entity_id': share.id, 'user_id': user_id, 'entity_type': 'share'})
        share.is_liking = bool(like.likenum) if like else False
        share.is_disliking = bool(like.dislikenum) if like else False

        share.is_collecting = bool(collect.collectnum) if collect else False

        # logger.info('user_id: {}'.format(user_id))
        # logger.info('share.is_liking: {}'.format(share.is_liking))

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
        # TODO
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
        img_url = self.get_argument("img_url", '')

        tags = tags.split()

        if link:
            url = link
            doc = Webcache.find_one({'url': url}, {'_id': 0})
            if doc:
                logger.info('already downloaded')
                doc_title = doc.title
                # markdown = doc.markdown
            else:
                sessions = requests.session()
                sessions.headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36'
                try:
                    # response = sessions.get(url)
                    response = sessions.get(url, timeout=4)
                # TODO: try to use a proxy
                except (requests.ConnectionError, requests.Timeout) as e:
                    print(e)
                    self.write("GFW...")
                    return
                # except requests.exceptions.HTTPError as e:
                #     if e.response.status_code == 400:
                #         error = e.response.json()
                #         code = error['code']
                #         message = error['message']

                except Exception as e:
                    logger.info('e: {}'.format(e))
                    # self.redirect("/")
                    self.write("GFW")
                    return
                # response.encoding = 'utf-8'  # TODO
                response.encoding = get_charset(response)
                logger.info('response.encoding {}'.format(response.encoding))
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

        if vote_open.isdigit():
            vote_open = int(vote_open)
        else:
            vote_open = 0
        if not title:
            title = doc_title

        # 处理封面链接

        if img_url and not post_img:
            ext = img_url.split('?')[0].split('.')[-1]
            ext = '.'+ext.lower()
            print(ext)
            assert ext in ['.jpg', '.jpeg', '.gif', '.png', '.bmp']
            img_dir = 'static/upload/img'
            now = datetime.datetime.now()
            t = now.strftime('%Y%m%d_%H%M%S_%f')
            img_name = '%s%s' % (t, ext)
            img_path = '%s/%s' % (img_dir, img_name)
            print(img_path)
            r = requests.get(img_url, verify=False, stream=True)  # stream=True)
            chunk_size = 100
            with open(img_path, 'wb') as image:
                for chunk in r.iter_content(chunk_size):
                    image.write(chunk)

            im = Image.open(img_path)
            width, height = im.size
            if width / height > 5 or height / width > 5:
                os.remove(img_path)  # 判断比例 删除图片
                print('请不要上传长宽比例过大的图片')
            else:
                # 创建1200x550 750x230 365x230缩略图
                make_post_thumb(img_path, sizes=[
                    (1200, 550), (750, 230), (365, 230), (260, 160)
                ])
                print('done')
                post_img = img_path.split('/')[-1]
                post_img = post_img.split('.')[0] + '_1200.jpg'

        res = {
            'title': title,
            'markdown': markdown,
            'content': content,
            'sharetype': sharetype,
            'slug': slug,
            'tags': tags,
            'post_img': post_img,
            'link': link,
            'vote_open': vote_open,
            'vote_title': vote_title,
            'updated': time.time(),
        }
        # if not markdown:
        #     self.redirect("/")
        #     return
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
        for i in tags:
            doc = {
                'name': i,
                'share_ids': share.id
            }
            Tag.new(doc)
        self.redirect("/share/" + str(share.id))
