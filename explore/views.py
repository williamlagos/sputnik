from django.contrib.auth.models import User
from tornado.auth import FacebookGraphMixin
from coronae import append_path
from random import shuffle
append_path()

import tornado.web
import simplejson as json
from unicodedata import normalize  
from core.views import *

from core.models import Profile,Place
from play.models import Playable,Schedule
from spread.models import Spreadable,Event
from create.models import Causable,Movement

objs = json.load(open('objects.json','r'))

def search(request):
    s = Search()
    if request.method == 'GET':
        return s.explore(request)

class Search(Efforia):
    def __init__(self): pass
    def explore(self,request):
        try:
            query = request.GET['explore']
        except KeyError,e: 
            query = ''
        filters = request.GET['filters']
        filtr = filters.split(',')[:-1]
        mixed = []
        for f in filtr:
            filter_index = normalize('NFKD', f.decode('utf-8')).encode('ASCII','ignore')
            queryset = globals()[objs['objects'][filter_index]].objects.all()
            for obj in queryset:
                if query.lower() in obj.name.lower(): mixed.append(obj)  
        shuffle(mixed)
        return render(request,'grid.jade',{'f':mixed,'static_url':settings.STATIC_URL},content_type='text/html')
