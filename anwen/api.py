# -*- coding:utf-8 -*-
from .api_base import JsonHandler
import options
from options import API


class ApiHandler(JsonHandler):

    def get(self):
        # incoming_arg_1 = self.request.arguments['some_arg_1']
        self.res['current_user_url'] = API + 'user'
        self.res['authorizations_url'] = API + 'authorizations'
        self.res['user_url'] = API + 'users/{user_id}'
        self.res['share_url'] = API + 'shares/{share_id}'
        self.write_json()
