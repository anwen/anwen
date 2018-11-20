# -*- coding: utf-8 -*-
port = 8888
debug = True
SEND_ERROR_MAIL = True
use_ssl = False

# 本网站域名 用于: email激活
# site_url = 'http://localhost:8888'  # 本地开发测试用
site_url = 'https://anwensf.com'
API = 'https://anwensf.com/api/'


db = {
    'name': 'anwen',
    'host': '127.0.0.1',
    'port': 27017,
    # 'username': '',
    # 'password': '',
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
    'title': '安问',
    'subtitle': '分享和创造有趣的东西',
    'intro': 'Discover, think, share, action together~',
    'author': 'Anwen',
    'email': 'anwen.in@gmail.com',  # optional
    'weibo': 'http://weibo.com/askender',  # optional
    'douban': 'http://site.douban.com/askender/',  # optional
    'description': '自由开源的理想主义社区与创造分享平台,致力于创造和分享最打动大家的或有趣的东西',
}

node_list = [
    'book',
    'film',
    'music',
    'sf',
    'goodlink',
    'ask',
    'eyeopen',
    'fire',
    'deleted',
]
node_about = {
    'home': {
        'icon': 'home',
        'name': 'Newest Share',
        'about': 'Create and Share, which can hit your heart~'
    },

    'book': {
        'icon': 'book',
        'name': 'Book',
        'about': 'Books, book reviews or essays'
    },
    'film': {
        'icon': 'film',
        'name': 'Film',
        'about': 'Light and shadow fragment record every inch sensation'
    },
    'music': {
        'icon': 'music',
        'name': 'Music',
        'about': 'Music which touch heart~'
    },
    'sf': {
        'icon': 'road',
        'name': 'SF',
        'about': 'Science Fiction is a life style, stars and ocean'
    },
    'goodlink': {
        'icon': 'link',
        'name': 'Goodlink',
        'about': 'nice things need share'
    },


    'ask': {
        'icon': 'question-sign',
        'name': 'Asks',
        'about': 'Give us a question, we can make the universe more fun'
    },
    'eyeopen': {
        'icon': 'eye-open',
        'name': 'Eyeopen',
        'about': 'feel and know yourself and the world'
    },

    'fire': {
        'icon': 'fire',
        'name': 'Create',
        'about': 'Record action of dreamers, maybe not so good, we are trying'
    },
    'deleted': {
        'icon': 'delete',
        'name': 'Deleted',
        'about': 'not good'
    },

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


EMAIL_HOST = 'smtp.exmail.qq.com'
EMAIL_PORT = 465
# EMAIL_USE_TLS = False
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'hello@anwensf.com'
EMAIL_HOST_PASSWORD = 'set in server_setting'
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
    from options.server_setting import *
except:
    pass

try:
    from options.local_setting import *
except:
    pass
