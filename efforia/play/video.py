from base import BaseHandler
import os,sys,stream
sys.path.append(os.path.abspath(".."))
from spread import models,social

class PlayerHandler(social.SocialHandler):
    def get(self):
        if not self.authenticated(): return
        user = self.current_user()
        known = self.current_relations()
        feed = stream.top_rated()
        favorites = self.favorites()
        return self.render(self.templates()+'play.html',user=user,known=known,feed=feed,favorites=favorites)
    
class UploadHandler(social.SocialHandler):
    def get(self):
        if not self.authenticated(): return
        #authsub_url = stream.get_authsub_url()
        user = self.current_user()
        known = self.current_relations()
        favorites = self.favorites()
        resp = stream.upload_video()
        post_url = resp[0]
        token = resp[1]
        return self.render(self.templates()+'expose.html',user=user,known=known,favorites=favorites,post_url=post_url,token=token)
