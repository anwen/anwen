# -*- coding:utf-8 -*-
import tornado.web
from anwen.api_base import JsonHandler
from db import Share, User, Like, Hit
import time
# Comment, Viewpoint
admin_ids = (1, 4, 60, 63, 64, 65, 69, 86)


# 现有的指标：

# 有KPI的
# 推送的数量 现在：725  计划两周后809
# 用户日活 现在0  计划从190519开始：2
# 每天推送文章数 现在0  计划从190519开始：6
# 推送的平均打开数 现在0 计划从190519开始：0.3  !!!
# rss来源数： 27  计划两周后40

# 无KPI的
# 内容数 5693
# 用户数 123
# 文章访问总数（只计算登录用户，每个用户每篇文章只算作一次）： 244
# 标签总数：1845
# 抓取文章数： 348

# 有tag的内容占比
# 有图片的内容占比
# 内容的 (用户)喜欢数 收藏数


class StatHandler(JsonHandler):

    @tornado.web.authenticated
    def get(self):
        user_id = self.current_user["user_id"]
        if user_id not in admin_ids:
            self.write_json()
            return

        share_num = Share.find().count()
        share_state1_num = Share.find({'status': {'$gte': 1}}).count()

        share_with_tag_num = share_num - Share.find({'tags': []}).count()
        share_state1_with_tag_num = share_state1_num - \
            Share.find({'status': {'$gte': 1}, 'tags': []}).count()

        user_num = User.find().count()
        user_rss_num = User.find({'user_rss': {'$ne': ''}}).count()

        like_num = Like.find().count()  # todo
        hit_num = Hit.find().count()  # todo
        hit_num_in_5_day = Hit.find({'hittime': {'$gt': time.time()-86400*5}}).count()
        # 日活
        self.res = {
            'share_num': share_num,
            'share_state1_num': share_state1_num,
            'share_with_tag_num': share_with_tag_num,
            'share_state1_with_tag_num': share_state1_with_tag_num,

            'user_num': user_num,
            'user_rss_num': user_rss_num,

            'like_num': like_num,
            'hit_num': hit_num,
            'hit_num_in_5_day': hit_num_in_5_day,
        }
        self.write_json()
