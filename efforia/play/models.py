from django.db.models import ForeignKey,TextField,CharField,IntegerField,DateTimeField,Model
from django.contrib.auth.models import User
from datetime import date
import sys,os
path = os.path.abspath("efforia")
sys.path.append(path)

class Playable(Model):
    name = CharField(default='',max_length=150)
    user = ForeignKey(User,related_name='+')
    category = IntegerField(default=1)
    description = TextField()
    token = CharField(max_length=20)
    credit = IntegerField(default=0)
    visual = CharField(default='',max_length=40)
    date = DateTimeField(default=date.today(),auto_now_add=True)
    
class Schedule(Model):
    name = CharField(default='',max_length=50)
    user = ForeignKey(User,related_name='+')
    play = ForeignKey(Playable,related_name='+')
    date = DateTimeField(default=date.today(),auto_now_add=True)

class ScheduleFollow(Model):
    follow = ForeignKey(Schedule,related_name='+')
    user = ForeignKey(User,related_name='+')
    date = DateTimeField(default=date.today(),auto_now_add=True)

class PlayableFan(Model):
    fan = ForeignKey(Playable,related_name='+')
    user = ForeignKey(User,related_name='+')
    date = DateTimeField(auto_now_add=True)
