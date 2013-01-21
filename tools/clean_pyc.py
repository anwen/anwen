#! /usr/bin/env python
#coding=utf-8

#for windows. = rm -rf *.pyc

import os

for dir, folders, files in os.walk('.'):
    for file in files:
        root, ext = os.path.splitext(file)
        if ext == '.pyc':
            os.remove(os.path.abspath(os.path.join(dir, file)))
