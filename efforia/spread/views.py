#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
import simplejson as json
from datetime import datetime,date
from coronae import Coronae,append_path
append_path()

import tornado.web,time,ast
from forms import *
from models import *
from tornado.auth import FacebookGraphMixin
from tornado import httpclient

from core.stream import *
from core.social import *
from core.models import *
from core.forms import *
from core.views import *
from play.models import *
from create.models import *

objs = json.load(open('objects.json','r'))

class Register(Efforia,GoogleHandler,TwitterHandler,FacebookHandler):#tornado.auth.TwitterMixin,tornado.auth.FacebookGraphMixin):
    @tornado.web.asynchronous
    def get(self):
        google_id = self.get_argument("google_id",None)
        google = self.get_argument("google_token",None)
        twitter_id = self.get_argument("twitter_id",None)
        twitter = self.get_argument("twitter_token",None)
        facebook = self.get_argument("facebook_token",None)
        self.google_token = self.twitter_token = self.facebook_token = response = ''
        google = 'empty' if not google else google
        if 'empty' not in google:
            if self.get_current_user():
                profile = Profile.objects.all().filter(user=self.current_user())[0]
                profile.google_token = google
                profile.save()
                self.redirect('/')
            else:
                if len(User.objects.all().filter(username=google_id)) > 0: return
                profile = self.google_credentials(google)
                profile['google_token'] = google
                self.google_enter(profile,False)
        if google_id:
            user = User.objects.all().filter(username=google_id)
            if len(user) > 0:
                token = user[0].profile.google_token
                profile = self.google_credentials(token) 
                self.google_enter(profile)
            else:
                self.approval_prompt()
        if twitter:
            user = User.objects.all().filter(username=twitter_id)
            prof = ast.literal_eval(str(twitter))
            if len(user) > 0: self.twitter_enter(prof)
            elif not self.get_current_user():
                self.twitter_token = prof 
                self.twitter_credentials(twitter)
            else:
                profile = Profile.objects.all().filter(user=self.current_user())[0]
                profile.twitter_token = prof['key']+';'+prof['secret']
                profile.save()
                self.redirect('/')
        elif facebook: 
            prof = Profile.objects.all().filter(facebook_token=facebook)
            if len(prof) > 0: self.facebook_token = self.facebook_credentials(facebook)
            elif not self.get_current_user(): self.facebook_token = self.facebook_credentials(facebook)
            else:
                profile = Profile.objects.all().filter(user=self.current_user())[0]
                profile.facebook_token = facebook
                profile.save()
                self.redirect('/')
        else:
            self._on_response(response)
    def google_enter(self,profile,exist=True):
        if not exist:
            age = date.today()
            contact = profile['link'] if 'link' in profile else ''
            data = {
                    'username':     profile['id'],
                    'first_name':   profile['given_name'],
                    'last_name':    profile['family_name'],
                    'email':        contact,
                    'google_token': profile['google_token'],
                    'password':     '3ff0r14',
                    'age':          age        
            }
            self.create_user(data)
        self.login_user(profile['id'],'3ff0r14')
    def twitter_enter(self,profile,exist=True):
        if not exist:
            age = date.today()
            names = profile['name'].split()[:2]
            given_name,family_name = names if len(names) > 1 else (names[0],'')
            data = {
                    'username':     profile['user_id'],
                    'first_name':   given_name,
                    'last_name':    family_name,
                    'email':        '@'+profile['screen_name'],
                    'twitter_token': profile['key']+';'+profile['secret'],
                    'password':     '3ff0r14',
                    'age':          age        
            }
            self.create_user(data)
        self.login_user(profile['user_id'],'3ff0r14')
    def facebook_enter(self,profile,exist=True):
        if not exist:
            strp_time = time.strptime(profile['birthday'],"%m/%d/%Y")
            age = datetime.fromtimestamp(time.mktime(strp_time))
            if 'first_name' not in profile:
                names = profile['name'].split()[:2]
                profile['first_name'],profile['last_name'] = names if len(names) > 1 else (names[0],'')
            data = {
                'username':   profile['id'],
                'first_name': profile['first_name'],
                'last_name':  profile['last_name'],
                'email':      profile['link'],
                'facebook_token': self.facebook_token,
                'password':   '3ff0r14',
                'age':        age
            }
            self.create_user(data)
        self.login_user(profile['id'],'3ff0r14')
    def _on_twitter_response(self,response):
        if response is '': return
        profile = self.twitter_token
        prof = ast.literal_eval(str(response))
        profile['name'] = prof['name']
        self.twitter_enter(profile,False)
    def _on_facebook_response(self,response):
        if response is '': return
        profile = ast.literal_eval(str(response))
        user = User.objects.all().filter(username=profile['id'])
        if len(user) > 0: self.facebook_enter(profile)
        else: self.facebook_enter(profile,False)
    def _on_response(self,response):
        form = RegisterForm()
        return self.render(self.templates()+"simpleform.html",form=form,submit='Entrar',action='register')
    @tornado.web.asynchronous
    def post(self):
        data = {
            'username':self.request.arguments['username'][0],
            'email':self.request.arguments['email'][0],
            'password':self.request.arguments['password'][0],
            'last_name':self.request.arguments['last_name'][0],
            'first_name':self.request.arguments['first_name'][0]
        }
        form = RegisterForm(data=data)
        if len(User.objects.filter(username=self.request.arguments['username'][0])) < 1:
            strp_time = time.strptime(self.request.arguments['birthday'][0],"%m/%d/%Y")
            birthday = datetime.fromtimestamp(time.mktime(strp_time)) 
            form.data['age'] = birthday
            self.create_user(form.data)
        username = self.request.arguments['username'][0]
        password = self.request.arguments['password'][0]
        self.login_user(username,password)
    def create_user(self,data):
        print data
        user = User.objects.create_user(data['username'],
                                        data['email'],
                                        data['password'])
        user.last_name = data['last_name']
        user.first_name = data['first_name']
        user.save()
        google_token = twitter_token = facebook_token = ''
        if 'google_token' in data: google_token = data['google_token']
        elif 'twitter_token' in data: twitter_token = data['twitter_token']
        elif 'facebook_token' in data: facebook_token = data['facebook_token']
        profile = Profile(user=user,birthday=data['age'],
                          twitter_token=twitter_token,
                          facebook_token=facebook_token,
                          google_token=google_token)
        profile.save()
    def login_user(self,username,password):
        auth = self.authenticate(username,password)
        if auth is not None:
            self.set_cookie("user",tornado.escape.json_encode(username))
            self.redirect("/")
        else:
            error_msg = u"?error=" + tornado.escape.url_escape("Falha no login")
            self.redirect(u"/login" + error_msg)
 
