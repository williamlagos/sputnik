from django.db.models import ForeignKey,TextField,DateTimeField,Model,CharField
from django.contrib.auth.models import User
    
class Relation(Model):
    user = ForeignKey(User,related_name='+')
    known = ForeignKey(User,related_name='+')
    date = DateTimeField(auto_now_add=True)
    
class Spreadable(Model):
    name = CharField(default='',max_length=50)
    user = ForeignKey(User)
    content = TextField()
    date = DateTimeField(auto_now_add=True)
    

