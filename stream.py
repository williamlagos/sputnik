import gdata.youtube.service
import gdata.youtube
import gdata.media

class StreamService(gdata.service.GDataService):
    def __init__(self):
        self.yt_service = gdata.youtube.service.YouTubeService()
        self.yt_service.developer_key = "AI39si7wyQ0h6KhpWLhZfJa-U4mU65rO3Dj-05grmYkZk-kn_sv8br5UdDIEORwG-itcRn5wSBTFbgu02KyR_FhSQNaR0QbvSQ"
        self.yt_service.client_id = "416575314846.apps.googleusercontent.com"
        self.yt_service.email = 'william.lagos1@gmail.com'
        self.yt_service.password = 'mk28to#$'
        self.yt_service.ProgrammaticLogin()
        
    def videos_by_user(self,username):
        uri = 'http://gdata.youtube.com/feeds/api/users/%s/uploads' % username
        return self.yt_service.GetYouTubeVideoFeed(uri)
    
    def top_rated(self):
        return self.yt_service.GetTopRatedVideoFeed()
        
    def video_entry(self,title,description,keywords):
        media_group = gdata.media.Group(title=gdata.media.Title(text=title),
                                        description=gdata.media.Description(description_type='plain',text=description),
                                        keywords=gdata.media.Keywords(text=keywords),
                                        category=[gdata.media.Category(text='Entertainment',
                                                                       scheme='http://gdata.youtube.com/schemas/2007/categories.cat',
                                                                       label='Entertainment')],
                                        player=None,
                                        private=gdata.media.Private())
        response = gdata.youtube.YouTubeVideoEntry(media=media_group)
        #response = self.yt_service.GetFormUploadToken(video_entry)
        return response
        
    def insert_video(self,video_entry,handle,content_type):
        return self.yt_service.InsertVideoEntry(video_entry,handle,content_type=content_type)
        
    def search_video(self,search_terms):
        gdata.youtube.service.YouTubeService()
        query = gdata.youtube.service.YouTubeVideoQuery()
        query.vq = search_terms
        query.orderby = 'viewCount'
        query.racy = 'include'
        feed = self.yt_service.YouTubeQuery(query)
        return feed
