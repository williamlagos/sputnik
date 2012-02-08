from base import BaseHandler
import os,sys
sys.path.append(os.path.abspath(".."))
from spread import models,social

class PlayerHandler(social.SocialHandler):
    def get(self):
	user = self.current_user()
	known = self.current_relations()
        return self.render(self.templates()+'play.html',user=user,known=known)
