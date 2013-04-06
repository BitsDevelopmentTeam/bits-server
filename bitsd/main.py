def main():
    tornado.options.parse_config_file('bitsd.conf')

    webserver = tornado.web.Application([
        (r'/', HomePageHandler),
        (r'/storico', LogHandler),
    ])

    statuserver = tornado.web.Application([
        (r'/', StatusHandler)
    ])

    LOG.debug('Starting web server on port {}'.format(options.web_port))
    webserver.listen(options.web_port)
    LOG.debug('Starting websocket status server on port {}'.format(options.web_port))
    statuserver.listen(options.ws_port)

    tornado.ioloop.IOLoop.instance().start()
