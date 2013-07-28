# -*- coding: utf-8 -*-

debug = True
port = 8888

db = {
    'name': 'anwen',
    'host': '127.0.0.1',
    'port': 27017,
    # 'username': 'aw',
    # 'password': 'lb',
}

default_editor = ''  # wysiwyg

web_server = {
    'login_url': '/login',
    'template_path': 'templates',
    'static_path': 'static',
    'locale_path': 'locale',
    'xsrf_cookies': False,
    'cookie_secret': "11oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
    'autoescape': None,
    'debug': debug,
}

site_info = {
    'title': 'Anwen',
    'subtitle': 'create and share something nice',
    'intro': 'Discover, think, share, action together~',
    'author': 'Anwen',
    'email': 'anwen.in@gmail.com',  # optional
    'weibo': 'http://weibo.com/askender',  # optional
    'douban': 'http://site.douban.com/askender/',  # optional
    'description': 'freedom and open-source dream world, \
which try to create and share things touch your soul',

    'bottom_info': '''
<div class="pull-right">
    <a href="https://github.com/askender/anwen.in">开源@github</a>
    <a href="/about">关于安问</a>
    <a href="/help">帮助中心</a>
    <a href="/changelog">行动日志</a>
</div>
<div class="pull-left copyleft">
    Copyleft © 2011-2013 安问
</div>
''',

}

node_list = [
    'eyeopen', 'music', 'film', 'book',
    'ask', 'sf', 'pencil', 'fire',
]
node_about = {
    'home': {
        'name': 'Newest Share',
        'about': 'Create and Share, which can hit your heart~'
    },
    'eyeopen': {
        'name': 'Eyeopen',
        'about': 'feel and know yourself and the world'
    },
    'music': {
        'name': 'Music',
        'about': 'Music which touch heart~'
    },
    'book': {
        'name': 'Book',
        'about': 'Books, book reviews or essays'
    },
    'film': {
        'name': 'Video',
        'about': 'Light and shadow fragment record every inch sensation'
    },
    'ask': {
        'name': 'Asks',
        'about': 'Give us a question, we can make the universe more fun'
    },
    'sf': {
        'name': 'SF',
        'about': 'Science Fiction is a life style, stars and ocean'
    },
    'pencil': {
        'name': 'Create',
        'about': 'Those created, we will cherish years later~'
    },
    'fire': {
        'name': 'Actions',
        'about': 'Record move of dreamers, maybe notsogood, we are trying'
    }
}

log = {
    'log_max_bytes': 5 * 1024 * 1024,  # 5M
    'backup_count': 10,
    'log_path': {
        # logger of running server; DONOT change the name 'logger'
        'logger': 'log/files/server.log',
        # logger of user behavior
        'user_logger': 'log/files/user.log'
    }
}

MAX_WAIT_SECONDS_BEFORE_SHUTDOWN = 2


# 本网站域名  email激活用地址
# site_url = 'http://0.0.0.0:8888'  # 本地开发测试用
site_url = 'http://anwensf.com'

EMAIL_HOST = 'smtp.exmail.qq.com'
EMAIL_PORT = 25
EMAIL_USE_TLS = False
EMAIL_HOST_USER = 'hello@anwensf.com'
EMAIL_HOST_PASSWORD = 'naw130621'
EMAIL_HOST_NICK = '安问'
SERVICE_EMAIL = 'hello@anwensf.com'
superadmin_email = 'askender43@gmail.com'
msg_footer = ''.join([
    '<p>如果你有任何疑问，可以回复这封邮件向我们提问。</p>',
])

douban_redirect_uri = 'http://anwensf.com/douban_login'
douban = {
    'douban_api_key': '032288b47028601309679a1d50792039',
    'douban_api_secret': '9b29399b82721746',
}

try:
    from .server_setting import *
except:
    pass
