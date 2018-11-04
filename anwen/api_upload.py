# -*- coding:utf-8 -*-
from .api_base import JsonHandler
import os
import datetime
from utils.img_tools import make_post_thumb
from PIL import Image
import tornado.web


class ImageUploadHandler(JsonHandler):

    @tornado.web.authenticated
    def post(self):
        img = None
        body = None
        ext = None
        if 'uploadImg' in self.request.files:
            img = self.request.files['uploadImg'][0]
            ext = os.path.splitext(img['filename'])[1].lower()
            body = img['body']
        if img and len(body) > 20 * 1024 * 1024:
            msg = {"status": "o", "info": "上传的图片不能超过2M"}
        elif ext and ext in ['.jpg', '.jpeg', '.gif', '.png', '.bmp']:
            img_dir = 'static/upload/img'
            now = datetime.datetime.now()
            t = now.strftime('%Y%m%d_%H%M%S_%f')
            img_name = '%s%s' % (t, ext)
            img_path = '%s/%s' % (img_dir, img_name)
            with open(img_path, 'wb') as image:
                image.write(body)
            im = Image.open(img_path)
            width, height = im.size
            if width / height > 5 or height / width > 5:
                os.remove(img_path)  # 判断比例 删除图片
                msg = {"status": "s", "info": "请不要上传长宽比例过大的图片"}
            else:
                # 创建1200x550 750x230 365x230缩略图
                make_post_thumb(img_path, sizes=[
                    (1200, 550), (750, 230), (365, 230), (260, 160)
                ])
                pic_1200 = '%s_1200.jpg' % t
                # users.save_user_avatar(user_id, avatar)#入库
                msg = {"status": "y", "pic_1200": pic_1200}
        else:
            msg = '{"status": "s", "info": "目前只支持jpg/gif/png/bmp格式的图片。"}'
        self.write_json_raw(msg)

    @tornado.web.authenticated
    def delete(self):
        content = self.request.body.decode('u8')
        img_name = content.split('img_name=')[1]
        img_dir = 'static/upload/img'
        for i in os.listdir(img_dir):
            if i.startswith(img_name):
                os.remove(img_dir + '/' + i)
        self.write("s")
