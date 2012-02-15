from base import BaseHandler
import os,sys,stream
sys.path.append(os.path.abspath(".."))
from spread import models,social

class PlayerHandler(social.SocialHandler):
    def get(self):
        if not self.authenticated(): return
        user = self.current_user()
        known = self.current_relations()
        feed = stream.TopRated()
        return self.render(self.templates()+'play.html',user=user,known=known,feed=feed)
