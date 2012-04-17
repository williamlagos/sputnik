from django.db.models import ForeignKey,TextField,CharField,DateTimeField,Model
from django.contrib.auth.models import User
    
class UserRelation(Model):
    user = ForeignKey(User,related_name='user',)
    known = ForeignKey(User,related_name='known',)
    date = DateTimeField(auto_now_add=True)
    
class Spreadable(Model):
    user = ForeignKey(User)
    content = TextField()
    date = DateTimeField(auto_now_add=True)
    
class Causable(Model):
    user = ForeignKey(User)
    title = CharField(max_length=100)
    content = TextField()
    video = TextField()
    date = DateTimeField(auto_now_add=True)
    

