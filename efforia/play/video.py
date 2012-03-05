from handlers import BaseHandler
from stream import StreamService
import os,sys,urllib,urllib2
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
        return self.render(self.templates()+'play.html',user=user,known=known,feed=feed,favorites=favorites)
    
class UploadHandler(social.SocialHandler):
    def get(self):
        if not self.authenticated(): return
        user = self.current_user()
        known = self.current_relations()
        favorites = self.favorites()
        access_token = self.get_cookie("token")
        service = StreamService()
        #response = service.upload_video(video_entry, access_token)
        response = service.getPostURLAndToken("A Test","This is a test.")
        post_url = response[0]
        youtube_token = response[1]
#        f = open("/home/william/Develop/efforia/static/teste.mp4", "rb")
#        data = urllib.urlencode({
#            'access_token': access_token,
#            'client_id': service.client_id,
#            'developer_key': service.yt_service.developer_key,
#            'video_content_type': "video/mp4",
#            'video_filename': "/home/william/Develop/efforia/static/teste.mp4",
#            'file': f,
#            'API_XML_REQUEST': video_entry
#        })
#        
#        opener = urllib2.build_opener(MultipartPostHandler.MultipartPostHandler)
#        urllib2.install_opener(opener)
#        
#        request = urllib2.Request(url='http://gdata.youtube.com/feeds/api/users/default/uploads',data=data)
#        print request.data
#        request_open = urllib2.urlopen(request)
#    
#        response = request_open.read()
#        print response
        
        return self.render(self.templates()+'expose.html',favorites=favorites,known=known,user=user,
                           post_url=post_url,youtube_token=youtube_token)
