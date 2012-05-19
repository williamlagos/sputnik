#!/usr/bin/python
# -*- coding: utf-8 -*-

import simplejson as json
from datetime import datetime
from handlers import BaseHandler,append_path
from stream import StreamService
append_path()

import tornado.web
from forms import SpreadForm,EventForm
from models import Spreadable,Relation,Event
from tornado.auth import FacebookGraphMixin

from core.models import Profile,Place
from play.models import Playable,Schedule
from create.models import Causable,Movement

objs = json.load(open('objects.json','r'))

class SocialHandler(BaseHandler):
    def get(self):
        if not self.authenticated(): return
        feed = []
        for o in objs['objects'].values(): 
            feed.extend(globals()[o].objects.all().filter(user=self.current_user()))
        feed.sort(key=lambda item:item.date,reverse=True)
        return self.srender('efforia.html',feed=feed,locale=objs['locale_date'])
    def twitter_credentials(self):
        credentials = {}
        user = self.current_user()
        credentials['user_id'] = user.username
        credentials['screen_name'] = user.email[1:]
        credentials['secret'] = user.profile.twitter_token.split(';')[0]
        credentials['key'] = user.profile.twitter_token.split(';')[1]
        return credentials
    def srender(self,place,**kwargs):
        user = self.current_user()
        kwargs['user'] = user
        today = datetime.today()
        birth = user.profile.birthday
        years = today.year-birth.year
        if today.month >= birth.month: pass
        elif today.month is birth.month and today.day >= birth.day: pass 
        else: years -= 1
        kwargs['birthday'] = years
        self.render(self.templates()+place,**kwargs)
    def accumulate_points(self,points):
        current_profile = Profile.objects.all().filter(user=self.current_user)[0]
        current_profile.points += points
        current_profile.save()

class FavoritesHandler(SocialHandler):
    def get(self):
        self.srender('favorites.html',
                     known=self.current_relations(),
                     favorites=self.favorites())
    def favorites(self):
        service = StreamService()
        return service.videos_by_user("AdeleVEVO")
    def current_relations(self):
        if not self.authenticated(): return
        user = self.current_user()
        relations = Relation.objects.filter(user=user)    
        rels = []
        for r in relations: rels.append(r.known)
        return rels

class SpreadHandler(SocialHandler,FacebookGraphMixin):
    def post(self):
        if not self.authenticated(): return
        spread = self.spread()
        spread.save()
        return self.redirect('spreads')
    def get(self):
        if not self.authenticated(): return
        form = SpreadForm()
        self.srender("spread.html",form=form)
    def spread(self):
        text = u'%s' % self.get_argument('content')
        #self.facebook_request("/me/feed",post_args={"message": text},
        #                      access_token=self.current_user().profile.facebook_token,
        #                      callback=self.async_callback(self._on_post))
        user = self.current_user()
        post = Spreadable(user=user,content=text,name='!'+user.username)
        return post
    def _on_post(self):
        self.finish()

class PostHandler(SocialHandler):
    def get(self):
        if not self.authenticated(): return
        user = self.current_user()
        spreads = Spreadable.objects.all().filter(user=user); feed = []
        for s in spreads: feed.append(s)
        feed.sort(key=lambda item:item.date,reverse=True)
        return self.srender('spreads.html',spreads=feed,locale=objs['locale_date'])

class KnownHandler(SocialHandler):
    def get(self):
        if not self.authenticated(): return
        model = Relation()
        user = self.current_user()
        model.user = user
        known = self.parse_request(self.request.uri)
        model.known = self.get_another_user(known)
        model.save()
        return self.redirect("/")

class CalendarHandler(SocialHandler,FacebookGraphMixin):
    @tornado.web.asynchronous
    def get(self):
	form = EventForm()
	form.fields['name'].label = 'Nome'
	form.fields['start_time'].label = 'Início'
	form.fields['end_time'].label = 'Fim'
	form.fields['location'].label = 'Local'
	self.srender('event.html',form=form)
    def post(self):
        token = self.current_user().profile.facebook_token
        self.facebook_request("/me/events",access_token=token,callback=self.async_callback(self._on_response))
    @tornado.web.asynchronous
    def _on_response(self,response):
        resp = response['data']
        return self.srender('calendar.html',response=resp)
