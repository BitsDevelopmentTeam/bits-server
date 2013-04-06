from ..pages import PageHandler

class HomePageHandler(PageHandler):
    def get(self):
        self.write(self.LOADER.load('homepage.html').generate())
