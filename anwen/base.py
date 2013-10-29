# -*- coding:utf-8 -*-

import json
from bson import ObjectId
from tornado.escape import json_decode
from tornado.web import RequestHandler, HTTPError
from pymongo import ASCENDING, DESCENDING
from log import logger
from options import site_info, node_list, node_about


class BaseHandler(RequestHandler):

    def get_template_namespace(self):
        ns = super(BaseHandler, self).get_template_namespace()
        ns.update({
            'site_info': site_info,
            'node_list': node_list,
            'node_about': node_about,
        })
        return ns

    def get_current_user(self):
        user_json = self.get_secure_cookie("user")
        if not user_json:
            return None
        return json_decode(user_json)

    def get_user_lang_by_cookie(self):
        user_json = self.get_cookie("lang")
        if not user_json:
            return None
        return json_decode(user_json)

    def get_user_lang(self, default="en_US"):
        lang_by_cookie = self.get_user_lang_by_cookie()
        if lang_by_cookie:
            return self.current_user
        if "Accept-Language" in self.request.headers:
            languages = self.request.headers["Accept-Language"].split(",")
            locales = []
            for language in languages:
                parts = language.strip().split(";")
                if len(parts) > 1 and parts[1].startswith("q="):
                    try:
                        score = float(parts[1][2:])
                    except (ValueError, TypeError):
                        score = 0.0
                else:
                    score = 1.0
                locales.append((parts[0], score))
            if locales:
                locales.sort(key=lambda l_s: l_s[1], reverse=True)
                return locales[0][0]
        self.set_cookie('lang', default)
        return default

    def write_error(self, status_code):
        self.render('error.html', status_code=status_code)
        #     super(RequestHandler, self).write_error(status_code, **kwargs)

    def write_json(self, obj):
        """Writes the JSON-formated string of the given obj
        to the output buffer"""

        self.set_header('Content-Type', 'application/json')
        from json import dumps

        def handler(obj):
            if hasattr(obj, 'to_json'):
                return obj.to_json()
            elif isinstance(obj, ObjectId):
                return str(obj)
            else:
                return dict(obj)
        return self.write(dumps(obj, default=handler))


class JSONHandler(BaseHandler):

    """Every API handler should inherit from this class."""

    def get_json_arg(self, name=None, *args):
        """Returns the value of the argument with the given name,
        from JSON-formated body"""

        headers = self.request.headers
        if not ('Content-Type' in headers
                and 'application/json' in headers['Content-Type']):
            logger.warn('Content-Type is not JSON, ignored.')
            return None
        try:
            obj = json.loads(self.request.body)
        except ValueError:
            logger.warn('Request body is not JSON formatted!')
            return None
        if not name:
            return obj
        try:
            return obj[name]
        except KeyError:
            if len(args) > 0:
                return args[0]
            else:
                raise HTTPError(
                    400,
                    'Missing argument [%s]!' % name)


def pop_spec(args, name, default=None):
    if name in args:
        return args.pop(name)[0]
    else:
        return default


class CommonResourceHandler(JSONHandler):
    # patch method is deleted
    res = None
    is_array = True

    @property
    def _objects(self):
        args = self.request.arguments.copy()

        _start = pop_spec(args, '_start')
        _limit = pop_spec(args, '_limit')

        _sort = pop_spec(args, '_sort')

        for k, v in args.copy().iteritems():
            try:
                v = json.loads(v[0])
            except ValueError:
                v = v[0]
            args[k] = v

        for key, value in args.copy().iteritems():
            if '_id' in key:
                if isinstance(value, list):
                    v = {'$in': [ObjectId(x) for x in value]}
                elif isinstance(value, unicode):
                    v = ObjectId(value)
                args[key] = v

        cur = self.res.find(args)

        if _sort:
            direction = DESCENDING if _sort.startswith('-') else ASCENDING
            cur = cur.sort(_sort.strip('-+'), direction)

        res = cur

        if _start and _limit:
            l = int(_start)
            limit = int(_limit)
            res = res[l:l + limit]
        total = len(res) if isinstance(res, list) else res.count()
        return {'total': total, 'objs': list(res)}

    def count(self):
        self.write_json({'total': self._objects.count()})

    def get(self, rid=None):
        if not rid:
            res = self._objects
        else:
            res = self.res.by_id(rid)
        if not res:
            return self.set_status(404)
        else:
            self.write_json(self.post_get(res))

    def post_get(self, res_obj):
        return res_obj

    def pre_post(self, json_arg):
        new_obj = self.res
        return new_obj.new(json_arg)

    def post(self):
        res = self.pre_post(self.get_json_arg())
        if not res:
            return self.set_status(500)
        self.set_status(201)
        self.write_json(self.post_post(res))

    @staticmethod
    def post_post(res_obj):
        return res_obj

    def delete(self, rid=None):
        rids = [rid]
        if not rid:
            rids = self.get_json_arg()
            if not isinstance(rids, list):
                # self.res.collection.drop()
                return
        for r in rids:
            res = self.res.by_id(r)
            if not res:
                return self.set_status(404)
            self.post_delete(res)
            res.delete()

    def post_delete(self, deleting_res_obj):
        pass
