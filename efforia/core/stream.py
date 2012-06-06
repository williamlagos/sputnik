import gdata.youtube
import gdata.media
from xml.dom.minidom import parseString
from social import *

class StreamService(GoogleHandler):
    def __init__(self):
#        self.yt_service = gdata.youtube.service.YouTubeService()
        self.developer_key = "AI39si7wyQ0h6KhpWLhZfJa-U4mU65rO3Dj-05grmYkZk-kn_sv8br5UdDIEORwG-itcRn5wSBTFbgu02KyR_FhSQNaR0QbvSQ"
        self.client_id = "416575314846.apps.googleusercontent.com"
#        self.yt_service.email = 'william.lagos1@gmail.com'
#        self.yt_service.password = 'mk28to#$'
#        self.yt_service.ProgrammaticLogin()
        
    def videos_by_user(self,username):
        uri = 'http://gdata.youtube.com/feeds/api/users/%s/uploads?alt=json' % username
        return self.google_request(uri)
#        return self.yt_service.GetYouTubeVideoFeed(uri)
    
    def top_rated(self):
        pass
#        return self.yt_service.GetTopRatedVideoFeed()
        
    def video_entry(self,title,description,keywords,access_token):
        media_group = gdata.media.Group(title=gdata.media.Title(text=title),
                                        description=gdata.media.Description(description_type='plain',text=description),
                                        keywords=gdata.media.Keywords(text=keywords),
                                        category=[gdata.media.Category(text='Entertainment',
                                                                       scheme='http://gdata.youtube.com/schemas/2007/categories.cat',
                                                                       label='Entertainment')],
                                        player=None,
                                        private=gdata.media.Private())
        video_entry = gdata.youtube.YouTubeVideoEntry(media=media_group) 
        url,token = self.get_upload_token(video_entry,access_token)
        return url,token
        
    def insert_video(self,video_entry,handle,content_type,boundary):
        pass
    
    def get_upload_token(self,video_entry,access_token):
        headers = {
                   'Authorization': 'OAuth %s' % access_token,
                   'X-gdata-key': 'key=%s' % self.developer_key,
                   'Content-type': 'application/atom+xml'
        }
        response = self.google_request('https://gdata.youtube.com/action/GetUploadToken',str(video_entry),headers)
        url = parseString(response.body).getElementsByTagName('url')[0].childNodes[0].data
        token = parseString(response.body).getElementsByTagName('token')[0].childNodes[0].data
        return url,token
        
    def search_video(self,search_terms):
        pass
#        gdata.youtube.service.YouTubeService()
#        query = gdata.youtube.service.YouTubeVideoQuery()
#        query.vq = search_terms
#        query.orderby = 'viewCount'
#        query.racy = 'include'
#        feed = self.yt_service.YouTubeQuery(query)
#        return feed
