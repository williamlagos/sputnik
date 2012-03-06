from handlers import append_path
from stream import StreamService
append_path()
from core import models
from spread.social import SocialHandler

class FeedHandler(SocialHandler):
    def get(self):
        if not self.authenticated(): return
        service = StreamService()
        feed = service.top_rated()
        return self.srender('play.html',feed=feed)
    
class UploadHandler(SocialHandler):
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
