# -*- coding:utf-8 -*-
import time
import markdown2
from pymongo import DESCENDING  # ASCENDING
from utils.fliter import cutter, filter_tags
from .base import BaseHandler
import options
from db import User, Share, Tag


class WelcomeHandler(BaseHandler):

    def get(self):
        if self.current_user:
            self.redirect('/')
            return
        self.render("pages/welcome.html")


class IndexHandler(BaseHandler):

    def get(self):
        if not self.current_user:
            self.redirect('/welcome')
            return
        self.redirect('/explore')


class ExploreHandler(BaseHandler):

    def get(self, node='home'):
        page = self.get_argument("page", 1)
        status = self.get_argument("status", 'gte_1')
        per_page = self.get_argument("per_page", 11)
        per_page = int(per_page)
        assert '_' in status
        # status = 0
        # status = {'$gte': 1}
        st_type, st_num = status.split('_')
        status = {'${}'.format(st_type): int(st_num)}

        conds = {'status': status}
        if node != 'home':
            conds['sharetype'] = node

        # sort type
        # 'score', DESCENDING
        share_res = Share.find(conds).sort(
            '_id', DESCENDING).limit(per_page).skip((int(page) - 1) * per_page)
        pagesum = int((share_res.count() + per_page-1) / per_page)
        shares = []
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
            tpl_name = 'node_alot'
        else:
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
            tpl_name = 'node'
        self.render(
            "{}.html".format(tpl_name),
            shares=shares,
            pagesum=pagesum, page=page,
            per_page=per_page,
            node=node,
        )


class NodeHandlerDelete(BaseHandler):

    def get(self, node):
        page = self.get_argument("page", 1)
        share_res = Share.find({'sharetype': node}).sort(
            '_id', DESCENDING).limit(11).skip((int(page) - 1) * 11)
        pagesum = (share_res.count() + 10) / 11

        shares = []
        for share in share_res:
            user = User.by_sid(share.user_id)
            share.name = user.user_name
            share.published = time.strftime(
                '%Y-%m-%d %H:%M:%S', time.localtime(share.published))
            share.domain = user.user_domain
            share.markdown = cutter(
                markdown2.markdown(share.markdown))
            share.title = share.title.split('_')[0]
            shares.append(share)

        node_info = options.node_about[node]
        self.render(
            "node.html", shares=shares,
            pagesum=pagesum, page=page,
            node=node, node_info=node_info)


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
