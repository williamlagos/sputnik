from django.conf.urls.defaults import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = patterns('',
		      (r'^discharge','store.views.discharge'),
		      (r'^recharge','store.views.recharge'),
		      (r'^balance','store.views.balance'),
		      (r'^enter','core.views.authenticate'),
		      (r'^verify','core.views.verify_login'))
urlpatterns += staticfiles_urlpatterns()
