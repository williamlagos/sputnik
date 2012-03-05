import gdata.youtube.service
import gdata.media
import sys,urllib,urllib2
try:
    from xml.etree import cElementTree as ElementTree
except ImportError:
    try:
        import cElementTree as ElementTree
    except ImportError:
        try:
            from xml.etree import ElementTree
        except ImportError:
            from elementtree import ElementTree

class StreamService(gdata.service.GDataService):
    def __init__(self):
        self.yt_service = gdata.youtube.service.YouTubeService()
        self.yt_service.developer_key = "AI39si7wyQ0h6KhpWLhZfJa-U4mU65rO3Dj-05grmYkZk-kn_sv8br5UdDIEORwG-itcRn5wSBTFbgu02KyR_FhSQNaR0QbvSQ"
        self.yt_service.client_id = "416575314846.apps.googleusercontent.com"
    def get_user_videos(self,username):
        uri = 'http://gdata.youtube.com/feeds/api/users/%s/uploads' % username
        return self.yt_service.GetYouTubeVideoFeed(uri)
        #print_feed(yt_service.GetYouTubeVideoFeed(uri))
    
    def top_rated(self):
        return self.yt_service.GetTopRatedVideoFeed()
        #return yt_service.GetMostViewedVideoFeed()
        
    def videoEntry(self):
        my_media_group = gdata.media.Group(title=gdata.media.Title(text='My Test Movie'),
                                           description=gdata.media.Description(description_type='plain',text='My description'),
                                           keywords=gdata.media.Keywords(text='cars, funny'),
                                           category=[gdata.media.Category(text='Autos',
                                                                          scheme='http://gdata.youtube.com/schemas/2007/categories.cat',
                                                                          label='Autos')],
                                           player=None,
                                           private=gdata.media.Private())
        return gdata.youtube.YouTubeVideoEntry(media=my_media_group)
   
    def getPostURLAndToken(self,title, description):
        #self.yt_service.developer_key = 'xxxxxxx'
        #self.yt_service.client_id = 'xxxxxxx'
        
        # A complete client login request
        self.yt_service.email = 'william.lagos1@gmail.com'
        self.yt_service.password = 'mk28to#$'
        #self.yt_service.source = 'xxxxxxxxxx'
        self.yt_service.ProgrammaticLogin()
    
        # create media group as usual
        my_media_group = gdata.media.Group(
          title=gdata.media.Title(text=title),
          description=gdata.media.Description(description_type='plain',
                                              text=description),
          keywords=gdata.media.Keywords(text='travel, entertainment'),
          category=[gdata.media.Category(
              text='Travel',
              scheme='http://gdata.youtube.com/schemas/2007/categories.cat',
              label='Travel')],
          player=None
        )
        
        # create video entry as usual
        video_entry = gdata.youtube.YouTubeVideoEntry(media=my_media_group)
        # upload meta data only
        response = self.yt_service.GetFormUploadToken(video_entry)
        return response
    
    def upload_video(self,video_entry,token):
        self.yt_service.email = "william.lagos1@gmail.com"
        self.yt_service.password = "mk28to#$"
        self.yt_service.ProgrammaticLogin()
        data = urllib.urlencode({
            'access_token': token,
            'client_id': self.yt_service.client_id,
            'developer_key': self.yt_service.developer_key,
            'content-type': "video/mp4",
            'content_length': 1941255,
            'API_XML_REQUEST': video_entry
        })
        request = urllib2.Request(url='http://gdata.youtube.com/action/GetUploadToken',data=data)
        request_open = urllib2.urlopen(request)
    
        response = request_open.read()
        return response
        
    def search_video(self,search_terms):
        gdata.youtube.service.YouTubeService()
        query = gdata.youtube.service.YouTubeVideoQuery()
        query.vq = search_terms
        query.orderby = 'viewCount'
        query.racy = 'include'
        feed = self.yt_service.YouTubeQuery(query)
        return feed
    
    #def print_feed(feed):
    #    for entry in feed.entry:
    #        print_feed(entry)
        
    #def print_standard_feed():
    #    print_feed(yt_service.GetTopRatedVideoFeed())
    #    print_feed(yt_service.GetMostViewedVideoFeed())
    #    print_feed(yt_service.GetRecentlyFeaturedVideoFeed())
    #    print_feed(yt_service.GetWatchOnMobileVideoFeed())
    #    print_feed(yt_service.GetTopFavoritesVideoFeed())
    #    print_feed(yt_service.GetMostRecentVideoFeed())
    #    print_feed(yt_service.GetMostDiscussedVideoFeed())
    #    print_feed(yt_service.GetMostLinkedVideoFeed())
    #    print_feed(yt_service.GetMostRespondedVideoFeed())
    #    # You can also retrieve a YouTubeVideoFeed by passing in the URI
    #    uri = 'http://gdata.youtube.com/feeds/api/standardfeeds/JP/most_viewed'
    #    print_feed(yt_service.GetYouTubeVideoFeed(uri))
    
    #def print_entry(entry):
    #    print 'Video title: %s' % entry.media.title.text
    #    print 'Video published on: %s ' % entry.published.text
    #    print 'Video description: %s' % entry.media.description.text
    #    print 'Video category: %s' % entry.media.category[0].text
    #    print 'Video tags: %s' % entry.media.keywords.text
    #    print 'Video watch page: %s' % entry.media.player.url
    #    print 'Video flash player URL: %s' % entry.GetSwfUrl()
    #    print 'Video duration: %s' % entry.media.duration.seconds
    # 
    #    print 'Video view count: %s' % entry.statistics.view_count
    # 
    #    for thumbnail in entry.media.thumbnail:
    #        print 'Thumbnail url: %s' % thumbnail.url