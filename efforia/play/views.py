import urllib,urllib2
from handlers import append_path
from stream import StreamService
append_path()
from spread.views import SocialHandler


class PlayerHandler(SocialHandler):
    def get(self):
	if not self.authenticated(): return
	token = self.parse_request(self.request.uri)
	data = urllib.urlencode({ 'token': token })
	request = urllib2.Request(url = 'http://efforia.herokuapp.com/play',data=data)
	urllib2.urlopen(request)

class FeedHandler(SocialHandler):
    def get(self):
        if not self.authenticated(): return
        service = StreamService()
        feed = service.top_rated()
	token = 'PgYKSxQeipE'
        return self.srender('play.html',feed=feed,token=token)
    def post(self):
	token = self.parse_request(self.request.body)
        service = StreamService()
        feed = service.top_rated()
        return self.srender('play.html',feed=feed,token=token)
	
    
class UploadHandler(SocialHandler):
    def get(self):
        if not self.authenticated(): return
        service = StreamService()
        response = service.video_entry("A Test","This is a test.")
        post_url = response[0]
        youtube_token = response[1]
        return self.srender('expose.html',post_url=post_url,youtube_token=youtube_token)
