# -*- coding: utf-8 -*-
import time
from db.ext import BaseModel


class Share(BaseModel):
    __collection__ = 'Share_Col'
    use_autorefs = True
    structure = {
        # 内部使用
        'id': int,
        # 兼容rss标准
        'title': str,
        'link': str,
        'source': str,  # source_title
        'category': str,  # category_title
        'content': str,
        'summary': str,

        'markdown': str,  # 安问
        'sharetype': str,  # rss
        'slug': str,
        'user_id': int,
        'status': int,  # 0=public, 1=draft, -1=deleted
        'tags': list,

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

        'published': float,
        'updated': float,
        'suggested': float,
        # deleted
        'upload_img': str,
        'author': str,
    }
    required_fields = ['id', 'user_id', 'sharetype', 'title']
    default_values = {
        'tags': [],
        'markdown': '',
        'link': '',
        'slug': '',
        'post_img': '',
        'source': '',
        'category': '',
        'content': '',
        'summary': '',
        'author': '',
        # 'upload_img': str,

        'commentnum': 0,
        'likenum': 0,
        'dislikenum': 0,
        'hitnum': 0,
        'suggestscore': 0.0,
        'score': 0.0,

        'vote_open': 0,
        'vote_title': '',

        'status': 0,  # 0=published,1=draft,2=deleted
        'published': time.time,  # for rss, it is real published time
        'updated': time.time,
        'suggested': time.time,
    }

    def by_slug(self, slug):
        return self.find_one({'slug': slug})

    def by_title(self, title):
        return self.find_one({'title': title})

    def count_by_tag(self, tag):
        return self.find({'tags': tag}).count()
