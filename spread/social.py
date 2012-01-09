from forms import SpreadForm,FriendSearch,UserForm
from models import Spread,UserProfile,UserFriend
from django.contrib.auth.models import User
from djtornado import BaseHandler
import tornado.web
import tornado.auth


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
        try:
            profile = self.request.user.profile
            people = UserFriend.objects.filter(user=self.request.user)
            return self.render('home.html',profile=profile,people=people)  
        except:
            form = UserForm()
            return self.render("../templates/registration/login.html",title="ABC",form=form)

class SearchHandler(BaseHandler): 
    def post(self):
        form = FriendSearch()
        if form.is_valid(): 
            friends = form.searchUser()
            profiles = UserProfile.objects.all()
            return self.render('people.html',locals(),form=form)

class GoogleHandler(tornado.web.RequestHandler, tornado.auth.GoogleMixin):
    @tornado.web.asynchronous
    def get(self):
        if self.get_argument("openid.mode", None):
            self.get_authenticated_user(self.async_callback(self._on_auth))
            return
        self.authenticate_redirect()

    def _on_auth(self, user):
        if not user:
            raise tornado.web.HTTPError(500, "Google auth failed")
        # Save the user with, e.g., set_secure_cookie()

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
