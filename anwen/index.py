# -*- coding:utf-8 -*-
import time
import markdown2
from pymongo import DESCENDING  # ASCENDING
from utils.fliter import cutter, filter_tags
from .base import BaseHandler
from db import User, Share, Tag
import gc

# ExploreHandler


class NodeHandler(BaseHandler):

    def get(self, node='home'):
        page = self.get_argument("page", 1)
        per_page = self.get_argument("per_page", 11)
        per_page = int(per_page)

        # 控制显示级别
        status = self.get_argument("status", 'gte_1')
        assert '_' in status
        st_type, st_num = status.split('_')
        status = {'${}'.format(st_type): int(st_num)}  # {'$gte': 1}

        # 当node不是home时，不控制显示级别
        conds = {'status': status}
        if node not in 'home'.split():
            conds['sharetype'] = node
            # if node not in 'rss'.split():
            conds['status'] = {'$gte': 0}

        # sort type
        # 'score', DESCENDING
        share_res = Share.find(conds).sort(
            '_id', DESCENDING).limit(per_page).skip((int(page) - 1) * per_page)
        pagesum = int((share_res.count() + per_page-1) / per_page)
        if 0:
            shares = []

            # 另外一种显示UI
            if per_page >= 20:
                for share in share_res:
                    if share.id in (48, 47):  # 临时屏蔽
                        continue
                    user = User.by_sid(share.user_id)
                    share.name = user.user_name
                    share.published = time.strftime(
                        '%Y-%m-%d %H:%M:%S', time.localtime(share.published))
                    share.domain = user.user_domain
                    md = share.markdown
                    md = md.replace('>\n', '> ')
                    share.markdown = cutter(markdown2.markdown(md))
                    share.title = share.title.split('_')[0]
                    shares.append(share)
                    del user
                tpl_name = 'node_alot'
            else:
                for share in share_res:
                    if share.id in (48, 47):  # 临时屏蔽
                        continue
                    # 获取用户信息，需要多次查表!!!
                    user = User.by_sid(share.user_id)
                    share.name = user.user_name
                    share.domain = user.user_domain

                    share.published = time.strftime(
                        '%Y-%m-%d %H:%M:%S', time.localtime(share.published))
                    md = share.markdown
                    md = md.replace('>\n', '> ')
                    share.markdown = cutter(markdown2.markdown(md))
                    share.title = share.title.split('_')[0]
                    shares.append(share)
                    del user
                tpl_name = 'node'
        tpl_name = 'node'
        shares = []
        pagesum = 1
        page = 1
        per_page = 1
        self.render(
            "{}.html".format(tpl_name),
            shares=shares,
            pagesum=pagesum, page=page,
            per_page=per_page,
            node=node,
        )
        del shares, share_res
        # del shares
        # ns = super(BaseHandler, self).get_template_namespace()
        # del ns
        return
        # https://stackoverflow.com/questions/15731024/what-state-does-self-finish-put-the-tornado-web-server-in
        # self.finish()

    def on_connection_close(self):
        print('NodeHandler close')
        gc.collect()


class TagHandler(BaseHandler):

    def get(self, name=None):
        if not name:
            tags = Tag.find()
            self.render("tag.html", tags=tags)
        else:
            tag = Tag.find_one({'name': name})
            shares = []
            for i in tag.share_ids.split(' '):
                share = Share.by_sid(i)
                user = User.by_sid(share.user_id)
                share.name = user.user_name
                share.published = time.strftime(
                    '%Y-%m-%d %H:%M:%S', time.localtime(share.published))
                share.domain = user.user_domain
                share.markdown = filter_tags(
                    markdown2.markdown(share.markdown))[:100]
                shares.append(share)
            self.render("tage.html", name=name, shares=shares)
