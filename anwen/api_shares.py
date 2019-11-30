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

        # number=number
        return self.write_json()
