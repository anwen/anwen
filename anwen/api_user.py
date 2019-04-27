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
wx_admin_ids = (60, 63, 64)


class AuthorizationsHandler(JsonHandler):

    def get(self):
        # for k in dir(self.request):
            # if not callable(getattr(self, k)):
                    # print(k, getattr(self.request, k))
        # 登录模式1
        email = self.get_argument('email', '')
        password = self.get_argument('password', '')
        # 登录模式2 Authorization: Basic base64("user:passwd")
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


class WxLoginHandler(JsonHandler):
    # https://api.weixin.qq.com/sns/jscode2session?appid=APPID&secret=SECRET&js_code=JSCODE&grant_type=authorization_code

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
        if not session_key or not openid:
            print(r)
            # return self.write_json()
            return self.write_error(402)

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
            self.res['is_admin'] = admin.is_admin(doc['id'])
            if doc['id'] in wx_admin_ids:
                self.res['is_admin'] = True

            return self.write_json()
        else:
            # res['id'] = User.find().count() + 1
            res = {}
            res['user_email'] = openid + '@wechat'
            res['user_pass'] = session_key
            res['user_name'] = 'null'
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
        # 获取头像
        if user.user_email.endswith('@wechat'):
            user.gravatar = get_avatar_by_wechat(user._id)
        else:
            user.gravatar = get_avatar(user.user_email, 100)
        # 删除敏感信息
        user = dict(user)
        user.pop('_id')
        user.pop('user_pass')
        # 添加管理员信息
        user['is_admin'] = admin.is_admin(user['id'])
        if user['id'] in wx_admin_ids:
            user['is_admin'] = True
        # 输出
        self.res = user
        return self.write_json()

    @tornado.web.authenticated
    def post(self):
        user = User.by_sid(self.current_user['user_id'])

        # Do not save user info if not necessary
        # 小程序的用户信息：
        # avatarUrl   String  用户头像，最后一个数值代表正方形头像大小（有0、46、64、96、132数值可选，0代表640 * 640正方形头像），用户没有头像时该项为空。若用户更换头像，原有头像URL将失效。
        # city nickName
        # 没有用到的暂时没有保存：
        # gender String  用户的性别，值为1时是男性，值为2时是女性，值为0时是未知
        # province    String  用户所在省份
        # country String  用户所在国家
        # language    String  用户的语言，简体中文为zh_CN
        # iv
        # signature
        # encryptedData
        # isignaturev

        # 获取待更新字段
        tags = self.get_argument('tags', None)
        remove_tag = self.get_argument('remove_tag', None)
        name = self.get_argument('name', None)
        if not name:
            name = self.get_argument('nickName', None)
        avatar_url = self.get_argument('avatarUrl', None)
        city = self.get_argument('city', None)
        say = self.get_argument('say', None)

        # 更新信息
        if avatar_url:
            try:
                r = requests.get(avatar_url)
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
        if city:
            user['user_city'] = city
        if name:
            user['user_name'] = name
        if say:
            user['user_say'] = say

        raw_rags = user['user_tags']
        if tags:
            new_tags = tags.strip().split(',')
            for t in new_tags:
                if t not in raw_rags:
                    raw_rags.append(t)
        if remove_tag:
            if remove_tag in raw_rags:
                raw_rags.remove(remove_tag)
        user['user_tags'] = raw_rags
        user.save()

        is_admin = admin.is_admin(user['id'])
        # user['is_admin'] =
        # user.pop('_id')

        # 只输出指定信息
        auser = {}
        auser['user_tags'] = user['user_tags']
        auser['is_admin'] = is_admin
        if user['id'] in wx_admin_ids:
            auser['is_admin'] = True
        self.res = auser
        return self.write_json()
