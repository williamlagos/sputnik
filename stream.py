import gdata.youtube.service

yt_service = gdata.youtube.service.YouTubeService()
yt_service.developer_key = "AI39si7wyQ0h6KhpWLhZfJa-U4mU65rO3Dj-05grmYkZk-kn_sv8br5UdDIEORwG-itcRn5wSBTFbgu02KyR_FhSQNaR0QbvSQ"

def PrintEntryDetails(entry):
    print 'Video title: %s' % entry.media.title.text
    print 'Video published on: %s ' % entry.published.text
    print 'Video description: %s' % entry.media.description.text
    print 'Video category: %s' % entry.media.category[0].text
    print 'Video tags: %s' % entry.media.keywords.text
    print 'Video watch page: %s' % entry.media.player.url
    print 'Video flash player URL: %s' % entry.GetSwfUrl()
    print 'Video duration: %s' % entry.media.duration.seconds
 
    print 'Video view count: %s' % entry.statistics.view_count
 
    for thumbnail in entry.media.thumbnail:
        print 'Thumbnail url: %s' % thumbnail.url

def PrintVideoFeed(feed):
    for entry in feed.entry:
        PrintEntryDetails(entry)
    
def GetAndPrintStandardFeeds():
    PrintVideoFeed(yt_service.GetTopRatedVideoFeed())
    PrintVideoFeed(yt_service.GetMostViewedVideoFeed())
    PrintVideoFeed(yt_service.GetRecentlyFeaturedVideoFeed())
    PrintVideoFeed(yt_service.GetWatchOnMobileVideoFeed())
    PrintVideoFeed(yt_service.GetTopFavoritesVideoFeed())
    PrintVideoFeed(yt_service.GetMostRecentVideoFeed())
    PrintVideoFeed(yt_service.GetMostDiscussedVideoFeed())
    PrintVideoFeed(yt_service.GetMostLinkedVideoFeed())
    PrintVideoFeed(yt_service.GetMostRespondedVideoFeed())
    # You can also retrieve a YouTubeVideoFeed by passing in the URI
    uri = 'http://gdata.youtube.com/feeds/api/standardfeeds/JP/most_viewed'
    PrintVideoFeed(yt_service.GetYouTubeVideoFeed(uri))

def TopRated():
    return yt_service.GetTopRatedVideoFeed()
#GetAndPrintStandardFeeds()
