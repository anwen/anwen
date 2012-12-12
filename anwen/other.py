# -*- coding:utf-8 -*-

from base import BaseHandler


class EditHandler(BaseHandler):
    def get(self):
        self.render("edit.html")
