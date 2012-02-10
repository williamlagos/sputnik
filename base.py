from django.contrib.auth.models import User

import re,string,urllib
import tornado.web
import tornado.escape

class BaseHandler(tornado.web.RequestHandler):
    def templates(self):
	return '../../templates/'
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
		self.redirect('login')
		return False
	else:
		return True
	
