from forms import SpreadForm,FriendSearch
from models import Spreadable,UserProfile,UserRelation
from django.contrib.auth.models import User
from base import BaseHandler
import tornado.web

class SocialHandler(BaseHandler):
    def get(self):
	if not self.authenticated(): return
	user = self.current_user()
	known = self.current_relations()
	return self.render(self.templates()+'home.html',user=user,known=known)
    def current_relations(self):
	if not self.authenticated(): return
	user = self.current_user()
	relations = UserRelation.objects.filter(user=user)	
	rels = []
	for r in relations: rels.append(r.known)
	return rels

class SpreadHandler(SocialHandler):
    def post(self):
	if not self.authenticated(): return
	spread = self.spread()
	spread.save()
        return self.redirect('spreads')
    def get(self):
	if not self.authenticated(): return
	form = SpreadForm()
	self.render(self.templates()+"spread.html",
	 	    form=form,user=self.current_user(),
		    known=self.current_relations())
    def spread(self):
	text = self.parse_request(self.request.body)
	post = Spreadable(user=self.current_user(),content=text)
	return post

class PostHandler(SocialHandler):
    def get(self):
	if not self.authenticated(): return
	user = self.current_user()
        spreads = Spreadable.objects.all().filter(user=user)
        return self.render(self.templates()+'spreads.html',
			   spreads=spreads,user=user,
			   known=self.current_relations())


class SearchHandler(SocialHandler):
    def get(self):
	if not self.authenticated(): return
        form = FriendSearch()
	user = self.current_user()
        return self.render(self.templates()+'search.html',
			   form=form,user=user,known=self.current_relations())
    def post(self):
	if not self.authenticated(): return
	user = self.current_user()
	name = self.parse_request(self.request.body)
	people = User.objects.all().filter(first_name=name)
        return self.render(self.templates()+'people.html',user=user,people=people,
			   known=self.current_relations())

class KnownHandler(SocialHandler):
    def get(self):
	if not self.authenticated(): return
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
	if not self.authenticated(): return
        people = User.objects.all()
        return self.render(self.templates()+'people.html',
			   user=self.current_user(),people=people,
			   known=self.current_relations())
