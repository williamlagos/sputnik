from django.contrib.auth.models import User
from tornado.auth import FacebookGraphMixin
from handlers import append_path
from random import shuffle
append_path()

import tornado.web
import simplejson as json
from unicodedata import normalize  
from spread.views import SocialHandler

from core.models import Profile,Place
from play.models import Playable,Schedule
from spread.models import Spreadable,Event
from create.models import Causable,Movement

objs = json.load(open('objects.json','r'))

class SearchHandler(SocialHandler):
    def get(self):
        if not self.authenticated(): return
        query = self.request.arguments['explore'][0]
        filters = self.request.arguments['filters'][0].split(',')[:-1]
        mixed = []
        for f in filters:
            filter_index = normalize('NFKD', f.decode('utf-8')).encode('ASCII','ignore')
            queryset = globals()[objs['objects'][filter_index]].objects.all()
            for obj in queryset:
                if query.lower() in obj.name.lower(): mixed.append(obj)  
        shuffle(mixed)
        return self.srender('search.html',mixed=mixed,locale=objs['locale_date'])
