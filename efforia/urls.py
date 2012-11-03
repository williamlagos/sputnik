from django.conf.urls.defaults import *
from staticfiles.urls import staticfiles_urlpatterns

urlpatterns = patterns('',
		      (r'^discharge','store.views.discharge'),
		      (r'^recharge','store.views.recharge'),
		      (r'^balance','store.views.balance'))
urlpatterns += staticfiles_urlpatterns()
