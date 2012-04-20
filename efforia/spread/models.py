from django.db.models import ForeignKey,TextField,DateTimeField,Model
from django.contrib.auth.models import User
    
class UserRelation(Model):
    user = ForeignKey(User,related_name='+')
    known = ForeignKey(User,related_name='+')
    date = DateTimeField(auto_now_add=True)
    
class Spreadable(Model):
    user = ForeignKey(User)
    content = TextField()
    date = DateTimeField(auto_now_add=True)
    

