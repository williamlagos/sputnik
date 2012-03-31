#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from models import UserProfile
from forms import RegisterForm
from handlers import BaseHandler
import tornado.web
import tornado.auth
import urllib,urllib2,ast,logging
import simplejson as json

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
        self.redirect(u"/login")

class GoogleOAuth2Mixin():
    def authorize_redirect(self,client_id,redirect_uri,scope):
        oauth2_url = "https://accounts.google.com/o/oauth2/auth?"
        redirect_uri = redirect_uri; client_id = client_id; scope = scope
        oauth2_url = "%sclient_id=%s&redirect_uri=%s&scope=%s&response_type=code&access_type=offline" % (oauth2_url,client_id,redirect_uri,scope)
        self.redirect(oauth2_url)
    def get_authenticated_user(self,redirect_uri,client_id,client_secret,code):
        data = urllib.urlencode({
      		'code': 	 code,
    		'client_id': 	 client_id,
    		'client_secret': client_secret,
    		'redirect_uri':  redirect_uri,
    		'grant_type':    'authorization_code'
    	})
        return self.google_request('https://accounts.google.com/o/oauth2/token',data)
    def google_request(self,url,data):
        request = urllib2.Request(url=url,data=data)
        request_open = urllib2.urlopen(request)
        response = request_open.read()
        request_open.close()
        return response

class TwitterHandler(tornado.web.RequestHandler,
                     tornado.auth.TwitterMixin):
    @tornado.web.asynchronous
    def get(self):
        if self.get_argument("oauth_token", None):
            self.get_authenticated_user(self.async_callback(self._on_auth))
            return
        self.authenticate_redirect()

    def _on_auth(self, user):
        if not user:
            raise tornado.web.HTTPError(500, "Twitter auth failed")
        access_token = user["access_token"]
        data = urllib.urlencode({ 'twitter_token': access_token })
        self.redirect("register?%s" % data)
        self.finish()
        
class GoogleHandler(tornado.web.RequestHandler,
		    GoogleOAuth2Mixin):
    def get(self):
        if self.get_argument("code",False):
            token = self.get_authenticated_user(
				redirect_uri="http://efforia.herokuapp.com/google",
				client_id="416575314846.apps.googleusercontent.com",
				client_secret="4O7-8yKLovNcwWfN5fzA2ptD",
				code=self.get_argument("code"))
            self.redirect("register?google_token=%s" % json.loads(token)['access_token'])
        self.authorize_redirect("416575314846.apps.googleusercontent.com",
                                "http://efforia.herokuapp.com/google",
                                "https://gdata.youtube.com+https://www.googleapis.com/auth/userinfo.profile")

class FacebookHandler(tornado.web.RequestHandler,
		      tornado.auth.FacebookGraphMixin):
    @tornado.web.asynchronous
    def get(self):
        if self.get_argument("code", False):
            self.get_authenticated_user(
				redirect_uri='http://efforia.herokuapp.com/facebook',
				client_id=self.settings["facebook_api_key"],
				client_secret=self.settings["facebook_secret"],
				code=self.get_argument("code"),
				callback=self.async_callback(self._on_login))
            return
        self.authorize_redirect(redirect_uri='http://efforia.herokuapp.com/facebook',
                              		client_id=self.settings["facebook_api_key"],
		                        extra_params={"scope": "read_stream,offline_access,user_birthday"})
    def _on_login(self, user):
        self.redirect("register?facebook_token=%s" % user['access_token'])

class RegisterHandler(BaseHandler,tornado.auth.TwitterMixin,tornado.auth.FacebookGraphMixin):
    @tornado.web.asynchronous
    def get(self):
        self.google_token = ""
        self.twitter_token = ""
        self.facebook_token = ""
        if self.get_argument("twitter_token",None):
            t = ast.literal_eval(urllib.unquote_plus(str(self.get_argument("twitter_token"))))
            self.twitter_token = "%s;%s" % (t['secret'],t['key'])
            self.twitter_request("/account/verify_credentials",access_token=t,callback=self.async_callback(self._on_response))
        elif self.get_argument("google_token",None):
            token = self.get_argument("google_token")
            self.google_token = token
            url="https://www.googleapis.com/oauth2/v1/userinfo"
            request = urllib2.Request(url=url)
            request_open = urllib2.urlopen(request)
            response = request_open.read()
            request_open.close()
            self._on_response(response)
        elif self.get_argument("facebook_token",None): 
            token = self.get_argument("facebook_token")
            self.facebook_token = token
            fields = ['id','first_name','last_name','link','birthday','picture']
            self.facebook_request("/me",access_token=urllib.unquote_plus(token),callback=self.async_callback(self._on_response),fields=fields)
        else:
            self._on_response("") 
    def _on_response(self, response):
        if response is not "":
            dat = ast.literal_eval(str(response))
            if 'id_str' in dat:
                try: lastname = dat['name'].split()[1]
                except IndexError: lastname = ""
                data = {
                    'username':   dat['id_str'],
                    'first_name': dat['name'].split()[0],
                    'last_name':  lastname,
                    'email':      '@'+dat['screen_name'],
                    'password':   '3ff0r14',
                    'age':        13
                }
                form = RegisterForm(data=data)
                if len(User.objects.filter(username=data['username'])) < 1: self.create_user(form)
                self.login_user(data['username'],data['password'])
            elif 'id' in dat:
                age = 2012-int(dat['birthday'].split('/')[-1:][0])
                data = {
                        'username':   dat['id'],
                        'first_name': dat['first_name'],
                        'last_name':  dat['last_name'],
                        'email':      dat['link'],
                        'password':   '3ff0r14',
                        'age': age        
                }
                form = RegisterForm(data=data)
                if len(User.objects.filter(username=data['username'])) < 1: self.create_user(form)
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
		    'first_name':self.request.arguments['first_name'][0],
		    'age':self.request.arguments['age'][0],
		}
        form = RegisterForm(data=data)
        if User.objects.filter(username=self.request.arguments['username'][0]) < 1: self.create_user(form)
        username = self.request.arguments['username'][0]
        password = self.request.arguments['password'][0]
        self.login_user(username,password)
    def create_user(self,form):
        user = User.objects.create_user(form.data['username'],
                                        form.data['email'],
                                        form.data['password'])
        user.last_name = form.data['last_name']
        user.first_name = form.data['first_name']
        user.save()
        google = self.google_token
        twitter = self.twitter_token
        facebook = self.facebook_token
        profile = UserProfile(user=user,age=form.data['age'],twitter_token=twitter,facebook_token=facebook,google_token=google)
        profile.save()
    def login_user(self,username,password):
        auth = self.authenticate(username,password)
        if auth is not None:
            self.set_cookie("user",tornado.escape.json_encode(username))
            self.redirect(self.get_argument("next", "/"))
        else:
            error_msg = u"?error=" + tornado.escape.url_escape("Falha no login")
            self.redirect(u"/login" + error_msg)
