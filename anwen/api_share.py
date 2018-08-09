# -*- coding:utf-8 -*-
from .api_base import JsonHandler
from db import Share, User, Like, Comment, Viewpoint, Hit
import markdown2
from random import randint


class ShareHandler(JsonHandler):

    def get(self, slug):
        if slug.isdigit():
            share = Share.by_sid(slug)
        else:
            share = Share.by_slug(slug)
        if not share:
            return
        share.hitnum += 1
        if 'vote_open' not in share:
            # res = {}
            # res['vote_open'] = 0
            # res['vote_title'] = ''
            # share.update(res)
            share.update({})
        share.save()
        user = User.by_sid(share.user_id)
        share.user_name = user.user_name
        share.user_domain = user.user_domain
        tags = ''
        if share.tags:
            tags += 'tags:'
            for i in share.tags.split(' '):
                tags += '<a href="/tag/%s">%s</a>  ' % (i, i)
        share.tags = tags

        user_id = int(
            self.current_user["user_id"]) if self.current_user else None
        like = Like.find_one(
            {'share_id': share.id, 'user_id': user_id})
        share.is_liking = bool(like.likenum % 2) if like else None
        share.is_disliking = bool(like.dislikenum % 2) if like else None

        comments = []
        comment_res = Comment.find({'share_id': share.id})
        for comment in comment_res:
            user = User.by_sid(comment.user_id)
            comment.name = user.user_name
            comment.domain = user.user_domain
            comment.gravatar = get_avatar(user.user_email, 50)
            comments.append(comment)

        if user_id:
            hit = Hit.find(
                {'share_id': share.id},
                {'user_id': int(self.current_user["user_id"])},
            )
            if hit.count() == 0:
                hit = Hit
                hit['share_id'] = share.id
                hit['user_id'] = int(self.current_user["user_id"])
                hit.save()
        else:
            if not self.get_cookie(share.id):
                self.set_cookie(str(share.id), "1")

        posts = Share.find()
        suggest = []
        for post in posts:
            post.score = 100 + post.id - post.user_id + post.commentnum * 3
            post.score += post.likenum * 4 + post.hitnum * 0.01
            post.score += randint(1, 999) * 0.001
            common_tags = [i for i in post.tags.split(
                ' ') if i in share.tags.split(' ')]
            # list(set(b1) & set(b2))
            post.score += len(common_tags)
            if post.sharetype == share.sharetype:
                post.score += 1  # todo
            if self.current_user:
                is_hitted = Hit.find(
                    {'share_id': share._id},
                    {'user_id': int(self.current_user["user_id"])},
                ).count() > 0
            else:
                is_hitted = self.get_cookie(share.id)
            if is_hitted:
                post.score -= 50
            suggest.append(post)
        suggest.sort(key=lambda obj: obj.get('score'))
        suggest = suggest[:5]
        viewpoints = Viewpoint.find({'share_id': share.id})

        l_viewpoints = []
        for j in viewpoints:
            j = dict(j)
            j.pop('_id')
            l_viewpoints.append(j)
        d_share = dict(share)
        d_share.pop('_id')
        d_share['viewpoints'] = l_viewpoints
        # comment suggest
        self.res = d_share
        self.write_json()
