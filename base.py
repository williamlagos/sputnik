from django.contrib.auth.models import User

import re,string
import tornado.web
import tornado.escape

class BaseHandler(tornado.web.RequestHandler):
    def current_user(self):
	name = self.get_cookie('user')
	user = User.objects.all().filter(username=name)
	return user
    def get_login_url(self):
        return u"/login"
    def get_current_user(self):
	user = self.get_cookie('user')
	name = re.split('[\s"]+',string.strip(user))[1]
	return name
    def authenticate(self,username,password):
        exists = User.objects.filter(username=username)
        if exists: return exists
        else: return None
