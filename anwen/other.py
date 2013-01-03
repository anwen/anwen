# -*- coding:utf-8 -*-

from base import BaseHandler


class EditHandler(BaseHandler):
    def get(self):
        self.render("edit.html")


class ErrHandler(BaseHandler):
    def get(self):
        self.render("404.html")
