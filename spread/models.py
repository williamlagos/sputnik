from django.db.models import ForeignKey,TextField,DateTimeField,Model,CharField
from django.contrib.auth.models import User
from datetime import date
    
class Spreadable(Model):
    name = CharField(default='',max_length=50)
    user = ForeignKey(User,related_name='+')
    content = TextField()
    spreaded = CharField(default='efforia',max_length=15)
    date = DateTimeField(auto_now_add=True)
    def name_trimmed(self): return self.name.split(';')[0][1:]
    def month(self): return self.date.month-1
    
class Event(Model):
    name = CharField(default='',max_length=50)
    user = ForeignKey(User,related_name='+')
    start_time = DateTimeField(default=date.today())
    end_time = DateTimeField(default=date.today())
    location = CharField(default='',max_length=100)
    id_event = CharField(default='',max_length=15)
    rsvp_status = CharField(default='',max_length=30)
    date = DateTimeField(default=date.today(),auto_now_add=True)
    def name_trimmed(self): return self.name.split(';')[0][1:]
    def month(self): return self.date.month-1

class EventSpread(Model):
    name = CharField(default='@$',max_length=10)
    user = ForeignKey(User,related_name='+')
    spread = ForeignKey(Spreadable,related_name='+')
    spreaded = ForeignKey(Event,related_name='+')
    date = DateTimeField(auto_now_add=True)
    def name_trimmed(self): return self.name.split(';')[0][1:]
    def month(self): return self.date.month-1

class SpreadableSpread(Model):
    name = CharField(default='@!',max_length=10)
    user = ForeignKey(User,related_name='+')
    spread = ForeignKey(Spreadable,related_name='+')
    spreaded = ForeignKey(Spreadable,related_name='+')
    date = DateTimeField(auto_now_add=True)
    def name_trimmed(self): return self.name.split(';')[0][1:]
    def month(self): return self.date.month-1
