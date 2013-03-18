from django.contrib.auth.models import User
from django.contrib.sessions.backends.cached_db import SessionStore
from django.conf import settings
from datetime import datetime

import re,string,urllib2,sys,os
import tornado.web
import tornado.httpserver
import tornado.ioloop
import json

def append_path(path=".."):
    sys.path.append(os.path.abspath(path))

class Coronae(tornado.web.RequestHandler):
    def paginate(self,request):
        pass
    def do_request(self,url,data=""):
        request = urllib2.Request(url=url,data=data)
        request_open = urllib2.urlopen(request)
        response = request_open.read()
        request_open.close()
        return response
    def current_user(self,request=None):
        name = self.get_current_user(request)
        user = User.objects.all().filter(username=name)
        return user[0]
    def get_login_url(self):
        return u"/login"
    def get_current_user(self,request=None):
        if request is None: key = self.get_cookie('sessionid')
        else: key = request.COOKIES['sessionid']
        s = SessionStore(key)
        session = s.load()
        if len(session): user = session['user']
        else: user = None
        #if user: name = re.split('[\s"]+',string.strip(user))[1]
        #else: name = ""
        return user
    def object_token(self,token):
        objs = json.load(open('objects.json','r'))
        objects,relations = objs['tokens'][token]
        return objects,relations
    def get_object_bydate(self,strptime,token,miliseconds=True):
        # TODO: Depreciar a busca por meio de data pela busca por indice.
        objs = json.load(open('objects.json','r'))
        form = ''
        if miliseconds: form += '.%f'
        now = datetime.strptime(strptime,'%Y-%m-%d %H:%M:%S'+form)
        objects,relations = objs['tokens'][token]
        return now,objects,relations
    def authenticate(self,username,password):
        exists = User.objects.filter(username=username)
        if exists:
            if exists[0].check_password(password): 
                return exists
        else: return None
    def authenticated(self):
        name = self.get_current_user()
        if not name: 
            #self.redirect('login')
            self.render('templates/enter.html',STATIC_URL=settings.STATIC_URL)
            return False
        else:
            return True
        
class Runtime():
    def __init__(self,handlers,social=None):
        urlhandlers = handlers
        if not social: self.application = tornado.web.Application(urlhandlers); return 
        apis = json.load(open(social,'r'))
        self.application = tornado.web.Application(urlhandlers,autoescape=None,cookie_secret=True,
        twitter_consumer_key=apis['twitter']['client_key'],twitter_consumer_secret=apis['twitter']['client_secret'],
        facebook_api_key=apis['facebook']['client_key'],facebook_secret=apis['facebook']['client_secret'])
    def run(self,port=None):
        try:
            http_server = tornado.httpserver.HTTPServer(self.application)
            if port: http_server.listen(int(port))
            else: http_server.listen(8888)
            tornado.ioloop.IOLoop.instance().start()
        except KeyboardInterrupt: sys.exit(0)
