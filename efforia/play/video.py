from base import BaseHandler

class PlayerHandler(BaseHandler):
    def get(self):
        return self.render(self.templates()+'play.html')
