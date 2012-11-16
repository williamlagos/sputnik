from django.conf.urls import patterns
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    (r'^$','core.views.main'),
    (r'^enter','core.views.authenticate'),
    (r'^verify','core.views.verify_login'),
    (r'^discharge','store.views.discharge'),
    (r'^recharge','store.views.recharge'),
    (r'^balance','store.views.balance'),
    # Examples:
    # url(r'^$', 'plethora.views.home', name='home'),
    # url(r'^plethora/', include('plethora.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
urlpatterns += staticfiles_urlpatterns()
