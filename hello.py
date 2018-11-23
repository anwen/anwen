#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import signal
import tornado.httpserver
import tornado.ioloop
import tornado.web
from log import logger
from options.url import handlers
from anwen.uimodules import EntryModule, UseradminModule
import options


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
    action='store',
    type=int,
    default=options.port,
    help='run on the given port'
)


args = parser.parse_args()

options.web_server.update(
    dict(ui_modules={"Entry": EntryModule, "Useradmin": UseradminModule},))
application = tornado.web.Application(handlers, **options.web_server)

tornado.locale.load_translations(options.web_server['locale_path'])
http_server = tornado.httpserver.HTTPServer(application, xheaders=True)

if options.use_ssl and args.port != 8888:
    http_server = tornado.httpserver.HTTPServer(
        application, ssl_options=options.ssl_options)
else:
    http_server = tornado.httpserver.HTTPServer(application)


def launch(port):
    http_server.listen(port)

    logger.info('Server started on %s' % port)
    tornado.ioloop.IOLoop.instance().start()


def sig_handler(sig):
    logger.warning('Caught signal: %s', sig)
    tornado.ioloop.IOLoop.instance().add_callback(shutdown)


def shutdown():
    import time
    logger.info('Stopping http server')
    http_server.stop()  # 不接收新的 HTTP 请求
    logger.info(
        'Will shutdown in %s seconds ...',
        options.MAX_WAIT_SECONDS_BEFORE_SHUTDOWN)
    io_loop = tornado.ioloop.IOLoop.instance()
    deadline = time.time() + options.MAX_WAIT_SECONDS_BEFORE_SHUTDOWN

    def stop_loop():
        now = time.time()
        if now < deadline and (io_loop._callbacks or io_loop._timeouts):
            io_loop.add_timeout(now + 1, stop_loop)
        else:
            io_loop.stop(
            )  # 处理完现有的 callback 和 timeout 后，可以跳出 io_loop.start() 里的循环
            logger.info('Shutdown')
    stop_loop()


if __name__ == '__main__':
    signal.signal(signal.SIGTERM, sig_handler)
    signal.signal(signal.SIGINT, sig_handler)
    if args.run_tests:
        from tests import tests
        import sys
        locals()['all'] = tests.all
        sys.argv = sys.argv[:1]
        tests.main()
    else:
        port = args.port
        launch(port)
