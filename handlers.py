from django.contrib.auth.models import User
from datetime import datetime

import re,string,urllib2,sys,os
import tornado.web
import simplejson as json

def append_path(path=".."):
    sys.path.append(os.path.abspath(path))

objs = json.load(open('objects.json','r'))

class BaseHandler(tornado.web.RequestHandler):
    def templates(self):
        return '../../templates/'
    def do_request(self,url,data=""):
        request = urllib2.Request(url=url,data=data)
        request_open = urllib2.urlopen(request)
        response = request_open.read()
        request_open.close()
        return response
    def current_user(self):
        name = self.get_current_user()
        user = User.objects.all().filter(username=name)
        return user[0]
    def get_login_url(self):
        return u"/login"
    def get_current_user(self):
        user = self.get_cookie('user')
        if user: name = re.split('[\s"]+',string.strip(user))[1]
        else: name = ""
        return name
    def get_object_bydate(self,strptime,token):
        now = datetime.strptime(strptime,'%Y-%m-%d %H:%M:%S.%f')
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
            self.render('templates/enter.html')
            return False
        else:
            return True
