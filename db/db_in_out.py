#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from db import User, Share, Comment, Hit, Tag, Feedback, Admin, Like, Viewpoint, Collect
import argparse
import yaml
import sys
import os
import re
from bson import ObjectId
import time
sys.path.append('..')
# db.dropDatabase()

doc_list = ['User', 'Comment', 'Hit', 'Tag', 'Feedback', 'Admin',
            'Like', 'Viewpoint', 'Collect', 'Share']


# Webcache
# Share


def make_doc():
    print(os.path)
    if os.path.isfile('data/Share.yaml'):
        print('load yaml')
        docs = yaml.load(open('data/Share.yaml', 'r').read())
        for i in docs:
            filename = '../docs/shares/%s_%s.md' % (i['id'], i['slug'])
            title = i['title']
            markdown = i['markdown']
            filebody = '%s\n========\n\n\n%s' % (
                title, re.sub(r'\r\n', r'\n', markdown))
            # with open(filename, 'w') as share:
            #     share.write(filebody)
            print(filename.encode('u8'))
            with open(filename, 'wb') as share:
                share.write(filebody.encode('u8'))
            print('share {} are markdownd'.format(i['id']))
        print('shares are markdownd')


def run_import(name):
    if name == 'all':
        for doc in doc_list:
            doc_import(doc)
    elif name in doc_list:
        doc_import(name)


def doc_import(doc):
    d = eval(doc)
    if d.find().count() == 0:
        if doc == 'User' and not os.path.isfile('data/' + doc + '.yaml'):
            doc = '%sSafe' % doc
            print('load usersafe')
        docs = yaml.load(open('data/' + doc + '.yaml', 'r').read())
        for i in docs:
            i['_id'] = ObjectId(i['_id'])
            # if isinstance(i['tags'], str):
            #     i['tags'] = i['tags'].split()
            if doc == 'UserSafe':
                i['user_email'] = ''
                i['user_pass'] = ''
            d.new(i)
        print('%s done' % doc)


def run_export(name):
    if name == 'all':
        for doc in doc_list:
            doc_export(doc)
    elif name in doc_list:
        doc_export(name)
    if name == 'User' and os.path.isfile('data/User.yaml'):
        with open('data/User.yaml') as input_file:
            with open('data/UserSafe.yaml', 'w') as output_file:
                a = re.sub(r'  user_pass: \S*\n', '', input_file.read())
                b = re.sub(r'  user_email: \S*\n', '', a)
                output_file.write(b)
        print('users are safe')
    # make_doc()


def doc_export(doc):
    d = eval(doc)
    print(d)
    obj = d.find().sort('_id', 1)
    if obj.count() == 0:
        return
    res = []
    for i in obj:
        if doc == 'Share' and i['id'] > 4500:
            time.sleep(0.01)
            print('sleep')
        print(i['_id'], i['id'])
        i['_id'] = str(i['_id'])
        if doc == 'Share' and i['sharetype'] == 'rss':
            print('skip rss')
            continue
        print(i['_id'], i['id'])
        i = dict(i)
        i = convert(i)
        res.append(i)

    with open('data/' + doc + '.yaml', 'w') as document:
        yaml.dump(
            res, document,
            default_flow_style=False,  # block style
            allow_unicode=True,
            # encoding='utf-8',
            # default_style=None,
            # canonical=False, indent=False, width=None,
            # line_break=None,
            # explicit_start=None, explicit_end=None,
            # version=None, tags=None
        )


def convert(sth):
    if isinstance(sth, dict):
        return dict((convert(k), convert(v)) for k, v in sth.items())
    elif isinstance(sth, list):
        return [convert(element) for element in sth]
    # elif isinstance(sth, byte):  # unicode
        # return sth.decode('utf-8')
    # elif isinstance(sth, str):  # unicode
    #     return sth.encode('utf-8')
    else:
        return sth


parser = argparse.ArgumentParser(
    description='Anwen DB in or out')

parser.add_argument(
    '-i', '--in',
    dest='run_import',
    action='store_const',
    const=True,
    default=False,
    help='run import'
)

parser.add_argument(
    '-o', '--out',
    dest='run_export',
    action='store_const',
    const=True,
    default=False,
    help='run export'
)

parser.add_argument(
    '-d', '--doc',
    dest='make_doc',
    action='store_const',
    const=True,
    default=False,
    help='make doc'
)

parser.add_argument(
    '-n', '--name',
    dest='name',
    action='store',
    type=str,
    default='all',
    help='document name'
)

if __name__ == '__main__':
    args = parser.parse_args()
    print(User, Share, Comment, Hit, Tag, Feedback, Admin, Like, Viewpoint, Collect)
    if args.run_import:
        run_import(args.name)
    elif args.run_export:
        run_export(args.name)
    elif args.make_doc:
        make_doc()
