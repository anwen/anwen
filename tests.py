#!/usr/bin/env python
# -*- coding: utf-8 -*-
import uuid
import random
import unittest
import tornado.testing
from json import dumps as jdump
from json import loads as jload
import tornado.web


def random_str():
    return uuid.uuid4().hex


def generate_args(*args, **kwargs):
    dic = dict([(a, random_str()) for a in args])
    dic.update(kwargs)
    return dic


def random_args(d):
    r = {}
    for k, v in d.iteritems():
        if isinstance(v, int):
            v = v * random.randint(0, 10)
        elif isinstance(v, unicode):
            v = unicode(random_str())
        elif isinstance(v, str):
            v = random_str()
        r[k] = v
    return r


def assert_similar(d1, d2):
    assert isinstance(d1, dict)
    assert isinstance(d2, dict)
    if d1 > d2:
        bigger, smaller = d1, d2
    else:
        bigger, smaller = d2, d1
        for k, v in smaller.iteritems():
            assert bigger[k] == v


class HttpTest(tornado.testing.AsyncHTTPTestCase):
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    create = True
    clist = ''
    cdict = {}
    data = {}

    def get_app(self):
        from hello import application
        return application

    def setUp(self):
        super(HttpTest, self).setUp()
        getattr(self, 'set_up', lambda: None)()
        if self.create:
            res = self.fetch(
                self.res_url, method='POST', body=self.jcreate_args)
            assert res.code == 201 or 200
            json = jload(res.body)
            assert_similar(json, self.create_args)
            try:
                self.oid = json['_id']
            except:
                pass

    def tearDown(self):
        getattr(self, 'tear_down', lambda: None)()
        if self.create:
            res = self.fetch(self.res_url + self.oid, method='DELETE')
            assert res.code == 200
            res = self.fetch(self.res_url + self.oid, method='GET')
            assert res.code == 404
            super(HttpTest, self).tearDown()

    def fetch_n(self, *args, **kwargs):
        return super(HttpTest, self).fetch(*args, **kwargs)

    def fetch(self, *args, **kwargs):
        if 'headers' not in kwargs:
            kwargs.update({'headers': {'Content-Type': 'application/json'}})
        return super(HttpTest, self).fetch(*args, **kwargs)


def common_setup(self):
    self.create_args = generate_args(
        *self.clist, **self.cdict
    )
    self.jcreate_args = jdump(self.create_args)
    updated = random_args(self.create_args)
    try:
        updated.update(self.udict)
    except:
        pass
    self.update_args = updated
    self.jupdate_args = jdump(self.update_args)


def common_update(self, url, method='PATCH'):
    res = self.fetch(
        url, method=method, body=jdump(self.update_args))
    if method == 'PATCH':
        assert res.code == 200
    elif method == 'PUT':
        assert res.code == 201
    assert res.body


def common_read(self):
    if hasattr(self, 'oid'):
        res = self.fetch(self.res_url + self.oid, method='GET')
        assert res.code == 200
        assert isinstance(jload(res.body), dict)
        if self.create:
            assert_similar(jload(res.body), self.create_args)

    res = self.fetch(self.res_url, method='GET')
    assert res.code == 200
    json = jload(res.body)
    assert isinstance(json, dict)
    return json


class TestIndex(HttpTest):
    create = False

    def test_read(self):
        res = self.fetch('/', method='GET')
        assert res.code == 200
        assert res.body


class TestUsers(HttpTest):
    res_url = '/users/'
    clist = 'user_email', 'user_pass'

    def set_up(self):
        res = self.fetch('/joinus', method='GET')
        assert res.code == 200
        res = self.fetch('/login', method='GET')
        assert res.code == 200
        # assert 'Set-Cookie' in res.headers
        # assert res.headers['Set-Cookie'].startswith('_xsrf=')
        # _xsrf = res.headers['Set-Cookie'].split(';')[0].split('=')[1]
        assert res.body
        common_setup(self)

    def tear_down(self):
        pass

    def test_read(self):
        common_read(self)

    def test_update(self):
        common_update(self, self.res_url + self.oid)


class TestShares(HttpTest):
    res_url = '/shares/'
    clist = 'markdown', 'title'

    def set_up(self):
        # res = self.fetch('/share', method='GET')
        # assert res.code == 200
        # assert res.body
        common_setup(self)

    def tear_down(self):
        pass

    def test_read(self):
        common_read(self)

    def test_update(self):
        common_update(self, self.res_url + self.oid)


TEST_MODULES = [
    'tests',
]


def all():
    return unittest.defaultTestLoader.loadTestsFromNames(TEST_MODULES)


def main():
    tornado.testing.main()

if __name__ == '__main__':
    main()
