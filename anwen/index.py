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
        # share_res = Share.find({'status': 0}).sort(
        #     'score', DESCENDING).limit(11).skip((int(page) - 1) * 11)
        share_res = Share.find({'status': {'$gte': 0}}).sort(
            '_id', DESCENDING).limit(11).skip((int(page) - 1) * 11)
        pagesum = (share_res.count() + 10) / 11
        shares = []
        for share in share_res:
            if share.id in (48, 47):
                continue
            user = User.by_sid(share.user_id)
            share.name = user.user_name
            share.published = time.strftime(
                '%Y-%m-%d %H:%M:%S', time.localtime(share.published))
            share.domain = user.user_domain
            share.markdown = cutter(
                markdown2.markdown(share.markdown))
            share.title = share.title.split('_')[0]
            shares.append(share)
        self.render(
            "node.html",
            shares=shares,
            pagesum=pagesum, page=page, node=node,
        )


class NodeHandler(BaseHandler):

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
            pagesum=pagesum, page=page, node=node, node_info=node_info)


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
