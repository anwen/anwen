# -*- coding:utf-8 -*-

from anwen.base import BaseHandler
from db import connection as con
from andesay import AndeSay
import say


class AndeHandler(BaseHandler):

    def get(self):
        _ = self.locale.translate
        msg = _(say.firstmeet())
        msg = msg + say.expression()
        self.render("ande.html", say=msg)

    def post(self):
        usersay = self.get_argument("ask0", '')
        # print usersay
        # user_lang = self.get_user_lang()
        userip = self.request.remote_ip
        a = AndeSay()
        andesay = a.get_andesay(usersay, userip)
        andesay += '<br/>your ip:' + userip
        andesay += '<br/>'

        user_id = ''
        if self.current_user:
            user_id = self.current_user["user_id"]
        if not user_id:
            user_id = userip.replace('.', '')
        Ande.create(
            user_id='1',
            usersay=usersay,
            andesay=andesay, )
        # print andesay
        self.write(andesay)
