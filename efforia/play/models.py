from django.db.models import ForeignKey,TextField,CharField,DateTimeField,Model
from django.contrib.auth.models import User
import sys,os
path = os.path.abspath("efforia")
sys.path.append(path)

from spread.models import Causable

class Playable(Model):
    user = ForeignKey(User,related_name='+')
    title = CharField(max_length=50)
    description = TextField()
    token = CharField(max_length=20)
    date = DateTimeField(auto_now_add=True)
    

class PlaySchedule(Model):
    user = ForeignKey(User,related_name='+')
    play = ForeignKey(Playable,related_name='+')
    name = CharField(max_length=50)
    date = DateTimeField(auto_now_add=True)
    
class CauseSchedule(Model):
    user = ForeignKey(User,related_name='+')
    cause = ForeignKey(Causable,related_name='+')
    name = CharField(max_length=50)
    date = DateTimeField(auto_now_add=True)
    
class CauseSchedBinding(Model):
    cause = ForeignKey(Causable,related_name='+')
    bind = ForeignKey(Causable,related_name='+')

class PlaySchedBinding(Model):
    play = ForeignKey(Causable,related_name='+')
    bind = ForeignKey(Causable,related_name='+')
    