#!/usr/bin/env python3
# encoding:utf-8
from utils.img_tools import make_post_thumb
from PIL import Image
import requests
import datetime
import sys
import options
import os
from pymongo import MongoClient
conn = MongoClient()
adb = conn.anwen
adb.authenticate(options.db['username'], options.db['password'])
sys.path.append('.')
from db import Tag, Share  # noqa


def check():
    for i in adb.Share_Col.find().sort('_id', 1):
        upload_img = i['upload_img']
        assert not upload_img
        if i['status'] >= 1:
            continue
        post_img = i['post_img']
        if post_img:
            print('not published:s', post_img)
            print('https://anwensf.com/share/{}'.format(i['id']))
    return
    for i in adb.Share_Col.find().sort('_id', 1):
        if i['status'] < 1:
            continue
        post_img = i['post_img']
        if post_img:
            continue
        markdown = i['markdown']
        if not markdown:
            print(1, i['title'])
            print('https://anwensf.com/share/{}'.format(i['id']))


def add():
    # fname = 'https://pic.001all.com/Wallpaper/Desktop%20Wallpaper/Space/FTP/2560%20x%201440/Shiny%20Star%20Wallpapers%20HD%202560%20x%201440%20Pixels%20Resolution.jpg'
    fname = sys.argv[1]
    print(fname)
    # 上传的图片不能超过2M
    ext = fname.split('?')[0].split('.')[-1]
    ext = '.'+ext.lower()
    print(ext)
    assert ext in ['.jpg', '.jpeg', '.gif', '.png', '.bmp']
    img_dir = 'static/upload/img'
    now = datetime.datetime.now()
    t = now.strftime('%Y%m%d_%H%M%S_%f')
    img_name = '%s%s' % (t, ext)
    img_path = '%s/%s' % (img_dir, img_name)
    # body = ''
    print(img_path)
    r = requests.get(fname, verify=False, stream=True)  # stream=True)
    chunk_size = 100
    with open(img_path, 'wb') as image:
        # image.write(r.raw.read())
        # r.raw
        for chunk in r.iter_content(chunk_size):
            image.write(chunk)

    im = Image.open(img_path)
    width, height = im.size
    if width / height > 5 or height / width > 5:
        os.remove(img_path)  # 判断比例 删除图片
        print('请不要上传长宽比例过大的图片')
    else:
        # 创建1200x550 750x230 365x230缩略图
        make_post_thumb(img_path, sizes=[
            (1200, 550), (750, 230), (365, 230), (260, 160)
        ])
        print('done')

        # def add2():
        # fname = 'static/upload/img/20190614_010621_032739.jpg'
        # post_img = '20190614_010621_032739_1200.jpg'
        # share_id = 322
        post_img = img_path.split('/')[-1]
        post_img = post_img.split('.')[0] + '_1200.jpg'
        share_id = sys.argv[2]
        share_id = int(share_id)

        r = adb.Share_Col.update({'id': share_id}, {'$set': {'post_img': post_img}})
        print(r)


# check()
# add()
# check()
# add2()
add()
