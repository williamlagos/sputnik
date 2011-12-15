from django.conf.urls.defaults import *

urlpatterns = patterns('',
    ('^$', 'core.views.profile'),
    ('^register/$', 'core.register.newuser'),
    ('^login/$', 'django.contrib.auth.views.login'),
    ('^logout/$', 'django.contrib.auth.views.logout'),
    ('^spread/$', 'core.social.spread'),
    ('^spreads/$', 'core.social.spreads'),
    ('^search/$', 'core.social.search'),
    ('^people/$', 'core.social.people'),
)