from django.conf.urls.defaults import *

urlpatterns = patterns('',
    ('^$', 'core.views.profile'),
    ('^register/$', 'core.views.register'),
    ('^login/$', 'django.contrib.auth.views.login'),
    ('^logout/$', 'django.contrib.auth.views.logout'),
    ('^spread/$', 'core.views.spread'),
    ('^spreads/$', 'core.views.spreader'),
)