# -*- coding: utf-8 -*-

# site_domain = 'http://0.0.0.0:8080'  # 本地开发测试用
# site_domain = 'http://anwensf.com/'  # 域名

site_info = {
    'title': 'Anwen',
    'subtitle': 'create and share something nice',
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

debug = True

port = 8888

db = {
    'name': 'anwen',
}

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

node_about = {
    'home': {
        'name': 'Newest Share',
        'about': 'Create and Share, which can hit your heart~'
    },
    'pencil': {
        'name': 'Create',
        'about': 'Those created, we will cherish years later~'
    },
    'music': {
        'name': 'Music',
        'about': 'Music which touch heart~'
    },
    'film': {
        'name': 'Video',
        'about': 'Light and shadow fragment record every inch sensation'
    },
    'book': {
        'name': 'Book',
        'about': 'Books, book reviews or essays'
    },
    'eyeopen': {
        'name': 'Eyeopen',
        'about': 'feel and change the world'
    },
    'ask': {
        'name': 'Asks',
        'about': 'Give us a question, we can make the universe more fun'
    },
    'sf': {
        'name': 'SF',
        'about': 'Science Fiction is a life style, stars and ocean'
    },
    'fire': {
        'name': 'Actions',
        'about': 'Record move of dreamers, maybe notsogood, we are trying'
    }
}

try:
    from server_setting import *
except:
    pass

# Old is blog.anwensf.com. Too many. So we let www.anwensf.com jump to blog.

old_links = [
    u'【5月21日】首届武汉地区高校科幻交流会全程记录/',
    u'机器人的时代，离我们还远吗？/',
    u'《银河帝国三部曲》简介/',
    u'赫胥黎和《美妙的新世界》/',
    u'太阳帆船/',
    u'克拉克和《童年的终结》/',
    u'冰柱沉入南极洲海底的可怕景象，宛如一部恐怖的/',
    u'艾米莉的那些事儿/',
    u'《趁生命气息逗留》评论——寻找怎样成为人的路/',
    u'不死的巨匠——向阿西莫夫敬礼/',
    u'上帝之子-等了很长了/',
    u'中国美术学院科幻艺术协会/',
    u'阿西莫夫和《钢窟》/',
]
