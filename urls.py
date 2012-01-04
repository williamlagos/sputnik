from django.conf.urls.defaults import *

urlpatterns = patterns('',
    ('^$',          'spread.social.profile'),
    ('^register/$', 'spread.register.newuser'),
    ('^login/$',    'django.contrib.auth.views.login'),
    ('^logout/$',   'django.contrib.auth.views.logout'),
    ('^spread/$',   'spread.social.spread'),
    ('^spreads/$',  'spread.social.spreads'),
    ('^search/$',   'spread.social.search'),
    ('^people/$',   'spread.social.people'),
    ('^know/$',     'spread.social.know'),
    ('^play/$',     'play.video.playvideo'),
)