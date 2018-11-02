# -*- coding:utf-8 -*-
from .api_base import JsonHandler
from options import API


class ApiHandler(JsonHandler):

    def get(self):
        # incoming_arg_1 = self.request.arguments['some_arg_1']
        self.res['shares_url'] = API + 'shares'
        self.res['shares_url_desc'] = 'show all shares'
        self.res['shares_url_query'] = 'has_vote:1 ;'
        self.res['share_url'] = API + 'shares/{id}'
        self.res['share_url_desc'] = 'show one share by id'
        self.res['authorizations_url'] = API + 'authorizations'
        # self.res['user_url'] = API + 'users/{user_id}'
        # self.res['current_user_url'] = API + 'user'
        self.write_json()