class FavoritesHandler(Efforia):
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
        
class FanHandler(Efforia):
    def get(self):
        miliseconds = True
        strptime,token = self.request.arguments['text'][0].split(';')
        if '@' in token: miliseconds = False
        print strptime
        now,obj,rel = self.get_object_bydate(strptime,token,miliseconds); u = self.current_user()
        if 'Profile' not in obj: obj_fan = globals()[obj].objects.all().filter(user=u,date=now)[0]
        else: obj_fan = globals()[obj].objects.all().filter(birthday=now)[0].user
        obj_rel = globals()[rel](fan=obj_fan,user=u)
        obj_rel.save(); rels = []
        for o in globals()[rel].objects.all().filter(user=u): rels.append(o.fan)
        self.render(self.templates()+'grid.html',feed=rels,number=len(rels),locale=objs['locale_date'])

class SpreadsHandler(Efforia):
    def get(self):
        self.srender('spreads.html')

class SpreadHandler(Efforia,TwitterHandler,FacebookHandler):
    def get(self):
        if 'view' in self.request.arguments:
            strptime,token = self.get_argument('object').split(';')
            now,obj,rel = self.get_object_bydate(strptime,token)
            spreaded = globals()[rel].objects.all().filter(date=now)[0]
            feed = []; feed.append(spreaded.spreaded)
            spreads = globals()[rel].objects.all().filter(spreaded=spreaded.spreaded)
            for s in spreads: feed.append(s.spread)
            self.render_grid(feed)
        else:
            tutor = True
            if not self.authenticated(): return
            if 'spread' in self.request.arguments: tutor = False
            form = SpreadForm()
            self.srender("spread.html",form=form,tutor=tutor)
    def post(self):
        if 'spread' in self.request.arguments:
            u = self.current_user()
            c = self.request.arguments['spread'][0]
            spread = Spreadable(user=u,content=c,name='!'+u.username)
            spread.save()
            strptime,token = self.request.arguments['time'][0].split(';')
            now,objs,rels = self.get_object_bydate(strptime,token)
            o = globals()[objs].objects.all().filter(date=now)[0]
            relation = globals()[rels](spreaded=o,spread=spread,user=u)
            relation.save()
            self.write('Espalhado com sucesso!')
        else:
            if not self.authenticated(): return
            spread = self.spread()
            spread.save()
            self.accumulate_points(1)
            user = self.current_user()
            spreads = Spreadable.objects.all().filter(user=user); feed = []
            for s in spreads: feed.append(s)
            feed.sort(key=lambda item:item.date,reverse=True)
            self.render_grid(feed)
    def spread(self):
        text = u'%s' % self.get_argument('content')
        twitter = self.current_user().profile.twitter_token
        facebook = self.current_user().profile.facebook_token
        if twitter:
            access_token = self.format_token(twitter)
            self.twitter_request(
                "/statuses/update",
                post_args={"status": text},
                access_token=access_token,
                callback=self.async_callback(self._on_post))
        if facebook:
            self.facebook_request("/me/feed",post_args={"message": text},
                              access_token=facebook,
                              callback=self.async_callback(self._on_post))
        user = self.current_user()
        post = Spreadable(user=user,content=text,name='!'+user.username)
        return post
    def _on_post(self,response):
        pass

