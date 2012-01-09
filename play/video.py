from djtornado import BaseHandler

class PlayerHandler(BaseHandler):
    def get(self):
        return self.render('../templates/play.html')