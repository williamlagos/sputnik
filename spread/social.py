from forms import SpreadForm,FriendSearch,UserForm
from models import Spread,UserProfile,UserFriend
from django.contrib.auth.models import User
from djtornado import BaseHandler
import tornado.web


class SpreadHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self):
        form = SpreadForm(self.request.POST)
        if form.is_valid():
            form.save(self.request.user)
            return self.redirect('spreads/')
    def get(self):
        spreads = Spread.objects.all().filter(user=self.request.user)
        return self.render('spreads.html', locals())

class ProfileHandler(BaseHandler):
    def get(self):
        user = self.get_django_request().user
        #profile = UserProfile.objects.filter(user=user)
        #people = UserFriend.objects.filter(user=user)
        return self.render('../templates/home.html',user=user)  

class SearchHandler(BaseHandler): 
    def post(self):
        form = FriendSearch()
        if form.is_valid(): 
            friends = form.searchUser()
            profiles = UserProfile.objects.all()
            return self.render('people.html',locals(),form=form)

class KnownHandler(BaseHandler):
    def get(self):
        model = UserFriend()
        model.user = self.request.user
        friends = User.objects.filter(username=self.request.GET.get('u',''))
        for f in friends: model.friend = f
        model.save()
        people = UserFriend.objects.filter(user=self.request.user)
        return self.render('home.html')

class PeopleHandler(BaseHandler):
    def get(self):
        friends = User.objects.all()
        profiles = UserProfile.objects.all()
        return self.render('people.html',locals())
