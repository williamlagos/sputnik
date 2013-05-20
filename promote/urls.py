from django.conf.urls import patterns,url,include

urlpatterns = patterns('promote.views',    
    (r'^$','init_create'),
    (r'^promoted','promoted'),
    (r'^projects','main'),
    (r'^backers','backers'),
    (r'^movements','movements'),
    (r'^promote','promote'),
    (r'^project','project'),
    (r'^linkproj','link'),
    (r'^movement','movement'),
    (r'^pledge','pledge'),
    (r'^grab','grab'),
    (r'^eventimage','event_image'),
    (r'^event','eventview'),
    (r'^calendar','event'),
)
