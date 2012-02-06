from django.db.models import ForeignKey,TextField,DateTimeField,IntegerField,CharField,Model
from django.contrib.auth.models import User

class Spread(Model):
    user = ForeignKey(User)
    content = TextField()
    date = DateTimeField(auto_now_add=True)

class UserProfile(Model):
    user = ForeignKey(User,unique=True)
    points = IntegerField(default=0)
    age = IntegerField(default=0)
    
class UserFriend(Model):
    user = ForeignKey(User,related_name='user',unique=True)
    friend = ForeignKey(User,related_name='friend',unique=True)
    date = DateTimeField(auto_now_add=True)
    
User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])

