from forms import SpreadForm,FriendSearch,UserForm
from models import Spread,UserProfile,UserFriend
from django.contrib.auth.models import User
from base import BaseHandler
import tornado.web

class SpreadHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self):
	spread = self.spread()
	spread.save()
        return self.redirect('spreads')
    def get(self):
	form = SpreadForm()
	user = self.current_user()
	print user
	self.render(self.templates()+"spread.html",form=form,user=user)
    def spread(self):
	text = self.parse_request(self.request.body)
	post = Spread(user=self.current_user(),content=text)
	return post

class PostHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
	user = self.current_user()
        spreads = Spread.objects.all().filter(user=user)
        return self.render(self.templates()+'spreads.html',spreads=spreads,user=user)

class ProfileHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
	name = self.get_current_user()
	if not name: self.redirect('login')
	else:
		user = self.current_user()
	        profile = UserProfile.objects.filter(user=user)[0]
	        #people = UserFriend.objects.filter(user=user[0])[0]
	        return self.render(self.templates()+'home.html',user=user,profile=profile)#,people=people)  

class SearchHandler(BaseHandler):
    def get(self):
        form = FriendSearch()
        return self.render('../../templates/search.html',form=form)
    def post(self):
	user = self.current_user()
	name = self.parse_request(self.request.body)
	friends = User.objects.all().filter(first_name=name)
        profiles = UserProfile.objects.all()
        return self.render('../../templates/people.html',user=user,friends=friends,profiles=profiles)

class KnownHandler(BaseHandler):
    def get(self):
        model = UserFriend()
        model.user = self.request.user
        friends = User.objects.filter(username=self.request.GET.get('u',''))
        for f in friends: model.friend = f
        model.save()
        people = UserFriend.objects.filter(user=self.request.user)
        return self.render('../../templates/home.html',people=people)

class PeopleHandler(BaseHandler):
    def get(self):
        friends = User.objects.all()
        profiles = UserProfile.objects.all()
        return self.render('../../templates/people.html',friends=friends,profiles=profiles)
