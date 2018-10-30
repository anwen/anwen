# -*- coding:utf-8 -*-
import tornado.escape
import tornado.web
import base64
import utils
import requests
from .api_base import JsonHandler
from db import User
from db import admin
from utils.avatar import get_avatar, get_avatar_by_wechat
from options import appinfo


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


# https://api.weixin.qq.com/sns/jscode2session?appid=APPID&secret=SECRET&js_code=JSCODE&grant_type=authorization_code

class WxLoginHandler(JsonHandler):

    def get(self):
        wx_code = self.get_argument("code", '')
        appname = self.get_argument("appname", '')
        if not wx_code or not appname:
            return self.write_error(401)
        wx_api = 'https://api.weixin.qq.com/sns/jscode2session'
        params = {}
        params['appid'] = appinfo[appname]['WX_APPID']
        params['secret'] = appinfo[appname]['WX_SECRET']
        params['js_code'] = wx_code
        params['grant_type'] = 'authorization_code'
        r = requests.get(wx_api, params=params)
        r = r.json()
        session_key = r.get('session_key')
        openid = r.get('openid')
        # 复用email password
        doc = User.by_email(openid + '@wechat')
        if doc:
            doc.update(
                {
                    'user_pass': session_key,
                }
            )
            doc.save()
            user_info = {
                'user_id': doc.id,
                'user_email': doc.user_email,
                'user_name': doc.user_name,
                'user_domain': doc.user_domain,
            }
            token = self.create_signed_value(
                'user', tornado.escape.json_encode(user_info))
            self.res['token'] = token.decode('u8')

            self.res['is_admin'] = doc['is_admin']
            if doc['id'] in (60, 63, 64):
                self.res['is_admin'] = True

            return self.write_json()
        else:
            res = {}
            # res['id'] = User.find().count() + 1
            res['user_email'] = openid + '@wechat'
            res['user_pass'] = session_key
            # res['user_name'] = ''
            # res['user_domain'] = ''
            user = User.new(res)
            user_info = {
                'user_id': user.id,
                'user_email': user.user_email,
                'user_name': user.user_name,
                'user_domain': user.user_domain,
            }
            token = self.create_signed_value(
                'user', tornado.escape.json_encode(user_info))
            self.res['token'] = token.decode('u8')

            return self.write_json()

        # not mini
        # https://wohugb.gitbooks.io/wechat/content/qrconnent/user_info.html

        # https://developers.weixin.qq.com/miniprogram/dev/api/api-login.html#wxloginobject
        # step1 get session_key openid
        # https://api.weixin.qq.com/sns/jscode2session?appid=APPID&secret=SECRET&js_code=JSCODE&grant_type=authorization_code
        # step2 get access_token
        # https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=APPID&secret=APPSECRET


class MeHandler(JsonHandler):

    @tornado.web.authenticated
    def get(self):
        user = User.by_sid(self.current_user['user_id'])
        if user.user_email.endswith('@wechat'):
            pass
            user.gravatar = get_avatar_by_wechat(user._id)
        else:
            # user.gravatar = get_avatar(user.user_email.encode('u8'), 100)
            user.gravatar = get_avatar(user.user_email, 100)
        user = dict(user)
        user.pop('_id')
        user.pop('user_pass')
        user['is_admin'] = admin.is_admin(user['id'])
        if user['id'] in (60, 63, 64):
            user['is_admin'] = True
        self.res = user
        return self.write_json()

    @tornado.web.authenticated
    def post(self):
        user = User.by_sid(self.current_user['user_id'])
        # do not save user info if not necessary
        # avatarUrl   String  用户头像，最后一个数值代表正方形头像大小（有0、46、64、96、132数值可选，0代表640 * 640正方形头像），用户没有头像时该项为空。若用户更换头像，原有头像URL将失效。
        # gender  String  用户的性别，值为1时是男性，值为2时是女性，值为0时是未知
        # province    String  用户所在省份
        # country String  用户所在国家
        # language    String  用户的语言，简体中文为zh_CN
        # iv
        # signature
        # encryptedData
        name = self.get_argument('name', None)
        if not name:
            name = self.get_argument('nickName', None)
        if name:
            user['user_name'] = name
        avatarUrl = self.get_argument('avatarUrl', None)
        if avatarUrl:
            try:
                r = requests.get(avatarUrl)
                if r.status_code == 200:
                    avatar_dir = 'static/avatar'
                    size = 'raw'
                    avatar_path = '%s/%s_%s.jpg' % (avatar_dir, user.id, size)
                    with open(avatar_path, 'wb') as f:
                        for chunk in r.iter_content():
                            f.write(chunk)
                    print('saved avatar')
            except Exception as e:
                print('Error:', e)
        city = self.get_argument('city', None)
        if city:
            user['user_city'] = city
        user['user_say'] = self.get_argument('say', None)
        user.save()
        user['is_admin'] = admin.is_admin(user['id'])
        user.pop('_id')

        auser = {}
        auser['is_admin'] = user['is_admin']
        if user['id'] in (60, 63, 64):
            auser['is_admin'] = True
        self.res = auser
        return self.write_json()

# avatarUrl
# city
# country
# encryptedData
# gender
# isignaturev
# iv
# language
# nickName
# province
