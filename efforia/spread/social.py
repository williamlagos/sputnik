from forms import SpreadForm,FriendSearch
from models import Spread,UserProfile,UserRelation
from django.contrib.auth.models import User
from base import BaseHandler
import tornado.web

class SocialHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
	name = self.get_current_user()
	if not name: self.redirect('login')
	else:
		user = self.current_user()
	        known = self.current_relations()
	return self.render(self.templates()+'home.html',user=user,known=known)
    def current_relations(self):
	user = self.current_user()
	relations = UserRelation.objects.filter(user=user)	
	rels = []
	for r in relations: rels.append(r.known)
	return rels

class SpreadHandler(SocialHandler):
    @tornado.web.authenticated
    def post(self):
	spread = self.spread()
	spread.save()
        return self.redirect('spreads')
    def get(self):
	form = SpreadForm()
	self.render(self.templates()+"spread.html",
	 	    form=form,user=self.current_user(),
		    known=self.current_relations())
    def spread(self):
	text = self.parse_request(self.request.body)
	post = Spread(user=self.current_user(),content=text)
	return post

class PostHandler(SocialHandler):
    @tornado.web.authenticated
    def get(self):
	user = self.current_user()
        spreads = Spread.objects.all().filter(user=user)
        return self.render(self.templates()+'spreads.html',
			   spreads=spreads,user=user,
			   known=self.current_relations())


class SearchHandler(BaseHandler):
    def get(self):
        form = FriendSearch()
	user = self.current_user()
        return self.render(self.templates()+'search.html',form=form,user=user)
    def post(self):
	user = self.current_user()
	name = self.parse_request(self.request.body)
	friends = User.objects.all().filter(first_name=name)
        profiles = UserProfile.objects.all()
        return self.render(self.templates()+'people.html',user=user,friends=friends,profiles=profiles)

class KnownHandler(SocialHandler):
    def get(self):
        model = UserRelation()
	user = self.current_user()
        model.user = user
        known = self.parse_request(self.request.uri)
	model.known = self.get_another_user(known)
        model.save()
        return self.render(self.templates()+'home.html',user=user,
			   known=self.current_relations())

class PeopleHandler(SocialHandler):
    def get(self):
        people = User.objects.all()
        return self.render(self.templates()+'people.html',
			   user=self.current_user(),people=people,
			   known=self.current_relations())
