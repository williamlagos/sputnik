from django.db.models import ForeignKey,TextField,DateTimeField,Model,CharField
from django.contrib.auth.models import User
from datetime import date
    
class Relation(Model):
    user = ForeignKey(User,related_name='+')
    known = ForeignKey(User,related_name='+')
    date = DateTimeField(auto_now_add=True)
    
class Spreadable(Model):
    name = CharField(default='',max_length=50)
    user = ForeignKey(User)
    content = TextField()
    spreaded = CharField(default='efforia',max_length=15)
    date = DateTimeField(auto_now_add=True)
    
class Event(Model):
    name = CharField(default="",max_length=50)
    user = ForeignKey(User,unique=True)
    start_time = DateTimeField(default=date.today())
    end_time = DateTimeField(default=date.today())
    location = CharField(default="",max_length=100)
    id_event = CharField(default="",max_length=15)
    rsvp_status = CharField(default="",max_length=30)
    date = DateTimeField(default=date.today(),auto_now_add=True)
