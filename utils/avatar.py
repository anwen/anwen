# -*- coding: utf-8-*-

import hashlib


def get_avatar(email, size=16):
    gravatar_id = hashlib.md5(email.lower()).hexdigest()
    size = str(size)
    return "http://www.gravatar.com/avatar/%s?size=%s" % (gravatar_id, size)
