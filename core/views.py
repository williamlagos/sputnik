#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.sessions.backends.cached_db import SessionStore
from django.db.models import Sum
from django.http import HttpResponse as response
from django.conf import settings
from django.shortcuts import *

from models import *
from spread.models import *
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
from tornado import httpclient
from spread.files import Dropbox
from explorer import Search,Explore,Favorites,Fans
from datetime import date,datetime,timedelta

sys.path.append(os.path.abspath("static"))

class Blank():
    def __init__(self):
        self.token = '%%'
        self.date = date.today()

class Helix():
    def __init__(self):
        self.token = '^'
        
class Action():
    def __init__(self,name,vals=None):
        self.token = '*'
        self.action = name
        self.href = ''
        self.date = date.today()
        self.vals = vals
        
def search(request):
    s = Search()
    if request.method == 'GET':
        return s.explore(request)

def explore(request):
    e = Explore()
    if request.method == 'GET':
        return e.view_userinfo(request)

def favorites(request):
    fav = Favorites()
    if request.method == 'GET':
        return fav.view_favorites(request)

def fan(request):
    f = Fans()
    if request.method == 'GET':
        return f.become_fan(request)
    elif request.method == 'POST':
        return f.stop_fan(request)

def main(request):
    e = Efforia()
    if request.method == 'GET':
        return e.start(request)
    elif request.method == 'POST':
        return e.external(request)

def config(request):
    return render(request,'config.html',{'static_url':settings.STATIC_URL},content_type='text/html')

def integrations(request):
    return render(request,'integrations.html',{'static_url':settings.STATIC_URL},content_type='text/html')

def ids(request):
    i = ID()
    if request.method == 'GET':
        return i.view_id(request)
    elif request.method == 'POST':
        return i.finish_tutorial(request)

def delete(request):
    d = Deletes()
    if request.method == 'GET':
        return d.delete_element(request)

def profile(request):
    prof = Profiles()
    if request.method == 'GET':
        return prof.view_profile(request)
    elif request.method == 'POST':
        return prof.update_profile(request)

def place(request):
    p = Places()
    if request.method == 'GET':
        return p.register_place(request)
    elif request.method == 'POST':
        return p.create_place(request)

def password(request):
    pasw = Passwords()
    if request.method == 'GET':
        return pasw.view_password(request)
    elif request.method == 'POST':
        return pasw.change_password(request)

def authenticate(request):
    data = request.REQUEST
    if 'username' not in data or 'password' not in data:
        return response(json.dumps({'error':'User or password missing'}),
                        mimetype = 'application/json')
    username = data['username']
    password = data['password']
    exists = User.objects.filter(username=username)
    if exists:
        if exists[0].check_password(password):
            obj = json.dumps({'username':username,'userid':exists[0].id})
            request.session['user'] = username
            return response(json.dumps({'success':'Login successful'}),
                            mimetype = 'application/json')
        else:
            obj = json.dumps({'error':'User or password wrong'})
            return response(obj,mimetype='application/json')

def leave(request):
    del request.session['user']
    return response(json.dumps({'success':'Logout successful'}),mimetype='application/json')

class Efforia(Coronae):
    def __init__(self): pass
    def start(self,request):
        if 'feed' in request.GET:
            # Verifica se esta logado.
            if 'user' in request.session:
                f = self.feed(user(request.session['user']))
            else:
                f = self.feed(user('efforia'))
            number = 0
            while len(f) < 24:
                if len(f) is not 12: f.append(Blank()) 
                else: f.append(Helix())
            if len(f) > 71: 
                h = Helix()
                f = f[:71-len(f)]
                f.insert(12,h)
                f.insert(36,h)
                f.insert(60,h)
            return render(request,'grid.jade',{'f':list(f),locale:locale,
                                               'number':number,
                                               'static_url':settings.STATIC_URL},content_type='text/html')
        elif 'user' in request.session:
            return render(request,'index.jade',{
                                                'static_url':settings.STATIC_URL,
                                                'user':user(request.session['user'])
                                                },content_type='text/html')
        return render(request,'enter.jade',{'static_url':settings.STATIC_URL},content_type='text/html')
    def external(self,request):
        u = self.current_user(request)
        if 'txn_id' in request.POST:
            credits = int(request.POST['quantity'])
            profile = Profile.objects.all().filter(user=u)[0]
            profile.credit += credits
            profile.save()
            return self.redirect('/')
        else:
            count = int(request.POST['number'])
            feed = self.feed(u)
            magic_number = 23
            if (len(feed)-71) % 70 is 0: feed = feed[count:(count+70)-len(feed)]
            else: feed = feed[count:]
            count += 70; number = -1
            while magic_number > len(feed): feed.append(Blank())
            return self.render_grid(feed,request)
    def feed(self,userobj):
        objs = json.load(open('objects.json','r'))
        feed = []; exclude = []; people = [userobj]
        fans = list(ProfileFan.objects.all().filter(user=userobj))
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
    def render_grid(self,feed,request=None):
        number = -1
        if len(feed) < 71: number = 0
        else: feed = feed[:71]
        magic_number = 24 + number
        while magic_number > len(feed): feed.append(Blank())
        if request is None: return self.srender('grid.html',feed=feed,number=number)
        else: return render(request,'grid.jade',{'f':feed,'static_url':settings.STATIC_URL},content_type='text/html')
    def render_form(self,form,action,submit):
        return self.srender('form.html',form=form,action=action,submit=submit)
    def render_simpleform(self,form,action,submit):
        return self.srender('simpleform.html',form=form,action=action,submit=submit)
    def accumulate_points(self,points,request=None):
        if request is None: u = self.current_user()
        else: u = self.current_user(request)
        current_profile = Profile.objects.all().filter(user=u)[0]
        current_profile.points += points
        current_profile.save()
    def write_error(self, status_code, **kwargs):
        import traceback
        if self.settings.get("debug") and "exc_info" in kwargs:
            exc_info = kwargs["exc_info"]
            trace_info = ''.join(["%s<br/>" % line for line in traceback.format_exception(*exc_info)])
            request_info = ''.join(["<strong>%s</strong>: %s<br/>" % (k, self.request.__dict__[k] ) for k in self.request.__dict__.keys()])
            error = exc_info[1]
            
            self.set_header('Content-Type', 'text/html')
            self.finish("""<html>
                             <title>%s</title>
                             <body>
                                <h2>Error</h2>
                                <p>%s</p>
                                <h2>Traceback</h2>
                                <p>%s</p>
                                <h2>Request Info</h2>
                                <p>%s</p>
                             </body>
                           </html>""" % (error, error, 
                                        trace_info, request_info))
        else:
            self.render(self.templates()+'500.html')

