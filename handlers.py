from django.contrib.auth.models import User

import re,string,urllib,urllib2,sys,os
import tornado.web

def append_path(path=".."):
    sys.path.append(os.path.abspath(path))

class BaseHandler(tornado.web.RequestHandler):
    def templates(self):
        return '../../templates/'
    def do_request(self,url,data=""):
        request = urllib2.Request(url=url,data=data)
        request_open = urllib2.urlopen(request)
        response = request_open.read()
        request_open.close()
        return response
    def parse_request(self,body):
        array = body.split("=")
        body_text = array[len(array)-1:][0]
        text = urllib.unquote_plus(body_text)
        return text
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
    def get_another_user(self,name):
        user = User.objects.filter(username=name)
        return user[0]
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
            self.render('templates/efforia.html')
            return False
        else:
            return True
