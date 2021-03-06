# -*- coding:utf-8 -*-
# 文章列表
from .api_base import JsonHandler
from db import Share, User, Hit
from bs4 import BeautifulSoup
from tornado.escape import json_decode
from utils import get_tags, get_tags_parents
import time
from utils.avatar import get_avatar, get_avatar_by_wechat, get_avatar_by_feed
import options
import copy
from log import logger

# from bs4 import BeautifulSoup
# from tornado.escape import json_decode
# import time
# from log import logger
# https://www.yuque.com/easytoknow/afi6hu/md7sld
# get_tags_parent
# logger.info('token: {}'.format(token))
# 文章列表API v2
# 没有summary
# 不同权限的用户看到的列表不同


wx_admin_ids = (60, 63, 64)
IMG_BASE = 'https://anwensf.com/static/upload/img/'


def fix_share(share):  # time
    if share['post_img']:
        share['post_img'] = 'https://anwensf.com/static/upload/img/' + \
            share['post_img'].replace('_1200.jpg', '_260.jpg')
    share['published'] = int(share['published'] * 1000)
    share['updated'] = int(share['updated'] * 1000)
    share['suggested'] = int(share['suggested'] * 1000)
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
        page = self.get_argument("page", 1)
        per_page = self.get_argument("per_page", 10)
        filter_type = self.get_argument("filter_type", '')  # my_tags
        tag = self.get_argument('tag', '')
        meta_info = self.get_argument("meta_info", 1)
        last_suggested = self.get_argument("last_suggested", 0)
        read_status = self.get_argument('read_status', 1)
        token = self.request.headers.get('Authorization', '')
        # has_vote = self.get_argument("has_vote", None)
        # vote_open = self.get_argument("vote_open", None)

        read_status = int(read_status)
        per_page = int(per_page)
        page = int(page)
        last_suggested = float(last_suggested) / 1000 + 1
        user = self.get_user_dict(token)

        cond = {}
        # 按照tags来过滤
        tags = None
        if user and filter_type == 'my_tags':
            d_user = User.by_sid(user['user_id'])
            if d_user:
                tags = d_user['user_tags']
        # 按照tag来过滤
        if tags:
            cond['tags'] = {"$in": tags}
        elif tag:
            cond['tags'] = tag

        # 不同的用户显示不同级别的推荐
        if user and user['user_id'] in wx_admin_ids:
            cond['status'] = {'$gte': 1}
        else:
            cond['status'] = {'$gte': 1}

        l_hitted_share_id = []
        if user and read_status:
            hits = Hit.find({'user_id': user['user_id']})
            l_hitted_share_id = [i['share_id'] for i in hits]

        # if vote_open:
        #     if not vote_open.isdigit():
        #         return self.write_error(422)
        #     cond['vote_open'] = int(vote_open)
        # if has_vote:
        #     cond['vote_title'] = {'$ne': ''}

        number = Share.find(cond, {'_id': 0}).count()
        # sort: _id
        if last_suggested:
            cond_update = copy.deepcopy(cond)
            cond_update['suggested'] = {'$gt': last_suggested}
            number_of_update = Share.find(cond_update, {'_id': 0}).sort(
                'suggested', -1).count()
            logger.info('number_of_update 1: {}'.format(number_of_update))

        num_shares = Share.find(cond, {'_id': 0, 'id': 1}).count()

        shares = Share.find(cond, {'_id': 0}).sort(
            'suggested', -1).limit(per_page).skip((page - 1) * per_page)
        # shares = [fix_share(share) for share in shares]
        new_shares = []
        for share in shares:
            share = fix_share(share)
            user = User.by_sid(share.user_id)
            share = dict(share)
            share['user_name'] = user.user_name
            share['markdown'] = ''
            if read_status:
                share['read'] = bool(share['id'] in l_hitted_share_id)

            soup = BeautifulSoup(share['content'], "lxml")
            # kill all script and style elements
            for script in soup(["script", "style"]):
                script.extract()    # rip it out

            # get text
            text = soup.get_text()

            # break into lines and remove leading and trailing space on each
            lines = (line.strip() for line in text.splitlines())
            # break multi-headlines into a line each
            chunks = (phrase.strip()
                      for line in lines for phrase in line.split("  "))
            # drop blank lines
            text = '\n'.join(chunk for chunk in chunks if chunk)
            # print(text)
            share['summary'] = text[:150]
            share['content'] = ''

            if user.user_email.endswith('@wechat'):
                share['user_img'] = options.site_url + \
                    get_avatar_by_wechat(user._id)
            if user.user_email.endswith('@anwensf.com'):
                share['user_img'] = options.site_url + \
                    get_avatar_by_feed(user.id)
            else:
                share['user_img'] = options.site_url + \
                    get_avatar(user.user_email, 100)
            new_shares.append(share)

        # if tag:
        #     shares = [share for share in shares if tag in share['tags']]
        meta = {}
        meta['page'] = page
        meta['articleNumber'] = num_shares
        if meta_info and last_suggested:
            meta['number_of_update'] = number_of_update
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

        logger.info('last_suggested time: {}'.format(last_suggested))

        if new_shares:
            logger.info('new_shares[0] time: {}'.format(new_shares[0]['title']))
            logger.info('new_shares[0] published time: {}'.format(
                new_shares[0]['published']))
            logger.info('new_shares[0] suggested time: {}'.format(
                new_shares[0]['suggested']))

        self.res = {'articles': list(new_shares)}
        self.meta = meta
        # number=len(self.res)
        # number=number
        return self.write_json()
