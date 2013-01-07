# -*- coding:utf-8 -*-

from anwen.base import BaseHandler
from andesay import AndeSay
import say
from db import Ande
from markdown2 import markdown


class AndeHandler(BaseHandler):

    def get(self):
        _ = self.locale.translate
        msg = _(say.firstmeet())
        msg = msg + say.expression()
        sayit = markdown(msg)
        self.render("ande.html", sayit=sayit)

    def post(self):
        usersay = self.get_argument("ask0", '')
        # print usersay
        user_lang = self.get_user_lang()
        userip = self.request.remote_ip
        a = AndeSay()
        andesay, andethink = a.get_andesay(usersay, userip)

        user_id = ''
        if self.current_user:
            user_id = self.current_user["user_id"]
        if not user_id:
            user_id = int(userip.replace('.', ''))

        doc = {
            'user_id': user_id,
            'usersay': usersay,
            'andesay': andesay,
        }
        Ande.new(doc)
        andethink += '<br/>userip:' + userip
        andethink += '<br/>user_lang:' + user_lang
        andethink += '<br/>'
        debug = True  # True False
        # print andesay
        if debug:
            andesay += andethink
        # print andethink
        self.write(andesay)
