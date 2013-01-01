#!/usr/bin/env python
# -*- coding: utf-8 -*-
import options
import argparse
import tornado.httpserver
import tornado.ioloop
import tornado.web
from log import logger
from options.url import handlers
from anwen.uimodules import EntryModule, UseradminModule


options.web_server.update(
    dict(ui_modules={"Entry": EntryModule, "Useradmin": UseradminModule},))
application = tornado.web.Application(handlers, **options.web_server)


def launch(port):
    tornado.locale.load_translations(options.web_server['locale_path'])
    http_server = tornado.httpserver.HTTPServer(application, xheaders=True)
    http_server.listen(port)
    logger.info('Server started on %s' % port)
    tornado.ioloop.IOLoop.instance().start()


parser = argparse.ArgumentParser(
    description='Welcome to Anwen World')

parser.add_argument(
    '-t', '--test',
    dest='run_tests',
    action='store_const',
    const=True,
    default=False,
    help='run tests'
)

parser.add_argument(
    '-p', '--port',
    dest='port',
    nargs=1,
    action='store',
    default=options.port,
    help='run on the given port'
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
        launch(args.port)
