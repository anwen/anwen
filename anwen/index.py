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
        status = self.get_argument("status", 'gte_1')

        per_page = int(per_page)
        # 控制显示级别
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

        shares = []
        if per_page >= 20:  # 另外一种显示UI
            for share in share_res:
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
                # if share.id in (48, 47):  # 临时屏蔽
                #     continue
                user = User.by_sid(share.user_id)  # 获取用户信息，需要多次查表!!!
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
                del share
                del md
            tpl_name = 'node'

        self.render(
            "{}.html".format(tpl_name),
            shares=shares,
            pagesum=pagesum, page=page,
            per_page=per_page,
            node=node,
        )
        del shares, share_res
        del tpl_name, pagesum, page, per_page, node, status
        return
        # https://stackoverflow.com/questions/15731024/what-state-does-self-finish-put-the-tornado-web-server-in
        # ns = super(BaseHandler, self).get_template_namespace()
        # del ns
        # self.finish()

    # def on_connection_close(self):
    #     print('NodeHandler close')
    #     gc.collect()

    # def on_finish(self):
    #     print('NodeHandler on_finish')
    #     gc.collect()


class TagHandler(BaseHandler):

    def get(self, name=None):
        if not name:
            tags = Tag.find()
            self.render("tag.html", tags=tags)
        else:
            tag = Tag.find_one({'name': name})
            shares = []
            share_ids = tag.share_ids.split(' ')
            share_ids = list(set(share_ids))
            cond = {}
            cond['_id'] = 0
            cond['user_id'] = 1
            cond['published'] = 1
            for share_id in share_ids:
                # share = Share.by_sid(share_id)
                share = Share.find_one({'id': share_id}, cond)
                print(share)
                # <!-- <p class="info">{{ escape(share.markdown) }} ...</p> -->
                user = User.by_sid(share.user_id)
                share.user_name = user.user_name
                share.user_domain = user.user_domain
                share.published = time.strftime(
                    '%Y-%m-%d %H:%M:%S', time.localtime(share.published))
                share.markdown = filter_tags(
                    markdown2.markdown(share.markdown))[:100]
                shares.append(share)
            self.render("tage.html", tag=tag, name=name, shares=shares)
