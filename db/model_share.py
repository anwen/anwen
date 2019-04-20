# -*- coding: utf-8 -*-
import time
from db.ext import BaseModel


class Share(BaseModel):
    __collection__ = 'Share_Col'
    use_autorefs = True
    structure = {
        # 内部使用
        'id': int,

        # 与rss一致
        'title': str,
        'link': str,
        'published': float,
        # 兼容rss标准
        'source': str,  # source_title
        'category': str,  # category_title
        # 'summary': str, # 复用content

        'markdown': str,  # 安问
        # 常规信息
        'sharetype': str,  # rss
        'tags': list,
        'user_id': int,
        'slug': str,
        'status': int,  # 0=public, 1=draft, -1=deleted

        # optional
        'content': str,
        'post_img': str,
        # 冗余信息
        'commentnum': int,
        'likenum': int,
        'dislikenum': int,
        'hitnum': int,
        'suggestscore': float,
        'score': float,

        'vote_open': int,
        'vote_title': str,

        'updated': float,
        # deleted
        'upload_img': str,

    }
    required_fields = ['id', 'user_id', 'sharetype']
    default_values = {
        'markdown': '',
        'tags': [],
        'link': '',
        'slug': '',
        'post_img': '',
        'source': '',
        'category': '',

        'commentnum': 0,
        'likenum': 0,
        'dislikenum': 0,
        'hitnum': 0,
        'suggestscore': 0.0,
        'score': 0.0,

        'vote_open': 0,
        'vote_title': '',

        'status': 0,  # 0=published,1=draft,2=deleted
        # 'published_real': 0,
        'published': time.time,  # for rss, it is real published time
        'updated': time.time,

        # 'title': str,
        # 'slug': str,
        # 'content': str,
        # 'upload_img': str,

    }

    def by_slug(self, slug):
        return self.find_one({'slug': slug})
