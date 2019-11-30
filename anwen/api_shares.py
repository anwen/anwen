# -*- coding:utf-8 -*-
# 文章列表
from .api_base import JsonHandler
from db import Share, User, Hit
from utils import get_tags, get_tags_parents
from utils.avatar import get_avatar, get_avatar_by_wechat, get_avatar_by_feed
import options
import copy
# from bs4 import BeautifulSoup
# from tornado.escape import json_decode
# import time
# from log import logger
wx_admin_ids = (60, 63, 64)
IMG_BASE = 'https://anwensf.com/static/upload/img/'

# https://www.yuque.com/easytoknow/afi6hu/md7sld
# get_tags_parent
# logger.info('token: {}'.format(token))
# 文章列表API v2
# 没有summary
# 不同权限的用户看到的列表不同


class SharesV2Handler(JsonHandler):
    def get(self):
        token = self.request.headers.get('Authorization', '')
        page = self.get_argument("page", 1)
        per_page = self.get_argument("per_page", 10)
        tag = self.get_argument('tag', '')
        filter_type = self.get_argument("filter_type", '')  # my_tags
        last_suggested = self.get_argument("last_suggested", 0)
        read_status = self.get_argument('read_status', 1)
        meta_info = self.get_argument("meta_info", 1)

        read_status = int(read_status)
        per_page = int(per_page)
        page = int(page)
        if not last_suggested:
            last_suggested = 0
        last_suggested = float(last_suggested) / 1000 + 1

        user = self.get_user_dict(token)

        cond = {}
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
        # if user and user['user_id'] in wx_admin_ids:
        if user and user['user_id'] == 1:
            cond['status'] = {'$gte': 1}
        else:
            cond['status'] = {'$gte': 1}

        # 已读列表 20ms
        l_hitted_share_id = []
        if user and read_status:
            hits = Hit.find({'user_id': user['user_id']}, {'_id': 0, 'share_id': 1})
            l_hitted_share_id = [i['share_id'] for i in hits]
        # number = Share.find(cond, {'_id': 0}).count() # 'id': 1

        filter_d = {}
        filter_d['_id'] = 0
        # 白名单里的属性才展示
        filter_d['id'] = 1
        filter_d['images'] = 1
        filter_d['title'] = 1
        filter_d['user_id'] = 1
        filter_d['tags'] = 1
        filter_d['published'] = 1
        filter_d['post_img'] = 1
        shares = Share.find(cond, filter_d).sort(
            'suggested', -1).limit(per_page).skip((page - 1) * per_page)
        # 过滤
        new_shares = []
        for share in shares:
            user = User.by_sid(share.user_id)
            # share = dict(share)
            share['type'] = 1
            # if share.post_img:
            # if hasattr(share, 'post_img'):
            if share.get('post_img'):
                share['type'] = 2
                share['images'] = [IMG_BASE + share['post_img'].replace('_1200.jpg', '_260.jpg')]
                share.pop('post_img')
            else:
                share['images'] = []
            share['author'] = user.user_name
            share['published'] = int(share['published'] * 1000)  # share.published
            if read_status:
                share['read'] = bool(share['id'] in l_hitted_share_id)

            if 0:  # 不展示作者头像
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

        if meta_info:
            meta = {}
            # if filter_type == 'my_tags':
            #     meta['tags'] = tags
            if last_suggested:
                cond_update = copy.deepcopy(cond)
                cond_update['suggested'] = {'$gt': last_suggested}
                number_of_update = Share.find(cond_update, {'_id': 0, 'id': 1}).count()
                meta['number_of_update'] = number_of_update
            if tag:  # 子标签的文章数量
                d_tags = get_tags()
                d_tags_parents = get_tags_parents()  # get_tags_parent
                if tag in d_tags:
                    sub_tags = []
                    for name in d_tags[tag]:
                        info = {}
                        info['name'] = name
                        # num = Share.find({'tags': name}, {'_id': 0}).count()
                        # num_recent = Share.find(
                        #     {'tags': name, 'published': {'$gt': time.time() - 86400 * 30}}, {'_id': 0}).count()
                        # info['num'] = num
                        # info['num_recent'] = num_recent
                        sub_tags.append(info)
                    meta['sub_tags'] = sub_tags
                meta['parent_tags'] = []
                if tag in d_tags_parents:
                    # meta['parent_tags'].append(d_tags_parent[tag])
                    meta['parent_tags'] = d_tags_parents[tag]  # hypernym

        # number=number
        return self.write_json()
