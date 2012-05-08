from django.contrib.auth.models import User
from tornado.auth import FacebookGraphMixin
from handlers import append_path
from random import shuffle
import re
append_path()

import urllib,tornado.web
from spread.views import SocialHandler

from core.models import UserProfile,Place,Event
from play.models import Playable,PlaySchedule
from spread.models import Spreadable
from create.models import Causable

filtered = {
            'causas':   Causable,
            'produtos': Playable,
            'postagens':Spreadable,
            'pessoas':  UserProfile,
            'programacoes':PlaySchedule,
            'lugares':  Place,
            'eventos':  Event
}

class FilterHandler(SocialHandler):
    def get(self):
        if not self.authenticated(): return
        return self.srender('filter.html')

class SearchHandler(SocialHandler):
    def get(self):
        if not self.authenticated(): return
        query = self.request.arguments['explore'][0]
        filters = self.request.arguments['filters'][0].split(',')[:-1]
        objects = {}; mixed = []
        for f in filters:
            objects[f] = filtered[f].objects.all()
            mixed.extend(objects[f])
        shuffle(mixed)
        return self.srender('search.html',mixed=mixed)
#    def post(self):
#        if not self.authenticated(): return
#        name = self.parse_request(self.request.body)
#        people = User.objects.all().filter(first_name=name)
#        return self.srender('people.html',people=people)

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