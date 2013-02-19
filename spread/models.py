from django.db.models import ForeignKey,TextField,CharField,IntegerField,DateTimeField,BooleanField,Model
from django.contrib.auth.models import User
from tornado import httpclient

from datetime import date
import sys,os
path = os.path.abspath("efforia")
sys.path.append(path)

locale = ('Jan','Fev','Mar','Abr','Mai','Jun','Jul','Ago','Set','Out','Nov','Dez')

class Spreadable(Model):
    name = CharField(default='',max_length=50)
    user = ForeignKey(User,related_name='+')
    content = TextField()
    spreaded = CharField(default='efforia',max_length=15)
    date = DateTimeField(auto_now_add=True)
    def token(self): return self.name[:1]
    def name_trimmed(self): return self.name.split(';')[0][1:]
    def month(self): return locale[self.date.month-1]
    
class Event(Model):
    name = CharField(default='@@',max_length=50)
    user = ForeignKey(User,related_name='+')
    start_time = DateTimeField(default=date.today())
    end_time = DateTimeField(default=date.today())
    location = CharField(default='',max_length=100)
    id_event = CharField(default='',max_length=15)
    rsvp_status = CharField(default='',max_length=30)
    date = DateTimeField(default=date.today(),auto_now_add=True)
    def token(self): return self.name[:2]
    def name_trimmed(self): return self.name.split(';')[0][1:]
    def month(self): return locale[self.date.month-1]

class EventSpread(Model):
    name = CharField(default='@$',max_length=10)
    user = ForeignKey(User,related_name='+')
    spread = ForeignKey(Spreadable,related_name='+')
    spreaded = ForeignKey(Event,related_name='+')
    date = DateTimeField(auto_now_add=True)
    def token(self): return self.name[:2]
    def name_trimmed(self): return self.name.split(';')[0][1:]
    def month(self): return locale[self.date.month-1]

class SpreadableSpread(Model):
    name = CharField(default='@!',max_length=10)
    user = ForeignKey(User,related_name='+')
    spread = ForeignKey(Spreadable,related_name='+')
    spreaded = ForeignKey(Spreadable,related_name='+')
    date = DateTimeField(auto_now_add=True)
    def token(self): return self.name[:2]
    def content_trimmed(self): return self.spreaded.content[:20]
    def name_trimmed(self): return self.name.split(';')[0][1:]
    def month(self): return locale[self.date.month-1]

class Playable(Model):
    name = CharField(default='',max_length=150)
    user = ForeignKey(User,related_name='+')
    category = IntegerField(default=1)
    description = TextField()
    token = CharField(max_length=20)
    credit = IntegerField(default=0)
    visual = CharField(default='',max_length=40)
    date = DateTimeField(default=date.today(),auto_now_add=True)
    def etoken(self): return self.name[:1]
    def name_trimmed(self): return self.name.split(';')[0][1:]
    def month(self): return locale[self.date.month-1]
    def date_formatted(self): return self.date.strftime('%Y-%m-%d %H:%M:%S.%f')
    
class Schedule(Model):
    name = CharField(default='',max_length=50)
    user = ForeignKey(User,related_name='+')
    play = ForeignKey(Playable,related_name='+')
    date = DateTimeField(default=date.today(),auto_now_add=True)
    def token(self): return self.name[:2]
    def name_trimmed(self): return self.name.split(';')[0][1:]
    def month(self): return locale[self.date.month-1]
    
class PlayablePurchased(Model):
    name = CharField(default='$>',max_length=10)
    owner = ForeignKey(User,related_name='owner')
    video = ForeignKey(Playable,related_name='video')
    date = DateTimeField(auto_now_add=True)
    def token(self): return self.name[:2]
    def name_trimmed(self): return self.name.split(';')[0][1:]
    def month(self): return locale[self.date.month-1]

class PlayableFan(Model):
    fan = ForeignKey(Playable,related_name='+')
    user = ForeignKey(User,related_name='+')
    date = DateTimeField(auto_now_add=True)
    def token(self): return self.name[:2]
    def name_trimmed(self): return self.name.split(';')[0][1:]
    def month(self): return locale[self.date.month-1]

class Page(Model):
    name = CharField(default='!#',max_length=10)
    content = TextField(default='')
    user = ForeignKey(User,related_name='+')
    date = DateTimeField(auto_now_add=True)
    def token(self): return self.name[:2]
    def name_trimmed(self): return self.name.split(';')[0][1:]
    def month(self): return locale[self.date.month-1]
    
class Image(Model):
    name = CharField(default='!%',max_length=10)
    link = CharField(default='',max_length=100)
    user = ForeignKey(User,related_name='+')
    date = DateTimeField(auto_now_add=True)
    def token(self): return self.name[:2]
    def name_trimmed(self): return self.name.split(';')[0][1:]
    def month(self): return locale[self.date.month-1]
    def visual(self):
        client = httpclient.HTTPClient()
        response = client.fetch(self.visual)
        url = '%s?dl=1' % response.effective_url
        return url