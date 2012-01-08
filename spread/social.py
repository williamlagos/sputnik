from django.contrib.auth.decorators import login_required
from django.conf import settings
from forms import SpreadForm,FriendSearch
from models import Spread,UserProfile,UserFriend
from django.contrib.auth.models import User
import django.contrib.auth.views
import tornado.web


class SpreadHandler(tornado.web.RequestHandler):
    def post(self):
        form = SpreadForm(self.request.POST)
        if form.is_valid():
            form.save(self.request.user)
            return self.redirect('spreads/')
    def get(self):
	spreads = Spread.objects.all().filter(user=self.request.user)
	return self.render('spreads.html', locals())

class ProfileHandler(tornado.web.RequestHandler):
    def get(self):
	try:
		profile = self.request.user.profile
        	people = UserFriend.objects.filter(user=self.request.user)
	    	return self.render('home.html',profile=profile,people=people)  
	except:
		#django.contrib.auth.views.login()
		return self.render("../templates/test.html",title="ABC") 
		pass

class SearchHandler(tornado.web.RequestHandler): 
    def post(self):
        form = FriendSearch(self.request.POST)
        if form.is_valid(): 
            friends = form.searchUser()
            profiles = UserProfile.objects.all()
            return self.render('people.html',locals(),form=form)

class KnownHandler(tornado.web.RequestHandler):
    def get(self):
        model = UserFriend()
        model.user = self.request.user
        friends = User.objects.filter(username=self.request.GET.get('u',''))
        for f in friends: model.friend = f
        model.save()
    	people = UserFriend.objects.filter(user=self.request.user)
    	return self.render('home.html')

class PeopleHandler(tornado.web.RequestHandler):
    def get(self):
	friends = User.objects.all()
	profiles = UserProfile.objects.all()
	return self.render('people.html',locals())
