from django.contrib.auth.models import User
from handlers import append_path
append_path()
from spread.views import SocialHandler
from forms import FriendSearch

class SearchHandler(SocialHandler):
    def get(self):
        if not self.authenticated(): return
        form = FriendSearch()
        return self.srender('search.html',form=form)
    def post(self):
        if not self.authenticated(): return
        name = self.parse_request(self.request.body)
        people = User.objects.all().filter(first_name=name)
        return self.srender('people.html',people=people)

class PeopleHandler(SocialHandler):
    def get(self):
        if not self.authenticated(): return
        people = User.objects.all()
        return self.srender('people.html',people=people)