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

from pure_pagination.paginator import Paginator,PageNotAnInteger,EmptyPage
from unicodedata import normalize
from difflib import SequenceMatcher
from datetime import date,datetime,timedelta
import json
 
from tornado.web import HTTPError
from spread.files import Dropbox
from search import Search,Follows
from feed import Mosaic

sys.path.append(os.path.abspath("static"))

class Helix():
    def __init__(self):
        self.token = '^'
        
def search(request):
    s = Search()
    if request.method == 'GET':
        return s.explore(request)

def explore(request):
    p = Profiles()
    if request.method == 'GET':
        return p.view_userinfo(request)

def mosaic(request):
    m = Mosaic()
    if request.method == 'GET':
        return m.view_mosaic(request)

def deadlines(request):
    m = Mosaic()
    if request.method == 'GET':
        return m.verify_deadlines(request)

def activity(request):
    p = Profiles()
    if request.method == 'GET':
        return p.view_activity(request)

def following(request):
    fav = Follows()
    if request.method == 'GET':
        return fav.view_following(request)

def follow(request):
    f = Follows()
    if request.method == 'GET':
        return f.become_follower(request)

def unfollow(request):
    f = Follows()
    if request.method == 'GET':
        return f.leave_follower(request)

def main(request):
    e = Efforia()
    if request.method == 'GET':
        return e.start(request)
    elif request.method == 'POST':
        return e.external(request)

def config(request):
    return render(request,'configapp.jade',{'static_url':settings.STATIC_URL},content_type='text/html')

def integrations(request):
    return render(request,'integrations.jade',{'static_url':settings.STATIC_URL},content_type='text/html')

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

def photo(request):
    p = Photos()
    if request.method == 'GET':
        return p.view_photo(request)
    elif request.method == 'POST':
        return p.change_photo(request)

def appearance(request):
    c = Control()
    if request.method == 'GET':
        return c.view_control(request)
    elif request.method == 'POST':
        return c.change_control(request)

def options(request):
    c = Control()
    if request.method == 'GET':
        return c.view_options(request)

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



class Efforia(Mosaic):
    def __init__(self): pass
    def start(self,request):
        if 'page' in request.GET:
            # Proxima pagina
            return self.view_mosaic(request)
        elif 'user' in request.session:
            # Painel do usuario
            u = user(request.session['user'])
            return render(request,'index.jade',{
                                                'static_url':settings.STATIC_URL,
                                                'user':user(request.session['user']),
                                                'name':'%s %s' % (u.first_name,u.last_name)
                                                },content_type='text/html')
        # Pagina inicial
        p = list(Page.objects.filter(user=user('efforia')))
        return render(request,'enter.jade',{'static_url':settings.STATIC_URL,'pages':p},content_type='text/html')
    def external(self,request):
        u = self.current_user(request)
        credits = int(request.POST['quantity'])
        profile = Profile.objects.all().filter(user=u)[0]
        profile.credit += credits
        profile.save()
        return self.redirect('/')
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

class Control(Efforia):
    def __init__(self): pass
    def view_control(self,request):
        p = Profile.objects.filter(user=self.current_user(request))[0]
        print p.typeditor
        return render(request,'appearance.jade',{
                                                 'static_url':settings.STATIC_URL,
                                                 'interface':p.interface,
                                                 'typeditor':p.typeditor,
                                                 'language':p.language,
                                                 'monetize':p.monetize },content_type='text/html')
    def view_options(self,request):
        p = Profile.objects.filter(user=self.current_user(request))[0]
        value = 0
        for k,v in request.GET.items():
            if 'interface' in k:
                value = p.interface
            elif 'typeditor' in k:
                value = p.typeditor
            elif 'language' in k:
                value = p.language
            elif 'monetize' in k:
                value = p.monetize
        return response(value)
    def change_control(self,request):
        p = Profile.objects.filter(user=self.current_user(request))[0]
        for k,v in request.POST.items():
            if 'interface' in k:
                p.interface = int(v)
            elif 'typeditor' in k:
                p.typeditor = int(v)
            elif 'language' in k:
                p.language = int(v)
            elif 'monetize' in k:
                p.monetize = int(v)
        p.save()
        return response('Settings changed successfully')

