#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from db import User, Share, Comment, Hit, Tag, Feedback, Admin, Like, Viewpoint, Collect
import argparse
import yaml
import sys
import os
import re
from bson import ObjectId
sys.path.append('..')

doc_list = ['User', 'Comment', 'Hit', 'Tag', 'Feedback', 'Admin',
            'Like', 'Viewpoint', 'Collect', 'Share']
