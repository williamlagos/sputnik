from django.conf.urls import patterns,url,include
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from efforia.pagseguro.urls import pagseguro_urlpatterns

urlpatterns = patterns('',
    (r'^efforia/',include('efforia.urls')),
    url(r'^(?P<name>\w+)$','efforia.views.profileview'),
    url(r'^','efforia.views.main'),
)

urlpatterns += staticfiles_urlpatterns()
urlpatterns += pagseguro_urlpatterns()