class Photos(Efforia):
    def __init__(self): pass
    def view_photo(self,request):
        return render(request,'photo.jade',{'static_url':settings.STATIC_URL},content_type='text/html')
    def change_photo(self,request):
        p = Profile.objects.filter(user=self.current_user(request))[0]
        photo = request.FILES['Filedata'].read()
        dropbox = Dropbox()
        link = dropbox.upload_and_share(photo)
        client = httpclient.HTTPClient()
        res = client.fetch(link)
        url = '%s?dl=1' % res.effective_url
        p.visual = url
        print url
        p.save()
        return response('Photo changed successfully')
    
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
        return render(request,'password.jade',{'password':password},content_type='text/html')
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
        oid = request.GET['id']
        obj = self.object_token(request.GET['token'])[0]
        print obj
        query = globals()[obj].objects.filter(id=oid)
        if len(query): query[0].delete()
        return response('Object deleted successfully')

class Profiles(Efforia):
    def __init__(self): pass
    def view_profile(self,request):
        user = self.current_user(request)
        return render(request,'profile.jade',{
                                                'static_url':settings.STATIC_URL,
                                                'profile':user.profile,
                                                'name':user.first_name.encode('utf-8'),
                                                'sname':user.last_name.encode('utf-8'),
                                                'birth':user.profile.birthday.strftime('%d/%m/%Y')
                                                },content_type='text/html')
    def update_profile(self,request):
        user = self.current_user(request)
        for key,value in request.POST.items():
            if len(value) is 0: continue
            elif 'user' in key: 
                user.username = value
                self.set_cookie("user",tornado.escape.json_encode(value))
            elif 'email' in key: user.email = value
            elif 'name' in key: user.first_name = value
            elif 'lastn' in key: user.last_name = value
            elif 'birth' in key: 
                strp_time = time.strptime(value,"%d/%m/%Y")
                profile = self.current_user(request).profile
                profile.birthday = datetime.fromtimestamp(time.mktime(strp_time))
                profile.save()
            user.save()
        return response('Profile updated successfully')
    def view_userinfo(self,request):
        nothimself = True; followed = False
        current = self.current_user(request)
        u = Profile.objects.filter(id=request.GET['profile_id'])[0].user
        f = Followed.objects.filter(followed=u.id,follower=current.id)
        if u.id == current.id: nothimself = False
        if len(f) > 0: followed = True
        return render(request,'profileview.jade',{'profile':u.profile,
                                                  'nothimself':nothimself,
                                                  'followed':followed},content_type='text/html')
    def view_activity(self,request):
        u = Profile.objects.filter(id=request.GET['profile_id'])[0].user
        profile_objects = self.feed(u)
        return render(request,'grid.jade',{'f':profile_objects,'p':u.profile,
                                           'static_url':settings.STATIC_URL},content_type='text/html')

class Places(Efforia):
    def __init__(self): pass
    def register_place(self,request):
        u = self.current_user(request)
        exists = len(Place.objects.filter(user=u))
        return render(request,'place.jade',{'exists':exists,'user':u},content_type='text/html')
    def create_place(self,request):
        u = self.current_user(request)
        country = city = code = ''
        for k,v in request.POST.items():
            if 'country' in k: country = v
            elif 'city' in k: city = v
            elif 'code' in k: code = v.replace('-','').replace(' ','')
        place = Place.objects.filter(user=u)
        if len(place): 
            p = place[0]
            p.country = country
            p.city = city
            p.code = code
            p.save()
        else:
            p = Place(user=u,country=country,city=city,code=code)
            p.save() 
        return response('Place created/updated sucessfully')