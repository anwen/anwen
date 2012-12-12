#!/usr/bin/env python
# -*- coding: utf-8 -*-
import options
import argparse
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.options
from log import logger
from options.url import handlers
from anwen.uimodules import EntryModule, UseradminModule


options.web_server.update(
    dict(ui_modules={"Entry": EntryModule, "Useradmin": UseradminModule},))
application = tornado.web.Application(handlers, **options.web_server)


def launch():
    tornado.locale.load_translations(options.web_server['locale_path'])
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(application, xheaders=True)
    http_server.listen(options.port)
    logger.info('Server started on %s' % options.port)
    tornado.ioloop.IOLoop.instance().start()


parser = argparse.ArgumentParser(description='Anwen Server')

parser.add_argument(
    '-t', '--test',
    dest='run_tests',
    action='store_const',
    const=True,
    default=False,
    help='run tests'
)

if __name__ == '__main__':
    args = parser.parse_args()
    if args.run_tests:
        import tests
        import sys
        locals()['all'] = tests.all
        sys.argv = sys.argv[:1]
        tests.main()
    else:
        launch()
