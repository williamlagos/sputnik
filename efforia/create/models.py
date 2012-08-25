from django.db.models import ForeignKey,CharField,TextField,DateTimeField,IntegerField,Model
from django.contrib.auth.models import User
from datetime import date

from play.models import Playable
from spread.models import Spreadable

class Causable(Model):
    name = CharField(default='',max_length=50)
    user = ForeignKey(User)
    start_time = DateTimeField(default=date.today())
    end_time = DateTimeField(default=date.today())
    play = ForeignKey(Playable)
    content = TextField(default='')
    credit = IntegerField(default=0)
    date = DateTimeField(auto_now_add=True)
    
class Movement(Model):
    name = CharField(max_length=50)
    user = ForeignKey(User,related_name='+')
    cause = ForeignKey(Causable,related_name='+')
    date = DateTimeField(auto_now_add=True)

class CausableDonated(Model):
    name = CharField(default='$#',max_length=10)
    value = IntegerField(default=1)
    donator = ForeignKey(User,related_name='donator')
    cause = ForeignKey(Causable,related_name='cause')
    date = DateTimeField(auto_now_add=True)

class CausableSpread(Model):
    name = CharField(default='@#',max_length=10)
    user = ForeignKey(User,related_name='+')
    spread = ForeignKey(Spreadable,related_name='+')
    spreaded = ForeignKey(Causable,related_name='+')
    date = DateTimeField(auto_now_add=True)

