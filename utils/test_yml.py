#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import locale
print(locale.getdefaultlocale())
print(locale.getpreferredencoding())

import yaml

data = dict(
    A='a',
    B=dict(
        C='c',
        D='d',
        E='你好',
    )
)

with open('data.yml', 'w') as outfile:
    yaml.dump(
        data, outfile,
        default_flow_style=False,
        allow_unicode=True,
        # encoding='utf-8',
    )
