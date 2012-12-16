from django.conf.urls import patterns,url,include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^$','core.views.main'),
    (r'^config','core.views.config'),
    (r'^profile','core.views.profile'),
    (r'^integrations','core.views.integrations'),
    (r'^enter','core.views.authenticate'),
    (r'^leave','core.views.leave'),
    (r'^store','store.views.init_store'),
    (r'^products','store.views.main'),
    (r'^payment','store.views.payment'),
    (r'^discharge','store.views.discharge'),
    (r'^recharge','store.views.recharge'),
    (r'^balance','store.views.balance'),
    (r'^connect','connect.views.main'),
    (r'^spreads','spread.views.init_spread'),
    (r'^spread','spread.views.main'),
    (r'^calendar','spread.views.event'),
    (r'^contents','spread.views.content'),
    (r'^causes','create.views.main'),
    (r'^movement','create.views.movement'),
    (r'^expose','play.views.upload'),
    (r'^collection','play.views.collection'),
    (r'^content','play.views.collection'),
    (r'^accounts/', include('userena.urls')),
    # Examples:
    # url(r'^$', 'efforia.views.home', name='home'),
    # url(r'^efforia/', include('efforia.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
urlpatterns += staticfiles_urlpatterns()
