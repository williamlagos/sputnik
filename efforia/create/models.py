from django.db.models import ForeignKey,CharField,TextField,DateTimeField,Model
from django.contrib.auth.models import User
from datetime import date

class Causable(Model):
    name = CharField(default='',max_length=50)
    user = ForeignKey(User)
    content = TextField()
    video = TextField()
    date = DateTimeField(auto_now_add=True)
    
class Movement(Model):
    name = CharField(max_length=50)
    user = ForeignKey(User,related_name='+')
    cause = ForeignKey(Causable,related_name='+')
    date = DateTimeField(auto_now_add=True)
    
class MovementBinding(Model):
    cause = ForeignKey(Movement,related_name='+')
    bind = ForeignKey(Movement,related_name='+')
    date = DateTimeField(default=date.today(),auto_now_add=True)