from django.contrib.auth.models import User
from tornado.auth import FacebookGraphMixin
from coronae import Coronae,append_path
from random import shuffle
append_path()

import tornado.web
import json
from unicodedata import normalize  
from views import *
from models import Profile,Place

from spread.models import Spreadable,Event,Playable,Schedule
from create.models import Causable,Movement

objs = json.load(open('objects.json','r'))

class Search(Coronae):
    def __init__(self): pass
    def explore(self,request):
        u = self.current_user(request)
        try:
            query = request.GET['explore']
        except KeyError,e: 
            query = ''
        # TODO: Separar filtragem e busca para um segundo momento
        #filters = request.GET['filters']
        #filtr = filters.split(',')[:-1]
        mixed = []
        for o in objs['objects'].values():
            #filter_index = normalize('NFKD', f.decode('utf-8')).encode('ASCII','ignore')
            queryset = globals()[o].objects.all()
            for obj in queryset:
                if query.lower() in obj.name.lower(): mixed.append(obj)  
        shuffle(mixed)
        return render(request,'grid.jade',{'f':mixed,'p':u.profile,'static_url':settings.STATIC_URL},content_type='text/html')
        
class Follows(Coronae):
    def __init__(self): pass
    def view_following(self,request):
        u = self.current_user(request); rels = []
        for f in Followed.objects.filter(follower=u):
            rels.append(Profile.objects.filter(id=f.followed)[0])
        return render(request,'grid.jade',{'rels':rels,'p':u.profile,'static_url':settings.STATIC_URL},content_type='text/html')
    def become_follower(self,request):
        u = self.current_user(request).id
        followed = Profile.objects.filter(id=request.GET['profile_id'])[0].user_id
        follow = Followed(followed=followed,follower=u)
        follow.save()
        return response('Profile followed successfully')
    def leave_follower(self,request):
        u = self.current_user(request).id
        followed = request.GET['profile_id']
        query = Followed.objects.filter(followed=followed,follower=u)
        if len(query): query[0].delete()
        return response('Profile unfollowed successfully')
