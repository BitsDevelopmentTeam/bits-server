from ..pages import PageHandler

class LogHandler(PageHandler):
    def get(self):
        self.write(self.LOADER.load('log.html').generate())
