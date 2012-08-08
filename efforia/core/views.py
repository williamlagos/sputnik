#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

from models import *
from spread.models import *
from play.models import *
from create.models import *
from store.models import *

from forms import *
from coronae import Coronae
from social import *
from unicodedata import normalize 
from tornado.web import HTTPError
import simplejson as json
import tornado.web
import tornado.auth
from files import FileHandler
from datetime import date,datetime

objs = json.load(open('objects.json','r'))

class Blank():
    def __init__(self):
        self.name = '%%'
        self.date = date.today()

class Action():
    def __init__(self,name,vals=None):
        self.name = '*%s' % name
        self.date = date.today()
        self.vals = vals

class Efforia(Coronae):
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
        if 'txn_id' in self.request.arguments:
            credits = int(self.request.arguments['quantity'][0])
            profile = Profile.objects.all().filter(user=self.current_user())[0]
            profile.credit += credits
            profile.save()
            self.redirect('/')
        else:
            count = int(self.get_argument('number'))
            feed = self.get_user_feed()
            magic_number = 23
            if (len(feed)-71) % 70 is 0: feed = feed[count:(count+70)-len(feed)]
            else: feed = feed[count:]
            count += 70; number = -1
            while magic_number > len(feed): feed.append(Blank())
            return self.srender('grid.html',feed=feed,number=number)
    def get_user_feed(self):
        feed = []; exclude = []; people = [self.current_user()]
        fans = list(ProfileFan.objects.all().filter(user=self.current_user()))
        for f in fans: people.append(f.fan)
        for u in people:
            for o in objs['tokens'].values():
                if 'Causable' in o or 'Event' in o or 'Spreadable' in o:
                    objects,relation = o 
                    rels = globals()[relation].objects.all().filter(user=u)
                    for r in rels: 
                        exclude.append(r.spreaded_id)                            
                        exclude.append(r.spread_id)
                    for v in rels.values('name').distinct():
                        ts = rels.filter(name=v['name'],user=u)
                        if len(ts): feed.append(ts[len(ts)-1]) 
            for o in objs['objects'].values():
                types = globals()[o].objects.all()
                if 'Schedule' in o or 'Movement' in o:
                    for v in types.values('name').distinct(): 
                        ts = types.filter(name=v['name'],user=u)
                        if len(ts): feed.append(ts[0])
                elif 'Playable' in o:
                    playables = types.filter(user=u)
                    for play in playables:
                        if not play.token and not play.visual: play.delete()
                    feed.extend(types.filter(user=u)) 
                elif 'Spreadable' in o or 'Causable' in o or 'Event' in o:
                    relations = types.filter(user=u)
                    for r in relations:
                        if r.id not in exclude: feed.append(r) 
                elif 'Profile' in o or 'Place' in o: pass
                else: feed.extend(types.filter(user=u))
        feed.sort(key=lambda item:item.date,reverse=True)
        return feed
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

class Handler(FileHandler):
    pass

class IntegrationsHandler(Efforia):
    def get(self):
        self.render(self.templates()+'integrations.html')

class LoginHandler(Efforia):    
    def get(self):
        form = AuthenticationForm()
        if self.get_argument("error",None): form.fields['username'].errors = self.get_argument("error")
        form.fields["username"].label = "Nome"
        form.fields["password"].label = "Senha"
        self.render(self.templates()+"login.html", next=self.get_argument("next","/"), form=form)
    def post(self):
        username = self.get_argument("username", "")
        password = self.get_argument("password", "")
        auth = self.authenticate(username,password) # DB lookup here
        if auth is not None:
            self.set_current_user(username)
            self.redirect(self.get_argument("next", "/"))
        else:
            error_msg = u"?error=" + tornado.escape.url_escape("Login incorrect.")
            self.redirect(u"/login" + error_msg)
    def set_current_user(self, user):
        if user:
            self.set_cookie("user",tornado.escape.json_encode(user))
        else:
            self.clear_cookie("user")

