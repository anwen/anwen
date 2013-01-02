#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import time
import yaml
import sys
sys.path.append('..')
from db import User, Share, Ande, Comment, Hit


res = User
if res.find().count() == 0:
    docs = yaml.load(file('anwen_user.yaml', 'r').read())
    for doc in docs:
        doc['user_jointime'] = time.mktime(
            time.strptime(doc['user_jointime'], '%Y-%m-%d %H:%M:%S'))
        doc['user_domain'] = str(doc['user_domain'])
        res.new(doc)
    print 'users done'

res = Share
if res.find().count() == 0:
    docs = yaml.load(file('anwen_share.yaml', 'r').read())
    for doc in docs:
        doc['published'] = time.mktime(
            time.strptime(doc['published'], '%Y-%m-%d %H:%M:%S'))
        doc['updated'] = time.mktime(
            time.strptime(doc['updated'], '%Y-%m-%d %H:%M:%S'))
        res.new(doc)
    print 'shares done'

res = Ande
if res.find().count() == 0:
    docs = yaml.load(file('anwen_ande.yaml', 'r').read())
    for doc in docs:
        # doc['usersay'] = str(doc['usersay'])
        doc['chattime'] = time.mktime(
            time.strptime(doc['chattime'], '%Y-%m-%d %H:%M:%S'))
        res.new(doc)
    print 'andes done'

res = Comment
if res.find().count() == 0:
    docs = yaml.load(file('anwen_comment.yaml', 'r').read())
    for doc in docs:
        doc['commenttime'] = time.mktime(
            time.strptime(doc['commenttime'], '%Y-%m-%d %H:%M:%S'))
        res.new(doc)
    print 'comments done'

res = Hit
if res.find().count() == 0:
    docs = yaml.load(file('anwen_hit.yaml', 'r').read())
    for doc in docs:
        doc['hittime'] = time.mktime(
            time.strptime(doc['hittime'], '%Y-%m-%d %H:%M:%S'))
        res.new(doc)
    print 'hits done'

docs = ['User', 'Share', 'Comment', 'Ande', 'Hit']


def run_export(name):
    if name == 'all':
        for doc in docs:
            doc_export(doc)
    elif name in docs:
        doc_export(name)


def doc_export(doc):
    d = eval(doc)
    obj = d.find()
    res = []
    for i in obj:
        i['_id'] = str(i['_id'])
        i = convert(i)
        res.append(i)
    document = open(doc + '.yaml', 'w')
    yaml.dump(res, document, canonical=False, default_flow_style=False)


def convert(input):
    if isinstance(input, dict):
        return dict((convert(k), convert(v)) for k, v in input.iteritems())
    elif isinstance(input, list):
        return [convert(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input

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
    '-n', '--name',
    dest='name',
    action='store',
    type=str,
    default='all',
    help='document name'
)

if __name__ == '__main__':
    args = parser.parse_args()
    if args.run_import:
        pass
        # run_import(args.name)
    elif args.run_export:
        run_export(args.name)
