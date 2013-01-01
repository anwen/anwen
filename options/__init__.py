# -*- coding: utf-8 -*-
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
    'xsrf_cookies': True,
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
