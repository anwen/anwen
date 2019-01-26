# -*- coding: utf-8 -*-
import time
from db.ext import BaseModel


class Share(BaseModel):
    __collection__ = 'Share_Col'
    use_autorefs = True
    structure = {
        'id': int,
        'title': str,
        'markdown': str,
        'tags': list,
        'link': str,
        'user_id': int,
        'slug': str,
        'sharetype': str,
        # optional
        'content': str,
        'post_img': str,

        'commentnum': int,
        'likenum': int,
        'dislikenum': int,
        'hitnum': int,
        'suggestscore': float,
        'score': float,

        'vote_open': int,
        'vote_title': str,

        'status': int,  # 0=public, 1=draft, -1=deleted
        'published': float,
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

        'commentnum': 0,
        'likenum': 0,
        'dislikenum': 0,
        'hitnum': 0,
        'suggestscore': 0.0,
        'score': 0.0,

        'vote_open': 0,
        'vote_title': '',

        'status': 0,  # 0=published,1=draft,2=deleted
        'published': time.time,
        'updated': time.time,

        # 'title': str,
        # 'slug': str,
        # 'content': str,
        # 'upload_img': str,

    }

    def by_slug(self, slug):
        return self.find_one({'slug': slug})
