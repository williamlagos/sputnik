from forms import SpreadForm,FriendSearch,UserForm
from models import Spread,UserProfile,UserFriend
from django.contrib.auth.models import User
from base import BaseHandler
import tornado.web


class SpreadHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self):
        form = SpreadForm(self.request.POST)
        if form.is_valid():
            form.save(self.request.user)
            return self.redirect('spreads/')
    def get(self):
        spreads = Spread.objects.all().filter(user=self.get_current_user())
        return self.render('spreads.html', locals())

class ProfileHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
	user = User.objects.filter(username = str(self.get_current_user()))[0]
        profile = UserProfile.objects.filter(user=user)[0]
        #people = UserFriend.objects.filter(user=user[0])[0]
        return self.render('../../templates/home.html',user=user,profile=profile)#,people=people)  

class SearchHandler(BaseHandler):
    def get(self):
        form = FriendSearch()
        return self.render('../../templates/search.html',form=form)
    def post(self):
        form = FriendSearch()
        if form.is_valid(): 
            friends = form.searchUser()
            profiles = UserProfile.objects.all()
            return self.render('../../templates/people.html',form=form,friends=friends,profiles=profiles)

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
