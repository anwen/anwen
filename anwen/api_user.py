# -*- coding:utf-8 -*-
import tornado.escape
import tornado.web
import base64
import utils
from .api_base import JsonHandler
from db import User
from utils.avatar import get_avatar


class AuthorizationsHandler(JsonHandler):

    def get(self):
        # for k in dir(self.request):
            # if not callable(getattr(self, k)):
                    # print(k, getattr(self.request, k))
        email = self.get_argument('email', '')
        password = self.get_argument('password', '')
        # Authorization: Basic base64("user:passwd")
        auth_header = self.request.headers.get('Authorization', None)
        if auth_header is not None:
            auth_mode, auth_base64 = auth_header.split(' ', 1)
            assert auth_mode == 'Basic'
            email, password = base64.b64decode(auth_base64).decode('u8').split(':', 1)
        if not (email and password):
            # self.set_header('WWW-Authenticate', 'Basic realm="%s"' % 'anwen')
            return self.write_error(402)
        password = utils.make_password(password)
        doc = User.by_email_pass(email, password)
        if doc:
            user_info = {
                'user_id': doc.id,
                'user_email': doc.user_email,
                'user_name': doc.user_name,
                'user_domain': doc.user_domain,
            }
            token = self.create_signed_value(
                'user', tornado.escape.json_encode(user_info))
            self.res['token'] = token.decode('u8')
            return self.write_json()
        return self.write_error(401)


class MeHandler(JsonHandler):

    @tornado.web.authenticated
    def get(self):
        user = User.by_sid(self.current_user['user_id'])
        user.gravatar = get_avatar(user.user_email.encode('u8'), 100)
        user = dict(user)
        user.pop('_id')
        user.pop('user_pass')
        self.res = user
        return self.write_json()

    @tornado.web.authenticated
    def post(self):
        user = User.by_sid(self.current_user['user_id'])
        user['user_name'] = self.get_argument('name', None)
        user['user_city'] = self.get_argument('city', None)
        user['user_say'] = self.get_argument('say', None)
        user.save()
        self.res = {'ok': 1}
        return self.write_json()
