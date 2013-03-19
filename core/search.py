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
from feed import Mosaic

objs = json.load(open('objects.json','r'))

class Search(Mosaic):
    def __init__(self): pass
    def explore(self,request):
        try: query = request.GET['explore']
        except KeyError,e: query = ''
        # TODO: Separar filtragem e busca para um segundo momento
        #filters = request.GET['filters']
        #filtr = filters.split(',')[:-1]
        mixed = []
        for o in objs['objects'].values():
            #filter_index = normalize('NFKD', f.decode('utf-8')).encode('ASCII','ignore')
            queryset = globals()[o].objects.all()
            filter(lambda obj: query.lower() in obj.name.lower(),queryset)  
            if 'Movement' in o: self.group_movement(queryset,mixed)
            else: mixed.extend(queryset)
        #shuffle(mixed)
        return self.view_mosaic(request,mixed)
        
class Follows(Mosaic):
    def __init__(self): pass
    def view_following(self,request):
        u = self.current_user(request); rels = []
        for f in Followed.objects.filter(follower=u.id):
            rels.append(Profile.objects.filter(id=f.followed)[0])
        return self.view_mosaic(request,rels)
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
