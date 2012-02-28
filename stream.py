import gdata.youtube.service
import gdata.media

yt_service = gdata.youtube.service.YouTubeService()
yt_service.developer_key = "AI39si7wyQ0h6KhpWLhZfJa-U4mU65rO3Dj-05grmYkZk-kn_sv8br5UdDIEORwG-itcRn5wSBTFbgu02KyR_FhSQNaR0QbvSQ"

def get_user_videos(username):
    yt_service = gdata.youtube.service.YouTubeService()
    uri = 'http://gdata.youtube.com/feeds/api/users/%s/uploads' % username
    return yt_service.GetYouTubeVideoFeed(uri)
    #print_feed(yt_service.GetYouTubeVideoFeed(uri))

def top_rated():
    return yt_service.GetTopRatedVideoFeed()
    #return yt_service.GetMostViewedVideoFeed()
    
def get_authsub_url():
    next_url = 'efforia.herokuapp.com'
    scope = 'http://gdata.youtube.com'
    secure = False
    session = True
    yt_service = gdata.youtube.service.YouTubeService()
    return yt_service.GenerateAuthSubURL(next_url, scope, secure, session)
    
def upload_video():
    my_media_group = gdata.media.Group(title=gdata.media.Title(text='My Test Movie'),
                                       description=gdata.media.Description(description_type='plain',text='My description'),
                                       keywords=gdata.media.Keywords(text='cars, funny'),
                                       category=[gdata.media.Category(text='Autos',
                                                                      scheme='http://gdata.youtube.com/schemas/2007/categories.cat',
                                                                      label='Autos')],
                                       player=None)
    video_entry = gdata.youtube.YouTubeVideoEntry(media=my_media_group)
    response = yt_service.GetFormUploadToken(video_entry)
    return response
    
def search_video(search_terms):
    yt_service = gdata.youtube.service.YouTubeService()
    query = gdata.youtube.service.YouTubeVideoQuery()
    query.vq = search_terms
    query.orderby = 'viewCount'
    query.racy = 'include'
    feed = yt_service.YouTubeQuery(query)
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