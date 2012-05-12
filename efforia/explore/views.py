from django.contrib.auth.models import User
from tornado.auth import FacebookGraphMixin
from handlers import append_path
from random import shuffle
append_path()

import tornado.web
import simplejson as json
from unicodedata import normalize  
from spread.views import SocialHandler

from core.models import Profile,Place,Event
from play.models import Playable,Schedule
from spread.models import Spreadable
from create.models import Causable,Movement

objs = json.load(open('objects.json','r'))

class FilterHandler(SocialHandler):
    def get(self):
        if not self.authenticated(): return
        return self.srender('filter.html')

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

class PeopleHandler(SocialHandler):
    def get(self):
        if not self.authenticated(): return
        people = User.objects.all()
        return self.srender('people.html',people=people)
    
class CalendarHandler(SocialHandler,FacebookGraphMixin):
    @tornado.web.asynchronous
    def get(self):
        token = self.current_user().profile.facebook_token
        self.facebook_request("/me/events",access_token=token,callback=self.async_callback(self._on_response))
    @tornado.web.asynchronous
    def _on_response(self,response):
        resp = response['data']
        return self.srender('calendar.html',response=resp)