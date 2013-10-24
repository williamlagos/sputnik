from django.conf.urls import patterns,url,include
from django.conf.urls.defaults import *
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from efforia.pagseguro.urls import pagseguro_urlpatterns

import xadmin
xadmin.autodiscover()
from xadmin.plugins import xversion
xversion.registe_models()

urlpatterns = patterns('',
    (r'^efforia/',include('efforia.urls')),
    url(r'^admin/',include(xadmin.site.urls)),
    url(r'^(?P<name>\w+)$','efforia.views.profileview'),
    url(r'^','efforia.views.main'),
)

urlpatterns += staticfiles_urlpatterns()
urlpatterns += pagseguro_urlpatterns()
