#!/usr/bin/env python
# coding: utf-8

import os
import Image
import ImageFilter


def dict_remove(d, *keys):
    for k in keys:
        if k in d:
            del d[k]


class MyGaussianBlur(ImageFilter.Filter):
    # 高斯模糊
    name = "GaussianBlur"

    def __init__(self, radius=2, bounds=None):
        self.radius = radius
        self.bounds = bounds

    def filter(self, image):
        if self.bounds:
            clips = image.crop(self.bounds).gaussian_blur(self.radius)
            image.paste(clips, self.bounds)
            return image
        else:
            return image.gaussian_blur(self.radius)


# 生成头像缩略图 （供裁剪用）
# def make_thumb(path, sizes=[(160,160)]):
def make_thumb(path):
    """
    sizes 参数传递要生成的尺寸，可以生成多种尺寸
    """
    base, ext = os.path.splitext(path)
    try:
        im = Image.open(path)
    except IOError:
        print ' in  IOError'
        return
    mode = im.mode
    if mode not in ('L', 'RGB'):
        if mode == 'RGBA':
            # 透明图片需要加白色底
            im.load()
            alpha = im.split()[3]
            bgmask = alpha.point(lambda x: 255 - x)
            im = im.convert('RGB')
            # paste(color, box, mask)
            im.paste((255, 255, 255), None, bgmask)
        else:
            im = im.convert('RGB')

    filename = base + "_160.jpg"
    im.thumbnail((160, 160), Image.ANTIALIAS)
    im.save(filename, quality=100)  # 默认 JPEG 保存质量是 75, 不太清楚。可选值(0~100)


def make_thumb_crop(path, x, y, w, h):
    # 裁剪缩略图
    base = os.path.splitext(path)[0][:-4]
    im = Image.open(path)
    filename = base + "_48.jpg"
    x2 = int(round(float(x)))
    y2 = int(round(float(y)))
    w2 = int(round(float(w)))
    h2 = int(round(float(h)))

    box = (x2, y2, x2 + w2, y2 + h2)
    region = im.crop(box)
    thumb = region.resize((48, 48), Image.ANTIALIAS)
    thumb.save(filename, quality=100)  # 默认 JPEG 保存质量是 75, 不太清楚。可选值(0~100)


def make_node_thumb(path):
    # 生成node 75x75 缩略图
    base, ext = os.path.splitext(path)
    try:
        im = Image.open(path)
    except IOError:
        print ' in  IOError'
        return

    mode = im.mode
    if mode not in ('L', 'RGB'):
        if mode == 'RGBA':
            # 透明图片需要加白色底
            im.load()
            alpha = im.split()[3]
            bgmask = alpha.point(lambda x: 255 - x)
            im = im.convert('RGB')
            # paste(color, box, mask)
            im.paste((255, 255, 255), None, bgmask)
        else:
            im = im.convert('RGB')

    width, height = im.size
    # 裁剪图片成正方形
    if width > height:
        delta = (width - height) / 2
        box = (delta, 0, width - delta, height)
        region = im.crop(box)
    elif height > width:
        delta = (height - width) / 2
        box = (0, delta, width, height - delta)
        region = im.crop(box)
    else:
        region = im

    filename = base + "_75.jpg"

    thumb = region.resize((75, 75), Image.ANTIALIAS)
    thumb.save(filename, quality=100)  # 默认 JPEG 保存质量是 75, 不太清楚。可选值(0~100)


def make_post_thumb(path, sizes=[(1200, 550), (750, 230), (365, 230)]):
    """
    生成post 1200x550 / 750x230 / 365x230 缩略图
    sizes 参数传递要生成的尺寸，可以生成多种尺寸
    """
    base, ext = os.path.splitext(path)
    try:
        im = Image.open(path)
    except IOError:
        print ' in  IOError'
        return
    mode = im.mode
    if mode not in ('L', 'RGB'):
        if mode == 'RGBA':
            # 透明图片需要加白色底
            im.load()
            alpha = im.split()[3]
            bgmask = alpha.point(lambda x: 255 - x)
            im = im.convert('RGB')
            # paste(color, box, mask)
            im.paste((255, 255, 255), None, bgmask)
        else:
            im = im.convert('RGB')

    width, height = im.size

    for size in sizes:
        filename = base + "_" + str(size[0]) + ".jpg"
        if float(width) / float(height) == float(str(size[0])) / float(str(size[1])):
            newimg = im.resize((int(size[0]), int(size[1])), Image.ANTIALIAS)
            box = (0, 0, int(size[0]), int(size[1]))
            region = newimg.crop(box)
            region.save(filename, quality=100)
        if float(width) / float(height) < float(size[0]) / float(size[1]):
            # 如果是高图，先把原图重设到size宽
            newimg = im.resize((int(size[0]), int(float(
                height) / (float(width) / float(size[0])))), Image.ANTIALIAS)
            newimg_width, newimg_height = newimg.size
            delta = (newimg_height - int(size[1])) / 2
            box = (0, delta, int(size[0]), delta + int(size[1]))
            region = newimg.crop(box)
            region.save(filename, quality=100)
        if float(width) / float(height) > float(size[0]) / float(size[1]):
            # 如果是宽图，先把原图重设到size高
            newimg = im.resize((int(float(width) / (float(
                height) / float(size[1]))), int(size[1])), Image.ANTIALIAS)
            newimg_width, newimg_height = newimg.size
            delta = (newimg_width - int(size[0])) / 2
            box = (delta, 0, delta + int(size[0]), int(size[1]))
            region = newimg.crop(box)
            region.save(filename, quality=100)
