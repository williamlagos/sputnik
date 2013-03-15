from django.db.models import *
from django.contrib.auth.models import User
from tornado import httpclient
from datetime import date

locale = ('Jan','Fev','Mar','Abr','Mai','Jun','Jul','Ago','Set','Out','Nov','Dez')

def user(name): return User.objects.filter(username=name)[0]

class Profile(Model):
    user = ForeignKey(User,unique=True)
    points = IntegerField(default=0)
    credit = IntegerField(default=0)
    visual = CharField(default="",max_length=100)
    career = CharField(default='',max_length=50)
    birthday = DateTimeField(default=date.today())
    google_token = TextField(default="",max_length=120)
    twitter_token = TextField(default="",max_length=120)
    facebook_token = TextField(default="",max_length=120)
    bio = TextField(default='',max_length=140)
    interface = IntegerField(default=1)
    typeditor = IntegerField(default=1)
    monetize = IntegerField(default=0)
    language = IntegerField(default=0)
    date = DateTimeField(default=date.today(),auto_now_add=True)
    def years_old(self): return datetime.timedelta(self.birthday,date.today)
    def token(self): return ''
    def get_username(self): return self.user.username
    def month(self): return locale[self.date.month-1]
    
class Place(Model):
    name = CharField(default="",max_length=50)
    user = ForeignKey(User,unique=True)
    code = CharField(default="",max_length=100)
    city = CharField(default="",max_length=100)
    country = CharField(default="",max_length=50)
    date = DateTimeField(default=date.today(),auto_now_add=True)

class Followed(Model):
    followed = IntegerField(default=1)
    follower = IntegerField(default=2)
    date = DateTimeField(auto_now_add=True)
    
Profile.year = property(lambda p: p.years_old())
Profile.name = property(lambda p: p.get_username())
User.profile = property(lambda u: Profile.objects.get_or_create(user=u)[0])
User.place = property(lambda p: Place.objects.get_or_create(user=p)[0])
