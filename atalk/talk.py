#!/usr/bin/env python
#
# Copyright 2009 Facebook
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import logging
import tornado.escape
import tornado.ioloop
import tornado.web
import tornado.websocket
import uuid
from tornado.escape import json_decode

from anwen.base import BaseHandler
from db import Talk


class TalkHandler(BaseHandler):

    def get(self):
        self.render("talk.html")


class MessageMixin(object):
    waiters = set()
    cache = []
    cache_size = 200

    def wait_for_messages(self, callback, cursor=None):
        cls = MessageMixin
        if cursor:
            index = 0
            for i in xrange(len(cls.cache)):
                index = len(cls.cache) - i - 1
                if cls.cache[index]["id"] == cursor:
                    break
            recent = cls.cache[index + 1:]
            if recent:
                callback(recent)
                return
        cls.waiters.add(callback)

    def cancel_wait(self, callback):
        cls = MessageMixin
        cls.waiters.remove(callback)

    def new_messages(self, messages):
        cls = MessageMixin
        logging.info("Sending new message to %r listeners", len(cls.waiters))
        for callback in cls.waiters:
            try:
                callback(messages)
            except:
                logging.error("Error in waiter callback", exc_info=True)
        cls.waiters = set()
        cls.cache.extend(messages)
        if len(cls.cache) > self.cache_size:
            cls.cache = cls.cache[-self.cache_size:]


class MsgNewHandler(BaseHandler, MessageMixin):

    def post(self):
        if self.current_user:
            user_name = self.current_user["user_name"]
            user_id = self.current_user["user_id"]
        else:
            user_name = 'guest'
            user_id = 0
        talk = {
            "id": str(uuid.uuid4()),
            "user_name": user_name,
            "user_id": user_id,
            "body": self.get_argument("body"),
        }
        talk["html"] = self.render_string("message.html", message=talk)
        if self.get_argument("next", None):
            self.redirect(self.get_argument("next"))
        else:
            self.write(talk)
        # self.new_messages([message])
        send_message(talk)


class MsgUpdatesHandler(BaseHandler, MessageMixin):

    @tornado.web.asynchronous
    def post(self):
        cursor = self.get_argument("cursor", None)
        self.wait_for_messages(self.on_new_messages,
                               cursor=cursor)

    def on_new_messages(self, messages):
        # Closed client connection
        if self.request.connection.stream.closed():
            return
        self.finish(dict(messages=messages))

    def on_connection_close(self):
        self.cancel_wait(self.on_new_messages)


class ChatSocketHandler(tornado.websocket.WebSocketHandler, BaseHandler):
    waiters = set()
    cache = []
    cache_size = 200

    def allow_draft76(self):
        # for iOS 5.0 Safari
        return True

    def open(self):
        ChatSocketHandler.waiters.add(self)

    def on_close(self):
        ChatSocketHandler.waiters.remove(self)

    def current_user(self):
        user_json = self.get_secure_cookie("user")
        if not user_json:
            return None
        return json_decode(user_json)

    def on_message(self, message):
        logging.info("got message %r", message)
        parsed = tornado.escape.json_decode(message)
        current_user = self.current_user()
        if current_user:
            user_name = current_user["user_name"]
            user_id = current_user["user_id"]
        else:
            user_name = 'guest'
            user_id = 0
        talk = {
            "id": str(uuid.uuid4()),
            "user_name": user_name,
            "user_id": user_id,
            "body": parsed["body"],
        }
        talk["html"] = self.render_string("message.html", message=talk)
        logging.info("sending message to %d waiters", len(self.waiters))
        send_message(talk)


def send_message(msg):
    talk = Talk
    doc = {
        'user_id': msg['user_id'],
        'body': msg['body'],
    }
    talk = talk.new(doc)
    for waiter in ChatSocketHandler.waiters:
        try:
            waiter.write_message(msg)
        except:
            logging.error('Error sending message', exc_info=True)

    for callback in MessageMixin.waiters:
        try:
            callback(msg)
        except:
            logging.error('Error in callback', exc_info=True)
    MessageMixin.waiters = set()
