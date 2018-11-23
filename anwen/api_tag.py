# -*- coding:utf-8 -*-
from .api_base import JsonHandler
from utils import get_tags


class TagsHandler(JsonHandler):

    def get(self):
        d_tags = get_tags()
        self.res = d_tags
        self.write_json()
