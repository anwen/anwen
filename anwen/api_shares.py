# -*- coding:utf-8 -*-
# 文章列表
from .api_base import JsonHandler
from db import Share, User, Hit
# from bs4 import BeautifulSoup
# from tornado.escape import json_decode
from utils import get_tags, get_tags_parents
import time
from utils.avatar import get_avatar, get_avatar_by_wechat, get_avatar_by_feed
import options
import copy
from log import logger
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


# https://www.yuque.com/easytoknow/afi6hu/md7sld


# get_tags_parent
# logger.info('token: {}'.format(token))

# 文章列表API v2
# 差异
# 没有summary
# 其他
# 不同权限的用户看到的列表不同
# 来源 来源图片


class SharesV2Handler(JsonHandler):
    def get(self):
        token = self.request.headers.get('Authorization', '')
        page = self.get_argument("page", 1)
        per_page = self.get_argument("per_page", 10)
        tag = self.get_argument('tag', '')
        filter_type = self.get_argument("filter_type", '')  # my_tags
        meta_info = self.get_argument("meta_info", 1)
        last_suggested = self.get_argument("last_suggested", 0)
        read_status = self.get_argument('read_status', 1)

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
        number = Share.find(cond, {'_id': 0, 'id': 1}).count()

        # number=number
        return self.write_json()
