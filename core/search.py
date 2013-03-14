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
        return render(request,'grid.jade',{'f':mixed,'static_url':settings.STATIC_URL},content_type='text/html')
        
class Favorites(Coronae):
    def __init__(self): pass
    def view_favorites(self,request):
        u = self.current_user(request); rels = []
        count = 0
        for o in ProfileFan,PlaceFan,PlayableFan:
            for r in o.objects.filter(user=u):
                if not count: rels.append(r.fan.profile) 
                else: rels.append(r.fan)
            count += 1
        return render(request,'grid.jade',{'rels':rels},content_type='text/html')
        
class Fans(Coronae):
    def __init__(self): pass
    def become_fan(self,request):
        u = self.current_user(request)
        ident,token = request.GET['text'].split(';')
        obj,rel = self.object_token(token)
        if 'Profile' not in obj: obj_fan = globals()[obj].objects.all().filter(user=u,id=ident)[0]
        else: obj_fan = globals()[obj].objects.all().filter(id=ident)[0].user
        obj_rel = globals()[rel](fan=obj_fan,user=u)
        obj_rel.save(); rels = []
        for o in globals()[rel].objects.all().filter(user=u): rels.append(o.fan)
        return response('Agora voce e fa disto.')
    def stop_fan(self,request):
        u = self.current_user(request)
        fan_id = request.POST['id']
        query = ProfileFan.objects.all().filter(user=u,fan=fan_id)
        if len(query): query[0].delete()
        feed = ProfileFan.objects.all().filter(user=u)
        return self.render_grid(feed,request)
