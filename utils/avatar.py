# -*- coding: utf-8-*-


def get_avatar(email, size=16):
    import hashlib
    import os
    import requests
    # gravatar_id = hashlib.md5(email.lower()).hexdigest()
    # size = str(size)
    # return "http://www.gravatar.com/avatar/%s?size=%s" % (gravatar_id, size)

    size = str(size)
    avatar_dir = 'static/avatar'
    default_avatar_path = '/%s/default/default.gif' % (avatar_dir)
    avatar_path = '%s/%s_%s.jpg' % (avatar_dir, email, size)
    if os.path.isfile(avatar_path):
        return '/%s' % (avatar_path)
    gravatar_id = hashlib.md5(email.lower()).hexdigest()
    link = "http://www.gravatar.com/avatar/%s?size=%s&d=404" % (
        gravatar_id, size)
    try:
        r = requests.get(link)
        if r.status_code == 200:
            with open(avatar_path, 'wb') as f:
                for chunk in r.iter_content():
                    f.write(chunk)
    except Exception as e:
        print('Error:', e)
    if os.path.isfile(avatar_path):
        return '/%s' % (avatar_path)
    return default_avatar_path
