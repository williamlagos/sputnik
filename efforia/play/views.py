from handlers import append_path
from stream import StreamService
append_path()
from spread.views import SocialHandler

class CollectionHandler(SocialHandler):
    def get(self):
        if not self.authenticated(): return
        self.render(self.templates()+'collection.html')

class FeedHandler(SocialHandler):
    def get(self):
        if not self.authenticated(): return
        service = StreamService()
        feed = service.top_rated()
        return self.render(self.templates()+'play.html',feed=feed)
    def post(self):
        token = self.parse_request(self.request.body)
        service = StreamService()
        feed = service.top_rated()
        return self.srender('play.html',feed=feed,token=token)

    
class UploadHandler(SocialHandler):
    def get(self):
        if not self.authenticated(): return
        #post_url,youtube_token = self.get_form()
        return self.srender('expose.html')
    def get_form(self,title="Um teste",description="Este foi um teste."):
        service = StreamService()
        return service.video_entry(title,description)
