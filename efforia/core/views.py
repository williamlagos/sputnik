#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from models import *
from spread.models import *
from play.models import *
from create.models import *
from forms import RegisterForm,PasswordForm,ProfileForm
from handlers import BaseHandler
from social import *
from unicodedata import normalize 
from tornado.web import HTTPError
import simplejson as json
import tornado.web
import tornado.auth
import urllib,urllib2,ast,datetime,os,stat,mimetypes,email.utils,time
from datetime import date,datetime

objs = json.load(open('objects.json','r'))

class IntegrationsHandler(BaseHandler):
    def get(self):
        self.render(self.templates()+'integrations.html')

class FileHandler(tornado.web.StaticFileHandler,BaseHandler):
    def get(self,path,include_body=True):
        if os.path.sep != "/":
            path = path.replace("/", os.path.sep)
        abspath = os.path.abspath(os.path.join(self.root, path))
        if not (abspath + os.path.sep).startswith(self.root):
            raise HTTPError(403, "%s is not in root static directory", path)
        if os.path.isdir(abspath) and self.default_filename is not None:
            if not self.request.path.endswith("/"):
                self.redirect(self.request.path + "/")
                return
            abspath = os.path.join(abspath, self.default_filename)
        if not os.path.exists(abspath):
            self.render(self.templates()+"404.html")
            #raise HTTPError(404)
        if not os.path.isfile(abspath):
            pass
            #self.render(self.templates()+"404.html")
            #raise HTTPError(403, "%s is not a file", path)

        stat_result = os.stat(abspath)
        modified = datetime.fromtimestamp(stat_result[stat.ST_MTIME])

        self.set_header("Last-Modified", modified)
        if "v" in self.request.arguments:
            self.set_header("Expires", datetime.datetime.utcnow() + \
                                       datetime.timedelta(days=365*10))
            self.set_header("Cache-Control", "max-age=" + str(86400*365*10))
        else:
            self.set_header("Cache-Control", "public")
        mime_type, encoding = mimetypes.guess_type(abspath)
        if mime_type:
            self.set_header("Content-Type", mime_type)

        self.set_extra_headers(path)
        ims_value = self.request.headers.get("If-Modified-Since")
        if ims_value is not None:
            date_tuple = email.utils.parsedate(ims_value)
            if_since = datetime.fromtimestamp(time.mktime(date_tuple))
            if if_since >= modified:
                self.set_status(304)
                return

        if not include_body:
            return
        file = open(abspath, "rb")
        try:
            self.write(file.read())
        finally:
            file.close()

class LoginHandler(BaseHandler):    
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

class LogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie("user")
        self.clear_cookie("google_token")
        self.clear_cookie("twitter_token")
        self.clear_cookie("facebook_token")
        self.redirect(u"/")

class RegisterHandler(BaseHandler,GoogleHandler,TwitterHandler,FacebookHandler):#tornado.auth.TwitterMixin,tornado.auth.FacebookGraphMixin):
    @tornado.web.asynchronous
    def get(self):
        google_id = self.get_argument("google_id",None)
        google = self.get_argument("google_token",None)
        twitter = self.get_argument("twitter_token",None)
        facebook = self.get_argument("facebook_token",None)
        self.google_token = self.twitter_token = self.facebook_token = response = ''
        google = 'empty' if not google else google
        if 'empty' not in google:
            if len(User.objects.all().filter(username=google_id)) > 0: return
            profile = self.google_credentials(google)
            profile['google_token'] = google
            self.google_enter(profile,False)
        if google_id:
            user = User.objects.all().filter(username=google_id)
            if len(user) > 0:
                token = user[0].profile.google_token
                print token
                profile = self.google_credentials(token) 
                self.google_enter(profile)
            else:
                self.approval_prompt()
        if twitter: 
            self.twitter_token = self.twitter_credentials(twitter)
            self._on_response(response)
        elif facebook: 
            self.facebook_token = self.facebook_credentials(facebook)
            self._on_response(response)
        else:
            self._on_response(response)
    def google_enter(self,profile,exist=True):
        print profile
        if not exist:
            age = date.today()
            #age = 2012-int(dat['birthday'].split('/')[-1:][0])
            data = {
                    'username':     profile['id'],
                    'first_name':   profile['given_name'],
                    'last_name':    profile['family_name'],
                    'email':        profile['link'],
                    'google_token': profile['google_token'],
                    'password':     '3ff0r14',
                    'age':          age        
            }
            self.create_user(data,age)
        self.login_user(profile['id'],'3ff0r14')
    def _on_response(self, response):
        if response is not "":
            print str(response)
            dat = ast.literal_eval(str(response))
            if 'id_str' in dat: #Facebook/Twitter
                try: lastname = dat['name'].split()[1]
                except IndexError: lastname = ""
                age = date.today()
                data = {
                    'username':   dat['id_str'],
                    'first_name': dat['name'].split()[0],
                    'last_name':  lastname,
                    'email':      '@'+dat['screen_name'],
                    'twitter_token': self.twitter_token,
                    'password':   '3ff0r14',
                    'age':        age
                }
                if len(User.objects.filter(username=data['username'])) < 1: self.create_user(data,age)
                self.login_user(data['username'],data['password'])
        else:
            form = RegisterForm()
            return self.render(self.templates()+"register.html",form=form)
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
            birthday = datetime.datetime.fromtimestamp(time.mktime(strp_time)) 
            self.create_user(form,birthday)
        username = self.request.arguments['username'][0]
        password = self.request.arguments['password'][0]
        self.login_user(username,password)
    def create_user(self,data,birthday):
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
        profile = Profile(user=user,birthday=birthday,
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
            
class ConfigHandler(BaseHandler):
    def get(self):
        self.render(self.templates()+'configuration.html')

class ProfileHandler(BaseHandler):
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
        
class PasswordHandler(BaseHandler):
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
        #if new1 in old: 
        #    print 'Password not changed'
        #if new1 not in new2: 
        #    print 'Passwords didnt match' 
        #self.write('Senhas não correspondem.')
        user.set_password(new1)
        user.save()
        self.write('Senha alterada!')
        
class DeleteHandler(BaseHandler):
    def get(self):
        strptime,token = self.request.arguments['text'][0].split(';')
        now,obj,rels = self.get_object_bydate(strptime,token); u = self.current_user()
        globals()[obj].objects.all().filter(user=u,date=now)[0].delete()
        
class FanHandler(BaseHandler):
    def get(self):
        miliseconds = True
        strptime,token = self.request.arguments['text'][0].split(';')
        if '@' in token: miliseconds = False
        now,obj,rel = self.get_object_bydate(strptime,token,miliseconds); u = self.current_user()
        if 'Profile' not in obj: obj_fan = globals()[obj].objects.all().filter(user=u,date=now)[0]
        else: obj_fan = globals()[obj].objects.all().filter(birthday=now)[0].user
        obj_rel = globals()[rel](fan=obj_fan,user=u)
        obj_rel.save(); rels = []
        for o in globals()[rel].objects.all().filter(user=u): rels.append(o.fan)
        self.render(self.templates()+'grid.html',feed=rels,number=len(rels),locale=objs['locale_date'])