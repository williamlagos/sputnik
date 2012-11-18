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
    def initial(self): return self.name[len(object.name)-4:]
    def name_trimmed(self): return self.name.split(';')[0][1:]
    def trim(self): return object.name.replace(" ","")
    def month(self): return self.date.month-1
    
class Movement(Model):
    name = CharField(max_length=50)
    user = ForeignKey(User,related_name='+')
    cause = ForeignKey(Causable,related_name='+')
    date = DateTimeField(auto_now_add=True)
    def name_trimmed(self): return self.name.split(';')[0][1:]
    def month(self): return self.date.month-1

class CausableSpread(Model):
    name = CharField(default='@#',max_length=10)
    user = ForeignKey(User,related_name='+')
    spread = ForeignKey(Spreadable,related_name='+')
    spreaded = ForeignKey(Causable,related_name='+')
    date = DateTimeField(auto_now_add=True)
    def name_trimmed(self): return self.name.split(';')[0][1:]
    def month(self): return self.date.month-1

