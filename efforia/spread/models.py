from django.db.models import ForeignKey,TextField,DateTimeField,IntegerField,CharField,Model
from django.contrib.auth.models import User

class UserProfile(Model):
    user = ForeignKey(User,unique=True)
    points = IntegerField(default=0)
    age = IntegerField(default=0)
    
class UserRelation(Model):
    user = ForeignKey(User,related_name='user',)
    known = ForeignKey(User,related_name='known',)
    date = DateTimeField(auto_now_add=True)
    
class Spread(Model):
    user = ForeignKey(User)
    content = TextField()
    date = DateTimeField(auto_now_add=True)

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])

