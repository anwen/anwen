# -*- coding:utf-8 -*-
# 全部列表
# 个性化列表
from .api_base import JsonHandler
from db import Share, User
from bs4 import BeautifulSoup
from tornado.escape import json_decode
from log import logger
from utils import get_tags, get_tags_parents
import time
from utils.avatar import get_avatar, get_avatar_by_wechat
import options
wx_admin_ids = (60, 63, 64)
# get_tags_parent
# logger.info('token: {}'.format(token))


def fix_share(share):  # time
    if share['post_img']:
        share['post_img'] = 'https://anwensf.com/static/upload/img/' + \
            share['post_img'].replace('_1200.jpg', '_260.jpg')
    share['published'] = int(share['published'] * 1000)
    share['updated'] = int(share['updated'] * 1000)
    return share


class SharesHandler(JsonHandler):

    def get_user_dict(self, token):
        user = None
        if token:
            key, token = token.split()
            if key == 'token' and token:
                user_json = self.get_secure_cookie('user', token)
                if user_json:
                    user = json_decode(user_json)
        else:
            user_json = self.get_secure_cookie("user")
            if user_json:
                user = json_decode(user_json)
        return user

    # 文章列表API
    # 不同权限的用户看到的列表不同
    # 来源 来源图片
    # 内容前150个字

    def get(self):
        # get params
        filter_type = self.get_argument("my_tags", '')

        page = self.get_argument("page", 1)
        per_page = self.get_argument("per_page", 10)

        meta_info = self.get_argument("meta_info", 1)
        tag = self.get_argument('tag', '')
        user_info = self.get_argument('user_info', 1)
        vote_open = self.get_argument("vote_open", None)
        has_vote = self.get_argument("has_vote", None)
        token = self.request.headers.get('Authorization', '')

        user_info = int(user_info)
        per_page = int(per_page)
        page = int(page)

        user = self.get_user_dict(token)

        tags = None
        if user and filter_type == 'my_tags':
            d_user = User.by_sid(user['user_id'])
            if d_user:
                tags = d_user['user_tags']

        # 按照tag来过滤
        cond = {}
        logger.info('tags: {}'.format(tags))
        if tags:
            cond['tags'] = {"$in": tags}
        elif tag:
            cond['tags'] = tag

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

        number = Share.find(cond, {'_id': 0}).count()
        shares = Share.find(cond, {'_id': 0}).sort(
            '_id', -1).limit(per_page).skip((page - 1) * per_page)
        # shares = [fix_share(share) for share in shares]
        new_shares = []
        for share in shares:
            share = fix_share(share)
            user = User.by_sid(share.user_id)
            share = dict(share)
            share['user_name'] = user.user_name
            share['markdown'] = ''

            soup = BeautifulSoup(share['content'], "lxml")
            # kill all script and style elements
            for script in soup(["script", "style"]):
                script.extract()    # rip it out

            # get text
            text = soup.get_text()

            # break into lines and remove leading and trailing space on each
            lines = (line.strip() for line in text.splitlines())
            # break multi-headlines into a line each
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            # drop blank lines
            text = '\n'.join(chunk for chunk in chunks if chunk)
            # print(text)
            share['summary'] = text[:150]
            share['content'] = ''

            if user.user_email.endswith('@wechat'):
                share['user_img'] = options.site_url+get_avatar_by_wechat(user._id)
            else:
                share['user_img'] = options.site_url+get_avatar(user.user_email, 100)
            new_shares.append(share)

        # if tag:
        #     shares = [share for share in shares if tag in share['tags']]
        meta = {}
        if meta_info and tag:
            d_tags = get_tags()
            # d_tags_parent = get_tags_parent()
            d_tags_parents = get_tags_parents()

            if tag in d_tags:
                sub_tags = []
                for name in d_tags[tag]:
                    num = Share.find({'tags': name}, {'_id': 0}).count()
                    num_recent = Share.find(
                        {'tags': name, 'published': {'$gt': time.time() - 86400 * 30}}, {'_id': 0}).count()
                    info = {}
                    info['name'] = name
                    info['num'] = num
                    info['num_recent'] = num_recent
                    sub_tags.append(info)
                meta['sub_tags'] = sub_tags
            meta['parent_tags'] = []
            if tag in d_tags_parents:
                # hypernym
                # meta['parent_tags'].append(d_tags_parent[tag])
                meta['parent_tags'] = d_tags_parents[tag]

        self.res = list(new_shares)
        self.meta = meta
        # number=len(self.res)
        return self.write_json(number=number)