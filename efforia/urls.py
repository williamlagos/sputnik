from django.conf.urls import patterns,url,include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       
    (r'^$','core.views.main'),
    (r'^config','core.views.config'),
    (r'^profile','core.views.profile'),
    (r'^photo','core.views.photo'),
    (r'^appearance','core.views.appearance'),
    (r'^options','core.views.options'),
    (r'^place','core.views.place'),
    (r'^password','core.views.password'),
    (r'^integrations','core.views.integrations'),
    (r'^enter','core.views.authenticate'),
    (r'^leave','core.views.leave'),
    (r'^delete','core.views.delete'),
    (r'^userid','core.views.ids'),
    (r'^activity','core.views.search'),
    (r'^search','core.views.search'),
    (r'^explore','core.views.search'),
    (r'^known','core.views.explore'),
    (r'^favorites','core.views.favorites'),
    (r'^fan','core.views.fan'),
    
    (r'^products','store.views.main'),
    (r'^store','store.views.init_store'),
    (r'^cart','store.views.cart'),
    (r'^cancel','store.views.cancel'),
    (r'^payment','store.views.payment'),
    (r'^discharge','store.views.discharge'),
    (r'^recharge','store.views.recharge'),
    (r'^balance','store.views.balance'),
    (r'^delivery','store.views.delivery'),
    (r'^correios','store.views.mail'),
    (r'^paypal','store.views.paypal_ipn'),
    
    (r'^spread','spread.views.main'),
    (r'^spreads','spread.views.init_spread'),
    (r'^spreaded','spread.views.spreaded'),
    (r'^spreadspread','spread.views.spreadspread'),
    (r'^spreadable','spread.views.spreadable'),
    (r'^playable','spread.views.playable'),
    (r'^images','spread.views.image'),
    (r'^image','spread.views.imageview'),
    (r'^event','spread.views.eventview'),
    (r'^pageview','spread.views.pageview'),
    (r'^pageedit','spread.views.pageedit'),
    (r'^calendar','spread.views.event'),
    (r'^contents','spread.views.content'),
    (r'^schedule','spread.views.schedule'),
    (r'^collection','spread.views.collection'),
    (r'^expose','spread.views.upload'),
    (r'^content','spread.views.collection'),
    (r'^pages','spread.views.page'),
    
    (r'^projects','create.views.main'),
    (r'^create','create.views.init_create'),
    (r'^movements','create.views.movements'),
    (r'^promote','create.views.promote'),
    (r'^project','create.views.project'),
    (r'^linkproj','create.views.link'),
    (r'^movement','create.views.movement'),
    (r'^grab','create.views.grab'),
    
    # Examples:
    # url(r'^$', 'efforia.views.home', name='home'),
    # url(r'^efforia/', include('efforia.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
urlpatterns += staticfiles_urlpatterns()