class LogoutHandler(Efforia):
    def get(self):
        self.clear_cookie("user")
        self.clear_cookie("google_token")
        self.clear_cookie("twitter_token")
        self.clear_cookie("facebook_token")
        self.redirect(u"/")
       
class ConfigHandler(Efforia):
    def get(self):
        self.render(self.templates()+'configuration.html')


class PasswordHandler(Efforia):
    def get(self):
        password = PasswordForm(user=self.current_user())
        password.fields['old_password'].label = 'Senha antiga'
        password.fields['new_password1'].label = 'Nova senha'
        password.fields['new_password2'].label = 'Confirmação' 
        self.render(self.templates()+'password.html',password=password)
    def post(self):
        old = self.request.arguments['old_password'][0]
        new1 = self.request.arguments['new_password1'][0]
        new2 = self.request.arguments['new_password2'][0]
        user = self.current_user()
        if not user.check_password(old): 
            self.write('Senha incorreta.')
            return
        user.set_password(new1)
        user.save()
        self.write('Senha alterada!')
        
class DeleteHandler(Efforia):
    def get(self):
        strptime,token = self.request.arguments['text'][0].split(';')
        now,obj,rels = self.get_object_bydate(strptime,token); u = self.current_user()
        globals()[obj].objects.all().filter(user=u,date=now)[0].delete()

class ProfileHandler(Efforia):
    def get(self):
        user = self.current_user()
        profile = ProfileForm()
        profile.fields['username'].initial = user.username
        profile.fields['email'].initial = user.email
        profile.fields['first_name'].initial = user.first_name
        profile.fields['last_name'].initial = user.last_name
        birthday = user.profile.birthday
        self.render(self.templates()+'profileconfig.html',profile=profile,birthday=birthday)
    def post(self):
        key = self.request.arguments['key[]'][0]
        user = User.objects.all().filter(username=self.current_user())[0]
        value = self.request.arguments['key[]'][1]
        generated = True
        if 'username' in key: 
            user.username = value
            self.set_cookie("user",tornado.escape.json_encode(value))
        elif 'email' in key: 
            user.email = value
        elif 'first_name' in key: 
            user.first_name = value
        elif 'last_name' in key: 
            user.last_name = value
        elif 'birthday' in key: 
            strp_time = time.strptime(value,"%d/%m/%Y")
            profile = Profile.objects.all().filter(user=self.current_user())[0]
            profile.birthday = datetime.fromtimestamp(time.mktime(strp_time))
            profile.save()
            generated = False
        if generated: statechange = '#id_%s' % key
        else: statechange = '#datepicker'
        user.save()
        self.write(statechange)

class PlaceHandler(Efforia):
    def get(self):
        form = PlaceForm()
        form.fields['name'].label = 'Nome'
        form.fields['country'].label = 'País'
        form.fields['city'].label = 'Cidade'
        form.fields['street'].label = 'Logradouro'
        self.render(self.templates()+'form.html',form=form,action='place',submit='Criar novo lugar')
    def post(self):
        data = {
                'city': self.get_argument('city'),
                'street': self.get_argument('street'),
                'username': self.get_argument('name'),
                'first_name': self.get_argument('name'),
                'last_name': '',
                'country': self.get_argument('country'),
                'password': self.get_argument('password'),
                'email': self.get_argument('email'),
                'latitude': 0.0,
                'longitude': 0.0
        }
        self.create_user(data)
    def create_user(self,data):
        user = User.objects.create_user(data['username'],
                                        data['email'],
                                        data['password'])
        user.last_name = data['last_name']
        user.first_name = data['first_name']
        user.save()
        place = Place(name=data['username'],user=user,
                      street=data['street'],city=data['city'],country=data['country'],
                      latitude=data['latitude'],longitude=data['longitude'])
        place.save()
        self.login_user(data['username'],data['password'])