class KnownHandler(Efforia):
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
            u = User.objects.all().filter(username=self.get_argument('activity'))[0]
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

class CalendarHandler(Efforia,FacebookGraphMixin):
    @tornado.web.asynchronous
    def get(self):
        if 'view' in self.request.arguments:
            strptime,token = self.get_argument('object').split(';')
            now,obj,rel = self.get_object_bydate(strptime,token)
            spreaded = globals()[rel].objects.all().filter(date=now)[0]
            feed = []; feed.append(spreaded.spreaded)
            spreads = globals()[rel].objects.all().filter(spreaded=spreaded.spreaded)
            for s in spreads: feed.append(s.spread)
            self.render_grid(feed)
        else:
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
        for t in times: 
            strp_time = time.strptime(t,'%d/%m/%Y')
            dates.append(datetime.fromtimestamp(time.mktime(strp_time)))
        facebook = self.current_user().profile.facebook_token
        if facebook:
            args = { 'name':name, 'start_time':dates[0], 'end_time':dates[1] }
            self.facebook_request("/me/events",access_token=facebook,post_args=args,
                                  callback=self.async_callback(self._on_response))
        event_obj = Event(name='@@'+name,user=self.current_user(),start_time=dates[0],
    		              end_time=dates[1],location=local,id_event='',rsvp_status='')
        event_obj.save()
        self.accumulate_points(1)
        events = Event.objects.all().filter(user=self.current_user())
        return self.srender('grid.html',feed=events)
    @tornado.web.asynchronous
    def _on_response(self,response):
        pass

class ContentHandler(Efforia):
    def get(self):
        self.srender("contents.html")

