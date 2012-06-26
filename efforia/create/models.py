from django.db.models import ForeignKey,CharField,TextField,DateTimeField,Model
from django.contrib.auth.models import User
from datetime import date

from play.models import Playable
from spread.models import Spreadable

class Causable(Model):
    name = CharField(default='',max_length=50)
    user = ForeignKey(User)
    play = ForeignKey(Playable)
    content = TextField(default='')
    date = DateTimeField(auto_now_add=True)
    
class Movement(Model):
    name = CharField(max_length=50)
    user = ForeignKey(User,related_name='+')
    cause = ForeignKey(Causable,related_name='+')
    date = DateTimeField(auto_now_add=True)
    
class MovementFollow(Model):
    follow = ForeignKey(Movement,related_name='+')
    user = ForeignKey(User,related_name='+')
    date = DateTimeField(default=date.today(),auto_now_add=True)

class CausableSpread(Model):
    name = CharField(default='#',max_length=10)
    user = ForeignKey(User,related_name='+')
    spread = ForeignKey(Spreadable,related_name='+')
    spreaded = ForeignKey(Causable,related_name='+')
    date = DateTimeField(auto_now_add=True)