class Handler(Dropbox):
    pass

class ID(Efforia):
    def __init__(self): pass
    def view_id(self,request):
        u = self.current_user(request)
        if 'first_turn' in request.GET:
            if u.profile.first_turn: return response('yes')
            else: return response('no')
        elif 'object' in request.GET:
            o,t = request.GET['object'][0].split(';')
            now,objs,rels = self.get_object_bydate(o,t)
            obj = globals()[objs].objects.all().filter(date=now)[0]
            if hasattr(obj,'user'): return response(str(obj.user.id))
            else: return response(str(self.current_user().id))
        else: return response(str(self.current_user().id))
    def finish_tutorial(self,request):
        u = self.current_user(request)
        p = Profile.objects.all().filter(user=u)[0]
        p.first_time = False
        p.save()
        return response('Tutorial finalizado.')

class Passwords(Efforia):
    def __init__(self): pass
    def view_password(self,request):
        return render(request,'password.html',{'password':password},content_type='text/html')
    def change_password(self,request):
        user = self.current_user(request)
        old = request.POST['old_password']
        new1 = request.POST['new_password1']
        new2 = request.POST['new_password2']
        if not user.check_password(old): 
            return response('Senha incorreta.')
        user.set_password(new1)
        user.save()
        return response('Senha alterada!')
        
class Deletes(Efforia):
    def delete_element(self,request):
        miliseconds = True
        strptime,token = request.GET['text'].split(';')
        if '>' in token or '#' in token: miliseconds = False
        now,obj,rels = self.get_object_bydate(strptime,token,miliseconds); u = self.current_user()
        query = globals()[obj].objects.all().filter(user=u,date=now)
        if len(query): query[0].delete()
        return response('Elemento deletado.')

class Profiles(Efforia):
    def __init__(self): pass
    def view_profile(self,request):
        user = self.current_user(request)
        profile = ProfileForm()
        profile.fields['username'].initial = user.username
        profile.fields['email'].initial = user.email
        profile.fields['first_name'].initial = user.first_name
        profile.fields['last_name'].initial = user.last_name
        birthday = user.profile.birthday
        return render(request,'profileconfig.html',{
                                                    'static_url':settings.STATIC_URL,
                                                    'profile':user.profile
                                                    },content_type='text/html')
    def update_profile(self,request):
        user = self.current_user(request)
        key = request.POST['name']
        value = request.POST['value']
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
        return response(statechange,content_type='text/plain')

class Places(Efforia):
    def __init__(self): pass
    def register_place(self,request):
        form = PlaceForm()
        form.fields['name'].label = 'Nome'
        form.fields['country'].label = 'País'
        form.fields['city'].label = 'Cidade'
        form.fields['street'].label = 'Logradouro'
        return render(request,'simpleform.html',{
                                                 'form':form,
                                                 'action':'place',
                                                 'submit':'Criar'
                                                },content_type='text/html')
    def create_place(self,request):
        data = {
                'city': request.POST['city'],
                'street': request.POST['street'],
                'username': request.POST['name'],
                'first_name': request.POST['name'],
                'last_name': '',
                'country': request.POST['country'],
                'password': request.POST['password'],
                'email': request.POST['email'],
                'latitude': 0.0,
                'longitude': 0.0
        }
        return self.create_user(data,request)
    def create_user(self,data,request):
        # TODO: Refazer ponte de login entre registros.
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
        return response('Lugar criado com sucesso.')
        #auth = self.authenticate(data['username'],data['password'])
        #if auth is not None:
        #    self.set_cookie("user",tornado.escape.json_encode(data['username']))
        #    self.redirect("/")
        #else:
        #    error_msg = u"?error=" + tornado.escape.url_escape("Falha no login")
        #    self.redirect(u"/login" + error_msg)
        #self.login_user(data['username'],data['password'])
