# coding=utf-8

import tornado.web


class EntryModule(tornado.web.UIModule):

    def render(self, entry):
        return self.render_string("modules/entry.html", entry=entry)


class UseradminModule(tornado.web.UIModule):

    def render(self):
        name = gravatar = domain = ''
        if self.current_user:
            name = tornado.escape.xhtml_escape(self.current_user["user_name"])
            domain = tornado.escape.xhtml_escape(
                self.current_user["user_domain"])
        return self.render_string(
            "modules/useradmin.html", name=name,
            gravatar=gravatar, domain=domain)
