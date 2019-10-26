# -*- coding:utf-8 -*-
from .base import BaseHandler


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
