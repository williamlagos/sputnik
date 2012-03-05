from handlers import BaseHandler
from stream import StreamService
import os,sys
sys.path.append(os.path.abspath(".."))
from spread import models,social

class PlayerHandler(social.SocialHandler):
    def get(self):
        if not self.authenticated(): return
        user = self.current_user()
        known = self.current_relations()
        service = StreamService()
        feed = service.top_rated()
        favorites = self.favorites()
        return self.render_page(self.templates()+'play.html',user=user,known=known,feed=feed,favorites=favorites)
    
class UploadHandler(social.SocialHandler):
    def get(self):
        if not self.authenticated(): return
        user = self.current_user()
        known = self.current_relations()
        favorites = self.favorites()
        service = StreamService()
        response = service.video_entry("A Test","This is a test.")
        post_url = response[0]
        youtube_token = response[1]
        return self.render(self.templates()+'expose.html',favorites=favorites,known=known,user=user,
                           post_url=post_url,youtube_token=youtube_token)
