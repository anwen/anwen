# -*- coding:utf-8 -*-
import tornado.web
from db import User, Share, Webcache
from .base import BaseHandler
import requests
import html2text
from readability import Document
from utils import get_charset
from log import logger


class ShareByGetHandler(BaseHandler):
    u"""直接通过get分享."""

    @tornado.web.authenticated
    def get(self):
        sharetype = self.get_argument("sharetype", "goodlink")
        link = self.get_argument("link", '')
        user_id = self.current_user["user_id"]
        assert link
        url = link
        doc = Webcache.find_one({'url': url}, {'_id': 0})
        if not doc:
            sessions = requests.session()
            sessions.headers[
                'User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36'
            response = sessions.get(url)
            # response.encoding = 'utf-8'  # TODO
            response.encoding = get_charset(response)
            logger.info('response.encoding {}'.format(response.encoding))
            doc = Document(response.text)
            doc_title = doc.title()
            summary = doc.summary()
            _markdown = html2text.html2text(summary)
            _markdown = _markdown.replace('-\n', '-').strip()
            res_webcache = {}
            res_webcache['url'] = url
            res_webcache['title'] = doc_title
            res_webcache['markdown'] = _markdown
            if _markdown:
                webcache = Webcache
                webcache.new(res_webcache)
        else:
            logger.info('already')
            doc_title = doc.title
        res = {
            'title': doc_title,
            'sharetype': sharetype,
            'link': link,
        }
        share = Share
        res['user_id'] = user_id
        share = share.new(res)
        user = User.by_sid(user_id)
        user.user_leaf += 10
        user.save()
        self.redirect("/share/" + str(share.id))
