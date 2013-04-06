from ..pages import PageHandler

class LogPageHandler(PageHandler):
    def get(self):
        self.write(self.LOADER.load('log.html').generate())
