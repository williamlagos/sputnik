#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
import simplejson as json
from datetime import datetime,date
from handlers import BaseHandler,append_path
append_path()

import tornado.web,time
from forms import SpreadForm,EventForm
from models import Spreadable,Event
from tornado.auth import FacebookGraphMixin
from tornado import httpclient

from core.stream import StreamService
from core.social import TwitterHandler,FacebookHandler,GoogleHandler
from core.models import Profile,Place,ProfileFan,PlaceFan
from play.models import Playable,Schedule,PlayableFan
from create.models import Causable,Movement

objs = json.load(open('objects.json','r'))

class Blank():
    def __init__(self):
        self.name = '%%'
        self.date = date.today()

class Action():
    def __init__(self,name):
        self.name = '*%s' % name
        self.date = date.today()

class SocialHandler(BaseHandler):
    def get(self):
        if not self.authenticated(): return
        if 'feed' in self.request.arguments: 
            feed = self.get_user_feed()
            magic_number = 24; number = 0
            while magic_number > len(feed): feed.append(Blank())
            if len(feed) > 71: feed = feed[:71-len(feed)]
            return self.srender('grid.html',feed=feed,number=number)
        else:
            u = self.current_user(); rels = []
            for o in ProfileFan,PlaceFan,PlayableFan:
                for r in o.objects.filter(user=u): rels.append(r.fan)
            visual = self.current_user().profile.visual
            if visual:
                client = httpclient.HTTPClient()
                response = client.fetch(visual)
                url = '%s?dl=1' % response.effective_url
            else:
                url = 'images/spin.png'
            return self.srender('efforia.html',rels=len(rels),visual=url)
    def post(self):
        count = int(self.get_argument('number'))
        feed = self.get_user_feed()
        magic_number = 23
        if (len(feed)-71) % 70 is 0: feed = feed[count:(count+70)-len(feed)]
        else: feed = feed[count:]
        count += 70; number = -1
        while magic_number > len(feed): feed.append(Blank())
        return self.srender('grid.html',feed=feed,number=number)
    def get_user_feed(self):
        feed = []
        for o in objs['objects'].values():
            types = globals()[o].objects.all()
            if 'Schedule' in o or 'Movement' in o:
                for v in types.values('name').distinct(): 
                    ts = types.filter(name=v['name'],user=self.current_user())
                    if len(ts): feed.append(ts[0])
            elif 'Profile' in o: pass
            else: feed.extend(types.filter(user=self.current_user()))
        feed.sort(key=lambda item:item.date,reverse=True)
        return feed
    def twitter_credentials(self):
        credentials = {}
        user = self.current_user()
        credentials['user_id'] = user.username
        credentials['screen_name'] = user.email[1:]
        credentials['secret'] = user.profile.twitter_token.split(';')[0]
        credentials['key'] = user.profile.twitter_token.split(';')[1]
        return credentials
    def render_grid(self,feed):
        number = -1
        if len(feed) < 71: number = 0
        else: feed = feed[:71]
        magic_number = 24 + number
        while magic_number > len(feed): feed.append(Blank())
        return self.srender('grid.html',feed=feed,number=number)
    def render_form(self,form,action,submit):
        return self.srender('form.html',form=form,action=action,submit=submit)
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
        kwargs['locale'] = objs['locale_date']
        if 'number' not in kwargs: kwargs['number'] = 0
        self.render(self.templates()+place,**kwargs)
    def accumulate_points(self,points):
        current_profile = Profile.objects.all().filter(user=self.current_user)[0]
        current_profile.points += points
        current_profile.save()

class FavoritesHandler(SocialHandler):
    def get(self):
        if not self.authenticated(): return
        u = self.current_user(); rels = []
        count = 0
        for o in ProfileFan,PlaceFan,PlayableFan:
            for r in o.objects.filter(user=u):
                if not count: rels.append(r.fan.profile) 
                else: rels.append(r.fan)
            count += 1
        self.render_grid(rels)

class SpreadHandler(SocialHandler,TwitterHandler):
    def post(self):
        if not self.authenticated(): return
        spread = self.spread()
        spread.save()
        self.accumulate_points(1)
        user = self.current_user()
        spreads = Spreadable.objects.all().filter(user=user); feed = []
        for s in spreads: feed.append(s)
        feed.sort(key=lambda item:item.date,reverse=True)
        self.render_grid(feed)
    def get(self):
        if not self.authenticated(): return
        form = SpreadForm()
        self.srender("spread.html",form=form)
    def spread(self):
        text = u'%s' % self.get_argument('content')
        twitter = self.current_user().profile.twitter_token
        if twitter:
            access_token = self.format_token(twitter)
            self.twitter_request(
                "/statuses/update",
                post_args={"status": text},
                access_token=access_token,
                callback=self.async_callback(self._on_post))
        #self.facebook_request("/me/feed",post_args={"message": text},
        #                      access_token=self.current_user().profile.facebook_token,
        #                      callback=self.async_callback(self._on_post))
        user = self.current_user()
        post = Spreadable(user=user,content=text,name='!'+user.username)
        return post
    def _on_post(self,response):
        pass

class KnownHandler(SocialHandler):
    def get(self):
        if not self.authenticated(): return
        if 'info' in self.request.arguments:
            rels = []
            if 'user' in self.request.arguments['info'][0]: filters = self.current_user().username
            else: filters = self.request.arguments['info'][0]
            u = User.objects.all().filter(username=filters)[0]
            for o in ProfileFan,PlaceFan,PlayableFan:
                for r in o.objects.filter(user=u): rels.append(r.fan) 
            today = datetime.today()
            birth = u.profile.birthday
            years = today.year-birth.year
            if today.month >= birth.month: pass
            elif today.month is birth.month and today.day >= birth.day: pass 
            else: years -= 1
            self.render(self.templates()+'profile.html',user=u,birthday=years,rels=len(rels))
        elif 'activity' in self.request.arguments:
            feed = []
            u = User.objects.all().filter(username=self.request.arguments.values()[0][0])[0]
            for o in objs['objects'].values():
                types = globals()[o].objects.all()
                if 'Schedule' in o or 'Movement' in o:
                    for v in types.values('name').distinct(): 
                        ts = types.filter(name=v['name'],user=u)
                        if len(ts): feed.append(ts[0])
                elif 'Profile' in o: pass
                else: feed.extend(types.filter(user=u))
            feed.sort(key=lambda item:item.date,reverse=True)
            self.render_grid(feed)

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
        name = self.get_argument('name')
        local = self.get_argument('location')
        times = self.get_argument('start_time'),self.get_argument('end_time')
        dates = []
        for t in times: strp_time = time.strptime(t,'%d/%m/%Y')
        dates.append(datetime.fromtimestamp(time.mktime(strp_time)))
        event_obj = Event(name='@@'+name,user=self.current_user(),start_time=dates[0],
    		              end_time=dates[1],location=local,id_event='',rsvp_status='')
        event_obj.save()
        self.accumulate_points(1)
        events = Event.objects.all().filter(user=self.current_user())
        return self.srender('grid.html',feed=events)
        #token = self.current_user().profile.facebook_token
        #self.facebook_request("/me/events",access_token=token,callback=self.async_callback(self._on_response))
    @tornado.web.asynchronous
    def _on_response(self,response):
        resp = response['data']
        return self.srender('calendar.html',response=resp)

class ContentHandler(SocialHandler):
    def get(self):
        self.srender("contents.html")

