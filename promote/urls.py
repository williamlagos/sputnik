from django.conf.urls import patterns,url,include

urlpatterns = patterns('promote.views',    
    (r'^projects','main'),
    (r'^create','init_create'),
    (r'^backers','backers'),
    (r'^movements','movements'),
    (r'^promote','promote'),
    (r'^project','project'),
    (r'^linkproj','link'),
    (r'^movement','movement'),
    (r'^pledge','pledge'),
    (r'^grab','grab'),
    (r'^event','eventview'),
    (r'^calendar','event'),
)
