import tornado.web

class LogPageHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('log.html')
