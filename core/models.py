from django.db.models import *
from django.contrib.auth.models import User
from tornado import httpclient
from datetime import date

def user(name): return User.objects.filter(username=name)[0]

class Profile(Model):
    user = ForeignKey(User,unique=True)
    points = IntegerField(default=0)
    credit = IntegerField(default=0)
    visual = CharField(default="",max_length=30)
    birthday = DateTimeField(default=date.today())
    google_token = TextField(default="",max_length=120)
    twitter_token = TextField(default="",max_length=120)
    facebook_token = TextField(default="",max_length=120)
    first_turn = BooleanField(default=True)
    date = DateTimeField(default=date.today(),auto_now_add=True)
    def years_old(self): return datetime.timedelta(self.birthday,date.today)
    def token(self): return ''
    def get_username(self): return self.user.username
    def get_visual(self):
            if self.visual:
                client = httpclient.HTTPClient()
                response = client.fetch(self.visual)
                url = '%s?dl=1' % response.effective_url
            else: url = 'static/img/spin.png'
            return url
    
class Place(Model):
    name = CharField(default="",max_length=50)
    user = ForeignKey(User,unique=True)
    street = CharField(default="",max_length=100)
    city = CharField(default="",max_length=100)
    country = CharField(default="",max_length=50)
    latitude = DecimalField(max_digits=8, decimal_places=2)
    longitude = DecimalField(max_digits=8, decimal_places=2)
    date = DateTimeField(default=date.today(),auto_now_add=True)

class ProfileFan(Model):
    fan = ForeignKey(User,related_name="+")
    user = ForeignKey(User,related_name="+")
    date = DateTimeField(auto_now_add=True)

class PlaceFan(Model):
    fan = ForeignKey(User,related_name="+")
    user = ForeignKey(User,related_name="+")
    date = DateTimeField(auto_now_add=True)
    
Profile.year = property(lambda p: p.years_old())
User.profile = property(lambda u: Profile.objects.get_or_create(user=u)[0])
Profile.name = property(lambda p: p.get_username())
